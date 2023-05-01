# ncnc

[![test](https://github.com/jun-harashima/ncnc/actions/workflows/test.yml/badge.svg)](https://github.com/jun-harashima/ncnc/actions/workflows/test.yml)

This is an implementation of C-value and NC-value methods proposed in the following paper:

- Automatic Recognition of Multi-Word Terms: the C-value/NC-value Method

## Installation

```SHELL
$ pip install ncnc
```

## Usage

### C-value

First, prepare a DataFrame object which has the total frequency of each n-gram in a corpus. The names of the column and index should be `f(a)` and `ngram`, respectivey. The following code shows an example.

```PYTHON
import pandas as pd


dict = {
    "adenoid cystic basal cell carcinoma": 5
    "cystic basal cell carcinoma": 11,
    "ulcerated basal cell carcinoma": 7,
    "recurrent basal cell carcinoma": 5,
    "circumscribed basal cell carcinoma": 3,
    "basal cell carcinoma": 984,
}
df = pd.DataFrame.from_dict(dict, orient="index", columns=["f(a)"]
df.index.name = "ngram"
```

Then, give the DataFrame object to `calc_c_value()`.

```PYTHON
from ncnc.c_value import calc_c_value


df = calc_c_value(df)
```

Now, you can see a C-value for each n-gram like this:

```PYTHON
df = df.sort_values(by="c-value", ascending=False)
print(df.loc[:, ["f(a)", "c-value"]])
```

The results are as follows:

```SHELL
                                     f(a)      c-value
ngram
basal cell carcinoma                  984  1551.361296
ulcerated basal cell carcinoma          7    14.000000
cystic basal cell carcinoma            11    12.000000
adenoid cystic basal cell carcinoma     5    11.609640
recurrent basal cell carcinoma          5    10.000000
circumscribed basal cell carcinoma      3     6.000000
```

### NC-value

You can also calculate a NC-value for each n-gram like this:

```PYTHON
from ncnc.nc_value import calc_nc_value


df = calc_nc_value(df)
df = df.sort_values(by="nc-value", ascending=False)
print(df.loc[:, ["f(a)", "c-value", "nc-value"]])
```

Note that the input of `calc_nc_value()` is the output of `calc_c_value()`. The NC-values can be calculated after calculating the C-values.

Also note that we use all part-of-speech elements as context words, whereas the original paper used only nouns, adjectives, and verbs.

The results are as follows:

```SHELL
                                     f(a)      c-value     nc-value
ngram
basal cell carcinoma                  984  1551.361296  1242.122370
ulcerated basal cell carcinoma          7    14.000000    11.200000
cystic basal cell carcinoma            11    12.000000     9.766667
adenoid cystic basal cell carcinoma     5    11.609640     9.287712
recurrent basal cell carcinoma          5    10.000000     8.000000
circumscribed basal cell carcinoma      3     6.000000     4.800000
```
