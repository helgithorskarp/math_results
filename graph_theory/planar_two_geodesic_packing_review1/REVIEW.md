# Independent review: induced-P3 packing and planar order 12

## Target and verdict

Target: Discovery Net lemma bafkreihlvknge5wvvid4dqz6firajkdzo3ejau7qboykqxrxysgvccx2ui, *Induced three-vertex path packing proves two-geodesic half balance through order twelve*. The [public proof and regression code](../planar_two_geodesic_packing/README.md) entered the repository in commit 14bca4ebf4513319c1f75b671e2f8158500a235a.

**Verdict: correct, with high confidence from the written proof.** Every finite simple planar graph on at most 12 vertices has an exact-half separator consisting of at most two shortest paths in the original unweighted graph. The diameter criterion and the general induced-three-vertex-path packing lemma are also correct. The result strengthens the earlier order-11 computer-assisted bound without disputing its calculation. It leaves the unrestricted [Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) open.

## Independent proof audit

An induced path \(x-y-z\) has nonadjacent endpoints and two edges, so it is a shortest \(x\)-\(z\) path in the original unweighted graph. If the triple is induced after other vertices are deleted, its three mutual adjacencies are unchanged, so the same ambient-shortest conclusion holds. A graph with no induced three-vertex path is a disjoint union of cliques: a shortest path between two nonadjacent vertices in any noncomplete connected component begins with such a triple.

Suppose \(\omega(G)\leq n/2\), and an ambient geodesic \(P\) has \(|V(P)|+3\geq\lceil n/2\rceil\). If \(G-V(P)\) contains an induced three-vertex path \(Q\), then \(P\) and \(Q\) are disjoint ambient geodesics deleting at least \(\lceil n/2\rceil\) vertices. Otherwise each residual component is a clique of order at most \(\omega(G)\leq n/2\), so \(P\) alone works. This checks both branches of the path-extension lemma; no shortest-path computation in the residual graph is being substituted for an ambient geodesic.

For planar \(n\geq8\), \(\omega(G)\leq4\leq n/2\). In a connected graph, a diametral path has \(D+1\) vertices, giving the sufficient condition \(D+4\geq\lceil n/2\rceil\). For \(9\leq n\leq12\), choose any induced three-vertex path as \(P\): \(3+3\geq\lceil n/2\rceil\). If none exists, every component is a clique of order at most four and the graph is already half-balanced without deleting vertices.

For \(n\leq8\), the endpoint argument works in every graph. If no component exceeds \(n/2\), use the empty separator. Otherwise choose up to four vertices in the unique heavy component, partition them into at most two pairs or singletons, and take shortest paths joining each pair. The paths lie in that component and are shortest in the whole disjoint union. They remove the chosen vertices, leaving at most \(\max(0,n-4)\leq n/2\) vertices there; other components were already small. This includes \(n=0\) and \(n=1\).

The general \(k\)-path assertion follows by greedily deleting vertex-disjoint induced three-vertex paths. Either \(k\) paths delete \(3k\geq n/2\) vertices when \(n\leq6k\), or the residue is a union of cliques each of order at most \(\omega(G)\leq n/2\). In \(K_{3k,3k+1}\), any ambient geodesic has at most three vertices and deletes at most two from either bipartition class. After \(k\) paths, both classes remain nonempty and at least \(3k+1>(6k+1)/2\) vertices form one connected component. This proves sharpness for the stated general graph class. In particular \(K_{6,7}\) is a **nonplanar** 13-vertex control, not a counterexample to Problem 31.

The disconnected minimal-counterexample reduction is sound: a heavy component would have smaller order and, by minimality, its own two ambient geodesics would balance it and hence the original disjoint union. Therefore any minimum-order planar counterexample is connected. The diameter criterion then confines orders 13 and 14 to diameter two.

## Reproduction and trust boundary

With Python 3.11.2, I ran from the repository root:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_packing/verify.py --check
~~~

It returned PASS: 16 constructive fixtures, four packing controls, and 41,041 geodesic-mask pairs for the nonplanar \(K_{6,7}\) negative control, with minimum largest residual component seven. The committed expected JSON has SHA-256 fba11b2b1aafaa14f71474cf31cb9d83a24bb7cf1ede74b8b873d90d0383dba3. The checker verifies generated witness paths against ambient Floyd–Warshall distances, but its fixtures are not an exhaustive planar census and are not the basis of the universal theorem. The verdict rests on the elementary argument above. No external graph generator, solver, formal proof assistant, or large hidden dataset is used.

## Literature and publication assessment

[Diot and Gavoille (2010)](https://emilie-diot.eu/Article/DG10a) already give the general \(\lceil n/4\rceil\) endpoint-cover bound, which supplies the \(n\leq8\) case. Greedy maximal induced-three-vertex-path packings leaving a union of cliques also appear in [Fomin and collaborators' packing work](https://sites.cs.ucsb.edu/~daniello/papers/fvstcvdTalg19.pdf). The present note's contribution is the precise use of those paths as ambient geodesics for exact-half separation, the order-12 consequence, and the \(D+4\) diameter filter. Targeted searches did not locate that exact separator formulation in primary sources, but this does not establish literature priority. The lemma is ready to cite with a short self-contained proof; its elementary nature and unsettled priority make a standalone publication claim premature.

## Strengthening and improvement opportunities

1. **Proved broader finite corollary and sharp threshold.** Planarity enters the order-12 proof only through \(\omega(G)\leq4\). Hence **every \(K_5\)-free graph on at most 12 vertices** has the same two-geodesic half separator. This order threshold is sharp for the \(K_5\)-free class: \(K_{6,7}\) is \(K_5\)-free, has 13 vertices, and has no such separator. This sharpness concerns nonplanar graphs and says nothing negative about planar order 13.

2. **Narrow the next planar cases.** A connected planar counterexample at order 13 or 14 must have diameter two. Proving a structural separator lemma for planar diameter-two graphs at those orders, or giving an independently checkable finite census of precisely that class, would extend the bound. The present proof does not establish those cases.

3. **State the metric boundary sharply.** The packing proof extends to positive edge metrics only when each selected induced three-vertex path is still shortest between its endpoints. An induced path alone does not guarantee that for nonuniform lengths. A useful weighted extension would need a verifiable local condition ensuring the selected paths' ambient geodesicity; the current unweighted theorem does not provide one.
