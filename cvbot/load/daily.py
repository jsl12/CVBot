import io
import logging
import re
from datetime import datetime
from typing import List

import pandas as pd
import requests

logger = logging.getLogger(__name__)


def load_dates(dates: List[datetime], place_cols: List[str] = ['Country', 'Region', 'Admin2']):
    df = pd.concat([load_date(d) for d in dates])

    logger.info('Setting index')
    res = df.set_index(place_cols + ['Date'])

    logger.info('Removing duplicated indices')
    res = res[~res.index.duplicated(keep='last')]

    logger.info('Unstacking MultiIndex')
    res = res.unstack(level=place_cols)

    logger.info(f'Filling in values')
    res = res.fillna(method='pad').fillna(0)

    if not res.columns.is_lexsorted():
        res = res.transpose().sort_index().transpose()

    return res


def load_date(date:datetime):
    logger.info(f'loading {date.strftime("%Y-%m-%d")}')
    url = form_url(date)
    res = pd.read_csv(io.BytesIO(requests.get(url).content))

    date_col = res.filter(regex=re.compile('update', re.IGNORECASE)).columns[0]
    country_col = res.filter(regex=re.compile('country', re.IGNORECASE)).columns[0]
    state_col = res.filter(regex=re.compile('state', re.IGNORECASE)).columns[0]

    res = res.rename(
        {
            date_col: 'Date',
            country_col: 'Country',
            state_col: 'Region'
        },
        axis=1
    )

    res['Date'] = pd.to_datetime(res['Date'])
    # res = res.set_index(['Date'])
    return res


def form_url(date: datetime) -> str:
    return f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date.strftime("%m-%d-%Y")}.csv'
