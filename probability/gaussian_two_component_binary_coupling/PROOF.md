# A common binary channel for two rigid Gaussian components

27 September 2026. Complete author proof; independent review is pending.
This is an actual-field comparison at every positive variance. It does
not establish Gaussian density majorisation, the two-body joint-superlevel
inequality, or a Kneser--Poulsen theorem. No historical priority is claimed
for the Gaussian interpolation or binary experiment arguments.

## 1. Statement and quantifiers

Let mu_A and mu_B be boundedly supported Borel probability measures on
R^d, where d>=1. Let I_A and I_B be Euclidean isometries and suppose

    |I_A(a)-I_B(b)| <= |a-b|
                 for every a in supp(mu_A), b in supp(mu_B).       (1)

If the supports overlap, (1) forces the two images to agree on their
intersection. Together the two isometries therefore define a contraction
on the union of the supports.

For one arbitrary common variance s>0, write

    f_A = mu_A * gamma_s,         g_A = (I_A#mu_A) * gamma_s,
    f_B = mu_B * gamma_s,         g_B = (I_B#mu_B) * gamma_s,        (2)

where gamma_s(x)=(2 pi s)^(-d/2) exp(-|x|^2/(2s)).

**Theorem.** There is a Markov kernel K from R^d to R^d such that

    (f_A dx) K = g_A dy,          (f_B dx) K = g_B dy.              (3)

The same K therefore maps lambda f_A+(1-lambda)f_B to
lambda g_A+(1-lambda)g_B for every lambda in [0,1]. It may depend on
the two entire component laws, the two isometries, and s. It is not
claimed to work simultaneously after either component law is changed.

Equivalently, all binary testing thresholds have the sign

    integral min(alpha g_A, beta g_B)
       >= integral min(alpha f_A, beta f_B)       (alpha,beta>=0), (4)

or, in stop-loss form,

    integral (g_A-t g_B)_+ <= integral (f_A-t f_B)_+     (t>=0).   (5)

In particular every convex f-divergence between the two component laws
decreases. More explicitly, for a convex real-valued function psi on
(0,infinity),

    integral g_B psi(g_A/g_B) <= integral f_B psi(f_A/f_B).         (6)

An affine supporting function can first be subtracted from psi, so this
statement has an unambiguous meaning even if one side is infinite.

There is no equality of anchored norms in the hypotheses, no motion
premise, no bound on the number of atoms, and no restriction on the
positive common variance. The conclusion includes the paired-rank-six
screw fixture discussed in Section 6.

## 2. A Gaussian interpolation identity with exact norm cancellation

First consider finitely supported component laws with positive atom
weights. Zero weights may be discarded. Rescaling x by sqrt(s) reduces
to s=1: both sides of (4) are invariant under this change of variables.
Label all atoms by i, keeping the two blocks disjoint as labels. Write
p_i for the source centre and q_i for its image. Put

    n_i = |p_i|^2-|q_i|^2,
    delta_ij = |p_i-p_j|^2-|q_i-q_j|^2.                            (7)

Thus delta_ij=0 within a block, and delta_ij>=0 between blocks. The
origin used to define n_i is arbitrary. We do not assume n_i=0 or
that another pair of origins would make every n_i vanish.

Let Phi be a C^2 function on the positive quadrant, homogeneous of
degree one, and set

    A(z)=sum_(i in A) w_i exp(z_i),
    B(z)=sum_(j in B) w_j exp(z_j),
    F(z)=Phi(A(z),B(z)).                                          (8)

For the functions used below, F and its first two derivatives are
bounded in absolute value by a constant times A+B. This is sufficient
for every differentiation and expectation in this section.

Let P and Q have columns p_i and q_i. For 0<=u<=1 choose a Gaussian
vector Z_u in R^N with mean and covariance

    m_(u,i) = -[(1-u)|p_i|^2+u|q_i|^2]/2,
    Gamma_u = (1-u) P^T P + u Q^T Q.                              (9)

These matrices are positive semidefinite. They need not have rank d,
and no path of configurations in R^d is asserted. One realization is

    Z_u = sqrt(1-u) P^T X + sqrt(u) Q^T Y + m_u,

with independent standard Gaussian vectors X,Y in R^d. At the two
endpoints, degree-one homogeneity and the standard Gaussian density
give the exact identities

    E F(Z_0) = integral Phi(f_A(x),f_B(x)) dx,
    E F(Z_1) = integral Phi(g_A(x),g_B(x)) dx.                      (10)

Indeed, f_A(x)=gamma_1(x) A(P^T x-(|p_i|^2/2)_i), and similarly
for B. The common factor gamma_1(x) can be taken outside Phi.

Differentiation of a Gaussian expectation, or integration by parts
in the displayed realization with X,Y, yields on 0<u<1

    d/du E F(Z_u)
      = (1/2) E [sum_i n_i F_i
                    + sum_ij (Q^T Q-P^T P)_ij F_ij].             (11)

This formula also holds when Gamma_u is singular; the proof by
integration by parts uses no inverse covariance. Its two ingredients are

    (P^T P-Q^T Q)_ij = (n_i+n_j-delta_ij)/2,
    sum_j F_ij = F_i.                                            (12)

The second identity follows by differentiating
sum_j F_j=F, the Euler identity in logarithmic coordinates.
Symmetry of the Hessian now cancels all norm terms in (11):

    d/du E F(Z_u)
       = (1/2) E sum_(i<j) delta_ij F_ij(Z_u)
       = (1/2) E sum_(i in A,j in B)
                     delta_ij w_i w_j exp(Z_(u,i)+Z_(u,j))
                                  Phi_AB(A(Z_u),B(Z_u)).         (13)

The factor 1/2 in (13) uses unordered pairs. In particular the derivative
is nonnegative whenever Phi_AB>=0. No sign of an individual n_i was
used. This is the decisive identity.

For completeness the stated bounds on F and its derivatives make the
right side of (11) uniformly integrable: E exp(Z_(u,i))=1 for every
u. For a fixed finite configuration the explicit X,Y realization also
gives an integrable exponential bound for these derivatives on [0,1].
Differentiate on compact subintervals of (0,1), integrate (13), and use
dominated convergence at the endpoints. This justifies the integrated
inequality without a nonsingular covariance or a hidden cutoff.

## 3. All testing thresholds

For 0<epsilon<4 define the smooth degree-one approximation

    Phi_epsilon(a,b)
       = [a+b-sqrt((a-b)^2+epsilon a b)]/2.                       (14)

It satisfies 0<=Phi_epsilon<=min(a,b) and converges to min(a,b)
as epsilon decreases to zero. With
Q_epsilon=(a-b)^2+epsilon a b, direct differentiation gives

    (Phi_epsilon)_AB
       = epsilon(4-epsilon) a b / (8 Q_epsilon^(3/2)) > 0.        (15)

This formula includes the factor 1/8. One way to check it without
radicals is

    (Q_epsilon)_A (Q_epsilon)_B
            -2 Q_epsilon (Q_epsilon)_AB
       = epsilon(4-epsilon) a b.                                 (16)

All derivatives needed in Section 2 have the claimed bounds. To see
this, normalize a+b=1. The quadratic Q_epsilon is strictly positive
on that compact segment, including its endpoints. Homogeneity then
bounds Phi_epsilon, a Phi_A, b Phi_B, a^2 Phi_AA,
ab Phi_AB, and b^2 Phi_BB by C_epsilon(a+b). The logarithmic
derivatives of F are sums of these quantities with coefficients in
[0,1].

Apply (13) to Phi_epsilon(alpha a,beta b), with alpha,beta>0.
The same positive cross derivative gives the integrated inequality.
Dominated convergence, using min(alpha f_A,beta f_B)<=alpha f_A,
then proves (4). If alpha or beta is zero, (4) is equality.
Finally, (a-tb)_+=a-min(a,tb) and each A density has mass one,
which proves (5).

For boundedly supported laws, separately approximate each component
by finitely supported laws with atoms in its support. For example,
partition a containing compact set into sets of diameter tending to
zero and choose a support point in each nonempty cell. The resulting
Gaussian mixtures converge in L1, as do their rigid images. This follows
directly from L1 continuity of translations of gamma_s; one may use

    ||gamma_s(.-a)-gamma_s(.-b)||_1
         <= sqrt(2/pi) |a-b|/sqrt(s).                             (17)

All selected cross pairs still satisfy (1). The inequality

    |min(alpha a,beta b)-min(alpha c,beta d)|
                      <= alpha|a-c|+beta|b-d|

therefore passes (4) to the limit. No density or boundary regularity
of the component measures is assumed.

## 4. Constructing one kernel for both component laws

All four Gaussian densities are strictly positive. Under the probability
law f_B(x)dx define R=f_A(x)/f_B(x), and under g_B(y)dy define
U=g_A(y)/g_B(y). Both variables are positive, integrable, and have
mean one. Equation (5) says

    E(U-t)_+ <= E(R-t)_+                         for every t>=0.   (18)

For negative t both sides equal 1-t. The stop-loss characterization of
one-dimensional convex order thus gives U <=_cx R. Strassen's martingale
coupling theorem supplies a joint probability eta(dr,du) with the
specified marginals and

    E[R | U]=U.                                                   (19)

This is the direction of the conditional expectation needed here.
The finite-first-moment version suffices; no bounded likelihood ratio
or finite entropy is needed. A primary modern statement is Theorem 1.1
of Leskela--Vihola, linked in SOURCES.md.

Disintegrate f_B(x)dx over its likelihood ratio r, and g_B(y)dy over
its likelihood ratio u. Conditional on (r,u) sampled from eta, sample
x and y independently from these two conditional measures. Standard
Borel disintegration applies on R^d. The resulting joint measure pi
has marginals f_B dx and g_B dy, and

    E_pi[f_A(x)/f_B(x) | y] = g_A(y)/g_B(y).                       (20)

To verify (20), condition first on u. The conditional law of y depends
only on u, and (19) gives the conditional mean of r; also u equals
g_A(y)/g_B(y) almost surely by construction.

Now disintegrate pi by x to obtain K(x,dy). Its unweighted second
marginal is g_B dy. Weighting pi by f_A(x)/f_B(x) leaves first marginal
f_A dx and, by (20), makes the second marginal g_A dy. Thus this
single K proves both identities in (3). Values on an f_B-null set
can be filled by any fixed probability measure; this also changes
nothing for f_A because both densities are strictly positive.

Conditional Jensen applied to (20) proves (6). Conversely (3) implies
(5) by the data-processing inequality for stop losses, or by the same
conditional Jensen argument. Hence (3)--(5) are equivalent here.

## 5. Exact boundary with the campaign's open criterion

The theorem proves an unrestricted threshold comparison for the
**likelihood ratio of two component laws under a probability base law**.
The campaign's density majorisation instead concerns density values
under Lebesgue measure, or the failure-coupling criterion in the
[global criterion](../gaussian_majorisation_global_criterion/PROOF.md).
No Lebesgue transport property is asserted for (3). In fact a
Lebesgue-preserving **forward** kernel would give the opposite convex
energy inequality by Jensen. The binary comparison orders information
about the component label; it is not the density-value coupling needed
for concentration of their mixture.

In the notation of the accepted
[two-body contact transfer](../gaussian_two_body_contact_transfer/PROOF.md),
put

    D(a,b)=|{g_A>a} intersect {g_B>b}|
                       -|{f_A>a} intersect {f_B>b}|.

Equation (4) proves, for every alpha,beta>0, the actual-field sign

    integral_0^infinity D(t/alpha,t/beta) dt >= 0.                 (21)

Tonelli applied separately to the two nonnegative overlap integrals
proves this identity. Both integrals are finite. Thus any adverse
joint-superlevel datum at this common variance must be compensated
elsewhere on its ray. We have not proved D(a,b)>=0 pointwise.
In particular (21) does not sign the different interaction integral

    integral_0^h D(t/lambda,(h-t)/(1-lambda)) dt,                  (22)

which is the missing hinge for a mixture prior 0<lambda<1. The accepted
transfer theorem quantifies over all joint thresholds and permits
unequal component variances; neither extension is asserted here.
There is no new Kneser--Poulsen consequence in this packet.

The previously established
[prior-independent Gaussian-channel obstruction](../gaussian_markov_intertwining/PROOF.md)
is also respected. Here K is constructed anew for each **pair of fixed
component laws**. It is uniform only over the one mixing parameter
lambda. A common kernel for all underlying atomic priors is a stronger
quantifier and is not provided. The positive result does not reopen that
closed universal-channel mechanism.

## 6. An actual unequal-anchored-norm control

INPUTS.json copies the eight rational centres from the accepted two-body
transfer packet. The A isometry is the identity. The B isometry is

    I_B(x,y,z)=(-y,x,z+1).                                       (23)

Both four-point blocks affinely span R^3. Within-block distances are
unchanged, and the sixteen cross squared-distance losses are

    10   2   4   2
     0  16   2   8
     9   1   5   5
     1  17   5  13.                                              (24)

The paired (p_i,q_i) configuration has affine rank six. At the displayed
origins the squared-norm offsets are (0,0,0,0,3,3,1,3).
Moreover **no pair of anchors makes all eight norms equal**. The four
independent A points first force the source and target anchors to be
the same point c. The four independent B points then imply
c=I_B^(-1)(c), because equality of |b-c|^2 and |I_B(b)-c|^2 on an
affine basis identifies their centres as quadratic functions of b.
The isometry (23) has no fixed point, since its third coordinate
increases by one. This proves the assertion without a numerical solve.

By the theorem, every pair of component probability laws supported on
these two finite blocks satisfies (3) at every common variance. This
is an algebraic control of the theorem's scope, not a separately
marketed sufficient class and not a numerical majorisation claim.

## 7. Reproducible checks and trust boundary

The written analytic proof establishes the universal assertion.
verify.py uses only Python integer and Fraction arithmetic. It checks
the geometry in (23)--(24), affine ranks and nonzero norm offsets;
the interpolation cancellation on a basis of all symmetric 8-by-8
Hessians; the polynomial numerator (16); and the two marginal identities
in an exact finite martingale-to-kernel control. It rejects deliberate
omission of the norm drift from (11). It does not perform Gaussian
quadrature, assume a sign from samples, construct the continuum kernel
numerically, or certify a hinge or Kneser--Poulsen inequality.

The remaining proof trust is ordinary real analysis (Gaussian integration
by parts, dominated convergence, L1 approximation), convex order,
Strassen's theorem, and standard Borel disintegration. No proof assistant
or independent reviewer has yet checked this packet.
