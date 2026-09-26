# Same-volume averaging does not cover the mixed source tests

Complete author proof, 26 September 2026; independent review is pending.
This note tests a specific possible bridge from the
[isometric-reference theorem](../gaussian_isometric_reference/PROOF.md)
to the full Gaussian question on the [uniform lattice sets](PROOF.md).
Even the closed convex hull of all isometric-reference source tests can
miss a mixed law's maximizing source test by a fixed positive amount.
The example itself satisfies full Gaussian majorisation by a known
continuous contraction. There is no counterexample to the conjecture.

## 1. The coverage question and the result

For a contraction T on a compact set E, a reference probability sigma
is called isometric here if T agrees with an ambient Euclidean isometry
on supp(sigma). At a prescribed volume v>0 its reference source test is
the unique Gaussian superlevel set

    C_sigma = {sigma*gamma_1 > h_sigma},    |C_sigma|=v.

Researcher 5's isometric-reference theorem proves the common-set
comparison for every such source test and every actual prior on E.
One possible extension would approximate an arbitrary maximizing source
indicator by positive averages of these indicators at the same volume.
The following rules out that coverage step, including arbitrarily small
approximation error, on one member of the full-question reduction class.

Let Q=[-1/2,1/2]^3 and e=(1,0,0), and set

    E=(-8e+Q) union (8e+Q),
    F=(-4e+Q) union (4e+Q),
    T(-8e+u)=-4e+u,    T(8e+u)=4e+u,    u in Q.

Let mu=1_E/2, f=mu*gamma_1, a=1/100, A={f>a}, and v=|A|.
Write V_v for the L1-closed convex hull of indicators of **all** convex
measurable sets of volume v in R3. In particular it contains the closed
convex hull of all the isometric-reference source tests for this E,T.

**Proposition.** The map T belongs to the strict whole-cube class of
PROOF.md, and 0<v<infinity. For every phi in V_v,

    ||1_A-phi||_1 >= 1/12.                                 (1)

There is also a constant epsilon_0>0, depending only on this fixed f,a,
such that for every phi in V_v,

    integral_A f - integral phi f >= epsilon_0.             (2)

Both statements hold for arbitrary well-defined probabilistic averages
of the reference indicators, as well as L1 limits of finite averages.
They do not merely concern a finite choice of reference laws. Moreover,
mu*gamma_s is majorised by (T#mu)*gamma_s for every s>0. Thus the
obstruction is to the indicated source-test coverage mechanism, even
within a known positive example.

## 2. All the isometric-reference tests are convex

For points in different source cubes, with offset difference h in [-1,1]^3,
the squared-distance loss is

    |16e+h|^2-|8e+h|^2 = 192+16 h_1 >=176>0.               (3)

Therefore an isometric reference cannot have support in both cubes.
Every such sigma is supported on a translate of Q. This includes singular
and arbitrarily distributed reference laws, not only the uniform cube law.

For p=sigma*gamma_1 the posterior law at z is

    d sigma_z(x) = gamma_1(z-x) d sigma(x) / p(z).

Direct differentiation under the compact-support integral gives

    Hess log p(z) = -I + Cov_(sigma_z)(X).                  (4)

For a unit vector b, the range of b.X on a unit cube has length at most
sum_j |b_j| <= sqrt(3). A real random variable in an interval of length L
has variance at most L^2/4: expand E[(Z-m)(M-Z)]>=0 and maximize
(E Z-m)(M-E Z). Hence (4) implies

    Hess log p(z) <= -(1/4) I                              (5)

as quadratic forms, uniformly over z and over these reference laws.
Every positive superlevel set of p is consequently convex.

Compact Gaussian mixtures are positive, analytic and tend to zero at
infinity. Every positive level set has measure zero, because the mixture
minus that level is a nonzero real analytic function. Their superlevel
volumes vary continuously and strictly from infinity to zero, so the
prescribed-volume test is well defined. Its uniqueness is the usual
threshold comparison obtained by integrating (1_C-1_D)(p-h).

## 3. Exact separated-box bounds at a rational threshold

Put P=[-1/4,1/4]^3 and P_+=8e+P, P_-=-8e+P. Their common volume is
V=1/8. We prove, using only elementary inequalities, that

    P_+ union P_- is contained in A,    P is disjoint from A. (6)

Let c=(2pi)^(-1/2) and

    k(t)=integral_(-1/2)^(1/2) c exp(-(t-u)^2/2) du.

Since pi<4 and exp(-r)>1-r for r>0,

    k(0)> (1/3)(7/8)=7/24.

Symmetry of the probability density proportional to exp(-u^2/2) on
[-1/2,1/2] gives

    k(t)/k(0)=exp(-t^2/2) E exp(tU) >= exp(-t^2/2).

Here E exp(tU)=E cosh(tU)>=1. For w in P, keep just the nearby half of
the mixture at either 8e+w or -8e+w. The other half is positive. Thus

    f(plus-or-minus 8e+w)
      >= (1/2) product_j k(w_j)
      >= (1/2) exp(-3/32) k(0)^3
      > (29/64)(7/24)^3
      = 9947/884736 > 1/100.                              (7)

For z in P and x in either source cube, |z_1-x_1|>=29/4. Bounding the
other two Gaussian factors by c, then averaging over either cube, gives

    f(z) <= c^3 exp(-841/32)
          < exp(-5) < (3/8)^5 = 243/32768 < 1/100.         (8)

We used c<1 and exp(1)>1+1+1/2+1/6=8/3. This proves (6) without numerical
Gaussian integration. In particular v is positive, and it is finite
because f tends to zero at infinity. Its threshold level is null by
analyticity, so A is the unique maximizing volume-v source set.

## 4. Uniform separation from convex sets and their averages

Let C be any convex measurable set of volume v and write

    delta=|A minus C|=|C minus A|.

Define U_+=(C intersect P_+)-8e and U_-=(C intersect P_-)+8e. They are
subsets of P, each of volume at least V-delta by (6). Inclusion-exclusion
therefore gives

    |U_+ intersect U_-| >= V-2delta.

For w in that intersection, both w+8e and w-8e belong to C, so convexity
puts their midpoint w in C. But w is in P, which is disjoint from A.
Consequently

    delta >= |U_+ intersect U_-| >= V-2delta,
    |A symmetric-difference C|=2delta >= 2V/3=1/12.        (9)

This argument needs no assertion about the shape or connectedness of A
outside the three displayed boxes.

If phi=sum_j lambda_j 1_(C_j), with lambda_j>=0 and sum_j lambda_j=1,
then 0<=phi<=1 and integral phi=v. More importantly, since 1_A takes
only the values zero and one,

    ||1_A-phi||_1 = sum_j lambda_j |A symmetric-difference C_j|. (10)

Equations (9)--(10) prove (1) for finite averages, and L1 continuity proves
it on V_v. Tonelli proves the same identity for any measurable probability
mixture of such indicators. This is a lower bound on every possible
same-volume convex average, not just on the best single reference test.

To prove (2), choose 0<eta<a/2 such that

    |{z: |f(z)-a|<eta}| < 1/24.                           (11)

Such an eta exists: these sets are contained in the bounded superlevel
{f>a/2}, and their decreasing intersection is the null set {f=a}.
Every phi in V_v still satisfies 0<=phi<=1 and integral phi=v. Therefore

    integral_A f - integral phi f
       = integral |1_A-phi| |f-a|
       >= eta (1/12-1/24) = eta/24.                       (12)

The first equality uses equal volumes and the signs on A and its
complement. The estimate uses (1), (11), and |1_A-phi|<=1. Thus one may
take epsilon_0=eta/24. No explicit numerical value of eta or of v is
claimed or needed for this uniform positive separation.

## 5. Why this is a coverage obstruction, not a negative comparison

For t in [0,1] translate the two cubes to centers plus-or-minus (8-4t)e,
keeping their internal offsets fixed. Same-cube distances are constant.
The derivative of a cross-cube squared distance is

    d/dt |(16-8t)e+h|^2 = -16(16-8t+h_1) <= -112<0.

This is a continuous contraction in R3. Aishwarya--Li's
[Theorem 1.4](https://arxiv.org/html/2609.07041v2)
therefore gives the full Gaussian comparison for every law on E, in
particular mu, at every variance. The example is entirely within the
known positive frontier.

The reference theorem remains valid without modification. If one keeps
only its inequalities C_(g_mu)(v)>=integral_C f_mu and averages them,
the resulting lower bound is integral phi f_mu for a same-volume source
average phi. For the displayed actual mu, the supremum of all those
lower bounds is at most C_f(v)-epsilon_0. Thus that loss-free coverage
step cannot reach the required mixed-law source value.

This averaging differs from the earlier
[common-target decomposition](../gaussian_majorisation_common_target/PROOF.md).
That argument averages source laws with one common target density and
uses convexity of internal energy. Here the actual law is fixed and the
objects being averaged are volume-v source-test indicators. The present
separation does not obstruct that different mechanism.

This does NOT rule out retaining quantitative reference slack, joint
target-set constructions, nonconstant spatial coefficients, or decompositions
with different volumes and additional overlap estimates. Those operations
are absent from (10), and would need their own proof. In particular the
statement is not that the isometric-reference theorem cannot contribute
to a solution. It says precisely why positive averaging of its source
tests at one volume is insufficient as the missing localization bridge.

The note neither proves a new positive map class nor creates a new
normal form for hypothetical failures. It closes this proposed coverage
step on the uniform-set frontier. The rigid-packet interaction sign in
PROOF.md and the unrestricted dimension-three conjecture remain open.

The proof is analytic and geometric. Its rational constants can be
checked directly; no quadrature, optimizer, solver, search output or
external certificate is a premise. The isometric-reference theorem is
used to identify the safe-test family and its existing comparison, not
to establish the separation (1)--(2), which holds for all convex sets.
Author verification is not independent mathematical acceptance.
