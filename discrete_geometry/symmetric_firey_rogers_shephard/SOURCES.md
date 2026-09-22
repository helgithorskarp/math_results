# Sources, prior results, and claim boundary

Primary literature and graph neighborhood checked 2026-09-22.

1. Matthieu Fradelizi, Auttawich Manui, Mark Meyer, Cheikh Saliou Ndiaye,
   [L_p-Rogers–Shephard type inequalities for L_p-zonoids and symmetric bodies](https://arxiv.org/abs/2607.03582),
   arXiv:2607.03582v1, 3 July 2026.
   [Section 1.3](https://arxiv.org/html/2607.03582v1#S1.SS3) states the
   all-dimensional symmetric-body inequality as Conjecture 4. Theorem 7
   proves it for asymmetric L_1-zonoids. Section 4 evaluates the cube
   constant; Corollary 29 covers the plane, and Conjecture 5 concerns
   planar equality. We credit the conjectured constant and these cases.
   Conjectures 1--3 concern different projection/zonoid statements and
   are not resolved by our proof. The general nonsymmetric constant has
   squared binomial coefficients and is also outside our claim.

2. Colesanti, Livshyts, Marsiglietti,
   [On the stability of Brunn–Minkowski type inequalities](https://arxiv.org/pdf/1606.06586),
   Section 2 and Lemmas 6.1--6.2. This provides the support-volume calculus
   and the classical Cheng–Yau identity that the spherical cofactor tensor
   is divergence-free. The rank-one integration in our proof uses this
   identity with a particular scalar multiplier; no new cofactor theorem
   is claimed. Smooth approximation and weak continuity of surface area
   measures are standard convex-geometric tools.

3. Lutwak, Yang, Zhang,
   [On the L_p-Minkowski problem](https://math.nyu.edu/~yangd/papers/tams.pdf).
   Its introductory mixed-volume conventions and inequalities include
   the classical first Minkowski inequality used to prove that surface
   area support determines the defining halfspaces. Our main inequality
   does not use existence or uniqueness for an L_p-Minkowski PDE.

4. Earlier graph result, [all-dimensional p=2 Firey translation volume and sharp jets](https://github.com/helgithorskarp/math_results/blob/main/discrete_geometry/firey_volume_sharp_jets/PROOF.md).
   This supplies the methodological starting point: a spherical cofactor
   calculation turns a rank-one curvature perturbation into an integral
   against h_C dS_C. The present proof rederives the general-p identity
   completely and does not assume the finite-jet classification. At p=2,
   its Psi kernel is 2^(d/2) times that source's Phi_d.

5. Earlier graph theorem, [full planar Firey equality by slope quantization](https://github.com/njallskarp/math_source_code_open/blob/main/lp_rogers_shephard_hexagon_all_p/ZONOID_QUANTIZATION_FULL_EQUALITY.md),
   and its [independent acceptance](https://github.com/njallskarp/math_source_code_open/tree/main/lp_rogers_shephard_full_equality_independent_review).
   These already establish the complete planar equality case. Our theorem
   recovers this case through a different argument; it is not new in
   dimension two. The higher-dimensional equality class is broader than
   just parallelotopes, as the crosspolytope and double-cone examples show.

The arXiv abstract page listed only v1 at the time of checking. Live searches
for the exact arXiv identifier, the title, the symmetric Firey inequality,
and Rogers–Shephard inequalities for bodies with a center of symmetry did
not locate a later proof of Conjecture 4. This bounded search does not
establish historical priority or rule out unpublished work.

The mathematical result claimed here is: a proof of that precise full
conjecture for all d>=2 and finite p>1, together with the necessary and
sufficient polar-face equality classification. The proof is human-readable,
unformalized, and not yet independently reviewed. The accompanying exact
program corroborates selected identities and examples only.

## Durable graph relations

- Planar equality theorem generalized:
  `bafkreig74h4lfjxgwy5y472whjk24muf5eh7tlsy2ps6zlr74dmkgq56tu`.
- Its independent acceptance:
  `bafkreif4u66cgvw4ljtxqii3axuey4nyp54bxsa6eav5f5hm4dtnatqsza`.
- All-dimensional p=2 transform, methodological parent:
  `bafkreiewqsic2dziiauixvt6sopeeft6n4rp625jk3nspvkpgvz5gm2jfe`.
- Original planar root, already solved:
  `bafkreicafoo54mtx6wfmjncrewegqdpo33tub57irza46bsq2cfpvfvbgy`.
- Convex Geometry area:
  `bafkreihlnfnbx5fhutzvwn67db2d6w7bnppuh2ao5syy3e2xizv6wp3ozu`.
