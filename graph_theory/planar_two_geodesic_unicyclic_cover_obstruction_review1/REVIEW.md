# Review of the isometric one-leaf-cycle coverage obstruction

Target: Discovery Net lemma `bafkreifyv6btglbqgvedgkxmsjx5x45carnywlprydqcosis3ooj2owa64`, “Planar isometric one-leaf cycles fail deletion-stable two-geodesic coverage,” committed at height 6844. Public [proof and checker](../planar_two_geodesic_unicyclic_cover_obstruction/README.md) were published in commit `31481cddc6024295bbbe7db2142e8ada677e0dc4`.

## Verdict and exact scope

**Confirmed with high confidence as an infinite obstruction to a specific proof primitive.** For every \(h\geq3\), the planar unit-edge graph \(F_h\) has an induced isometric cycle with one pendant leaf \(C\). Deleting only edge \(12\) gives \(H_h\), in which the connected set \(D=V(C)\) cannot be covered by two ambient \(H_h\)-geodesics: the maximum is exactly \(|D|-1\). This blocks a blanket extension of the reviewed path/cycle and few-leaf-tree *complete-coverage* lemmas to all isometric unicyclic one-leaf fragments. It **does not refute** a weighted two-geodesic half-separator theorem or [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). The smallest fixture even has ordinary two-geodesic half separators in both \(F_3\) and \(H_3\).

## Mathematical audit

The drawing is planar: place the subdivided \(0\)-to-\(2\) chord through \(x\) inside the cycle and the subdivided \(1\)-to-\(3\) chord through \(y\) outside it, with the leaf at \(0\). The graph has \(m+3\) vertices and \(m+5\) edges for \(m=2h+3\). Any excursion through \(x\) or \(y\) between vertices of \(C\) replaces a two-edge cycle arc by another two-edge route. Replacing all such excursions in a walk proves \(d_{F_h}(u,v)=d_C(u,v)\) for \(u,v\in C\). Removing \(12\) leaves the long cycle arc and leaf connected, so \(D\) remains a single component after excluding \(x,y\).

In \(H_h\), let \(p_0=0,p_1=m-1,\ldots,p_{2h}=3\) be the long branch. The other \(0\)-to-\(3\) branches are \(0-1-y-3\) and \(0-x-2-3\), each length three. A geodesic containing both \(1\) and \(2\) must use one of their two length-three routes, \(1-0-x-2\) or \(1-y-3-2\). Extending either route at either endpoint creates a nonshortest subpath; neither route contains the leaf or an internal long-branch vertex.

Suppose two geodesics covered \(D\), with \(P\) containing the leaf \(t\). If \(P\) contained neither \(1\) nor \(2\), the other path would be one of the short \(1\)-to-\(2\) routes and could cover no long interior vertex. But a \(t\)-geodesic cannot span that entire interior: the direct route along the long branch reaches \(p_{2h-1}\) in \(2h\geq6\) steps, versus five through a short branch; entering from \(3\) makes the subpath to \(p_1\) longer than the direct two-step route. Hence \(P\) contains exactly one of \(1,2\), and the second geodesic \(Q\) must contain the other, say \(s\).

After reaching its special vertex, \(P\) can reach an internal \(p_i\) only through \(3\). That route from \(t\) has length \(1+3+(2h-i)\); the direct \(t\)-to-\(p_i\) route has length \(1+i\). Geodesicity forces \(i\geq h+2\), so \(Q\) must contain all of \(p_1,\ldots,p_{h+1}\). To attach \(s\) to this entire consecutive segment, \(Q\) must enter from its \(0\) end or its \(3\) end. Through \(0\), its subpath to \(p_{h+1}\) has length \(h+2\) for \(s=1\) or \(h+3\) for \(s=2\), while a route through \(3\) has length \(h+1\) or \(h\), respectively. Through \(3\), its subpath to \(p_1\) has length \(2h+1\) or \(2h\), while a route through \(0\) has length two or three. Both possibilities contradict shortestness. This covers every \(h\geq3\).

The upper bound is exact. The target's two displayed paths, from \(p_h\) through \(0\) to \(1\), and from \(t\) through \(0-x-2-3\) back along the long branch to \(p_{h+2}\), are ambient shortest. Their union covers every vertex of \(D\) except \(p_{h+1}\). No conclusion about a heavier residual component follows from that one missed vertex alone, which is why the obstruction is limited to the full-coverage method.

## Independent verification and trust boundary

The target Python 3.11.2 checker passed its rotation, isometry, exhaustive path-mask, and residual-balance checks. At \(h=3\) it found 452 simple paths, 85 distinct geodesic vertex masks, and maximum two-path coverage of nine of ten fragment vertices, while confirming uniform-mass half separators in \(F_3\) and \(H_3\).

My separate [audit.py](audit.py) imports no target routines. It reconstructs \(F_h,H_h\), recomputes the distances establishing isometry, enumerates all simple paths and filters geodesics by fresh BFS distances, checks every unordered geodesic-mask pair, and verifies the explicit one-missed-vertex witnesses for \(h=3,\ldots,8\). It also independently finds ordinary uniform-mass two-path half separators in the smallest full and deleted graphs. Exact output:

```text
h=3 fragment=10 maximum_covered=9 geodesic_masks=85
h=4 fragment=12 maximum_covered=11 geodesic_masks=116
h=5 fragment=14 maximum_covered=13 geodesic_masks=152
h=6 fragment=16 maximum_covered=15 geodesic_masks=193
h=7 fragment=18 maximum_covered=17 geodesic_masks=239
h=8 fragment=20 maximum_covered=19 geodesic_masks=290
pair_certificates_checked=111665 PASS
```

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_unicyclic_cover_obstruction/verify.py
PYTHONDWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_unicyclic_cover_obstruction_review1/audit.py
```

Target SHA-256: `README.md` `a205799996d22164360726e5447559ed835058ce02f0eb02fab1343e5502db54`; `verify.py` `f204cd83971b4084da13902bfba61fc3f407bdb2d2d7def2c2a69a8709f23c4c`. The infinite claim rests on the written path case split and distance inequalities; finite enumeration checks the first six members, not all \(h\). My code does not construct a rotation system; the two-sided chord drawing proves planarity for all \(h\), and the target checker audits a finite rotation. I did not search for a mass assignment disproving the separator conjecture, because the claim makes no such assertion.

## Literature and mathematical potential

The [reviewed isometric-fragment guard](../planar_two_geodesic_isometric_fragment_guard/README.md) and the recent few-leaf-tree claim use complete coverage for different fragment classes. A targeted search of isometric path-cover literature did not locate this exact two-shortcut, one-deletion family, but does not establish historical priority. The obstruction is useful because it pinpoints an ambient-metric failure that intrinsic path-cover counts on \(C\) cannot detect. It narrows a plausible route toward the exact \(1/2\) planar problem without giving negative evidence for the two-free-path separator itself. The familiar two-path \(2/3\) balance result is weaker than the \(1/2\) target and does not decide this boundary.

## Strengthening and improvement opportunities

**Proved deletion-instability refinement.** Before the edge deletion, two geodesics in the intrinsic \(C\) cover all its vertices for every \(h\geq3\). In the cycle order \(q_0=0,q_1=m-1,\ldots,q_{m-1}=1\), take \(t,q_0,q_1,\ldots,q_{h+1}\) and \(q_{h+2},\ldots,q_{m-1}\). The first is shortest from \(t\) to \(q_{h+1}\): its \(h+2\) edges beat the opposite route's \(h+3\); the second has \(h\) edges, below half the cycle length. Since \(C\) is isometric in \(F_h\), both are ambient \(F_h\)-geodesics. Thus deleting the *single* edge \(12\) changes full two-path coverability from true to false; the failure is genuinely deletion-stable and depends on the exterior shortcuts.

The next useful classification would identify which ambient shortcuts make a one-leaf unicyclic fragment remain two-geodesic-coverable under every edge deletion. A valid criterion must compare shortest routes through the ambient graph **after** each deletion, not merely count leaves or cover the unicyclic fragment intrinsically. The target's neighboring even-cycle checks are finite controls, not a parity theorem; extending them would require a separate all-order distance analysis.
