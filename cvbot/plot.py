import matplotlib.pyplot as plt
import pandas as pd

def cv_plot(df: pd.DataFrame, base_size: int = 5) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(base_size*(19.2/10.8), base_size))
    ax.plot(df)
    ax.set_xlim(0, df.index[-1])
    ax.legend(df.columns)
    ax.grid(True)
    return fig
