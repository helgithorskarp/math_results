# Edge-deletion certificates for planar order 15

**Result.** Every finite simple planar graph on at most
**15 vertices** has a half-balanced separator covered by at most two shortest
paths in the original unweighted graph. The argument uses the team's
[order-14 theorem](../planar_two_geodesic_triangulation14/README.md) and an
exact finite computation on the order-15 triangulations. The unrestricted
[Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf)
remains open. No literature priority claim is made.

## Why spanning subgraphs need a new certificate

Every simple planar graph can be completed on the same vertex set to a
triangulation. A balanced cut of at most four vertices in a triangulation
remains balanced in every spanning subgraph. Any four vertices can be covered
by two shortest paths measured in that subgraph, by pairing the vertices.
Likewise, if a connected order-15 triangulation has diameter at least four,
each connected spanning subgraph has diameter at least four. A diametral path
and an induced three-vertex path, or the residual clique components, give the
two-geodesic half separator by the prior path-extension lemma. Disconnected
spanning subgraphs follow from the order-14 theorem by induction on their
largest component.

The triangulations left by those two monotone conditions have diameter at
most three and no balanced four-vertex cut. A two-geodesic witness in a
triangulation alone does not automatically transfer to a spanning subgraph:
an edge of a witness path might be missing. The following finite induction
handles every possible missing edge without enumerating all spanning
subgraphs.

**Witness-edge lemma.** Let `F` be a finite graph and suppose a pair of
ambient geodesics `P,Q` half-balances it. If a spanning subgraph `H` of `F`
contains every edge of `P` and `Q`, then the same paths are ambient geodesics
in `H` and still half-balance it. Indeed, deleting edges cannot shorten a
distance or join residual components, while the retained paths still realize
their original endpoint distances. Therefore, if every `F-e` for an edge `e`
used by `P` or `Q` has the required property **for all its spanning
subgraphs**, then so does `F`: a subgraph either retains all witness edges or
misses at least one such `e` and lies in `F-e`.

This is a well-founded edge-deletion induction. At a graph `F`, the checker
first accepts either monotone terminal condition: a balanced four-vertex cut,
or diameter greater than three (including disconnection). Otherwise it
enumerates **all** ambient geodesics and searches their pairs for a
half-balancing witness. A shortest path has at most three edges because the
diameter is at most three. For each edge used by the selected witness, it
recurses on `F-e` unless that child already satisfies a terminal condition
or has been proved earlier. Every recursive step deletes an edge, so the
procedure terminates. Its chosen pair minimizes the number of nonterminal
child edges, then the total witness-edge count; this ordering affects runtime
only. If no pair exists, the program prints the graph6 record and exits
without claiming the theorem.

The induction proves the property for **all** spanning subgraphs of each
processed triangulation. It uses original-graph shortestness at every node:
the checker recomputes distances after each edge deletion, and the
witness-edge lemma transfers only paths whose edges survive. At no point are
shortest paths in a residual graph substituted for ambient geodesics.

## Exact census and reproduction

The [official plantri guide](https://users.cecs.anu.edu.au/~bdm/plantri/plantri-guide.txt)
states that `plantri -g 15` emits graph6 for every simple planar
triangulation of order 15, one per isomorphism class. The source tarball used
was plantri 5.8, SHA256
`e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8`.
The C++17 checker needs only the standard library. From the repository root:

```sh
g++ -O3 -std=c++17 -Wall -Wextra -o /tmp/planar-order15-verify \
  graph_theory/planar_two_geodesic_edge_deletion15/verify.cpp
set -o pipefail
plantri -g 15 | /tmp/planar-order15-verify
```

The program checks the graph6 order, padding, and triangulation edge count
for every input record. It computes exact BFS distances, tests every
four-vertex candidate cut by component traversal, and enumerates singleton,
edge, two-edge, and three-edge ambient geodesics before testing path pairs.
It prints counts of the initial cases and recursive states, and checks them
against the expected complete-census values. The plantri 5.8 run returned:

```json
{"records":2406841,"initial_four_cut":2310682,"initial_large_diameter":5619,"initial_hard":90540,"states":390274,"terminal_four_cut":0,"terminal_large_diameter":0,"internal":390274,"max_depth":10}
```

The three initial classes partition all 2,406,841 triangulations. The
390,274 states are the distinct difficult edge-deletion states reached by
the recursion; terminal children are recognized when the program selects
its witness edges, before entering the recursive function. Hence the two
`terminal_*` counters are zero. Maximum recursion depth was ten deleted
edges. No graph lacked a two-geodesic witness.

Independent controls addressed different risks. The separate
[`filter_hard.cpp`](filter_hard.cpp) found the same 90,540 hard triangulations;
its graph6 stream had SHA256
`bc321a297b9c7ce75c147dac93e7877b77426d72eba2432bc0902efe7acab4dc`.
The team's [independent all-path-pairs checker](../planar_two_geodesic_finite/check.py)
enumerated all ambient geodesics on every one of those 90,540 records and
found zero failures. The separate [`audit_sample.py`](audit_sample.py)
implementation of the witness-edge recursion certified 50 roots chosen as
the first 30 and every 4,500th hard record; it visited 139 states, reached
depth six, and found zero failures. Reproduce these controls with:

```sh
g++ -O3 -std=c++17 -o /tmp/planar-order15-hard \
  graph_theory/planar_two_geodesic_edge_deletion15/filter_hard.cpp
set -o pipefail
plantri -g 15 | /tmp/planar-order15-hard > /tmp/planar-order15-hard.g6
sha256sum /tmp/planar-order15-hard.g6
python3 graph_theory/planar_two_geodesic_finite/check.py --order 15 \
  < /tmp/planar-order15-hard.g6
PYTHONDONTWRITEBYTECODE=1 python3 \
  graph_theory/planar_two_geodesic_edge_deletion15/audit_sample.py \
  /tmp/planar-order15-hard.g6
```

Address and undefined-behavior sanitizer builds of the C++
checker passed a 2,330-record plantri partition, including 92 hard cases.

The conclusion depends on plantri's enumeration coverage and the C++
implementation. The checker verifies the two-path property of each hard
triangulation and, by the written induction, of every spanning subgraph. It
does not prove the universal planar assertion. The generator's planarity and
class coverage are external dependencies; the checker does not independently
reconstruct an embedding for every generated graph.
