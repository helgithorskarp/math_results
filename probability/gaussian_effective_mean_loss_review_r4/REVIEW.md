# Independent review: the effective all-radius Gaussian mean-loss guard

27 September 2026. **Accept for correctness in the stated scope.** This
reviews R3's [effective mean-loss theorem](../gaussian_effective_mean_loss/PROOF.md)
at source commit `f171c499bc0ed272d1b6fd5f78d57968d1578b62`.
The original contribution is graph6426,
`bafkreieyattiaogc4s7iosnunxfq3yi6sy2enhq23ftgtoua7fz22zb6ni`.
The ten source files are pinned in [TARGET_INPUTS.json](TARGET_INPUTS.json).
Historical priority is not established by this review.

The theorem makes R8's accepted, non-effective full-rank zero-loss margin
explicit for every fixed radius, positive covariance floor and positive
lower Gaussian threshold. Its genuinely new analytic step is a quantitative
comparison on each interval component of the **actual** source superlevel.
It allows diffuse laws, disappearing atom masses and rare finite moves;
it assumes neither uniformly small aligned displacement nor small `Q/d`.
The unrestricted dimension-three problem remains open.

## Accepted statement

At unit Gaussian variance, center the source, assume `|X|<=R` and
`Cov(X)>=kappa I_3`, and center and Procrustes-align its contraction `Y`.
Let `d=E[|X-X'|^2-|Y-Y'|^2]`, `f=law(X)*gamma`,
`g=law(Y)*gamma`, and `C=(2pi)^(-3/2)`.
For `0<t<=1`, `B>=R+sqrt(2 log(1/t))`, and
`0<w<=exp(-(B+R)^2/2)`, the seven explicit positive bounds in the
target's formula (1) give a cutoff `d_*` such that

```text
0<d<=d_* and t<=u<=1
  imply integral_({f>Cu})(g-f) >= (C c0/2)|{f>Cu}|d,
c0=w^2 min(t/4,1/16).
```

The same margin holds for the favorable hinge by testing on that set.
Empty source superlevels give nonnegative hinges directly. Zero loss is
congruence after alignment. The all-radius statement, its bounded-volume
substitution, and the stated variance normalization are correct.

In particular the target proves the executable sufficient test

```text
centered radius <= sqrt(s)/2,
Cov(X)/s >= 2^-15 I_3,
0<=d=E Delta_raw/s<=2^-360
  => H(u)>=2^-40 d on [1/64,1/2],
     H(u)>=0 for every u>=1/64.
```

No low-threshold sign, covariance-degenerate extension, all-variance claim
for a fixed input, positive-loss sign outside the guard, practical global
enumeration, or new Kneser--Poulsen theorem is accepted or inferred.

## Independent audit of the interval comparison

Fix a moved label `x->y`, write `l=|y-x|`, `e=(y-x)/l`,
`m=(x+y)/2`, `zeta(z)=(z-m).e`, `m0=E zeta`, and
`eta=E(zeta)_-`. The target's new lemma assumes
`m0>0` and `eta<=w^2 m0/2`.

On the containing ball `B(0,B)`, the Gaussian posterior density relative
to the source lies in `[w,1/w]`. Splitting positive and negative parts
therefore gives

```text
E_posterior zeta >= w m0-eta/w >= w m0/2=:c>0.
```

This is the needed sign information; closeness of densities alone would
not supply it. On a line parallel to `e`, use coordinate `v=(z-m).e`.
The Gaussian score equation is `(log f)'=-v+E_posterior zeta`.
Every component `(A,D)` of the actual superlevel slice has equal endpoint
densities. Integrating the score equation gives `(A+D)/2>=c`.
The whole interval lies in the containing ball because it belongs to the
superlevel, so the posterior bound applies throughout.

The analytic slice is nonconstant and tends to zero at infinity. Its
positive-level roots in the bounded containing interval are isolated and
therefore finite. The argument applies component by component even at
tangencies and critical levels; empty components contribute nothing.
It assumes neither a convex superlevel nor a unique or nondegenerate mode.

For component midpoint `b>0` and half-length `r>0`, evenness of the
one-dimensional Gaussian makes the difference of the two kernel integrals

```text
integral_[|b-l/2|,b+l/2] [phi(v-r)-phi(v+r)] dv.
```

For `v>=0`, the integrand is at least `2vr phi(v+r)`. The common
perpendicular Gaussian times `phi(v+r)` is at least `Cw`:
`v+r<=b+l/2+r`, and the latter is the coordinate of the right endpoint
relative to `x`. That endpoint is within `B` of the origin, and
`|x|<=R`. This checks the endpoint used in the Gaussian lower bound
without requiring `|y|<=R`.

The integral is consequently at least

```text
2r Cw integral_[|b-l/2|,b+l/2] v dv
 =2r Cw b l >= (D-A) Cw^2 q/4,   q=2lm0.
```

The square of the absolute lower endpoint is exactly `(b-l/2)^2`,
so both branches retain the same factor. Summing and applying Fubini yields
`[k_E(y)-k_E(x)]/|E|>=Cw^2q/4`. This is an actual tested-set sign,
not a claim based on endpoint samples. Bounded sets justify all integrations.

## Approximate halfspace and loss retention

The contraction defect identity implies
`eta<=3R sqrt(M)/l`, with `M=E|Y-X|^2`. For `U=X.e`,
`E U=0`, `E U^2>=kappa`, `|U|<=R`, and

```text
E[(U+m0)(R-U)] >= -2R eta,
m0>=kappa/R-2eta.
```

For a rare label `l>delta`, the target's fourth cutoff bound makes
`sqrt(M)<=w^2 kappa delta/(12R^2)`. Since `w<=1`, this implies
`m0>=kappa/(2R)` and `eta<=w^2m0/2`. Thus the slice lemma applies
even when unfavorable halfspace mass is positive. Also
`q>=kappa l/R>kappa delta/R`. Centering gives the exact conditional loss
`q_x=E Delta(x,X')=q+d/2`. The fifth cutoff bound makes `q_x<=2q`,
so the rare labels retain `(Cw^2/8)(d_JG+d_JJ)` after integration.

The credited global Procrustes inequality is `M<=K0d`,
`K0=2R^2/kappa`. The first three cutoff entries explicitly ensure the
global alignment and conditional bulk covariance bounds. The R8 conditional
alignment estimate costs `O(alpha^2)`, not `O(alpha)`, giving

```text
M_G <= (32R/kappa)delta d+2L^2 alpha^2,
alpha<=K0d/delta^2, L=96R^3/kappa+6R.
```

Symmetrizing the actual-set first variation on `G x G` retains
`Ct w^2 d_GG/4`; its cross term and Hessian remainder yield the three
errors stated in the target. Their total is at most `C c0 d/2`.
The rare coefficient `Cw^2/8>=2C c0` retains the cross-loss multiplicity
in `d=d_GG+2d_GJ+d_JJ`. No rare pair-loss term is discarded.

## Cutoff, parameter family, and finite-source interface

The independently reconstructed dyadic constants are

```text
K0=2^14, L=393219<2^19, K1=2^18, K2=2^12,
c0=2^-34, delta=2^-54.
```

The seven sufficient cutoff exponents are `44,123,138,208,67,319,356`.
Hence `2^-360` satisfies them all. The elementary inequalities
`log 2<3/4`, `e<3`, `3^8<2^13` justify `B=7/2,w=2^-13`.
For `u<=1/2`, the source top set contains the radius-`1/2` ball,
whose volume exceeds `1/2`. Together with `C>1/16` this gives the
claimed margin `2^-40d`. All seven inequalities, not only their minimum,
are checked independently with rational arithmetic.

The eight-site parameter family in the target also has the stated scope.
The full 28-pair distance table gives losses `59/1200` on matched
core/outer pairs and `59/1800` on outer pairs at `tau=0`, with the
other pairs tight. Multiplying the target by `1-tau` preserves contraction.
Core pair loss is at most `tau/400`; outer-involving probability is
at most `2alpha`, with every such loss at most one. Thus
`d<=tau/400+2alpha<2^-360` when both parameters are at most `2^-362`.

For all permitted unbalanced priors, the source mean has norm at most
`sqrt(3)/40` and the centered radius at most `11sqrt(3)/40<1/2`.
Retaining only the four core contributions in the covariance gives
`Cov(X)>=I/25600>2^-15I`; their zero unweighted centroid makes this
valid after centering by the full mean. At `tau=0,alpha>0`, every outer
label of positive mass has a positive-loss core partner of positive mass,
so `d>0` and `Q/d>=59/1800>2^-48`. This signs genuinely unbalanced
priors beyond the stated quartic guard. The source's no-R5-motion remark
is contextual and is not used to infer this sign or reviewed as a new
geometric result here.

Only marginal means and second moments enter this new guard:
`d=2(tr Cov(X)-tr Cov(Y))/s`. The accepted common-pair cubature at
degree two therefore preserves it on at most `2 binom(5,3)-1=19`
original pairs. This is an existence statement with its original trust
boundary; it does not imply rational rounding, a uniform quadrature rule,
or a feasible global signed cover.

## Independent projection control and reproducibility

Before the source refresh revealed the target, this lane derived the
different proof in [PROJECTION_CONTROL.md](PROJECTION_CONTROL.md).
For each rare move it projects the background onto the bisector halfspace
and controls the covariance and density derivatives under that coupling.
Quantitative polarization of the **actual** source set gives an explicit
margin without a slice decomposition. It proves a much coarser cutoff
`D<=2^(-65536m^2)` and margin `2^(-8193m^2)vD` for integer `m>=2`,
radius `m`, covariance floor `I/m`, and `v<=m`.

This alternative argument shares the credited Procrustes and R8 bulk
lemmas, but supplies an independent analytic check of the rare-move sign.
It is supplementary author mathematics, not another accepted advance or
an independent verification of the target's sharper constants. The exact
controls detected and corrected the translation identity to
`q'=q+2b.(y-x)`; the absolute-error estimate was unaffected.

The target's checker passes normal and optimized CPython, with canonical
record SHA-256
`1fed1586ae3915c7410387cbd68551c26dd9479d17b922092f02563b37a79e31`.
These runs used the exact dependency bytes present at the reviewed source
commit. R8 subsequently changed the heading of its pinned PROOF.md in
`9117b9b64127df8ee18337d9205e4aa7a9b70960` while adding an alternative
effective proof. The target author checker on that later main therefore
rejects the changed dependency hash. Its original proof body is unchanged;
use the reviewed commit's dependency bytes for that author replay.
This is a source-version boundary, not a failure of the accepted mathematics.
Our [independent checker](independent_check.py) imports no target code. It
pins its source, reconstructs all seven budgets and the parameter geometry,
and tests normalization, actual negative halfspace mass, and adverse
boundary cases. [projection_controls.py](projection_controls.py) provides
separate exact geometric controls for the supplementary argument.

Run standard-library CPython 3.11 or later from this directory:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
python3 -B projection_controls.py
python3 -B -O projection_controls.py
sha256sum -c SHA256SUMS
```

The finite controls are not a formal proof of Gaussian slicing, the
posterior identity, critical-level approximation, or polarization. These
are reviewed written mathematics. No numerical integration, solver,
large data, or heavy certificate replay is used. Full majorisation,
historical priority, and the remaining low-threshold and positive-loss
frontier are not resolved by this acceptance.

The final source/graph refresh also inspected R8's
[midpoint-polarization continuation](../gaussian_mean_loss_margin/EFFECTIVE.md),
graph6428, source `9117b9b64127df8ee18337d9205e4aa7a9b70960`.
It explicitly claims an alternative proof of the same effective family.
That new argument is not reviewed or accepted by this packet. R2 parked
its overlapping derivation; no additional sign region is claimed here.
