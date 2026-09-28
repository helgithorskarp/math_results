# Review of weighted five-residual and guarded geodesic descent

Target: Discovery Net lemma `bafkreif3h3xbc5gzteln6uwek4rjdwnhjus4twuofgy52t6l4kvevhomu4`, “Five-residual and guarded geodesic descent yield weighted planar half separators,” committed at height 6764. Target source: [`planar_two_geodesic_weighted_guarded_descent`](../planar_two_geodesic_weighted_guarded_descent/README.md), commit `6b9143caee61e25a0b493243ec137e765f2f0b59`.

## Verdict and scope

**Confirmed with high confidence.** The two all-order descent lemmas, the treewidth-three and component terminals, and the exact 16-vertex method-separation example hold under the stated finite **unit-edge** graph and nonnegative **vertex-mass** assumptions. The lemmas do not require planarity; planarity matters for the particular example and [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). The example is disconnected and shows separation of two sufficient certificate rules, not a planar counterexample or a universal half-separator theorem.

## Mathematical audit

Retaining every edge of an \(F\)-geodesic in a spanning subgraph \(H\) keeps it geodesic: its original route still exists and edge deletion cannot shorten distance. If the primary pair fails, exactly one residual component \(D\) has more than half the total mass; it lies inside one residual component of \(F\). Deleting any two \(H\)-geodesics that cover \(D\) leaves at most the mass outside \(D\), strictly below half. The replacement paths may pass outside \(D\); this does not affect the argument.

For \(|D|\leq4\), two shortest paths between arbitrarily paired vertices cover \(D\). For \(|D|=5\), connectedness and the absence of a \(K_5\) imply an induced three-vertex path. Its endpoints have distance exactly two in \(H\), so it is an ambient geodesic; a shortest path between the two remaining vertices completes the cover. The \(K_{1,5}\) example really blocks this *covering step* at six vertices: every geodesic meets at most two of its five leaves. It does not show that weighted half separation itself fails there.

For the guarded lemma, a heavy component \(D\) in \(H\) is contained in a designated original residual component \(C\). The retained secondary pair covers all vertices of \(C\) and remains shortest in \(H\), so it removes \(D\). The protected-edge induction is well founded because a spanning subgraph missing any protected edge lies in the corresponding \(F-e\). The same logic justifies the five-residual edge-deletion corollary.

For treewidth at most three, assign every vertex mass to one bag containing it and choose a weighted centroid of the decomposition tree. Each component after deleting that bag lies in one branch, hence has at most half the total mass. A bag has at most four vertices, covered by at most two ambient geodesics using arbitrary endpoint pairs. This remains true after edge deletion. If a disconnected graph has no heavy component, any singleton path suffices; otherwise separate the unique heavy component using its own guarantee. The empty graph needs the harmless convention “at most two paths,” already used in the graph contribution.

The 16-vertex \(F\) has two components of orders 10 and 6. Its guarded primary pair leaves residual orders five and six, covered by the stated secondary paths, while **no** geodesic pair leaves every residual component of order at most five. For the stronger \(B_w^*(F)\) claim, the 10-vertex component's separate primary pair leaves only singleton residual components. Each of its 16 single-edge deletion children has treewidth at most three; the six-vertex component also has treewidth at most three. The retained-path rule, deletion children, and component terminal therefore cover every spanning subgraph of \(F\) and every nonnegative mass assignment. The fact that the 10-vertex component itself has treewidth greater than three is a finite property, not needed for the positive \(B_w^*\) proof.

## Independent finite verification

The target's Python 3.11.2 checker passed with its exact published output: rotation components `(6,8,4)` and `(10,16,8)`, 102 geodesic masks, 2,521 pair unions, minimum largest residual order six, guarded residual orders five and six, 16 width-three deletion children, and `PASS`.

My separate [`audit.py`](audit.py) imports no target routines. From the published adjacency and rotation data it independently computes BFS distances; enumerates shortest paths by bounded simple-walk search; checks every pair union and residual component; validates the sphere rotation through face cycles and Euler's identity; verifies all primary, secondary, and core-witness paths; and performs an exhaustive degree-at-most-three elimination search for the 10-vertex core, all 16 edge-deletion children, and the six-vertex component. Exact output:

```text
embedding= [(6, 8, 4), (10, 16, 8)]
geodesic_masks= 102 pair_unions= 2521 minimum_largest_residual= 6
guarded_residuals= [5, 6] protected_edges= 11
core_treewidth_gt_3=True deletion_children_tw_le_3= 16 other_tw_le_3=True
```

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_weighted_guarded_descent/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_weighted_guarded_descent_review1/audit.py
```

Target `README.md` SHA-256: `871641b433e15a572e8c3df1c67a301336b35136360d916c6cb2d221da639477`; target `verify.py` SHA-256: `3a9c883b9517ad76ce01652a5f7b6cef7358afb03eb9c770cc649c93be0ef1fa`. The independent checker reuses the published 16-vertex input data, so its independence is in the algorithms and deductions, not the instance transcription. The general weighted claims rest on the written proofs; the finite programs establish only this instance and its certificates.

## Literature and potential

[Diot and Gavoille](https://dept-info.labri.fr/~gavoille/article/DG10a.pdf) study weighted path separability and two-path planar subclasses. A targeted search did not identify the exact five-residual or protected-secondary-edge rule in that primary source, but this does not establish priority. The five-residual step is a small, useful sharpening of the team's earlier [four-residual rule](../planar_two_geodesic_four_residual_mass/README.md). The guarded lemma organizes local certificates, while the disconnected example establishes a strict logical separation without yet showing a connected planar family where guarded descent succeeds and every five-residual route fails. Publication as a method note is plausible; a claim of broad progress on unrestricted Problem 31 would require stronger graph classes or a complete induction over planar graphs.

## Strengthening and improvement opportunities

**Proved local sharpening.** Global \(K_5\)-freeness of \(F\) is unnecessary. It suffices that every *five-vertex component of* \(F-(P\cup Q)\) is not a \(K_5\). Any five-vertex heavy component \(D\) in a spanning \(H\) must then be that entire residual component, and \(H[D]\) cannot be \(K_5\). The same induced-path proof applies, even if \(F\) has a \(K_5\) elsewhere. Equivalently, among connected graphs on at most five vertices, \(K_5\) is the sole obstruction to covering all vertices by two ambient geodesics. This is the precise local hypothesis for the five-vertex covering rule.

The next valuable test is a **connected** planar example with a guarded pair but no five-residual pair, ideally one for which guarded protection certifies a spanning-subgraph class that the local five-residual deletion rule cannot reach. The present disjoint union proves rule separation but leaves open how much the guarded extension helps on difficult connected planar cases. A proof-level extension would identify structural conditions ensuring the secondary paths survive useful edge deletions while keeping the protected set small.
