import logging
from typing import List

import discord
import pandas as pd

from . import load, utils
from .parser import CV_PARSER, parse_args_shlex

logger = logging.getLogger(__name__)


def parse_report(input_str: str, skip=1):
    args = parse_args_shlex(CV_PARSER, input_str, skip=skip)
    return report(
        places=args.places,
        command=args.command,
        double=args.double,
        series=args.series
    )


def report(places: List[str], command: str, double: bool, series: bool):
    CMD_MAP = {
        'cases': load.confirmed_stats,
        'deaths': load.death_stats,
        'recovered': load.recovered_stats
    }
    df = CMD_MAP[command]()

    try:
        res = df[places].groupby(level=0, axis=1).sum()
    except KeyError as e:
        logger.info(f'Invalid key(s) {[p for p in places if p not in df.columns]}')

    if double:
        res = utils.double_period(res)
    elif not series:
        return ' '.join(res.iloc[-1].apply(lambda v: str(int(v)) if not pd.isnull(v) else '').values.tolist())

    # remove rows of all 0s
    res = res[~res.apply(lambda row: (row == 0).all(), axis=1)]

    return res


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

                # drop rows until the result can fit within the 2000 limit Discord has on messages
                while len(str(res)) > 2000:
                    res = res.iloc[1:]

                return str(res)
