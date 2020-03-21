import logging

import discord
import pandas as pd

from . import load, utils
from .parser import CV_PARSER, parse_args

logger = logging.getLogger(__name__)

class CoronaVirusBot:
    def __init__(self):
        self.client = discord.Client()
        return

    def run(self, apikey: str):
        self.client.run(apikey)

    def process_message(self, msg: discord.Message):
        if self.client.user in msg.mentions and msg.content[0] == '<':
            if ('-h' in msg.content) or ('--help' in msg.content):
                return CV_PARSER.format_help()

            try:
                args = parse_args(CV_PARSER, msg.content, skip=1)
            except Exception as e:
                return repr(e)
            else:
                CMD_MAP = {
                    'cases': load.confirmed_stats,
                    'deaths': load.death_stats,
                    'recovered': load.recovered_stats
                }
                df = CMD_MAP[args.command]()

                if args.compare:
                    places = [args.country] + args.compare
                else:
                    places = [args.country]

                try:
                    res = df[places].groupby(level=0, axis=1).sum()
                except KeyError as e:
                    logger.info(f'trying to parse {args.country} as a US state')
                    try:
                        res = df['US'][args.country].iloc[:,0]
                    except KeyError as e:
                        return repr(e)

                if args.double:
                    res = utils.double_period(res)
                elif not args.series:
                    return ' '.join(res.iloc[-1].apply(lambda v: str(int(v)) if not pd.isnull(v) else '').values.tolist())

                # remove rows of all 0s
                res = res[~res.apply(lambda row: (row == 0).all(), axis=1)]

                # drop rows until the result can fit within the 2000 limit Discord has on messages
                while len(str(res)) > 2000:
                    res = res.iloc[1:]

                return str(res)
