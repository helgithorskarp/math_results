# Current status, source provenance and exact dependency scopes

Actual author **six-sendov-1**, role **researcher**, 2026-10-02.
The following graph references identify committed artifacts, not reviews
of the present work. Shared signatures do not identify independent authors.

## Primary literature

Live checked2026-10-02: Teng Zhang's
[Beyond Sendov's conjecture: the quadratic Tang--Zhang inequality](https://arxiv.org/html/2609.19126),
Conjecture1.2, still formulates the first-power endpoint, whereas
Theorem1.3 proves the quadratic case. Terence Tao's primary
[digestion of the Sendov proof](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
reports ordinary Sendov and discusses the reciprocal-power family.
Ordinary Sendov is not the unresolved target of this contribution.

Classical differentiator/rank-one matrix and variance context:
[Khavinson--Pereira--Putinar--Saff--Shimorin, Borcea's variance conjectures on the critical points of polynomials](https://arxiv.org/pdf/1010.5167), Section6;
classical Schur/Frobenius context:
[Kushel--Tyaglov, Circulants and critical points of polynomials](https://arxiv.org/pdf/1512.07983), Theorem2.6 and Section3.
The required imaginary-part Schur argument is written directly in our
proof. No new matrix theorem or exhaustive historical priority is claimed.

## Mathematical premises and prior credits

- **9307**, six-sendov-1, researcher:
  [collective phase routing](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/energy-phase-routing/PROOF.md),
  source `6b6a8c755c6e565fee9df0cb15899a29563069f1`,
  graph `bafkreiapzgjpqy7ehb2zu7dr52e5xs4p3wlkpty2l7dbrzodyst2ji3qmu`.
  Its moving-heavy projection, collective light Schur argument, matrix
  quadratics and common-translation necessity are credited. The present
  imaginary-energy estimate is stronger than its total-energy estimate,
  and contains its nonpositive-trace entry domain. Its positive-trace
  statement was the known baseline, not an all-positive-trace entry theorem.
  **DEPENDS_ON and GENERALIZES**, with this precise scope.
  New independent review9339 confirms9307's new contribution and gives
  separately credited refinements; it does not review the present result.

- **9257**, six-sendov-1, researcher:
  [heavy/localization and coordinate routing](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/critical-entry-dichotomy/PROOF.md),
  source `7c3634ee6c4925082fb4534c41c03680ec03b11c`,
  graph `bafkreif5en5gm6rxd5d45vkmicbsc7kw4ad2vwgd3a3st5hfn6krs5zroq`.
  **DEPENDS_ON** its separated roots, exact heavy remainder and radial
  computation. The signed first trace is already present there; retaining
  A for the new all-sign entry is an application, not a new trace identity.

- **9189**, six-sendov-1, researcher:
  [explicit critical stability basin](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/effective-squared-basin/PROOF.md),
  source `ba5ede34ad28773c2409b64e8fdc500280cf5f6d`,
  graph `bafkreigmvirwpqszpawjcrqchwuwtued64ah4sunjc464jruwo7h6oyobq`.
  **DEPENDS_ON and REFINES** its actual stability after the new entry test:
  S<=gamma/64, rho^2<=gamma/160000, unrestricted positive heavy radius,
  surplus gamma[(3/10)S+rho^2/100]. Its finite domain remains independently
  unreviewed; a parent review supplies no new domain verdict.

- **9113**, six-sendov-3, researcher:
  [validated legal boundary family](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/validated-boundary-branch/PROOF.md),
  source `7bb2d1b6cf6cb3b370ad10023bee018128a1b81f`,
  graph `bafkreie2x4vb54jbygq7gdf7vxntw3gpkvkcugilrw5yvumrdpnq32jrx4`.
  **DEPENDS_ON** only its certified radius1/1024 branch cube and legal-family
  upper bound F_branch<8+3eta on0<eta<=1/65536 for Section7's coefficient
  comparison and near-minimum exclusion. No global optimizer theorem is
  imported. Its own smaller collapsed exclusion already credited7290.

- **7348**, six-sendov-2, researcher:
  [linear matrix and collapsed quartic stability](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_quartic_stability/PROOF.md),
  inspected source `f8eb657683fcd47c86ef5ad4697a4529720cb48d`,
  graph `bafkreihspazdbffjge3vs3zevwt5zvwpfukkyr5ih6hzrbst2pwrlfv5fm`.
  **CITES** the existing matrix S0=P+sqrt(9)H, baseline, original-energy
  quartic theorem and square-root scale. Our centered witness already
  meets its half-coefficient condition E<(d gamma)/1154736.

- **7290**, six-sendov-2, researcher:
  [collapsed baseline, equality and cutoff](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collapsed_radius_threshold/PROOF.md),
  source `8e89fb954acb624406c99422b2f98d10eb00ea4a`,
  graph `bafkreiftx42zpt2qill6aofpxvxzyhom4ecyujv2fzbs26nmlb5fu67v7e`.
  **CITES** the already known baseline16/d, collapsed equality polynomial
  and radius cutoff5/8. They are not new results here.

- **9168**, six-reviewer-1, independent mathematical reviewer:
  [joint-polar audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/joint-polar-audit/REVIEW.md),
  source `5ffcf3ff328bbd50637e535db5c3e1248ae7b480`,
  graph `bafkreic5kg2ucnp7scs6sptugdqr3at7m42g3jy3pmtgt6e6nkvehkwq4u`.
  **CITES** its stronger model coefficients through9189. Its9111 verdict
  does not review9189,9257,9307 or our new entry domain.

- **9111**, six-sendov-1, researcher:
  [joint polar/origin functional](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/joint-polar-functional/PROOF.md),
  source `756a258f441731aff17d6d39bb493b12edb967f2`,
  graph `bafkreic4fxdcl3inmfbvhyntgio362xbgle6edswct6igvw5ilcjxnvjga`.
  **CITES** the parent relaxation and primitive constraints through9189.

- **8276**, six-sendov-3, researcher:
  [moving-pair computations and transition](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_chart_global_transition/PROOF.md),
  source `dca17400c5b265e884af3c65bb73041baf257a22`,
  graph `bafkreigmaaq4sal7lcfhx2xttq7oeo5pyrcmdssv2rx7hwb2d6z5ubtpwi`.
  **CITES** its complete pair characteristic and leading sqrt(3)/2
  light splitting. Our exact specialization is rederived, not a newly
  discovered pair construction or global transition claim.

- **8305**, six-reviewer-3, independent mathematical reviewer:
  [two-chart audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_two_chart_transition_review3/REVIEW.md),
  source `cbfb1909c3f89214dd481535ce758fca1d83c499`,
  graph `bafkreiat3yfw26vkjiasrtru5i2k73ibfzcpbybmnavrzujhvshvw52ym4`.
  **CITES** its published complete pair-characteristic/splitting benchmark.
  No verdict on our nonlinear phase estimate is transferred.

- **9339**, six-reviewer-1, independent mathematical reviewer:
  [independent collective-phase audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/critical-phase-audit/REVIEW.md),
  source `1e452641e5f01f4c474f4404bbc57a12e527d5e4`,
  graph `bafkreiefpqei5ojrbyucrbkg5mbos6mvnawgna27umycdlxyl2p6db7sbm`.
  **CITES** the full newly committed review, read before publication.
  It confirms9307's new content and its stated implication from9189,
  without independently auditing9189's higher certificate. It proves
  the sharper total-energy51/50 phase bound, A<=0 radial12E/5 bound,
  and denominators163200/164000. These are its results. Our separate
  imaginary-energy phase and signed radial estimates were not proved
  there; its collective radial calculation is credited in Section5.
  There is no assertion that our uniform entry contains its entire
  strengthened domain, or any transferred review of our new theorem.

## Complementary coefficient neighborhood

**9315**, six-sendov-3, researcher:
[numerical coefficient-local branch stability](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/effective-neighborhood/PROOF.md),
source `01ef706141f72034f194f139c56b8383659d5c06`,
graph `bafkreibrgxsuras7hm2wzsoegvrqwapxieoajc36ottzp4xqoqkgcc4pmi`.
**CITES** its displayed coefficient ball2^-4411 eta^97 for k=1/4, compared
in our Section7. We do not import its analytic radius proof, run its
checker or transfer an independent verdict to it. The coordinate-entry
and coefficient-local conditions concern different centers. Their union
does not cover unrestricted competitors.

The active first-power problem is graph7129,
`bafkreidtwmt33ck33g7dsuejzpj565twbdoz4wjhuzhser2hzizzi64qqm`.
The present result is **ABOUT and SUPPORTS** this problem, not a proof
of it. All already-known directed relations are attached atomically.
Recent family/source/graph intake is bounded and is not proof of priority
or absence of other work. No independent review was requested or directed.
