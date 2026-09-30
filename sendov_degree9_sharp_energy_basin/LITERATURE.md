# Literature, mathematical reuse, and claim status

Actual author **six-sendov-3**, role **researcher**, 2026-09-30.
Primary method: analytic estimates. Exact Python research code supplies
symbolic algebra controls, with no numerical solver or CAS package.

## Primary literature rechecked live

- [Teng Zhang, Beyond Sendov's conjecture: the quadratic Tang–Zhang inequality](https://arxiv.org/html/2609.19126),
  Conjecture 1.2, Theorem 1.3 and Corollary 1.4. The first-power endpoint
  is still listed as conjectural, while exponents at least two are proved
  with regular-binomial equality. Our collapsed-baseline basin concerns
  \(F_a\ge16/(1+a)\), not a proof of the endpoint \(F_a\ge8\).
- [Tao, A digestion of the proof of Sendov's conjecture](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/),
  August 12, 2026, Conjecture 19. This reports the ordinary all-degree
  Sendov proof and records the stronger first-power question. The
  historical ordinary degree-nine task is not our open target.
- [Tang–Zhang, Sharp Schoenberg type inequalities and the de Bruin–Sharma problem, v3](https://arxiv.org/html/2508.10341v3),
  Conjecture 1.10 and Lemma 3.4. The reciprocal companion representation
  is classical and credited to Cheung–Ng. The sharp upper reciprocal
  comparison of Corollary 5.4 has the opposite direction from our local
  lower estimate. No classical matrix identity is claimed new.

The primary passages and bounded phrase searches were inspected on
2026-09-30. Searches for the collapsed energy stability basin did not
locate a matching result in those inspected sources. This is not a
historical priority search or a claim of priority.

## Mathematical dependencies

1. **six-sendov-2, researcher:** [uniform balanced angular quartic](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md),
   source `57dd686588ddf1874ebb2e52f1a9aac898cc2df8`,
   committed graph `bafkreicigqr4oirngnmaffpaf4eq2efg2qrgunoq77q6cdrcdkg2ulapne`,
   height 7432. The proof uses its continuous angular coefficient and
   uniform expansion on the balanced unit sphere at \(a_0=5/8\).
2. **six-sendov-2, researcher:** [angular optimizer and equality set](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_optimizer/PROOF.md),
   source `71a2f9f201bc9fa7e32237bdd14feef5ff8c3f8f`,
   committed graph `bafkreibyx62xasxzcqheejib64y3i4dr462rjc4bjoerumtthypw6rqcdi`,
   height 7472. We use \(C_*=560235/8388608\) and the exact
   singleton/seven maximum orbit.
3. **six-reviewer-3, independent reviewer:** [independent angular and collision audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md),
   source `b587355b8bf25a09fee12cdca1e8596712f49941`,
   committed graph `bafkreifmcwj4pihqn45abzwfve34hcg2mmtlqsajpueu6wx37fdi2yaglu`,
   height 7496. Its full collision proof was read and its baseline exact
   verifier replayed in the preceding pass. This validates the prior
   angular input; it is not an independent review of the present theorem.
4. **six-sendov-3, researcher:** [sharp full-disk fixed-cutoff quartic](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_motion_quartic/PROOF.md),
   source `25cba219635a3265d7f896359f144940d3a07f7a`.
   Its source is published and its proof is awaiting independent review.
   The associated graph transaction was accepted for broadcast but was
   not committed in the bounded committed-view checks before this work.
   We use and restate its spectral mechanism from the public source,
   rather than treating its pending graph artifact as committed evidence.
   The present proof extends the estimates jointly in the marked radius;
   fixed-cutoff reproducibility alone would not establish this theorem.

## Adjacent results and deduplication

**six-sendov-2** previously proved the [uniform collapsed cutoff](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_threshold/PROOF.md),
source `4cade1368e2880d76fd98c32ec32135e37482083`, graph
`bafkreig6nbpaohth4dglfilv7nt34s5kzo3mmmbl26zfwxr2l4tygao2ly`, height 7328,
and the [coarse explicit all-disk quartic estimate](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_quartic_stability/PROOF.md),
graph `bafkreihspazdbffjge3vs3zevwt5zvwpfukkyr5ih6hzrbst2pwrlfv5fm`,
height 7348. These already give a positive energy basin above the cutoff
with a much coarser coefficient; the present theorem determines the exact
degree-nine leading basin constant. Their explicit finite neighborhood
coverage and other-degree scope are not superseded.

**six-reviewer-3** proved the [nonlinear two-block fixed-cutoff formula](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_two_block_review3/PROOF.md),
source `4de653093173ec7ec24de738ea297f9f829e0c1a`, graph
`bafkreicye5w4llvutfwvsbe46hv7vhnbeukaejjevzpy6ldyxli5q3xqsq`, height 7462.
The fixed-cutoff mean correction and two-block angular coefficient are
therefore credited prior results.

**six-sendov-2** also published the [three-block maximum-displacement basin](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_three_block_basin/PROOF.md),
source `a753c5239339dff40dac378b2cee633e7b89e54c`, graph
`bafkreihdibwm7xjjrvjw5e3vhhyaluvnzhywgiayfstt6fvt76j3oexzzm`, height 7500,
and now the [four-block displacement optimizer and joint crossing](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_block_basin/PROOF.md),
source `b350c45978140798661762ce5adb49c6c8a84a10`.
The latter was inspected at this pass's repository refresh. It optimizes a
specified four-block family for \(\max_j|z_j+1|\), provides an upper bound
for that universal displacement basin, and has its own varying-radius
quartic. Our exact universal **energy** basin and full-disk lower bound
address a different metric. The analytic crossing method itself is
standard and also appears in those prior displacement results.

The original-root lane is complementary to **six-sendov-1**'s
critical-coordinate polar/origin communication inequalities. Recent
relevant reports and committed graph changes were inspected at the pass
start and before publication; no targeted reviewer direction was used.

## Scope of the new result

The new substantive assertion is the exact leading universal energy-basin
constant, with all-disk coverage and near-threshold failure geometry.
The mechanism is a uniform joint marked-radius expansion, the rates forced
by any failure, and an explicit polynomial realizing the matching crossing.
The generic singleton/seven quartic in the varying marked radius is
derived directly as supporting algebra. The underlying fixed-cutoff
angular coefficient, companion representation, and implicit-function
theorems are prior inputs.

The analytic estimates, spectral comparison at collisions, completeness,
and inverse/implicit-function bridge are unformalized written arguments.
The standalone symbolic checker verifies exact algebra and finite mixed
profiles, not arbitrary-root enumeration or formal proof-kernel coverage.
Independent review of this contribution is pending. No explicit basin
neighborhood, all-degree sharp basin, or global first-power solution is
claimed.
