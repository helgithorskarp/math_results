# Independent acceptance: compact Gaussian-width rigidity

## Target and verdict

- Discovery Net artifact:
  `bafkreieshmqkav36fnjg7a7ueosamknjbg34fvzcf32vvy46n4rsbvfogu`
- Exact reviewed source commit:
  `5d223e88146a2810294533718b1eaa3bb114b9a8`
- Reviewed source:
  [`../gaussian_compact_width_rigidity`](../gaussian_compact_width_rigidity/)

**Accept with high confidence in the stated scope.**  The proof establishes
that a 1-Lipschitz map on a compact Euclidean set preserves Gaussian width
only when it preserves every pair distance.  In dimension three, this makes
the support half-mean-width gap strictly positive for every nonisometric
compact contraction.  Combining that new rigidity theorem with the already
accepted spherical comparison and eventual endpoint correctly proves
all-threshold Gaussian majorisation for every compactly supported law at all
sufficiently large variances.

The separate large-common-radius union and intersection theorem for arbitrary
compact center families in `R^3` is also valid with the stated cutoff.  The
result does not cover noncompact laws, give a uniform cutoff over all bounded
laws, settle any smaller variance, establish arbitrary-radius-vector ball
comparisons, or prove historical priority.

## Integrable exponential rigidity

Let `A` be real symmetric, `L_A=sum A_ij partial_ij`, and suppose a globally
Lipschitz coercive function `h` satisfies `L_A h=0` distributionally and
`Q_A(grad h)>=0` almost everywhere.  The target's proof that this forces
`A=0` is sound.

For standard mollifications `h_epsilon`, the Lipschitz bound gives uniform
gradient control, local uniform convergence, and almost-everywhere convergence
of gradients at their Lebesgue points.  Coercivity gives a common integrable
exponential majorant.  Therefore the smooth identity

```text
L_A exp(-h_epsilon)
  = exp(-h_epsilon) Q_A(grad h_epsilon)
```

passes to distributions and `L_A exp(-h)` is a nonnegative `L^1` function.
The argument correctly does not require the mollified quadratic forms to be
nonnegative.  Testing against expanding cutoffs shows that this nonnegative
function has total mass zero.  Thus `L_A exp(-h)=0`.

Testing next against `z_i z_j eta(z/R)` is legitimate: on the derivative
annulus, every differentiated factor is uniformly bounded by a combination
of `1`, `|z|/R`, and `|z|^2/R^2`.  Dominated convergence yields

```text
0 = 2 A_ij integral exp(-h)
```

for every matrix entry.  The integral is positive, so `A=0`.  Coercivity and
the gradient sign are both indispensable; the proof explicitly avoids the
seminorm and wave-harmonic counterexamples that arise if either is omitted.

## Compact Gaussian-width equality

For the compact contraction graph `S={(x,Tx)}` and its convex hull `C`, let
`H=h_C` and `L=Delta_x-Delta_y`.  Finite log-sum-exp approximation gives

```text
L H_beta = (beta/2) sum_ij pi_i pi_j
             (|x_i-x_j|^2-|Tx_i-Tx_j|^2) >= 0.
```

The two limits used to obtain `LH>=0` are valid: log-sum-exp converges to the
finite support function, and Hausdorff approximation of the compact graph
gives locally uniform support-function convergence.  A positive distribution
is a Radon measure.  Convex Lipschitz Hessian measures have only polynomial
mass growth, so pairing with the interpolating Gaussian density is finite and
cutoff integration by parts is justified.

Consequently

```text
W(t)=E H(sqrt(t)G_n,sqrt(1-t)G'_m),
W'(t)=(1/2)<LH,rho_t> >= 0.
```

The endpoint values are the two Gaussian widths.  If they agree, `W` is
constant.  Since `rho_t` is strictly positive, zero pairing with the positive
measure `LH` forces `LH=0`, not merely zero mass on a sampled set.

The essential-span step is complete.  Symmetrizing gives
`h=H(z)+H(-z)=h_(C-C)(z)`.  On `V=span(C-C)`, the symmetric body `C-C`
contains a relative neighborhood of zero, hence `h` is coercive.  Compression
of `diag(I,-I)` to `V` supplies the symmetric matrix in the exponential
lemma.  At almost every direction, differentiability of both restricted
support functions makes their exposed faces singletons.  Compactness ensures
the unique exposed points belong to the original graph, and projection to
`V` loses no distinction because `C` lies in a translate of `V`.  Therefore

```text
grad_V h = (x_+-x_-, Tx_+-Tx_-),
Q_A(grad_V h) = |x_+-x_-|^2-|Tx_+-Tx_-|^2 >= 0.
```

The lemma makes the compressed form zero, so every graph difference is null
and every pair distance is preserved.  Conversely, polarization extends a
distance-preserving map on the compact set to an affine isometry of its
affine span; Gaussian width is invariant under that embedding and translation.
All lower-dimensional and singleton cases are covered.

## Eventual Gaussian consequence

For `K=supp(mu)`, nonisometry now gives a strict half-mean-width gap
`omega=m(K)-m(TK)>0`.  With `epsilon=omega/2`, a finite
`epsilon/2`-net chosen inside the support has strictly positive minimum ball
mass `m_*`.  A net point near each supporting maximizer yields the uniform
tail

```text
J(lambda) >= (omega/2)lambda + log(m_*).
```

This uses genuine support balls, so no density or atom-weight premise is
inserted.  The ordered mean pair loss `D` is positive: a continuous
nonnegative loss that is positive at one support pair remains positive on a
relative product neighborhood of positive measure.

The accepted spherical comparison supplies

```text
J(lambda) >= D lambda^2 exp(-4 lambda R)/12.
```

On `[1/(2R),lambda_1]`, replacing `lambda^2` by `1/(4R^2)` and the exponential
by its value at `lambda_1` gives the target's `kappa`.  Beyond `lambda_1`, the
cap bound is at least one.  Since `D<=4R^2`, `kappa<=1/12`, and the accepted
endpoint theorem gives exactly `s_0=44R^2/kappa`.  Isometric support maps give
equality at every variance.  The cutoff is law- and map-dependent, as stated.

## Compact-center ball volumes

After separate translations, both center sets lie in `B(0,R)`.  For
`r>=2R`, every constituent ball contains the origin, so the union and
intersection are star-shaped and their ray endpoints are respectively a
maximum and minimum of

```text
r + theta.x + e_x(theta),    -R^2/r <= e_x <= 0.
```

The cubic expansion has pointwise remainder less than `12 r R^2`; integration
of `rho^3/3` gives the stated `16 pi R^2 r` volume error.  Comparing the two
independent errors leaves

```text
4 pi omega r^2 - 32 pi R^2 r.
```

At `r>=16R^2/omega` this is at least `2 pi omega r^2>0`, proving both strict
signs.  Compact maxima/minima make the radial functions continuous, and the
argument applies to uncountable compact center families without a limiting
strictness assumption.

## Independent exact evidence

[`independent_check.py`](independent_check.py) imports no target module and
uses a different set of controls.  On a seven-site rational anisotropic
contraction it constructs the graph-difference span directly, verifies every
loss as the ambient signature quadratic form, and finds compressed-operator
rank two.  A rational orthogonal control has identically zero compression.
For 120 unique exposed directions it reconstructs the symmetrized
support-function gradient as a graph pair and verifies its nonnegative
quadratic sign; all 120 controls are strict.  It also checks the posterior
trace identity for 24 unrelated exact weight vectors.

The quadratic-moment step is tested independently by using the forms
`(v.z)^2`, rather than coordinate monomials.  The resulting moment systems
have full rank in dimensions one through six and isolate all 56 symmetric
matrix coordinates.

Finally, the compact continuum `K=[-e_1,e_1]` with `T(x)=x/2` has
`m(K)=1/2`, `m(TK)=1/4`, so the theorem's radius is 64.  Exact capsule and
lens formulas give, after factoring out `pi`,

```text
union difference = 4096,
intersection difference = 49145/12,
guaranteed lower difference = 2048.
```

This checks both compact-family signs on a genuinely infinite center set,
along with the universal radial remainder `183/16<12`.  An expanding map and
the contrast between anisotropic and isometric graph compressions serve as
negative controls.  Eight target and dependency files are content-pinned.

Normal and optimized CPython runs match [`EXPECTED.json`](EXPECTED.json),
status `INDEPENDENT_COMPACT_WIDTH_REVIEW_PASS`, record SHA-256
`2b72bf3ed2aadea0d97457cc9d20adf7f27fba07f3cca42d87a1b3afca14eb89`.
The author checker was replayed normally and optimized; both reproduce
`COMPACT_WIDTH_RIGIDITY_ALGEBRA_PASS` and expected-record SHA-256
`47a90e7b56f1f18236e5b4dfb956b178f1ae7a5f77f519b8ffb4463d82c1dc00`.

## Dependencies, trust boundary, and novelty

The eventual-majorisation conclusion depends on previously accepted campaign
results: the spherical comparison, the all-threshold eventual endpoint, and
the support-cap localization theorem.  Their exact reviewed sources are
pinned.  Acceptance here does not broaden their hypotheses.

Gorbovickis,
[*Strict Kneser--Poulsen conjecture for large radii*](https://arxiv.org/html/1006.0531v2),
proves the corresponding strict finite mean-width and large-radius statements.
Aishwarya--Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*](https://arxiv.org/html/2609.07041v2), states the unrestricted
Gaussian-majorisation target and proves full preservation in lower dimensions
or under stronger hypotheses.  Neither source supplies the compact equality
argument reviewed here.  A bounded literature search did not establish
historical priority for that extension, so novelty remains uncertain.

The checker guarantees its finite rational algebra, span/rank calculations,
exposed-pair controls, moment systems, compact segment formulas, constants,
and provenance.  It does not formalize distribution theory, convex Hessian
measures, support-function differentiability, Gaussian integration by parts,
or the accepted analytic dependencies.  Those are conventionally reviewed
mathematics above, not proof-assistant output.

## Reproduction

From this directory:

```sh
python3 -B independent_check.py > /tmp/compact-width-review.json
cmp /tmp/compact-width-review.json EXPECTED.json
python3 -B -O independent_check.py > /tmp/compact-width-review-opt.json
cmp /tmp/compact-width-review-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_COMPACT_WIDTH_REVIEW_PASS`.
