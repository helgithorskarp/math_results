# No 5-chromatic unit-distance graph on at most 508 vertices inside the degree-7 completion pool of the Parts 509-graph

**Claim status:** exact computer-assisted theorem.  Solver-free witness certificates
(forced vertices, killing sets) replayed against an exhaustively recomputed exact edge
list, also by an independent SymPy checker; the constrained hitting-set lower bound is
proof-checked (VeriPB on a RoundingSat cutting-planes proof of the decision instance) and
recomputable with two exact solvers; the reduction to "at least four added points" rests on
the committed closures of the Parts graph (vertex-criticality, delete-2-add-1,
delete-3-add-2, delete-4-add-3).

## Statement

Let G = (V, E) be Parts's 509-vertex 5-chromatic unit-distance graph with exact coordinates
in K = Q(√3, √5, √11) (directory `hadwiger_nelson_parts509_criticality`).  For k ≥ 3 let

    P_k = { p ∈ K² \ V : p is at unit distance from at least k vertices of V }

be the level-1 completion points of degree ≥ k.  Every point of the plane at unit distance
from ≥ 3 vertices of V is the circumcentre of three points of K² and lies in K², so P_3 is
the set of *all* plane points with ≥ 3 vertex neighbours; it has 1,158 points (exact
enumeration in `hadwiger_nelson_parts509_swap_closure`, list `completion_points.json`), with
degree histogram 3:461, 4:322, 5:180, 6:119, 7:29, 8:27, 9:16, 10:4.  Hence P_k is a
canonical, definition-level pool (no choice of ties or search history enters it).  The
accumulative graph A_k is the strict unit-distance graph on V ∪ P_k.

| pool | points | vertices of A_k | unit edges | forced F | free R | certified bound m* (hitting sets with ≥ 4 points) | 509 − F |
|---|---|---|---|---|---|---|---|
| P_7 (points with ≥ 7 vertex neighbours) | 76 | 585 | 3,083 | 451 | 134 = 58 vertices of G + 76 points | 58 (425 killing sets, 337 inclusion-minimal, sizes 2–15; 50 IHS rounds, 1,325 SAT calls, 579 s) | 58 |

**Theorem.** A_7 contains no 5-chromatic subgraph with at most 508 vertices.  Equivalently:
for every D ⊆ V and every A ⊆ P_7 with |A| < |D| the unit-distance graph G − D + A is
4-colourable.  The minimum order of a 5-chromatic subgraph of A_7 is exactly 509 (attained
by G).  Since P_8, P_9, P_10 ⊆ P_7, the same holds for A_8, A_9, A_10.

**Corollary (with the committed closures).** Every 5-chromatic unit-distance graph H on at
most 508 vertices contains a point outside V with at most 6 unit neighbours in V.  (A
vertex-critical 5-chromatic subgraph H' ⊆ H whose extra points all had ≥ 7 vertex
neighbours would be a subgraph of A_7.)  Together with the committed closures, H shares at
most 504 vertices with G, contains at least four points outside V, and at least one of them
has at most 6 vertex neighbours.

## Method

Identical to `hadwiger_nelson_parts509_tie_union_minimum` (forced vertices, killing sets,
closure constraint |X ∩ P| ≥ 4, implicit hitting sets with disjoint layers, HiGHS MILP with
RC2 cross-check); see that directory's README for the definitions and for the proof that a
5-chromatic subgraph on ≤ 508 vertices must contain ≥ 4 pool points.  In brief: u ∈ A_k is
*forced* if A_k − u is 4-colourable (every 5-chromatic subgraph contains u; points are never
forced since A_k − p ⊇ G), D ⊆ R = A_k \ F is a *killing set* if A_k − D is 4-colourable,
and F ∪ X is 5-chromatic iff X ⊆ R meets every killing set; the theorem follows once every
hitting set of the certified family with ≥ 4 pool points has size ≥ 509 − |F|.  The forced
scan tested all 585 single deletions (CaDiCaL, `forced_vertices.py`); the implicit
hitting-set search (`ihs_thin2.py`, seed 1) certified the bound 58 after 50 rounds.

## Certificate and verification

`certificate_D7.json` holds the exact coordinates of A_7, a proper 4-colouring of A_7 − u
for every forced u, a proper 4-colouring of A_7 − D for every killing set D of the final
family, the pool, `min_points` = 4 and the bound m* = 58.

```text
python3 tie_union_certificate.py verify certificate_D7.json                      # solver-free part
python3 independent_check.py certificate_D7.json                                 # SymPy replay, independent code
python3 tie_union_certificate.py verify certificate_D7.json --rc2 --milp         # recompute m* with two exact solvers
python3 tie_union_certificate.py pb certificate_D7.json --out card.opb           # pseudo-Boolean decision instance
roundingsat card.opb --proof-log=card.pb                                          # regenerate the cutting-planes proof (742 s, 381 MB)
python3 tie_union_certificate.py verify certificate_D7.json --veripb card.pb --veripb-bin veripb   # VeriPB check (34 s)
python3 build_degree_pools.py completion_points.json out 7                       # rebuild the pool (ambient indices)
```

Expected output in `expected_D7.txt` (all checks true; 3,083 exact edges; 451 + 425 witness
colourings; RC2 = HiGHS = 58; VeriPB VERIFIED UNSATISFIABLE; proof hashes; independent check
PASSED).  The verifier recomputes the complete unit-distance edge list of A_7 by exhaustive
exact arithmetic in K (float screen with tolerance 1e-6, then exact confirmation of every
candidate pair), replays every witness colouring, and checks the bound in three ways.  The
cutting-planes proof is regenerable and not committed (381 MB); its SHA-256 is recorded.  A
DRAT route for the cardinality CNF was not attempted for this pool.

## Trust boundary

* Solver-free: forced vertices and killing sets (witness colourings replayed against the
  exhaustive exact edge list, by two independent implementations), the exact coordinates.
* The lower bound m* = 58: VeriPB-checked cutting-planes proof of the decision instance, and
  two exact solvers (RC2, HiGHS) agreeing.  VeriPB and the exact-arithmetic replay are the
  trust base.
* The closure constraint (≥ 4 points) depends on the committed contributions
  `hadwiger_nelson_parts509_criticality`, `..._swap_closure`, `..._pair_closure`,
  `..._triple_closure`.
* The pool P_7 is defined by the exact level-1 completion enumeration of the swap closure
  (points with ≥ 3 vertex neighbours are K-rational, so the enumeration is complete).
  Nothing is claimed about points with ≤ 6 vertex neighbours.

## Files

* `tie_union_certificate.py`, `independent_check.py` — verifier and independent checker
  (copies of the tie-union tools; `pb` writes the OPB decision instance).
* `build_degree_pools.py` — builds `union_deg{k}.json` (ambient indices: V = 0..508, point q
  of `completion_points.json` = 509 + q) from the level-1 completion list.
* `forced_vertices.py`, `ihs_thin2.py` — the search (python-sat 1.8.dev24 / CaDiCaL 1.9.5,
  scipy/HiGHS, RoundingSat 2 commit d4edbf7, VeriPB 3.0.2); they read the scratch layout of
  the search and are included for provenance.
* `certificate_D7.json`, `expected_D7.txt`.
