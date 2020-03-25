import logging
from datetime import timedelta
from typing import List

import pandas as pd

from .load.constants import states
from .load.series import load_all
from .parser import parse_args_shlex, CV_PARSER
from .plot import cv_plot

logger = logging.getLogger(__name__)


def parse_report(input_str: str) -> pd.DataFrame:
    """
    Wrapper for report() that parses an string of arguments with shlex.split()

    :param input_str:
    :param skip:
    :return:
    """
    args = parse_args_shlex(CV_PARSER, input_str)
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
    df = load_all(preserve_region=False)

    try:
        res = df.loc[:, pd.IndexSlice[command, places]].applymap(int)
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


def normalize_index(df: pd.DataFrame, threshold: int = 0):
    data = {col: trim_start(df[col], threshold) for col in df.columns}
    data = {col: data[col].set_axis(data[col].index.to_series().apply(lambda d: (d - data[col].index[0]).days).values) for col in data}
    res = pd.DataFrame(data)
    res.index = res.index.to_series().apply(lambda d: timedelta(days=d))
    return res


def trim_start(s: pd.Series, threshold: int = 0):
    return s[s > threshold]


def filter_us_states(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Groups the US states together and sums

    :param df:
    :return:
    '''
    df = df.groupby(by=lambda i: i.split(', ')[-1] if ', ' in i else i, level='Region', axis=1).sum()
    df = pd.DataFrame({abb: df.filter(regex=f'{name}|{abb}').sum(axis=1) for abb, name in states.items()})
    return df
