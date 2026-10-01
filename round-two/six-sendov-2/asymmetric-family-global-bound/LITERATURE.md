# Status, dependencies and prior art

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Current primary status was refreshed live during this pass.

[Zhang, Beyond Sendov's conjecture: the quadratic Tang--Zhang inequality](https://arxiv.org/html/2609.19126)
states the strongest first-power endpoint in Conjecture1.2. Theorem1.3
is quadratic, with powers at least2 in Corollary1.4. Ordinary Sendov is
reported resolved. Our degree-nine target remains first power and nearby
rigorous original-root angular/stability structure; this theorem gives
no finite-energy or full endpoint conclusion.

The exact prerequisite is
[8753: sharp three-level ratio, full-sphere local stability and finite attained transition](../angular-three-level-transition/PROOF.md),
source6efce877eb9dcde6e12b6a90930d65382b29dd89. The new proof inherits its
continuous uniform extension16 and its sharp three-level bound/equality
classification. Partition-specific boundary estimates are also in that
source. These were complete ordinary author proofs and independently
unreviewed at the initial refresh. That status is not upgraded merely
by using them. The new stationary reduction and universal asymmetric
formula are independently verified here. The basic rational polynomial
routines are adapted with attribution from its standalone checker.

Additional credited campaign prior art:

- [7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
  and [review7496](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md)
  establish the balanced angular framework, full eigenspace conventions
  and collision continuity. The moment identities are elementary spectral
  linear algebra, not a newly invented method.
- [7940](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_level_displacement/PROOF.md),
  sourceb4615bc31642df64a3a4a6d83d31882935103b9a, develops quotient-companion
  algebra and a four-level restriction for a DIFFERENT displacement
  objective. Its optimizer does not imply the present negative-parameter
  ratio bound. The technique is credited; the new claim is the sharp
  ratio on the entire asymmetric family.
- [8672](../triple-angular-persistence/PROOF.md),
  source4587f5f3776a0ec8c22d43ec8b264c8b48915218, proves the sharp208/9
  comparison only on the symmetric triple-pair slice, along with other
  persistence/stability statements. Equation8 rechecks the exact slice
  comparison; no universal208/9 assertion is attributed to8672.
- [8702](../asymmetric-angular-obstruction/PROOF.md),
  source9b33444a3e8478d3f056b615caf499525cfcd524, disproves the universal208/9
  extension and explicitly leaves the sharp all-sphere constant open.
  Its compact witness lies in the family studied here. This new upper
  bound is compatible with every published obstruction.
- [Independent review8749](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/angular-obstruction-audit/REVIEW.md),
  source014505f0875998063a69c687b7c20d1d50432fb7, confirms8702 and supplies
  stronger exact benchmarks. It is credited as prior evidence and is
  not a verdict on8753 or the present theorem.
- [8160](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_moving_pair_comparison_boundary/PROOF.md)
  and [review8230](https://github.com/helgithorskarp/math_results/blob/main/sendov_moving_pair_threshold_review3/REVIEW.md)
  give the radius interpretation of the affine angular functional
  `J_R=RX-eta`. The present family ratio theorem is self-contained once
  its stated8753 prerequisite is inherited and asserts no new disk
  asymptotic reduction.

SymPy1.14.0 exploration produced a factored stationary resultant in
under3seconds, with all native threads one. The theorem relies on the
independent sparse-Q and fraction-free determinant checker, not that
exploratory output, a floating optimization or a presumed exhaustive
search. The full unconstrained Cstar and other four-or-more-level
multiplicity patterns remain unresolved. No historical-priority claim,
peer's unpublished input or requested reviewer verdict is involved.
