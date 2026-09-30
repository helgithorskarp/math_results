# Tammes-15: independent degree-four audit and full-range skeleton exclusion

**six-reviewer-4**, independent mathematical reviewer, 2026-09-30.
[REVIEW.md](REVIEW.md) confirms six-tammes-1's committed h7786 theorem and
proves that no connected four-regular selected contact skeleton on fifteen
sphere points has exclusively simple strictly convex hemispherical T/Q
faces, even if some contacts are omitted. All pairs must have distance
at least the common selected-edge length. The theorem covers all possible
cosines, \(113/225\le c<1\); quadrilaterals may differ.

It does not classify arbitrary Tammes optimizers or improve a global
numerical bound. The earlier and newer conditional count claims retain
their own trust boundaries.

The independent implementation regenerates 15,740 labelled degree graphs,
28 graph orbits, five unoriented sphere covers and ten oriented maps.
It uses undirected edge double covers and vertex links, followed by
homogeneous angle matrices over \(\mathbb Q[c]\); no author modules are
imported. The sole corner-compatible map forces an angle below the weak
packing bound.

Reproduce from this directory using CPython >=3.11 and SymPy 1.14.0:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
.venv/bin/python -B audit.py --check
.venv/bin/python -B -O audit.py --check
sha256sum -c SHA256SUMS
```

The pinned original source directory must be present next to this one in
the repository. An alternative repository root may be passed with
`--repository /path/to/math_results`. To regenerate the full compact
independent output, omit `--check` and compare it with `EXPECTED.json`.
Expected data is comparison-only; every map is regenerated first.
Each run fits one CPU and the authorized 2 GiB process scope; native
thread counts must remain one.

Files: `maps.py` is the independent complete graph/surface census;
`angles.py` reconstructs the original medial map and proves the exact
angle obstruction; `audit.py` combines them with pinned input checks
and bounded controls; `EXPECTED.json` holds compact independent output;
`provenance.json` pins all target source files and identifies methods;
`validation.json` records completed checks and resources.

The full review states written geometric premises, exact scope,
dependencies, primary literature and strengthening opportunities.
The verified source commit is recorded in the subsequent graph review
and durable campaign checkpoint; reader-facing links use main paths.
