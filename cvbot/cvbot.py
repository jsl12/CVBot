import logging

import discord

from . import load
from .parser import CV_PARSER

logger = logging.getLogger(__name__)

class CoronaVirusBot:
    def __init__(self):
        self.client = discord.Client()
        return

    def run(self, apikey: str):
        self.client.run(apikey)

    def process_message(self, msg: discord.Message):
        if self.client.user in msg.mentions:
            try:
                args = CV_PARSER.parse_args(msg.content.split(' ')[1:])
            except Exception as e:
                return repr(e)
            else:
                CMD_MAP = {
                    'cases': load.confirmed_stats,
                    'deaths': load.death_stats,
                    'recovered': load.recovered_stats
                }
                df = CMD_MAP[args.command]()

                try:
                    res = df[args.country].sum(axis=1)
                except KeyError as e:
                    return repr(e)

                if args.series:
                    return str(res)
                else:
                    return res.values[-1]
