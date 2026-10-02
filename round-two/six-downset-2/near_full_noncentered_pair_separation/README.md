# Noncentered sixteen-point positive support and an all-order S2 energy budget

Actual author **six-downset-2**, role **researcher**. See [PROOF.md](PROOF.md).

On D(16,14), every real capped H matrix has positive original unordered
proper-union mass>1/64 between two sets both of size at least3; some entry
exceeds2^-31. Centering/invariance/rationality/sign assumptions are absent.
Six rational PD duals and one rank-one degree-three lower term cancel all19
S2 parameters; the remaining30 orbit coefficients are positive.

For every n>=6 an invariant ordinary S2 H also satisfies the explicitly
quantified diagonal two-set/complement budget in the proof. This is a
necessary condition, not a positive construction or an all-order cap exclusion.
General H/I remain open. Ordinary bridges are unformalized; these new results
are independently unreviewed. Review9295 retains its separate verdict on9269.

Reproduce with **CPython3.12.14**, standard library only, from this directory:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -B verify.py --check expected.json
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -B -O verify.py --check expected.json
```

`dual.json` contains exact rational upper triangles, labels and claimed bounds.
`verify.py` reconstructs the whole affine functional and every individual
coefficient, checks two exact PSD algorithms and the universal cleared
quadratic identity, and compares every regenerated expected field. `model.py`
contains the credited physical forms and new exact pair/mean Schur reduction;
`affine.py` has separate star-only RREF and singleton completion. `exact.py` is
a byte-identical credited copy of the9017 PSD backend. No center equation,
solver, floating proof input or large matrix is needed for replay.

Both complete frozen replays passed in 7.214/7.637s (normal/optimized),
with observed peak child RSS 24,132KiB. The child guards were45s;
the existing1CPU2GiB scope and all six native thread variables1 were retained.
Whole canonical record SHA256:
`2ba78bcbdb3752828e912f5c8313ed7e3780ed9ffd3ea05129dafebfcfa662ea`.

Compact expected output has `ok: true`,49 full affine directions,19 exact S2
cancellations,30 positive omitted orbits,18,942,222 unordered original pairs,
63 bounded S2 validation directions, and17 rejected damages. All six duals are
PD by both exact algorithms. The universal identity has four nonzero monomials
in six formal variables. Original affine controls cover orders57 and247, both
signs of a noninvariant32-position rectangle trade, and actual empty loops and
rows. These original controls validate definitions and do not assert capped
feasibility. The known six- and ten-point seeds are credited prior controls.

`expected.json` is a complete regenerated record, not a tolerance comparison.
The17 damage checks reject: floating dual input, a triangle width, a layer
label, a lower/upper mode, a negative rank-one multiplier, the unordered count,
a false PSD matrix, a PSD-preserving change that destroys affine cancellation,
a false constant, the universal mixed coefficient, a floating S2 coordinate,
a singular complement range violation, a negative mean bulk, a forbidden
large original allocation, an actual empty-loop change, false centering of
the empty row, and a wrong harmonic Gram factor. Explicit exceptions remain
active with `-O`.

Generated caches are ignored. Private discovery scripts, proposals, recovery
outputs and checkpoints are excluded. No full65,519-order matrix or external
proof corpus is a replay input. Discovery used CVXPY1.7.4/Clarabel0.11.1/NumPy1.26.4
on CPython3.11.2; portable checking uses CPython3.12.14 standard library only.
