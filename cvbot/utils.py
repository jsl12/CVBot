import numpy as np
import pandas as pd


def compare(df: pd.DataFrame, indices, all=False):
    res = pd.DataFrame(data={s.index.name: s for s in [convert(df, i) for i in indices]})
    if not all:
        res = res.dropna().astype(np.dtype('int64'))
    return res


def convert(df: pd.DataFrame, index: str):
    res = df[index].apply(sum, axis=1)
    res = res[res > 0]
    res.index = res.index.to_series().apply(lambda d: d - res.index[0])
    res.index.name = index
    return res


def df_to_str(df: pd.DataFrame, padding=2) -> str:
    col_widths = [len(str(df.index.name)) + padding] + [s + padding for s in col_sizes(df)]
    res = ''.rjust(col_widths[0])
    for i, width in enumerate(col_widths[1:]):
        res += str(df.columns[i]).rjust(width)
    res += '\n'
    for i, row in df.iterrows():
        res += str(i).rjust(col_widths[0])
        for col, val in row.items():
            res += f'{val:.0f}'.rjust(col_widths[row.index.get_loc(col)+1])
        res += '\n'
    return res


def col_sizes(df: pd.DataFrame):
    return [
        len(str(i)) if len(str(i)) > val else val
        for i, val
        in df.applymap(lambda val: len(f'{val:.0f}')).max().iteritems()
    ]