import re
from typing import Dict

import pandas as pd
from ncnc.logging import logger
from tqdm import tqdm


def calc_nc_value(df: pd.DataFrame, n: int = 100) -> pd.DataFrame:
    logger.info('started setting df["nc-value"]')
    context_to_weight = _extract_context(df, n)
    df["nc-value"] = [
        _calc_nc_value(df, ngram, context_to_weight) for ngram in tqdm(df.index)
    ]
    return df


def _extract_context(df: pd.DataFrame, n: int = 100) -> Dict[str, float]:
    context_to_weight: Dict[str, float] = {}

    n = min(n, len(df))

    # use the top candidate terms from the C-value list as pseudo real terms (see 3.4 in the paper)
    df = df.sort_values(by="c-value", ascending=False)[:n]

    # ngram => "basal cell carcinoma"
    # longer_ngrams => ["adenoid cystic basal cell carcinoma", ...]
    for ngram, longer_ngrams in zip(df.index, df["longer ngrams"]):
        if len(longer_ngrams) == 0:
            continue

        precede_contexts = set()
        follow_contexts = set()

        pattern = re.compile(r"^({} )|( {} )|( {})$".format(ngram, ngram, ngram))

        # longer_ngram => "adenoid cystic basal cell carcinoma"
        for longer_ngram in longer_ngrams:
            # => "adenoid cystic [term]"
            longer_ngram = pattern.sub(replaced_string, longer_ngram)

            # => ["adenoid", "cystic", "[term]"]
            context_words = longer_ngram.split()

            # => 2
            term_index = context_words.index("[term]")

            # => "cystic [term]"
            context = " ".join(context_words[term_index - 1 : term_index + 1])
            if context != "" and context != "[term]":
                precede_contexts.add(context)

            # => "[term] xxx" (if any)
            context = " ".join(context_words[term_index : term_index + 2])
            if context != "" and context != "[term]":
                follow_contexts.add(context)

        for context in precede_contexts:
            context_to_weight.setdefault(context, 0.0)
            context_to_weight[context] += 1 / n

        for context in follow_contexts:
            context_to_weight.setdefault(context, 0.0)
            context_to_weight[context] += 1 / n

    # => {"cystic [term]": 0.xxx, ...}
    return context_to_weight


def replaced_string(match: re.Match) -> str:
    if not match.group(0).startswith(" "):
        return "[term] "
    elif not match.group(0).endswith(" "):
        return " [term]"
    else:
        return " [term] "


def _calc_nc_value(
    df: pd.DataFrame, ngram: str, context_to_weight: Dict[str, float]
) -> float:
    total_weight = 0.0

    for context, weight in context_to_weight.items():
        longer_ngram = context.replace("[term]", ngram)
        for _longer_ngram in df.loc[ngram]["longer ngrams"]:
            if longer_ngram in _longer_ngram:
                total_weight += df.loc[_longer_ngram]["f(a)"] * weight

    nc_value: float = 0.8 * df.loc[ngram]["c-value"] + 0.2 * total_weight
    return nc_value
