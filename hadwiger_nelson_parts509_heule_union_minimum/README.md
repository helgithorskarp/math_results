# No 5-chromatic unit-distance graph on at most 508 vertices inside the union of the Parts 509-graph and Heule's 510-vertex graph

**Claim status:** exact computer-assisted theorem.  Solver-free witness certificates (forced vertices,
killing sets) replayed against an exhaustively recomputed exact edge list of the union, also by an
independent SymPy checker; the hitting-set lower bound is proof-checked (VeriPB on a RoundingSat
cutting-planes proof) and recomputable with two exact solvers (RC2, HiGHS); the reduction to "at least
four added points" rests on the committed closures of the Parts graph (vertex-criticality,
delete-2-add-1, delete-3-add-2, delete-4-add-3; with the one-anchor and all-anchored delete-5-add-4
closures the true constraint is even "at least five", which is not needed).

## Statement

Let G = (V, E) be Parts's 509-vertex 5-chromatic unit-distance graph (exact coordinates in
K = Q(√3, √5, √11), directory `hadwiger_nelson_parts509_criticality`) and let H be Marijn Heule's
510-vertex 5-chromatic unit-distance graph (`510.vtx` of the CNP-SAT repository, same coordinate field,
2,504 unit edges).  Among the isometries of the plane that map three or more vertices of H onto vertices
of G with K-rational rotation (`align.py`: origin-fixing rotations/reflections determined by pairs of
points at equal distance from the origin, verified exactly), the one with the largest overlap identifies
466 vertices of H with vertices of G (`aligned_510.json`).  The *union* A* = V ∪ H is the strict
unit-distance graph on the 553 distinct points (all in K²): 2,776 exact unit pairs
(2,442 inside V, 16 between two Heule-only points, 318 between a Heule-only point and V); all
2,504 edges of H and all 2,442 edges of G are among them.

**Theorem.**  A* has no 5-chromatic subgraph with at most 508 vertices.  Equivalently, for every
D ⊆ V and A ⊆ H \ V with |A| < |D| the unit-distance graph G − D + A is 4-colourable: no recombination
of the two record-size constructions at this alignment yields a smaller 5-chromatic graph.  The minimum
order of a 5-chromatic subgraph of A* is exactly 509 (attained by G).

## Method (as in the tie-union theorem, `hadwiger_nelson_parts509_tie_union_minimum`)

* u ∈ A* is *forced* if A* − u is 4-colourable; every 5-chromatic subgraph of A* contains every
  forced vertex.  Here F = 447 vertices (all in V ∩ H), free set R = A* \ F of 106 vertices
  (62 of V, 44 Heule-only points, the 44 Heule-only points are never forced since A* − p ⊇ G).
* D ⊆ R is a *killing set* if A* − D is 4-colourable; X ⊆ R gives a 5-chromatic F ∪ X iff X meets
  every killing set.
* Closure constraint: a 5-chromatic subgraph of A* on ≤ 508 vertices contains a vertex-critical one
  V − D' + A' ⊇ F with A' ⊆ H \ V; the committed closures force |A'| ≥ 4 (|A'| ≤ 3 would give
  |D'| ≤ |A'|).  Hence it suffices that every X ⊆ R meeting all killing sets with |X ∩ (H \ V)| ≥ 4
  has |X| ≥ 509 − |F| = 62.
* Implicit hitting sets (`ihs_thin2.py`, seed 1): 41 rounds, 383 killing sets, exact minimum
  constrained hitting set 62 (HiGHS MILP; RC2 cross-check 62); every intermediate hitting set
  X had F ∪ X 4-colourable (its extension gave the next killing sets, in disjoint layers).

## Certificate and verification

`certificate_H510.json` (0.55 MB): the exact coordinates of all 553 vertices with provenance
(`P`, `510`, `P+510`), the forced vertices with one witness colouring each, the killing sets with witness
colourings, the field `min_points = 4`, and the claimed minimum 62.

```bash
python3 -m venv /scratch/heule-union-venv && /scratch/heule-union-venv/bin/pip install -r requirements.txt
/scratch/heule-union-venv/bin/python union_certificate.py verify certificate_H510.json --rc2 --milp   # exact edge list, witnesses, two exact hitting-set solvers
/scratch/heule-union-venv/bin/python union_certificate.py pb certificate_H510.json --out card.opb      # decision instance "hitting set of size <= 61 with >= 4 points"
roundingsat card.opb --proof-log=card.pb && veripb card.opb card.pb                                    # VERIFIED UNSATISFIABLE
/scratch/heule-union-venv/bin/python independent_check.py certificate_H510.json                        # SymPy rebuild of the edge list + witness replay
```

Expected output: `expected_H510.txt` (verify with `--veripb card.pb`: all_checks=true; proof file hashes
listed there; the proof is regenerable and not committed).

## Regeneration of the search inputs

`align.py 510.vtx --reflect --out aligned_510.json` (Heule's `510.vtx`, sha256 `66defa1743e64073776ed4c6a2e9c496abbd4628bf7d973dcc07cf834ce35b37`, from github.com/marijnheule/CNP-SAT, not redistributed here), `union_graph.py aligned_510.json union_510.json` (exact union points/edges), `make_union_inputs.py` (search inputs `tu_H510.json`/`ambient_H510.json`), `forced_vertices.py 1 tu_H510.json forced_H510.json` and `ihs_thin2.py --seed 1 --tag _H510 --union tu_H510.json --forced forced_H510.json --ambient ambient_H510.json --min-points 4` (environment: `HN_ROOT` = scratch tree holding `completion_points.json`/outputs, `CADICAL`, `DRAT_TRIM`; the searches need CaDiCaL and PySAT, the certificate needs none of the search outputs beyond what `union_certificate.py build` packs).

## Trust boundary

Exact arithmetic in K for all coordinates and unit incidences (the union edge list is recomputed
exhaustively by the verifier and by the SymPy checker).  Witness colourings are checked directly.  The
bound "no constrained hitting set of size ≤ 61" is certified by a VeriPB-checked cutting-planes
proof and recomputed by RC2 and HiGHS.  The closure constraint relies on the committed closures.  The
alignment is one specific isometry (the maximum-overlap K-rational one); other relative placements of
the two graphs define other unions, not covered here.  Nothing here improves 5 ≤ χ(ℝ²) ≤ 7 or the
509-vertex record.

## Sources

Heule, *Computing small unit-distance graphs with chromatic number 5*, Geombinatorics 28 (2018), arXiv:1805.12181;
data `github.com/marijnheule/CNP-SAT` (510.vtx/510.edge).  Parts, *Graph minimization, focusing on the example of
5-chromatic unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), arXiv:2010.12665.
