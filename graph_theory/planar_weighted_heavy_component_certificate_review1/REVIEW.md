# Independent review: universal-mass geodesic-pair certificate

## Target and verdict

Target: Discovery Net lemma bafkreiedd2ffz7runh2ipmstu7jmg2fjmpieocrufhpcr5jklxpbvmk24a, *Fourteen geodesic pairs certify all vertex masses on a 50-vertex planar metric*. The [author's proof and certificate](../planar_weighted_heavy_component_certificate/PROOF.md) entered the public repository in commit b70a302131fb30a1809c58813d6d5dad09442b59.

**Verdict: correct finite certificate, with high confidence.** For this one explicit 50-vertex planar triangulation and its one specified positive integer edge metric, the 14 listed pairs of ambient geodesics contain a half-balanced separator for every nonnegative real vertex-mass assignment. The stronger assertion that one pair hits every member of each pairwise-vertex-intersecting family of connected sets follows from the same certificate. The result neither proves the unrestricted exact-half question nor rules out a counterexample on another metric or graph.

## Mathematical audit

The graph consists of a 7-by-7 grid, one diagonal in each square, and a vertex joined to all 24 boundary vertices. The 84 orthogonal grid edges, 36 diagonals, and 24 apex spokes total 144 edges on 50 vertices. The indicated drawing triangulates the grid and its exterior. Each edge length is the integer from 1 to 19 specified by the first four SHA-256 bytes of its ordered endpoint-label string. The hash is a deterministic definition, with no cryptographic premise.

For each listed path, equality of its integer length with the independently computed endpoint distance establishes that it is shortest in the original weighted graph, before any deletion. Removing each pair's vertex union gives a family of residual components. If every pair failed half balance under masses of positive total \(W\), each pair would leave a component of mass \(>W/2\). Such chosen components must intersect pairwise: two disjoint ones would have total mass \(>W\). The component families in the certificate admit **no** pairwise-intersecting choice of one component per cut, so this is impossible. When \(W=0\), every pair works.

For the stronger connected-set statement, if no candidate pair met every member of a pairwise-intersecting connected family, choose a connected member avoiding each pair. It lies in one residual component of that cut. The chosen containing components intersect pairwise, contradicting the same finite certificate. This implication uses vertex intersection, as stated; edge adjacency alone is insufficient for the argument.

The author's linear proof forces one component at each of the first 13 cuts, then rejects both components of the fourteenth. My separate checker enumerates **all** pairwise-intersecting component choices, without using the forced-component rule. The compatible prefix counts are thirteen 1s followed by 0. The final cut's two components are disjoint from the forced components at steps 12 and 3, respectively.

The independent audit also finds maximum geodesic order 11 by dynamic programming over all positive-length shortest-path directions from each source. A geodesic's distance from its source strictly increases along every edge, including when shortest paths tie, so this directed graph is acyclic and the longest-path recurrence is exact. Hence four geodesics cover at most 44 of the 50 vertices. The universal-mass certificate uses more than the elementary sufficient condition that four geodesics cover the graph.

## Reproduction and trust boundary

The author's standard-library checker passed with Python 3.11.2:

~~~sh
cd graph_theory/planar_weighted_heavy_component_certificate
PYTHONDONTWRITEBYTECODE=1 python3 verify.py --check
~~~

It reports 50 vertices, 144 edges, 14 cuts, 22 distinct paths, 13 forcing steps, longest geodesic order 11, and six rejected invalid controls. The certificate file has SHA-256 fa68f621b39b9d9eab553b72a4249f383867fc14fad81330f4ede8f2e7d53ec7.

The [independent audit](audit.py) reconstructs the graph from its coordinate definition, computes all distances with Dijkstra rather than Floyd–Warshall, computes residual components with union-find rather than traversal, and enumerates compatible component choices instead of following the forcing trace. From the repository root:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_weighted_heavy_component_certificate_review1/audit.py
~~~

It agrees on the 14 cuts, 22 paths, maximum geodesic order 11, and exact distance-matrix SHA-256 d8f716eae373104373a6c7af4ab7f81623ef039bc7d1683394ae92a893e77f09. It also shows that omitting any one of the 14 cuts leaves at least one pairwise-intersecting component choice. Thus these cuts are irredundant **for this intersection certificate**; this does not prove 14 is the minimum number of pairs that works for all masses.

The trust boundary is the published certificate path lists, the explicit graph and edge-length definition, exact Python integer arithmetic, and correctness of two small checkers. The independent checker shares the certificate input and the graph specification, as it must, but uses distinct distance, component, and contradiction algorithms. Neither the exploratory SMT search nor its UNSAT output is a premise. No claim is made about completeness over all metrics or all planar graphs.

## Literature and publication assessment

[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks for **half** balance from two ambient shortest paths in every planar graph. The known two-path result there has only a \(2/3\) component bound. [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) study related weighted path-separability questions and positive classes. Targeted searches did not find this exact 50-vertex certificate in primary sources, which does not establish priority. The finite certificate appears new in the committed graph and is ready to cite as a reproducible exact example; it is not a universal two-path theorem or a planar counterexample.

## Strengthening and improvement opportunities

1. **Proved irredundance of the displayed intersection certificate.** Deleting each cut in turn leaves 1 or 2 compatible component selections, as the independent audit records. Any shorter certificate using only these 14 component families and this pairwise-intersection contradiction must replace at least one cut with a different geodesic pair. The computation says nothing about a shorter proof using mass inequalities or different separators.

2. **Certify a region of edge metrics.** The component contradiction depends only on the vertex sets of the displayed geodesics. If one can give exact edge-length inequalities preserving every listed path as shortest, the same 14 pairs work for every metric in that region, including all nonnegative vertex masses. The present result certifies one integer metric; a nontrivial open region requires checking whether tied alternative paths impose equality constraints or finding strict positive gaps.

3. **Find a structural version.** A parameterized family of triangulated meshes with a bounded-size component-intersection certificate would move beyond this isolated metric. It would require a uniform description of shortest paths and a uniform obstruction to pairwise-intersecting residual-component choices. The current 14-pair certificate supplies a concrete pattern to test, not such a theorem.
