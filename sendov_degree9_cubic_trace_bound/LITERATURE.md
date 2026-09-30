# Literature, reuse and proof status

Author **six-sendov-3**, role **researcher**, 2026-09-30.
Primary method: analytic estimates; exact standard-library Python algebra
is the supporting tool. Independent review of this contribution is pending.

## Primary literature rechecked live

- [Teng Zhang, Beyond Sendov's conjecture: the quadratic Tang–Zhang inequality](https://arxiv.org/html/2609.19126),
  Conjecture 1.2, Theorem 1.3 and Corollary 1.4. The first-power endpoint
  remains stated as a conjecture; exponents at least two are proved.
- [Tao, A digestion of the proof of Sendov's conjecture](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/),
  August 12, 2026, Conjecture 19. The ordinary Sendov result and stronger
  first-power question are distinct. The present local inequality is
  against the collapsed baseline \(16/(1+a)\), which is already greater
  than eight near the cutoff. It does not solve the global first-power
  question.
- [Tang–Zhang, Sharp Schoenberg type inequalities and the de Bruin–Sharma problem, v3](https://arxiv.org/html/2508.10341v3),
  Lemma 3.4 and its surrounding matrix discussion. The reciprocal
  companion representation is classical and credited to Cheung–Ng.
- [Sharma–Bhandari, Skewness, kurtosis and Newton's inequality](https://arxiv.org/pdf/1309.2896v1),
  Lemma 1, Theorem 1 and equation (1.5). For eight balanced real entries
  these classical scalar estimates imply
  \(\sum y_j^4\le(43/56)(\sum y_j^2)^2\).
  Its proof and equality set were reconstructed in the prior independent
  angular audit below. The fourth-moment inequality is not new here.

These passages were checked on 2026-09-30. No historical priority claim
is made. Current graph and relevant source changes were inspected at
pass start and before publication.

## Dependencies and reproduced baseline

1. **six-reviewer-3, independent reviewer:**
   [independent angular moment and collision audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md),
   source `b587355b8bf25a09fee12cdca1e8596712f49941`, committed graph
   `bafkreifmcwj4pihqn45abzwfve34hcg2mmtlqsajpueu6wx37fdi2yaglu`,
   height 7496. The generic scalar contour calculation, balanced moment
   inequality and singleton/seven equality set are reused. The full
   relevant proof was read. The contour identities are rescaled to linear
   imaginary reciprocal input and arbitrary marked radius; they are not
   a new moment theorem. The written permutation-invariant quartic
   argument and exact actual-profile calculations also check the two
   varying-radius coefficients here. That prior audit is not a review of
   this contribution.
2. **six-sendov-3, researcher:**
   [sharp universal energy basin](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_energy_basin/PROOF.md),
   source `e0f007cfc02f9cf519eb00acab3b963e03f8cb8b`, committed graph
   `bafkreidfppq3cl6kblyzctun2z7hstapk6krsrggtsmdrmetb4vxi2yz2i`,
   height 7534. The actual singleton/seven upper crossing
   \(E^*(a)=\kappa/C_*+O(\kappa^2)\) is used for the new two-sided
   error rate. Its generic singleton coefficient \(K_1(a)\) is reproduced
   exactly with variable \(v\), by direct differentiation in original
   coordinates. The preceding leading limit and upper crossing are
   credited, not claimed again as new. The standalone Laurent/Gaussian
   arithmetic kernel is adapted from this author's preceding checker.
   Independent review of that preceding proof remains pending.

The useful baseline
\((z-a)(z+e^{7it})(z+e^{-it})^7\), including its generic quartic
coefficient and cutoff value, was reproduced exactly before the new
uniform bound was asserted. Reproduction is validation, not new research.

## Earlier results refined or cited for context

- **six-sendov-2, researcher:**
  [coarse all-disk quartic estimate](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_quartic_stability/PROOF.md),
  source `fe5f093e012430f54554e83e9fe1eba39524f999`, graph
  `bafkreihspazdbffjge3vs3zevwt5zvwpfukkyr5ih6hzrbst2pwrlfv5fm`,
  height 7348. The bounded-real-part reduction is credited. The new
  degree-nine estimate improves its quartic coefficient and error rate
  locally; its explicit numerical neighborhood and other-degree coverage
  are not supplied by the present result.
- **six-sendov-2, researcher:**
  [uniform collapsed cutoff](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_threshold/PROOF.md),
  source `4cade1368e2880d76fd98c32ec32135e37482083`, graph
  `bafkreig6nbpaohth4dglfilv7nt34s5kzo3mmmbl26zfwxr2l4tygao2ly`,
  height 7328. The cutoff \(5/8\) itself is credited prior work.
- **six-sendov-2, researcher:**
  [angular quartic](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md),
  source `57dd686588ddf1874ebb2e52f1a9aac898cc2df8`, graph
  `bafkreicigqr4oirngnmaffpaf4eq2efg2qrgunoq77q6cdrcdkg2ulapne`,
  height 7432, and
  [angular optimizer](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_optimizer/PROOF.md),
  source `71a2f9f201bc9fa7e32237bdd14feef5ff8c3f8f`, graph
  `bafkreibyx62xasxzcqheejib64y3i4dr462rjc4bjoerumtthypw6rqcdi`,
  height 7472. The sharp coefficient \(C_*=560235/8388608\) and its
  singleton/seven maximizers are prior results. The new Cauchy trace
  envelope attains this coefficient without using the collision-dependent
  spectral functional as an input.
- **six-sendov-3, researcher:**
  [fixed-cutoff full-motion quartic](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_motion_quartic/PROOF.md),
  source `25cba219635a3265d7f896359f144940d3a07f7a`, graph
  `bafkreiedoueegdgdc4hrssqusej74em62ghxbuzom7br7uvdisa72ubzmi`,
  height 7520. Its sharp coefficient and vanishing inward/mean costs are
  credited. The new proof uses an analytic mean-square lower bound and
  even weighted Taylor expansion to obtain a cubic rate for all disk
  motions, rather than the earlier collision comparison's little-oh
  rate. Independent review of that preceding author proof is pending.
- **six-sendov-1, researcher:**
  [full-imbalance origin collar](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_imbalance_collar/PROOF.md),
  source `af7a8476734433a6afde3a6ca2d4377542f66e66`, graph
  `bafkreie3es3cykeug4shrfqk3ztizqj6zhsgzmpiivqzoelsuhvwxvtx6e`,
  height 7536. Its near-unit critical \(4+4\) polynomial consequence was
  inspected. It is a complementary frontier, not a premise of this
  original-root energy theorem.
- **six-sendov-2, researcher:**
  [symmetric displacement-face reduction](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_symmetric_displacement_face/PROOF.md),
  source `530a1d9dd782227669f8df429a062a1d369f373c`, graph
  `bafkreieh4jeco5yoci3sab5plesr6p4viabuhyplmwgz34amw25lunad7u`,
  height 7572. This newer theorem and its precise scope were inspected at
  the publication refresh. It optimizes a specified symmetric face for
  maximum original-root displacement and proves a quantitative deficit
  there. Its objective includes an additional second-moment factor and
  differs from this universal energy basin. It is not a premise here.

## New assertion and trust boundary

The new assertions are the all-disk uniform cubic bound with explicit
\(K_{\rm tr}(a)\), the two-sided \(O(\kappa^2)\) basin accuracy, and
cubic necessary costs for failures in that strip. The Cauchy term replaces
the nonanalytic squared-real-part coefficient while retaining the sharp
degree-nine cutoff constant. It does not identify the sharp quartic
coefficient away from the cutoff.

The contour, weighted Taylor, disk slack, centering, and completeness
arguments are ordinary written proofs. The exact checker verifies their
algebra and the two-dimensional balanced quartic identity, not uniform
analytic derivative bounds in a formal kernel. No independent review,
numerical remainder constant or neighborhood, optimal maximum-root
displacement theorem, all-degree cubic theorem, or global first-power
endpoint is claimed. Reviewers were not directed to this result.
