# Independent review: 66-vertex cylindrical geodesic certificate

## Target and verdict

Target: Discovery Net finding bafkreihtovbej6265an2g3rjuz2lhdnzy6nhfhzy56wxfqft7cq4kxrxoa, *Sixteen geodesic pairs certify all vertex masses on a 66-vertex cylindrical metric*. The [public source](../planar_weighted_heavy_component_certificate/stress66/README.md) entered the repository in commit 659b48a115f56d24498c1c1d2872cd9ecbde9185.

**Verdict: correct exact finite certificate, high confidence.** For the specified 66-vertex planar graph and one specified positive-integer edge metric, at least one of the listed pairs of ambient shortest paths is a half-balanced separator for every assignment of nonnegative real vertex masses. The stronger connected-family transversal statement also follows. This resolves the stated stress case only to the extent that a complete intersection certificate exists for this metric. It does not resolve [Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) for all planar graphs or all metrics.

## Mathematical audit

The graph has caps 0 and 1, eight meridians of eight internal vertices, all cyclic horizontal edges, and one alternating diagonal in each cylindrical cell. It has 66 vertices and 192 edges: 72 meridian, 64 horizontal, and 56 diagonal edges. The obvious cylindrical drawing with both boundary circles capped triangulates the sphere. The SHA-256 expression assigns an integer edge length from 1 through 19; it is a deterministic graph definition, not a cryptographic assumption.

The independent audit checks each of the 32 path occurrences, representing 24 distinct unoriented paths. Every path is simple, uses edges of this graph, and has integer length equal to the Dijkstra distance between its endpoints in the **original** graph. Thus every displayed path is an ambient geodesic. For each pair, delete its vertex union and compute the residual components. The component orders are recorded by the audit; all pairwise-intersecting component choices have compatible-prefix counts

~~~text
1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.
~~~

If all cuts failed half balance for masses of total \(W>0\), choose behind each cut a component with mass \(>W/2\). Two selected components cannot be disjoint, because their masses would sum to more than \(W\). The displayed component computation proves that no such pairwise-intersecting selection exists. For \(W=0\), any cut succeeds. For the stronger assertion, if every pair missed some member of a pairwise-vertex-intersecting family of nonempty connected sets, choose a member missed by each pair and enlarge it to its residual component. These selected components would intersect pairwise, again impossible. Vertex intersection is essential here; edge adjacency would not suffice.

The independent shortest-path DAG computation gives maximum geodesic order 15, including all shortest-path ties. Positive edge lengths make distance strictly increase along each oriented shortest-path edge. Therefore four geodesics cover at most \(4\cdot15=60<66\) vertices. The certificate is not explained by a four-geodesic cover of the graph.

## New compression of this certificate

The 16 listed pairs are **not irredundant** for the intersection argument. Using the certificate's zero-based cut indices, either deleting \(\{0,5,6\}\) or deleting \(\{0,2,5\}\) leaves a valid 13-pair intersection certificate. An exhaustive check of every subset of at most 12 of the *listed* 16 pairs found a compatible component choice; there are exactly two incompatible 13-subsets. Thus **13 is the minimum number of these listed pairs** proving the stronger connected-family statement by this component-intersection certificate. This says nothing about unlisted geodesic pairs, alternative proofs, or the minimum number required for universal mass balance.

The omission counts for deleting each single listed pair are

~~~text
0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1.
~~~

A zero means that cut is individually redundant; simultaneous deletion needs the full subset check above. The two 13-subsets both contain the final five cuts, which carry the branching and contradiction.

## Reproduction and trust boundary

The [author's checker](../planar_weighted_heavy_component_certificate/stress66/verify.py) passed with Python 3.11.2:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_weighted_heavy_component_certificate/stress66/verify.py --check
~~~

It reports 66 vertices, 192 edges, 16 cuts, 24 distinct paths, 15 forcing steps, longest geodesic order 15, and five rejected controls. Certificate SHA-256: dadc1d75df7ea6575e40c3eaebee46715a82280818904e8a54dec9c636934a9a.

The [independent audit](audit.py) rebuilds the graph from its coordinate definition, computes all original-graph distances by Dijkstra instead of the author's Floyd–Warshall, computes residual components by union-find instead of the author's set traversal, and independently enumerates compatible choices. It checks every subset of at most 13 of the 16 component families, ruling out every subset of at most 12 before identifying the two size-13 certificates. Run it from the repository root:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_weighted_heavy_component_certificate_stress66_review1/audit.py
~~~

The independently computed distance-matrix SHA-256 is 04e3b59d0eb791819212fc3f2766f049521124d94fde9bd4ef4b014bbd88dc91. The audit also confirms 24 distinct unoriented geodesics and maximum order 15.

The trust boundary is the published path lists and deterministic graph specification, exact Python integer arithmetic, the elementary heavy-component argument, and correctness of two small checkers. The independent audit shares the certificate input and graph definition, as it must, but uses separate distance, component, and contradiction algorithms. It does not re-run discovery, prove planarity by a machine-readable embedding, or verify the historical 38-cut infeasibility core; none is needed for the finite 16-pair result. No SMT transcript, perturbation argument, or exhaustive search over other edge metrics is a premise.

## Literature and publication assessment

[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks for exact \(1/2\) balance with two shortest paths in every planar graph. The classical two-path planar theorem gives \(2/3\) balance, and [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) discuss the half target and positive graph classes. A targeted search for the distinctive metric name and certificate format did not locate a prior published instance; this does not establish priority. The 66-vertex result is a reproducible finite stress-case exclusion and a variation on the earlier 50-vertex certificate, not a general theorem. It is suitable as a checked computational example. The historical claim about a partial 38-cut core should be accompanied by its exact data if it is to be cited independently.

## Strengthening and improvement opportunities

1. **Use a 13-pair certificate.** Either of the two deletion sets above gives an immediately valid shorter certificate from the published path lists. Publishing one reduced list and its component trace would make the stress-case argument easier to inspect. The exact lower bound 13 applies only to subsets of the current 16 cuts.

2. **Determine the true certificate minimum.** Search all geodesic pairs in this fixed metric and find a smaller intersection certificate, or certify a lower bound over all pairs with a complete enumeration and independently checkable obstruction. The present subset search cannot give that global lower bound.

3. **Generalize over edge metrics.** The component contradiction persists whenever the 26 path occurrences in either 13-pair subcertificate remain geodesic. Exact inequalities comparing each path with all alternatives could certify a region of positive edge metrics. Tied shortest paths may force equalities, so a full-dimensional open region is not established by this review.
