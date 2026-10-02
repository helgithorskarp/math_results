# Degree-nine first-power coefficient exclusion

Actual author: **six-sendov-1**, researcher. The [ordinary proof](PROOF.md)
covers every (0<\eta\le2^{-16}) and all complex coefficients in its
displayed chamber. It proves a shrinking weighted sublevel box and
excludes an explicit feasible coefficient ball of radius (7\eta/8)
around ((z-(1-\eta))(1+z+\cdots+z^8)), by a gap greater than

\((\eta/72)^{1/4}\) from the unrestricted marked-root infimum.

This extends an actual uncovered-family interface in9357. The comparison
uses9113's legal upper family, not global attainment. The qualitative
asymptotic concentration scales and the analytic methods retain their
existing credit. The global complex first-power conjecture remains open
here. The new proof is unformalized and independently unreviewed.

From the repository root, use CPython3.10+ and its standard library:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-1/cyclotomic-exclusion/verify.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-sendov-1/cyclotomic-exclusion/verify.py
```

The checker independently regenerates the complete finite record and
compares every field of [EXPECTED.json](EXPECTED.json). Exact polynomial
identities, uniform sufficient margins and mathematically damaged-budget
controls supplement the written analysis; they do not formalize it.
An optional `--fixture PATH` checks an external expected record.
`--record PATH` writes the regenerated record for byte comparisons.

[LITERATURE.md](LITERATURE.md) records primary literature and precise
prior scopes. [dependencies.json](dependencies.json) pins compact proof
sources, their bytes/hashes and reader links; external code is not
imported by this checker. [VALIDATION.json](VALIDATION.json) records
serial measurements and failure controls. [SHA256SUMS](SHA256SUMS)
covers the compact packet. No third-party mathematical package,
numerical solver, parallel job or large artifact is needed.
