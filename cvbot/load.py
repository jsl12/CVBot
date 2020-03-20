import io
import logging

import pandas as pd
import requests

logger = logging.getLogger(__name__)

def death_stats() -> pd.DataFrame:
    return git_csv_to_df(
        r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
    )

def confirmed_stats() -> pd.DataFrame:
    return git_csv_to_df(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    )

def git_csv_to_df(url: str, index_col=['Country/Region', 'Province/State', 'Lat', 'Long']) -> pd.DataFrame:
    logger.info(f'converting to DataFrame: {url}')
    res = pd.read_csv(io.BytesIO(requests.get(url).content), index_col=index_col).transpose()
    res.index = pd.to_datetime(res.index)
    return res


if __name__ == '__main__':
    df = death_stats()
    pass