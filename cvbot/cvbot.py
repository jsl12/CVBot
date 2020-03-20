import logging
import re

import discord

from . import load, utils

logger = logging.getLogger(__name__)

class CoronaVirusBot:
    REGEX = re.compile(f'(corona|virus)', re.IGNORECASE)
    STAT_REGEX = re.compile(f'#([\w ,]+)-(deaths|cases|recovered)')
    COMPARE_REGEX = re.compile(f'^#compare', re.IGNORECASE)
    DOUBLE_REGEX = re.compile(f'^#double-([\w ]+)', re.IGNORECASE)

    def __init__(self):
        self.client = discord.Client()
        return

    def run(self, apikey: str):
        self.client.run(apikey)

    def process_message(self, msg: discord.Message):
        match = self.STAT_REGEX.search(msg.content)
        c_match = self.COMPARE_REGEX.search(msg.content)
        d_match = self.DOUBLE_REGEX.search(msg.content)

        if match is not None:
            if match.group(2) == 'deaths':
                stats = load.death_stats()
            elif match.group(2) == 'cases':
                stats = load.confirmed_stats()
            elif match.group(2) == 'recovered':
                stats = load.recovered_stats()

            if msg.content[-6:] == 'series':
                try:
                    stats = stats[match.group(1)].sum(axis=1)
                    stats = stats[stats > 0]
                    return str(stats)[-2000:]
                except Exception as e:
                    logger.warning(f'Invalid key: {match.group(1)}')
                    return

            try:
                stats = stats[match.group(1)]
            except KeyError as e:
                logging.info(f'trying to parse {match.group(1)} as a US state')

                try:
                    stats = stats['US'][match.group(1)]
                except KeyError as e:
                    logger.warning(f'Invalid key: {match.group(1)}')
                else:
                    return f'{stats.max().sum()}'
            else:
                return f'{stats.max().sum()}'

        elif c_match is not None:
            res = utils.compare(load.confirmed_stats(), msg.content[9:].split('-'))
            res.index = res.index.to_series().apply(lambda t: f'{t.days} days')
            return utils.df_to_str(res, 2)

        elif d_match is not None:
            res = utils.double_period(load.confirmed_stats()[d_match.group(1)].apply(sum, axis=1))
            return str(res)
