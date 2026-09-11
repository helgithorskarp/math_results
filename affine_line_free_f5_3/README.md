# Global reductions for 73-point line-free sets in F_5^3

The open parameter is the largest cardinality of a subset of F_5^3 containing
no complete affine line. The published interval remains **70 <= r_5(F_5^3) <= 73**.
This contribution proves necessary structure and exhaustive reductions at 73;
it does **not** change either endpoint or decide existence.

For every hypothetical 73-point set S:

* At least nine parallel-plane directions have profile (9,16,16,16,16) or
  (10,15,16,16,16), and at least 74 affine planes contain 16 points.
* Three such directions are independent. Consequently four specified
  coordinate-profile cases cover every S up to affine equivalence.
* A second, classification-based cover has three branches: a direction with
  at most three points on each parallel line; a lifted strong (3 mod 5) dual
  with planar base size 18, 23, 28 or 33; or the unique exceptional dual of
  size 128. The exceptional duals of sizes 143 and 168 cannot occur.

The first two claims use elementary incidence counting. The last imports the
published classification of strong (3 mod 5)-arcs. Its exhaustive scope includes
the full-hyperplane and lifted cases; neither is silently discarded.
The first branch has exactly two line-occupancy profiles: one line of size 1
and 24 of size 3, or two lines of size 2 and 23 of size 3.

## Proof and dependencies

See [proof.md](proof.md) for the complete deductions and coverage arguments.
The small planar facts (no 17-point line-free set; no 12-point set meeting each
line in at most three points) are independently replayed by `plane_caps.cpp`.
The external classification is a cited theorem, **not** re-proved by this package.
Its computer-assisted proof is an explicit external trust boundary.

Primary literature:

1. C. Elsholtz, L. Führer, E. Füredi, Z. Kovács, P. P. Pach, D. G. Simon,
   and D. Velich, *Maximal line-free sets in F_p^n*, Periodica Mathematica
   Hungarica 90 (2025), 7–21,
   [DOI](https://doi.org/10.1007/s10998-024-00617-x),
   [arXiv:2310.03382v2](https://arxiv.org/abs/2310.03382v2).
   Theorem 1.5 supplies the upper endpoint 73; Figure 4 supplies the 70-point
   control, transcribed in `known70.json`. Neither is a new result here.
2. S. Kurz, I. Landjev and A. Rousseva, *Classification of (3 mod 5) arcs in
   PG(3,5)*, Advances in Mathematics of Communications 17 (2023), 172–206,
   [DOI](https://doi.org/10.3934/amc.2021066),
   [arXiv:2108.04871v2](https://arxiv.org/abs/2108.04871v2).
   Theorems 5.2 and 5.3 give the three exceptional arcs and their multiplicity
   spectra; Theorem 3.3 defines lifting. Our reference numbering is to this
   specified arXiv version.

## Reproduce the exact checks

From this directory, with Python 3.10+ and a C++20 compiler:

```sh
mkdir -p build
g++ -O3 -std=c++20 -Wall -Wextra -Wconversion plane_caps.cpp -o build/plane_caps
build/plane_caps
python3 check_reduction.py
```

The C++ output is `expected_planar.json`; the Python output is
`expected_reduction.json`. Both use integer arithmetic only. The former visits
all 5,200,300 labelled 12-subsets and all 1,081,575 labelled 17-subsets of the
affine plane. The latter builds the geometry independently from pairs of
points, checks its incidences, enumerates every parallel profile, verifies
the numerical inequalities, and checks the known 70-point witness.
These computations support the human proof; arithmetic assertions alone
are not a replacement for its logical coverage argument.

## Exact unrestricted CNF cover

With `python-sat==1.9.dev15` installed:

```sh
python3 generate.py --case 0 --out build/case0.cnf
python3 generate.py --case 1 --out build/case1.cnf
python3 generate.py --case 2 --out build/case2.cnf
python3 generate.py --case 3 --out build/case3.cnf
```

`--many-full` optionally adds the proved lower bound of 74 planes of size 16.
The four baseline CNFs are byte-for-byte the instances probed in this pass;
hashes and dimensions are in `runs.json`. Each native Kissat probe stopped
at its 300-second limit with **UNKNOWN**. All four cases remain unresolved.
The classification-based branches have not yet received exhaustive solver runs.
No solver timeout or fractional relaxation is used as a mathematical premise.

Point variable `25*x+5*y+z+1` expresses membership. Each of the 775 five-point
lines contributes the clause excluding simultaneous membership of all its
points. Totalizers encode |S|=73, every plane size <=16 and the coordinate
profiles proved below. The optional cut uses indicators implying plane size
>=16 and requires at least 74 indicators. Existing plane upper bounds make
this equivalent to requiring at least 74 size-16 planes. Auxiliary assignments
exist for every S satisfying these cardinalities, by the totalizer encoding.

A satisfying model must be decoded and checked against the original line
definition. A future exclusion requires a checked proof for every retained
case plus the coverage theorem. Raw instances, incomplete proof traces and
exploratory logs are omitted from Git; their provenance is recorded in the
compact run manifest. The current result is a structural reduction, with
the numerical question still open.
