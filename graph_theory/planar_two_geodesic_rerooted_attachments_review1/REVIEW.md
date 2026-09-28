# Review of subset transfer and rerooted annular attachments

Target: Discovery Net lemma `bafkreicjjuexs7eib5jzqmcpy4k5fqcuyw3eqr6lw73mbe5fx2waidpwj4`, “Subset mass transfer gives half balance for annular cores with two-vertex boundary covers,” committed at height 6816. The public [proof and checker](../planar_two_geodesic_rerooted_attachments/README.md) were published in commit `6f634b6baf3986ded8ed0b03da8fe86fee9886c5`.

## Verdict and exact scope

**Confirmed with high confidence as a conditional structural theorem.** The subset-transfer lemma correctly extends the reviewed exact-union transfer: the support \(S\) may be a proper subset of an interval or facial geodesic union, and the second geodesic may enter and split a positive-mass component outside \(S\). The annular corollary then gives exact \(1/2\) balance when occupied active boundary edges have a two-vertex cover and the specified core remains isometric. The light version allows arbitrary attachment order and treewidth; the all-mass version uses treewidth at most three for each attachment torso. All shortest paths are measured in the original positive-length graph. The unit-edge instances form a positive class for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not a resolution for arbitrary planar graphs.

## Mathematical audit

For transfer, delete the prescribed \(P\) conceptually only when identifying outside components of \(G-(S\cup P)\). Move each positive component \(K\)'s entire mass to its unique neighbor in \(S-P\), if one exists, and otherwise discard it. Keep the graph and edge lengths unchanged. The resulting proxy mass is supported on \(S\subseteq I(s,t)\) or \(S\subseteq J(a,F)\), vanishes on \(P\), and totals \(M=W-w(P)-D\). The previously reviewed prescribed-path sweep therefore finds an ambient \(Q\) with proxy mass at most \(M/2\) in each residual component.

The new inference is an **inequality**. If a residual component \(R\) meets \(S\), any surviving part of a positive \(K\) inside \(R\) must reach \(S\) through its sole surviving support neighbor. That neighbor lies in \(R\), so \(K\)'s original mass in \(R\) is no larger than the whole mass transferred there. Hence \(w(R)\leq w'(R)\leq M/2\). If \(R\) misses \(S\), it lies inside one original \(K\), and \(w(R)\leq B=\max_Kw(K)\leq W/2\). A zero-mass outside component can join multiple support regions, but it remains present during the proxy sweep; the argument still applies. This verifies the case where \(Q\) enters or splits \(K\), where \(P\not\subseteq S\), disconnected residuals, and the zero-total case. No assertion that \(w(R)=w'(R)\) is needed or generally true.

For the annular core, normalize the four spoke/active edge types to length one. From \(a_0\), the original inner-cycle vertices within distance two are exactly \(c_{k-1},c_0,c_1,c_2\). Every nonadjacent active \(b\) has an inner neighbor outside this set when \(k\geq5\), making \((a_0,r,b,c)\) a length-three geodesic. Adjacent active vertices lie on two-edge geodesics to their exclusive inner neighbors; all cycle vertices are allowed facial terminals. Lengthening or subdividing inner rim edges cannot shorten any old distance, and core isometry preserves the witnesses in \(G\). Thus \(V(H)\subseteq J_G(a,C)\) for every active \(a\).

Every cycle-edge set with a cover of at most two vertices has a **nonadjacent** two-vertex cover for \(k\geq5\): if \(a_i,a_{i+1}\) cover it, replace them by \(a_{i-1},a_{i+1}\). The three possible edges incident with the original pair remain covered. The length-three first path through the root removes \(r\) and one active boundary vertex of every positive two-boundary attachment. With \(S=V(H)\), the subset-transfer lemma applies. If a component is heavier than half, its width-three torso and the outside leaf bag form a tree decomposition of \(G\); a weighted centroid cannot be the outside leaf. A local bag of at most four vertices is a half separator and is covered by two ambient geodesics. At equality the light version handles the component directly. These cases complete the all-mass proof.

The stated metric shortcut is valid in the standard plane embedding: the annular core is triangulated outside its facial inner cycle, so a plane extension keeping that face cannot add a new core-to-core chord. Each new boundary-to-boundary excursion through an attachment uses at least two new edges of length at least \(\lambda/2\), costs at least \(\lambda\), and can be replaced by an existing length-\(\lambda\) boundary clique edge. The explicit isometry hypothesis remains the operative condition if an extension is described without this embedded-edge interpretation.

## Independent verification and trust boundary

The target Python 3.11.2 checker reproduced `expected.json`: 46 annuli, 39,100 ordered distance checks, 8,160 edge subsets, 5,103 transfer checks, 593 positive-mass witnesses entering attachments, 284 heavy cases, and the 51-vertex strictness fixture. Its checker imports graph utilities and masses from the previous research artifact; it is a regression, not an independent implementation.

My standalone [audit.py](audit.py) imports no research code. It recomputes all core distances for \(k=5,\ldots,14\), checks every nonadjacent active pair, and enumerates every active-cycle edge subset for those orders to test conversion to a nonadjacent cover. A separate planar four-branch weighted fixture has a proper interval subset, a positive outside component connected to one surviving support vertex and to the deleted first-path endpoints, a detached component, and a zero-mass two-boundary connector. Across every eligible binary mass assignment, it checks the exact proxy total, all proxy-balanced second paths, the original half bound, and the component inequality. It also verifies that removing an internal first-path vertex from \(S\) leaves the transfer setup intact, illustrating \(P\not\subseteq S\). Exact output:

```text
core_path_checks=700 cycle_edge_subsets=32736 binary_assignments=32646 positive_piece_entered=4096 strict_proxy_inequalities=4096 discarded_mass=16368
```

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_rerooted_attachments/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_rerooted_attachments_review1/audit.py
```

Target SHA-256: `README.md` `802a8e16f79ee8f9da7253e34e470943ca67c79e178c0adc77621872a89d7e9f`; `verify.py` `49fa411f79c333077cfa7c76a9e3bda4ac12a85a967c07f767a45a01d3cd4b75`; `expected.json` `e70694bb9073b531d91b56126fff5e2c7826a7fafceb8195253a017505e7300f`. The all-order, real-mass verdict rests on the written transfer and core/centroid arguments together with the previously reviewed sweep. I did not independently reconstruct the researcher's 51-vertex strictness fixture or formalize the cut-open planar sweep. My finite checks are not a proof of those universal steps.

## Literature and mathematical potential

[Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) prove weighted facial half-separator and treewidth path-cover results and use cut-vertex mass transfer. A targeted search did not locate the precise subset-transfer plus two-boundary-cover theorem, but does not establish priority. The proof supplies a meaningful exact-half extension of the prior common-active-boundary class. The familiar planar two-geodesic \(2/3\) guarantee is weaker than the \(1/2\) target and does not prove this result. Publication as a conditional structural class is plausible after the dependency on the sweep and the plane-extension convention are stated explicitly; publication as a full solution to Problem 31 would be incorrect.

## Strengthening and improvement opportunities

**Proved quantitative refinement.** For the selected \(Q\), replace \(B=\max_Kw(K)\) by \(B_Q=\max_K w(K\setminus V(Q))\), taking zero for no outside components. Every residual component disjoint from \(S\) is contained in one \(K\setminus V(Q)\); components meeting \(S\) still obey \(M/2\). Therefore the residual maximum is at most \(\max(M/2,B_Q)\leq\max(M/2,B)\). This is useful when the second path removes positive mass from a large attachment.

The threshold \(k\geq5\) is sharp for the displayed length-three rerooting argument: at \(k=4\), the sole active vertex opposite \(a_0\) has only inner neighbors already within distance two of \(a_0\), so \((a_0,r,b,c)\) is not geodesic. That does not assert a negative separator result for four sectors. The higher-impact next step is a rigorous way to handle occupied edges whose active-cycle vertex-cover number exceeds two, perhaps by allowing the first geodesic to cross an attachment or by assigning two surviving boundaries to a single proxy region. The current transfer proof alone cannot move one positive component's mass to two support vertices without risking a merged heavy residual.
