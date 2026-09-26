# A positive endpoint scatter representation fails for b_(7,0)

Author proof with an exact certificate; independent review pending.
This rules out a specific candidate for signing the first generally unsigned
beta test at all variances. **It is not a negative Gaussian beta value or a
counterexample to majorisation.** In the exhibited contraction the actual
beta is strictly positive at every variance.

## 1. The candidate finite dependency

For a finite contraction, every normalized Gaussian moment is a finite
Laplace sum in inverse variance tau=1/s. The beta test is a signed combination
of these moment sums. One possible way to extend a variance-specific
certificate to all variances is to order the integrated endpoint scatter
spectra. In the notation below, this means A(t)>=0 for every t,
which would immediately imply beta(tau)>=0 for every tau>0.

This is a concrete stronger condition being tested here, not a claimed
necessary consequence of majorisation or a theorem attributed to R5/R8.
The question is whether complete endpoint and prior-weight averaging repairs
the sign lost in the individual conditional terms. It does not repair this
particular integrated-scatter condition.

## 2. An actual contraction and the full endpoint formula

Take the probability law

    mu=(delta_(-e_1)+delta_(e_1))/2 on R3,
    T(-e_1)=T(e_1)=0.

The map is a contraction (squared pair distance 4 becomes 0) with a constant
1-Lipschitz extension. For s=1/tau>0, put

    f_s=mu*gamma_s,  g_s=gamma_s,  C_s=(2 pi s)^(-3/2),
    d_m(tau)=C_s^(1-m) integral(g_s^m-f_s^m),
    B(tau)=b_(7,0)(tau)
          =8 sum_(m=2)^9 (-1)^(m-2) binom(7,m-2) d_m(tau)/(m(m-1)). (1)

The Gaussian replica identity is the existing normalization used by the
finite certificate chain. If r of m independent source replicas equal +e_1,
the total squared distance over unordered pairs is 4r(m-r). Consequently

    a_(m,r)=2r(m-r)/m,
    d_m(tau)=m^(-3/2)
        [1-2^(-m) sum_(r=0)^m binom(m,r) exp(-tau a_(m,r))].        (2)

This is the full actual weighted endpoint expression. No intermediate
six-dimensional cloud, distinguished-pair sign, or polarized monomial is
substituted for B.

Define the signed atomic measure

    nu=sum_(m=2)^9 c_m
           [delta_0-2^(-m)sum_(r=0)^m binom(m,r)delta_(a_(m,r))],
    c_m=8(-1)^(m-2)binom(7,m-2)/(m(m-1)m^(3/2)).                   (3)

Then nu has finite support and exactly zero total mass, and

    B(tau)=integral exp(-tau a) nu(da).

Every knot a is rational and every coefficient belongs to
Q(sqrt2,sqrt3,sqrt5,sqrt7). The checker verifies this spectrum by both
binomial multiplicities and all 1020 ordered binary replica assignments
at sizes 2,...,9, calculating pair distances directly in the latter method.
The two spectra agree entry by entry, not just in total mass.

## 3. The integrated spectrum is strictly negative

Set

    A(t)=integral (t-a)_+ nu(da),   t>=0.                         (4)

Fubini for the finite signed sum gives exactly

    B(tau)/tau^2=integral_0^infinity exp(-tau t) A(t) dt.          (5)

The factor tau^2 matters. It comes from integrating (t-a)_+ against the
exponential, not from changing the spatial normalization.
A is continuous and piecewise affine. Its only internal knot on
[33/25,27/20] is 4/3. At that knot the closed expression is

    A(4/3)=31667/15552 +(1663/3072)sqrt2 -(28/27)sqrt3
                     -(7/10)sqrt5 +(217/648)sqrt6 -(3/28)sqrt7.  (6)

Rational outward root bounds in [CERTIFICATE.json](CERTIFICATE.json)
prove (6) is between -23/1000 and -22/1000. They also certify the two
endpoints and the internal knot are each less than -1/125. Affinity on
the two intervening segments therefore proves the whole interval bound

    A(t)<-1/125,   33/25<=t<=27/20.                              (7)

The certificate contains all three radical expressions and rational
intervals. Root bounds use integer square roots at scale 10^12; the
checking code verifies their squared endpoints. No approximate root,
spatial quadrature or solver verdict is used as a sign premise.

## 4. A finite obstruction to every positive Laplace representation

The negative density in (5) already suggests that B(tau)/tau^2 cannot
have a different representation as a Laplace transform of a nonnegative
measure. The following explicit derivative certificate proves this directly,
without relying on inverse-Laplace uniqueness or numerically differentiating.

Because nu has zero mass,

    A(t)=-integral min(t,a) nu(da),
    |A(t)|<=integral a |nu|(da)
       <=4 sum_(m=2)^9 binom(7,m-2)/m^(5/2)
       <=4 sum_(m=2)^9 binom(7,m-2)/m^2
        =954881/45360<128.                                      (8)

For the first estimate on total variation, use the uncollected terms (3).
The delta_0 part contributes zero, and the binomial identity
E[2r(m-r)/m]=(m-1)/2 gives the displayed sum. Cancellation when collecting
knots can only decrease this upper bound.

Let

    n=2^28,  u=267/200,  h=3/200,
    lambda=(n+1)/u=53687091400/267.

If Z has the Gamma law with shape n+1 and rate lambda, then
E Z=u and Var Z=u^2/(n+1). The interval in (7) is exactly [u-h,u+h].
Chebyshev's inequality and (7)-(8) give

    Pr(|Z-u|>h)<=7921/(n+1),
    E A(Z)<=-1/125+(128+1/125)*7921/(n+1)
            =-141691536/33554432125<0.                           (9)

Writing F(tau)=B(tau)/tau^2, differentiation of (5) is legitimate to every
finite order because A is bounded. The Gamma density gives

    (-1)^n F^(n)(lambda)
        =integral_0^infinity t^n exp(-lambda t) A(t) dt
        =[n!/lambda^(n+1)] E A(Z)<0.                            (10)

No factorial, huge polynomial or derivative expansion is computed. The
certificate stores n and lambda and verifies the rational inequality (9).
The derivative order is deliberately conservative and is not an optimized
mathematical threshold.

Every Laplace transform of a nonnegative measure, finite for all tau>0,
has nonnegative alternating derivatives. Differentiation follows by bounding
t^n exp(-lambda t) by a constant times exp(-lambda t/2). Thus (10) proves:

**Proposition.** B(tau)/tau^2 is not completely monotone, and there is no
nonnegative Borel measure sigma on [0,infinity) with

    B(tau)/tau^2=integral exp(-tau t) sigma(dt)  for every tau>0.  (11)

This excludes all such positive measures, not just the explicit density A.
It is an exact obstruction after the complete endpoint difference and
prior-weight averaging. It does not exclude non-Laplace positive features,
a representation depending on tau, or a proof retaining signed scatter
cancellations.

## 5. The actual beta remains strictly positive at every variance

On[0,1] let

    U(v)=((1-v)^9-1+9v)/72,   U''(v)=(1-v)^7.

The function is strictly convex on [0,1], with U(0)=U'(0)=0, and

    B(tau)=8 C_s integral[U(g_s/C_s)-U(f_s/C_s)].                 (12)

The two translated normalized Gaussians are different outside the null
plane {x_1=0}. Strict Jensen convexity therefore gives

    integral U((gamma_s(.-e_1)+gamma_s(.+e_1))/(2C_s))
       <(1/2) integral U(gamma_s(.-e_1)/C_s)
        +(1/2) integral U(gamma_s(.+e_1)/C_s)
        =integral U(gamma_s/C_s).

These integrals are finite since U(v)=O(v^2) near zero. Hence B(tau)>0
for every tau>0. The same elementary collapse is already a known positive
majorisation case; it is used as a control, not claimed as a new subclass.

The proposition refutes the attempted sufficient representation (11),
not the Gaussian-majorisation question. In particular the generally
unsigned b_(7,0) and the unrestricted R3 theorem remain open.

## 6. Meaning for the current certificate chain

R8's author-side interval certificate encloses the final exponential sums
on its stated asymmetric metric region. This result does not challenge
that certificate or the reviewed q<=6 strip. It shows that extending such
calculations to all variances by demanding pointwise nonnegative integrated
scatter spectra can fail even in a fully positive two-point example.

R5's open endpoint-coupling obligation is more general than (11). The present
candidate was tested in this lane; its failure must not be attributed as
a flaw in R5's proved projection theorem or as a refutation of every possible
endpoint coupling. The complete Gaussian Laplace averaging retains useful
cancellation here, and cannot simply be replaced by nonnegativity of A.

R4's subsequent all-variance theorem for orthocentric depth-one flaps has
an accepting R7 team review. That exact family is closed; R8's nearby
nonflap region and explicit margins have separate scope. Neither statement
is a premise of this obstruction. See [SOURCES.md](SOURCES.md) for attribution.
