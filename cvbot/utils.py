import logging
from typing import List

import pandas as pd

from . import load
from .parser import parse_args_shlex, CV_PARSER

logger = logging.getLogger(__name__)


def double_period(df: pd.DataFrame) -> pd.DataFrame:
    def last_half(s: pd.Series, val, date):
        try:
            last_date = s[s < (val / 2)].index[-1]
        except IndexError:
            return 0
        return (date - last_date).days

    res = pd.DataFrame(
        data={col: [last_half(df[col], val, date) for date, val in df[col].iteritems()] for col in df.columns},
        index=df.index
    )
    return res


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
        res = double_period(res)
    elif not series:
        return ' '.join(res.iloc[-1].apply(lambda v: str(int(v)) if not pd.isnull(v) else '').values.tolist())

    # remove rows of all 0s
    res = res[~res.apply(lambda row: (row == 0).all(), axis=1)]

    return res
