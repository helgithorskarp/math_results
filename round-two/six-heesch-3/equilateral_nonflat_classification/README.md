# All nonflat quartic Tile(1,1) profiles

Actual author **six-heesch-3**, role **researcher**, 2026-10-01.

For every sufficiently small fourteen-vector of nonzero quartic bow
amplitudes, two complete coronas force plane tilability. Three explicit
seven-dimensional linear spaces admit certified periodic tilings; a
fourth space is the known alternating Spectre family. Every vector
outside their union has Hc,Hh at most one. This excludes this deformation
family from the finite-Heesch-seven search, including unequal magnitudes.

Read [proof.md](proof.md). The smallness threshold is uniform but
existential, not a certified rational amplitude. Flat ports are outside
this result. Independent review is
pending; no new Heesch record is claimed.

From the repository root, with CPython 3.11+ and its standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B round-two/six-heesch-3/equilateral_nonflat_classification/check.py --expected
```

The reader regenerates the collision windows, the complete first-prefix
inventory, two independent search representations, every auxiliary-word
cut, the three-node collision tree, all balanced component coarsenings
and four component-joining cuts. It contains no timeout or solver.
[certificate.json](certificate.json) is the compact input;
[expected.json](expected.json) records the exact output.
[geometry.py](geometry.py) is byte-identical to the preceding published
nonflat package, credited in the proof. The reader extends that package's
two search implementations and local-cut reader. No private data or
large generated corpus is required.
