# Two-point augmentation closure of the Parts 509-vertex graph

## Result and scope

Let `G` be the strict unit-distance graph on Jaan Parts's 509 algebraic points
(vertex set `V`, 2,442 edges, `chi(G) = 5`, 5-vertex-critical; see
`../hadwiger_nelson_parts509_criticality`), and let `Q3` be the exact list of
the 1,158 points of the plane outside `V` at unit distance from at least three
Parts vertices (`../hadwiger_nelson_parts509_swap_closure/completion_points.json`).
For a set `D` of vertices and points `q1, q2`, write `G - D + q1 + q2` for the
strict unit-distance graph on `(V \ D) ∪ {q1, q2}` (it contains the edge
`q1 q2` exactly when the two points are at unit distance).

The evidence in this directory establishes, with exact arithmetic throughout:

1. **Pair closure.**  For every vertex `u` and every pair `{q1, q2}` of
   distinct points of `Q3`, the graph `G - u + q1 + q2` is 4-colourable, except
   for exactly 12,901 declared instances `({q1, q2}, u)`.  Of these,
   12,727 contain a certified swap point of `u` (so `G - u + q1` is
   already 5-chromatic) and 174 are new: `G - u + q1 + q2` is a
   510-vertex 5-chromatic unit-distance graph although both `G - u + q1` and
   `G - u + q2` are 4-colourable.  (The non-4-colourability of the declared
   instances is a solver report, not part of the certificate; see the trust
   boundary.)

2. **Small deletion sets.**  Write `U(A)` for the set of vertices `u` with
   `({q1, q2}, u)` declared.  The distribution of `|U(A)|` over the
   12,838 pairs with non-empty `U(A)` is

   ```text
   |U(A)| = 1: 12,775 pairs;  |U(A)| = 2: 63 pairs;  |U(A)| >= 3: none
   ```

   No pair has three or more critical deletion vertices, so no direct 508-vertex test was needed: the closure below follows from the pair witnesses alone.  The 63 pairs with two critical vertices are the 55 pairs of distinct swap points (each contributing its own swap vertex), the six pairs of degree-10 points among the four such points with U = {350, 353}, and the pairs (43, 60), (43, 658), (96, 139), (133, 175) (indices into the Q3 list; the second member of each of these U sets is solver-reported).

3. **No 508 by "delete three, add two".**  For every three-element set
   `D ⊂ V` and every two distinct points `q1, q2` of the plane, the strict
   unit-distance graph on `(V \ D) ∪ {q1, q2}` is 4-colourable.  No 5-chromatic
   unit-distance graph on 508 vertices arises from the Parts graph by deleting
   three vertices and adding two points of the plane.

Item 3 extends the one-point swap closure (`../hadwiger_nelson_parts509_swap_closure`:
no 508 by deleting two vertices and adding one point) by one more deleted
vertex and one more added point.  Nothing here improves the bounds
`5 <= chi(R^2) <= 7` or the 509-vertex record.

## Reduction to a finite exact computation

- **Which points matter.**  Let `|D| = 3`.  If `q1 ∈ V`, then
  `G - D + q1 + q2 = G - D' + q2` with `|D'| <= 2` (or `<= 3` with `q2` as the
  only new point), which is 4-colourable by the swap closure.  If `q1 ∉ V` has
  at most two unit neighbours in `V`, then `q1` has degree at most 3 in
  `G - D + q1 + q2` (its only other possible neighbour is `q2`), so any proper
  4-colouring of `G - D + q2` extends to it, and `G - D + q2` is 4-colourable by
  the swap closure.  Hence a 5-chromatic `G - D + q1 + q2` needs both points in
  `Q3`, whose completeness (every point with at least three unit neighbours is
  the circumcentre of three of them, hence lies in `K^2`,
  `K = Q(sqrt3, sqrt5, sqrt11)`, and is found by the exact pair-intersection
  enumeration) is certified by the swap-closure directory and, by an
  independent circumcircle count, by the sibling census.
- **Layering.**  If `G - D + A` is 5-chromatic for `A = {q1, q2}`, then so is
  its supergraph `G - u + A` for every `u ∈ D`; that is, `D ⊆ U(A)`.  So it
  suffices to (a) exhibit, for every `(A, u)` outside the declared list, a
  proper 4-colouring of `G - u` that extends to both points, and (b) for every
  pair `A` with `|U(A)| >= 3` and every 3-subset `D ⊆ U(A)`, exhibit a proper
  4-colouring of `G - D + A` directly.
- **Extension test.**  A proper 4-colouring `c` of `G - u` extends to `A` if
  and only if each point has a free colour (a colour absent from its surviving
  unit neighbours) and, when `q1 q2` is a unit edge, the two free-colour sets
  are not the same singleton.  A colouring that extends to `A` from `G - u`
  still extends after deleting further vertices, which gives (a) for every
  `D ∋ u`.
- **Exact incidences.**  All point–vertex and point–point unit distances are
  recomputed by the verifier with integer arithmetic in the basis of `K`
  (coordinates scaled by the common denominator 288), independently of the
  committed lists; the integer test also re-derives the 2,442 base edges.

## Certificate

`pair_certificate.json` contains, for every vertex `u`, additional proper
4-colourings of `G - u` (1,981 rows in total, at most 17 per vertex,
packed as in the sibling certificates), the declared instances per vertex, the
pairs with `|U(A)| >= 2`, and zero explicit proper 4-colourings of
508-vertex graphs `G - D + A` for all 3-subsets `D` of every `U(A)` with at
least three members.  Together with the 509 base deletion colourings and the
1,190 swap-closure family rows it covers all
`C(1158, 2) * 509 = 340,980,627` instances except the declared ones.

## Verification

Solver-free primary verifier (CPython 3.11, NumPy for the coverage matrices,
SymPy only for parsing the published coordinate expressions through the
sibling `parts509.py`; the sibling directories must be present):

```bash
python3 -m venv /scratch/parts509-pair-venv
/scratch/parts509-pair-venv/bin/pip install -r requirements.txt
/scratch/parts509-pair-venv/bin/python pair_certificate.py verify \
  ../hadwiger_nelson_parts509_swap_closure/completion_points.json pair_certificate.json
```

This re-enumerates all completion points exactly (about six minutes with eight
processes; `--skip-enumeration` reuses the committed list, whose hash is
checked against the swap-closure certificate), recomputes all unit distances
among the 1,667 points of `V ∪ Q3` exactly, decodes every colouring, checks
8,951,669 retained-edge inequalities, replays the coverage of all pair
instances, and checks every triple witness.  Expected summary:

```text
all_checks=true
q3_points=1158  q3q3_unit_pairs=3744  pairs=669903  pair_instances=340980627
colourings_checked=3680  retained_edge_checks=8951669
declared_instances=12901  pairs_with_nonempty_U=12838  U_histogram={1: 12775, 2: 63}
pairs_with_U_ge3=0  triple_instances_needed=0  triple_witnesses_checked=0
```

Independent checker, importing none of the primary code (coordinates parsed
into SymPy's `AlgebraicField`, completion points rebuilt from their rational
coefficient vectors and checked against the field elements; point–vertex and
point–point unit distances decided exactly by an exact rejection screen through
two ring homomorphisms `K -> F_p` followed by `AlgebraicField` confirmation of
every surviving pair, so that no unit pair can be missed; own row decoder,
pure-Python bitmask coverage):

```bash
/scratch/parts509-pair-venv/bin/python independent_pair_check.py \
  ../hadwiger_nelson_parts509_swap_closure/completion_points.json pair_certificate.json
```

It must report `all_checks: true` with the same counts (about 35 minutes on
a loaded machine; the SymPy parse of the published expressions dominates).

The 63 pairs with two critical deletion vertices are natural candidates for
further 509-vertex 5-chromatic graphs `G - U(A) + A`; they are not examined
here and no claim is made about them.

## Regeneration

```bash
/scratch/parts509-pair-venv/bin/python pair_closure.py --workers 6          # layer 1, writes pair_results/
/scratch/parts509-pair-venv/bin/python pair_closure_layer2.py                # layers 2-3, writes pair_layer2_results.json
/scratch/parts509-pair-venv/bin/python pair_certificate.py build \
  pair_results pair_layer2_results.json \
  ../hadwiger_nelson_parts509_swap_closure/completion_points.json /scratch/pair_certificate_new.json
```

Layer 1 uses CaDiCaL 1.9.5 through PySAT with one incremental solver per
deleted vertex, selector literals per completion point, and greedy coverage;
every model is decoded and checked before it is stored.  `ambient_w3_edges.json`
(exact unit pairs of `V ∪ Q3`, regenerated by `ambient_edges.py`) is used only
by the generator; the verifier recomputes all incidences.  Regenerated
certificates may contain different valid colourings and therefore different
hashes.  The layer-1 run took about 28 minutes (1,700 s wall clock, shared with other jobs) on six worker processes.

## Hashes

```text
pair_certificate.json
  bba74f49405e408238394c8c1cd8a8c8fdb0a631d9d91056ece372bcb018cf40
packed family rows before base64
  f05afa788baf8f5a73abf5a7c52d116f56e2f5ccf96367cd9a9a763690d60c38
packed triple rows before base64
  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
completion_points.json (sibling)  b82909c48ce088deb89b555f4c8fa554bba44030570fdaaf0b9b607e9552a5a6
swap_certificate.json (sibling)   a36a11bf3e63d3ec887b0f4507d51623773b968842a964a314e364713ac46ca3
exact 2442-edge list              5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c
```

## Trust boundary

- Exact geometry trusts the published coordinate input, CPython integers and
  `fractions.Fraction`, SymPy 1.14.0 parsing and denesting of the coordinate
  expressions (through the sibling `parts509.py`), and the sibling tower-field
  implementation `kfield.py`; the independent checker replaces the last two by
  SymPy's `AlgebraicField` arithmetic.
- The 4-colourability side (items 1–3 apart from the declared instances)
  trusts only the solver-free checkers; SAT solvers were used to find
  witnesses.
- The completeness of `Q3` is the separately certified census (exact
  pair-intersection enumeration, re-run by the verifier, and the independent
  circumcircle count of the sibling census).
- The declared instances are *not* certified non-4-colourable here: they are
  solver reports (CaDiCaL 1.9.5 via PySAT) recorded for completeness, and the
  theorem does not depend on them.  The 12,727 swap-implied instances
  inherit the DRAT-verified status of the eleven swaps.
- `chi(G) = 5` itself is the separately reviewed sibling result.
- No proof-assistant formalisation was performed.

## Provenance

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137–166,
  <https://arxiv.org/abs/2010.12665>.
- Exact base reconstruction and deletion certificate:
  `../hadwiger_nelson_parts509_criticality`.
- One-point swap closure, completion points and tower-field tooling:
  `../hadwiger_nelson_parts509_swap_closure`.
