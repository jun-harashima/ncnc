import math
import re
from typing import List

import pandas as pd
from ncnc.logging import logger
from tqdm import tqdm


def calc_c_value(df: pd.DataFrame) -> pd.DataFrame:
    ngrams = df.index.values

    logger.info('started setting df["|a|"]')
    df["|a|"] = [len(ngram.split()) for ngram in tqdm(ngrams)]

    logger.info('started setting df["longer ngrams"]')
    df["longer ngrams"] = [_get_longer_ngrams(ngrams, ngram) for ngram in tqdm(ngrams)]

    # number of longer ngrams that contain the ngram
    logger.info('started setting df["c(a)"]')
    df["c(a)"] = [len(df.loc[ngram]["longer ngrams"]) for ngram in tqdm(ngrams)]

    # total frequency of the longer ngrams
    logger.info('started setting df["t(a)"]')
    df["t(a)"] = [_calc_t(df, ngram) for ngram in tqdm(ngrams)]

    logger.info('started setting df["c-value"]')
    df["c-value"] = [_calc_c_value(df.loc[ngram]) for ngram in tqdm(ngrams)]

    return df


def _get_longer_ngrams(ngrams: List[str], ngram: str) -> List[str]:
    ngram = re.escape(ngram)
    pattern = re.compile(r"(?:^{} | {} | {}$)".format(ngram, ngram, ngram))

    longer_ngrams = []
    for _ngram in ngrams:
        if pattern.search(_ngram) is not None:
            if _ngram not in longer_ngrams:
                longer_ngrams.append(_ngram)

    return longer_ngrams


def _calc_t(df: pd.DataFrame, ngram: str) -> int:
    row = df.loc[ngram]

    # total frequency of longer ngrams of the ngram
    _df = df.loc[row["longer ngrams"]]
    t1: int = _df["f(a)"].sum()

    # total frequency of longer ngrams of longer ngrams of the ngram
    ngrams: List[str] = sum(_df["longer ngrams"].tolist(), [])
    t2: int = df.loc[ngrams]["f(a)"].sum()

    return t1 - t2


def _calc_c_value(row: pd.Series) -> float:
    c_value: float = 0.0
    try:
        if row["c(a)"] == 0:
            c_value = math.log2(row["|a|"]) * row["f(a)"]
        else:
            c_value = math.log2(row["|a|"]) * (
                row["f(a)"] - 1 / row["c(a)"] * row["t(a)"]
            )
    except ValueError:
        logger.warning(f"the following row could not be preprocessed:\n {row}")

    return c_value
