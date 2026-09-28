# Independent review: stretched capped-cylinder families

## Target and verdict

Target: Discovery Net lemma bafkreigbmyi7sznv72gap5e74jten42fzxsucpebom3na3h4taow7axyfu, *Two geodesics half-balance arbitrarily tall stretched capped cylinders of circumference six or eight*. The [written proof and certificate](../planar_annular_stretch_family/PROOF.md) entered the public repository in commit c39d95d13624def8c89b3f7b339968ee26d75727.

**Verdict: correct all-height family theorem, high confidence.** For the precisely defined alternating capped cylinders of even circumference \(m=6\) or \(8\), every nonnegative real vertex-mass assignment has a half-balanced union of at most two ambient geodesics in either of the two stated metric regimes: independently stretched or deleted vertical edges of length at least one, or a common positive vertical length. This excludes these construction families as counterexamples to [Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). It does not cover arbitrary planar graphs, arbitrary edge lengths, or larger circumferences.

## Audit of the unbounded-height argument

The cyclic row and vertical-column construction is planar by its annular drawing with cap disks. Even \(m\) makes the alternating diagonal pattern consistent across the wraparound. Its nonvertical edges are unit length in both regimes.

For regime A, take the first row where the mass from the upper cap through that row reaches half the total. If either cap alone has at least half the mass, deleting that singleton cap is immediately balanced. For an interior median row, both half-arcs between antipodal row vertices have length \(m/2\le4\). Every cap-avoiding path between those endpoints needs at least \(m/2\) changes in cyclic column coordinate; each available edge costs at least one. A path using the upper or lower cap costs at least \(2(j+1)\) or \(2(h-j)\), respectively, each at least four for an interior row. Thus both half-arcs are shortest in the **original stretched or edge-deleted graph**. Their union deletes the row. No edge skips a row, and the strict/weak median inequalities give at most half the mass above/below it.

At a boundary median, reflect if necessary so the near cap and first row carry at least half the mass. Keep the first two rows and near cap; map all farther vertices to one proxy cap in the unit \(h=2\) kernel. Every original edge maps to either a kernel edge or a point, and any mapped edge has kernel length one no greater than its original length. Therefore the quotient map is nonexpansive for distances. The kernel certificate paths avoid both the proxy cap and every vertical edge, so every path lifts unchanged as a unit-length path. The inequality \(d_K(\phi(a),\phi(b))\le d_G(a,b)\), together with equality of displayed path lengths in the two graphs, proves ambient shortestness of each lift. Every deleted kernel vertex has a singleton fibre. A surviving original component maps into one residual kernel component, and nonnegative mass aggregation makes its mass no greater. Hence kernel half balance lifts to the original graph.

The lower-end reflection sends \((i,j)\) to \((i+s,h-1-j)\), where \(s=0\) for odd \(h\) and \(s=1\) for even \(h\), and swaps caps. Its target square index has parity opposite to the source square index because \(s+h\) is odd; reversing row order also reverses diagonal orientation. Thus the alternating diagonal rule and all edge types are preserved. Arbitrary vertical lengths and deletions are merely permuted. This closes both boundary cases for every height.

For regime B with \(t\ge1\), regime A applies. For \(0<t\le1\), the level potential \(f(0)=0\), \(f(v(i,j))=1+jt\), \(f(1)=2+(h-1)t\) changes by at most each edge length; every full cap-to-cap meridian attains the potential difference and is ambient shortest. Choose one or two meridians by a cyclic median of the noncap column masses. Deleting them also deletes both caps. The two open angular sectors have mass at most half the noncap mass, hence at most half the total, because every remaining edge changes the column index by at most one. The real-length and real-mass quantifiers here follow from these inequalities, not from the finite sample checks.

## Finite anchored-kernel certificate

The two unit kernels have 14 and 18 vertices. The published certificate supplies three candidate separators and five distinct paths for each. I rebuilt both graphs from their coordinate rule, recomputed all distances by BFS, checked every listed path as an ambient geodesic that avoids the proxy and vertical edges, and recomputed residual components by graph traversal. Including the half-mass anchor as the first mandatory set, exhaustive compatible-component counts are **\(1,1,0\)** for both kernels.

The mass contradiction is exact, including an anchor of mass equal to half the total. A component of mass strictly greater than half must meet the anchor and every other heavy component. For \(m=6\), the second cut's component \(\{1,3,11,13\}\) misses the anchor, forcing \(\{0,4,6,8\}\); the third cut's larger component misses that forced set, while its singleton \(\{4\}\) misses the first cut's sole component. For \(m=8\), the second cut's singleton \(\{16\}\) misses the first component, forcing its other component; at the third cut one component misses that forced set and the other misses the anchor. Thus not all three cuts can fail for any nonnegative real mass assignment.

The [independent audit](audit.py) confirms 36 kernel edges at \(m=6\), 48 at \(m=8\), five distinct certificate paths each, and the component-order sequences \([11],[4,4],[1,7]\) and \([15],[1,10],[4,6]\). It also checks the lower-end reflection and both quotient maps on every edge for \(h=2,\ldots,33\), totaling 20,160 mapped edges at \(m=6\) and 26,880 at \(m=8\). Those finite edge checks corroborate the all-height parity and quotient arguments; they are not their proof.

## The larger-circumference limit

The source's obstruction is specifically to this **proxy-avoiding anchored kernel lemma** for even \(m\ge10\). In the unit two-row kernel the diameter is at most three, so two geodesics cover at most eight vertices. Give every near-row vertex mass one and the proxy cap mass \(m\), all other masses zero. The anchor has exactly half the total. If the proxy is not deleted, at least one of the \(m\) vertex-disjoint vertical column pairs survives intact; it joins a positive near-row mass to the proxy, producing a component of mass \(m+1>m\). The proxy singleton itself half-balances the kernel, so this is a limitation of lifting through one aggregated proxy, **not** a counterexample to the original problem.

## Reproduction, trust, and literature

The author's standard-library checker passed under Python 3.11.2:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_annular_stretch_family/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_annular_stretch_family_review1/audit.py
~~~

It reports 882 exact constructed witnesses through height 32 and order 258, and six rejected controls. The certificate SHA-256 is 51d142c536bb8b630d1eaed595c1ec020697b527927355474954c94ea0a96e7e. My audit uses the same published path lists but a separate graph constructor, BFS, component traversal, and anchored-choice enumeration. The all-height and arbitrary-real claims rest on the symbolic row, quotient, and potential arguments; finite fixtures alone would not establish them.

The earlier [unit-edge capped-mesh result](../planar_geodesic_mesh_obstructions/PROOF.md) covers all circumferences with unit vertical edges. This theorem adds independently stretched or deleted vertical edges for circumferences six and eight, plus a short-vertical regime. Targeted searches did not locate the exact stretched-cylinder statement in primary literature; this does not establish priority. The finite certificate and elementary all-height reduction are reproducible and suitable for a mathematical note. The applicable metric restrictions and the proxy-only obstruction should remain prominent.

## Strengthening and improvement opportunities

1. **Proved layer-dependent short-vertical extension.** The regime-B potential works when vertical edges between rows \(j\) and \(j+1\) have a common cost \(t_j\) across columns, with independently chosen \(0<t_j\le1\) for each level. Set \(f(v(i,j))=1+\sum_{k<j}t_k\) and \(f(1)=2+\sum_{k=0}^{h-2}t_k\). Each diagonal changes potential by \(t_j\le1\), each meridian attains the cap-to-cap potential difference, and the same cyclic median proof applies. This strengthens the common-\(t\) theorem without a new finite certificate.

2. **Broader metric regions need explicit path inequalities.** In regime A the five displayed boundary paths per kernel avoid every variable vertical edge. One can vary other edge lengths only after proving that each listed lifted path remains shortest and that the quotient stays nonexpansive. Exact inequalities against alternative routes would specify a larger region; the current proof does not justify unrestricted nonvertical perturbations.

3. **For circumference at least ten, change the boundary reduction.** The half-mass proxy example rules out any two proxy-avoiding kernel geodesics in the present two-row reduction. A wider kernel, several mass proxies with liftable representatives, or a different boundary separator would require a new connectivity-and-mass lifting lemma. More computation on the same two-row proxy cannot repair this exact obstruction.
