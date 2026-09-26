# Validation record

The following commands passed on 26 September 2026:

```sh
python3 verify.py --check
python3 -O verify.py --check
```

Both modes used CPython 3.11.2. The ordinary check also passed on CPython
3.12.14. Only the Python standard library is required. Explicit exceptions
keep every mathematical check active under `-O`.

The largest calculation is exact row reduction of a `78 x 48` rigidity
matrix over `fractions.Fraction`, once for each endpoint of the flap.
The entire validation takes roughly one second on the publication host.
It does not use the host's ongoing certificate audits or any native proof
checker.

The generated flap coordinates were compared entry by entry with the
existing `gaussian_majorisation_rank_abel/flap_fixture.json` at source
commit `f7c122d6a5ade217930d63da27e67f9a9e55a539`; both lists agree.
All 16 labels are retained even though the target has 10 distinct sites.

For the octahedral mesh, all eight binary choices along one dual spanning
tree are examined. Exactly four produce consistent images at shared
vertices. For each accepted map the checker tests all source pair
inequalities, every mesh-edge equality, and rigidity rank 12 on the
actual mesh edges. An expansive tetrahedron is rejected, and elementary
rank controls include a dependent matrix and the zero matrix.

The generated record is [EXPECTED.json](EXPECTED.json), SHA256:

```text
e0c3cc8b723505a10f47ac545ab6fd92f7be13ae90978d3c3f8969dbe5fc054a
```

These are finite controls of the written geometric argument, not an
independent review. The general extension theorem and analytic hinge
transfer are not certified by these calculations. No Gaussian sign has
been numerically estimated, and no counterexample search was run.
