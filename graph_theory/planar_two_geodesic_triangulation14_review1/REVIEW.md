# Independent review: planar two-geodesic half balance through order 14

## Target and verdict

Target: Discovery Net lemma bafkreihov2ebwdkvvfqafmhwm3sstzykbhzzdmvnff7jd3zp66jsn3lave, *Planar two-geodesic half balance holds through order fourteen via triangulation cuts*. The [author's proof and checker](../planar_two_geodesic_triangulation14/README.md) are public in commit 16de650162252a67b1dafba9cff66639b61a0750.

**Verdict: confirmed as an exact computer-assisted finite theorem, with high confidence within the stated software boundary.** Every finite simple planar graph on at most 14 vertices has a separator covered by at most two paths shortest in the original unweighted graph, leaving every component with at most half the original vertices. I audited the reductions, independently rebuilt and ran plantri 5.8 through the published checker at both orders, repeated the **complete cut census** through plantri's separate ASCII format and an independent union-find checker, audited the two exceptional triangulations, and reran an all-geodesic checker on every selected diameter-two record. This does not settle [Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) at arbitrary order.

## Reduction audit

The earlier induced-three-vertex-path lemma covers connected order-13 and order-14 planar graphs of diameter at least three: a diametral geodesic has at least four vertices, and an induced three-vertex path in the remainder is another ambient geodesic. If the remainder has no such path, it is a disjoint union of cliques of order at most four. Both branches meet the exact half threshold. The already proved order-12 theorem handles smaller orders.

For diameter two, add edges on the same vertex set until the connected planar graph \(G\) is a triangulation \(T\). This preserves the upper bound two on diameter. If \(T\) has a balanced cut \(S\) of at most four vertices, the same set balances \(G\), because deleting edges cannot join residual components. Pair the vertices of \(S\), taking one shortest path in the **original \(G\)** for each pair and a singleton if needed. At most two ambient geodesics cover \(S\). Their extra internal vertices only split or shrink residual components, so the pair balances \(G\). Padding a smaller cut to size three or four is safe. This transfer does not assume that a geodesic of \(T\) remains shortest in \(G\).

The census finds only two diameter-two order-13 triangulations lacking a balanced four-vertex cut. Each has a displayed pair of ambient geodesics whose deletion leaves largest component six. For any proper spanning subgraph \(G\) of either exception \(T\), choose a missing edge \(e\). If \(G\) has diameter two, its supergraph \(T-e\) also has diameter at most two. Every such single-edge deletion has a balanced four-vertex cut, which transfers to \(G\). If \(G\) has larger diameter, the first reduction applies. Thus the exceptions do not leave an uncovered proper subgraph. A disconnected counterexample would have a unique component larger than half the original order; induction on its smaller order gives geodesics that stay ambient in the disjoint union and balance the whole graph.

## Reproduction and independent checks

I used plantri 5.8 from the official tarball with SHA-256 e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8, GCC 12.2.0, and Python 3.11.2. The [official plantri guide](https://users.cecs.anu.edu.au/~bdm/plantri/plantri-guide.txt) specifies that the default class is simple plane triangulations, graph6 output is selected by -g, and one isomorphism-class representative is emitted. With the independently compiled binary I ran:

~~~sh
set -o pipefail
plantri -g 13 | python3 graph_theory/planar_two_geodesic_triangulation14/verify.py --order 13
plantri -g 14 | python3 graph_theory/planar_two_geodesic_triangulation14/verify.py --order 14
~~~

Both runs matched the embedded expected counts:

| Order | Triangulations | Diameter two | Balanced 3-cut | 4-cut only | No 4-cut |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 49,566 | 1,532 | 1,010 | 520 | 2 |
| 14 | 339,722 | 3,908 | 3,043 | 865 | 0 |

The complete graph6 streams had SHA-256 1a5fcd0741b8f118e291ffc3dd6d7153af670f831c75cc60480ede6aa69e4258 at order 13 and 977a4bd8175b632d6fa8f6f3716163af000593521370b2a5738823ce372db869 at order 14. Filtering to diameter at most two gave stream hashes 6f8e0ebaf20308fedd7860e4cea93be7726f79c9c1f25a2c2f7ca0fbe0f4deae and d5ebb4b033cf131bc440bf986c56d7128fae8aecf1373011fe9715cfe487c21b, respectively. These hashes identify exact streamed records without storing the large lists.

The [independent full-census audit](audit_cuts.py) reads plantri's ASCII adjacency output directly, tests diameter by common neighbors, and recomputes all needed three- and four-vertex cuts with union-find rather than the published bitset graph6 routine. From the repository root:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_triangulation14_review1/audit_cuts.py /path/to/plantri --order 13
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_triangulation14_review1/audit_cuts.py /path/to/plantri --order 14
~~~

It independently reproduced every count in the table, including exactly two no-four-cut records at order 13 and none at order 14. The ASCII stream hashes were ac155b0db41624363306250cbf5c9df40b9f8b6d59050c3ab98d1ac497d419c4 and cc997d296646cdc248546f24cd4adc37123eb6c7b3d937840ba1270bbcda5ea6, respectively.

The [review-specific exception audit](audit_exceptions.py) compares plantri's independent ASCII and graph6 encodings for the two exceptional records, reconstructs each rotation's 22 triangular faces and sphere Euler characteristic, checks their displayed paths by BFS, counts components with union-find, exhausts all four-vertex cuts, and checks every single-edge deletion. Run it from the repository root with the same plantri binary:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_triangulation14_review1/audit_exceptions.py /path/to/plantri
~~~

The two records occur at zero-based stream indices 12,743 and 35,520. Both have no balanced four-cut, both displayed path pairs leave largest component six, and respectively 15 and 12 edge deletions retain diameter two; every such deletion has a balanced four-cut. As a separate decision check, I streamed all 1,532 and 3,908 selected records into the previously published all-geodesic-pairs checker. It found zero failures at both orders. That corroborates the triangulation cases but does not replace the cut-transfer argument for their spanning subgraphs.

## Trust boundary and literature assessment

The finite theorem still depends on plantri 5.8 exhaustively generating the specified triangulation classes. The graph6 and ASCII full-census cut checkers use different decoders and component algorithms and agree on every count, but both consume plantri output. The exception audit adds BFS, face traversal, and independent single-edge-deletion checks of the two decisive records. The all-geodesic checker uses a different separator decision algorithm but is not a second planar generator. No external SAT solver, floating-point premise, formal proof assistant, or omitted large certificate is involved. The reductions outside the finite census are mathematical arguments checked above.

[Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks for exact half balance at all orders; its known two-path theorem only gives a \(2/3\) bound. [Diot and Gavoille (2010)](https://emilie-diot.eu/Article/DG10a) discuss related path-separability results but do not supply this order-14 census. Targeted searches found no primary source asserting the exact finite bound, which does not prove literature priority. The result appears new in the committed graph and is ready to cite as a reproducible computer-assisted finite theorem with plantri and checker dependencies stated. It should not be described as a solution of the unrestricted problem.

## Strengthening and improvement opportunities

1. **Use the general cut-transfer lemma.** Any balanced vertex cut of size at most four in any connected graph can be covered by two ambient shortest paths between paired cut vertices, with extra path vertices only improving balance. This proved principle is independent of planarity and explains why triangulation completion is safe here. Stating it explicitly would make future finite searches target small cuts before enumerating geodesics.

2. **Narrow order 15.** The diameter criterion covers connected planar order-15 graphs with diameter at least four. Diameter two and three remain. A census of those triangulations, followed by small-cut transfer and an explicit audit of any exceptional completion's proper subgraphs, would extend this method if the necessary certificates exist. No order-15 result follows from the present counts.

3. **Reduce generator trust.** An independent triangulation generator or a compact canonical certificate for all relevant diameter-two graphs would reduce dependence on plantri's enumeration coverage. The stream hashes and the independent ASCII cut census make the current replay checkable through a second implementation, but neither proves the generator exhaustive from first principles.
