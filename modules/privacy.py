import pandas as pd
import numpy as np

def generalize_age(df, col='age', bins=None):
    bins = bins or [0, 18, 30, 45, 60, 100]
    df[col + '_binned'] = pd.cut(df[col], bins=bins, labels=False)
    return df

def suppress_rare(df, col, threshold=10):
    vc = df[col].value_counts()
    df[col] = df[col].apply(lambda x: 'Suppressed' if vc.get(x, 0) < threshold else x)
    return df

def dp_noise(df, col, epsilon=1.0):
    noise = np.random.laplace(0, 1 / epsilon, len(df))
    df[col + '_dp'] = df[col] + noise
    return df
