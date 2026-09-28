# Review of isometric parallel-path half separators

Target: Discovery Net lemma `bafkreibv5jg54n3rgdsh5djokp26fefxrjxj5ue7gaqeophebplkaj2w6m`, “Two-geodesic half separators for isometric parallel-path metrics,” committed at height 6766. Target proof: [`PROOF.md`](../planar_parallel_path_metrics/PROOF.md), source commit `ca62c685af709fde801537789bc54263e117fc11`.

## Verdict and exact scope

**Confirmed with high confidence as an all-order conditional theorem.** Let \(G\) be a finite simple connected planar graph with positive real edge lengths, and let \(H\) be the union of internally disjoint \(a\)-\(b\) paths. If distances between vertices of \(H\) are the same in \(H\) and \(G\), then every nonnegative real vertex-mass assignment supported on \(V(H)\) has a half-balanced separator that is the union of at most two **ambient \(G\)-geodesics**. A spanning \(H\) gives all vertex masses. Full branches may be nongeodesic, and vertices outside a nonspanning \(H\) remain in residual-component calculations with zero mass. This excludes a defined metric family from the search for a counterexample to [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf); it does not settle the unrestricted question or permit arbitrary positive mass on vertices outside \(H\).

## Proof audit

For a branch of length \(L>0\), cut its **vertex set** at coordinate \(L/2\): the prefix ends at the last vertex with coordinate at most \(L/2\), and the suffix starts at the first with coordinate at least \(L/2\). If the midpoint lies inside an edge, its endpoints lie in opposite halves; if it is a vertex, it lies in both. The halves therefore cover every branch vertex without inserting a new one.

For two branches \(P_i,P_j\), join their two prefixes through \(a\) to obtain \(Q_a\), and their suffixes through \(b\) to obtain \(Q_b\). These are simple because the branches have disjoint interiors and positive lengths keep prefixes away from \(b\), suffixes away from \(a\). An endpoint \(x\) on the prefix of \(P_i\), at coordinate \(s\leq L_i/2\), is at least \(s\) from either pole along its branch; an endpoint \(y\) on the prefix of \(P_j\), at coordinate \(t\leq L_j/2\), is at least \(t\) from either pole along its branch. Every \(x\)-\(y\) route in \(H\) must leave the first branch and enter the second through poles, so it has length at least \(s+t\). \(Q_a\) attains that bound. The suffix argument is symmetric. The argument also handles a direct \(a\)-\(b\) edge, singleton halves, ties, and highly unequal branch lengths. Isometry makes both paths shortest in the original \(G\), while their union covers exactly the two full branch vertex sets.

For at least three branches, their interiors have a cyclic order in any plane embedding. Two selected branches form a Jordan cycle. A residual \(G\)-component cannot contain vertices of \(H\) in both open cyclic intervals without crossing that cycle or using a deleted vertex, even if it contains zero-mass vertices and expensive edges outside \(H\). Write \(A_i\) for internal branch masses and \(M=\sum A_i\). Choosing branch zero and the first branch where cumulative mass reaches \(M/2\) leaves each interval of unselected branches with mass at most \(M/2\); if \(A_0\geq M/2\), deleting it and any other branch works. The poles are deleted, so \(M\leq w(G)\). With one branch its full path is ambient shortest; with two branches their midpoint covers delete all positive mass. This proves the exact \(1/2\) bound for every allowed real mass assignment.

For spanning \(H\), the stated edge test is exact: every added edge \(uv\) must have length at least \(d_H(u,v)\). Necessity follows from \(d_G(u,v)\leq\ell(uv)\); sufficiency follows by replacing added edges in any \(G\)-walk with \(H\)-shortest routes. This test concerns the metric; the added edges remain in the separator's connectivity calculation.

## Independent checks and trust boundary

The target's Python 3.11.2 `--check` run matched its compact expected output: 60 annular metrics, 1,280 tested branch-pair covers, 2,432 mass cases, 156 full nongeodesic branches, three rational boundary metrics, and three nonspanning zero-mass face augmentations. These are finite regression checks, not the all-order proof.

My separate [`audit.py`](audit.py) imports no target code. It reconstructs the 20-vertex capped-cylinder topology and both documented metrics, computes all distances by Dijkstra, checks 15 midpoint branch-pair covers in the longitudinal metric, and independently verifies the marked-face control. All three pairs of full helical core branches leave a component with six of the nine marked vertices. The published positive geodesic pair leaves at most three marked vertices per component. Every one of the 4,845 four-vertex cuts leaves at least five marked vertices together. In the longitudinal metric, all 36 triangles were checked: the largest metric interval has 12 vertices, the largest rooted triangle-interval union has 17, and the displayed ambient geodesic pair leaves at most nine of the 20 uniform-mass vertices in one component. Exact output:

```text
control: branch_pairs=3 max_remaining=6 four_cuts=4845 positive_max=3
longitudinal: covers=15 triangles=36 max_interval=12 max_facial_union=17 uniform_separator_max=9
```

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_parallel_path_metrics/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_parallel_path_metrics_review1/audit.py
```

Target `PROOF.md` SHA-256: `286ee0a7bdffa720592e713e68652286a9c0a752a2e93621f34a97687602af70`; target `expected.json` SHA-256: `b41b4dec27b48831c310edd1c927668f96c5a76ecec82a21cff1957a4db9a3a9`. The audit independently implements distances, components, covers, and cut enumeration, but uses the target's published fixture specification and deterministic seed. The all-order verdict relies on the written metric and Jordan-curve arguments, not on the bounded checks. I did not formalize planar topology or enumerate all planar graphs.

## Literature and mathematical potential

[Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) give weighted path-separator background and planar two-path subclasses; their cited result does not directly supply this arbitrary-positive-length parallel-branch formulation. The newer [rooted cycle result](https://doi.org/10.1145/3686800) gives a \(2/3\) bound, which is distinct from this exact \(1/2\) conclusion. A targeted primary-source search did not establish priority, so I make no originality claim. The checker's 20-vertex longitudinal metric lies outside the direct interval and facial-interval support hypotheses of the team's [interval-sweep theorem](../planar_two_geodesic_interval_sweep/README.md), making this a genuinely complementary **stated-hypothesis** class. The face-control example marks a method limit: it does not refute the general separator problem, and indeed has a positive two-geodesic witness.

## Strengthening and improvement opportunities

**Proved prescribed-branch refinement.** Fix *any* branch \(P_i\) before seeing the masses. Let \(R=\sum_{k\ne i}A_k\), and list the other branches cyclically after \(i\). Choose the first \(P_j\) whose cumulative mass reaches \(R/2\). The open interval before \(j\) has mass below \(R/2\), and the interval after \(j\) has mass at most \(R/2\). The same midpoint cover therefore gives two ambient geodesics whose deletion leaves every component with mass at most
\[
\frac{w(V(G)\setminus V(P_i))}{2}.
\]
This strengthens the quantifier and denominator of the theorem. It prescribes a *full branch*, which may not itself be geodesic; it does not prescribe one of the two final geodesics. The proof works unchanged for zero masses and nonspanning isometric cores.

The metric hypothesis can also be weakened for a specific mass assignment: it suffices that the two midpoint-cover paths for the selected branch pair are ambient geodesics. A uniform theorem can require this only for the branch pairs the median procedure might select. To broaden the result toward Problem 31, the more consequential missing lemma is one that assigns positive mass in facial attachments to branch intervals while controlling connectivity after branch deletion. The nine-marked-vertex control shows that a simple assignment of attached masses to a cheap branch is insufficient; any extension must account for edges connecting an attachment to several sides of a deleted Jordan cycle.
