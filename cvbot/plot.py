import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def cv_plot(df: pd.DataFrame, base_size: int = 5) -> plt.Figure:
    if isinstance(df.index, pd.TimedeltaIndex):
        df.index = df.index.to_series().apply(lambda v: v.days)

    fig, ax = plt.subplots(figsize=(base_size*(19.2/10.8), base_size))
    ax.plot(df)
    ax.set_xlim(df.index[0], df.index[-1])
    ax.legend(df.columns)
    ax.grid(True)

    if isinstance(df.index, pd.DatetimeIndex):
        # locator = mdates.AutoDateLocator(minticks=3, maxticks=10)
        locator = mdates.WeekdayLocator(mdates.SUNDAY)
        formatter = mdates.DateFormatter('%m-%d')
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)

    return fig
