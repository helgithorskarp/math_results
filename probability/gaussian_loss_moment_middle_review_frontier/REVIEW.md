# Independent review: a quartic-loss Gaussian middle guard

## Verdict and exact scope

**Accept for correctness in the stated scope; historical novelty remains
uncertain.**  At exact source commit
[`93cdc19b3452cd244b20fd765c11d855ce26e02b`](https://github.com/helgithorskarp/math_results/tree/93cdc19b3452cd244b20fd765c11d855ce26e02b/probability/gaussian_loss_moment_middle),
the uniform middle-threshold guard, its second-loss-moment cubature, and its
eight-site parameter family are correct.  This verifies Discovery Net
contribution
`bafkreig4z2sgxtkwwalum5gjmqxrga4lmvqlbok767ejxj2ler6tzvdqwi`
at height 6408.

Precisely, for a bounded law in `R^3`, a 1-Lipschitz image, Gaussian variance
`s`, normalized pair loss `d`, and normalized squared pair loss `Q`, the
reviewed theorem assumes

```text
|X-E X| <= sqrt(s)/2,
Cov(X)/s >= 2^-15 I,
Q <= 2^-48 d.
```

It proves `H(u)>=2^-40 d` for every `u` in `[1/64,1/2]` and `H(u)>=0`
for every `u>=1/64`, where the favorable gap is target hinge minus source
hinge.  It does not sign `0<u<1/64`, remove the covariance or loss-ratio
hypotheses, or prove the full dimension-three conjecture.  The primary paper
itself reports full preservation only through dimension two and partial
higher-dimensional results: [Aishwarya--Li,
arXiv:2609.07041v2](https://arxiv.org/abs/2609.07041v2).

## Reconstruction of the analytic guard

Scale by `sqrt(s)`, center both endpoint laws, and make the orthogonal
Procrustes alignment used in the accepted near-isometry result.  Put
`h=Y-X`, `M=E|h|^2`, and `kappa=2^-15`.  The exact accepted rigidity estimate
used by this packet is

```text
M <= Q/(2 kappa).
```

It follows by double centering the pair-loss kernel and applying the
full-rank source covariance bound to the Procrustes trace identity.  I
checked that its normalization is the present dimensionless `Q`, not `d^2`
or an unscaled loss.

At a fixed `0<u<1`, let `C=(2 pi)^(-3/2)`, `f=law(X)*gamma_1`, and
`E={f>Cu}`.  A positive Gaussian-mixture level set is null, so `E` is the
actual source top set of volume `|E|`; no differentiability of a moving
threshold is needed.  The accepted first-variation identity on this set is

```text
integral_E dot f_0
 = (Cu/4) integral_E E_(pi_z x pi_z)
              [Delta+|h-h'|^2] dz.
```

For `|X|<=R`, the Gaussian envelope puts `E` in
`B(0,R+sqrt(2 log(1/u)))`.  Since `f<=C`, each posterior density relative
to the source law is at least

```text
exp(-(2R+sqrt(2 log(1/u)))^2/2)
```

on `E`.  Applying this to both replica labels and discarding the nonnegative
displacement term gives

```text
integral_E dot f_0 >= (C|E|/4) q_R(u)d,
q_R(u)=u exp(-(2R+sqrt(2 log(1/u)))^2).
```

The global directional-Hessian bound for `gamma_1` loses at most
`C|E|M/2` when moving all the way to the target.  Because the same source
set is an admissible target competitor, the exact resulting inequality is

```text
H(u) >= (C|E|/4)[q_R(u)d-Q/kappa].
```

This step is a valid reuse of the independently accepted first-variation
and Procrustes theorem.  It does not assume a contracting interpolation or
infer a sign from a difference of two unrelated optimizers.

## Uniform constants and the high-threshold join

For `R<=1/2` and `1/64<=u<=1/2`, `log 2<3/4` gives
`sqrt(2 log(1/u))<3`.  Hence

```text
q_R(u) > 2^-6 exp(-16) > 2^-32,
```

where the last comparison follows from `e<3` and `3^16<2^26`.
For every `|z|<=1/2`, the lower Gaussian envelope gives
`f(z)>=C exp(-1/2)>C/2>=Cu`; thus `B(0,1/2)` lies strictly in `E` and
`|E|>pi/6>1/2`.  Also `(2pi)^3<(44/7)^3<256`, so `C>1/16`.

The loss hypothesis gives `Q/kappa<=2^-33 d`.  For `d>0`, the bracket is
therefore strictly greater than `2^-33 d`, while
`C|E|/4>2^-7`.  This proves the claimed `2^-40 d` uniformly on the full
closed interval.  If `d=0`, the loss-ratio condition forces `Q=0`, the
rigidity estimate forces `M=0`, and the two Gaussian densities differ only
by a rigid motion; every hinge gap is zero.

For the rest of the range, the accepted high-noise theorem applies with
`epsilon=R^2/s<=1/4`.  Its cutoff exponent obeys

```text
L_epsilon=(4-5epsilon)^2/[32epsilon(1-epsilon)]
          >=121/96>log 2.
```

Consequently it signs every `u>=1/2`; both hinges vanish for `u>=1` because
every variance-`s` Gaussian mixture is bounded by `C_s`.  Kirszbraun
extension supplies the global 1-Lipschitz map required by that dependency
without changing the endpoint law.  The two intervals therefore join with
no gap, but give no information below `1/64`.

## Preservation of the squared loss moment

In centered, dimensionless coordinates write
`h=|x|^2-|y|^2`, `A=E xx^T`, `B=E yy^T`, and `Cxy=E xy^T`.  Expanding the
ordered-pair definition directly gives

```text
Q = 2 E h^2 + 2(E h)^2
      +4[tr(A^2)+tr(B^2)-2||Cxy||_F^2].
```

The potentially troublesome mixed term vanishes because both coordinate
means are zero.  Marginal moments through degree four preserve
`E|x|^4`, `E|y|^4`, the marginal second moments, and `d`.  The nine cross
seconds `x_i y_j` and one cross quartic `|x|^2|y|^2` preserve everything
else in the formula.  Since the marginal first moments also remain fixed,
the centering constants used to define those ten features remain valid
after sparsification.

The accepted paired feature vector has

```text
M_q=2 binom(2q+3,3)-1
```

coordinates, including its constant coordinate.  Appending ten scalar
features and applying finite-function Caratheodory on the constant-one
affine hyperplane therefore needs at most `M_q+10` original pairs.  For
`q=2`, this is 79.  Retaining original pairs preserves contractivity, while
retaining only source sites and the same source mean preserves the centered
radius bound.  Compact-support finite-function cubature also covers diffuse
laws, but is an existence statement rather than an effective diffuse-law
oracle.

The prior-independent 85-pair option is also correct.  In uncentered
six-coordinate notation, the additional vector
`E[(Z^T J Z)Z]` requires exactly the six listed mixed cubics beyond the nine
cross seconds and one cross quartic.  Direct expansion gives the stated
correction `-8 v^T J m`; no further mixed feature is missing.

## The rare-motion parameter family

The four tetrahedral vectors have zero sum and second-moment sum `4I`.
The complete 28-pair distance table was independently reconstructed.  At
`t=0`, the four pair types have source/target squared distances, before the
common division by 6400,

```text
8 / 8,
1163 / 1163,
1323 / (3025/3),
3200 / (26912/9).
```

Multiplying every target by `1-t` makes every distinct-pair loss positive
for `t>0`.  All source squared distances and therefore all losses are at
most `1/2`.

For arbitrary priors satisfying the displayed core lower bounds and outer
mass `alpha`, the source mean has norm at most
`sqrt(3)(1+19alpha)/80<=sqrt(3)/40`.  Thus its centered support radius is
at most `11sqrt(3)/40<1/2`.  Keeping only the mandatory core masses gives

```text
Cov(X) >= (1-alpha)I/12800 >= I/25600 > 2^-15 I.
```

For the twelve ordered distinct-core pairs, their common loss is
`(2t-t^2)/800`; the weight lower bounds give
`d>=3t/51200`.  Their contribution satisfies `Q_cc<=(t/400)d`.  The coarse
but valid bound on all pairs involving an outer label is
`Q-Q_cc<=2alpha`.  Hence, throughout the full continuous parameter and
prior region,

```text
Q/d <= t/400+102400 alpha/(3t)
     <= (2161/2400)2^-48 < 2^-48.
```

The remaining relative slack is `239/2400`.  This is a universal inequality,
not an inference from the packet's 225 sample controls.  It also explains
why rare macroscopic motions are compatible with the theorem: their mass is
controlled relative to `t`, while no essential-supremum displacement enters
the retained Procrustes remainder.

## Reproduction and clean-room evidence

The target was exported from the exact cited commit rather than replayed
from a moving branch.  Normal and optimized CPython runs both returned
`LOSS_MOMENT_MIDDLE_PASS`; all eight manifest entries matched.  The emitted
target record has SHA-256
`f0f53dcc75a41d9bc082187784c5a329a0466690c3381c909c3668c7ea8ef6f8`.

[`independent_check.py`](independent_check.py) imports no target code or
target expected record.  It:

- pins six exact target files;
- checks the rational constant chain, tetrahedral identities, complete
  distance table, covariance floor, and exact `2161/2400` loss ratio;
- compares the direct ordered-pair definition of `d,Q` against both the
  centered and uncentered moment formulas on 84 nonuniform rational laws;
- exhibits two contracting pairings with identical marginals and `d` but
  different `Q`, so marginal moments alone cannot suffice; and
- builds a different nonlinear 80-pair contraction, finds a clean-room
  right-to-left exact dependence, reduces it to 79 nonnegative weighted
  original pairs, recomputes both means and centered features, and verifies
  all 79 feature expectations and both `d,Q` exactly.

Normal and optimized runs reproduce [`EXPECTED.json`](EXPECTED.json) and
return `LOSS_MOMENT_MIDDLE_INDEPENDENT_ACCEPT`.  Run from the repository root:

```sh
python3 -B probability/gaussian_loss_moment_middle_review_frontier/independent_check.py
python3 -B -O probability/gaussian_loss_moment_middle_review_frontier/independent_check.py
cd probability/gaussian_loss_moment_middle_review_frontier
sha256sum -c SHA256SUMS
```

## Guarantees, dependencies, and exclusions

The executable evidence guarantees the pinned bytes and its exact finite
algebraic controls.  The continuum conclusion additionally relies on the
written Gaussian-envelope, top-set, Taylor, and compactness arguments and on
the separately accepted near-isometry first variation, high-noise signed
window, and paired-cubature theorem.  Those dependencies were checked for
statement and normalization compatibility here; their full proofs are not
duplicated by this review.  There is no proof-assistant formalization.

The loss-relative approximation theorem and the newer Jackson schedule are
only downstream compatibility observations; neither is needed for the new
exact sign guard.  The geometric no-motion obstruction is likewise not a
premise for the Gaussian sign.  This review does not accept the unrestricted
dimension-three frontier, low thresholds, covariance-degenerate inputs,
arbitrary loss ratios, effective rational weight bounds, alternative
rematchings of the eight-site family, or any claim of historical priority.
