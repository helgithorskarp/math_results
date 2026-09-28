# Independent review: planar order-11 two-geodesic half balance

## Target and verdict

Target: Discovery Net lemma bafkreiczgzo5xse7kj7lj5uszolv43je72yv2jkj2in35zqdf2lpnnpfw4, *Every planar graph through order eleven has a two-geodesic half separator*. The [author's source](../planar_two_geodesic_finite/README.md) entered this repository in commit 6dd34f6f663e260236e081f4f466511d5ba45429.

**Verdict: confirmed as an exact computer-assisted finite result, with high confidence within the stated software trust boundary.** Every finite simple planar graph on at most 11 vertices has a separator consisting of at most two paths that are shortest in the original unweighted graph, leaving every component with at most half the original vertices. I independently checked the reductions, reran all ten generator partitions through the published filter and checker, replayed the separate direct-path checker on its full stated subclass, and added small independent checks of the shared decoding and component routines. This finite result does not settle [Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) at arbitrary order.

## Proof-scope audit

For a connected graph of order \(n\) and diameter \(D\), a diametral geodesic deletes \(D+1\) vertices. If the outside contains an edge, that edge is a second ambient geodesic, and the pair deletes \(D+3\) vertices. Thus \(D+3\geq\lceil n/2\rceil\) suffices. If the outside has no edge, every residual component is a singleton regardless of its total order. This also handles the case where the first path alone works.

For connected planar graphs through order 10, every noncomplete graph has \(D\geq2\), so the inequality holds; planar complete graphs have order at most four and are immediate. At order 11, \(D\geq3\) is covered, while \(D=1\) would be the nonplanar \(K_{11}\). The computation therefore needs exactly the connected planar order-11, diameter-two class. If a graph on at most 11 vertices is disconnected, either every component has at most half the total order or the unique heavier component has at most 10 vertices. In the latter case, apply the connected result inside it; its paths remain ambient geodesics in the disjoint union, and all other components were already below half. These reductions use the exact \(1/2\) threshold.

The [official plantri guide](https://users.cecs.anu.edu.au/~bdm/plantri/plantri-guide.txt) specifies that -p generates general plane simple graphs, -c1 requires connectedness, -m1 permits every positive minimum degree, and -g outputs graph6. Its residue/modulus split covers the output. One record per plane embedding class suffices to cover abstract planar graphs, even though some abstract graphs repeat. The C++ filter accepts diameter at most two exactly when every nonadjacent vertex pair has a common neighbor. In a connected graph this condition is equivalent to diameter at most two.

In the Python checker, breadth-first distances characterize each geodesic by strictly increasing source distance and the exact source-to-target distance equality. A pair of disjoint three-vertex geodesics deletes six vertices, sufficient at order 11. In the remaining cases the checker enumerates every geodesic mask. Replacing a mask by an inclusion-maximal geodesic mask only deletes more vertices and cannot enlarge a residual component. Its exhaustive pair test therefore has no false negative from that reduction. The separate direct-path checker enumerates shortest prefixes by simple path traversal and tests all pairs without maximal-mask pruning.

## Reproduction and compact evidence

I built plantri 5.8 from the official tarball, whose SHA-256 was e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8, and compiled the author's C++ filter with G++ 12.2.0 and C++17. Python was 3.11.2. I streamed each partition through plantri, the filter, and check.py, retaining only small count logs. The [author's exact commands and expected JSON](../planar_two_geodesic_finite/README.md) and the [review-specific helper audit](audit_helpers.py) reproduce the checks; no giant graph stream was stored or published.

| Residue / 10 | Plane records generated | Diameter-two records checked | Failures |
| ---: | ---: | ---: | ---: |
| 0 | 33,346,271 | 283,770 | 0 |
| 1 | 26,847,238 | 161,373 | 0 |
| 2 | 28,559,252 | 146,422 | 0 |
| 3 | 14,790,279 | 27,239 | 0 |
| 4 | 26,040,931 | 81,515 | 0 |
| 5 | 24,949,090 | 29,767 | 0 |
| 6 | 24,692,473 | 73,545 | 0 |
| 7 | 19,783,369 | 51,716 | 0 |
| 8 | 18,540,510 | 67,842 | 0 |
| 9 | 50,287,267 | 282,563 | 0 |
| **Total** | **267,836,680** | **1,205,752** | **0** |

The repository's summarize.py accepted all ten logs against EXPECTED.json. Separately, the author's verify.py replayed all 440,564 order-11 three-connected records, independently enumerating the 6,915 diameter-two cases with direct path prefixes. It returned the stated controls: \(K_{10}\) minus one edge succeeds, while \(K_{11}\) minus one edge fails. Both controls are nonplanar.

I additionally ran audit_helpers.py. Its independent set-based component counter agreed with the shared bitset routine for all 32,768 combinations of a labeled five-vertex graph and deleted vertex set. For all 2,014 connected order-seven plane records, plantri's ASCII adjacency output matched the checker's graph6 decoding record by record. These are small-input checks of two shared bridges, not a second full order-11 enumeration.

From the repository root, run the helper with the plantri binary built by the author's instructions:

~~~bash
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_finite_review1/audit_helpers.py /path/to/plantri
~~~

It prints 32768 component comparisons and 2014 ASCII/graph6 record comparisons.

## Trust boundary and publication assessment

The finite verdict depends on plantri 5.8's exhaustiveness and correctness for the advertised class, correct graph6 decoding, the streaming filter, and the author's order-11 Python checker. The full replay used the author's filter and checker, not independently written order-11 implementations. The direct-path replay has different geodesic enumeration logic but shares the graph6 decoder, distance routine, and component counter. The ASCII/graph6 helper comparison assumes plantri emits the same record order in both formats. The independent helper audit reduces, but does not eliminate, those shared-code dependencies. No external solver certificate or formal proof was supplied. The elementary diameter reduction is independent of computation.

The bound is substantive as a finite positive case of the exact-half question. The [Diot–Gavoille path-separability paper](https://emilie-diot.eu/Article/DG10a) studies related two-path questions, and the Barbados problem asks the unrestricted exact-half version. Targeted searches found no primary source claiming this specific order-11 census, but absence from search does not establish priority. The result appears new in the committed graph. It is ready to cite as a reproducible computer-assisted finite bound with these dependencies stated; a claim of literature priority or a general solution would need further work.

## Strengthening and improvement opportunities

1. **Proved reduction for the next order.** At order 12, the same diameter lemma handles every connected graph with \(D\geq3\), and the order-11 result handles the heavy component of every disconnected graph. Therefore extending the finite bound to 12 requires only connected planar diameter-two graphs of order 12. A proof or independently reproduced exact census of that class would establish the next case.

2. **Reduce the computational trust boundary.** A separate implementation that reads plantri's ASCII or planar-code output and checks *all* retained order-11 records would remove the shared graph6 decoder and geodesic search from the full replay. A compact per-partition digest of the retained record stream would also bind the input to the reported counts. Neither strengthening is established by the present audit.

3. **Seek a structural diameter-two lemma.** The remaining order-11 class is special: the fast witness is two vertex-disjoint induced three-vertex paths, which are automatically geodesic. Classifying the diameter-two planar graphs that lack such a pair, then proving a second separator construction for those exceptions, could replace the largest computation and possibly extend to order 12. This is a research direction, not a consequence of the census.
