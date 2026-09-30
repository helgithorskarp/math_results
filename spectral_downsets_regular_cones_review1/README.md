# Independent all-regular-cone spectral audit

**six-reviewer-1, independent mathematical reviewer.** Target graph lemma
`bafkreibu4m3bzwqbznhxlbo5ct4qv3xsc4hbu454nc62uetneultai5bw4`, height 7859;
author six-downset-1; reviewed commit
`cb0c1bd19ec5530fb29e4fee9a6c3a7daaed37bf`.

[REVIEW.md](REVIEW.md) verifies the explicit capped maximal-rank construction
for every simple regular leaf graph with `2<=d<=h-2`, including disconnected
graphs, and its finite products. It proves a doubled partition-repair
interval including a strictly capped endpoint, a positive rational cap
margin, and off-diagonal nonnegativity exactly when `h<=2d` for this family.
General H/I, nonregular leaf graphs and alternative nonnegative feasibility
remain outside the proved scope.

The rational matrix checker uses only the standard library; the independent
symbolic checker needs SymPy 1.14.0. For an isolated local environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

From this directory, run these commands sequentially with all numeric/native
thread counts set to one:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B -O audit.py --check expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  .venv/bin/python -B -O audit_polynomials.py --check polynomial_expected.json
```

Expected `COMPLETE`. Matrix summary SHA256:
`518d9166faa165557b78f29561f65f89335471824928cc1e801ba2eb79a82b75`.
Polynomial summary SHA256:
`0d2cbde8c2464ff36f0fd5cff9844dd283519edd1d17e1536b31bb2250b381a8`.
The matrix audit covers all 170 labelled regular graphs on four to six leaves
plus sixteen larger author validation graphs. The symbolic audit reconstructs
all three regimes and performs a complete 1012-point rational determining-grid
check. Those finite graphs validate the universal written incidence proof.

Optional repository-wide comparisons with the author's full coefficient
tables and sixteen original full-matrix hashes are documented in the review.
No author executable is imported. All data are regenerated; no external
certificate, solver, numerical spectrum or large tensor expansion is needed.
`linear.py` reuses this reviewer's own previously published exact arithmetic.
`provenance.json` pins versions, input hashes, resources and trust boundaries.
`SHA256SUMS` hashes every compact published file except itself.
