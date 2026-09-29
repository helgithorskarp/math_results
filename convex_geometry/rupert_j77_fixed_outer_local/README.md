# Fixed-outer local exclusion for J77

Author: **six-rupert-2**, role **researcher**, 2026-09-29.

For every fixed projection direction of the paragyrate diminished
rhombicosidodecahedron (Johnson solid J77), sufficiently small nonzero
relative rotations cannot produce even closed shadow containment,
with arbitrary translations and passage scale at least one.
The bound depends on the fixed direction. The global Rupert question
remains unresolved.

[PROOF.md](PROOF.md) proves the claim from an exact finite certificate.
The asymmetric solid has 50 antipodally paired vertices and five cap
vertices. Opposite supporting contacts cancel translations where
available; the remaining regions use five-dimensional contact cones
that include translation coordinates.

Reproduce from the repository root with Python 3.11+, standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B convex_geometry/rupert_j77_fixed_outer_local/verify.py --self-test
```

The same command with `python3 -O -B` gives identical output.
[expected.json](expected.json) records the finite checks: 191 leaf
triangles, four exceptional open edges, five exceptional vertices,
94,380 support comparisons, and 11,806 nonnegative cubic/quintic
coefficients. The 28 KB [certificates.json](certificates.json) contains
selected contact indices, not search traces. Every boundary is checked.

[model.py](model.py) regenerates the named solid independently of its
vertex fixture. [chamber.py](chamber.py) regenerates the direction
partition, and [q5.py](q5.py) supplies exact ordered-field arithmetic.
The verifier independently replays determinants and ordered signs;
no floating-point software or external input is required.

A measured optimized-mode verification took 16.9 seconds and 51,032 KiB
on Python 3.11.2, one CPU job and one thread. The proof is unformalized;
no independent review is claimed. See PROOF.md for literature,
complementary team results, and the precise quantifiers.
