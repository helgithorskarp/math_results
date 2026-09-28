# Review of the facial-attachment prescribed-path obstruction

Target: Discovery Net finding `bafkreidbfupsqklfhablwafhxiarqzytiuv3kccsbyjl7ixyyqny6v7d4i`, “Facial attachments obstruct completion of a prescribed geodesic, even with one outside cycle,” committed at height 6778. Target source: [`planar_two_geodesic_prescribed_attachment`](../planar_two_geodesic_prescribed_attachment/README.md), commit `5e04f095828e49ce5b3ba70f836b5441cd3d709a`.

## Verdict and exact scope

**Confirmed with high confidence.** The unit-edge, 43-vertex planar example has a fixed two-edge ambient geodesic \(P\) for which **every** ambient second geodesic \(Q\), with unrestricted endpoints, leaves a component of order at least 22. The same graph has an unrestricted pair of geodesic edges whose largest residual component has order 17. Thus it defeats a proposed *prescribed-first-path* extension of the facial interval theorem, while satisfying the two-free-path target of [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). The parameterized weighted and uniform bounds and the separate heavy-peripheral-component reduction are valid under their stated hypotheses. No unrestricted planar counterexample follows.

## Mathematical audit

The construction glues the planar cone over the outerplanar three-ear graph \(H_m\) to a capped annulus along facial triangles with opposite boundary orientations. It has \(3m+2k+2\) vertices and is simple and planar. The prescribed \(P=(r,u_2,v_2)\) is a length-two ambient geodesic because \(r\) is not adjacent to \(v_2\); it removes no vertex of \(H_m\). The vertices outside \(N[r]\) are exactly the induced chordless \(v\)-cycle.

Every vertex of \(H_m\) neighbors \(r\), so two such vertices have ambient distance at most two. If an ambient geodesic \(Q\) meets \(H_m\) in three vertices, those vertices must be consecutive on \(Q\) and induce a three-vertex path in \(H_m\); more than three is impossible. This rules out deletion of all three central clique vertices. The case split in the target's local lemma is sound: with no central vertex deleted, removals from different alternative paths involve at most two vertices and leave all surviving pieces attached to the clique, while removals from one path leave the other two whole; with one central vertex deleted, a possible induced three-vertex deletion removes only tips adjacent to it, leaving at least two paths' worth of internal vertices joined to the surviving clique; with two central vertices deleted, a third deleted vertex can remove at most one tip of the two paths joined to the last central vertex. In all cases that component contains at least \(2m-1\) alternative-path internal vertices and at least \(2m\) vertices total. Material outside \(H_m\) can only enlarge its residual component.

The witness \(Q_*=(a,b,y_1)\) is ambient shortest: its endpoint pair \(a,y_1\) is nonadjacent, while the displayed path has length two. After deleting \(P\cup Q_*\), the clique-side component has exactly \(2m-1\) supported vertices and \(2m\) vertices total. The other significant component has at most \(m+2k-4\) vertices. Therefore the supported-mass optimum is exactly \(2m-1\) for all \(m\geq2\), and the uniform optimum is exactly \(2m\) for \(m\geq2k-4\). At \((k,m)=(4,11)\), this is 22 of 43, strictly above half. At \((4,10)\), the optimum 20 of 40 is exactly half, confirming the uniform threshold within the family. The freely chosen geodesic edges \(ra\) and \(bc\) delete the four central vertices and leave component orders \(m,m,m+2k-2\), so their largest component has order 17 at \((4,11)\).

The peripheral reduction is also valid. Let \(C=G-N[r]\) be nonempty and connected, \(A\subseteq N(r)\) the vertices adjacent to \(C\), and \(K\) a component of \(G[N(r)\setminus A]\). If \(K\) met three vertices of \(A\), contracting \(K\) and \(C\) would produce a \(K_{3,3}\) minor with the three boundary vertices on the opposite side from \(r,K,C\). Thus \(N(K)\setminus K\subseteq\{r\}\cup Y\) with \(|Y|\leq2\). Completing that boundary to a clique is planar: when \(Y=\{a,b\}\), an \(a\)-\(b\) path through connected \(C\) realizes the extra edge by a minor operation. The torso has universal vertex \(r\), so its remainder is outerplanar and its treewidth is at most three. Joining a local decomposition at its boundary clique bag to one outside bag gives a decomposition of \(G\). If \(w(K)>w(G)/2\), the outside bag cannot be a weighted centroid. A centroid local bag has at most four vertices and is covered by two ambient shortest paths between arbitrary paired vertices. This proof allows arbitrary positive edge lengths and changes both paths.

## Independent finite verification and trust boundary

The target's Python 3.11.2 `--check` run matched `expected.json`: 9,262 ambient geodesics across seven original fixtures and a triangulated control, 8,880 local deletion sets for \(m=2,\dots,16\), a 43-vertex optimum of 22, a 19-vertex supported optimum of five, and an unrestricted 43-vertex witness with largest component 17.

My separate [`audit.py`](audit.py) imports no target routines. It constructs the graph from the stated paths and annulus edges, independently computes BFS distances, enumerates all geodesics by endpoint-directed search, and computes full residual components. It also checks every admissible local deletion set of size at most two or inducing a three-vertex path for \(m=2,\dots,16\). Exact output:

```text
k=4 m=3 vertices=19 geodesics=286 prescribed_uniform=6 prescribed_supported=5 unrestricted_largest=9
k=4 m=10 vertices=40 geodesics=1021 prescribed_uniform=20 prescribed_supported=19 unrestricted_largest=16
k=4 m=11 vertices=43 geodesics=1162 prescribed_uniform=22 prescribed_supported=21 unrestricted_largest=17
k=5 m=13 vertices=51 geodesics=1649 prescribed_uniform=26 prescribed_supported=25 unrestricted_largest=21
local_deletion_sets=8880
```

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_prescribed_attachment/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_prescribed_attachment_review1/audit.py
```

Target `README.md` SHA-256: `caa8bf6f36078b638ce0a40b63553bbf38ade28c5a2d63c4fc8a480d81fea00f`; target `verify.py` SHA-256: `f209c4f1adeb6d93a35af90b9e503b96f241e15ff47fba67585941602b2aac1b`. The independent checker uses the same mathematical family but separately implements construction, path enumeration, and residual calculations. The finite checks verify the stated instances and local sets; the unbounded family and peripheral reduction rely on the written arguments. I did not formally verify planar gluing or the tree-decomposition centroid theorem. The target checker independently supplies a spherical rotation for each tested fixture.

## Literature and potential

The earlier [interval and facial sweep theorem](../planar_two_geodesic_interval_sweep/README.md) requires every positive-mass vertex to lie in the relevant metric interval union. The attached cone places positive-mass neighbors of \(r\) outside that union and pinpoints why the prescribed-path quantifier cannot simply survive this attachment. The classical [two-rooted-shortest-path planar cycle theorem](https://doi.org/10.1145/3686800) has a \(2/3\) balance bound and does not supply an exact \(1/2\) completion of a fixed path. A targeted primary-source search did not establish historical priority for this precise obstruction, so this review makes no priority claim. The finding is publishable as a method boundary and a usable peripheral reduction; it is not evidence against the unrestricted two-free-path conjecture.

## Strengthening and improvement opportunities

**Proved boundary refinement.** The peripheral reduction also handles \(w(K)=w(G)/2\). Delete its boundary \(\{r\}\cup Y\), of size at most three. Every remaining component inside \(K\) has mass at most \(w(K)=w(G)/2\); every component outside \(K\) has mass at most \(w(G)-w(K)=w(G)/2\). Two ambient geodesics between arbitrary paired boundary vertices cover that boundary, regardless of positive edge lengths. Thus the reduction may state \(w(K)\geq w(G)/2\). This equality case does not need the treewidth argument.

The most valuable remaining bridge is for the case in which every peripheral \(K\) is light but positive mass still lies outside the facial interval union. The present family proves that fixing the annular path \(P\) cannot work in general, while its free two-edge witness shows that changing the first path can. A useful next lemma would identify when a free path can absorb one facial attachment without losing ambient shortestness or causing the opposite annular side to exceed half. Any proposed claim should be tested against the \((4,11)\) uniform certificate and the \((4,3)\) supported-mass certificate.
