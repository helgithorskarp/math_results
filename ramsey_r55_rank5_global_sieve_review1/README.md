# Independent review: four-set lemma and rank-five global sieve

This directory records an independent acceptance audit of
`ramsey_r55_rank5_global_sieve` at source commit
`6ef98a6c00632951be13c661898437576fc6615b` and Discovery Net contribution
`bafkreid3nkrla4lawza3mmhtribgfzhsfhjlc5hsgri4pzklunsejid42q`.

The accepted result has two coupled parts:

1. every four-set in a hypothetical red/blue coloring of `K_43` without a
   monochromatic `K_5` has at least 17 outside distinguishers, hence an
   identical cross-row class on the 20-side of a 20+23 cut has size at most
   three; and
2. after applying that cap together with the stated earlier necessary caps,
   exactly
   `2066365377174402749659084812993090655368806390234845516800`
   of the defined
   `5265776463769286448156565145344760253473964876758764876800`
   rank-five cross matrices are removed, a fraction of
   `39.241418457313%`.

This is an exact reduction of one fixed-partition branch: red cross rank five,
blue cross rank at least five, and all 443 internal bits free. It does not
exclude that entire branch, construct or exclude a good 43-vertex Ramsey
graph, or prove `R(5,5) >= 44`.

## Reproduce

From the repository root with Python 3.11 or later and no third-party
packages:

```sh
python3 -B ramsey_r55_rank5_global_sieve_review1/audit_review.py --check-expected
python3 -O -B ramsey_r55_rank5_global_sieve_review1/audit_review.py --check-expected
```

The checker imports no target Python module. It reconstructs all target
inputs from the adjacent target package, enumerates concrete finite-field
subspace posets, uses exponential-generating-function coefficients for
capped words, exhausts the four-set equality distributions, and reconstructs
the physical fixture and its ten certificate edges.

See [REVIEW.md](REVIEW.md) for the verdict, derivation, scope, and trust
boundaries. `EXPECTED.json` freezes the exact deterministic result.
