# Every spherical tail test passes for independent radii and directions

Complete author proof, 27 September 2026; independent review is pending.
This is an exclusion for an actual necessary condition of Gaussian
majorisation. It is **not** full Gaussian majorisation for the class below,
and it gives no new Kneser--Poulsen inequality.

## 1. The class and the exact comparison

Let A be a bounded real random variable and U an independent random vector
on the unit sphere of R^d. Its angular law is arbitrary: it need not be
uniform, symmetric, continuous or supported on a hemisphere. Let h:R->R
be odd and 1-Lipschitz. Put

    X=A U,           Y=h(A) U.

Signed A is allowed. Define the radial map

    T(0)=0,     T(r u)=h(r)u  for r>0 and |u|=1.            (1)

Oddness makes Y=T(X), including negative A. This T is a contraction. Indeed,
for real a,b and unit u,v, put c=u.v. Then

    |a u-b v|^2-|h(a)u-h(b)v|^2
      = (1+c)/2 [(a-b)^2-(h(a)-h(b))^2]
        +(1-c)/2 [(a+b)^2-(h(a)+h(b))^2] >= 0.             (2)

The difference term uses the Lipschitz hypothesis. The sum term uses it
at a,-b and oddness. Formula (2) also handles zero coefficients, coincident
directions and antipodal directions.

For independent copies X',Y' of their respective laws, our stronger
probabilistic statement is

    Y-Y' <=_cx X-X'.                                      (3)

Here multivariate convex order means E Phi(Y-Y')<=E Phi(X-X') for every
finite convex function Phi:R^d->R. All variables are bounded, so these
expectations are finite. In particular, for every t in R^d,

    M_Y(t) M_Y(-t) <= M_X(t) M_X(-t),
    M_Z(t)=E exp(t.Z).                                    (4)

Consequently, for normalized spherical area sigma and every lambda>0,

    S_X(lambda):=integral log M_X(lambda theta) d sigma(theta)
       >= S_Y(lambda).                                   (5)

The statement holds in every dimension; the campaign application is d=3.
It holds for every distribution of A and U under the stated independence,
and for all odd scalar contractions, including profiles that reverse sign
or radial order arbitrarily often. It is not a finite-order moment check.

## 2. The four-point convex comparison

We give a direct finite proof of (3). No comparison theorem for Gaussian
convolutions is a premise.

Take iid A,B and iid U,V, with the two pairs independent. For fixed values
a,b,u,v, write

    p=(u+v)/2, q=(u-v)/2, D=a-b, E=a+b,
    D'=h(a)-h(b), E'=h(a)+h(b).

Independently exchanging a,b and exchanging u,v gives the four vectors

    epsilon D p + delta E q,     epsilon,delta in {-1,1}.  (6)

Each exchange preserves the joint probability law. Therefore X-X' has
the same law as (6) with fresh independent uniform signs, averaged over
a,b,u,v. The analogous statement for Y-Y' replaces D,E by D',E'.
This separate exchangeability is precisely where radius--direction
independence is needed.

We have |D'|<=|D| and |E'|<=|E|. If D!=0 put rho=D'/D; if D=0 then D'=0
and put rho=0. Define tau similarly from E',E. Both lie in [-1,1].
For target signs epsilon_0,delta_0, set

    C[(epsilon_0,delta_0),(epsilon,delta)]
       = (1+epsilon epsilon_0 rho)(1+delta delta_0 tau)/4.  (7)

This 4-by-4 matrix is nonnegative and each row and column sums to one.
Its indicated row has barycenter

    sum_(epsilon,delta) C[...] (epsilon D p+delta E q)
       = epsilon_0 D' p+delta_0 E' q.                     (8)

Jensen's inequality applied to every row, followed by averaging the four
rows, proves the convex comparison conditional on a,b,u,v. Integrating
proves (3). This is an application of the elementary contraction principle
for two Rademacher coefficients, not a new general contraction principle.

Taking Phi(z)=exp(t.z) proves (4). Taking logarithms is legitimate because
all moment-generating functions are strictly positive. Finally spherical
area is invariant under theta -> -theta, so

    S_X-S_Y = (1/2) integral
       log [M_X(lambda theta)M_X(-lambda theta)
                         /(M_Y(lambda theta)M_Y(-lambda theta))] d sigma
       >= 0.

The same argument works for any symmetric probability distribution of t
for which the displayed logarithms are integrable.

An equivalent check on (4), avoiding convex-order terminology, is the
identity

    M_X(t)M_X(-t)
       = E cosh((A-B)t.(U+V)/2) cosh((A+B)t.(U-V)/2).     (9)

Both absolute coefficients decrease on replacing A,B by h(A),h(B).
Monotonicity of cosh on [0,infinity) gives (4) directly. This is an
independent reading of the same exchange identity, not independent review.

## 3. A signed fold and a uniform strict margin

Take the odd 1-Lipschitz profile

    h(a)=a                         if |a|<=1,
         2 sign(a)-a               if |a|>=1.             (10)

This is reflection in the metric projection onto the unit ball: inner
points stay fixed and points of radius greater than two cross to the
opposite direction. The theorem on nonnegative radial profiles does not
apply to (10) on this whole domain.

Give A the probabilities

    Pr(A=0)=1/5,   Pr(A=1)=3/10,   Pr(A=4)=1/2.           (11)

For **every** independent unit-vector law U in R^3, (5) has the explicit
strict lower bound

    S_X(lambda)-S_Y(lambda) >= lambda^2 exp(-8 lambda)/5
                              >0,       lambda>0.        (12)

To see this, write P_X(t)=M_X(t)M_X(-t), and similarly P_Y. All conditional
differences in (9) are nonnegative. Retain only the events (A,B)=(0,4)
and (4,0), whose total probability is 1/5. Their averaged contribution is

    P_X(t)-P_Y(t)
       >= (1/5) E[cosh(4t.U)-cosh(2t.U)]
       >= (6/5) E(t.U)^2.                               (13)

The second inequality follows term by term from the power series for cosh.
Since |X|<=4, P_X(lambda theta)<=exp(8lambda). For 0<z<=1,
-log z>=1-z, hence

    log(P_X/P_Y) >= (P_X-P_Y)/P_X
                 >= exp(-8lambda)(P_X-P_Y).

In R^3, integral(theta.u)^2 d sigma=1/3 for every unit u. Combining these
facts with the factor 1/2 in the preceding section gives (12). There is
no angular density lower bound, mass floor for individual directions,
numerical integration, or limiting angular argument in this estimate.

## 4. Exact non-orthocentric rank-six instance

For a finite asymmetric instance use

    u_1=(1,0,0), u_2=(3/5,4/5,0), u_3=(1/3,2/3,2/3),
    Pr(U=u_1,u_2,u_3)=(1/2,1/3,1/6).

With (11), the seven distinct source and target sites are

    X: 0, u_1,u_2,u_3, 4u_1,4u_2,4u_3,
    Y: 0, u_1,u_2,u_3,-2u_1,-2u_2,-2u_3,

with weights (1/5,3/20,1/10,1/20,1/4,1/6,1/12).
All directions have unit norm and det[u_1;u_2;u_3]=8/15.
The determinant of the six nonzero paired vectors (x_i,y_i) is

    (-6)^3 (8/15)^2 = -1536/25 != 0.                     (14)

Thus the paired affine rank is six. There are 12 strict and 9 tight pairs;
the least strict squared-distance loss is 16/5. These assertions are checked
over rational numbers. No angular quadrature is used to claim (12).

This example is a signed radial fold on three nonorthogonal rays and the
origin. It is not the closed orthocentric flap assignment. We make no claim
that its full Gaussian comparison is false or outside every other positive
theorem. Rank six alone only excludes the paired-rank-five criterion.

## 5. Why the independence condition cannot be silently removed

The stronger directional statement (4) can fail without independence even
for a two-point contraction satisfying the full Gaussian inequality.
With equal weights, take the correlated radius--direction inputs

    (A,U)=(1,(1,0,0)),
          (13/5,(5/13,12/13,0)).

Under (10), both source first coordinates equal one, whereas the target
first coordinates are 1 and -3/13. At t=t_1 e_1, therefore,

    M_X(t)M_X(-t)=1,
    M_Y(t)M_Y(-t)=cosh(8t_1/13)^2>1  if t_1!=0.           (15)

The pair loses squared distance 256/65, checked exactly. This is only a
control showing the scope of (3)--(4). It is not a negative spherical
average or a Gaussian counterexample; its two-point Gaussian comparison
belongs to an already positive class.

## 6. Consequence for the shared counterexample search

The existing spherical-tail transfer proves that a negative S_X-S_Y would
produce a negative Gaussian hinge at sufficiently large variance and an
explicitly small threshold. Equations (5) and (12) rule out that entire
route for the independent-radius class, including signed profiles and
asymmetric rank-six supports. This supplies an exact failed-search boundary
with a reusable four-point certificate, not another family of untested
templates. Raw angular minima contradicting (12) are necessarily wrong.

The converse implication is not available: positive spherical tests do
not prove all Gaussian hinges. A counterexample with independent radii and
directions at a different variance/threshold is not excluded. Nor is a
spherical-tail counterexample with radius--direction dependence excluded.
The full R3 problem and every unrestricted Kneser--Poulsen conclusion remain
open. We do not recommend another adjacent beta strip or a positive-neighborhood
computation as a consequence of this note.

## 7. Reproduction and trust boundary

Run `python3 -B verify.py --check`, `python3 -B -O verify.py --check`, and
`sha256sum -c SHA256SUMS` from this directory. Standard-library Python 3.11
or later suffices. EXPECTED.json records exact four-point certificates,
the rank-six fixture, direct finite-law convex tests, and damaged-input
rejections. No external solver, floating sign or omitted dataset is used.

The universal theorem rests on the written exchangeability and Jensen
argument. The executable checks the rational identities and finite controls;
it is not a formalization, an independent review, or a proof of Gaussian
majorisation. The classical ingredients and team dependencies are distinguished
in SOURCES.md. Priority of this particular deduction is provisional.
