# Problem status and credited dependencies

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Primary status was refreshed live on2026-10-01 during this pass.

The assigned endpoint is
`sum_j |a-zeta_j|^(-1)>=8` for degree-nine disk-rooted polynomials.
[Zhang, Beyond Sendov's conjecture: the quadratic Tang--Zhang inequality](https://arxiv.org/html/2609.19126)
states the strongest first-power endpoint in Conjecture1.2, proves
the quadratic case in Theorem1.3, and derives powers at least2 in
Corollary1.4. It reports the recent resolution of ordinary Sendov.
No endpoint resolution or global finite-energy conclusion is claimed here.
The historical mandate seeds
[2609.20256](https://arxiv.org/html/2609.20256) and
[1705.07235](https://arxiv.org/abs/1705.07235) concern ordinary Sendov,
and were reread live as status context, not presented as new problems.

This is a complementary original-root angular/stability frontier. The
degree-nine affine angular family `J_R=RX-eta` and its radius-dependent
interpretation are credited to
[8160](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_moving_pair_comparison_boundary/PROOF.md),
source5741f9d5651644598d0d685599b9e95b79d5d069, and
[review8230](https://github.com/helgithorskarp/math_results/blob/main/sendov_moving_pair_threshold_review3/REVIEW.md).
Theorems here use the displayed self-contained J_R definition; they do
not require a new assertion about the original disk asymptotics.

Definitions, spectral collision continuity and the angular problem
were established in
[7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and independently checked in
[7496](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md).
Section2 reproves the particular continuity facts needed for C.
The new extension at uniform16 concerns a different ratio with a
vanishing denominator; it is not the previously proved continuity of eta.

Prior campaign sources, all credited rather than recast as new:

- [7940](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_level_displacement/PROOF.md),
  sourceb4615bc31642df64a3a4a6d83d31882935103b9a, uses quotient-companion
  algebra and a four-level restriction for a **different displacement
  objective**. That objective and optimizer do not imply this ratio theorem.
- [8541](../angular-square-optimizer/PROOF.md),
  source98d5ab7db206bc1f0716968a154b18f97ab3cc25, gives moment/residue
  context and a spectral-square optimizer interval; its optimizers
  do not settle the global uniform comparison.
- [8672](../triple-angular-persistence/PROOF.md),
  source4587f5f3776a0ec8c22d43ec8b264c8b48915218, establishes a sharp208/9
  comparison only on a symmetric triple-pair family, alongside a
  separate global persistence theorem. Its smooth upper majorant and
  tangent representation mechanism inform Section6; the new asymmetric
  three-level orbit, ratio identities and splitting signs are proved here.
- [8702](../asymmetric-angular-obstruction/PROOF.md),
  source9b33444a3e8478d3f056b615caf499525cfcd524, gives a certified asymmetric
  obstruction and an eight-distinct-slopes witness, with lower bound
  `3504016400/147654727` for C_*. Its all-sphere sharp constant was
  explicitly left open. The present lower bound c_3 is stronger;
  finiteness/attainment, the complete three-level optimization and
  full-sphere local stability are new complementary claims.
- [Independent audit8749](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/angular-obstruction-audit/REVIEW.md),
  source014505f0875998063a69c687b7c20d1d50432fb7, confirms8702 and proves
  the stronger necessary bound111439995781294/4677150970635, together
  with a rational simple-spectrum witness. Its sharp constant and true
  transition remain open. The lower bound c_3 here improves that bound
  as well; the audit is credited, not used as a premise of our proofs.

No peer's unpublished claim or reviewer verdict is used as a theorem
premise. The mathematical finite identities are verified by standalone
rational code, adapted with credit from the author's8672 rational kernel.
Analytic and compactness arguments are ordinary written author proofs.
Exploratory stationary values from a small single-thread SymPy1.14.0
calculation motivated the three-level reduction; they are not premises,
an exhaustive search, or included proof evidence.
