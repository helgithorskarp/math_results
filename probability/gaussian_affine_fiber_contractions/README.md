# Gaussian and ball-volume comparison for parallel affine fibers

The [author proof](PROOF.md) gives a simultaneous contracting motion in `R5`
for **every 1-Lipschitz map on complete parallel lines that is affine on
each line and maps them into parallel lines**. In fixed independent endpoint
frames it has the form

```text
T(u,z)=(H(u), a z+b(u)),       u in K subset R2, z in R.
```

The common slope is forced by shortness. For `|a|<1`, the exact hypothesis is
that `G=(H,b/sqrt(1-a^2)):K->R3` be short. The transverse set can be arbitrary
closed and the profile fully nonlinear. All bounded supported laws satisfy
Gaussian majorisation at every positive variance. Every finite selection of
centers satisfies both union and intersection comparisons for arbitrary
individual ball radii.

For `0<a<1`, `c=sqrt(1-a^2)` and `g=b/c`, the motion is

```text
Phi_t=(sqrt(1-t)u, sqrt(t)H(u), (a z+t c g(u))/sqrt(a^2+t c^2)).
```

Its squared pair distance equals the source distance squared minus
`t L + t/(a^2+t c^2) S`, where
`L=|Delta u|^2-|Delta H|^2-(Delta g)^2>=0` and
`S=(c Delta z-a Delta g)^2>=0`. Both coefficients increase. Negative, zero,
and saturated slopes have the explicit endpoint-isometry or separate
motions in the proof. The Gaussian and Kneser--Poulsen transfers are credited
existing theorems.

This complements the accepted
[nonlinear parallel-slice class](../gaussian_parallel_slice_contractions/README.md).
A whole-domain quadratic profile here has no parallel-slice representation
in any fixed endpoint frames, and seven rational labels have paired affine
rank six. These are precise breadth controls, not a historical-priority
certificate or an exclusion of all older compositions.

**Status:** complete author proof awaiting independent review. Historical
priority is unverified; unrestricted R3 majorisation remains open. The
complete-line/affine-fiber premises cannot be inferred merely from sampled
pairwise contraction. [SOURCES.md](SOURCES.md) records scope and dependencies.

## Reproduction

Use CPython 3.11 or later and its standard library, from this directory:

```sh
python3 -B verify.py
python3 -B -O verify.py
python3 -B verify.py INPUT.json
sha256sum -c SHA256SUMS
```

The first two commands check the complete result against [EXPECTED.json](EXPECTED.json).
Expected status: `AFFINE_FIBER_EXACT_CONTROLS_PASS`.
Exact-state SHA-256:
`99ac582da241237015efc020fbf25bb1f24f3f2d723759a64edcb71a8b4b9c04`.
Four universal polynomial identities are expanded exactly, alongside 2,970
endpoint pairs, 20,790 motion and derivative checks, 12 finite certificates,
zero-loss controls, all slope branches and 14 failed/malformed controls.
The seven-label paired determinant is `-1/40`.
Normal and optimized runs took 2.29 and 2.40 seconds on the author's
CPython 3.11.2 host and reproduced the same complete record.

For other finite data, use [INPUT.json](INPUT.json)'s three fields: rational
3-vectors `source`, corresponding `target`, and rational `slope` in `[-1,1]`.
Coordinates are already in the prescribed source and target frames. The
certificate proves existence of a global affine-fiber short extension at
that slope exactly when its pair budgets pass. It does not construct the
Kirszbraun extension or search over frames or algebraic slope intervals.
Failed class membership does not give an adverse Gaussian sign. Malformed
input raises an error; floats are rejected.

The [checker](verify.py) verifies rational algebra and the stated finite
controls. The universal motion, time regularity, Kirszbraun extension, density
coupling and volume transfers are written mathematical arguments; there is
no numerical integration, solver, external dataset or formal proof assistant.
