# A vertex-critical K2,3-free five-chromatic abstract graph on 301 vertices

This package gives a vertex-critical, exactly five-chromatic **abstract** graph
with 301 vertices and 1,452 edges. It contains neither `K2,3` nor `K4`. The
graph is an induced core of a repaired member of the earlier
[H516 degree-four surgery family](../hadwiger_nelson_h516_degree4_surgeries),
and it removes the elementary geometric obstruction that closed all 53,276
members of that family.

The 301-vertex graph has not been realized as a unit-distance graph in the
Euclidean plane. It therefore does not improve the 509-vertex unit-distance
record. Its value is a positive realization interface: it is far below the
target order, passes the first two necessary planar unit-distance gates, and
carries a machine-checked chromatic obstruction.

## Construction

Start with labelled case 24 (zero-based order in the complete surgery family):

```
(102; 75=105), (109; 76=106), (293; 272=281), (299; 273=276).
```

Each triple deletes the degree-four centre and identifies the displayed
nonadjacent pair of its neighbours. The resulting 508-vertex quotient has
2,520 edges, no `K4`, and six vertex pairs with at least three common
neighbours. Delete

```
0-142, 0-145, 0-146, 0-149, 15-119, 15-120.
```

This leaves the 2,514-edge [`parent508.json`](parent508.json), which has neither
`K2,3` nor `K4` and is not four-colourable. The checker proves that six is the
minimum number of deletions capable of hitting all twelve `K2,3` triple
constraints in this parent: there are 14,400 minimum hitting sets. A bounded
solver screen found the displayed repair at zero-based rank 11, after eleven
four-colourable repairs.

An UNSAT-core reduction followed by a deterministic label-order deletion pass
found the induced 301-vertex [`graph.json`](graph.json). The published claim
does not trust that minimization procedure: explicit proper four-colourings in
[`vertex_deletion_colours.json`](vertex_deletion_colours.json) independently
show that deleting any one of the 301 final vertices makes the graph
four-colourable. Five of the six parent edge deletions remain relevant in the
core. Those five are again minimum for eliminating its five `K2,3` apex pairs;
there are 2,400 minimum five-edge hitting sets.

The four nontrivial quotient classes are represented by labels `75`, `76`,
`272`, and `273`. Their final degrees are 13, 13, 14, and 15. The other 297
vertices retain labels and coordinate provenance from the exact H516 source,
but the four merged classes do not yet have plane coordinates.

## Exact chromatic certificate

[`five_colouring.json`](five_colouring.json) is a directly checked proper
five-colouring. [`four_colour.cnf`](four_colour.cnf) encodes four-colourability
with 1,204 variables and 6,112 clauses, including three sound triangle pins.
The committed [`four_colour.lrat`](four_colour.lrat) refutes that CNF.

DRAT-trim accepted the generated DRAT and retained 7,971 lemmas using 685,802
resolution hints. The strict positive-hint checker then accepted all 7,971
LRAT additions and the final empty clause. Combined with the five-colouring,
this proves chromatic number exactly five. Combined with the 301 explicit
vertex-deletion colourings, it proves vertex-criticality. The solver runs
alone are not trusted as proofs.

The standard-Python checker reconstructs both graphs from the exact published
H516 source, enumerates all common-neighbour and `K4` obstructions, proves the
two minimum edge-deletion claims, validates all 302 colourings, rebuilds the
CNF byte for byte, and rejects three mutations. It does not import the producer
or invoke a solver.

## Reproduction

From the repository root:

```sh
python3 -B hadwiger_nelson_h516_k23free_edge_repair/verify.py --work /tmp/h516-edge-repair-check
g++ -O3 -std=c++17 hadwiger_nelson_h516_k23free_edge_repair/strict_lrat.cpp -o /tmp/h516-strict-lrat
/tmp/h516-strict-lrat hadwiger_nelson_h516_k23free_edge_repair/four_colour.cnf hadwiger_nelson_h516_k23free_edge_repair/four_colour.lrat
```

Expected: 301 vertices, 1,452 edges, minimum degree four, zero final `K2,3`
pairs, zero `K4`, 301 accepted deletion colourings, and
`VERIFIED_STRICT_RUP_LRAT` with 7,971 accepted additions.

To replay the bounded 508-vertex parent-repair screen, install
`python-sat==1.9.dev15` and run:

```sh
python3 -B hadwiger_nelson_h516_k23free_edge_repair/produce.py --work /tmp/h516-edge-repair-producer
```

[`prove.py`](prove.py) can generate a fresh DRAT proof for the final CNF with
Glucose42. Check a fresh proof independently with DRAT-trim before accepting
it; proof bytes may vary by version. The committed LRAT is the stable proof
artifact.

## Realization boundary

No plane realization, rigidity theorem, or nonrealizability theorem is claimed.
A realization may move all 301 vertices; fixing the inherited 297 coordinates
is only one possible restricted model. The next useful step is an exact or
certified realization of this graph, or a further constraint repair that keeps
an independently checked non-four-colourability certificate while admitting
coordinates.
