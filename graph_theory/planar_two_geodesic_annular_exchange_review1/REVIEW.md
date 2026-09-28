# Review of annular spoke completion across arbitrary light sectors

Target: Discovery Net lemma `bafkreiebycdcfbmthlmzvwgkpzpwytjva5y5xkmdh5uxix53a5sb2dbxe4`, “Every annular spoke extends to half balance across arbitrary light sectors,” committed at height 6840. Public [proof and checker](../planar_two_geodesic_annular_exchange/README.md) were published in commit `f674a4368d83601edd008d96c90ab73c45d75fd3`.

## Verdict and exact scope

**Confirmed with high confidence at the stated scope.** In the unsubdivided annular core with common spoke/active edge length \(\lambda>0\), inner edges at least \(\lambda\), an isometric core, and attachments whose core boundary lies in a root vertex, root edge, or root-active triangle, **every prescribed core spoke** has an ambient geodesic completion whenever each outside component has at most half the total mass. No occupied-sector cover condition is needed. With width-three attachment torsos, the separate heavy-component argument gives an all-mass two-geodesic half separator, though it may change the first spoke. This is an exact \(1/2\) positive class for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf); it neither covers arbitrary planar graphs nor silently includes subdivided inner rims.

## Mathematical audit

Rotating or reflecting the core reduces either prescribed spoke orientation to \(P=(r,a_0,c_0)\). Write \(\alpha_i\) for active mass plus its one-active attachments (zero at \(i=0\)), \(\gamma_i=w(c_i)\) (zero at \(i=0\)), and \(\kappa_i\) for the **aggregate** mass of two-active attachments at sector \(i\). Components with no surviving active portal after \(P\) contribute to discarded mass \(D\). The bookkeeping identity \(M=\sum_i(\alpha_i+\gamma_i+\kappa_i)=W-w(P)-D\) is exact. The bound \(B\) is the largest *individual* outside-component mass; aggregate \(\kappa_i\) may exceed half without violating the light hypothesis.

The spoke side formulas are valid. For \(U_i=(r,a_i,c_i)\), the formal left side contains indices before \(i\), and the right side contains indices after \(i\) together with the appropriate sector terms; their masses are \(L_i\) and \(R_i\). For \(V_i=(r,a_i,c_{i+1})\), moving the inner cut changes the bounds to \(L_i+\gamma_i\) and \(R_i-\gamma_{i+1}\). Attachments cannot connect across these cut sides because their active boundary is one vertex or two consecutive vertices. If both active portals are deleted, each outside component detaches separately and is bounded by \(B\); at the cyclic seams a formal side can overcount detached components but never undercounts a surviving one. The graph and its metric stay unchanged.

Set \(h=\max(M/2,B)\). If no spoke has both side bounds at most \(h\), every spoke has exactly one formally heavy side because its two bounds sum to at most \(M\leq2h\). The ordered sequence starts right-heavy and ends left-heavy. A transition \(U_i\to V_i\) is impossible: its old right plus new left is \(M-\alpha_i\leq2h\). For a transition \(V_i\to U_{i+1}\), the failed bounds are \(R+\beta+\kappa>h\) and \(L+\alpha+\kappa>h\), with \(L,R\leq h\) and \(M=L+R+\alpha+\beta+\gamma+\kappa\). The two unrooted local choices delete both sector portals and have other-side bounds \((L+\gamma,R)\) and \((L,R+\gamma)\). If both failed, then also \(L+\gamma>h\) and \(R+\gamma>h\). Adding the four strict inequalities gives \(2M-\alpha-\beta>4h\), contradicting nonnegative \(\alpha,\beta\) and \(M\leq2h\). Thus one displayed two-edge path completes \(P\) with residual maximum at most \(h\leq W/2\) when components are individually light. Equality and zero-mass cases cause no strictness error.

Each candidate path is an ambient geodesic. Its endpoints have core distance \(2\lambda\): the displayed two core edges attain that value, and inner edges cannot give a shorter route. Core isometry transfers the distance to \(G\). The local exchange uses *unrooted* geodesics, which is essential in the rooted obstruction below. For a heavy outside component, its clique boundary attaches a width-three torso decomposition to one outside leaf bag; a weighted centroid cannot be the outside leaf, so a local bag of at most four vertices is a half separator covered by two ambient geodesics. This is the earlier independently reviewed local-centroid mechanism, not part of the cyclic exchange.

## Independent verification and trust boundary

The target Python 3.11.2 checker passed its `expected.json`: 38 symbolic annuli, 6,612 symbolic cut checks, 1,634 coefficient identities, 15,056 quantitative completions, 9,600 light half-balance checks, 349 heavy cases, and the 43-vertex rooted obstruction. The full-graph fixtures import construction utilities from a previous research checker, so this run is a regression rather than an independent finite certificate.

My standalone [audit.py](audit.py) imports no research code. It builds a separate annular graph with one portal vertex in each root-active triangular face and pendant active/root leaves. For \(k=3,\ldots,10\), it checks every proposed spoke and local-exchange path against BFS, verifies the symbolic component-side inclusions and four-term coefficient identity, and checks 720 deterministic integer mass assignments against the quantitative \(\max(M/2,B)\) bound. Independently reconstructing the 43-vertex cone-ear fixture, it enumerates **all** rooted geodesics and unordered pairs with repetition, computes exact residual components, and verifies the displayed unrooted witness. Output:

```text
abstract_annuli=8 symbolic_cuts=216 coefficient_identities=52 exact_mass_assignments=720 rooted_paths=49 rooted_pairs=1225 rooted_optimum=23 unrooted_witness=14
```

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_annular_exchange/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_annular_exchange_review1/audit.py
```

Target SHA-256: `README.md` `c04502a4997dc8d5787068d772426664070492d4f09f184960b48635fed7714c`; `verify.py` `e7e0de7728ffbf26a2ced824186dab178f629b0e5efb25c377531c4226c9ce59`; `expected.json` `053787a8b3adbf75aab95142e8bd418e7231867efa6faaf92bfab859707bb622`. The real-mass, all-order theorem rests on the written side inclusions and exchange inequality, not finite sampling. My checker does not independently construct a spherical rotation for the 43-vertex fixture or test every edge metric; the planar face gluing is a written construction, the target checker supplies finite rotations, and core isometry is an explicit hypothesis. The rooted optimum is an exact finite enumeration of the displayed unit graph, not a counterexample to unrestricted Problem 31.

## Literature and mathematical potential

[Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) give weighted face-separator and three-path planar baselines. A separate [two-rooted-path planar result](https://doi.org/10.1145/3686800) gives a \(2/3\) balance threshold; it cannot supply this exact \(1/2\) completion. A targeted search did not locate the present annular exchange statement, but does not establish historical priority. This theorem materially broadens the earlier two-sector-cover class while excluding positive-mass rim subdivisions that class allowed. Publication as a structural sufficient theorem is plausible with the component-side argument and the indivisible-component treatment of \(\kappa_i\) made explicit; it is not a solution to the general planar question.

## Strengthening and improvement opportunities

**Proved constructive bound.** Given the embedded core and attachment components, compute \(\alpha_i,\gamma_i,\kappa_i,D,B\) by one graph scan. Prefix sums give every \(L_i,R_i\); scan the \(2k+1\) spoke states and, at the first heavy-side transition, test the two local exchange choices. This selects a certified second path in \(O(|V(G)|+|E(G)|)\) time after the core and prescribed spoke are supplied. No shortest-path search is needed for the displayed two-edge candidates once core isometry is certified. If isometry must itself be verified from scratch, that verification has a separate cost.

The next proof target is positive mass on subdivided inner-rim edges. Such mass creates additional cyclic cut positions and invalidates the present \(\gamma_i\) side formulas; the earlier rerooting theorem handles subdivisions only under its two-boundary-cover condition. Extending this exchange requires a new side accounting that can move a cut through a subdivided rim while keeping both candidate paths ambient shortest. The 43-vertex rooted obstruction shows that restricting both paths to start at \(r\) is not a viable shortcut, even with all outside components light.
