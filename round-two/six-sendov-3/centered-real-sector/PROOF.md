# Effective centered-real curvature and a local six-real stability supremum

Actual author **six-sendov-3**, role **researcher**, 2026-10-02.
Complete ordinary analytic argument with exact interval arithmetic;
unformalized and independently unreviewed. The validated branch and its
symmetric curvature are attributed inputs, not new results here.

## 1. Exact branch, parameters and theorem

Set `e=1/65536`, `rho=1/1024`, and let `c=cos(pi/9)`, the unique root of
`8c^3-6c-1` in `(3/4,1)`. Use the branch in author lemma9113,
[validated boundary branch](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/validated-boundary-branch/PROOF.md),
verified source `7bb2d1b6cf6cb3b370ad10023bee018128a1b81f`. Its exact tuple
`v(eta)=(x,y,T,xi3,xi4,omega)` solves the six divided polynomial equations
there throughout `[0,e]`. It lies in the true cube of radius `rho` about
the exact tuple regenerated in [initial.py](initial.py). In the notation

    a=1-eta, r=eta x, s=eta y,
    A=a-r=1-eta(1+x), D=a-s=1-eta(1+y), W=1+eta omega,

the monic polynomial has

    p'(z)=9(z-r)^6[(z-s)^2+eta T], p(a)=0,
    W^2=D^2+eta T, F(p,a)=6/A+2/W.

For `0<eta<=e`, the input proves `A,D,W,T>0`, nine simple original roots,
four original roots exactly on the unit circle and the five remaining
original roots strictly inside. It also proves stationarity of the
common-real critical family and its scalar curvature `Phi_eta''(x)>22eta^2`.
The input9113 is author-checked and currently independently unreviewed.
Its complete exact checker was replayed before this extension; a replay
is validation, not an independent verdict.

Fix any `0<eta<=e`. Allow six labelled real normalized small critical
positions `u=(u1,...,u6)` near `u0=x(eta) 1`. Define the real monic family by

    p_u'(z)=9 product_{j=1}^6(z-eta u_j)[(z-eta y)^2+eta T],
    p_u(z)=integral_a^z p_u'(w) dw.                     (1)

The two unit-root phase abscissae are `t3=-1/2+eta xi3` and
`t4=-c+eta xi4`. The two imaginary and two real circle equations, together
with `W^2-D^2-eta T=0`, determine the five tail parameters
`(y,T,xi3,xi4,omega)` locally and analytically as functions of `u`.
Existence, uniqueness and feasibility are proved below. This is a
labelled parameter family; permutations can represent the same polynomial.
No injective coefficient coordinate map at the repeated critical point
is assumed. Its literal Euclidean metric is `||u-u0||^2=sum_j(u_j-x)^2`.
Let `f_eta(u)=F(p_u,a)` and `H_eta=D_u^2 f_eta(u0)`.

**Theorem.** Throughout `0<eta<=1/65536`, `u0` is stationary and

    W_real={h in R^6: sum_j h_j=0}

is a five-dimensional eigenspace of `H_eta`, with eigenvalue `lambda_W`
satisfying the strict bounds

    eta^2(1-5eta) < lambda_W(eta) < eta^2(1-3eta).       (2)

The complementary common-real eigenvalue is greater than
`(11/3)eta^2`. Thus `lambda_W` is the least eigenvalue of the **six-real**
Hessian, its eigenspace has exactly dimension five there, and `u0` is a
strict local minimum in this real family.

Define the local stability supremum in this same labelled real family by

    kappa_real(eta)=sup{k>=0: some R>0 satisfies
      f_eta(u)-f_eta(u0)>=k eta^2 ||u-u0||^2
      for all ||u-u0||<R in the local parameter family}.

Then

    kappa_real(eta)=lambda_W(eta)/(2eta^2),
    1/2-(5/2)eta < kappa_real(eta) < 1/2-(3/2)eta.      (3)

Every smaller nonnegative coefficient has a neighborhood at each fixed
eta. The neighborhood radius is existential and may depend on eta and
the coefficient; attainment of the supremum is not asserted. This is
relative to the branch value `f_eta(u0)`, rather than the unrestricted
global infimum. In particular, no all-complex twelve-coordinate lower
bound or identification of the branch with the global minimum on the
entire explicit interval is claimed.

The exact first asymptotic correction was already established in9033
and independently confirmed in9080:

    ell=-4441/540+(7046/135)c-(2288/45)c^2,
    lambda_W=eta^2[1+ell eta+O(eta^2)].                 (4)

This contribution makes the curvature and restricted local stability
supremum effective on the stated eta interval. It does not claim(4) as new.

## 2. Uniform five-constraint regularity and a genuine feasible family

For a real polynomial `p(z)=sum_j b_j z^j` and `t=cos(theta)`, use

    I(p,t)=sum_{j>=1} b_j U_{j-1}(t),
    R(p,t)=sum_j b_j T_j(t),

where `T_j,U_j` are Chebyshev polynomials. Then
`p(exp(i theta))=R+i sin(theta) I`. The first four equations are the
two `I` and two `R` equations at `t3,t4`. Write the first five undivided
equations as `G_c`, and set `H_c=G_c/eta`. For the common tuple, this is
exactly the first five equations in9113 and [system.py](system.py).

At eta0 the anchored primitive is `z^9-1`. Both fixed phases are ninth
roots, and the distance equation also vanishes. The same fact holds for
every nearby real `u`, so `H_c` has a removable analytic extension to0.
At a common tuple `u=x 1`, put

    B=D_(y,T,xi3,xi4,omega) H_c(eta,v).

The enclosure below, on the whole certified cube and eta interval, proves
`||I-B0^(-1)B||_infinity=beta<1`. Thus the actual block is invertible at
every branch point. The real analytic implicit function theorem gives
the five analytic tail functions in(1) at each fixed positive eta.
The positive opening, distance denominators and interior phase abscissae
persist in a sufficiently small real parameter ball.

The original roots at the branch are simple. Their local analytic
continuations preserve the marked root and the four explicitly prescribed
unit roots. The other four roots are strictly interior and remain so by
continuity; the marked root a is strictly interior and fixed. Thus all
polynomials in a sufficiently small parameter ball are legal disk-rooted
polynomials, with exactly four active original roots and zero radial slack.
Their small real reciprocal distances `a-eta u_j` stay positive. Accordingly

    f_eta(u)=sum_j 1/(a-eta u_j)+2/W(u)                 (5)

is an analytic real function. This argument supplies a pointwise parameter
radius, not an explicit uniform displacement radius.

## 3. Literal centered forcing and the normalized response

Hold the mean x fixed and set

    u=(x+delta,x-delta,x,x,x,x), sigma=delta^2,
    Delta=r-s, Bp=Delta^2+eta T, X=z-r.

Then the critical factorization in(1) is exactly

    p_u'(z)=9[(z-r)^6-eta^2 sigma(z-r)^4]
                                  [(z-s)^2+eta T].     (6)

Here the prime denotes differentiation in z. Differentiating the anchored
primitive in sigma while holding all tail parameters fixed gives the
**divided sigma forcing**

    partial_sigma p/eta^2
      =-(9/7)(X^7-A^7)-3Delta(X^6-A^6)
                                      -(9/5)Bp(X^5-A^5). (7)

The final primitive constant is minus its positive-degree coefficients
evaluated at a. No unanchored constant remains. The checker compares
every coefficient in(7) with a separate literal critical-factor product
over an exact sigma dual number, at three positive rational eta values.

Let `U=(I3,I4,R3,R4,0)` be the circle evaluations of(7) at the current
phase parameters. Applying the implicit function theorem directly to the
polynomial sigma family(6) gives an analytic tail in sigma at0; uniqueness
identifies it with the even delta family. Since `partial_sigma G_c=eta^2 U` and
`D_tail G_c=eta B`, the tail response obeys

    partial_sigma tail=eta w, B w=-U.                 (8)

At eta0, `B0` is independent of **all** nearby parameters. To see this
directly, expand the general common primitive:

    p=z^9-1+eta[9+b8(z^8-1)+b7(z^7-1)]+O(eta^2),
    b8=-9(3x+y)/4, b7=9T/7.

With `tau3=-1/2,tau4=-c`, the affine first-order equations are

    (H_c)_I,k(0,v)=b8 U7(tau_k)+b7 U6(tau_k)
                                           +xi_k U8'(tau_k),
    (H_c)_R,k(0,v)=9+b8[T8(tau_k)-1]+b7[T7(tau_k)-1],
    (H_c)_5(0,v)=2omega+2(1+y)-T.                     (9)

In the real equations the phase derivative is zero because
`T9'=9U8` and `U8(tau_k)=0`. Formula(9) proves the universal constant B0;
all25 entries are compared with separate series/dual differentiation.
The initial forcing is the phase evaluation of `-(9/7)(z^7-1)`, so it too
is independent of nearby v. The regenerated exact vectors satisfy

    w0=(0,1,0,0,1/2), B0 w0=-U0.                     (10)

Write, using divided differences rather than division of intervals,

    B=B0+eta B1, U=U0+eta U1, w=w0+eta w1.

Substitution in(8) gives the exact equation

    B w1=-U1-B1 w0.                                  (11)

The full initial vector `w1(0,v0)` is reconstructed in the cubic field
from25 first-eta-derivative block entries and five forcing entries. It
reproduces the reviewed coefficient exactly:

    6(1+x0)+2omega0-2(w1(0,v0))_omega=ell.             (12)

No numerical fit or prior expected fixture supplies these coefficients.

## 4. Covered interval arithmetic for the second mixed response

Every interval endpoint is an integer divided by `2^192`; products and
reciprocals use integer floor/ceiling for outward rounding. The positive
cubic embedding is enclosed by160 exact bisections in `(3/4,1)`.
The true cube `||v-v0||_infinity<=rho` is enclosed by a single dyadic
rectangle about outward enclosures of the exact v0. The exact eta domain
is `[0,e]`. Every segment `(t eta,v)`, `0<=t<=1`, stays in the rectangle.
There is no mesh, omitted endpoint or empirical stopping rule.

[interval.py](interval.py) extends the attributed9113 kernel by keeping
21 Taylor/dual components: eta coefficients0,1,2 and six parameter
derivatives for each eta coefficient. The new six degree2 mixed entries
are `partial_eta^2 partial_v/2`. Their multiplication includes every term

    ga2 b0+ga1 b1+ga0 b2+a2 gb0+a1 gb1+a0 gb2.

Thus exact interval automatic differentiation encloses

    Bactual = integral_0^1 G_c,eta,tail(t eta,v) dt,
    B1actual=integral_0^1(1-t)G_c,eta,eta,tail(t eta,v)dt,
    U1actual=integral_0^1 U_eta(t eta,v) dt.             (13)

The middle integral is a convex average of the mixed degree2 entry with
weight `2(1-t)`, whose integral is1. Formula(9) justifies the subtracted
constant B0 uniformly in v, rather than solely at v0. These identities
also extend through eta0. Denote the componentwise enclosures by
`Bbar,B1bar,U1bar`.

Let `Y=B0^(-1)` at the true fixed c, and let `w1star=w1(0,v0)`. Both inverse
products are verified exactly. The complete rational quantities recorded
in [expected.json](expected.json) are

    beta=bound ||I-Y Bbar||_infinity <1/50,
    R1=bound ||Y[-U1bar-B1bar w0-Bbar w1star]||_infinity,
    E1=R1/(1-beta)<9/20.

Since `Y Bactual` is invertible with inverse norm at most `1/(1-beta)`,
(11) proves

    ||w1actual-w1star||_infinity<=E1.                 (14)

The interval computation centers this response at the entire exact vector,
not at a floating approximation. It then bounds the omega component in
(14). Every field is separately recomputed with Fraction endpoint
operations rounded to the same fixed dyadic grid. That alternate arithmetic
shares the polynomial equations and jet and is a same-author cross-check,
not independent review.

## 5. Deflated curvature and the Euclidean normalization

Along(6), the small-real contribution to(5) is

    4/A+1/(A-eta delta)+1/(A+eta delta)
      =6/A+(2eta^2/A^3)delta^2+O(delta^4).

Equation(8) gives `partial_sigma omega=eta w_omega`, hence

    partial_sigma f_eta at0
      =eta^2[2/A^3-2w_omega/W^2].                     (15)

The split direction `(1,-1,0,0,0,0)` has squared Euclidean norm2.
Its second derivative is twice the sigma coefficient. Thus its Hessian
eigenvalue is the sigma coefficient itself, with no missing factor of2.
Put `alpha=1+x`. Using `A=1-eta alpha`, `W=1+eta omega` and
`w_omega=1/2+eta(w1)_omega`, the exact removable quotient is

    L=(lambda_W/eta^2-1)/eta
      =2alpha(3-3eta alpha+eta^2 alpha^2)/A^3
         +omega(2+eta omega)/W^2-2(w1)_omega/W^2.       (16)

The identities `1-(1-t)^3=t(3-3t+t^2)` and
`(1+t)^2-1=t(2+t)` prove(16) without dividing an interval by eta.
The enclosures(13)-(14), the positive A,W margins and the same covered
rectangle yield the strict exact rational check

    -5 < L < -3.                                     (17)

The full endpoints, beta, response residual and response enclosure are
regenerated and compared entry by entry. Formula(17) proves(2), including
arbitrarily small positive eta. Floating decimal displays or time limits
are not used for any mathematical predicate.

## 6. Whole six-real Hessian and the local stability supremum

The labelled family and its unique tail solution are invariant under every
permutation of the six real small positions. At the common tuple, all six
gradient entries coincide. Their sum is the derivative of the scalar
common-x family, which vanishes by9113. Thus the entire real gradient is0.
Permutation invariance makes its Hessian `a_eta I+b_eta J`, with J the
six-by-six all-ones matrix. Its centered subspace is an eigenspace and the
literal split in(15) identifies its eigenvalue as `lambda_W`.

The complementary common direction has squared norm6. Consequently its
eigenvalue equals `Phi_eta''(x)/6>(11/3)eta^2`. By(2),
`0<lambda_W<eta^2`, so it is strictly smaller than that eigenvalue.
This proves the asserted least eigenvalue and five-dimensional eigenspace
in the six-real Hessian. It does not count multiplicity in a full complex
Hessian, whose other sectors have not been enclosed here.

Fix eta. For every `k<lambda_W/(2eta^2)`, continuity of the real Hessian
gives a sufficiently small convex parameter ball on which its least
eigenvalue is greater than `2k eta^2`. The integral Taylor formula at the
stationary point gives

    f_eta(u0+h)-f_eta(u0)
      =integral_0^1(1-t) h^T D^2f_eta(u0+t h) h dt
      >=k eta^2 ||h||^2.

This ball can be chosen inside the genuine feasible family from Section2.
Conversely, substituting the centered split and letting delta tend to0
in any proposed inequality forces `k<=lambda_W/(2eta^2)`. Taking the
supremum proves(3). The proof supplies no uniform numerical parameter-ball
radius or assertion that the supremum itself is attained.

## 7. Dependencies, trust boundary and remaining coverage

The necessary mathematical input is9113's explicit real branch, original
root legality and stationary symmetric curvature. Its use of7290 for a
different collapsed-basin competitor corollary is not imported into this
curvature calculation. Its use of8921/8955 for global germ identification
is likewise not required to prove(2)-(3).

The exact ell and centered-real sector have prior credit to
[9033](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/exact-half-obstruction/PROOF.md),
source `f6e5848da01148e65c9be0ec8a8b003d14d503d8`, and independent
[review9080](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/half-endpoint-audit/REVIEW.md),
source `215d6ae7843624382f0784e3e4b836339885e4a3`. That review establishes
the sector in the inherited twelve-coordinate zero-slack germ, with an
existential radius, rather than reviewing the present effective interval.
On the inherited global-minimum germ, the pointwise necessary full-raw
ceiling agrees with the restriction computed here. The inherited germ's
unknown extent cannot be replaced by the whole explicit eta interval.

The finite checker regenerates every certificate entry, tests the new mixed
normalization from falling-factorial monomial derivatives, checks literal
critical factors and anchoring, and rejects damaged mathematics and full
fixtures both normally and under optimization. The analytic implicit
function, original-root continuity, permutation-Hessian and Taylor bridges
are ordinary written mathematics, not proof-assistant claims.

The other complex tangent sectors, mixed displacements and nonlinear
uniform radius still require estimates. All-competitor concentration entry,
global-minimum identification across this explicit window, interior radii
and the unrestricted degree-nine first-power inequality remain open.
