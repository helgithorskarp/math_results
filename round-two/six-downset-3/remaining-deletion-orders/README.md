# Exact remaining deletion orders

Actual author six-downset-3, researcher. This extends the precise
affine-table/four-edge ansatz for Spectral Chvatal H. Independent review
of THIS extension is pending; ordinary counting, whole-space and lift
bridges remain unformalized. General H/I remain unresolved.

For every integer5<=k<=24, every q>=max(4,k), every deletionZ, capped H
in the ansatz exists iff q>=b(k)-5 for k in
{8,10,13,16,18,19,21,22,24}, and iff q>=b(k)-4 for
{5,6,7,9,11,12,14,15,17,20,23}. k5/k6 were already known; NEW
complete all-q classification is k7..24. Negative conclusions do not
exclude arbitrary H. A NEW three-vector original dual applies for EVERY
k>=2,q>=3k; its complementary negative test is not a converse.

[Full proof](PROOF.md), [exact verifier](verify.py), [all coefficient
certificates](three_vectors.py), [complete imported inputs](dependencies.py),
[entire frozen record](EXPECTED.json), [replayed record](RESULTS.json),
[manifest](SHA256SUMS).

From this directory, CPython3.12 standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python -O verify.py
sha256sum -c SHA256SUMS
```

Every requirement raises under optimized mode. BOTH modes compare the
ENTIRE canonically normalized record, including six pinned inputs.
Frozen records are never silently regenerated: --freeze refuses an
existing EXPECTED.json. Native threads1, one serial mathematical process,
fixed60s and unchanged1CPU2GiB. No solver/incomplete/resource failure
is a mathematical exclusion. The old cofactor/inverse method stays paused.

Coverage:20 boundary cases plus credited infinite positive/negative
corridors; ALL291661 original baseline pairs;23*3211=73853 new original
exception representative positions;133 exact positive coefficients
covering the ENTIRE new dual quadrant; both exact PSD algorithms on
all nine positives; concrete false-floor/negative-kappa/scope/asymmetry
and original dual damages. Representative symmetry is explained in the
proof; full10-million-pair exception enumeration is not claimed. No
network, solver, credential, private ledger or large corpus is required.
