# Articulation growth of a Heesch-four polyhex

Researcher: **six-heesch-2**. This directory classifies a bounded family of
unmarked eighteen-cell polyhexes and checks its finite upper bounds through
local contact certificates. The finite-Heesch-five target remains open.

Let `S` be the sixteen-cell `H_c = H_h = 4` polyhex in `family.py`, from
[Kaplan's author dataset](https://cs.uwaterloo.ca/~csk/heesch/hex/16hex_3up.txt).
Delete one articulation cell of `S`, then add three cells. Require the final
shape to be connected and hole-free; allow intermediate disconnected shapes
and holes. Identify shapes under translations, six rotations and reflections,
and remove all shapes obtainable by adding two cells to `S`.

**Claim.** This family has exactly 1,557 members: 1,326 have `H_c = H_h = 0`,
149 have `H_h = 1` and `H_c <= 1`, and 82 tile the plane periodically.
Thus this family cannot supply a finite Heesch number at least five.
The periodic certificates use two copies for 70 shapes and four copies for 12.
No exact `H_c` value is asserted for the 149 one-surround cases.

The finite claims use 1,624 independently checked DRAT proofs: 1,326 first-surround
obstructions, 149 local contact-exclusion certificates, and 149 two-surround
obstructions using those exclusions. Source regenerates all formulas and proofs;
the generated proof corpus stays outside this directory.

## Conventions and completeness

Coordinates are axial hexagonal-grid coordinates with neighbor differences
`(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)`. All rotations and reflections are
allowed. `H_c` requires every corona prefix to be hole-free. `H_h` permits holes
only in the final prefix. Every new copy touches the preceding patch and covers
its boundary together with the other new copies.

The seed and its Heesch-four classification are prior work:
[Kaplan, *Heesch Numbers of Unmarked Polyforms*, arXiv:2105.09438](https://arxiv.org/abs/2105.09438),
Contributions to Discrete Mathematics 17(2), 150–171 (2022). The exact source
download had SHA-256 `cee2e3ef029fbd8a603f489835265e2f2077a75908423c539384e2e3cd259aa0`.
The coordinates are embedded, so reproduction requires no download.

**Grid alignment.** Polyhex boundary corners have angles 120 or 240 degrees,
and all boundary edges have unit length. On a completely covered boundary,
a vertex on another edge's interior would leave an impossible 60-degree gap
after angles 120 and 180, or would overlap after angles 240 and 180. Covered
edges therefore match vertex to vertex. At a filled vertex contact the angle
list is `(120,240)` or `(120,120,120)`. The known tile determines the three
120-degree hexagon sectors; each new copy occupies one or two of those exact
sectors and contains a hexagon of the same grid. A smooth contact matches a
whole unit edge and fixes the grid as well. Induction over coronas therefore
includes copies initially touching at a vertex. This is the local version of
the known full-tiling angle argument
in Paul Church, *Snakes in the Plane* (Waterloo thesis, 2008), Proposition 2.2.1.1;
no priority is asserted for grid alignment. The argument also appears in our
[two-cell-growth source](../heesch_polyhex_two_cell_growth/README.md).
The finite vertex-sector step is also explicit in
[six-heesch-3's curved-polyhex converse](../heesch_weighted_matching_obstruction/hex_grid_locking.md).

**Family.** The three articulation cells are `(-3,3),(-2,2),(1,2)`.
The free growth-stage counts are `3,73,1002,10301`. Exactly 1,881 final shapes
are connected and hole-free; 324 belong to the earlier two-cell-growth family.
In any connected final enlargement, every added cell has a path to the seed
union in the final cell graph. Insert added cells in nondecreasing graph
distance to that union. Each insertion is then a halo cell, proving completeness
even though the fifteen-cell remainder is disconnected. All intermediate holes
are allowed. Canonicalization under the twelve grid symmetries gives one free
representative. The canonical 1,557-shape SHA-256 is recorded in `summary.json`.

## Local contact certificates and upper bounds

For a fixed tile `T`, enumerate every disjoint congruent copy meeting `halo(T)`.
Every such copy has a cell `p` mapping to some halo cell `q`, so testing all
translations `q-p` for every orientation is complete.

Let `F_1` be the first-surround formula: every halo cell is covered and no two
selected copies overlap anywhere in their full footprints. Copies meeting the
halo are exactly the candidates. Therefore `F_1` represents every first
surround, with no final hole restriction. Direct exact-cover branching supplies
a surround witness for each of the 149 one cases. It checks full footprints
for overlap, congruence and halo coverage, establishing `H_h >= 1`.
For the 1,326 zero cases, `F_1` is certificate-checked UNSAT.

Compute a set `A` of contacts by exact cover with each contact forced in turn.
The support computation is a discovery aid; its negative decisions receive a
separate Boolean certificate. Check

```
F_1 AND OR { selected(U) : U is a contact outside A }
```

for UNSAT. This proves that **every** first surround uses only `A`. A superset
would also suffice. No correctness of the support search's exclusions is assumed
without this certificate. Rotating, reflecting or translating a complete first
surround transfers this eligibility statement to every congruent interior copy.

Now form `U_2`, the finite placements reachable from the center by at most two
contacts in `A`, excluding overlap with the center. Every genuine two-corona
patch is represented: the center and each first-corona copy have a complete
surround, so all their contacts are eligible. Every second-corona copy touches
a first-corona copy, giving a path of length at most two using `A`.

Let `d(P)` be minimum contact distance in `U_2`. Use cumulative variables
`z(P,i)` for `d(P)<=i<=2`. Force the center at level zero, require
`z(P,i) -> z(P,i+1)`, and forbid overlap among the final selected copies.
For every `i<2` and every halo cell `q` of `P`, require

```
z(P,i) -> OR { z(Q,i+1) : Q covers q and is an eligible contact of P }.
```

Each admissible two-corona patch gives a satisfying assignment. The clauses
allow holes in every prefix, providing a sound relaxation for upper bounds.
Certificate-checked UNSAT therefore proves `H_h < 2`. All 149 first-surround
cases have such an obstruction, including the one case where the exploratory
pair-pruning bound was initially only two.

The first certificate transports local eligibility to every interior copy;
the second checks the resulting finite packing obstruction. If there are `s`
eligible contacts, `|U_2| <= 1+s+s^2`. This can substantially reduce the second
formula's candidate set while retaining all actual two-corona patches. Local
eligibility follows from a complete surround. Basic corona SAT and the
cumulative-prefix framework are prior methods; no absolute priority claim is
made for the certificate factoring. This source applies separately checked
eligibility certificates to this specific growth family.
It builds on our earlier polyhex source and the cumulative-prefix framework in
[six-heesch-1's source](../heesch_polyomino_euler_cnf/README.md).

Combining this result with the earlier 324-member classification gives all
1,881 articulation-grown shapes: 1,526 zero cases, 221 `H_h=1` cases and 134
periodic tilers. This combined statement depends on the cited earlier result.

**Periodic cases.** A certificate lists copies and integer periods `(w,0),(s,h)`.
The checker tests all occupied-cell difference vectors. A difference `(dx,dy)`
lies in the period lattice exactly when `h` divides `dy` and `w` divides
`dx-s*(dy/h)`. Exactly `w*h` cells in distinct lattice classes provide exact
coverage and disjointness under all lattice translates. This checker uses
difference-vector membership, independently of the residue-mask search.

## Reproduce

Environment used: Python 3.12.14, `python-sat==1.8.dev24`, Glucose 4.1,
DRAT-trim commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, GCC 12.2.0.
Keep solver and numerical-library threads at one. From the repository root:

```bash
python3 -m venv scratch/heesch-bridge-env
scratch/heesch-bridge-env/bin/pip install -r heesch_polyhex_bridge_growth/requirements.txt
git clone https://github.com/marijnheule/drat-trim.git scratch/heesch-bridge-drat
git -C scratch/heesch-bridge-drat checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C scratch/heesch-bridge-drat drat-trim -j1
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  scratch/heesch-bridge-env/bin/python heesch_polyhex_bridge_growth/verify.py \
  --checker scratch/heesch-bridge-drat/drat-trim --work-dir scratch/heesch-bridge-proofs
```

The final counts are `Hh0:1326, Hh1:149, infinite:82`, with 1,624 checked proofs
and `full_family_verified:true`. The label `infinite` denotes the periodic
plane-tiling certificates. The formula-evidence digest must match `summary.json`.
Proof byte sequences may vary with solver builds; their hashes are provenance,
not the acceptance criterion. Only the current formula and proof are kept in
the work directory, plus a small per-case evidence log.

For bounded runs use `--start a --stop b` to verify exactly the interval `[a,b)`.
These runs report `full_family_verified:false`; all intervals must be covered
without gaps to check the entire family. A timeout, placement/clause limit,
failed proof check or unfinished interval supplies no missing upper bound.

The trust boundary includes the written geometric/encoding arguments, exact
Python, PySAT's cardinality encoder, and DRAT-trim/compiler. Mathematical
calculations use exact integers. No
assumed tiling from a large patch, or timeout-based exclusion is used. These
results have no formal-proof or independent-review verdict. Larger simultaneous
cell exchanges remain open research directions.
