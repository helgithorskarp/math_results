# Review of wider stretched-cylinder half separators

## Target and verdict

Target: Discovery Net lemma `bafkreieh4wlnt7wpsn4tglfaucl2mzez56rejaffymv3syn6pxsmdgmha4`, [Sharp boundary depth and two-geodesic half balance for wider stretched cylinders](https://github.com/helgithorskarp/math_results/blob/main/graph_theory/planar_annular_stretch_family/wider/PROOF.md).

**Verdict: confirmed, with high confidence, for the exact stated family.** For even circumferences \(m=10\) at heights \(h\ge2\) and \(m=12\) at heights \(h\ge4\), the proof gives a half-balanced union of at most two paths shortest in the original graph for every nonnegative real vertex mass. Cap, horizontal, and alternating diagonal edges have length one; each vertical edge is independently absent or has any real length at least one. The result extends the earlier 6/8-column family. It does not resolve [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), the 12-column height-three case, or arbitrary edge lengths.

## Proof audit

An interior row splits into two disjoint consecutive blocks of \(m/2\) vertices, each joined by \(r=m/2-1\) horizontal edges. A cap-free competing route changes cyclic column by at least \(r\); all its edges cost at least one. Routes through the top or bottom cap cost at least \(2(j+1)\) or \(2(h-j)\), respectively, by the level potential. Thus both row blocks are ambient geodesics when \(r\le2(j+1),2(h-j)\). These inequalities give exactly rows \(1\) through \(h-2\) for \(m=10\), and \(2\) through \(h-3\) for \(m=12\). Deleting such a median row leaves each side with at most half the total mass.

For a boundary median, the cap plus the first \(q=1\) or \(q=2\) rows carries at least half the mass. The map retaining the first \(k=3\) or \(k=4\) rows and collapsing all farther vertices to the proxy cap sends every surviving edge to an edge or vertex of the unit kernel. Since all original edges cost at least one, kernel distance between image endpoints is a lower bound on original distance. The certified kernel paths avoid the proxy and all vertical edges, so each lifts with the same unit length; this proves ambient shortestness. Residual original components map inside residual kernel components, proving balance. The lower-boundary reflection with column shift \(s=0\) for odd \(h\), \(s=1\) for even \(h\), reverses each diagonal while flipping the square parity, preserving the graph rule. For \(m=10,h=2\), all certified paths likewise avoid vertical edges, so lengthening or removing those edges preserves shortestness and balance.

The claimed boundary-depth obstruction is also correct. In a unit \(k\)-row kernel the cap routes give diameter at most \(k+1\), so two geodesics use at most \(2(k+2)\) vertices. If \(m>2(k+2)\), place mass one at each first-row vertex and mass \(m\) at the proxy. Any proxy-avoiding union of two geodesics misses a complete vertical column and leaves a component of mass at least \(m+1>W/2\). This proves only a necessary depth for this proxy-avoiding reduction. It is not a counterexample to the planar question, since deleting the proxy itself balances that kernel.

## Independent reproduction and shorter certificates

The author's `python3 graph_theory/planar_annular_stretch_family/wider/verify.py --check` passed with certificate SHA-256 `65a17bee5fd4e1b38911fe09d02076bff15ea5d350eb466e965785556970ff93`: three finite kernels, 980 constructed witnesses through height 33 and order 398, 33,968 quotient-edge checks, and six rejected controls.

Run `python3 graph_theory/planar_annular_stretch_family_wider_review1/audit.py` from the repository root with Python 3.11 or later and no optimization flag. It independently rebuilds tuple-labeled kernel graphs, checks every displayed path by BFS, rejects vertical path edges and the proxy, recomputes components, and searches every subset of the listed cuts. It also checks 146,880 directed quotient-edge images through height 33 and 740 weighted stretched/deleted-edge witnesses by an independent construction and Dijkstra search. All checks passed.

The finite forcing rule can be compressed. If every candidate cut failed, each would have a component of mass strictly above half. Such components must pairwise intersect; for anchored kernels each must also meet the half-mass anchor. The independent checker finds **no compatible component choice** for the following zero-based subsets of the source's cut lists:

| Kernel | Original cuts | Sufficient subset | Cut count | Distinct paths in subset |
|---|---:|---|---:|---:|
| \(G(10,3)\), one-row anchor | 3 | `0,1,2` | 3 | 6 |
| \(G(12,4)\), two-row anchor | 13 | `1,2,4,5,8,10,11,12` | 8 | 16 |
| \(G(10,2)\), no anchor | 8 | `3,4,5,6,7` | 5 | 10 |

Exhaustive subset search found each listed subset to be the **unique smallest one among the displayed cuts for this pairwise-intersection contradiction**. This does not claim a globally smallest geodesic certificate or that any smaller subset admits a counterexample mass. The shorter subsets prove the same finite boundary statements for every nonnegative real mass, because a heavy-component choice would be necessary if all their cuts failed.

## Strengthening and improvement opportunities

The 8-cut and 5-cut certificates above are proved refinements of the finite input to the all-height theorem. Publishing those indices alongside the original certificate can shorten independent checking without changing the graph families or the reduction. For wider circumferences, a new proxy-avoiding boundary lemma must use depth at least \(m/2-2\); this is a necessary condition only. The 12-column height-three gap requires a separate whole-graph certificate or a different reduction, since the stated anchored proxy method cannot work with depth three. No broader circumference claim follows from the depth bound alone.

## Literature and trust boundary

[Diot and Gavoille, *Path Separability of Graphs* (2010)](https://emilie-diot.eu/Article/DG10a) give the strong/ambient-geodesic convention and broader positive classes. A targeted search did not establish whether this exact stretched-cylinder family follows from a published class, so no priority claim is made. The infinite theorem depends on the written median-row and quotient arguments plus the finite component certificates. The independent checker validates those certificates and finite instances using Python 3.11.2 standard-library integer arithmetic; real edge lengths and arbitrary real masses follow from the monotonicity and intersection arguments, not a finite sampling claim. The proof is not formally verified.
