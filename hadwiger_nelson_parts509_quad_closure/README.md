# All-anchored four-point augmentation closure of the Parts 509-vertex graph (delete five, add four)

## Result and scope

Let `G` be the strict unit-distance graph on Jaan Parts's 509 points (vertex set `V`, 2,442 edges,
`chi(G) = 5`, 5-vertex-critical; `../hadwiger_nelson_parts509_criticality`), `K = Q(sqrt3, sqrt5, sqrt11)`
its coordinate field, and `Q` the set of all points of the plane outside `V` at unit distance from at least
two vertices.  `Q` is finite and known exactly from the sibling closures: every such point is an
intersection point of two unit circles around vertices, and

- `Q3` (1,158 points, exact `K`-coordinates) are those with at least three vertex neighbours
  (`../hadwiger_nelson_parts509_swap_closure/completion_points.json`; a point at unit distance from three
  points of `K^2` is their circumcentre and lies in `K^2`),
- `Q2K` (2,705 points, exact `K`-coordinates) are the `K`-rational points with exactly two vertex neighbours,
- the 135,468 non-`K` intersection points have exactly two vertex neighbours (their generating pair) and are
  at unit distance from no other point of `K^2` (`../hadwiger_nelson_parts509_triple_closure`, with the exact
  interval enclosures of `nonk_interval_certificate.json`).

The unit distances inside `Q` are known exactly as well: 3,744 among `Q3`, 4,537 between `Q2K` and `Q3`,
4,790 inside `Q2K`, and 162,584 among the non-`K` points (which form 30,160 unit triangles and 8,470
diamonds and no `K4`); non-`K` points are never adjacent to `K`-points.

Write `n_V(y)` for the number of unit neighbours of a point `y` among all 509 vertices (and `n_D(y) <= n_V(y)`
for the surviving ones after deleting `D`).  Call a 4-set `A ⊂ Q` *admissible* if every point of `A` with
`n_V = 2` has at least two unit neighbours inside `A` and every point with `n_V = 3` has at least one (the
necessary condition `m(y) >= 4 - n_V(y)` for the added points of a 5-vertex-critical graph, whose minimum
degree is 4; a point of `Q` with `n_D(y) = 1` after the deletion is covered here, not by the one-anchor closure,
which treats the points with `n_V <= 1`).  For a set
`D` of vertices write `G - D + A` for the strict unit-distance graph on `(V \ D) ∪ A`.

**Theorem (exact computer-assisted).**  For every admissible 4-set `A ⊂ Q` and every set `D ⊆ V` with
`|D| >= 5`, the graph `G - D + A` is 4-colourable.

**Corollary.**  Together with the sibling closures (delete one add none / delete two add one / delete three
add two / delete four add three, `../hadwiger_nelson_parts509_{criticality,swap_closure,pair_closure,triple_closure}`)
and the one-anchor closure (`../hadwiger_nelson_parts509_one_anchor_closure`): *every 5-chromatic
unit-distance graph with at most 508 vertices has at least five vertices outside `V`, i.e. it shares at most
503 vertices with the Parts graph.*  Proof: a 5-chromatic unit-distance graph `H` with at most 508 vertices
contains a 5-vertex-critical subgraph `H'`; the strict unit-distance graph `H''` on `V(H')` is 5-chromatic
with minimum degree at least 4 and `V(H'') = (V \ D) ∪ A` with `A ∩ V = ∅`, `|A| <= |D| - 1`.  The sibling
closures exclude `|A| <= 3` (their exceptional sets `U(A)` have at most `|A|` elements, or the 508-vertex
graphs were coloured directly).  For `|A| = 4` we have `|D| >= 5`; if some point of `A` has at most one
vertex neighbour, the one-anchor closure gives `|Û(A)| <= 1`, so `D ⊆ U(A)` is impossible; otherwise
`A ⊂ Q`, and a point `y ∈ A` has degree `|N(y) ∩ (V \ D)| + |N(y) ∩ A| <= n_V(y) + m(y)` in `H''` (n_V = number of unit neighbours among all
vertices, an upper bound for the surviving ones), so `A` is admissible and the theorem applies.  Hence `|A| >= 5`.

Combined with `../hadwiger_nelson_parts509_degree_pool_minimum`, at least one of these five points has at
most six unit neighbours in `V`.  Nothing here improves the bounds `5 <= chi(R^2) <= 7` or the 509-vertex
record.

## Reduction to a finite exact computation

- **Layering.**  If `G - D + A` is 5-chromatic then so is `G - u + A` for every `u ∈ D`, i.e.
  `D ⊆ U(A) := {u : G - u + A is 5-chromatic}`.  A proper 4-colouring `c` of `G - u` *covers* `A` if it
  extends to `A`: the points of `A` can be coloured from their free lists (colours absent from their
  surviving vertex neighbours) with distinct colours on the unit edges inside `A`.  A colouring that covers
  `A` from `G - u` still covers it after further deletions, so `u ∉ U(A)` whenever some listed colouring of
  `G - u` covers `A`.  Write `Û(A)` for the set of vertices `u` at which `A` contains a *declared* set (a set
  that no listed colouring of `G - u` covers; see below); then `U(A) ⊆ Û(A)`, and it suffices that
  `|Û(A)| <= 4` for every admissible `A`, or that `G - D + A` is coloured directly for every 5-subset
  `D ⊆ Û(A)`.
- **Minimal failing sets.**  Failing (not being covered by `c`) is monotone under supersets, and a minimal
  failing set is connected in the internal unit graph of `Q` (a disconnected list-colouring instance is
  infeasible only if a component is).  Hence for `|A| <= 4`, `c` fails on `A` iff `A` contains one of the
  minimal failing sets of `c` of size at most four: points with an empty list (necessarily in `Q3` with at
  least four vertex neighbours), unit edges of `Q3` whose two ends have the same one-element list, failing
  connected triples and failing connected 4-subsets of the `K`-internal graph (102,408 connected triples and
  1,144,333 connected 4-subsets, decided by exhaustive list-colouring tables `tables.py`), and failing non-`K`
  unit triangles and diamonds (non-`K` points have lists of at least two colours, so non-`K` paths, stars and
  4-cycles never fail, and a failing paw contains a failing triangle).
- **Enumeration (`uncovered_sets.py`).**  For each vertex `u`, all sets `A ⊂ Q` with `|A| <= 4` that no
  listed colouring of `G - u` covers are enumerated by branching: at a node `A` pick a colouring `c` that
  does not fail on `A` and branch over the minimal failing sets `B` of `c` with `|A ∪ B| <= 4`; nodes that
  contain a declared set are pruned; when one point is missing the completions are obtained by intersecting
  over the unsatisfied colourings.  Every uncovered set contains a leaf (by induction along any of its
  failing witnesses) or a declared set.  The driver (`run4.py`) tests the leaves with CaDiCaL: a satisfying
  assignment gives a new listed colouring (validated directly), otherwise (UNSAT or 20,000-conflict budget)
  the leaf is declared; it stops when the enumeration returns no leaf.  The verifier repeats the
  enumeration from scratch with the final colourings and declared sets and requires that it returns nothing.
- **Aggregation (`aggregate4.py`).**  Every declared set of size `<= 3` (11 swap points, 174 declared pairs,
  2,184 declared triples, 282 `Q2K` clusters of the sibling certificates) carries at most 4 vertices, so a
  4-set with `|Û(A)| >= 5` is a declared 4-set with five labels or contains two distinct declared sets; all
  4-sets that are unions of declared sets are enumerated (union closure within size 4), `Û(A)` is computed
  from all declared subsets, and the admissible ones with `|Û(A)| >= 5` are tested directly on every
  5-subset of `Û(A)`.

## Certificate (`certificate.json.gz`)

For every vertex `u`: 5,889 additional proper 4-colourings of `G - u` in total (2-bit packing as in the
sibling certificates) and the declared 4-sets (12,269 in total: 11,549 solver-UNSAT, 720
budget-exhausted; point references `q3:I`, `k2:I`, `n:I:J:S`), the `|Û(A)|` histogram over the
90,415 union-closed sets of size four

```text
|Û(A)| = 1: 22933, |Û(A)| = 2: 51149, |Û(A)| = 3: 15030, |Û(A)| = 4: 1258, |Û(A)| = 5: 44, |Û(A)| = 6: 1
```

the 45 admissible candidates with `|Û(A)| >= 5` and the 50 explicit proper 4-colourings of the
508-vertex graphs `G - D + A` (`D` a 5-subset of `Û(A)`), and the SHA-256 hashes of the sibling inputs.  Per-vertex run statistics (rows, declared sets, solver calls, passes, seconds) are summarised in `run_summary.txt`.
Together with the 509 base deletion colourings, the 1,190 swap-closure rows, the 1,981 pair-closure rows and
the 3,653 triple-closure rows, the listed colourings cover every set of at most four points of `Q` at every
vertex except the declared ones.

The declared 4-sets are conservative: they are sets for which the solver found no extending colouring within
the budget; 11,549 of them were reported unsatisfiable (each such `G - u + A` is then a 509-vertex
5-chromatic unit-distance graph, a "tie"), but no UNSAT answer is certified here, and the proof only uses
`U(A) ⊆ Û(A)`.

## Verification

Solver-free verifier (CPython 3.11, NumPy, SymPy only to parse the sibling coordinates; the sibling
directories must be present and `q2k_extra.json`, `nonk_exact.json` regenerated in the triple-closure
directory as described there):

```bash
python3 -m venv /scratch/parts509-quad-venv
/scratch/parts509-quad-venv/bin/pip install -r requirements.txt
/scratch/parts509-quad-venv/bin/python verify4.py certificate.json.gz --workers 2   # add --checkpoint DIR to make an interrupted run resumable
```

It checks the input hashes, rebuilds the universe of points and unit incidences from the sibling files and
compares it with the triple certificate, decodes and validates every certificate row, repeats the exhaustive
enumeration for all 509 vertices with the final colourings and declared sets (nothing may remain), re-checks
that every declared 4-set is uncovered, recomputes the aggregation and the candidate list, and validates every
direct witness exactly (vertex edges, vertex-point incidences, point-point unit edges).  Expected final lines:

```text
{"checks": {"sha256:completion_points.json": true, "sha256:swap_certificate.json": true, "sha256:pair_certificate.json": true, "sha256:ambient_w3_edges.json": true, "sha256:triple_certificate.json": true, "q2k_points": true, "q2k_incidences": true, "nonk_counts": true, "no_undeclared_uncovered_set": true, "candidates_match": true, "hist4_match": true, "direct_witnesses": true, "all_checks": true}, "undeclared_uncovered": 0, "nodes": 6191796, "stale": 274, "candidates": 45, "valid_candidates": 45, "direct_tests": 50, "hist4": {"2": 51149, "1": 22933, "3": 15030, "4": 1258, "5": 44, "6": 1}, "hist_small": {"1": 2626, "2": 11, "3": 1}, "seconds": 3196}
all_checks=true
```

(3196 s with two worker processes.)

Independent check (`independent_check.py`, importing none of the enumeration code): for chosen vertices it
re-validates the certificate rows by a direct edge scan, enumerates *completely* all independent sets of at
most four points inside the union `E(u)` of the empty-list sets of the colourings (these contain every
minimal independent uncovered set) and decides coverage by hitting the empty-list sets, and tests thousands of
further sets (perturbations of the declared sets, sets of "hot" points and their unit neighbours) by a direct
recursive list colouring (`cluster_U.extends` of the triple closure); every uncovered set must contain a
declared set.

```bash
/scratch/parts509-quad-venv/bin/python independent_check.py certificate.json.gz 0 16 21 220 347 415 --samples 20000
```

Expected: every line ends with `ok=True`, last line `all_ok=true` (all_ok=true (136s)).

## Regeneration

```bash
python build_universe.py                       # universe4.json (cache; ~20 s)
python run4.py --workers 2                     # results/u_XXX.json (resumable; 5.9 CPU-hours over the vertices (2,447 enumeration passes))
python aggregate4.py results aggregate4.json   # union closure, Û(A), candidates
python direct4.py aggregate4.json direct4.json # 4-colourings of G - D + A for the candidates
python pack4.py results aggregate4.json direct4.json certificate.json && gzip certificate.json
```

The published run used CaDiCaL 1.9.5 through PySAT (python-sat 1.8.dev24), one incremental solver per vertex
with selector literals, conflict budget 20,000, 18,158 solver calls.  Regenerated certificates differ in
the colourings found (and possibly in the declared sets) but must pass the same verifier.

## Trust boundary

- Exactness: vertex coordinates, `Q3`, `Q2K`, all unit incidences among `V ∪ Q3 ∪ Q2K` and among the non-`K`
  points, and the fact that non-`K` points have no other unit neighbours in `K^2` come from the sibling
  certificates (exact arithmetic in `K` and in the quadratic extensions `K(t1, t2)`; the float screens are
  complete by the error bounds stated there and by the interval certificate of the triple closure).
- The enumeration is an exhaustive deterministic search; its completeness argument is the connectedness of
  minimal failing sets and the branching invariant above.  The driver and the verifier share the enumeration
  code; `independent_check.py` is a different algorithm with the limited scope described above.
- SAT answers are used only for discovery: satisfying assignments are validated as colourings before use,
  and UNSAT / budget answers only enlarge `Û(A)`.
- The corollary relies on the published sibling and one-anchor closures for the cases `|A| <= 3` and for
  4-sets containing a point with at most one vertex neighbour.
