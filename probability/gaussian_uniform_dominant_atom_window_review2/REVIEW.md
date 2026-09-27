# Independent acceptance: uniform dominant-atom Gaussian middle signs

## Verdict

**Accept for correctness in the stated scope.** Let a probability law have an
atom of mass `1-alpha`, with all remaining support within radius `R` of that
atom, and let its image be any anchored contraction. At Gaussian variance
`s`, put `rho=R/sqrt(s)` and let `d` be normalized mean pair-distance loss.
For every finite `L>0`, the target's explicit positive `alpha_*(rho,L)`
correctly guarantees

```text
H(u) >= u d exp(-5rho^2)/(6 sqrt(pi))
              *(-log(u)-2alpha)_+^(3/2) >= 0
```

for every `exp(-L)<=u<=1`. There is no covariance floor, atom-count bound,
minimum rare weight, or positive lower bound on `d`.

At unit variance and radius one, `alpha<=2^-21` consequently signs every
`u>=2^-11` and gives `H(u)>=2^-24 d` throughout
`[2^-11,1/4]`. This is a genuine complement to the accepted full-rank
small-loss theorem: dominant-atom laws may have collapsing covariance and
the certificate remains normalized by arbitrarily small actual loss.

The exact target is Discovery Net artifact
`bafkreihlsbbnbcpgyx5aelqr5mnh7tozv4amt7f5qmkpqrhxeqd4yde32m` at source
commit `a86e9ef2f7a4a3951e8d2214c2c4a52b9bf045d0`. All six target files are
content-pinned in `TARGET_INPUTS.json`. The author checker passes in normal
and optimized modes; its expected record has SHA-256
`8ef13a64c7aa1e827267b9f3cb126a67cec58d93de86a9e49d43f2d0bce8c338`.

This theorem does not sign thresholds below the displayed floor, cover
general prior weights, prove unrestricted dimension-three Gaussian
majorisation, or imply a Kneser--Poulsen result. No overlap with a separate
low-threshold certificate is established. Historical novelty was not
exhaustively checked.

## Local Abel identity

After scaling to variance one, the lifted interpolation in six dimensions
has potential `V_t=-log Q_t` and nonnegative loss kernel `h_t`. The credited
replica identity gives integer Laplace moments of `H`. For

```text
Phi(ell)=exp(ell)H(exp(-ell)),
Psi(ell)=integral_0^ell (ell-v)Phi(v)dv,
```

two integrations contribute `k^-2`, converting the replica factor
`sqrt(k)/(32pi^3)` into `k^(-3/2)/(32pi^3)`. The Laplace transform of
`(ell-V)_+^(1/2)` contributes `Gamma(3/2)=sqrt(pi)/2`, so the coefficient
`1/(16pi^3 sqrt(pi))` in the local primitive identity is exact.

Equality at all integer Laplace parameters is sufficient here. Under
`u=exp(-ell)`, the difference multiplied by `u` is integrable on `[0,1]`
and has all polynomial moments zero; polynomial density and continuity then
give pointwise equality. This does not assume global convexity or regularity
outside the finite level interval.

On each strictly convex local sublevel, polar coarea gives `A_t(w)`. Its
modal behavior `A_t=O((w-v_t^*)^2)` and
`A_t'=O(w-v_t^*)` removes boundary atoms and justifies two differentiations.
The resulting Abel kernel has coefficient `1/(32pi^3 sqrt(pi))`. The
independent checker reconstructs both `1/32` normalizations and the final
`1/6` margin coefficient exactly.

## Uniform posterior geometry

Factoring out the dominant Gaussian writes

```text
Q(z)=exp(-|z|^2/2)p(z).
```

The Hessian of `log p` is the posterior covariance. On the required ball it
is bounded by

```text
delta=2 alpha R^2 exp(RW) <= 1/P.
```

Thus `(1-delta)I<=D^2V<=I`. Every stationary point lies in the radius-`R`
ball, so strict convexity on the larger controlled ball gives one global
minimum. Its value is at most `-log(1-alpha)<=2alpha`; all sublevels needed
for `ell<=L` and their radial segments stay within the controlled region.

Along a ray from the minimum, the log-mixture remainder `B` obeys
`0<=B<=delta r^2/2`, `0<=B_r<=delta r`, and
`0<=B_rr<=delta`. Hence, with `r_0=sqrt(2v)`,

```text
1 <= r/r_0 <= 1+delta,
1-delta <= V_r/r, V_rr <= 1.
```

These bounds are uniform over the rare law, contraction, interpolation time,
and arbitrarily small loss.

## Angular sign and perturbation budget

Normalize the pair-loss measure by `d`. For each contributing pair, the
quadratic-potential angular integrand is

```text
exp(u_theta)(u_theta+4).
```

Antipodal pairing gives

```text
integral exp(u_theta)(u_theta+4)
    >= 4 integral exp(u_theta) >= 4pi^3.
```

This averaging is essential: no pointwise ray sign is asserted. The pair
prefactor is at least `exp(-5R^2)`, so retaining it also retains the exact
loss factor when only rare-to-rare pairs shorten.

The perturbation estimates have adequate uniform slack. For
`0<=delta<=1/4`, the independent checker clears denominators and certifies
the three worst endpoint residuals in a Bernstein basis on `[0,1/4]`. Their
coefficient lists are all positive:

```text
(7,15/4,19/16),
(2,9/8,1/2),
(8,11/2,11/3,149/64).
```

These certify the stated bounds for the tilt coefficient, inverse square,
and inverse cube. Together with `|q^2-1|<=9delta/4`, they give a combined
radial constant `919/16<71`. At `R=1,L=8`, the remaining budgets reproduce

```text
c=16, U=56, V_0=424, J=3512, P=4+U+J=3572.
```

Consequently the angular perturbation costs less than one copy of
`integral exp(u_theta)`, leaving more than the `2pi^3` used in the proof.
After multiplying by `r_0^2=2v`, this gives
`A_t'(v_t^*+v)>=4pi^3 d exp(-5R^2)v`. Abel integration then yields the
accepted theorem.

## Dyadic specialization and boundary control

The exact elementary bound

```text
exp(41/8) < 161051/896
```

gives posterior-curvature product
`143818543/234881024<1` at `alpha=2^-21`. The same certificate fails after
weakening this to `alpha=2^-20`, so the published value is safely on the
correct side of the explicit estimate. Elementary lower bounds on `e` place
`2^-11` inside the `L=8` window. On `[2^-11,1/4]`, the raw rational margin is
`1/11943936`, which is strictly larger than `2^-24`.

The independent checker also reconstructs the seven-site example without
target code. All six anchor losses vanish, all 15 rare-pair losses are
positive, their minimum is `730/429`, and their mean is
`2366536/1254825`. The paired six-by-six determinant is
`-15616/9062625`, while the full normalized loss is exactly
`295817/689847339162009600`, quadratic in the rare mass. Thus the example
validly demonstrates that the uniform theorem does not depend on a nonzero
first rare-mass variation. It is an illustration, not a classification of
all positive contraction classes.

## Evidence and trust boundary

`independent_check.py` uses only standard-library integers and
`fractions.Fraction`, imports no target code, and checks source hashes before
running. It supplies exact finite evidence for the perturbation envelopes,
Abel constants, dyadic specialization, and boundary configuration. It does
not formalize Gaussian integration, coarea differentiation, polynomial-
moment uniqueness, posterior calculus, or the probability-law quantifiers;
those remain reviewed written mathematics. The replica and first-derivative
identities are credited dependencies with prior independent review.

Reproduce with standard-library CPython 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_DOMINANT_ATOM_WINDOW_REVIEW_PASS`. Expected
record SHA-256:
`531924c3f2a930dcfd02f263887d9aea77bf598a588f794a1ee932af349e3097`.
