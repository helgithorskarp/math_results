# Arbitrary-degree polynomial profiles on Tile(1,1)

Author **six-heesch-3**, role **researcher**.

[proof.md](proof.md) extends the all-small-nonflat quartic obstruction to
arbitrary-degree nonzero polynomial profiles with unchanged endpoint
positions and tangents. A covered 120/240-degree endpoint forces a whole
primitive port partner. Endpoint colors remove interface reversal, so
the unchanged sign-graph certificate forces one of three periodic
plane tilings or the known Spectre construction whenever two coronas exist.
Every non-tiler in this neighborhood has Hc,Hh<=1. No record improvement.

The result depends on the full
[previous exact graph certificate](../equilateral_nonflat_classification/README.md).
Run its reader first, then the new finite-hypothesis reader:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B round-two/six-heesch-3/equilateral_nonflat_classification/check.py --expected
python3 -B round-two/six-heesch-3/equilateral_polynomial_profiles/check.py --expected
```

The new reader checks corner partitions, periodic reversal bits and an
exact degree-five partial-coincidence example. The degree-independent
analytic/topological bridge is proved in writing. Uniform C1 smallness
is existential; zero profiles, nonpolynomial interfaces and larger
deformations remain outside the theorem. Author proof; independent
review pending.
