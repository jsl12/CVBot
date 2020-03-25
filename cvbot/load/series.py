import io
import logging

import pandas as pd
import requests

logger = logging.getLogger(__name__)


def load_all(preserve_region: bool = False) -> pd.DataFrame:
    df = pd.concat(
        objs=[f() for f in CMD_MAP.values()],
        keys=CMD_MAP.keys(),
        names=['type'],
        axis=1,
        sort=True
    )
    # this is needed to make df.is_lexsorted() True, which enables slicing the MultiIndex without a warning
    df = df.transpose().sort_index().transpose()

    if not preserve_region:
        df = df.groupby(level=['type', 'Country'], axis=1).sum()

    return df


def git_csv_to_df(url: str, index_col=['Country/Region', 'Province/State', 'Lat', 'Long']) -> pd.DataFrame:
    logger.info(f'converting to DataFrame: {url}')
    res = pd.read_csv(io.BytesIO(requests.get(url).content), index_col=index_col).transpose()
    res.index = pd.to_datetime(res.index)
    res.columns = res.columns.droplevel(index_col[-2:])
    res = res.transpose().sort_index().transpose()
    res.columns.names = ['Country', 'Region']
    return res


def death_stats() -> pd.DataFrame:
    return git_csv_to_df(
        r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    )


def confirmed_stats() -> pd.DataFrame:
    return git_csv_to_df(
        r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    )


def recovered_stats() -> pd.DataFrame:
    return git_csv_to_df(
        r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'
    )


CMD_MAP = {
    'cases': confirmed_stats,
    'deaths': death_stats,
    # 'recovered': recovered_stats
}