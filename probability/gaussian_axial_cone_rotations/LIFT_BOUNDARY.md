# An absolutely continuous Gram path can have no rectifiable geometric lift

Complete author proof, 26 September 2026; independent review is pending.
This is a correctness boundary for the existing [matrix module](MATRIX_PATHS.md)
and [regularity completion](REGULARITY.md). It uses the original cone slopes
and finite benchmark. It gives no new positive subclass, negative Gaussian
hinge, or obstruction to a different motion between the same endpoints.

The auxiliary assertion being disproved is:

> Every absolutely continuous, admissible relative Gram path of two rigid
> clouds admits a geometric lift of bounded variation, perhaps after a
> monotone change of time or a moving choice of frames.

Even strict support-cost reserve does not imply this assertion. The issue
is loss of variation on taking a square root at infinitely many rank drops.
That general square-root phenomenon is classical; the point here is to
exhibit it inside the precise contracting-motion hypotheses of M1, with
the same endpoints as the already positive axial benchmark.

## 1. A control with strict reserve on the original cones

Take the original slopes p=3/4, q=4/5, so pq=3/5, and let alpha=1/32.
For n>=1 set

    I_n=[1-2^(-n), 1-2^(-n-1)],       h_n=alpha/n^2.

These consecutive intervals fill [1/2,1). On I_n let a(t) be the triangular
function that is zero at both endpoints and h_n at the midpoint. Set a(1)=0.
It is continuous, takes values in [0,alpha], and is absolutely continuous:
its piecewise derivative is integrable and reconstructs a by integration,
including at t=1. In particular,

    integral_(1/2)^1 |a'| = 2 alpha sum_(n>=1) 1/n^2 < 4 alpha = 1/8. (1)

The strict inequality uses 1/n^2<1/[n(n-1)] for n>=2 and telescoping.
Define a real 2-by-2 matrix path

    A(t)=R_(pi(1-2t))                    for 0<=t<=1/2,
    A(t)=diag(1,1-a(t))                  for 1/2<=t<=1.   (2)

It is absolutely continuous, A(0)=-I, A(1)=I, and ||A(t)||op=1.
Its operator length is pi+2 alpha sum 1/n^2. For the full disk sections
of radii p and q, the M1 support function and cost are exactly

    k(t)=(3/5)||A'(t)||op,
    J=integral k < (3/5)(pi+1/8) < 549/280 <2.            (3)

The last bound uses the classical pi<22/7; the reserve is greater than
11/280. No decimal approximation or numerical summation is used.

Set

    c(t)=-1+(2/J) integral_0^t k,
    d(t)=sqrt(1-c(t)^2),
    L(t)=diag(A(t),c(t)).                               (4)

Thus L is absolutely continuous. In M1 notation it is the relative cross
Gram matrix. A continuous rank-one residual factor is ell=0 on [0,1/2]
and

    ell(t)=(0,sqrt(2a(t)-a(t)^2))                         (5)

on [1/2,1]. The formula

    F_t(v,z)=(A(t)v,c(t)z,ell(t)v,d(t)z) in R5           (6)

is a continuous isometric embedding of the moving cloud, with the other
cloud embedded by the fixed standard inclusion. The cross inner product
has derivative z_a z_b [u^T A'v+c']>=0 because c'=2k/J>=k and
u^T A'v>=-k. Hence all cross distances decrease, while within-cloud
distances remain constant. This directly verifies a continuous contraction
of C_p union (-C_q) with the required endpoints and strict reserve.

## 2. Every lift of this prescribed Gram path has infinite variation

Write e_2 for the second transverse coordinate in R3. Let G_t,F_t be
**any** continuous isometric embeddings R3->R^m, for any fixed finite m,
with

    G_t^T G_t=F_t^T F_t=I_3,       G_t^T F_t=L(t).         (7)

The first cloud need not be fixed. Its orthogonal residual vector is

    E(t)=(I_m-G_t G_t^T)F_t e_2.

On the second half of the interval, (7) gives the invariant identity

    |E(t)|^2 = 1-|L(t)e_2|^2 = 2a(t)-a(t)^2.            (8)

Let r(t)=|E(t)|. On every I_n it is zero at both endpoints, whereas at
the midpoint

    r >= sqrt(h_n)=sqrt(alpha)/n,                        (9)

since 0<=h_n<=1. Thus its scalar total variation is infinite: on the
first N such intervals it is at least

    2 sqrt(alpha) sum_(n=1)^N 1/n.                      (10)

This lower bound depends only on L, not on signs of a square root or the
choice of the moving frames. More quantitatively, for any two times,

    |r(t)-r(s)| <= |E(t)-E(s)|
                 <= ||F_t-F_s||op+2||G_t-G_s||op.        (11)

Here orthogonal projections have norm one, F_s e_2 has norm one, and
||G_t G_t^T-G_s G_s^T||op<=2||G_t-G_s||op. Summing (11) along partitions
shows that G and F cannot both have finite total variation. In particular
they cannot both be absolutely continuous. Increasing the ambient dimension
does not repair this prescribed Gram curve.

A continuous nondecreasing surjection of the time interval preserves the
ordered visits to every endpoint and midpoint in (10). Therefore no such
reparametrization makes a lift rectifiable. This is an obstruction to a
lift of the specified entire curve L, not merely to the particular factor
in (5).

## 3. The obstruction is already visible on the existing finite benchmark

Use the original 25 labeled sites from [PROOF Section 5](PROOF.md),

    X=(0,{(p d,1):d in D12},-{(q d,1):d in D12}),
    Y=(0,{(p d,1):d in D12},{(q d,1):d in D12}).

Both anchored clouds span R3. Their rigidity determines the embeddings
G_t and F_t from three independent labeled vectors in each cloud, using
fixed linear coefficients. This follows directly from their preserved
within-cloud inner products. If the anchor and all 24 point trajectories
had bounded variation in a lift of the prescribed Gram data, subtracting
the anchor and applying these fixed coefficients would make both frames
BV, contrary to (10)--(11). Hence at least one point trajectory has
infinite variation in every such finite geometric realization.

No new finite configuration or positive class has been introduced. The
same endpoints have the explicit analytic R4 motion in PROOF equation
(15). Replacing the entire Gram path by that different motion removes the
obstruction. It is therefore not a minimum-dimension theorem, a failure
of the Gaussian comparison, or a Kneser--Poulsen counterexample.

## 4. Exact consequence for the review and lane handoff

Absolute continuity of a matrix control or of its relative Gram data does
not imply absolute continuity, bounded speed, finite length, or finite
total variation of a geometric lift. This remains false with strict
support-cost reserve and with moving frames. A proof using such an upgrade
must supply additional hypotheses or replace the curve.

The published [regularity proof G](REGULARITY.md) assumes no such upgrade.
It approximates A strongly in W1,1 and controls squared pair distances
directly; its finite smooth approximating motions need not follow the
original curve. This note supplies a concrete reason to retain that
distinction in researcher 4's deformation interface as well.

There is a further logical boundary. Infinite variation **does not by
itself rule out** the exact notion of piecewise smoothness used in
[Bezdek--Connelly, Section 3](https://arxiv.org/pdf/math/0108098): coordinates
may be smooth away from finitely many parameter values without having
finite variation near those exceptional values. No impossibility of that
weaker regularity is inferred here. Conversely, the density-value coupling
in [Aishwarya--Li Theorem 1.4(i)(a)](https://arxiv.org/html/2609.07041v2)
requires only continuous trajectories. Its stronger smooth-flow clause
has separate differentiability and integrability assumptions.

This is a written analytic counterexample to the stated auxiliary lifting
assertion, not independent review of M or G. The infinite variation follows
from the harmonic lower bound (10); a finite path grid cannot establish it.
No new checker is offered as doing so. The rational reserve arithmetic is
reproducible with the Python standard library:

```sh
python3 - <<'PY'
from fractions import Fraction as Q
upper = Q(3,5)*(Q(22,7)+Q(1,8))
print(upper, 2-upper)
PY
sha256sum -c SHA256SUMS
```

Expected first line: `549/280 11/280`. The manifest checks source integrity,
not mathematical validity. The original fourteen core proof/checker files
and REGULARITY.md remain unchanged.
