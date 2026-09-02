# Three-point augmentation closure of the Parts 509-vertex graph

## Result and scope

Let `G` be the strict unit-distance graph on Jaan Parts's 509 algebraic points
(vertex set `V`, 2,442 edges, `chi(G) = 5`, 5-vertex-critical; see
`../hadwiger_nelson_parts509_criticality`), `K = Q(sqrt3, sqrt5, sqrt11)` the
coordinate field, `Q3` the exact list of the 1,158 points of the plane outside
`V` at unit distance from at least three Parts vertices
(`../hadwiger_nelson_parts509_swap_closure/completion_points.json`), and `Q2`
the set of points outside `V` at unit distance from exactly two Parts vertices.
For a set `D` of vertices and a set `A` of points write `G - D + A` for the
strict unit-distance graph on `(V \ D) ∪ A`.

The evidence in this directory establishes, with exact arithmetic throughout:

1. **Triple closure on `Q3`.**  For every vertex `u` and every 3-set
   `A ⊂ Q3`, the graph `G - u + A` is 4-colourable except for the declared
   instances `(A, u)`: 2,184 explicit triples (listed per vertex), all
   triples containing a certified swap point of `u` (11 swaps), and all
   triples containing a declared pair of `u` (12,901 pairs of the sibling pair
   closure).  Write `U(A)` for the set of vertices `u` with `(A, u)` declared.
   The distribution of `|U(A)|` over the triples with a declared vertex that
   is not swap-implied is

   ```text
   |U(A)| = 1: 186,665 triples;  |U(A)| = 2: 11,165;  |U(A)| = 3: 114;  |U(A)| = 4: 2;  |U(A)| >= 5: none
   ```

   Exactly two triples have four critical deletion vertices: `A = {27, 30, 43}` with `U(A) = {383, 415, 442, 479}` and `A = {43, 60, 658}` with `U(A) = {392, 415, 455, 499}` (indices into the `Q3` list; point 43 is the swap point of vertex 415).  For both, the 508-vertex graph `G - U(A) + A` is 4-colourable, and the certificate contains the two explicit colourings.

2. **Two-neighbour points.**  Exactly 2,705 points of `K^2 \ V` are at unit
   distance from exactly two Parts vertices (`Q2K`, enumerated exactly from
   the 18,199 vertex pairs with `K`-rational unit-circle intersections).  They
   have 4,537 exact unit incidences with `Q3` and 4,790 with each
   other, giving 10,015 triples of type (ii) (`p ∈ Q2K` adjacent to two `Q3`
   points), 650 of type (iii-a) (`p1 ~ p2 ∈ Q2K` both adjacent to a
   `Q3` point) and 468 unit triangles inside `Q2K`.  For each of these
   11,133 clusters `U(A)` was computed in the same way; the histogram of
   `|U(A)|` is `{0: 10,851; 1: 282}`.  No cluster has two or more critical deletion vertices (the 282 single vertices are exhausted-budget declarations, almost all the swap-implied instances of point 80 with vertex 220), so no direct test was needed for them.
   The 135,468 non-`K`-rational unit-circle intersection points of vertex
   pairs (each at unit distance from exactly its two generating vertices and
   from no other point of `K^2`) contain 162,584 exact unit pairs
   (all with `rho1 rho2` a square in `K`; the perpendicular-chord case does
   not occur) and 30,160 exact unit triangles; every triangle is a
   further cluster (three added points, each keeping its two generating
   vertices).  The histogram of `|U(A)|` over these clusters is
   `{0: 30,160}`.  No non-`K` triangle has a critical deletion vertex at all: every one of the `30,160 * 509` instances is covered by an existing library colouring (no fresh witness was needed).

3. **No 508 by "delete four, add three".**  For every four-element set
   `D ⊂ V` and every set `A` of three distinct points of the plane, the strict
   unit-distance graph on `(V \ D) ∪ A` is 4-colourable.  Together with the
   sibling closures (delete one / delete two, add one / delete three, add two):
   *every 5-chromatic unit-distance graph with at most 508 vertices has at most
   504 vertices in common with the Parts graph.*

Nothing here improves the bounds `5 <= chi(R^2) <= 7` or the 509-vertex record.

## Reduction to a finite exact computation

- **Vertex-critical core.**  If `G - D + A` (`|D| = 4`, `|A| = 3`) is
  5-chromatic, take a minimal `W' ⊆ (V \ D) ∪ A` whose strict unit-distance
  graph `H'` is 5-chromatic; `H'` is vertex-critical, so every vertex of `H'`
  has degree at least 4.  Write `W' = (V \ D') ∪ A'` with `D' ⊇ D`,
  `A' ⊆ A`.  If `|A'| <= 2`, `H'` is a subgraph of `G - D'' + A'` for a
  subset `D'' ⊆ D'` with `|D''| = |A'| + 1`, which is 4-colourable by the
  sibling closures.  Hence `A' = A`, and each added point has at most two
  neighbours in `A`, so at least two unit neighbours in `V`.  Points of `V`
  itself are excluded (they reduce to a smaller deletion set).
- **Which points matter.**  A point at unit distance from three points of
  `K^2` is their circumcentre, hence lies in `K^2`; so every added point with
  at least three unit neighbours in `V` is in `Q3`, and a point with exactly
  two must be adjacent to both other added points.  This leaves four shapes:
  (i) `A ⊂ Q3`; (ii) one point `p` of `Q2` adjacent to two `Q3` points, so
  `p` has four unit neighbours in `K^2` and `p ∈ Q2 ∩ K^2 = Q2K`;
  (iii-a) two adjacent points of `Q2`, both adjacent to a `Q3` point, again
  both in `Q2K`; (iii-b) a unit triangle in `Q2`, either inside `Q2K` or with
  all three points outside `K^2` (a mixed triangle is impossible, since a
  non-`K` point would then have three `K^2` unit neighbours).
- **Layering.**  If `G - D + A` is 5-chromatic then so is `G - u + A` for
  every `u ∈ D`, i.e. `D ⊆ U(A)`.  So it suffices to (a) exhibit, for every
  `(A, u)` outside the declared list, a proper 4-colouring of `G - u` that
  extends to `A`, and (b) for every `A` with `|U(A)| >= 4` and every 4-subset
  `D ⊆ U(A)`, a proper 4-colouring of `G - D + A` directly.
- **Extension test.**  A proper 4-colouring of `G - u` extends to `A` iff the
  points of `A` can be list-coloured from their free colours (colours absent
  from their surviving unit neighbours) with distinct colours on the unit
  edges inside `A`.  A colouring that extends from `G - u` still extends after
  further deletions, which gives (a) for every `D ∋ u`.
- **Non-`K` triangles.**  The two intersection points of the unit circles
  around a vertex pair `(v_i, v_j)` at distance `d < 2` are
  `p = m ± t n` with `m` the midpoint, `n` the rotated chord and
  `t = sqrt(rho)`, `rho = (4 - d^2)/(4 d^2) ∈ K`; `p ∉ K^2` exactly when
  `rho` is not a square in `K` (decided exactly by the sibling square-root
  test).  For two such points, `|p1 - p2|^2 = 1` is decided exactly in the
  extension `K(t1, t2)`: if `rho1 rho2 = k^2` with `k ∈ K`, then
  `t2 = k t1 / rho1`, `p1 - p2 = a + t1 b` with `a, b ∈ K^2`, and the
  condition is `|a|^2 + rho1 |b|^2 = 1` and `a·b = 0`; otherwise
  `{1, t1, t2, t1 t2}` is a `K`-basis and the condition is that the three
  cross terms vanish and the `K`-part equals one.  The candidate pairs are
  produced by a floating-point annulus search (coordinates to 50 decimal
  digits, rounded to doubles with absolute error below `1e-14`, tolerance
  `1e-7`, every pair of grid cells meeting the unit annulus examined), so no
  exact unit pair is missed; the exact test is then applied to every
  candidate.  A non-`K` point is at unit distance from no point of `K^2`
  other than its two generating vertices (three `K^2` neighbours would force
  it into `K^2`); the 201 near-miss candidates against `Q3 ∪ Q2K`
  are all confirmed non-unit exactly.

## Certificate

`triple_certificate.json` contains, for every vertex `u`, additional proper
4-colourings of `G - u` (3,653 rows, at most 77 per vertex, packed
as in the sibling certificates), the explicitly declared triples per vertex,
the exact `Q2K` points with their unit incidences, the `U(A)` lists of the
11,133 `Q2K` clusters and of the 30,160 non-`K` triangle clusters
(in a canonical order that the verifier reconstructs) with their fresh
witness rows (26 and 0), and 2 explicit
proper 4-colourings of 508-vertex graphs `G - D + A`.  Together with the 509 base deletion colourings, the 1,190
swap-closure rows and the 1,981 pair-closure rows it covers all
`C(1158, 3) * 509 = 131,391,201,604` `Q3`-triple instances and all
`11,133 * 509` cluster instances except the declared ones.

## Verification

Solver-free primary verifier (CPython 3.11, NumPy, mpmath for the 50-digit
non-`K` coordinates, SymPy only for parsing the published coordinate
expressions through the sibling `parts509.py`; the sibling directories must be
present):

```bash
python3 -m venv /scratch/parts509-triple-venv
/scratch/parts509-triple-venv/bin/pip install -r requirements.txt
/scratch/parts509-triple-venv/bin/python triple_certificate.py verify triple_certificate.json --workers 8
```

It re-derives the exact edge list, decodes and validates every colouring,
recomputes all unit incidences among `V ∪ Q3 ∪ Q2K` exactly, replays the
coverage of all triple and cluster instances, checks every direct witness,
re-enumerates `Q2K` and the non-`K` points and repeats the annulus screen.
Expected summary:

```text
all_checks=true
layer1: uncovered=43655 implied_by_pairs=41646 explicit=2009 n_undeclared=0 (stale=175)
U_histogram={1: 186665, 2: 11165, 3: 114, 4: 2}  q3_candidates=2  q3_direct_tests=2
clusters=11133  cluster_U_histogram={0: 10851, 1: 282}  cluster_direct_tests=0
nonk: points=135468 candidate_pairs=163375 exact_unit_pairs=162584 triangles=30160 K-point candidates=201 (unit: 0)
nonk_cluster_U_histogram={0: 30160}  nonk_direct_tests=0
```

(About 38 minutes with six worker processes on a loaded machine; `--skip-nonk` omits the non-`K` layer, which takes about half of it.)

```text
(the JSON summary printed last also lists every individual check)
```

Independent replay of layer (i) for chosen vertices, importing none of the
primary coverage code (pure-Python free masks from the neighbour lists,
Python-integer bitsets, complete enumeration by boolean matrix products,
exact list colouring for triples with internal edges):

```bash
/scratch/parts509-triple-venv/bin/python triple_verify.py triple_certificate.json 0 16 19 220 415 445
```

Each line must end with `"ok": true` (`undeclared_uncovered` 0); a
`stale_declarations` count only records declared triples that a later witness
happens to cover.  These six vertices (including the two with swap points 43
and 80) were checked this way; every vertex is covered by the primary
verifier.

## Regeneration

```bash
python triple_closure.py --workers 4 --budget 20000        # layer (i), writes triple_results/
python two_neighbour_points.py                             # Q2K, incidences, non-K screen -> q2k_extra.json
python cluster_U.py --q2k q2k_extra.json --out extra_U.json # U(A) of the Q2K clusters
python nonk_exact.py q2k_extra.json nonk_exact.json        # exact non-K unit pairs and triangles
python -c "import json; json.dump(json.load(open('nonk_exact.json'))['clusters'], open('nonk_clusters.json','w'))"
python cluster_U.py --clusters nonk_clusters.json --out nonk_U.json   # U(A) of the non-K triangles
python aggregate_triples.py                                # U(A) table of the Q3 layer
python direct_tests.py                                     # 4-subset tests for |U(A)| >= 4
python triple_certificate.py build triple_results q2k_extra.json extra_U.json direct_witnesses.json \
    triple_certificate.json --nonk-exact nonk_exact.json --nonk-u nonk_U.json
```

Layer (i) uses CaDiCaL 1.9.5 through PySAT with one incremental solver per
deleted vertex, selector literals per completion point and a conflict budget
of 20,000 per call; calls that exhaust the budget are declared (conservative:
declaring an instance can only enlarge `U(A)`).  Every model is decoded and
checked before it is stored.  The run took about 76 minutes wall clock (17,860 CPU-seconds, 5,837 solver calls, 3,653 witnesses) on four worker
processes.

## Hashes

```text
triple_certificate.json
  27bb217997885c8312a0f735cc202a3307d14eaf6679e8bb62eb49e7073732b1
packed family rows before base64
  8ef8a8431be5bd772bb5b6002ae4042ba3f56d4767e744c74a8d3706d31727fa
packed Q2K-cluster fresh rows before base64
  7a961fd644f85cc55854812736037347fb74f61a964362e581344d629699cc82
packed non-K-cluster fresh rows before base64 (empty)
  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
certificate.json (criticality sibling)   d354f9629c41639168b80fc1aa6feb6e4187dd37dee7efcb83b4ef6ebe68d16c
swap_certificate.json (sibling)          a36a11bf3e63d3ec887b0f4507d51623773b968842a964a314e364713ac46ca3
pair_certificate.json (sibling)          bba74f49405e408238394c8c1cd8a8c8fdb0a631d9d91056ece372bcb018cf40
completion_points.json (sibling)         b82909c48ce088deb89b555f4c8fa554bba44030570fdaaf0b9b607e9552a5a6
```

## Trust boundary

- Exact geometry trusts the published coordinate input, CPython integers and
  `fractions.Fraction`, SymPy 1.14.0 parsing of the coordinate expressions
  (through the sibling `parts509.py`), and the sibling tower-field
  implementation `kfield.py`.
- The 4-colourability side (items 1-3 apart from the declared instances)
  trusts only the solver-free checkers; SAT solvers were used to find
  witnesses.
- The completeness of `Q3` is the separately certified census; `Q2K` and the
  non-`K` points are enumerated here from all 129,286 vertex pairs by the
  same exact square-root test.
- The non-`K` annulus screen is floating point with an explicit error margin
  (values correct to about 1e-14, tolerance 1e-7); it only produces
  candidates, every one of which is decided exactly in `K(t1, t2)`.  Its
  completeness (no unit pair outside the tolerance) rests on the stated
  error bound of the 50-digit evaluation and the double rounding.
- The declared instances are *not* certified non-4-colourable here (solver
  reports or exhausted budgets); the theorem does not depend on them.
- `chi(G) = 5` itself is the separately reviewed sibling result.
- No proof-assistant formalisation was performed.

## Provenance

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137-166,
  <https://arxiv.org/abs/2010.12665>.
- Exact base reconstruction and deletion certificate:
  `../hadwiger_nelson_parts509_criticality`.
- One-point swap closure, completion points and tower-field tooling:
  `../hadwiger_nelson_parts509_swap_closure`.
- Two-point pair closure and its witness rows:
  `../hadwiger_nelson_parts509_pair_closure`.
