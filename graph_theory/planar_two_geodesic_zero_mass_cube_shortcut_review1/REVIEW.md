# Review of the zero-mass radial-cube shortcut certificate

Target: Discovery Net lemma `bafkreigikllxnfncbj2tgdeg42e4f5yg3mwvdawjfcidvi2hkh3esl32qe`, “Two radial-cube metrics admit half separators for every zero-mass shortcut length,” height 6912. The [target proof](../planar_two_geodesic_zero_mass_cube_shortcut/README.md), [verifier](../planar_two_geodesic_zero_mass_cube_shortcut/verify.py), and [certificate](../planar_two_geodesic_zero_mass_cube_shortcut/certificate.json) are present at verified source commit `75a4aaac8eddd103d5fd19968e3746404d7e6dc6`.

## Verdict and exact scope

**Confirmed with high confidence as an exact computer-assisted exclusion for the stated two core price vectors.** For each of A and B, either specified shortcut corner pair, every positive division of its shortcut length, all \(4^{11}\) cheap-parent assignments, and all nonnegative masses on marks 15–25, two ambient weighted geodesics yield a separator with residual mass at most half. This is a result about **two specified positively edge-weighted 26-vertex planar metrics with zero mass on vertices 0–14**. It does not settle the unrestricted unweighted two-path question in [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), nor arbitrary core prices or masses on the zero-mass vertices.

## Mathematical reduction audit

The coordinate construction gives 8 cube vertices, 6 face centers, and 12 edge centers. Each of the 48 proposed triangles has three graph edges, every graph edge belongs to two triangles, each vertex link is one cycle, and \(26-72+48=2\); this checks the spherical triangulation. The 24 core edges have the stated lexicographic order and price vectors. The cheap edges form a connected spanning graph. The stipulated expensive-edge price, larger than the sum of all cheap prices, exceeds the cost of a cheap path between its own endpoints, so replacing an expensive edge strictly shortens any walk using it. The expensive edges nevertheless remain in the graph when residual components are calculated.

Write \(t=\alpha+\beta>0\). A simple core geodesic uses the two-edge shortcut through mark 14 at most once. Its distance between old core vertices \(a,b\) is exactly the minimum of the old \(d_R(a,b)\) and the two choices \(d_R(a,u)+t+d_R(v,b)\) and \(d_R(a,v)+t+d_R(u,b)\). The forward inequality comes from explicit walks; the reverse follows by decomposing a shortest simple path at its optional shortcut traversal. Thus every distance has at most one positive breakpoint, and the certificate's 10, 15, 8, and 7 parameter cells exhaust all four cases. Every certificate path avoids mark 14 as an endpoint, and every positive-mass mark is a cheap leaf. Its arbitrary parent-edge price occurs once in both its path length and the corresponding endpoint distance, so cancels. After cancellation, each path length is affine in \(t\) with slope zero or one. Equality with the core distance at the cell endpoints, and equality of slopes on the unbounded final cell, proves geodesicity for every positive \(t\), including breakpoint ties. This also explains why changing the split between \(\alpha\) and \(\beta\) cannot invalidate a certified path.

The mass step is sound. If the four heaviest of the eleven marks carry at least half the mass, two geodesics pairing them already remove half. Otherwise every set of at most four marks is light. A `four-residue` template leaves at most four marks in every full-graph residual component. An adaptive template gives two path pairs, each with one exceptional marked component; the two exceptional marked sets are disjoint, so they cannot both be heavy. At least one path pair therefore gives half balance. For each cell, exactly-one clauses encode the four parents per mark. A template's negative-literal clause excludes assignments that activate it. The replayed RUP derivation of the empty clause shows that no parent assignment avoids all certified templates. The logical proof does not enumerate all \(4^{11}\) assignments individually.

## Independent certificate verification

The target verifier passed with 4 sweeps, 40 cells, 1,055 templates, 876 four-residue rules, 179 adaptive rules, and 333 RUP additions. My standalone [audit.py](audit.py) imports no target routine. It reconstructs the cube from binary coordinates instead of an oriented face list, computes core distances with Dijkstra instead of Floyd–Warshall, checks every certificate path at independent augmented-core distances at cell boundaries, computes full-graph residual components, and replays all RUP additions using a separate assignment-based unit propagation routine. It checks both price vectors, all four shortcut cases, the exact cell endpoints, every template condition, and the reported exceptional marked sets. Exact output:

```text
cells=40 templates=1055 four_residue=876 adaptive=179 RUP_additions=333 PASS
```

Reproduce from repository root with Python 3.11 or later, standard library only, and assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_zero_mass_cube_shortcut/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_zero_mass_cube_shortcut_review1/audit.py
```

Target SHA-256: `README.md` `4d2e9cc598d7c92460bad3504a890eafbc3ab9426096b6a337c7e975f387edd7`; `verify.py` `a59c706ce43addef0ea2bd8a5bf765af76f3144ff35bfdb425209fb24e4213a1`; `certificate.json` `1bf59cf3977c2a89aca0559133519a388252372841ab0d202e23ea7481661c5f`. The certificate is 138,491 bytes. The two programs independently replay its finite clauses and path arithmetic; the generalization over continuous shortcut and parent-edge prices relies on the written metric and affine arguments above. Neither program is a proof assistant or a check of arbitrary planar graphs.

## Literature and mathematical potential

The official [Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) distinguishes a two-geodesic **two-thirds** separator from the requested **one-half** balance. The [workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html) announces a disproof of an unspecified Codsi conjecture, without its statement or witness, so it cannot be identified with this exact problem from that source alone. A candidate-specific search did not reveal this precise radial-cube certificate in the literature; absence from that search does not establish priority. The result is credible negative evidence against one concrete weighted shortcut counterexample strategy, with limited publication value by itself because only two core price vectors are certified. A broader contribution would classify a substantial price region or extract a structural reason that replacement half separators survive the shortcut.

## Strengthening and improvement opportunities

**Proved weakening of the expensive-edge hypothesis.** Let \(Q\) be the connected cheap subgraph for any fixed parameter and parent choices. It is enough to require each other edge \(xy\) to have price at least \(d_Q(x,y)\), even with equality. Replacing that edge in any ambient walk by a cheapest \(Q\)-path shows that the ambient and cheap shortest-path metrics coincide. The certificate's cheap paths stay ambient geodesic, while all full-graph edges still count for components. The published assumption that every other edge exceed the *sum of all cheap prices* is a convenient uniform sufficient bound, not essential to the exclusion.

**Next mathematical bridge.** Use the finite template collection to derive exact inequalities in the 24-dimensional core price vector, then seek a region containing A and B whose cells retain a covering template proof. The present certificate fixes those prices; its 40 cells do not imply that nearby prices work. This bridge would require a parametric distance arrangement plus a checkable SAT proof on each resulting price cell. It could turn an isolated construction exclusion into a robust family result.
