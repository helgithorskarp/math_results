# Literature and scope audit

Agent: six-sendov-2, researcher. Checked 2026-09-29.

The original mandate asks for degree-nine Sendov. Current primary sources
cover that assertion already:

1. [Tao, A digestion of the proof of Sendov's conjecture, 12 August 2026](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
   reports a full all-degree proof and the Phelps–Rodriguez equality
   classification. Its boundary section uses the reciprocal identity.
2. [The author's formalization README](https://github.com/teorth/sendov/blob/master/README.md)
   states the quantified full-generality theorems and describes an axiom
   audit. The top-level statements were inspected; the project was not
   rebuilt here. This note does not independently certify its build.
3. [Zhang, Beyond Sendov's conjecture: the quadratic Tang–Zhang inequality](https://arxiv.org/html/2609.19126)
   explicitly records the all-degree resolution and develops a stronger
   reciprocal-square result. The complementary researcher six-sendov-1
   is pursuing the still conjectural first-power endpoint. This contribution
   instead studies boundary stability, so the two scopes are complementary.
   The near-equality hypothesis for our stronger version is the deficit
   in the boundary case of this paper's quadratic inequality. Section 8,
   Lemma 8.3 establishes the equality case; our new work quantifies it
   and controls the original roots at linear scale.

The older degree-nine claim remains a separate audit question.
[Meng, arXiv:1705.07235](https://arxiv.org/abs/1705.07235) is a 2017 proof
claim, with the latest listed revision v3 dated 17 May 2018. Its arXiv page
provides no journal reference. The bounded search did not locate a primary
acceptance record or a primary refutation. No assertion that Meng's
argument is either accepted or false follows from this search.
[The supplied large-degree seed](https://arxiv.org/html/2609.20256) reports
the older degree-at-most-eight status. That is a discrepancy in status
reporting, not a mathematical refutation of Meng. The newer all-degree
sources make resolving that historical discrepancy unnecessary for the
validity of the quantitative result proved here.

The following primary work is particularly relevant to the new estimate:

- [Tang–Zhang, Sharp Schoenberg type inequalities and the de Bruin–Sharma problem](https://arxiv.org/html/2508.10341),
  Section 5, equation (5.1) and Remark 5.1, gives the translated reciprocal
  identity and its immediate boundary Sendov application. We use this
  classical identity, with attribution, as the starting point. Neither
  the identity nor the equality classification is claimed new.
- [McCoy, A principle of O. Szász and the Sendov–Ilieff problem for polynomials near z^n−1](https://www.tandfonline.com/doi/abs/10.1080/17476939808815077)
  studies a sufficient neighborhood of regular polynomials for Sendov.
  Its accessible primary abstract was checked, but its full text was not
  available in this run. Our implication has the reverse direction:
  a boundary distance deficit controls root displacement.

Targeted searches included Sendov with “quantitative stability”,
“near-extremal”, “boundary”, “Rubinstein”, and “Schur”, as well as the
current primary sources above. No duplicate of the explicit degree-nine
linear matching theorem and sharpness family was found. This supports
only “not found in the searched sources”, not a claim of priority or an
exhaustive literature review. The numerical constants are not optimized.
