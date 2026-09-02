# No 5-chromatic unit-distance graph on at most 508 vertices inside the tie-union accumulative graphs of the Parts 509-graph

**Claim status:** exact computer-assisted theorem.  Solver-free witness certificates
(forced vertices, killing sets) replayed against an exhaustively recomputed exact edge
list, also by an independent SymPy checker; the hitting-set lower bound is proof-checked
(VeriPB on cutting-planes proofs for all pools, drat-trim on a DRAT proof of the cardinality
CNF for P25) and recomputable with two exact solvers; the reduction to "at least
four added points" rests on the committed closures of the Parts graph (vertex-criticality,
delete-2-add-1, delete-3-add-2, delete-4-add-3).

## Statement

Let G = (V, E) be Parts's 509-vertex 5-chromatic unit-distance graph (exact coordinates in
K = Q(√3, √5, √11), directory `hadwiger_nelson_parts509_criticality`).  The committed
closures show that deleting d ≤ 4 vertices and adding d − 1 completion points never gives
a 5-chromatic graph; along the way they produced 150 *ties*: 509-vertex 5-chromatic
unit-distance graphs G − D + A with |D| = |A| ≤ 3 (11 swaps, 60 pair ties from the
committed pair-replacement classification, and 79 triple ties DRAT-certified here,
`tie_results.json`; the other 43 candidate triple instances are 4-colourable).

An *accumulative graph* is the strict unit-distance graph on A* = V ∪ P for a finite set P
of K-rational completion points.  For the pools

| pool | points | vertices of A* | forced |F| | free |R| | certified bound m* (hitting sets with ≥ 4 points) | 509 − |F| |
|---|---|---|---|---|---|---|
| P25 = the 25 points used by the 150 ties | 25 | 534 | 483 | 51 | 26 (67 killing sets, 9 IHS rounds, 2 seeds merged) | 26 |
| P44 = the 44 points of all 196 candidate tie instances | 44 | 553 | 475 | 78 | 34 (170 killing sets, 28 IHS rounds) | 34 |
| P44 ∪ level-2 points around P44 (pruned) | 139 | 648 | 475 | 173 | 34 (659 killing sets incl. 237 transplanted from P25/P44, 69 IHS rounds) | 34 |

**Theorem.** None of these accumulative graphs contains a 5-chromatic subgraph with at most
508 vertices.  Equivalently: for every D ⊆ V and A ⊆ P with |A| < |D|, the unit-distance
graph G − D + A is 4-colourable — no recombination of the known ties, with any number of
deletions and additions from the pool, yields a smaller 5-chromatic graph.  The minimum
order of a 5-chromatic subgraph of each A* is exactly 509 (attained by G and by the ties).

## Method (Parts-style reduction, made exact)

* u ∈ A* is *forced* if A* − u is 4-colourable; every 5-chromatic subgraph of A* contains
  every forced vertex.  F = forced set, R = A* \ F.  (A point is never forced, since
  A* − p ⊇ G; so F ⊆ V.)  Vertices of degree ≤ 3 in the union are pruned iteratively
  (`prune_union.py`): they are never in a minimum-order 5-chromatic subgraph.
* D ⊆ R is a *killing set* if A* − D is 4-colourable.  For X ⊆ R the graph F ∪ X is
  5-chromatic iff X meets every killing set.
* *Closure constraint.*  A 5-chromatic subgraph H of A* with |H| ≤ 508 contains a
  vertex-critical 5-chromatic subgraph H' = V − D' + A' ⊇ F.  If |A'| ≤ 3, the committed
  closures (with monotonicity: un-deleting vertices keeps 5-chromaticity) force |D'| ≤ |A'|,
  so |H'| ≥ 509; hence |A'| ≥ 4 and X = H \ F contains at least 4 points of P.
  Therefore: if every set X ⊆ R that meets every killing set and contains ≥ 4 points has
  |X| ≥ 509 − |F|, then A* has no 5-chromatic subgraph on ≤ 508 vertices.
* Implicit hitting sets (`ihs_thin2.py`): exact minimum hitting set X of the killing sets
  found so far subject to |X ∩ P| ≥ 4 (HiGHS MILP, RC2 cross-check); if |X| ≥ 509 − |F|
  the theorem is certified; otherwise F ∪ X is tested by SAT (a 5-chromatic answer would
  be a record) and its 4-colouring is extended greedily to a maximal 4-colourable set C
  (the rainbow free vertices form the killing set R \ C); the sets found in a round are
  forced back in so that successive killing sets are pairwise disjoint.  For the level-2 pool
  the killing sets of the smaller pools were transplanted by greedy extension of their witness
  colourings (`seed_l2_from_p44.py`); merging them completed the bound at once.

## Certificate and verification

`certificate_<pool>.json` holds the exact coordinates of A*, a proper 4-colouring of
A* − u for every forced u, a proper 4-colouring of A* − D for every killing set D of the
final family, the free pool points, `min_points` = 4, and the bound m*.

```text
python3 tie_union_certificate.py verify certificate_P25.json                      # solver-free part
python3 independent_check.py certificate_P25.json                                 # SymPy replay, independent code
python3 tie_union_certificate.py verify certificate_P25.json --rc2 --milp         # recompute m* with two exact solvers
python3 tie_union_certificate.py pb certificate_P25.json --out card.opb           # pseudo-Boolean decision instance
roundingsat card.opb --proof-log=card.pb                                          # regenerate the cutting-planes proof
python3 tie_union_certificate.py verify certificate_P25.json --veripb card.pb --veripb-bin veripb
python3 tie_union_certificate.py card certificate_P25.json --out card.cnf         # cardinality CNF (Sinz counters)
cadical card.cnf card.drat                                                        # regenerate the DRAT proof
python3 tie_union_certificate.py verify certificate_P25.json --drat-card card.drat --drat-trim /path/to/drat-trim
```

The verifier recomputes the complete unit-distance edge list of A* by exhaustive exact
arithmetic in K (float screen with tolerance 1e-6, far above the double-precision error,
then exact confirmation of every candidate pair), replays every witness colouring, and
checks the bound m* in up to three ways: recomputing the constrained minimum hitting set
with RC2 and HiGHS; VeriPB on a RoundingSat proof of the pseudo-Boolean decision instance
(family clauses, "at least 4 pool selectors", "at most m* − 1 selectors"; proofs of 4.5 KB,
284 KB and 122 MB for the three pools, checked in seconds); and drat-trim on a CaDiCaL DRAT
proof of the cardinality CNF (Sinz sequential counters; 3.7 MB for P25, checked by drat-trim;
the 150 MB P44 proof was generated by CaDiCaL but its drat-trim check did not complete, and
the level-2 instance was not attempted with DRAT: for P44 and the level-2 pool the proof-checked
route is VeriPB only).  Proof files are regenerable; their
SHA-256 and sizes are recorded in `expected_<pool>.txt`, which also contains the output of
`independent_check.py`.

## Trust boundary

* Solver-free: forced vertices and killing sets (witness colourings replayed against the
  exhaustive exact edge list), the exact coordinates, pruning.
* The lower bound m*: VeriPB-checked cutting-planes proof of the decision instance (all pools), drat-trim-checked DRAT proof of the cardinality CNF (P25 only), and two exact solvers (RC2, HiGHS) agreeing.
* The closure constraint (≥ 4 points) depends on the committed contributions
  `hadwiger_nelson_parts509_criticality`, `..._swap_closure`, `..._pair_closure`,
  `..._triple_closure`.
* The pools are finite choices; nothing is claimed about points outside them.  Level-2
  points were enumerated exactly as all K-rational intersections of unit circles around a
  point of P44 and a point of V ∪ P44 with at least three unit neighbours in V ∪ P44
  (`level2_points.py`).
* The 79 triple ties: CaDiCaL UNSAT checked by drat-trim (hashes in `tie_results.json`;
  proofs regenerable with `tie_certify.py`).

## Files

* `tie_union_certificate.py` — build/verify (`card` writes the cardinality CNF, `pb` the OPB decision instance).
* `independent_check.py` — independent replay with SymPy arithmetic (edge list recomputed from the certificate coordinates without the main verifier's field code; all witnesses replayed).
* `ihs_thin2.py`, `forced_vertices.py`, `prune_union.py`, `seed_l2_from_p44.py`, `build_tie_union.py`,
  `build_union_all.py`, `level2_points.py`, `tie_certify.py`, `tie_swap.py` — the search
  (python-sat 1.8.dev24 / CaDiCaL 1.9.5, scipy/HiGHS, RoundingSat 2 commit d4edbf7, VeriPB 3.0.2, drat-trim); they read the scratch
  layout of the search (`HN_SCRATCH`) and are included for provenance.
* `tie_results.json` — the 79 DRAT-certified triple ties (D, A, CNF and proof hashes).
* `certificate_*.json`, `expected_*.txt`.
