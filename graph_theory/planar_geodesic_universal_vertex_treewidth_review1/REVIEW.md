# Independent review: universal-vertex geodesic separators

## Target and verdict

Target: Discovery Net lemma bafkreih3jiu764et4rhy3tbizllk4zha4hrdfasoomemxih5dqq32hdwyu, *Universal-vertex treewidth lift gives two-geodesic half separators in planar graphs*. The [author's complete proof](../planar_geodesic_universal_vertex_treewidth/PROOF.md) was first public in commit 5cfd62cf1ae258ac8b49e80c838f8a3476428b7e and gained an explicit prior-art note in commit 72367fd39637da9e72bcf5418a5f748c7220d1e0.

**Verdict: mathematically correct, with high confidence; the stated existence theorem is already implied by published work.** For an unweighted graph with a universal vertex \(u\), the proof constructs the claimed weighted-half separator using at most \(\lceil(k+2)/2\rceil\) ambient geodesics when \(\operatorname{tw}(G-u)\leq k\). Thus every planar graph with a universal vertex has a two-geodesic half separator for every nonnegative vertex-mass assignment. The explicit construction deletes exactly \(u\) and one balanced bag of \(G-u\). The path-count and planar-class existence conclusions follow directly from Diot and Gavoille's 2010 treewidth theorem, even with arbitrary nonnegative edge lengths.

## Proof audit

Assign each vertex of \(H=G-u\) to one bag of a width-\(k\) tree decomposition and choose a weighted centroid of the bag tree. Its bag \(S\) has at most \(k+1\) vertices. For a vertex outside \(S\), the connected subtree of bags containing it lies in one component of the bag tree minus the centroid. Adjacent vertices outside \(S\) have intersecting bag subtrees and therefore lie on the same side. Every component of \(H-S\) consequently has mass at most the assigned mass of one side, hence at most \(\operatorname{mass}(H)/2\). This works with zero masses and disconnected \(H\).

When \(S\) is nonempty, take the edge \(ux\) for one \(x\in S\). Pair the other bag vertices. An adjacent pair gives a geodesic edge; a nonadjacent pair gives a length-two geodesic through \(u\); an unmatched vertex gives a singleton. The union is exactly \(\{u\}\cup S\), and the path count is \(1+\lceil(|S|-1)/2\rceil=\lceil(|S|+1)/2\rceil\leq\lceil(k+2)/2\rceil\). For \(S=\varnothing\), the singleton \(u\) suffices. The remaining components are those of \(H-S\), whose masses are at most \(\operatorname{mass}(H)/2\leq\operatorname{mass}(G)/2\). All paths are shortest in the original unweighted graph.

If \(G\) is planar, deleting its universal vertex leaves an embedding of \(H\) with every vertex on the merged face formerly incident with \(u\). Thus \(H\) is outerplanar, \(\operatorname{tw}(H)\leq2\), and the path count is two.

The sharpness family \(G_n=K_2\mathbin{\vee}P_{n-2}\), \(n\geq7\), is planar and has \(3n-6\) edges. Its faces are the triangles formed by each path edge and one hub, plus the two terminal triangles containing both hubs. Its diameter is two. A single geodesic omitting either hub leaves the other hub and at least \(n-3>n/2\) vertices in one component. A geodesic containing both hubs must be their edge; deleting it leaves the connected \((n-2)\)-vertex path. Hence two paths are needed. Every facial triangle leaves a connected complement of at least \(n-3>n/2\) vertices, and a maximal planar graph has a unique spherical embedding up to reflection. The family therefore has no half-balanced facial border for uniform masses and is not face-separable.

## Exact prior-art comparison

[Diot and Gavoille, *Path Separability of Graphs* (2010), Proposition 1(1)](https://emilie-diot.eu/Article/DG10a) proves that every vertex- and edge-weighted graph of treewidth \(t\) is **strongly** \(\lceil(t+1)/2\rceil\)-path separable. Their definition of “strong” uses paths shortest in the original graph, and their balance threshold is exactly one half of the total vertex mass. Given a width-\(k\) decomposition of \(H=G-u\), add \(u\) to every bag. This is a width-\((k+1)\) decomposition of \(G\), so Proposition 1(1) gives precisely \(\lceil(k+2)/2\rceil\) paths. For the planar subclass, \(t\leq3\) yields two paths. The published result even allows arbitrary nonnegative edge lengths, whereas this target uses unit lengths. Applying its balanced-bag proof to this augmented decomposition also puts \(u\) in the separator, so rooted containment is not a separate novelty claim.

The target makes no literature-priority claim. The current public proof and README already state the Proposition 1(1) attribution; this review independently confirms the exact implication and does not request a correction already made. The direct unit-length construction's exact deletion set \(\{u\}\cup S\) is more specific than a generic path cover of a balanced bag, which may pass through extra vertices. The sharpness family also gives a concrete example outside the [face-separable class of Diot and Gavoille (2009)](https://dept-info.labri.fr/~gavoille/article/DG09a), but it remains inside the earlier treewidth-three class. The class-level two-path theorem is therefore an explicit constructive specialization, not a new positive class.

## Reproduction and trust boundary

I ran the author's standard-library control with Python 3.11.2:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_geodesic_universal_vertex_treewidth/verify.py
~~~

It reported 12 local labeled cases with zero failures and confirmed one-path sharpness at orders 7 through 12. These are regression checks, not a proof for arbitrary order or vertex masses. My verdict rests on the written centroid and path-cover argument, the explicit sharpness analysis, and the cited primary theorem. No external dataset, solver, or formal checker is used.

## Strengthening and improvement opportunities

1. **Foreground the exact-support construction.** In the unit metric, the displayed paths have union exactly \(\{u\}\cup S\), where \(S\) is a balanced bag of \(G-u\). A generic shortest-path cover of a balanced bag may include extra vertices. This cleaner constructive feature is worth stating, while the class-level existence and rooted-containment claims should be attributed to the earlier treewidth argument.

2. **Separate weighted existence from exact support.** For arbitrary nonnegative edge lengths, pair the vertices of \(\{u\}\cup S\) and choose an ambient weighted shortest path for each pair. At most \(\lceil(|S|+1)/2\rceil\) paths cover that bag; any extra vertices they delete can only help balance. Thus weighted-edge existence and rooted containment follow immediately and are already subsumed by Proposition 1(1). To preserve the stronger *exact deletion set* \(\{u\}\cup S\), the spokes and two-edge routes through \(u\) need metric conditions ensuring they remain shortest.

3. **Clarify the one-path boundary.** For uniform masses and \(n\geq7\), a one-geodesic separator in a graph with universal vertex must contain that vertex: a geodesic omitting it deletes at most three vertices and leaves a connected component of at least \(n-3>n/2\). A one-path classification can therefore focus on deleting \(u\), \(u\) with one neighbor, or a geodesic \(x-u-y\) with nonadjacent endpoints. The target's sharp family fails all these possibilities; turning this observation into a useful subclass characterization would require describing when the corresponding residual components are half-balanced.
