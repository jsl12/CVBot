import logging

import discord
import pandas as pd

from .parser import CV_PARSER
from .utils import parse_report

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
            else:
                res = parse_report(msg.content)

                res.index = res.index.to_series().dt.to_pydatetime().apply(lambda dt: dt.strfteim('%m-%d'))

                # drop rows until the result can fit within the 2000 limit Discord has on messages
                while len(str(res)) > 2000:
                    res = res.iloc[1:]

                return str(res)
