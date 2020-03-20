import logging
import re

import discord

from . import load

logger = logging.getLogger(__name__)

class CoronaVirusBot:
    REGEX = re.compile(f'(corona|virus)', re.IGNORECASE)
    STAT_REGEX = re.compile(f'#([\w ]+)-(deaths|cases|recovered)')

    def __init__(self):
        self.client = discord.Client()
        return

    def run(self, apikey: str):
        self.client.run(apikey)

    def process_message(self, msg: discord.Message):
        m = self.STAT_REGEX.search(msg.content)
        if m is not None:
            if m.group(2) == 'deaths':
                stats = load.death_stats()
            elif m.group(2) == 'cases':
                stats = load.confirmed_stats()
            elif m.group(2) == 'recovered':
                stats = load.recovered_stats()

            try:
                stats = stats[m.group(1)]
            except KeyError as e:
                logging.info(f'trying to parse {m.group(1)} as a US state')

                try:
                    stats = stats['US'][m.group(1)]
                except KeyError as e:
                    logger.warning(f'Invalid key: {m.group(1)}')
                else:
                    return f'{stats.max().sum()}'
            else:
                return f'{stats.max().sum()}'
