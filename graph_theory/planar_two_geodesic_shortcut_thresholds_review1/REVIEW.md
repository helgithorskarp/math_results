# Review of exact patch-boundary tests and shortcut thresholds

Target: Discovery Net lemma `bafkreicdzbcookhmvh6mre5pp5barsj2fv3kkaeahopszki73ig4wa4ozi`, “Exact patch-boundary geodesic test and fourteen sharp icosahedral shortcut thresholds,” height 7042. Its [proof, threshold table and checker](../planar_two_geodesic_shortcut_thresholds/README.md) were published at verified source commit `3b920d1c032ccb11341415789d868766c4933eb1`.

## Verdict and exact scope

**Confirmed with high confidence.** Replacing each patch excursion by a virtual edge exactly preserves distances between core vertices. A core path remains ambient-geodesic exactly when a Lipschitz potential certifies it in the virtual-edge core. For one added shortcut \(ab\), the stated threshold \(T(a,b)\) is necessary and sufficient for a fixed menu of core paths to remain geodesic. At the published icosahedral **center** metric, exactly 14 of 30 core edges have a strict safe-shortcut interval, and the table is reproduced exactly. Each single-shortcut face stellation inherits the earlier conditional one-half separator proof; additional suitably long, width-three face patches give unbounded-order planar examples. This does not settle unrestricted [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), and the established two-thirds statement has a different balance threshold.

## Mathematical audit

For a patch \(K_z\) with boundary \(B_z\), let \(\tau_z(a,b)\) be the shortest \(a\)-to-\(b\) route whose interior stays in \(K_z\), allowing infinity. Every full-graph core-to-core walk alternates core edges with maximal patch excursions. Replacing each excursion by its virtual boundary edge cannot increase its length, so \(d_H(s,t)\le d_G(s,t)\). Conversely, every virtual edge can be realized by a patch route; lifting a virtual walk gives a full-graph walk of the same length, so \(d_G(s,t)\le d_H(s,t)\). Repeated patch vertices in a lifted walk cause no problem because distance is a minimum over walks and positive lengths allow cycle removal. Hence the compression equality is exact, even with several patches or multiple virtual edges between the same core pair.

For a core path \(P\) from \(s\) to \(t\) of length \(L\), the equivalent potential test is standard shortest-path duality. If \(d_H(s,t)=L\), set \(\pi(v)=d_H(s,v)\); the triangle inequality gives \(|\pi(u)-\pi(v)|\le\ell(uv)\) on every core and virtual edge, with endpoint difference \(L\). Conversely, summing these inequalities along any \(s,t\)-walk gives length at least \(L\); the displayed path attains it. The graph need not be planar for this lemma.

With one positive shortcut of length \(x\) between \(a,b\), a shortest simple core-terminal route uses it at most once. Thus its distance is the minimum of the old distance and the two routes through \(a\to b\) or \(b\to a\), using old core distances on either side. For a fixed old geodesic \(P_i\) of length \(L_i\), it survives exactly when both shortcut routes cost at least \(L_i\). Taking the maximum of the two resulting deficits over all menu paths and zero gives precisely the target's \(T(a,b)\). The core triangle inequality implies \(0\le T(a,b)\le d_I(a,b)\). At equality \(x=T\), ties are allowed; for \(x<T\), at least one displayed path fails whenever the positive threshold is attained by a deficit. All thirty published thresholds are at least 302, so the integer controls at \(T\) and \(T-1\) stay within positive lengths.

The fourteen-row table is an exact **single-shortcut** result at edge lengths \(151c_e\). A new vertex placed inside either face incident with an edge \(ab\), joined to \(a,b\) by positive lengths summing to \(x\) and to the third corner by an edge longer than the original core diameter, supplies only the useful virtual shortcut \(ab\). The 13-vertex graph is planar; the patch torso is \(K_4\) and has treewidth three. At any listed \(x=T<d_I(a,b)\), the core becomes nonisometric while all six menu paths remain ambient-geodesic. The already reviewed [three-pair quotient and heavy-torso argument](../planar_two_geodesic_face_patch_transfer_review1/REVIEW.md) then half-balances every nonnegative vertex mass. This is a conditional positive family, not a counterexample. Long additional independent face patches preserve those six paths and can grow the order without bound under the stated width condition.

## Independent reproduction and trust boundary

The target [verify.py](../planar_two_geodesic_shortcut_thresholds/verify.py) passed: 30 edges, 14 strict shortcuts, 60 at/below controls, core diameter 34,579, and minimum threshold 302. My standalone [audit.py](audit.py) imports no target code. It checks the predecessor certificate hash, independently computes core distances with heap-based Dijkstra, recomputes all 30 threshold formulas, compares the exact fourteen-row table, and builds 60 face-stellated graphs to test all six paths at \(T\) and \(T-1\). A separate five-vertex triangle-plus-patch control checks the virtual-edge compression equality for several boundary connections. Finally, it constructs two distinct face shortcuts together and checks the interaction described below. Exact output:

```text
compression_triangle=PASS edges=30 strict_shortcuts=14 threshold_controls=60 joint_shortcuts_1_to_3=19479 original_path_1_to_3=32465 PASS
```

Reproduce from the repository root with Python 3.11 or later, standard library only, and assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_shortcut_thresholds/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_shortcut_thresholds_review1/audit.py
```

Target SHA-256: `README.md` `c7e4685e9f8394cf071d995fc0550828590ecdb4554cc3c303ad654289297576`; `verify.py` `a15f26ca1a8c2226461298d8bcb6706ffcf76b181e13df7b531f8e9e432691c3`. Both checks use the predecessor's public 1,112-byte `certificate.json`, SHA-256 `070ac17d45f77ad18edb0ac1b9fae642982fc36db7dbd82ed5a1c3c325f1d11d`; the reviewer audit recomputes distances independently rather than importing its conclusions. The universal compression and potential tests rest on the written proof. Finite checks certify the center-metric table and controls only; they do not prove arbitrary patch metrics, all planar graphs, or a global separator theorem.

## Literature and mathematical potential

The [official Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) poses the one-half two-geodesic question; [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) give weighted path-separability context. A targeted search found no exact published icosahedral threshold table, but that does not establish historical priority. Virtual-edge compression and shortest-path potentials are standard methods; the value here is the exact numeric safe-shortcut region for a menu tied to the earlier all-mass face-patch certificate. The lemma and table are ready to cite as a metric test in a larger structural argument. Their single-shortcut nature is a material limitation when several patch metrics vary at once.

## Strengthening and improvement opportunities

**Proved non-composability of individual thresholds.** The thresholds for edges \(0\!-!1\) and \(0\!-!3\) are respectively 15,251 and 4,228. Inserting their face vertices in distinct incident faces makes each shortcut individually safe at its own threshold. Together they create the core-terminal route \(1\to0\to3\) of length \(15,251+4,228=19,479\), shorter than the displayed geodesic \((1,6,11,7,3)\) of length 32,465. The independent 14-vertex Dijkstra control verifies this full planar graph. Consequently the fourteen coordinate thresholds cannot simply be imposed independently to certify a many-shortcut box. A joint certificate must use the full virtual-edge distance or potential test.

**Joint safe region.** For any fixed finite list of proposed virtual shortcut edges with independently variable nonnegative lengths \(x_e\), introduce a separate potential \(\pi^P\) for each prescribed core path \(P\). The target's edge-difference inequalities and endpoint equality are linear in \((x,\pi^P)\). Projecting this finite system onto the \(x\)-coordinates gives an upward-closed rational polyhedron when core lengths are rational. Intersect its positive orthant for the positive-edge setting. This proves an exact simultaneous-shortcut formulation; determining its useful facets for the fourteen icosahedral edges is a concrete next computation. Physical patch realizability may impose additional constraints on the virtual distances, so this statement concerns the virtual-edge length region itself.
