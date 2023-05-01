import pandas as pd
from ncnc.c_value import _get_longer_ngrams, calc_c_value
from pandas.testing import assert_frame_equal


def test_calc_c_value() -> None:
    input_df = pd.read_csv("tests/sample.csv", index_col=0)
    output_df = calc_c_value(input_df)
    expected_df = pd.DataFrame(
        {
            "f(a)": [5, 11, 7, 5, 3, 984],
            "|a|": [5, 4, 4, 4, 4, 3],
            "longer ngrams": [
                [],
                ["adenoid cystic basal cell carcinoma"],
                [],
                [],
                [],
                [
                    "adenoid cystic basal cell carcinoma",
                    "cystic basal cell carcinoma",
                    "ulcerated basal cell carcinoma",
                    "recurrent basal cell carcinoma",
                    "circumscribed basal cell carcinoma",
                ],
            ],
            "c(a)": [0, 1, 0, 0, 0, 5],
            "t(a)": [0, 5, 0, 0, 0, 26],
            "c-value": [11.609640, 12, 14, 10, 6, 1551.361296],
        },
        index=[
            "adenoid cystic basal cell carcinoma",
            "cystic basal cell carcinoma",
            "ulcerated basal cell carcinoma",
            "recurrent basal cell carcinoma",
            "circumscribed basal cell carcinoma",
            "basal cell carcinoma",
        ],
    )
    expected_df.index.name = "ngram"
    assert_frame_equal(output_df, expected_df)


def test__get_longer_ngrams() -> None:
    ngrams = ["aa bb", "aa bb cc", "cc aa bb", "cc dd aa", "dd aa"]

    longer_ngrams = _get_longer_ngrams(ngrams, "aa")
    assert longer_ngrams == ["aa bb", "aa bb cc", "cc aa bb", "cc dd aa", "dd aa"]

    longer_ngrams = _get_longer_ngrams(ngrams, "aa bb")
    assert longer_ngrams == ["aa bb cc", "cc aa bb"]

    longer_ngrams = _get_longer_ngrams(ngrams, "dd aa")
    assert longer_ngrams == ["cc dd aa"]

    longer_ngrams = _get_longer_ngrams(ngrams, "a bb")
    assert longer_ngrams == []

    longer_ngrams = _get_longer_ngrams(ngrams, "dd a")
    assert longer_ngrams == []
