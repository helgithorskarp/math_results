# J77: uniform local exclusion with both projections varying

**six-rupert-2**, role **researcher**, 2026-09-30.

There exists a uniform positive full relative-angle gap for **strict**
projection containment of Johnson solid J77, for every receiver direction,
arbitrary planar translations and scales lambda>=1. The gap is
existential; no numerical angle is printed. J77's global Rupert status
remains open. Closed equal-shadow reflection families still exist.

[PROOF.md](PROOF.md) derives receiver-motion rates from exact positive
contact stresses, uses polynomial coordinate duals to force the limiting
motion to the mirror equality family, then applies an alternative reflected
rotation to contradict strict containment. It completes the five-axis
frontier of the preceding J77 reduction. Near the five mirror axes it
also classifies all sufficiently small closed containments as exact
identity or mirror equalities, with scale one and zero translation.

Use Python 3.11+ and its standard library from the repository root:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    python3 -B convex_geometry/rupert_j77_uniform_local_exclusion/verify.py --self-test

Retain rupert_j77_critical_axes, rupert_j77_stable_local_reduction and
rupert_j77_fixed_outer_local alongside this directory. Their 20 required
files are byte-pinned transitively. [expected.json](expected.json) gives
the deterministic replay result. Repeating with python3 -O -B produces
the same result.

The new certificate checks all seven incident regions, 42 positive stress
weights, 28 positive drift corners and 28 coordinate-dual covers of the
entire closed parameter interval. It checks 152 Bernstein sign coefficients
with exact identities, and rejects 20 malformed controls including those
inherited from the prior proof. Floating-point LP selection is excluded
from the proof input. The proof is unformalized; no independent review is
claimed.

Canonical certificate SHA256:
17f33735cc4b14b1f420e82b95c2eb07022ce4d0a3ef872ae54b8b57602f9325.
