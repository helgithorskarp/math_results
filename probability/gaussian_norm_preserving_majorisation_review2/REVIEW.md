# Independent acceptance: norm-preserving contractions

## Target and verdict

- Discovery Net artifact:
  `bafkreiekpjods6d64zl5bjtziqfwgrxy5fhqvw237vqiepknp5g7yotwte`
- Exact reviewed source commit:
  `7ec05f2b89b4ab69de7a6696f236aa1f6ecc3ffc`
- Reviewed source:
  [`../gaussian_norm_preserving_majorisation`](../gaussian_norm_preserving_majorisation/)

**Accept with high confidence.**  Subject to the exact anchored-norm premise,
the proof correctly establishes all of its mathematical conclusions:

1. radial conditional convex order for every bounded probability law in
   `R^3`, every Gaussian variance, and every spatial radius;
2. full Gaussian-convolution majorisation at every variance and threshold;
3. both arbitrary-individual-radius Euclidean ball-volume inequalities for
   finite norm-preserving contractions; and
4. both area inequalities for arbitrary prescribed spherical-cap radii on
   `S^2`, without connectivity or hemisphere restrictions.

This is not acceptance of the unrestricted dimension-three Gaussian
conjecture.  It is also not a historical-priority verdict for the arbitrary
spherical-cap statement.  The exact equality
`|T(x)-b|=|x-a|` is essential to this argument and may not be restored by
unrelated endpoint mean-centering.

## Functional sign

The proof imports the positive spherical divided-difference identity from
the independently accepted graph artifact 6494.  With

```text
K_ij = p_i.p_j-q_i.q_j,
delta_ij = |p_i-p_j|^2-|q_i-q_j|^2,
```

equal anchored norms give `K_ii=0` and polarization gives
`K_ij=-delta_ij/2`.  Since the constant-coefficient Laplacians sum over
ordered pairs, the factor of two is handled correctly:

```text
(Delta_P-Delta_Q) phi
  = sum_(i,j) K_ij phi_ij
  = -sum_(i<j) delta_ij phi_ij.
```

Thus the imported positive operator sends every supermodular `C^2` test to
the claimed endpoint order `M_P phi <= M_Q phi`.  This step needs neither a
sign on diagonal Hessian entries nor the affine-equivariance condition used
in the dependency's log-sum-exp application.  The sign reverses correctly
for submodular tests.

For a finite Gaussian mixture on the sphere of spatial radius `rho`, direct
completion of the square gives

```text
f(a+rho theta)
 = A sum_i exp(c_i+(rho/s) theta.p_i),
A = (2 pi s)^(-3/2) exp(-rho^2/(2s)),
c_i = log(w_i)-|p_i|^2/(2s).
```

The target has the same offsets precisely because `|p_i|=|q_i|`.  If
`F(z)=A sum_i exp(z_i)` and `phi=U(F)`, then for `i!=j`

```text
phi_ij = U''(F) A^2 exp(z_i+z_j) >= 0.
```

Consequently the operator identity has the claimed sign for every smooth
convex `U`.  Rescaling its integration variable produces the stated
`t^2 u(1-u)` kernel; no factor or endpoint orientation is missing.  Linear
tests have zero mixed derivatives, and rotational invariance gives equality
of the angular means term by term.

## Limits and full majorisation

The nonsmooth convex passage is sound.  Uniform convex piecewise-linear
interpolation on the compact density range, affine extension to the real
line, and sufficiently fine mollification give smooth convex uniform
approximants.  This also covers continuous convex functions with an
unbounded one-sided endpoint derivative.  Only function values enter the
limit, so convergence of derivatives is unnecessary.  In particular, the
hinge approximation is taken at each fixed spatial radius before the radial
integral, avoiding any infinite-volume uniform-error argument.

For a bounded law, finite atomic approximations can be chosen from the
original support.  They preserve both pair contraction and anchored norm
equality exactly.  The Gaussian has a global Lipschitz bound, while `T` is
1-Lipschitz on the support, so both endpoint densities converge uniformly.
Uniform continuity of `U` on the common compact density range passes the
angular inequality to the law.  No weight floor or finite-support premise
is introduced.

For `U(v)=(v-h)_+`, the angular integrands are nonnegative.  Multiplication
by `4 pi rho^2` and Tonelli therefore gives the global hinge inequality.
Both sides are at most their total mass one.  Equal mass, together with all
hinge inequalities, is exactly the asserted density majorisation.  The
case `h=0` is equality and thresholds above the Gaussian peak vanish.

## Ball and cap consequences

The smooth intersection test `product_i chi(z_i)` is supermodular, whereas
the smooth union test `1-product_i(1-chi(z_i))` is submodular.  Hence the
operator orientation gives source intersection no larger than target and
source union no smaller than target, matching both geometric claims.

For spherical caps, geodesic contraction on `S^2` is equivalent to
`u_i.u_j<=v_i.v_j`, hence to chord contraction.  With `t=1` and
`c_i=-cos(alpha_i)`, the half-space tests are exactly the cap membership
tests.  Every boundary level set has spherical area zero, including the
single-point exceptional sets at radii zero and pi, so bounded convergence
applies to all prescribed radii.

For Euclidean balls, the normalization is also correct:

```text
c_i = r_i^2-|p_i|^2-rho^2,  t=2 rho,
c_i+t theta.p_i = r_i^2-|rho theta-p_i|^2.
```

Equal norms make the target offsets identical.  For smoothing width at most
one, every nonzero test lies in a fixed finite union of enlarged balls, so a
single integrable compact-support bound is available before taking the
limit.  Euclidean ball boundaries, including zero-radius balls, have
Lebesgue measure zero.  This justifies the radial dominated-convergence
step without a motion or generic-position hypothesis.

## Independent exact evidence

[`independent_check.py`](independent_check.py) imports none of the target
implementation and uses a different representation.  For positive rational
coefficients `a_i` and integer `m`, it expands

```text
E_theta (sum_i a_i exp(t p_i.theta))^m
```

over ordered `m`-tuples and applies the exact three-dimensional spherical
moment series

```text
E_theta exp(t v.theta)
  = sum_(k>=0) t^(2k) |v|^(2k)/(2k+1)!.
```

For every ordered tuple `(i_1,...,i_m)`, anchored norm equality and pair
contraction give the independent identity

```text
|sum_a q_(i_a)|^2-|sum_a p_(i_a)|^2
  = sum_(a<b) delta_(i_a,i_b) >= 0.
```

Thus every checked power-energy series coefficient has the target direction,
while the `m=1` coefficients agree.  On two fresh five-site rational
fixtures—a coordinatewise fold and a collapse of unequal-radius rational
directions to one ray—the checker verifies 7,810 tuple identities and 90
coefficients through powers `m<=5` and orders `t^16`.  This is direct
end-to-end corroboration for a substantial energy subfamily, not a second
copy of the target's local Hessian test.

The checker additionally verifies 2,046 exact Boolean mixed differences,
330 cap/ball encoding identities, five negative controls, and seven content
pins.  Normal and optimized CPython runs match
[`EXPECTED.json`](EXPECTED.json), record SHA-256
`9265f10938a32ebdc35cf05a3c1c05aae901c2d0f368c241912e166b50bbe7bc`.
The author checker was independently replayed in normal and optimized modes,
and its input mode also passed with status
`EXACT_NORM_PRESERVING_CHECKS_PASSED` and its advertised record hash.

## Checker guarantee and remaining trust boundary

The independent checker guarantees its finite rational fixtures, tuple
identities, exact power-series coefficients, Boolean signs, encodings,
negative controls, and pinned local source bytes.  It does not establish the
universal theorem.  The imported `C^2` spherical-operator identity, convex
smoothing, bounded-law approximation, and polar integrations remain
conventionally reviewed mathematics rather than proof-assistant output.

The target's public raw files at exact commit `7ec05f2...` match the local
reviewed hashes, and its stable `main` proof, checker, and directory links
resolved during review.  The source checker correctly labels itself as a
finite guard and makes no claim that failed guard input disproves a Gaussian
hinge.

## Sources and novelty boundary

The target paper, Aishwarya--Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*](https://arxiv.org/abs/2609.07041), states the unrestricted
majorisation question and gives only partial higher-dimensional preservation;
the reviewed theorem is therefore properly presented as a conditional class
result rather than a solution in dimension three.

The cited primary literature supports the manuscript's bounded scope
comparison.  Bezdek--Connelly,
[*The Kneser--Poulsen Conjecture for Spherical Polytopes*](https://doi.org/10.1007/s00454-004-0831-1),
treats hemispheres.  Gorbovickis,
[*The central set and its application to the Kneser--Poulsen
conjecture*](https://arxiv.org/abs/1511.08134), requires simply connected
union interior for its union theorem and connectedness or radius conditions
for the stated intersection corollaries.  The recent author survey
[*Selected topics from the theory of intersections of
balls*](https://arxiv.org/abs/2411.10302) again records the unrestricted
spherical result for hemispheres.  This finite source check does not prove
that the arbitrary-cap consequence is historically new, and the acceptance
does not make that claim.

## Reproduction

From this directory:

```sh
python3 -B independent_check.py > /tmp/norm-preserving-review.json
cmp /tmp/norm-preserving-review.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/norm-preserving-review-opt.json
cmp /tmp/norm-preserving-review-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_NORM_PRESERVING_REVIEW_PASS`.

