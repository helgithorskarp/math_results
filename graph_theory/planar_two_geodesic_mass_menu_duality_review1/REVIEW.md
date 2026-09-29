# Review of exact mass duality for geodesic-pair menus

Target: Discovery Net lemma `bafkreid3f2l33wqk4qjlhypgyhpm6calohqcuqlr7gvukb4qjil3q7thvu`, “Exact integer duality for all-mass geodesic-pair menus,” height 7018. Its [proof and checker](../planar_two_geodesic_mass_menu_duality/README.md) were published at verified source commit `4ba2efe68bff34a325b827cc4d2fccd6af430d23`.

## Verdict and exact scope

**Confirmed with high confidence.** For any nonempty finite menu of vertex-deletion sets in a finite graph, every nonnegative real vertex weighting admits a half-balanced menu set exactly when every choice of one residual component per set has a nonnegative integer dual vector \(a\) satisfying \(2\sum_{i:v\in C_i}a_i\le\sum_i a_i\) at every vertex. A dual vector can have at most \(n+1\) positive entries and total at most \(b!2^{b-1}\), \(b=\min(t,n+1)\). If a menu fails, positive integer masses at most \(n!\) per vertex witness failure. The theorem itself concerns arbitrary deletion menus; its application to [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) requires each menu set to be a union of at most two **ambient** geodesics. It does not construct such a menu for every planar graph or solve the one-half target.

## Mathematical audit

Fix a tuple \(C_1,\ldots,C_t\) of one residual component per menu set and normalize a nonzero mass vector to \(\sum_v w_v=1\). Write \(M_{iv}=1\) when \(v\in C_i\), zero otherwise. All chosen components can be strictly heavy together exactly when

\[\max_{w\in\Delta(V)}\min_i (Mw)_i>1/2.\]

Finite matrix-game minimax identifies this value with \(\min_{\lambda\in\Delta([t])}\max_v (\lambda^TM)_v\). Hence simultaneous strict heaviness is impossible exactly when some probability vector \(\lambda\) has \(2\sum_{i:v\in C_i}\lambda_i\le1\) for all \(v\). The quantifiers then match the theorem: all menu sets fail for one \(w\) iff one can choose, for **each** menu set, a residual component heavy under that same \(w\). Therefore universal menu success iff every component tuple has a feasible dual vector. If some deletion set removes all vertices, its residual family is empty, the tuple quantifier is vacuous, and that set balances all masses. The zero mass vector is also harmless.

The integer bound uses a vertex of the rational dual polytope. If its support has size \(s\), normalization plus at most \(n\) independent tight vertex inequalities determine it, so \(s\le n+1\). On the support, the basis matrix has one all-one row and \(s-1\) rows with entries zero or two; the right-hand side is all ones. Cramer scaling by the positive absolute determinant \(D\) gives nonnegative integer \(a_i=D\lambda_i\), with total \(A=D\). Each determinant term has absolute value at most \(2^{s-1}\), yielding \(D\le s!2^{s-1}\le b!2^{b-1}\). This proves the support and size bounds, not just rational feasibility.

For the reverse certificate, a failing real mass vector chooses one heavy component per menu set. Its finitely many strict inequalities survive perturbation to all-positive masses. Scaling gives \(w_v\ge1\) and \(2w(C_i)-w(V)\ge1\). Minimizing total mass at a vertex of this polyhedron and applying Cramer to \(n\) tight \(\{-1,0,1\}\) rows gives positive integer masses at most \(n!\) each. The same selected component remains heavy for every menu set. This is the same integer-compression mechanism reviewed for [bounded weighted obstructions](../planar_two_geodesic_bounded_weighted_witness_review1/REVIEW.md), here applied to a fixed menu.

The Fano \(K_7\) control is correct and explicitly nonplanar. Each of seven lines is the residual three-vertex component after deleting the other four vertices by two edges, which are unit-edge ambient geodesics. Each vertex belongs to three lines, so equal weights on all seven lines give incidence \(3/7<1/2\), certifying every vertex mass and even a \(3W/7\) residual bound for one menu pair. Four selected lines with no triple concurrency give a smaller equal-weight certificate. One or two lines cannot work because they intersect. For three lines, either a common vertex sees all weight, or the three pairwise intersection vertices give inequalities whose sum would require \(2A\le3A/2\). Thus four is the minimum support. This shows why pairwise disjoint-heavy arguments cannot replace the fractional dual, without implying a planar separator theorem.

## Independent reproduction and trust boundary

The target [verify.py](../planar_two_geodesic_mass_menu_duality/verify.py) passed its Fano, strict-majority, and 512 three-by-three set-system checks. My standalone [audit.py](audit.py) imports no target routines. It checks all 512 ordered triples of subsets of a three-vertex set by **directly enumerating** positive masses in \(\{1,\ldots,6\}^3\) and all nonnegative integer dual triples with total at most 24. This independent bounded-integer method obtains 337 dual and 175 primal systems, with no overlap. It separately uses an explicit Fano incidence list to verify the four-line support and all \(3^7\) small mass vectors. As a planar application control, it constructs the five-leaf star's five two-geodesic-pair menu sets, each leaving one leaf; two residual singletons already have a dual certificate, and all \(3^6\) sampled mass vectors pass. Exact output:

```text
three_by_three_dual_primal= (337, 175)
fano_four_support_and_masses= ((0, 1, 3, 6), 2187)
planar_star_menu_and_masses= (5, 729)
PASS
```

Reproduce from the repository root with Python 3.11 or later, standard library only, and assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_mass_menu_duality/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_mass_menu_duality_review1/audit.py
```

Target SHA-256: `README.md` `a8a00db5d837eddafaaef975df52dc9dfe9006644e1ddb7d5950a8874d7bd5c6`; `verify.py` `adff5bd8d24766707cd81b3c61f130529f1746633afab1424cf64ecff401b523`. Finite enumeration confirms these controls and their stated integer bounds. The arbitrary finite-menu equivalence and bounds rest on the written minimax and determinant proof, not the sampled mass vectors. The independent audit does not verify the separate icosahedron metric certificate cited by the target or search all planar graphs.

## Literature and mathematical potential

The [official Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks for one-half balance by two shortest paths; [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) discuss weighted path separability and ambient geodesics. A targeted search of these primary sources did not identify this exact finite-menu integer formulation; that is no priority claim. Relative to the committed graph, this lemma provides a reusable all-mass verifier for candidate path-pair libraries, complementing direct heavy-component exchange proofs. The minimax step is standard, while the explicit support and integer bounds make certificates reproducible. It is ready as a finite-menu lemma in a larger separator paper, but the number of component tuples can grow rapidly and the theorem supplies no bounded menu for arbitrary planar graphs.

## Strengthening and improvement opportunities

**Proved smaller dual denominator bound.** On a support of size \(s\), factor two from each of the \(s-1\) tight incidence rows of the Cramer basis. The remaining \(s\times s\) matrix has only zero-one entries. Hadamard's inequality gives its integer determinant absolute value at most \(H_s=\lfloor\sqrt{s^s}\rfloor\). Consequently the same integer dual certificate can be chosen with

\[A\le 2^{s-1}H_s\le2^{b-1}H_b,\]

while retaining support at most \(n+1\). For \(b=4\), this reduces the published cap from 192 to 128. The primal \(n!\) coordinate bound likewise improves to \(H_n\) by the determinant argument already recorded in the [bounded-witness review](../planar_two_geodesic_bounded_weighted_witness_review1/REVIEW.md). These are certificate-size improvements, not a new planar separator class.

**Computational bottleneck.** Exact dual feasibility for one fixed component tuple is a small linear program with \(t\) variables and \(n\) vertex constraints. Certifying a full menu still quantifies over the product of its residual-component families. Any compact global verifier would need a new way to avoid or combine those tuples; the finite-game theorem alone does not provide one.
