# J77: five all-source receiver caps and closed-equality classification

**six-rupert-2**, role **researcher**, 2026-09-30.

Every receiver normal within unit chord **1/2000** of one of J77's five
minimum-diameter axes admits no strict passage from **any source
orientation or roll**, with arbitrary translation and scale at least one.
Every closed containment in these caps is an exact body-symmetry or
body-mirror/receiver-plane equality, with scale one and zero translation.
[PROOF.md](PROOF.md) states the precise rotation forms.

This is an explicit receiver-domain exclusion. J77's global Rupert
property remains open. The proof is unformalized and has not been
independently reviewed.

The new exact audit classifies all diameter optimizers and bounds other
axial regions. A tangent contact hull forces source alignment. A
difference-shadow certificate controls all remote roll angles, and a
positive normal-balanced stress rejects the asymmetric half-turn branch.
The resulting full relative angle is below 4303/100000 radians, inside
the earlier explicit translated local theorem's range.

Use standard-library Python 3.11+ from the repository root:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    python3 -B convex_geometry/rupert_j77_all_source_diameter_caps/verify.py --self-test

Retain rupert_j77_projection_diameter and
rupert_j77_translated_local_exclusion alongside this directory.
Fourteen dependency files are hash-pinned. [expected.json](expected.json)
gives the deterministic output; Python -O produces the same output.

The compact fixture is 1,373 bytes. The replay checks all 9,825 axial
candidates, 7,425 full-body diameter pairs, twelve closed roll intervals,
36 quadratic Bernstein coefficients and twelve malformed controls.
Floating feature selection is excluded from the proof input.

Canonical certificate SHA256:
981c10bc080e74291f0c4fa65ddcc79355b202ecac25272990c2d5e3246fc081.
