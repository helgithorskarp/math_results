# Edge-deletion certificate through planar order 16

**Finite result.** Every finite simple planar graph on at most 16 vertices has
a half-balanced separator covered by at most two shortest paths in the
original unweighted graph. This extends the [order-15 certificate](../planar_two_geodesic_edge_deletion15/README.md).
It does not settle the unrestricted [Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Proof reduction

Every order-16 planar graph is a spanning subgraph of an order-16
triangulation. Three facts certify whole families of spanning subgraphs.

1. If a graph has a four-vertex set whose deletion leaves components of size
   at most eight, every spanning subgraph does too. Pair the four vertices
   into two pairs and take shortest paths between the paired endpoints *in
   the spanning subgraph*. Their union contains the cut, so deleting it can
   only split the residual components.
2. If a connected order-16 graph has diameter at least four, the
   [path-extension lemma](../planar_two_geodesic_packing/README.md) gives two
   ambient geodesics: a diametral path has at least five vertices, and an
   induced three-vertex path adds three, reaching eight. If a spanning
   subgraph remains connected, its diameter cannot decrease. Disconnected
   spanning subgraphs follow from the order-15 theorem by applying it to
   their unique component, if any, larger than eight.
3. Suppose two ambient geodesics P,Q half-balance a graph F. Any spanning
   subgraph that retains every edge of P and Q has the same witness: deletion
   of other edges cannot shorten endpoint distances or join residual
   components. A spanning subgraph missing a witness edge e lies in F-e.
   Thus, if each such F-e has been certified for all its spanning subgraphs,
   then F has too. This is the [witness-edge induction](../planar_two_geodesic_edge_deletion15/README.md).

The checker applies these facts to each triangulation. It first tests every
four-vertex cut and then diameter. At each remaining state it enumerates all
ambient shortest paths, tests pairs for half-balance, and recurses only on
deletions of edges used by one valid pair. Every recursive step removes an
edge. At a state of diameter at most three, each path has at most three
edges, so the enumeration is exhaustive. The pair-selection heuristic
minimizes nonterminal child edges, then total witness edges; it affects
runtime only. The proof covers *all spanning subgraphs* of every generated
triangulation, even though they are not individually enumerated.

## Complete census

The [official plantri guide](https://users.cecs.anu.edu.au/~bdm/plantri/plantri-guide.txt)
gives 17,490,241 isomorphism classes of order-16 simple planar
triangulations. We used plantri 5.8 from source tarball SHA256
e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8.
From the repository root, compile the standard C++17 verifier and stream the
full generator output:

~~~sh
g++ -O3 -std=c++17 -Wall -Wextra -o /tmp/planar-order16-verify \
  graph_theory/planar_two_geodesic_edge_deletion16/verify.cpp
set -o pipefail
plantri -g 16 | /tmp/planar-order16-verify
~~~

Expected exact output:

~~~json
{"records":17490241,"initial_four_cut":16875528,"initial_large_diameter":76899,"initial_hard":537814,"states":1995878,"terminal_four_cut":0,"terminal_large_diameter":0,"internal":1995878,"max_depth":9}
~~~

The three initial classes partition all 17,490,241 triangulations. All
537,814 difficult roots certified, with 1,995,878 distinct difficult
edge-deletion states and maximum recursion depth nine. Terminal descendants
are recognized while selecting witness edges, before entering recursion;
this explains the zero terminal counters. The verifier checks graph6 order,
padding, and triangulation edge count, and rejects a truncated stream through
exact count assertions. It recomputes exact BFS distances and residual
components after every edge deletion. No state lacked a witness pair.

## Independent controls

The separate [hard-case filter](../planar_two_geodesic_edge_deletion15/filter_hard.cpp)
on plantri residue 0/1000 found 399 difficult roots among 17,168
triangulations. The hard stream has SHA256
a1ee18fc00018b938e76cf40925df78f5b69d86f41788babceb04af139e69c92.
The independent [all-path-pairs Python checker](../planar_two_geodesic_finite/check.py)
found zero failures on all 399, and this directory's
[Python induction audit](audit_sample.py) certified 27 selected roots,
visiting 109 states with maximum depth six. Reproduce them with:

~~~sh
g++ -O3 -std=c++17 -o /tmp/planar-hard-filter \
  graph_theory/planar_two_geodesic_edge_deletion15/filter_hard.cpp
set -o pipefail
plantri -g 16 0/1000 | /tmp/planar-hard-filter 16 > /tmp/planar-16-sample.g6
sha256sum /tmp/planar-16-sample.g6
python3 graph_theory/planar_two_geodesic_finite/check.py --order 16 \
  < /tmp/planar-16-sample.g6
PYTHONDONTWRITEBYTECODE=1 python3 \
  graph_theory/planar_two_geodesic_edge_deletion16/audit_sample.py \
  /tmp/planar-16-sample.g6
~~~

For a denser independent subset, plantri -m4 -g 16 produces 65,619
triangulations. The separate filter found 10,570 difficult roots; their
stream has SHA256
26f7217645ef2c99f65517cc0deb625f44d6a8412d49e71bf2dbd2a03311497d.
The Python all-path-pairs checker found zero failures on every one. The
full C++ verifier also passed an address and undefined-behavior sanitizer
build on the 17,168-record residue, including its 399 difficult roots.

~~~sh
plantri -m4 -g 16 | /tmp/planar-hard-filter 16 > /tmp/planar-16-m4-hard.g6
sha256sum /tmp/planar-16-m4-hard.g6
python3 graph_theory/planar_two_geodesic_finite/check.py --order 16 \
  < /tmp/planar-16-m4-hard.g6
~~~

The infinite step is the written spanning-subgraph induction. The finite
coverage depends on plantri's published enumeration and the C++ verifier;
the checker does not reconstruct a plane embedding for every generated
graph. The Python controls sample the induction and independently test path
pairs on specified subsets. No raw census dump is required or published.
