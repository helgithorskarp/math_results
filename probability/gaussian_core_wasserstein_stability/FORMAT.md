# Exact family-certificate format

`INPUT.json` uses schema `core-wasserstein-family-input-v1`.
Coordinates and scalars are integers or exact rational strings; floats and
booleans are rejected in numerical input fields. No approximate tolerance is used.

- `core_stages`: at least two stages, each with the same k>=2 core labels in R3.
- `background_vertices`: a nonempty rational list V. Every point of conv(V)
  is fixed at every reference stage. Vertices need not be distinct or extreme.
  **These are geometric data, with no attached positive mass requirement.**
- `step_guards`: one `norm`, `straight` or `orthogonal_lift` guard per link.
  Norm guards include two anchors. Straight and lift guards are verified
  by their respective endpoint derivative or affine-rank predicates.
- `comparison_radius`: integer R>=1 for the initial source and all N anchors.
- `endpoint_centers`, `endpoint_radius`: translations and integer Re>=1 for
  the source core and the target envelope. The whole reference source must
  satisfy R, but only its core is required to satisfy Re.
- `mass_exponent`: ell>=0. Each **core** weight is at least 2^-ell; their sum
  is at most one. Remaining mass is any measure on conv(V). Nonemptiness
  requires k<=2^ell, not k+len(V)<=2^ell.
- `variance_ratio`: rational S>=1, giving the normalized interval [1,S].
- `width_witness`: the reused nested-hulls/rational-cap guard. It has k+len(V)
  containment rows, one per final core point and background vertex. Each row
  has k nonnegative entries summing to one and representing that centered
  target point in the **initial core** hull. `source_witness` indexes a core
  point. `perpendicular_bits` controls upward square-root rounding only.
- `endpoint_anchor_obstruction`: optional length-k left-kernel dual with
  a nonzero squared-norm residual. It is not a prerequisite for the theorem.

`CERTIFICATE.json` stores the separate core and all-geometry loss sums.
**Only the former enters the uniform loss floor.** It also stores transverse
upper bounds, the support-width lower bound, target-thickening exponent
b_rho, and all-threshold transport-budget exponent B. Huge powers 2^B
are never expanded. `verify.py --input I --certificate C` checks inequalities,
so safe larger exponents or smaller positive bounds are permitted provided
all dependent schedule and conclusion fields remain consistent.

The result applies to arbitrary actual probability laws of finite first
moment when W1(mu,mu')+W1(nu,nu')<=2^-B and
supp(nu') is contained in the certified target hull plus B(0,2^-b_rho).
There is no actual source support bound. **Membership in these two guards
must be supplied by the consumer**: this format does not encode an arbitrary
measure, solve optimal transport, or verify its support. For finite laws,
a coupling of certified cost suffices in place of exact optimal W1 values.

Malformed inputs or violated guards exit nonzero. Failure of a sufficient
guard means unresolved, never an adverse Gaussian hinge. No analytic import
is formalized by this record, and a valid record is not independent review.
