# The sharp paired-rank boundary for conditional beta positivity

Complete author proof with an exact finite certificate. Independent review
is pending. The full dimension-three Gaussian-majorisation problem remains
open. This result concerns the conditional kernels before their required
replica and interpolation averages.

## 1. Precise conclusion

For a finite contraction x_i -> y_i in R3, put

    Z_i(t)=(sqrt(1-t)x_i,sqrt(t)y_i),
    Q_A(t)=sum_(i in A)|Z_i(t)-mean_A Z(t)|^2.

Labels may repeat in a tuple. For a base B of p>=2 positions containing a
distinguished pair, and q additional positions C, the established
pair-conditioned beta identity uses

    K_(B,C)(t,s)=sum_(S subset C)(-1)^|S|
        (p+|S|)^(-5/2) exp[-Q_(B union S)(t)/(2s)].             (1)

Actual beta coefficients average (1) against nonnegative distinguished
pair losses and then integrate t from zero to one.

**Theorem.** Fix a nonempty finite contraction in R3, and let r be the
affine dimension of its paired sites (x_i,y_i) in R6. The following are
equivalent:

1. Every kernel (1), for every base and remaining tuple drawn with
   repetition from these sites, every t in [0,1], and every s>0, is
   nonnegative.
2. r<=5.

When r<=5, every such kernel is in fact positive. When r=6, kernels with
a positive-loss distinguished pair fail at t=1/2 and arbitrarily large
variances. No particular failing order or tuple is identified.

The explicit finite certificate below uses only the seven sites

    x=(0,+e1,-e1,+e2,-e2,+e3,-e3),
    y=(0,+e1,+e1,+e2,+e2,+e3,+e3),                            (2)

The distinguished pair can be +e1,-e1, of squared loss 4. Seven sites are
therefore the exact minimum support size for failure of this uniform
pointwise-kernel property: six paired sites have affine rank at most five.
This is not a minimum support theorem for majorisation counterexamples.

The proof gives a finite exact obstruction: a 36-by-36 joint moment matrix
has an integer coefficient vector with quadratic value -1. It proves the
existence assertion in the theorem, but **does not specify a negative
kernel's order, multiplicities or variance, or give an order bound**.
Those parameters are obtained existentially through the multivariate
Bernstein theorem and finite-difference convergence.

Every actual Gaussian beta for (2) is nonnegative for every choice of prior
weights and variance, by the elementary isometric-mixture argument below.
Thus this is neither a negative beta nor a majorisation counterexample.
The [earlier instantaneous-lift obstruction](../gaussian_majorisation_local_lift_obstruction/PROOF.md)
already refuted unrestricted pointwise positivity. The additional statement
here is the sharp classification for each finite paired geometry, with a
small algebraic certificate. R8's finite seven-factor positivity theorem
is not contradicted or independently audited here.

## 2. An admissible rank-six cloud

The map (2) is coordinatewise absolute value on its support and hence is
1-Lipschitz. Of its 21 unordered pairs, the three opposite-axis pairs
have squared loss 4, and all eighteen other pairs have loss zero.

At t=s=1/2, subtract the centroid of the base pair +e1,-e1 and divide by
sqrt(s). The resulting seven vectors in R6 are

    w0=(0,0,0,-1,0,0),
    w1=(1,0,0,0,0,0),       w2=(-1,0,0,0,0,0),
    w3=(0,1,0,-1,1,0),      w4=(0,-1,0,-1,1,0),
    w5=(0,0,1,-1,0,1),      w6=(0,0,-1,-1,0,1).

The coordinate list is also in [CERTIFICATE.json](CERTIFICATE.json).
Put v_i=w_i-w0, 1<=i<=6. Directly,

    v_i.v_j=2 delta_ij.                                      (3)

Consequently the seven sites have affine rank six. This is an actual
paired contraction cloud with a positive-loss base pair, rather than an
arbitrary six-dimensional configuration substituted for physical data.

Define S=sum_(i=0)^6 t_i and the analytic normalized function

    Phi(t)=(1+S/2)^(-5/2)
       exp[-(sum_i t_i|w_i|^2)/2
                     +|sum_i t_i w_i|^2/(2(2+S))].            (4)

It is positive on the nonnegative orthant and Phi(0)=1. Equation (4) is
the conditional Gaussian factor for the p=2 base, after removing the
constant base scatter and normalizing the value at zero. The variables
t_i are formal continuous replica weights, not prior probabilities.

## 3. A finite negative square

For a polynomial in seven indeterminates Y=(Y0,...,Y6), define the linear
functional

    L(Y^a)=(-1)^|a| partial^a Phi(0).

Let

    P(Y)=4Y0-sum_(i=1)^6 (1+Y0-Yi)^2
        =-6-8Y0+2sum_i Yi-6Y0^2
                                  +2Y0 sum_i Yi-sum_i Yi^2.  (5)

The central exact certificate is

    L(P^2)=-1.                                               (6)

Here are two ways to verify the finite identity.

First expand (4) through total degree four, using rational power series.
For the 36 monomials Y^a of total degree at most two, form

    M_(a,b)=(-1)^|a+b| partial^(a+b) Phi(0).

All entries are rational. The integer vector of coefficients in (5) has
v^T M v=-1. [verify.py](verify.py) computes every Taylor coefficient through
degree four, reconstructs the full matrix, and checks this equality.
The canonical matrix hash is

    5a4184e0e5125adc397baa7fedaa49ed866de805a36d4eda23403832600bc373.

Second, the following formal-polynomial derivation explains the sign.
Let Z be a six-dimensional Gaussian with covariance I/2. Independently
adjoin a **formal linear functional**, not a probability law, on a symbol R:

    ell(R^k)=(-1/2)_k / 2^k.

Its formal Laplace series is (1+u/2)^(1/2). Gaussian square completion gives

    E exp[-sum_i t_i |Z-w_i|^2/2]
       =(1+S/2)^(-3)
         exp[-sum_i t_i|w_i|^2/2
                         +|sum_i t_i w_i|^2/(2(2+S))].

Multiplication by the formal R series identifies the Taylor functional L
with the substitution

    Yi=R+|Z-w_i|^2/2.                                        (7)

Only coefficients through degree four are needed. No negative-shape Gamma
random variable, distributional inverse transform, or positive measure is
assumed to exist.

For (7), 1+Y0-Yi=v_i.(Z-w0). By (3),

    sum_(i=1)^6 (1+Y0-Yi)^2=2|Z-w0|^2,
    P(Y)=4R.

Therefore

    L(P^2)=16 ell(R^2)=16*(-1/2)*(1/2)/4=-1,

proving (6). The code separately expands the polynomial substitution and
verifies P(Y)=4R, without using its Taylor-matrix calculation. This is a
second author calculation, not an independent mathematical review.

As normalization controls, replacing 5/2 in (4) by 3 makes L(P^2)=0,
and replacing it by 7/2 makes L(P^2)=3. Those values correspond to residual
shapes zero and positive one half, respectively, and are checked exactly.

## 4. Phi has no common positive Laplace measure

Suppose a nonnegative Borel measure rho on [0,infinity)^7 represented Phi:

    Phi(t)=integral exp(-t.Y) rho(dY),  t_i>0.                 (8)

By monotone convergence and Phi(0)=1, rho has total mass one. At any
positive t its mixed derivatives are the corresponding exponentially
weighted moments. Letting t approach zero through positive equal
coordinates and using analyticity of (4) shows that every required moment
through degree four is finite and equals L(Y^a). Thus

    integral P(Y)^2 rho(dY)=L(P^2)=-1,

which contradicts nonnegativity of the integrand. This proves directly
that (8) is impossible.

The multivariate Bernstein--Hausdorff--Widder--Choquet theorem identifies
complete monotonicity on the positive orthant with representations (8).
See Scott--Sokal, Theorem 2.2, in the
[authors' primary manuscript](https://people.maths.ox.ac.uk/scott/Papers/compmono.pdf).
Consequently Phi is not completely monotone: some finite mixed derivative
has the wrong alternating sign at a strictly positive argument. This
classical representation theorem is an explicit external premise for the
next step, not part of the finite arithmetic certificate.

## 5. From the obstruction to actual finite conditional kernels

This step retains the admissible geometry and the positive distinguished
pair. It does not infer a Gaussian beta sign from a kernel sign.

Fix any a in the nonnegative orthant and a multi-index k of total degree
q. Let epsilon=1/n and choose nonnegative integers m_i with

    a_n=(m_0/n,...,m_6/n) -> a.

In the original support (2), make a base B_n consisting of n copies each
of +e1 and -e1, plus m_i copies of site i. Designate one +e1,-e1 pair;
its loss is 4. The base length is p_n=2n+sum_i m_i. Make the remaining
q-position tuple C_k with k_i copies of site i. Work at interpolation
time 1/2 and Gaussian variance s_n=n/2.

To verify the exact scaling, write u_i=(x_i,y_i) in R6. At t=1/2 and
s_n=n/2, Z_i/sqrt(s_n)=sqrt(epsilon)u_i. Translate by the original base
centroid and use w_i from Section 2. The first 2n positions have mean zero
and scaled scatter 2. If r_i further labels are included, their full
scatter is

    2+sum_i (a_n,i+epsilon r_i)|w_i|^2
       -|sum_i(a_n,i+epsilon r_i)w_i|^2
                                 /(2+sum_i(a_n,i+epsilon r_i)).

Their cardinality is epsilon^(-1)[2+sum_i(a_n,i+epsilon r_i)].
Consequently the exact conditional kernel (1) is

    K_(B_n,C_k)(1/2,s_n)
      = epsilon^(5/2) exp(-1) 2^(-5/2)
         sum_(r<=k) (-1)^|r| [product_i binom(k_i,r_i)]
                                         Phi(a_n+epsilon r). (9)

Suppose all such conditional kernels were nonnegative. The prefactor in
(9) is positive, so all displayed alternating differences would be
nonnegative. Divide by epsilon^q and let n tend to infinity. The ordinary
finite-difference formula and analyticity give

    (-1)^q partial^k Phi(a)>=0

for every a>0 and every multi-index k. This would make Phi completely
monotone, contradicting Section 4. Hence a finite n, m and k yield a
strictly negative kernel in (9). This proves the seven-site assertion;
the next section treats every finite paired geometry.

The implication is existential. The 36-by-36 matrix certificate does not
identify which derivative, discrete order or replica tuple fails. In
particular it does not locate the first failure just beyond an existing
positive diagonal. It does show that a proof requiring positivity of
**every** individual conditional kernel cannot establish the unrestricted
beta hierarchy. A successful approach must keep additional averaging or
use a different sign mechanism.

## 6. Complete the sharp rank classification

First suppose the paired affine rank is at most five. At every lift time,
all centers lie in an affine space of dimension at most five. Subtract
the base centroid and embed the resulting vectors w_i in R5. Gaussian
square completion gives

    K=exp[-Q_B/(2s)] (2pi s)^(-5/2)
        integral_R5 exp[-p|u|^2/(2s)]
                     product_(i in C)(1-exp[-|u-w_i|^2/(2s)]) du >0.

This is the existing Gaussian-product positivity argument. The integrand
is positive off finitely many points, including when labels coincide.
It proves the sufficient direction with all orders and variances at once.

Now suppose the paired rank is six. Choose seven affinely independent
paired sites. Some pair among them has positive squared distance loss:
otherwise the restriction preserves all distances, hence is the restriction
of a Euclidean isometry, and its paired affine rank is at most three.
Use that positive-loss pair as the two-position base. At t=s=1/2, let
w_0,...,w_6 be their dimensionless paired coordinates relative to its
centroid. The six vectors v_i=w_i-w_0 are linearly independent. Write

    G_ij=v_i.v_j,       d_i=|v_i|^2/2,
    r_i(Y)=Y0-Yi+d_i,
    R_G(Y)=Y0-(1/2) r(Y)^T G^(-1) r(Y).                     (10)

Define Phi by (4) with these new w_i. The formal Gaussian calculation
of Section 3 remains unchanged. Under Yi=R+|Z-w_i|^2/2,
r_i(Y)=v_i.(Z-w_0), so positive definiteness of G gives

    r^T G^(-1)r=|Z-w_0|^2,
    R_G(Y)=R,
    L(R_G^2)=-1/16.                                        (11)

Thus every full-rank seven-site cloud has a negative quadratic form in
its degree-two moment matrix. The integer vector (5) is a compact special
case; no enumeration over all real Gram matrices is required for (11).
For rational paired coordinates, G, R_G and the finite certificate are
rational and can be computed exactly.

Sections 4--5 now apply without a special geometric assumption. Replicate
the selected positive-loss base pair n times and the seven chosen sites
according to the finite-difference construction. Their original dimensionless
base scatter is some fixed Q_0 instead of 2; the factor exp(-1) in (9)
is replaced by exp(-Q_0/2), which is still positive. Every other term and
the cardinality scaling are identical. The negative derivative provided
by failure of complete monotonicity gives negative finite differences for
all sufficiently large n. Therefore the associated conditional kernels
are negative at variances s_n=n/2, which are arbitrarily large.

This proves necessity and the asserted classification. A finite constant
number of positive beta diagonals, or stronger margins on them, cannot
remove this boundary on any full-rank paired configuration. The result
does not obstruct proofs retaining the replica and time averages, nor
does it classify endpoint majorisation by paired rank.

## 7. The actual seven-site contraction is positive

For any prior weights on (2), group the +ei and -ei weights into W_i;
retain the mass W_0 at zero. For each of the eight sign choices
sigma in {+1,-1}^3, put mass W_i at sigma_i ei and W_0 at zero.
Coordinate reflection maps this four-site law isometrically to the same
target law, of mass W_i at +ei. Choose the sign independently with
probabilities w_(+i)/W_i and w_(-i)/W_i whenever W_i>0; ignore zero groups.
The corresponding convex mixture of the eight source laws is the original
prior. Their Gaussian convolutions are congruent to the common target
convolution. Jensen's inequality, followed by integration, therefore gives
majorisation of the mixture by the target at every variance.

This is the standard common-target convexity argument, used as a known
positive control. With all seven weights positive, distinct reflected
densities occur, so every beta energy with curvature u^j(1-u)^q has a
strictly positive endpoint gap. The negative conditional kernel provided
by Section 5 is compensated in the complete replica/time average.

## 8. Scope and certificate trust

The finite certificate verifies 21 exact pair contractions, the orthogonal
affine-difference basis, all 330 Taylor coefficients through degree four,
the 36-by-36 rational moment matrix and its integer negative vector, and
the independent polynomial substitution. It uses no floating-point sign,
solver, numerical integral, hidden source file or large certificate.
Three altered compact records are rejected. Standard-library Python
integer/Fraction arithmetic is the implementation trust boundary.

Gaussian square completion, the formal-series identity, the classical
multivariate Bernstein theorem, and the discrete scaling/limit remain
written analytic premises. Independent review is pending. The unrestricted
Gaussian conjecture, actual higher beta signs and the endpoint Hankel
condition 3d2d4>=2d3^2 remain open. No new Kneser--Poulsen theorem or
historical-priority claim is made.
