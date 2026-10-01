# Literature, dependencies and exact evidence boundaries

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
The following primary passages were checked live before the claim.

- [Teng Zhang, Beyond Sendov's conjecture: the quadratic Tang--Zhang inequality](https://arxiv.org/html/2609.19126),
  Conjecture 1.2, Theorem 1.3 and Corollary 1.4. The strongest first-power
  endpoint remains proposed; the proved quadratic statement gives powers
  at least two. Our finite-energy stability theorem does not settle the
  unrestricted first-power assertion.
- [Terence Tao, A digestion of the proof of Sendov's conjecture](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/),
  Conjecture 19, distinguishes that stronger reciprocal-power problem
  from ordinary Sendov.
- [Sharp Schoenberg type inequalities and the de Bruin--Sharma problem](https://arxiv.org/html/2508.10341v3),
  Lemma 3.4, records the Cheung--Ng critical matrix formula. Our complete
  reciprocal characteristic is also derived directly from the actual
  degree-nine polynomial.

Targeted live literature queries and bounded committed graph/source
inspection were performed. No exhaustive literature search or historical
priority claim is made. Matching known source output is validation,
not a new result or an independent review.

## Direct inputs and original credit

- **7328**, actual **six-sendov-2**, researcher:
  [moving-pair construction PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_threshold/PROOF.md).
  Verified original source commit
  `4cade1368e2880d76fd98c32ec32135e37482083`;
  graph `bafkreig6nbpaohth4dglfilv7nt34s5kzo3mmmbl26zfwxr2l4tygao2ly`.
  The actual Q polynomial and its exact energy retain this original
  author's credit. Section 2 of our proof rederives the pair identity
  directly as preparation for the new energy-transfer calculation.
- **8276**, actual **six-sendov-3**, researcher:
  [moving-pair two-chart PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_chart_global_transition/PROOF.md).
  Source `dca17400c5b265e884af3c65bb73041baf257a22`;
  graph `bafkreigmaaq4sal7lcfhx2xttq7oeo5pyrcmdssv2rx7hwb2d6z5ubtpwi`.
  Sections 4--6 supply the full fixed-energy Q chart, separated
  five-critical group, normalized analytic harmonic support, defect
  through collisions, exact stationarity, and limiting mean/inward
  coefficients. Its leading split coefficient and radius a_- are credited
  inputs. Its support construction is valid near a_- independently
  of the sign of the leading split coefficient; its positive local
  theorem itself has domain compact subsets of `(a_-,a_+)`.
  The present positive-side theorem uses the support and replaces that
  theorem's leading positivity argument by the exact finite-energy sign.
  Its exact a_- endpoint status was expressly left open. Independent
  review 8305 now confirms 8276; review of this extension is pending.
  The new endpoint descent
  and scalar stability curve are direct polynomial derivations and do
  not assume that support.
- **8305**, actual **six-reviewer-3**, independent mathematical reviewer:
  [two-chart transition REVIEW.md](https://github.com/helgithorskarp/math_results/blob/main/sendov_two_chart_transition_review3/REVIEW.md).
  Source `cbfb1909c3f89214dd481535ce758fca1d83c499`;
  graph `bafkreiat3yfw26vkjiasrtru5i2k73ibfzcpbybmnavrzujhvshvw52ym4`.
  Fresh review inspected in full, including its committed graph body,
  before this publication. It independently confirms all five 8276
  theorems and their analytic bridges with 165 exact identities. It also
  proves a compact-uniform classification on `(a_-,1]`, a two-chart true
  global excess law and a complete positive fourth-order angular loss
  on the one opposite-pair split curve at a_-. Those improvements retain
  the reviewer's credit and are not republished as our results. Its
  finite-energy a_- endpoint is explicitly open. The new derivative
  and true finite-energy curve remain outside that review's verdict.
  The executable independent evidence was not freshly replayed here.

## Reviewed antecedents and scoped refinements

- **8160**, actual **six-sendov-3**, researcher:
  [moving-pair comparison boundary PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_moving_pair_comparison_boundary/PROOF.md).
  Source `5741f9d5651644598d0d685599b9e95b79d5d069`;
  graph `bafkreifg47qbe67ligskpxi32jy6myeuooqrmsms6sadtcurgnr3kzcsd4`.
  Its complete Q cubic and two-family comparison were independently
  confirmed by 8230. The global equal-value curve near a_G is distinct
  from the lower split-stability curve here.
- **8230**, actual **six-reviewer-3**, independent mathematical reviewer:
  [moving-pair threshold REVIEW.md](https://github.com/helgithorskarp/math_results/blob/main/sendov_moving_pair_threshold_review3/REVIEW.md).
  Source `c1f303ddef9e7d19d839455ba829cd0bcc8b7db0`;
  graph `bafkreifuvcaf4xx6ml63ldtrwwmlae65qdb2lto5hyaqcz6lkevboysrjm`.
  It confirmed 8160, strengthened a spectral Gram consequence, and
  proved the sufficient closed leading angular Q interval `[a_-,a_G]`,
  including uniqueness at a_-. That leading optimizer and all such
  improvements retain the reviewer's credit. This review did not prove
  actual finite-energy Q minimality at a_- or inspect the correction here.
- **8212**, actual **six-sendov-3**, researcher:
  [sharp-radius full-disk PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_radius_global_minima/PROOF.md).
  Source `aa48e0abbe1ab5fa080d4f653b8696f7d46db972`;
  graph `bafkreienkebe5vry36bkcptomxbbeo3ybilnnujblvl6ksmuilopefcpv4`.
  Its full-disk bootstrap and quartic reduction were independently
  confirmed by 8258. They underpin 8276, but no global-entry theorem
  from a shrinking degenerate chart is assumed in the present result.
- **8258**, actual **six-reviewer-3**, independent mathematical reviewer:
  [sharp global-radius REVIEW.md](https://github.com/helgithorskarp/math_results/blob/main/sendov_sharp_global_radius_review3/REVIEW.md).
  Source `a51751eed3e3c0a0c16af714b9b1b176de348a2e`;
  graph `bafkreicjon3wz6u76csgkgoc3xc6bcww3q43dzkxpuzlckuwryrypzpoz4`.
  It confirmed 8212 and proved evaluated quadratic minimum asymptotics
  and uniform leading Q geometry on the closed angular interval.
  This is compatible with actual Q instability at a_-: leading geometry
  does not specify the exact finite-energy minimizer. Its verdict does
  not cover 8276 or the present theorem.

The 8276 full mandatory fixture was reproduced before this derivation:
79 identities, ten strict signs, all eight linear-compression basis
inputs, six literal matrix moments, seven damaged expressions and
all 50 complete records, record SHA256
`0477c3f7d30ab4472ea742fb4616a958e6ccbb4e05e709e6c02a6c0e8bea0ec1`.
The run took 0.202 seconds and peak child RSS 18340 KiB.
This is baseline validation, not independent mathematical review.

## Complementary context inspected

New **six-sendov-1**, researcher, source
`a275b756a822eabb1ea528076cbfd4f1621af755`,
[full reflected-light first power](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_reflected_light_mean_first_power/PROOF.md),
proves its critical `6+1+1` reflected-light class and a specified complex
center tube. Its written source was read in full; its executable was
not replayed and it is not a premise of this original-root stability
claim. The later literature-credit commit
`f93b9864c4519deb005dffa2e6a4c40982af1b20` preserves that separation.
Its committed graph contribution is **8291**,
`bafkreiawvvn53q3zhhwjalbmajxrjk24e3lrmcthuotdehq4eybddjocrm`.

The prior **six-sendov-2**, researcher,
[saturated-triple displacement source](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_saturated_triple_displacement/PROOF.md),
commit `bb485c46b9781979f06c50ca0949ba6f1d3a8c2e`, graph 8236
`bafkreih2liynxhmb4t3n7npphjn7bophvnqfof6hliewtqg6u5se7la2rq`,
is complementary collapsed angular/displacement work, not a premise
or independent review. No peer or reviewer was directed to a task.
The later attribution correction
`179b41b89efefdcb4923b8a09b6c76b29206b271` was inspected and credits
the balanced angular formula correctly to six-sendov-2. The uncommitted
six-level one-triple draft reported by that researcher is not a premise.

## What the new exact source checks

The self-contained `verify.py` checks the actual opposite-pair reciprocal
transform and energy, all eight original and critical multiplicities,
the full quintic perturbation and separated-factor derivative,
the far cubic root and positive modulus expansions, every coefficient
of h1/h2, the exact lower-endpoint reduction and stability-curve slope,
and the remaining positive mean/inward signs. Every full record is
compared with the mandatory compact fixture. All exact arithmetic is
standard-library CPython 3.11.2; there are no private inputs, finite
search-completeness assumptions or floating-point sign premises.

The ordinary analytic bridges and support dependency are explicitly
identified in PROOF.md. Independent review of the new result is pending.
The shifted zero-Hessian curve's quartic behavior and the lower global
minimizing branch are the next frontier; a_- itself is now proved unstable.
