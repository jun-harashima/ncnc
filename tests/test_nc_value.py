import pandas as pd
from ncnc.c_value import calc_c_value
from ncnc.nc_value import _extract_context, calc_nc_value
from pandas.testing import assert_series_equal


def test_calc_nc_value() -> None:
    df = pd.read_csv("tests/sample.csv", index_col=0)
    df = calc_c_value(df)
    df = calc_nc_value(df)
    s = pd.Series(
        {
            "adenoid cystic basal cell carcinoma": 0.8
            * df.loc["adenoid cystic basal cell carcinoma"]["c-value"]
            + 0.2 * 0,
            "cystic basal cell carcinoma": 0.8
            * df.loc["cystic basal cell carcinoma"]["c-value"]
            + 0.2
            * (
                # adenoid [term]
                df.loc["adenoid cystic basal cell carcinoma"]["f(a)"]
                * 0.16666666666666666
            ),
            "ulcerated basal cell carcinoma": 0.8
            * df.loc["ulcerated basal cell carcinoma"]["c-value"]
            + 0.2 * 0,
            "recurrent basal cell carcinoma": 0.8
            * df.loc["recurrent basal cell carcinoma"]["c-value"]
            + 0.2 * 0,
            "circumscribed basal cell carcinoma": 0.8
            * df.loc["circumscribed basal cell carcinoma"]["c-value"]
            + 0.2 * 0,
            "basal cell carcinoma": 0.8 * df.loc["basal cell carcinoma"]["c-value"]
            + 0.2
            * (
                # cystic [term]
                df.loc["adenoid cystic basal cell carcinoma"]["f(a)"]
                * 0.16666666666666666
                + df.loc["cystic basal cell carcinoma"]["f(a)"] * 0.16666666666666666
                # ulcerated [term]
                + df.loc["ulcerated basal cell carcinoma"]["f(a)"] * 0.16666666666666666
                # recurrent [term]
                + df.loc["recurrent basal cell carcinoma"]["f(a)"] * 0.16666666666666666
                # circumscribed [term]
                + df.loc["circumscribed basal cell carcinoma"]["f(a)"]
                * 0.16666666666666666
            ),
        },
        name="nc-value",
    )
    s.index.name = "ngram"
    assert_series_equal(df["nc-value"], s)


def test__extract_context() -> None:
    df = pd.DataFrame(
        {
            "longer ngrams": [
                ["aa bb", "cc aa bb", "dd aa"],
                ["cc aa bb"],
                [],
                [],
            ],
            "c-value": [0.2, 0.3, 0.5, 0.4],
        },
        index=["aa", "aa bb", "cc aa bb", "dd aa"],
    )
    context_to_weight = _extract_context(df)
    assert context_to_weight == {
        "cc [term]": 0.50,
        "[term] bb": 0.25,
        "dd [term]": 0.25,
    }

    df = pd.read_csv("tests/sample.csv", index_col=0)
    df = calc_c_value(df)
    context_to_weight = _extract_context(df)
    assert context_to_weight == {
        "adenoid [term]": 0.16666666666666666,
        "cystic [term]": 0.16666666666666666,
        "ulcerated [term]": 0.16666666666666666,
        "recurrent [term]": 0.16666666666666666,
        "circumscribed [term]": 0.16666666666666666,
    }
