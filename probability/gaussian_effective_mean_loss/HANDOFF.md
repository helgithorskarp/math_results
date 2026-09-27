# Effective R2/R3/R8 zero-loss handoff

The new author theorem replaces the non-effective cutoff in R8's mean-loss
margin by seven explicit inequalities. Independent acceptance of the new
argument is pending. R8's original qualitative theorem and R3's previous
quartic guard retain their own review status; this is not a self-review.

## Consumer contract

Use favorable H=target hinge minus source hinge and dimensionless mean
pair loss d=E[|X-X'|^2-|TX-TX'|^2]/s. With centered radius<=sqrt(s)/2
and Cov(X)/s>=2^-15 I:

| Exact input condition | Certified output |
| --- | --- |
| d=0 | H is identically zero |
| 0<d<=2^-360 | H>=2^-40 d on every u in [1/64,1/2]; H>=0 for u>=1/64 |
| Q<=2^-48 d | The previously accepted quartic guard gives the same interval, without the new mean-loss cutoff |
| Neither sufficient guard | UNRESOLVED |

Neither row signs u<1/64. The two nonzero-loss tests are complementary.
The new test covers rare-motion laws for which Q/d remains macroscopic.
The old test can sign inputs whose mean loss is much larger than 2^-360.

`certificate.finite_guard(x,y,p,variance)` implements the NEW dyadic test
on exact rational finite data. It checks all positive-weight pair distances,
computes d by two formulas, and checks the source covariance using all
seven principal minors. Zero-weight labels are discarded. Bad probability
data, nonrational data or an expansion raise ValueError. Valid data outside
the guard return UNRESOLVED; this is never evidence of an adverse hinge.
No numerical Procrustes solve or top-set computation is required.

For other centered radius/covariance bounds use

```python
from fractions import Fraction as F
from certificate import rational_schedule, audit_cutoff
c = rational_schedule(F(2), F(1, 4), 12)
d_cut = F(1, 2**c['cutoff_exponent'])
audit_cutoff(c, d_cut)
```

This is an all-radius exact rational schedule signing every u>=2^-12
under those radius/covariance hypotheses. The constants depend strongly on
the inputs. `constants(...)` is only a low-level algebra routine: if used
directly, its posterior lower weight must separately satisfy the B,w
conditions in PROOF.md. `rational_schedule` supplies these bounds itself
using log 2<3/4 and e<3.

## What paired cubature must retain

Only the two marginal means and second moments are needed for the new
guard. In particular,

```
d=2(tr Cov(X)-tr Cov(Y))/s.
```

The existing accepted common-pair cubature at degree two preserves these
quantities, the centered radius, and source covariance on at most

```
2 binom(5,3)-1 = 19
```

original pairs. This is a direct use of that theorem, not a new cubature
construction. For a Jackson/Taylor degree 2q, keep the ordinary
M_q=2 binom(2q+3,3)-1 pairs; **no extra mixed features are required**.
The prior quartic guard still needs its ten centered or sixteen raw
additional features when that separate guard is used.

The 19-pair statement gives an exact existence reduction. It does not
produce a uniform cubature rule for an entire parameter family, a rational
denominator bound for arbitrary real data, or an effective diffuse-law
integration oracle. Finite rational inputs permit ordinary rational affine
elimination on existing sites. Independent rounding is not asserted to
preserve any guard.

## Remaining finite-sign obligations

The small-loss part of the chosen middle domain can now be removed with a
KNOWN cutoff. A search outside it may impose d>=2^-360 (retaining the
boundary harmlessly). This makes division by d quantitatively bounded;
it does not supply a positive sign on the remainder. Loss-proportional
cubature and Jackson reconstruction remain available there with their
original hypotheses and errors. Any absolute approximation error eta
becomes at most 2^360 eta after normalization on that remainder. This
large factor is a limitation, not a practical running-time claim.

The new constants also make R8's bounded-volume margin explicit, by the
t,B substitution in PROOF.md. A separately proved uniform lower-threshold
sign can be joined to the new cutoff theorem; no such tail is supplied
here. Covariance collapse and unbounded radius or volume limits still
need separate arguments.

The family in PROOF.md has independent tau,alpha in [0,2^-362], arbitrary
permitted unbalanced core/outer priors, and includes tau=0, alpha>0.
At that boundary Q/d>=59/1800, so its sign is not obtained by silently
reusing the old quartic guard. Balanced orbit controls were already signed
by the parity theorem and are not claimed as new examples.

## Review-sensitive step

The new analytic obligation is Section 2 of PROOF.md: every interval
component of the ACTUAL Gaussian source superlevel has the required
midpoint bias, because its endpoint densities agree. The explicit Gaussian
interval comparison preserves a margin proportional to the component
length. Summing these components handles disconnected, nonconvex and
arbitrarily small-volume top sets. Using a fixed reference ball in place
of the actual superlevel would not justify that endpoint identity.

The code only checks exact constants, finite loss/covariance identities,
normalization, and deliberately ineligible inputs. It does not replace
this analytic proof, re-audit teammate computations, or independently
accept the new theorem.
