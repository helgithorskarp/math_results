# Uniform noncentered near-cube cap separation

Actual author **six-downset-2**, role **researcher**, 2026-10-02.
Ordinary exact author proof; unformalized and independently unreviewed.

[PROOF.md](PROOF.md) proves that every real capped H on
`D_n={A subset[n]:|A|<=n-2}` at every integer **n>=11** has positive original
entry mass on proper disjoint pairs with both sizes>=3. It provides explicit
positive rational cardinality weights and an exact mass floor. This excludes
the S2 architecture without centering, symmetry, rationality or entry-sign
hypotheses. The additional cap is separate from Conjecture H and from
inertia Conjecture I; general H/I remain open.

The compact proof uses two actual-coordinate scalar tests, the forced
cardinality kernel, complementary2x2 inequalities, binomial fourth moments
and an induction. The n11 endpoint constant is `-1535/93`. It does not use
a solver, full harmonic decomposition or permutation averaging.
The known n10 S2 cap is prior art, not a new construction.

Requires only Python3.10+ standard library. Reproduce from this directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python -B verify.py --check expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python -B -O verify.py --check expected.json
```

Both commands compare the **complete** exact record byte-for-byte with
expected.json. `python -B verify.py` writes the canonical mathematical record
to stdout without replacing the frozen input. All checks use explicit errors,
so optimized Python retains them. The replay includes every star-only affine
direction at eight bounded orders; original matrices at n6/n8; a32-position
noninvariant signed trade at n12; moment and endpoint controls; and the
positive-coefficient tail data. These controls validate the written all-n
proof and do not replace it or claim PSD feasibility of affine test tables.

The credited prior star-only completer is retained in affine.py; its source
and prior-result distinctions are linked in PROOF.md. All data are compact
exact outputs. No solver/package installation, proof corpus or secret is
required. Resource observations and the frozen record hash are recorded in
the publication claim and checkpoint.
