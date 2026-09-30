# Independent saturated single-pair review

six-reviewer-2, independent mathematical reviewer, 2026-09-30.

Confirms exact maxima **56/53** when two degree-20 points have pair degree one.
Proves that the degree-20/19 absent-pair maximum **59 is attained**, with
**one equality type**, degree multiset **15^4,16^8,17^4,19,20**, and full
coordinate automorphism group order **4**. The completed-line nonarc branches
have sharp maxima **55/52**. Global A(18,6,5) bounds remain **69–72**.

[REVIEW.md](REVIEW.md) gives complete reductions, exact scope, dependency and
trust boundaries, primary literature and strengthening opportunities.

From a complete repository checkout, Python3.11+standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B constant_weight_single_pair_review2/audit.py
```

The full deterministic output matches [expected.json](expected.json).
The required sibling `constant_weight_absent_pair_review1/expected.json`
is an explicitly inherited, previously peer-reviewed93-plane cover;
SHA256 **46dd2aa871cd825130474fb32e6a7ffa9debdb0263e4f059f3998f3118fa5806**.
`--absent-census PATH` selects those same pinned bytes elsewhere.
The older93-plane enumeration is not claimed rerun.

Independent method: fresh affine-frame and exceptional carrier enumeration;
106direct point-pair exact-cover searches,8204states;29fresh residual maxima;
1860missing-line cases,97291states; all5760point maps, explicit complete-code
transport and stabilizers. No target code import or target fixtures supply
these computations. Optional `--compare-author PATH` checks the29actual
plane/residual/maxima lists and106carrier rows against the pinned original
source and checks its56-word fixture; it does not alter the proof record.

Normal and optimized outputs are identical. All1100simple graphs through
five vertices agree with brute-force independence numbers, and five malformed
or zero-cap controls reject. Search caps fail with INCOMPLETE. Resources,
versions and hashes are in [VALIDATION.json](VALIDATION.json).

[INPUT.json](INPUT.json) records exact source provenance.
The expected output contains compact selected cases, histograms, stream hashes,
one59-word equality type and its explicit full attaining code. No raw search
corpus, private input, solver, credentials or proof-assistant result is used.
