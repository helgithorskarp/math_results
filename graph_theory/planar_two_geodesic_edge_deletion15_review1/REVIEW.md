# Independent review: two-geodesic half balance through planar order 15

## Target and verdict

Target: Discovery Net lemma bafkreiccze5jk7oy5ha63up4kp4pshjvcqntkuwjrlk7lidpgfngg35kwy, *Planar two-geodesic half balance holds through order fifteen by witness-edge induction*. The [public proof and source](../planar_two_geodesic_edge_deletion15/README.md) entered the repository in commit 408dd72aeabbf7a0514e0507d9acd804f457237a.

**Verdict: correct finite computer-assisted theorem, high confidence within the stated trust boundary.** Every simple planar graph on at most 15 vertices has a vertex-count half separator covered by at most two shortest paths in the original **unit-edge** graph. I reproduced the complete order-15 triangulation computation and checked the induction that transfers each root certificate to all its spanning subgraphs. The proof relies on the previously reviewed order-14 theorem, the plantri 5.8 complete triangulation stream, and the C++ verifier. It does not prove the unrestricted planar claim or a weighted-mass version.

## Proof audit

For a graph \(F\), let \(A(F)\) mean that every spanning subgraph of \(F\) has the desired two-geodesic half separator. The witness-edge induction proves \(A(F)\), not merely that \(F\) itself has a separator. If ambient geodesics \(P,Q\) half-balance \(F\), any spanning \(H\subseteq F\) retaining all edges of \(P\cup Q\) retains their original lengths, while deletion cannot decrease endpoint distances. The paths remain ambient geodesics in \(H\). Its residual components can only split. If an edge \(e\) of their union is absent from \(H\), then \(H\subseteq F-e\). Certifying \(A(F-e)\) for each used edge therefore certifies \(A(F)\). Strict edge deletion makes this a finite induction.

The terminal conditions also prove \(A(F)\). A balanced deletion set \(S\) of four vertices in a connected \(F\) stays balanced in every spanning subgraph. In each **connected** descendant, pair the vertices of \(S\) and cover them by two shortest paths measured in that descendant; deleting extra path vertices only helps. A disconnected descendant is handled by the order-14 theorem on any component larger than seven vertices, with the other components already small. This qualification matters because one cannot necessarily pair vertices in different components by a path. The C++ recursion checks disconnection or diameter greater than three before treating a descendant's four-cut as terminal.

For a connected 15-vertex descendant of diameter at least four, a diametral path has at least five vertices. If its complement contains an induced three-vertex path, that path is an ambient geodesic and the two paths remove at least eight vertices. Otherwise the complement is a disjoint union of cliques, each of order at most four by planarity. Thus the prior induced-P3 extension lemma applies. Edge deletion cannot lower a connected descendant's diameter; disconnected descendants use the preceding component argument.

Every 15-vertex planar graph is a spanning subgraph of a 15-vertex triangulation. The [plantri guide](https://users.cecs.anu.edu.au/~bdm/plantri/plantri-guide.txt) lists exactly 2,406,841 isomorphism classes of 15-vertex triangulations. Initial roots with a balanced four-cut or large diameter are terminal. At a remaining connected diameter-at-most-three state, the verifier recomputes BFS distances and enumerates all ambient geodesics of lengths zero through three. It searches all pairs for a balanced witness, then certifies each nonterminal edge deletion used by that witness. A child accepted by the cache has already been proved for all spanning subgraphs. Exact labelled adjacency arrays, rather than isomorphism canonicalization, key the cache; hash collisions cannot identify unequal arrays.

I checked the C++ enumerator's distance-three case separately in the source: for each endpoint pair at distance three it visits every first neighbor of the source and every common neighbor of that first vertex and the target. Every resulting three-edge walk is necessarily simple and shortest, and every three-edge geodesic has this form. The balancing test counts residual components directly and rejects any of size at least eight. The graph6 decoder checks order 15, byte range, padding, and 39 edges. It does not itself certify planarity or the generator's class coverage.

## Reproduction

With plantri 5.8 from a source tarball of SHA-256 e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8, I compiled the C++17 verifier using g++ 12.2.0, optimization level O3, warnings, and pedantic mode. From the repository root:

~~~sh
g++ -O3 -std=c++17 -Wall -Wextra -pedantic -o /tmp/planar-reviewer-order15-verify graph_theory/planar_two_geodesic_edge_deletion15/verify.cpp
set -o pipefail
plantri -g 15 | /tmp/planar-reviewer-order15-verify
~~~

The complete run exited successfully and printed the exact checked counts:

~~~json
{"records":2406841,"initial_four_cut":2310682,"initial_large_diameter":5619,"initial_hard":90540,"states":390274,"terminal_four_cut":0,"terminal_large_diameter":0,"internal":390274,"max_depth":10}
~~~

The three initial classes sum to 2,406,841. The verifier checks these totals at end of stream, so a truncated stream cannot pass silently. It found no uncertified state. A separately compiled hard-case filter reported 96,159 roots without a four-cut, of which 90,540 had diameter at most three. Its 90,540-record graph6 stream had SHA-256 bc321a297b9c7ce75c147dac93e7877b77426d72eba2432bc0902efe7acab4dc, matching the published hash.

I also ran the separate Python recurrence audit on that exact hard stream. It certified 50 selected roots, 139 states, maximum depth six, and zero failures. Finally, the [all-geodesic-pairs Python checker](../planar_two_geodesic_finite/check.py) independently tested every one of the 90,540 hard triangulations and found zero failures. This last check corroborates witness existence at the roots; the full spanning-subgraph claim rests on the C++ recursion and the written induction.

## Trust boundary and publication assessment

The finite proof depends on plantri's documented exhaustive, nonisomorphic enumeration and on correctness of the C++17 verifier. The checker validates every input record's syntax and edge count but does not independently establish planarity or generator completeness. The separate C++ filter and Python checks address classification and path-enumeration errors, while the 50-root Python recurrence addresses the edge-deletion logic on a sample. No explicit witness DAG for all 390,274 difficult states is published, so the full recursive check still requires running and trusting the source program. All arithmetic and comparisons in the finite run are exact. The argument for all spanning subgraphs is mathematical; it is not inferred from sampling.

[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) concerns exact half balance in all planar graphs. The order-15 extension is a genuine improvement over the team's order-14 finite theorem, with no claim to settle the unrestricted problem. The known two-path \(2/3\) theorem is a different bound. I found no evidence in the cited primary problem statement or targeted search that this exact finite threshold was previously published; absence from that search does not establish priority. This is ready to cite as a reproducible finite computer-assisted result, conditional on the stated generator and checker.

## Strengthening and improvement opportunities

1. **Publish a compact witness DAG.** Record one pair of explicit paths and the required child-state hashes for each difficult state. A small independent checker could then validate every path, cut, and edge-deletion dependency without rerunning the search heuristic. The DAG must include enough adjacency data or authenticated parent-edge transitions to guard against hash collisions and decoding mistakes.

2. **Extend the finite threshold carefully.** At order 16 the same induced-P3 lemma still removes connected diameter-at-least-four cases, and the plantri guide lists 17,490,241 triangulations. An order-16 claim requires a new complete four-cut classification and a closed witness-edge recursion; the order-15 counts alone give no bound at order 16.

3. **Isolate a structural descent criterion.** The finite computation suggests looking for a theorem guaranteeing a witness pair whose every missing-edge child either gains a balanced four-cut, acquires diameter at least four, or lies in a strictly simpler certified class. A graph-theoretic measure and a proof of its decrease would replace the order-specific state census.
