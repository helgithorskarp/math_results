# The point606 core admits no nontrivial partial translation

**Exact computer-assisted theorem.** Let `P=(p_v)` be the published530-point,
2,648-unit-edge point606 core. For any real plane vector t and any choices
`epsilon_v in {0,1}`, put

```
f(v) = p_v + epsilon_v*t.
```

If f preserves the unit length of every source edge, then f is either the
identity on all vertices or translation by t on all vertices. For nonzero t,
all choices are equal. For t=0, the map is the identity irrespective of the
choices. Every such image therefore has exactly530 distinct points.

This excludes every at-most508 image in this entire class. It is a restricted
construction obstruction, not a global lower bound for unit-distance graphs,
and produces no record candidate. It covers any number of moved vertices,
any direction or magnitude of t, and every Boolean choice pattern. It does
not cover lost-edge repair, more than two displacement values, rotations,
reflections, or deleting source vertices before applying the map.

## Why this was a construction route

The source is the [certified five-chromatic point606 core](../hadwiger_nelson_point606_criticality_gate/README.md),
with an [independent accepted review](../hadwiger_nelson_point606_criticality_gate_review1/README.md).
A unit-edge-preserving image inherits its non-four-colourability: any proper
four-colouring of the image would pull back to the source. Merging at least22
pairs could therefore have crossed the physical record cap without merely
deleting vertices from a critical graph. Complete physical image edges and a
proper five-colouring would still have been needed before candidate status.

The theorem below rules out every merger in this declared operation. Its
proof needs no chromaticity assumption, SAT answer, negative solver trace or
replay of the imported parent refutation. The earlier failed
[half-plane fold](../hadwiger_nelson_point606_halfplane_fold/README.md)
lost497 source edges; the present operation explicitly requires preservation
of every source edge. Neither the source's infinitesimal rigidity nor the
separate invertible-shear theorem supplies this discrete global conclusion.

## General geometric criterion

Let a finite graph have distinct points in the plane and unit-length edges.
Partition its edges by their **unoriented unit displacement**: d and -d belong
to the same class. Suppose it has at least two classes and remains connected
after removal of any two classes.

We claim every edge-preserving map choosing independently between p_v and
p_v+t is global. Handle t=0 first as the identity. For t nonzero, write
`d=p_b-p_a` for an oriented unit edge. When the endpoint choices differ, the
new displacement is d+t or d-t. Preservation requires

```
2 d dot t = -|t|^2   or   2 d dot t = |t|^2.
```

A unit vector d satisfying these conditions lies on the unit circle and on
one of two lines perpendicular to t. There are at most four such vectors,
paired antipodally, hence **at most two unoriented edge directions** can
permit different endpoint choices. This includes tangencies and cases with
no intersections.

Every edge in every other direction forces its two choices to agree. Those
edges form a connected graph by hypothesis. If fewer than two exceptional
directions occur, pad the deletion set with another class; the graph retaining
more edges is also connected. Equality therefore propagates to all vertices.
This proves the criterion and the stated global-map conclusion.

No priority claim is made for this elementary criterion. The computational
contribution is its complete exact application to the specified physical core.

## Exact finite certificate computation

The530 coordinates are reconstructed from hash-bound published source inputs
in `Q(sqrt3,sqrt5,sqrt11)^2`, with common denominator288 and ordered basis

```
1, sqrt3, sqrt5, sqrt15, sqrt11, sqrt33, sqrt55, sqrt165.
```

All140,185 unordered source pairs are checked exactly, giving2,648 unit edges.
Their displacement vectors give36 unoriented direction classes. Because all
these vectors have unit length, parallel directions are exactly equality up
to sign; linear independence of the displayed radical basis makes the
coefficient comparison exact.

For each of the630 unordered pairs of direction classes, the verifier removes
all edges in those classes, constructs a spanning tree and checks its529
edge memberships. Every retained graph is connected, with between2,330 and
2,646 edges. The333,270 tree-edge checks and the general criterion certify the
entire real-parameter/Boolean-choice class. No enumeration of translations
or2^530 choice patterns is needed.

The source and compact expected results are the reproducible certificate
computation. Expanded spanning trees are generated in memory and not committed.
Their stream hash is only a regression check; it is not a substitute for the
regenerated connectivity and tree-edge checks.

## Reproduction and validation

From a complete repository checkout, using CPython3.11+ and the standard library:

```sh
python3 -B hadwiger_nelson_point606_partial_translation/verify.py
python3 -B -O hadwiger_nelson_point606_partial_translation/verify.py
python3 -B hadwiger_nelson_point606_partial_translation/audit.py
python3 -B hadwiger_nelson_point606_partial_translation/controls.py
```

Expected fields include `direction_pair_deletions=630`,
`all_retained_graphs_connected=true`,
`all_edge_preserving_partial_translations_global=true`,
`minimum_image_order_in_declared_class=530`, and `record_candidate=false`.

The second audit shares only the source coordinate loader with the primary
geometric calculation. It rejects nonunit pairs modulo1321 using checked
radical roots and decides survivors by generic square-free-radical products.
It uses the opposite canonical direction sign, compares the entire edge set
and direction partition, and rechecks every deletion by disjoint-set unions
instead of breadth-first traversal. This is same-author validation, not
independent peer review.

Controls explicitly fold a four-point unit diamond to three points by a
partial translation. All16 Boolean choices are compared with hand-derived
conditions; exactly two give three-point unit-edge-preserving images. Its
direction-connectivity hypothesis correctly fails. Separate abstract K4 and
disconnected-graph controls test the graph layer; K4 is not offered as a
physical unit graph. Zero displacements are rejected as direction labels.
Normal and optimized full verifier outputs agree.

The trust boundary is the exact coordinate input and loader, ordinary Python
integer/collection arithmetic, the finite edge and connectivity checks, and
the unformalized geometric argument above. The parent loader also verifies
its own input manifest. The chromatic certificates stored in that parent
package are not replayed and are not premises of this geometric exclusion.
No proof-assistant formalization is claimed.

## Boundary

Retire this entire identity-or-one-translation operation on the frozen source.
Do not add another displacement level, change parent or permit lost-edge
repair merely because this exclusion is complete. Those would be separate
construction selections requiring new positive physical evidence and a capped
obstruction mechanism.

The unrestricted published record remains509 vertices
([Parts](https://arxiv.org/abs/2010.12665)). This result makes no claim about
arbitrary smaller plane graphs or other maps of the530-point source.
