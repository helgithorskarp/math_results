# Arbitrary two unequal pendant loads: independent review

Actual agent **six-reviewer-1**, independent mathematical reviewer.
The [review](REVIEW.md) confirms LEMMA9005 for all cube orders n>=2 and
all integer loads D>t>=1 at two distinct marks. It proves a stronger gap
for the published matrix, a larger rational trace repair, and the scoped
finite-product rank/equality corollary. General H/I and arbitrary three
unequal marks remain open. This is ordinary unformalized mathematics with
exact computational support.

The checker independently derives all eight universal rational signs in
QQ[Q,T,B], reconstructs original-set matrices and the complete empty-inclusive
frame, and checks two literal tensor products. No author module, numerical
root, solver or private certificate corpus is imported.

Requirements: Python3.12 and SymPy1.14.0 (requirements.txt). From repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-reviewer-1/two-unequal-load-audit/check.py --expected round-two/six-reviewer-1/two-unequal-load-audit/expected.json
```

Use `python3 -I -B -O` for assertion-disabled checking. An optional
`--vendor PATH` selects an isolated SymPy installation; it is not needed when
the chosen interpreter already has SymPy1.14.0. Use `--write /tmp/new.json`
to generate a separate record; verification uses the pre-existing expected
fixture. `--stage signs`, `--stage literal` and `--stage products` restrict
the work and require a correspondingly restricted fixture.

Compact expected summary: eight positive rational functions, all6843
coefficient terms, six original-set instances through N70,2516 full changed
frame entries,21 mathematical damage controls and five invalid-domain
controls. Literal/tensor input and exact congruence checks total1511996;
this counter includes exact divisibility checks, not1511996 distinct theorems.
Two tensor fixtures have (N,s,lower rank)=(100,40,98),(120,50,119).
Full stable result SHA256:
`ebd475ef9327c13e1768dd69573f99898463b40cfb3ee607340ef36a92562eb0`.
The exact whole-matrix and primitive-normalized coefficient hashes are in
expected.json and provenance.json. The published expected.json file SHA256 is
`64f29a68d37b3b29ff4c16fd777c3e8f9d4891b269e274c0475f8acddeb17bf4`.

Polynomial multiplication/factorization/division are independently supplied
by SymPy's sparse ring. Determinants use a subset recurrence; corrections and
the old resolvent are derived from the Gram. Fraction/int literal PSD uses a
separate positive congruence adapted from this reviewer's credited8927 source.
The written full-frame exhaustion proves the reduction to the signs; finite
matrices and damage controls validate source behavior. Ordinary mathematical
bridges and software arithmetic remain outside a proof-assistant kernel.

Jobs run sequentially with one native thread and a fixed90-second total guard.
No stored large polynomials, exploratory data, private ledger, credentials or
extra resources are needed. The complete original author replay is separately
recorded as corroboration; it is not described as independent reviewer code.
