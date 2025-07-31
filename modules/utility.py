from scipy.stats import ks_2samp

def ks_table(orig, mod, cols):
    results = {}
    for col in cols:
        if orig[col].dtype.kind in "biufc":
            stat, p = ks_2samp(orig[col], mod[col])
            results[col] = {'KS': stat, 'p': p}
    return results
