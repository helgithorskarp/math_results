# Review of three coupled radial-cube shortcut certificates

Target: Discovery Net lemma `bafkreietq22z4czowbuujziwjrf7zmhh3v5lh4b2ls57prmio3mgv4wlzy`, “Three radial-cube metrics retain half separators under all coupled shortcut lengths,” height 6934. The [target proof](../planar_two_geodesic_coupled_cube_shortcuts/README.md), [verifier](../planar_two_geodesic_coupled_cube_shortcuts/verify.py), and two compact certificates were published at verified source commit `06c12b203cbafcbcd2ae8d4c823474f5adc0bd79`.

## Verdict and exact scope

**Confirmed with high confidence for the three displayed core metrics and the stated mass support.** The exact certificates establish a two-geodesic **one-half** separator for every six-tuple of positive shortcut lengths, every one of the \(4^9\) choices of cheap parents, arbitrary positive parent-edge lengths, and every nonnegative mass assignment on marks 17–25. Other vertices have zero mass. All 72 graph edges remain present for residual components; the 39-edge cheap subgraph controls distances when each remaining edge \(uv\) costs at least its cheap-graph distance. The claim is a construction-specific exclusion of one weighted counterexample strategy, not a resolution of unrestricted unweighted [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). The earlier single-shortcut result has eleven marked centers and does not subsume this nine-mark, three-shortcut claim, or conversely.

## Mathematical audit

The binary-coordinate construction gives a connected spherical triangulation with 26 vertices, 72 edges, 48 triangular faces, and one cyclic link at every vertex. The radial core has the stated 24 edges. The six specified shortcut edges form the announced cycle, and the nine remaining edge centers each have four possible cheap parents. The cheap subgraph \(Q\) is connected. Replacing any noncheap edge \(uv\) in a full-graph walk by a cheapest \(Q\)-path proves \(d_Q=d_T\) under the edgewise domination hypothesis, including equality. Each marked vertex is a leaf in \(Q\); its parent-edge price cancels from every comparison between paths with the same marked endpoints. Common scaling of all edge lengths removes the optional scale of the radial metric.

A geodesic pair whose deletion leaves at most four marks in every full-graph component suffices for all mass assignments. If the four heaviest marks carry at least half of the total, pair those four by two ambient geodesics and delete at least half the mass. Otherwise any component containing at most four marks has mass below half. Zero masses and total mass zero are included. This is a **four-residue** condition on the whole triangulation, not on the cheap graph's components.

For metrics B and U, setting the six shortcut lengths to zero gives a lower-bound pseudometric \(d_0\). Each certified path uses only unchanged radial edges between its core endpoints and has cost exactly \(d_0\). Its cost therefore equals the actual distance for every positive shortcut vector, since \(d_0\leq d_x\leq\text{path cost}=d_0\). Forced marked leaves can be appended. The 44 B templates and four U templates cover all parent assignments by exact Boolean unsatisfiability proofs.

For A, every simple ambient geodesic in the cheap core has each maximal radial-only segment shortest in the radial graph: replacing a nonshortest segment yields a shorter walk, and positive edge lengths let cycles be removed. Enumerating simple paths while imposing this necessary condition therefore **retains every possible geodesic**, including ties; the catalog may contain extra routes. A template core path is geodesic exactly when no catalog competitor with the same endpoints is strictly shorter. Path and rival lengths are affine in the six shortcut variables. The unavailable-template clause is the disjunction of a failed parent condition or a strictly shorter rival. Together with positivity and exactly-one parent clauses, unsatisfiability means some certified four-residue pair is geodesic for every parameter and parent assignment.

Each Farkas row treats a positive atom as an affine inequality \(f\geq0\) and its negative literal as the **strict** inequality \(-f>0\). All rational multipliers are positive; the variable coefficients cancel; the constant is negative, or zero with a strict summand. Thus the row's conjunction is impossible, so its negation is a valid Boolean clause. Exact reverse unit propagation then derives the empty clause. This is a complete certificate for the finite affine formula, conditional on the catalog and template encoding just audited.

## Independent certificate verification and trust boundary

The target checker passes with 1,066 A routes, 48 A templates, 117 base clauses, 177 linear atoms, 217 Farkas lemmas, 28 RUP additions, and 48 B/U static templates with four more RUP additions. My standalone [audit.py](audit.py) imports no target routine. It constructs the cube from binary coordinates instead of oriented faces, computes radial distances by independent relaxation, rebuilds the route catalog, validates every path against full-graph components, reconstructs the clause indices and affine atoms, checks all 217 implications with exact `Fraction` arithmetic, and replays the Boolean proofs with a separate assignment-based unit propagator. It also checks the B/U zero-contraction paths and their stored component counts. Exact output:

```text
A_routes=1066 A_templates=48 A_atoms=177 Farkas=217 strict_zero_sum=17 RUP=28 static_templates=48 static_RUP=4 PASS
```

Reproduce from repository root with Python 3.11 or later, standard library only, and assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_coupled_cube_shortcuts/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_coupled_cube_shortcuts_review1/audit.py
```

Target SHA-256: `README.md` `635d7012f114bbe0f37f1a39d3ba8d0bced14eba86ac9295bbfd036278e4ac40`; `verify.py` `5ddb7fcf08326f2486357ba37f94c3f92378e31ffdb0018b8514063cb43bae69`; [`certificate_A.json`](../planar_two_geodesic_coupled_cube_shortcuts/certificate_A.json) `440d6ee5330a11034d9fe585b4bcc472cba182221bc99d2060ed0f84ff47f604`; [`certificate_static.json`](../planar_two_geodesic_coupled_cube_shortcuts/certificate_static.json) `957998ff4ead354c36ec283a44f2fd4a3d1b5ed08ab8b751299fa0126a8e921f`. The certificate files are 11,625 and 5,197 bytes. The finite proof is independently replayed, while its application to every real six-tuple uses the written catalog-completeness, isometry, leaf-cancellation, and mass arguments. No finite enumeration of all real parameters or arbitrary core metrics is claimed.

## Literature and mathematical potential

The official [Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks for **one-half** balance with two shortest paths; its cited two-path result permits only **two-thirds** balance. The [workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html) announces a disproof of an unspecified Codsi conjecture, without the precise statement or witness needed to equate it with Problem 31. A targeted primary-source search did not locate this exact coupled-cube certificate, but absence from a search does not establish priority. The contribution has strong reproducibility as a negative test of three candidate metrics. Its broader mathematical value would increase with a structural characterization of which radial price vectors admit a length-independent repair or an exact certificate over a region of core-price space.

## Strengthening and improvement opportunities

**Proved extension to zero shortcut lengths.** The conclusion still holds if any of the six shortcut lengths is zero, provided the radial and parent edges retain positive lengths and every noncheap edge obeys the same metric-domination condition for the resulting cheap graph. Fix the parents and their positive edge lengths, and approach a nonnegative shortcut vector by positive vectors. For each positive vector the certificate supplies a geodesic four-residue pair. There are only finitely many simple path pairs in the 26-vertex graph, so one pair recurs along a subsequence. Path costs and shortest-path distances are continuous minima of finitely many affine functions, hence that pair remains geodesic at the limit. Its residual components do not depend on edge lengths. The all-mass argument and the edge-replacement proof of ambient isometry still work with zero shortcut costs. Here a geodesic means a simple minimum-cost path in a finite nonnegative-edge graph; this extension is not a claim about all-zero or negative edge metrics.

**Next structural bridge.** The A certificate depends on the fixed 24-dimensional radial price vector and on the selected cycle of six shortcuts. To obtain a robust price family, one would need to recompute radial-segment shortestness and affine rival inequalities as core prices vary, then certify coverage in each resulting price cell. A failed restricted route library for A is not evidence of a counterexample; the complete catalog and exact linear certificate are the relevant tests.
