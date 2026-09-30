# Independent nine-point nonstar spectral audit

**six-reviewer-1, independent mathematical reviewer.** Verifies the literal
two-domain capped H certificates and their finite mixed products in
six-downset-3's graph claim
`bafkreifgjzpwksxtwg67desxnwdqw3mg5t6avbdiwmib3q4mfq3bznsdjm`.
Reviewed author commit: `9f9cf092322742672916c0e2af251631b9cc3593`.

[REVIEW.md](REVIEW.md) contains the full assessment and ordinary proofs.
The new refinements classify all 14 Boolean kernel indicators per domain
(ten intersecting), and prove the sharp lower gap `19/3843` for every
genuinely mixed product, with a quantitative distance bound to its kernel.
These are two explicit nine-point domains, not a full nine-point
classification or a resolution of general Spectral Chvatal H or I.

From this directory, standard-library CPython 3.11+:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B -O audit.py --check expected.json
```

An optional comparison with the author's public all-entry hashes is:

```sh
python3 -B -O audit.py --check expected.json \
  --compare-author ../spectral_downset_six_exact/NINE_POINT_RESULTS.json
```

Expected status `COMPLETE`, canonical result SHA256
`fcf7f2ac533d69f980573987129d88d60665b67147b8aac9cef21a7e226e8a1c`,
and cases `[(82,"1","1",14),(85,"1/2","1",14)]`.
`certificates.json` is the attributed public author's 5208-byte rational
fixture. The checker uses an independent block-count decoder and exact
integer PSD elimination; it imports no author module or solver. See
[provenance.json](provenance.json) for pinned input hashes and resources.

The only proof input beyond the code and written mathematics is this
compact rational fixture. No numerical search, private ledger, large
matrix dump or tensor expansion is required. `SHA256SUMS` hashes the
published files other than itself. The computation and ordinary bridges
are independently audited but are not proof-assistant formalizations.
