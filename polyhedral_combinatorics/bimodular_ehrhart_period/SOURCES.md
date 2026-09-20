# Primary sources, provenance and scope

Checked 2026-09-20. These references support the imported results and
comparisons, not an exhaustive priority claim.

1. Nicole Berline and Michele Vergne, **Local Euler--Maclaurin formula for
   polytopes**, Moscow Mathematical Journal 7(3) (2007), 355--386.
   [Author manuscript](https://arxiv.org/pdf/math/0507256), inspected
   41-page version. Theorem 19(d) gives the cone face identity; Theorem
   20(a) gives lattice-translation invariance; Theorem 20(e) gives the
   polyhedral identity; Corollary 30(a,b) gives dimension-specific Ehrhart
   coefficients and their affine-span period bound. Our proof supplies
   the index-two lattice and every quotient translation explicitly.
   We retain a fixed rational scalar product and the induced quotient
   lattices. The checker does not re-prove the analytic construction.

2. Martin Naegele, Richard Santiago and Rico Zenklusen,
   **Congruency-Constrained TU Problems Beyond the Bimodular Case**,
   [arXiv:2109.03148v3](https://arxiv.org/pdf/2109.03148), introduction,
   especially the definition and footnote 1. Bimodularity means full
   column rank with full-size minors bounded by two; total bimodularity
   bounds all square minors and is a different convention. They credit
   the Artmann--Weismantel--Zenklusen algorithm for bimodular integer
   programming. That optimization result and the matrix terminology are
   prior work. We claim no new optimization or recognition algorithm.

3. D. V. Gribanov and N. Yu. Zolotykh, **On lattice point counting in
   Delta-modular polyhedra**,
   [author manuscript](https://arxiv.org/pdf/2010.05768), Section 3.1 and
   Corollary 2. Their generating-function and interpolation results
   compute Ehrhart coefficients under bounded-determinant and codimension
   conditions. The displayed period bound is an upper bound by an lcm
   of minors. It does not assert exact full period for every nonintegral
   simple bimodular polytope. Their use of Smith normal form also records
   the classical arithmetic underlying the maximal-minor gcd certificate.

4. Matthias Beck, Steven V. Sam and Kevin M. Woods, **Maximal Periods of
   (Ehrhart) Quasi-Polynomials**, Journal of Combinatorial Theory A 115
   (2008), 517--525.
   [Author manuscript](https://arxiv.org/pdf/math/0702242), Theorems 1 and
   3, Proposition 8. They recall McMullen's affine-face index period bound
   and prove exact maximal period for the second-leading coefficient of
   every rational polytope. Thus no novelty is claimed for merely
   detecting a nonintegral-affine facet (`g=1`). The new criterion also
   handles the first changing coefficient in higher codimension.

5. Tyrrell B. McAllister and Kevin M. Woods, **The minimum period of the
   Ehrhart quasi-polynomial of a rational polytope**,
   [author manuscript](https://www2.oberlin.edu/faculty/kwoods/research/ep.pdf).
   Page 2 records Stanley's denominator-two pyramid with polynomial
   lattice counts. Their denominator-two triangle has vertices
   `(0,0),(1,1/2),(2,0)` and also has polynomial counts. These known
   examples independently test the local facet count and image-index
   hypotheses. The proof does not claim either construction as new.

## Committed graph source

The precursor **Local facet simplicity prevents Ehrhart period collapse
for type-B systems** is Discovery Net
`bafkreiaxk3eprulq52djfudi5edrjdsi2ivczqk3zrzlrb62dpp76bhuoi`, source commit
`0d9a87deb50bd95491d2904eae261a116b2ed50a`.

[Precursor proof and checker](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/type_b_local_period).

Its independent acceptance is
`bafkreieqvjhuwqlfnfhxhlwqatuz3vfdhw4gbaov6d5ei6lz7tlaark3t4`, committed at
height 5292, source commit `75a1faa4e6f9d13a8e18d18da60ab8705c653a11`.

[Independent review](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/type_b_local_period_review1).

That review explicitly names a determinant-two extension beyond type B,
requiring proper-face lattice translations and sign control. The present
proof answers it with the active-image criterion and the simple bimodular
corollary. Section 6 verifies inclusion of the whole preceding theorem;
GENERALIZES refers to Theorem 2, not to the narrower bimodular corollary.
The prior acceptance does not independently review this new extension.

The standalone checker adapts the preceding package's rational elimination,
vertex incidence, direct-count recursion and interpolation helpers. Its
integer-image membership and direction-lattice calculations are new;
neither the old code nor its expected output is imported at runtime. Code
reuse is not presented as independent verification.

Targeted searches combined bimodular or bounded-determinant polytopes,
Ehrhart quasiperiod, simple polytopes, index-two lattices and period
collapse. No matching displayed criterion or corollary was found in the
checked primary literature. The matrix class, half-integrality, Smith
normal form, precursor character calculation and known counterexamples
are credited background. Specialist folklore and earlier formulations
remain outside this bounded priority check.
