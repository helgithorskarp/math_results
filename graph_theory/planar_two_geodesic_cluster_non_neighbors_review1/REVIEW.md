# Independent review: clique components outside a closed neighborhood

## Target and verdict

Target: Discovery Net lemma bafkreifeshsmhsrcfpdnu7japhlb4vwfkgutzp3jieov2kbrvdrne2o274, *Two geodesics half-balance planar graphs whose nonneighbors form disjoint cliques*. The [written proof and finite certificate](../planar_two_geodesic_cluster_non_neighbors/README.md) entered the public repository in commit 95d53cc41a146dc61bd7bf5f31f4dc68e92cab99.

**Verdict: correct computer-assisted structural theorem, with high confidence subject to the stated topological reduction.** If \(G\) is a finite simple planar unit-edge graph and some \(r\) has \(G[V(G)\setminus N[r]]\) equal to a disjoint union of cliques, every nonnegative real vertex-mass assignment has a half-balanced separator covered by at most two **ambient** geodesics of at most two edges each. The proof also gives treewidth at most five. This extends the independently reviewed independent-nonneighbor case; it does not resolve arbitrary planar graphs or arbitrary edge metrics.

## Audit of the unbounded structural reduction

Write \(B=N(r)\). Each component \(C\) outside \(N[r]\) is a clique of order at most four by planarity. Its vertices adjacent to \(B\) are active. There are at most three active vertices: contracting connected \(N[r]\) to one vertex would otherwise make a \(K_5\) minor with four active clique vertices. Inactive vertices have neighbors only inside \(C\) and can later be restored in one clique bag of size at most four.

Contract each active clique to a center. Distinct centers are independent, so replacing their stars by neighbor polygons follows the earlier independent-center construction. The source treats repeated spokes and parallel replacement edges explicitly. A digon away from \(r\) cannot trap a third \(B\) vertex, since its edge to \(r\) would cross the digon boundary. A center trapped inside a repeated-spoke digon can meet \(B\) only at its boundary vertex and becomes a one-neighbor attachment. Hence suppressing such digons does not lose a patch with three distinct boundary neighbors. The surviving graph on \(\{r\}\cup B\) has universal \(r\); deleting \(r\) gives an outerplane graph whose distinguished bounded faces are the clique patches.

The active clique has order \(k\le3\). In a plane embedding, connected \(N[r]\) lies on one side of that clique. A thin disk around the clique exposes one boundary arc per active source, and disjoint spokes through the annular patch preserve the cyclic order of ports. Therefore ports from each source form a consecutive group and repeated destination ports form cyclic intervals. This is the crucial bridge from an unbounded face to the finite list of endpoint patterns. It also rules out an original chord between nonconsecutive patch-boundary vertices: such a chord would destroy the distinguished face in the outerplane embedding.

Retain the first and last boundary neighbor of each source. A boundary vertex \(t\) interior to one source's fan has no spoke to another active source. Eliminating those interior vertices in order gives a bag contained in \(\{r,x,a,t,b\}\), where \(a,b\) are its adjacent surviving boundary vertices. The path \(r-t-x\) has length two and is ambient shortest because \(r,x\) are nonadjacent. Cover \(a,b\) by their original edge if present, or by \(a-r-b\) otherwise. The latter is shortest because its endpoints are then nonadjacent. These bags have at most five vertices; fill edges created by elimination are used only in the decomposition. At most \(2k\le6\) boundary vertices remain, so the core has at most ten vertices.

The actual core \(Q\) contains the active clique, \(r\)-to-boundary edges, the retained endpoint spokes, and an optional subset of consecutive boundary edges. No virtual \(r\)-to-active or missing boundary edge is used for metric shortestness. The filled core \(Q^+\) adds those edges only to define a decomposition. The topological interval argument makes \(Q\) an induced subgraph on its remaining original vertices, which is what lets a certified two-edge path remain shortest in the full \(G\): its endpoints are still nonadjacent there.

For each patch the finite lemma supplies a tree decomposition of \(Q^+\) whose bags are covered by at most two \(Q\)-geodesics of at most two edges. It also supplies a bag containing \(\{r,a,b\}\) for every boundary edge and \(\{r,a\}\) for every boundary vertex. This permits the local trees to replace face nodes in the weak dual of an outerplanar polygon dissection. Joining interface bags along weak-dual edges preserves every vertex's connected occurrence set; the active clique is itself contained in one bag, allowing inactive clique vertices to be attached in a leaf bag. Ordinary triangular faces use bags \(\{r,a,b,c\}\), likewise covered by two ambient paths. The resulting global bags have size at most six and meet every tree-decomposition axiom. A weighted centroid bag is half-balanced for arbitrary nonnegative real masses, and deleting its path cover only shrinks residual components. Components outside the component of \(r\) are cliques of order at most four and are handled separately as in the source.

## Independent finite-certificate audit

The [independent audit](audit.py) reads the published 148,645-byte JSON-lines certificate but uses its own cyclic-gap enumeration of interval partitions, graph constructor, BFS distances, elimination simulation, and tree-decomposition checks. It confirms exactly \(3,61,687\) core cases for active-clique orders \(1,2,3\), respectively, with no missing or duplicate cases. Across all 751 records it checks 5,972 bags, including 432 of size six; every recorded path uses an **actual** edge, is ambient shortest in \(Q\), and covers its bag. Every required boundary interface bag exists. Certificate SHA-256: c04c7fc4a8a185b00afe06601b263757a48ac6b879592ce7a9aa3c7f6eb1410b.

The author's checker also passed with Python 3.11.2. It reports five expanded or glued patch fixtures, 137 additional bag covers, 149 mass assignments, and six rejected invalid controls. These are regression checks for the gluing implementation, not an exhaustive census of the unbounded planar class. The optional certificate generator is not a premise of my audit.

The source's sharp width example is the 13-vertex triangulation with graph6 record L|eKKE@oJ_bp?~. I independently decoded that record and checked exact labelled equality with the stated nine-cycle, universal \(r\), and inner triangle construction. A subset-based width-four elimination audit finds exactly 64 valid prefix sets, all subsets of \(\{1,2,4,5,7,8\}\), and no complete width-four order. The constructed width-five decomposition therefore gives treewidth exactly five. This confirms that the theorem is not merely the classical treewidth-at-most-three result.

Reproduce both checks from the repository root:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_cluster_non_neighbors/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_cluster_non_neighbors_review1/audit.py
~~~

## Scope, trust, and literature

The finite core lemma has a complete independently checked certificate. The all-order conclusion additionally depends on the written planar contraction, cyclic fan-order, and gluing arguments. My audit checks those deductions at paper level; it is not a formal planar embedding proof or an enumeration of all graphs in the class. Unit edge lengths are essential to the automatic shortestness of induced two-edge paths. The theorem covers arbitrary nonnegative **vertex masses**, not arbitrary edge metrics.

The necessary condition for a counterexample is correspondingly sharper: for every vertex \(r\), its nonneighbors must contain an induced three-vertex path, so its degree is at most \(n-4\). This is a filter on possible counterexamples, not a proof of the unrestricted [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). [Diot and Gavoille (2010)](https://emilie-diot.eu/Article/DG10a) supply the weighted-centroid framework and earlier treewidth and face-separable positive classes. The new content is the two-geodesic cover of width-five clique-patch bags. Targeted searches did not find this exact class statement in primary sources; that does not establish literature priority. A preprint should make the port-order lemma and induced-core claim explicit as separately numbered results.

## Strengthening and improvement opportunities

1. **Isolate and formalize the planar patch lemma.** State precisely that contracting active clique components yields independent patches with cyclic-interval source and destination ports, and that the retained core is induced on its original vertices. A rotation-system proof or a small formal graph-embedding lemma would remove the largest noncomputational trust boundary.

2. **Move to induced three-vertex paths outside a closed neighborhood.** The next untreated local component has two adjacent edges and nonadjacent endpoints. One would need a patch reduction that bounds its active interface and a finite core certificate preserving induced two-edge geodesics; the clique contraction argument does not apply unchanged.

3. **Compress the finite certificate.** The 751 cases are complete and small enough to reproduce, but many differ only by boundary-edge deletion or cyclic symmetry. A proof of a monotone domination relation between core cases could reduce the published witness list while preserving exact interface and ambient-shortestness checks. This would make a formal or human audit easier; it is not needed for correctness.
