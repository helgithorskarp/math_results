# A two-list extension mechanism for the fixed 122 completion centres

Let H be the archived 510-point Heule support. Let F be the fixed list of
122 points in `../hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json`.
All graphs here are strict Euclidean unit-distance graphs: every pair of
distinct points at distance exactly one is an edge. This package studies
the interactions inside F and between F and H, not the enumeration that
originally found F.

## Exact finite incidence statement

The graph induced by F has 122 vertices, 57 edges and 66 components:

| Component order | Multiplicity | Edges in each component |
|---:|---:|---:|
| 1 | 55 | 0 |
| 2 | 7 | 1 |
| 4 | 1 | 3 |
| 6 | 2 | 5 |
| 37 | 1 | 37 |

The first 65 components are trees. The 37-vertex component is unicyclic,
with its unique cycle, in cyclic order,

```
1239 -- 1370 -- 1522 -- 1371 -- 1239.
```

These are the archived `centre_index` labels, not H vertex indices.
The full edge list, component membership and old attachment sets are in
`certificate.json` and the pinned input table. All 7,381 unordered F pairs
and all 62,220 F-by-H pairs have been checked. There are 551 F-to-H edges.
The finite domain is complete simply by taking every pair in these two
explicit finite Cartesian domains; no geometric symmetry reduction is used.

The coordinates lie in Q(sqrt(3),sqrt(5),sqrt(11)), in the ordered basis
`(1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165)`. The eight basis
elements are linearly independent over Q: 3,5,11 generate independent
square classes, so their multiquadratic extension has degree eight.
Thus exact squared distance is one if and only if its coefficient vector
is `(1,0,0,0,0,0,0,0)`. All 632 points are distinct, with common
coefficient denominator 96.

The producer uses rational coefficient vectors and XOR multiplication.
The checker instead uses sparse dictionaries indexed by squarefree
radicands. It expands each square using its diagonal terms and twice each
unordered cross term; for squarefree a,b it uses
`sqrt(a*b) = gcd(a,b) * sqrt(a*b/gcd(a,b)^2)`.
It uses arbitrary-precision integers at scale 96 and imports no producer
code. The complete 69,601 squared-distance vectors agree entry by entry
in the local replay. A fresh standalone replay also verifies the complete
edge and attachment data without that transcript.

For the combinatorial decomposition, the producer uses graph traversal
and simultaneous leaf removal. The checker uses union-find to build a
spanning forest; exactly one non-tree edge occurs, and its forest path
recovers the displayed four-cycle. This verifies the component structure
entry by entry, not just by agreement of aggregate counts.

## Two-choosability

**Lemma.** A graph whose components are trees or trees attached to a single
even cycle is two-choosable. Consequently the graph induced by F and every
one of its subgraphs are two-choosable.

Here two-choosable means that every assignment of at least two allowed
colours to each vertex admits a proper colouring using those lists. The
colour universe need not have four elements.

**Proof.** First reduce each list to an arbitrary two-element sublist. In
a tree, choose a root colour and then colour outward: at each new vertex
at most its parent's colour is forbidden.

For an even cycle, if all two-element lists are equal, alternate their
two colours. Otherwise two consecutive vertices u,v have different
two-element lists. Choose at u a colour in its list but outside v's
list. Follow the cycle from u in the direction that visits v last,
greedily avoiding the preceding colour. There are two choices at each
step before excluding that preceding colour. At the last vertex v, the
colour of u is already absent from v's list, so the closing edge causes
no additional obstruction. Finally extend outward through all trees
attached to the cycle. Components are independent. Restricting a
two-choosable graph to a subgraph preserves two-choosability: extend the
given lists arbitrarily to omitted vertices, colour the full graph and
restrict. QED.

As a finite control specific to the four-colour application, the checker
also tests every one of the 6^4 = 1,296 assignments of two-element subsets
of `{0,1,2,3}` to the certified four-cycle, against all proper four-colour
assignments on that cycle. The proof for arbitrary lists is the argument
above, not an extrapolation from this finite control.

## Uniform extension criterion, with arbitrary deletions

**Corollary.** Let O be any subset of H and Q any subset of F. Let c be a
proper four-colouring of the graph induced by O. If, for every v in Q,
the retained old neighbours `N_H(v) intersect O` use at most two distinct
colours under c, then c extends to a proper four-colouring on O union Q.

**Proof.** Give v the list

```
A(v) = {0,1,2,3} minus {c(u): u in N_H(v) intersect O}.
```

The hypothesis ensures `|A(v)| >= 2`. The preceding lemma colours Q
from these lists, satisfying all fresh edges. List membership satisfies
all old-to-fresh edges, and c already satisfies the old edges. QED.

The condition is sufficient, not necessary. In particular, a retained
fresh vertex with a one-element list need not cause non-four-colourability.
For any non-four-colourable induced subgraph O union Q, every proper
four-colouring of O must give at least three distinct colours to the old
neighbours of some vertex of Q. This necessary condition has no existence
content when O itself has no proper four-colouring.

## Exact extension with arbitrary lists

The same certificate supplies an exact extension procedure even with
empty or singleton lists. It is a mathematical reduction; a compiled
SAT formula or a production extension-oracle implementation is not part
of this package.

For a rooted tree, process children before parents and define

```
S(v) = {a in A(v): for every child w, S(w) contains a colour other than a}.
```

By induction, S(v) is exactly the set of possible colours at v in a proper
list colouring of its entire descendant subtree. The tree is colourable
exactly when the root set is nonempty. Choices can then be recovered from
root to leaves.

In the unique component with a cycle, fix a cycle vertex z. For each
`a in A(z)`, delete z and remove a from the lists of all its retained
neighbours. The remaining graph is a forest. The original component is
colourable exactly when one of these forest tests succeeds. A selected
subset Q may already have broken the cycle, in which case no branching
is needed. Components factor independently once c is fixed. With four
colours, at most four forest tests suffice for the one cyclic component;
all other components need one test. This is linear time in the fixed
incidence data for a given old colouring, including construction of lists.

## Location of the coupling

Classify an old H vertex as L when both coordinate axes have zero
coefficients at sqrt5, sqrt15, sqrt55 and sqrt165; the other old vertices
form S. There are 375 old L vertices and 135 old S vertices. Classify a
fresh point as L-only, S-only or mixed by its complete old neighbour set.
The counts are 43, 75 and 4. The mixed points are precisely
`170,436,1239,1527`; their old L neighbour sets are all `{0}`.

The fresh edges by endpoint type are

```
L-only/L-only: 1; mixed/mixed: 3;
mixed/S-only: 7; S-only/S-only: 46.
```

There is no fresh edge from an L-only point to either other type. The
37-vertex component contains all four mixed points and 33 S-only points.
It attaches to just the old origin on the L side and to 100 distinct old
S vertices. Its sole cycle includes three points outside H514. Thus the
published H514 path is part of a larger coupled support; the H514 closure
does not close this support. Nor can its positive deletion colourings be
transferred without checking their extension.

These results establish a finite extension mechanism, not a bound of 508
on any non-four-colourable graph, and not a closure of the full 632-point
support. They say nothing about completion points outside the fixed list.
