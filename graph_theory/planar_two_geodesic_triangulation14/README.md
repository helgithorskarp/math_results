# Two geodesic half separators through planar order 14

**Result.** Every finite simple planar graph with at most **14 vertices** has
a vertex set covered by at most two shortest paths in the original unweighted
graph whose deletion leaves components of at most half the vertices. The
unrestricted [Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf)
remains open. This is a finite computer-assisted theorem, conditional on the
[plantri 5.8](https://users.cecs.anu.edu.au/~bdm/plantri/) triangulation
enumeration and the exact checker here; no literature priority claim is made.

The team's [elementary order-12 and diameter result](../planar_two_geodesic_packing/README.md)
leaves only connected diameter-two graphs at orders 13 and 14. The new step
checks **triangulations only**, then transfers their cut certificates to every
planar spanning subgraph. This avoids enumerating all plane graphs.

## Reduction to triangulations

Every simple planar graph on at least three vertices can be completed, by
adding edges on the same vertex set, to a simple planar triangulation. If a
connected graph `G` has diameter two, every completion `T` also has diameter
at most two.

Suppose `T` has a set `S` of at most four vertices such that every component
of `T-S` has at most `floor(n/2)` vertices. The same set balances `G`, because
deleting edges can only split components. Pair the vertices of `S` arbitrarily;
for each pair take **any shortest path in the original `G`** between them,
and use a singleton path if one vertex remains. At most two ambient geodesics
cover `S`. Their extra internal vertices only split or shrink the remaining
components. Thus `G` has the required separator. This argument uses only the
existence of a small balanced cut, so it is valid when shortest paths change
under triangulation.

The exact check of all order-13 and order-14 diameter-two triangulations gives:

| Order | All triangulations | Diameter two | Balanced 3-cut | 4-cut but no 3-cut | No 4-cut |
|---:|---:|---:|---:|---:|---:|
| 13 | 49,566 | 1,532 | 1,010 | 520 | 2 |
| 14 | 339,722 | 3,908 | 3,043 | 865 | 0 |

Here a 3-cut or 4-cut means deletion of exactly that many vertices, with all
components of order at most `floor(n/2)`. A smaller balanced cut can always
be padded to three vertices, so checking exact sizes three and four is
sufficient. The two exceptional order-13
triangulations are the following exact graph6 records, with explicit pairs of
ambient shortest paths. The checker recomputes their distances and components
and independently validates explicit rotation systems as sphere embeddings.

| graph6 | First path | Second path | Largest remaining component |
|:---|:---|:---|---:|
| `L\|eKKE@oJ_bp?~` | `0,1` | `3,11,6` | 6 |
| `L\|fIID@SJ_aEFx` | `0,1` | `3,12,6` | 6 |

Every **proper** spanning subgraph `G` of either exceptional triangulation
also has the property. Choose an edge `e` missing from `G`. If `T-e` has
diameter at most two, the checker finds a balanced 4-cut in `T-e`; the cut
transfers to `G`. If `T-e` has diameter at least three, then `G` cannot have
diameter two. The checker examines every one of the 33 edges of each
exception: respectively 15 and 12 single-edge deletions retain diameter two,
and all of these have a balanced 4-cut. Thus the two exceptions create no
gap in the planar completion reduction.

For completeness, if a connected planar graph of order 13 or 14 has diameter
at least three, take a diametral shortest path `P`. It has at least four
vertices. If the remainder contains an induced three-vertex path `Q`, then
`Q` is another ambient geodesic, and `P union Q` removes at least seven
vertices. Otherwise the remainder is a disjoint union of cliques, each of
order at most four by planarity. Either way all remaining components have
order at most `floor(n/2)`. The already proved order-12 theorem handles the
base cases. A disconnected graph is handled by induction on order: if a
component exceeds half the total order, apply the result inside that smaller
component; otherwise no deletion is needed.

## Reproduction and trust boundary

The [official plantri guide](https://users.cecs.anu.edu.au/~bdm/plantri/plantri-guide.txt)
states that its default class is simple planar triangulations, `-g` emits
graph6 records, and one isomorphism-class representative is emitted. A
triangulation is 3-connected, so its sphere embedding is unique up to
reflection. The checker verifies order, graph6 padding, and `3n-6` edges for
every record, then exactly tests diameter, all relevant 3- and 4-vertex
candidate cuts, both exceptional path pairs, and each exceptional single-edge
deletion. It validates the two exceptional graphs' planarity from explicit
rotation systems, but does not independently prove plantri's enumeration
coverage or the planarity of every generated record.

The source tarball used was plantri 5.8, SHA256
`e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8`.
With Python 3.11 or later and a compiled plantri 5.8 binary:

```sh
set -o pipefail
plantri -g 13 | python3 graph_theory/planar_two_geodesic_triangulation14/verify.py --order 13
plantri -g 14 | python3 graph_theory/planar_two_geodesic_triangulation14/verify.py --order 14
```

Expected JSON counts are embedded in `verify.py` and checked automatically.
The run performed for this note returned:

```json
{"diameter_two": 1532, "exception_edge_deletions_diameter_two": 27, "exceptions": 2, "four_cut_only": 520, "order": 13, "records": 49566, "three_cut": 1010}
{"diameter_two": 3908, "exception_edge_deletions_diameter_two": 0, "exceptions": 0, "four_cut_only": 865, "order": 14, "records": 339722, "three_cut": 3043}
```

As an independent check of the decisive diameter-two records, the team's
[separate all-geodesic-pairs checker](../planar_two_geodesic_finite/check.py)
was run on all 1,532 and 3,908 selected triangulations and found zero
failures. That check is corroboration; the proof above uses the small-cut
certificate and exceptional edge-deletion audit.
