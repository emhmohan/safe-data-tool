def k_anonymity(df, quasi_ids):
    eq_sizes = df.groupby(quasi_ids).size()
    num_unique = sum(eq_sizes == 1)
    k = eq_sizes.min()
    total = len(df)
    return {
        'num_unique': int(num_unique),
        'k-anonymity': int(k),
        'unique_pct': float(num_unique) / total if total > 0 else 0
    }
