# Review of exact-half separators for subdivided annuli

Target: Discovery Net lemma `bafkreic4n4udd3u47uyadox5z23tdm22xaugjyjmh2eae3hih2tp2ffki4`, “Exact-half annular gluing with arbitrary unit rim subdivisions,” committed at height 6856. The [proof and checker](../planar_two_geodesic_subdivided_annuli/README.md) were published at commit `ad5173ca0434df7184def02865a095ed09affb4e`.

## Verdict and exact scope

**Confirmed with high confidence at the stated scope.** In the specified isometric annular core, each inner arc has length at least \(\lambda\), and an arc with internal vertices has length at least \(2\lambda\). Attachments meet only a root vertex, root-active edge, or root-active triangle. If each individual outside component is light, two ambient geodesics half-separate every nonnegative vertex-mass assignment. If each attachment torso has treewidth at most three, the same holds without the lightness assumption. This covers arbitrary unit-edge inner-rim subdivisions and arbitrary positive mass on their vertices; it is a sufficient class for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not a resolution for all planar graphs. A prescribed core spoke is completable when every outside component and every specified two-arc rim patch is light; a heavy patch may require changing both paths.

## Mathematical audit

The three-terminal path-cover lemma is sound. For opposite-ear vertices at coordinates \(x,y\), degree two at the other internal vertices forces any route to leave and enter through \(u,m,v\). The four route types have lengths \(x+s+y\), \(x+p+B-y\), \(A-x+q+y\), and \(A-x+B-y\), with \(p=d(u,m),q=d(m,v),s=d(u,v)\). The proposed cuts \(z=(2A-p+q-s)/4\) and \(t=(2B+p-q-s)/4\) lie on their ears by triangle inequalities. At predecessors of these cuts, \(2x\leq A+q-s\), \(2y\leq B+p-s\), and \(2(x+y)\leq A+B-s\), so the outer walk attains the first route length. At successors, the reversed inequalities make the inner walk attain the fourth. Positive edge lengths then rule out repeated vertices. Rounding between adjacent vertices leaves no gap in their union. This proves complete coverage of any two consecutive inner arcs by two ambient geodesics; a patch heavier than \(W/2\) is therefore removed entirely, leaving less than \(W/2\) total mass outside the pair.

For the light-patch sweep, the classes \(\alpha_i,\gamma_i,\tau_i,\kappa_i\) form an exact partition of the represented mass \(M=W-w(P)-D\), where \(P\) is the prescribed spoke and \(D\) is already detached mass. A two-active-portal sector may have aggregate mass greater than \(W/2\); only each *individual* detached component must be light. The spoke bounds are \(U_i:(L_i,R_i)\) and \(V_i:(L_i+\gamma_i+\tau_i,R_i-\gamma_{i+1}-\tau_i)\). At cyclic seams, an actual surviving component stays inside one formal side, so these bounds cannot underestimate it. Every candidate is measured in the original graph.

If no spoke balances, one bound is strictly heavy at each state because the two bounds sum to at most \(M\leq W\). The ordered states begin right-heavy and end left-heavy. At a transition \(U_i\) to \(V_i\), the two root spokes extend toward the metric midpoint of \(T_i\). Every internal vertex is removed by at least one extension. Their potentially heavy side supports are disjoint subsets of represented mass; both cannot exceed \(W/2\). Each extension is an ambient geodesic because both arc endpoints are at root distance \(2\lambda\), every internal arc vertex has degree two in the full graph, and the extension goes no farther than halfway.

At a transition \(V_i\) to \(U_{i+1}\) with a subdivided adjacent arc, \(Q=(c_i,a_i,a_{i+1},c_{i+2})\) has length \(3\lambda\). Any route through \(c_{i+1}\) has length at least \(3\lambda\), and every other route uses at least three branch edges of length at least \(\lambda\); \(k\geq5\) excludes a shorter wraparound. Core isometry makes \(Q\) ambient shortest. Deleting \(P\cup Q\) leaves core components inside the two old light sides or the light rim patch; sector attachments detach individually. If both adjacent arcs are unsubdivided, the two older local detours apply. Failure of the adjacent spokes and both detours would imply \(2M-\alpha_i-\alpha_{i+1}>2W\), contrary to \(M\leq W\). The strict inequalities also handle equality at half mass.

For a heavy outside component in the all-mass corollary, its boundary is a clique of at most three vertices. Glue a width-three torso decomposition to an outside leaf bag at that clique. A weighted centroid cannot be the outside leaf when the component exceeds half the total mass. Its local bag has at most four vertices and half-separates the full graph; pairing the at most four bag vertices gives two ambient geodesics whose union contains the bag. Deleting the additional geodesic vertices preserves the bound. This is the previously reviewed heavy-attachment reduction, and covers the case excluded from the light-attachment sweep.

## Independent verification and trust boundary

The target Python 3.11.2 checker passes its `--check` run: 240 general portal models, 560 annular covers, 2,976 ambient-path/component checks, 9,406 light-patch balance checks, 1,896 heavy-patch replacements, 4,328 heavy-attachment checks, and 39 local decompositions across six fixtures. It imports earlier construction utilities, so its finite runs are exact regressions, not an independent proof.

My [audit.py](audit.py) imports no target code. It builds the core and permitted boundary components from the definitions, computes fresh Dijkstra distances, checks core isometry, all candidate paths and component-side inclusions for 420 rotated or reflected annular systems with \(5\leq k\leq9\), and executes integer mass profiles through the heavy-patch and both sweep transitions. It separately tests the metric path-cover cuts on 500 general three-terminal models. Exact output:

```text
metric_models=500 systems=420 three_portal_covers=3060 heavy_patch=3060 midpoint=17 subdivided_sector=2799 unsubdivided_sector=296 spokes=16748 PASS
```

Reproduce from the repository root with Python 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_subdivided_annuli/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_subdivided_annuli_review1/audit.py
```

Target SHA-256: `README.md` `fee495559063e2c6bf10649027ba80928d6489b5f4b33ae04dab2209c6fc096c`; `verify.py` `df40d83e25486a71c17d8f49558b99a4976b380f250de4f47708fbc8cf97a448`; `expected.json` `d793fe405c5016901dc1c33d22d941aaf31d0f0b6102c9f239c4ad47c9788453`. The all-order, real-mass theorem rests on the written inequalities and component inclusions, not finite sampling. The independent checker uses integer edge lengths and masses and does not certify planar embeddings or local treewidth decompositions. The target checker validates rotations and sample decompositions; the all-mass centroid step relies on the written argument and the prior independent review.

## Literature and mathematical potential

The primary [Diot–Gavoille paper](https://dept-info.labri.fr/~gavoille/article/DG09a) gives a two-path result for face-separable planar graphs. Its class and recursive notion of path separability are different from this explicit one-shot, arbitrary-mass annular gluing theorem, so it does not itself verify the present result. The [Problem 31 statement](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) distinguishes the known two-path \(2/3\) conclusion from the open \(1/2\) target. A targeted search did not locate this precise rim-subdivision exchange, but cannot establish priority. The proof is a credible structural sufficient theorem and a useful path-cover device; a publication would need a polished component-inclusion diagram and a clear comparison with face-separable and earlier annular subclasses.

## Strengthening and improvement opportunities

**Proved structural strengthening.** Ambient planarity can be dropped from both the light-attachment theorem and the width-three all-mass corollary. The proof uses the cyclic annular core, its isometry, the stated attachment-boundary pattern, and local torso width; no step uses an embedding of the full graph. Nonplanar attachments meeting the same boundary rule therefore satisfy the same separator conclusion. This strengthening preserves all metric and boundary hypotheses and does not claim anything for arbitrary nonplanar graphs.

The next substantial boundary is a subdivided arc of total length between \(\lambda\) and \(2\lambda\). The sector detour can then lose shortestness to the route through \(c_{i+1}\), so the current proof genuinely needs a new local exchange or a counterexample at that metric boundary. A second worthwhile direction is to characterize attachments with wider or nonconsecutive active boundaries; the current side inclusions fail as soon as one component bridges both formal sides. Neither extension follows from the finite short-arc rejection control.
