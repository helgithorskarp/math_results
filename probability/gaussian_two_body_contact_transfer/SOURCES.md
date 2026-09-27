# Sources and attribution

- Gautam Aishwarya and Dongbin Li,
  [Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
  Conjecture 1.1 and Section 5, especially Theorem 5.1 and equations
  (101)--(105). This is the sole research problem source. The implication
  from full Gaussian majorisation to arbitrary-radius ball unions and
  its exponentially weighted small-variance construction are theirs.
  Section 5 of our proof makes the finite contrapositive quantitative.
- Erik Carlsson and John Carlsson,
  [Alpha shapes in kernel density estimation](https://arxiv.org/html/2303.12213v3),
  Theorem 1(2), Lemma 1, and Section 3.1. They give a Gaussian KDE
  superlevel representation by power-shifted balls using Fenchel duality.
  The equivalent probability-simplex/Gibbs formula used here is classical.
  We do not claim its discovery, or any of their topological conclusions.
- The classical Kirszbraun extension theorem identifies contractions on a
  compact support with restrictions of global Euclidean 1-Lipschitz maps.
  A modern primary account, including an explicit extension formula, is
  [Kirszbraun's theorem via an explicit formula](https://arxiv.org/abs/1810.10288).
  This standard extension fact is the only input needed to put a finite
  violating support map in the exact global-map form of the headline.
- The prior team
  [shift-averaged interaction boundary](../gaussian_prior_localization/SHIFT_AVERAGING_BOUNDARY.md)
  gives the hinge interaction decomposition and shows that an interaction
  sign can fail when the component maps are not rigid, even though the
  full Gaussian comparison holds. Component rigidity is essential here.
  The scalar two-component identity in (8) is elementary and is not new.
  Our proof is self-contained and does not import that asymptotic example.
- The
  [two-body proper screw](../gaussian_two_body_screw_obstruction/README.md)
  motivates the unresolved geometric regime. Our rational control uses
  the same paraboloid rule, with a different eight-site list. It is only
  an algebra control; no new nonliftability or Gaussian sign is asserted.
  The
  [primitive-composition obstruction](../gaussian_screw_primitive_obstruction/README.md)
  explains why two-body maps remain relevant beyond the existing positive
  mechanisms. Its twenty-four-site obstruction is not proved again here.

The claimed contribution is the fixed-two-body equivalence, including
unequal component variances, and the explicit adverse-contact-to-hinge
certificate interface. A bounded search of the repository, committed graph,
and primary literature found the ball-envelope and Gaussian-to-KP
antecedents above; priority for their stated converse combination has not
been established. This is an author proof awaiting independent review.

The checker uses Python integers and Fraction only. It audits exact
geometry, variance cancellation, finite simplex rounding and conditional
tail-budget constants. It is not a certifier for transcendental profile
volumes, entropy-ball covers, or a numerical witness. The proof requires
no numerical oracle or omitted large artifact; a future counterexample
application must supply the explicit adverse-volume premise separately.
