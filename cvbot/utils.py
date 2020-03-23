import logging
from datetime import timedelta
from typing import List

import pandas as pd

from .load import CMD_MAP
from .parser import parse_args_shlex, CV_PARSER
from .plot import cv_plot

logger = logging.getLogger(__name__)


def parse_report(input_str: str, skip=1) -> pd.DataFrame:
    args = parse_args_shlex(CV_PARSER, input_str, skip=skip)
    return report(
        places=args.places,
        command=args.command,
        double=args.double,
        series=args.series,
        normalize=args.normalize,
        plot=args.plot
    )


def report(
        places: List[str],
        command: str,
        double: bool = False,
        series: bool = False,
        normalize: bool = False,
        plot: bool = False
) -> pd.DataFrame:
    df = CMD_MAP[command]()

    try:
        res = df[places].groupby(level=0, axis=1).sum()
        res = res[~res.apply(lambda row: (row == 0).all(), axis=1)]
    except KeyError as e:
        logger.info(f'Invalid key(s) {[p for p in places if p not in df.columns]}')

    if normalize:
        res = normalize_index(res)
        res.index = res.index.to_series().apply(lambda v: v.days)
        series = True

    if double:
        res = double_period(res)
        series = True

    if plot:
        return cv_plot(res)

    if not series:
        res = pd.DataFrame(
            data=[res.iloc[-1]],
            index=[res.index[-1]],
            columns=places
        )

    return res


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


def normalize_index(df: pd.DataFrame):
    data = {col: trim_start(df[col]) for col in df.columns}
    data = {col: data[col].set_axis(data[col].index.to_series().apply(lambda d: (d - data[col].index[0]).days).values) for col in data}
    res = pd.DataFrame(data)
    res.index = res.index.to_series().apply(lambda d: timedelta(days=d))
    return res


def trim_start(s: pd.Series, threshold: int = 0):
    return s[s > threshold]
