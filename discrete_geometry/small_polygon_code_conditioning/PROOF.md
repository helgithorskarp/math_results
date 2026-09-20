# Uniform conditioning and uniqueness for polygon sign codes

For n>=3 fix c=(c_0,...,c_(n-1)) in {+1,-1}^n. Normalize

    0=phi_0 < phi_1 < ... < phi_(n-1) < phi_n=pi,
    alpha_j=phi_(j+1)-phi_j,
    F(phi)=sum_(j=0)^(n-1) 2sin(alpha_j/2),
    g(phi)=sum_(j=0)^(n-1) c_j(exp(i phi_(j+1))-exp(i phi_j)).

Identify complex numbers with R^2. The free variables are phi_1,...,phi_(n-1).
Feasibility means g=0; the strict ordering is also essential. Let J=Dg,
f=-F, and U_n=2n sin(pi/(2n)). This uses the full perimeter, not half of it.

**Theorem 1 (sharp conditioning).** At every feasible strict angle vector,
for every lambda in R^2,

    ||J^T lambda||_infinity >= ||lambda||_2.                (1)

The constant one is sharp. In particular J has rank two, sigma_min(J)>=1,
and every equality-stationary multiplier obeys
||lambda||_2 <= ||grad f||_infinity.

**Theorem 2 (uniform uniqueness).** For every n>=3 and every sign code,
there is at most one feasible stationary angle vector in the superlevel

    F >= U_n - 1/(400 n^5).                                (2)

Here stationary means grad f+J^T lambda=0 for some lambda. If this
superlevel contains any feasible vector, the fixed code has a unique global
maximizer on the closed ordered simplex, and this maximizer lies in (2).
Its full Lagrangian Hessian is bounded below by I/(2n^3), and its equality
KKT matrix is nonsingular. No existence is asserted for codes that cannot
reach the superlevel.

**Polygon consequence.** For every power of two n>=2^17, every code that
can match Bingane's polygon B_n has a unique global maximum. Every global
maximum in the original small-polygon problem is one of these code maxima,
using the previously proved saturation theorem. This does not imply that
only one code, or one congruence class, attains the unrestricted maximum.
The cutoff and deficit constant are sufficient values, not sharp claims.

## 1. Alternating switch coefficients and half-circle cuts

Summation by parts gives

    g=sum_(j=0)^(n-1) a_j u(phi_j),   u(theta)=(cos theta,sin theta),
    a_0=-(c_0+c_(n-1)),  a_j=c_(j-1)-c_j for 1<=j<n.

After deleting zero coefficients and dividing by two, the nonzero
coefficients are an alternating list of +1 and -1 of odd length.
Indeed, if c_0=c_(n-1), the number of internal switches is even and
a_0=-2c_0 is the additional first coefficient. If c_0=-c_(n-1), a_0=0
and the number of internal switches is odd. The list is nonempty.

This statement is invariant under moving the cut of the half-circle.
To move a terminal block to the front, subtract pi from its angles and
negate its coefficients, preserving every vector term. An odd alternating
list has equal first and last signs, so the negated terminal block joins
the initial block with opposite signs. The resulting list is again odd
and alternating. Empty blocks cause no exception.

The fixed term at angle zero is the only coefficient absent from J.
If a_0!=0 and it is omitted, the remaining nonzero coefficients are an
even alternating list in the original order. This distinction matters.

## 2. A short-arc chord bound

Let beta_1<...<beta_(2k) lie in a real interval I of angular length
L<pi/3. Then

    |sum_(r=1)^k (u(beta_(2r))-u(beta_(2r-1)))|
        <= 2sin(L/2) < 1.                                  (3)

To see this, express the sum V as the integral of u'(theta) over the
union E of the k disjoint selected subintervals of I. The derivative
directions range over an arc of length L<pi/2. If V!=0 its direction is
in their convex cone, so its scalar product with every u'(theta), theta
in I, is positive. For v=V/|V|, enlarging E to I therefore gives

    |V|=integral_E <v,u'(theta)> dtheta
       <= <v,u(right I)-u(left I)> <= 2sin(L/2).

If E is empty the same conclusion is immediate. Also an odd alternating
sum of unit vectors in I cannot vanish: leave its first term unpaired
and apply (3) to the remaining even list. The paired part has norm <1,
while the unpaired vector has norm one.

## 3. Free switches cannot fit in a projective arc shorter than pi/3

View angles modulo pi, so that a half-turn of a representative negates
both its unit vector and its coefficient. Suppose all nonzero *free*
switch angles (j>=1) fit in a projective arc I of length L<pi/3.

If a_0=0, choose representatives in I. Section 1 gives an odd alternating
list there, whose sum cannot be zero by Section 2. If a_0!=0 and the
fixed angle zero also belongs to I, the same argument applies to the
full switch list.

In the remaining case a_0!=0 and angle zero is outside I. Since I avoids
zero modulo pi, it can be represented inside (0,pi) without wrapping.
All free switches are then an even alternating list in I. Their signed
sum has norm <1 by (3), whereas closure requires it to cancel the fixed
term (a_0/2)u(0), of norm one. This is again impossible.

Empty free lists are also impossible, since the full coefficient list is
nonempty and a nonzero fixed unit vector cannot sum to zero. Hence the
free switches are not contained in any projective arc of length <pi/3.

For lambda!=0, let theta be its direction. If every free switch satisfied
|sin(phi_j-theta)|<1/2, they would all lie in a projective arc of length
strictly less than pi/3, since the set is finite. Thus at least one has
|sin(phi_j-theta)|>=1/2. Its Jacobian column is a_j u'(phi_j), |a_j|=2,
which proves (1). Lambda=0 is immediate.

Sharpness occurs at n=3, c=(+1,-1,+1), phi=(0,pi/3,2pi/3,pi).
Then a=(-2,2,-2), closure holds, and for lambda=(0,1) the two components
of J^T lambda both equal one. This proves the sharp infinity-norm
constant; it does not claim that sigma_min(J)>=1 is itself sharp.

Feasibility is indispensable. At arbitrary infeasible ordered angles,
the switched columns can be arbitrarily close to parallel. Mere rank two
away from degeneracy, already known in the literature, is weaker than (1).

## 4. Gap localization without a code-dependent estimate

Let h(x)=2sin(x/2), t=pi/n, and D=U_n-F. On the whole interval [0,pi],

    h(t)+h'(t)(x-t)-h(x) >= t(x-t)^2/(6pi).                 (4)

For completeness, -h''(s)=sin(s/2)/2>=s/(2pi). For x>=t its Taylor
integral is at least t(x-t)^2/(4pi); for x<=t it is at least
(t-x)^2(x+2t)/(12pi). Both imply (4).
Summing and using sum alpha_j=pi gives

    ||alpha-t||_2^2 <= 6nD.                                (5)

This is valid also on the closed ordered simplex. If D<=1/(400n^5),
then (5) implies

    t/2 < alpha_j < 3t/2.                                 (6)

For example, 6nD<=3/(200n^4)<pi^2/(4n^2). Thus no gap or ordering
boundary is present in the asserted superlevel. The band (6) is convex
in the normalized free angles; the segment between any two points in
the superlevel stays in that band even if it does not satisfy closure.

## 5. Uniform Hessian and multiplier bounds

For v_0=v_n=0, the exact Hessian identity is

    v^T Hess(f) v = sum_j [sin(alpha_j/2)/2](v_(j+1)-v_j)^2.

On (6), each weight is at least 1/(4n), by sin x>=2x/pi.
Put d_j=v_(j+1)-v_j. Then sum d_j=0 and

    v_k=sum_j (1_(j<k)-k/n)d_j,
    |v_k|^2 <= [k(n-k)/n] sum_j d_j^2 <= (n/4)sum_j d_j^2.

Summing over k=1,...,n-1 yields ||v||_2^2<=n^2||d||_2^2/4.
Consequently throughout the convex band

    Hess(f) >= I/n^3.                                     (7)

The jth free gradient component is

    (grad f)_j=cos(alpha_j/2)-cos(alpha_(j-1)/2).

On (6), the derivative of cos(x/2) has magnitude at most 3t/8.
Equation (5) and |alpha_j-alpha_(j-1)|<=sqrt(2)||alpha-t||_2 give

    ||grad f||_infinity <= (3pi sqrt(12)/8)sqrt(D/n)
                         <= 5sqrt(D/n).                   (8)

The last scalar constant follows, for example, by squaring and using
pi<22/7. At a feasible stationary point Theorem 1 and stationarity give

    ||lambda||_2 <= ||grad f||_infinity
                 <= 5sqrt(D/n) <= 1/(4n^3).               (9)

All estimates hold for every code; no switch-root sum or candidate
singular-value calculation is required.

## 6. Two-point uniqueness, existence and nonsingularity

For any free increment d, the closure map satisfies the global bound

    ||D^2g(w)[d,d]||_2 <= 2||d||_2^2,

because |a_j|<=2. If u,v are feasible and d=u-v, Taylor expansion at
both endpoints, with its factor 1/2, gives

    ||Dg(u)d||_2 <= ||d||_2^2,
    ||Dg(v)d||_2 <= ||d||_2^2.                             (10)

Assume both points satisfy (2) and are stationary, with multipliers
lambda_u,lambda_v. Strong convexity (7) along their joining segment and
the two stationarity equations imply

    ||d||_2^2/n^3
      <= d dot (grad f(u)-grad f(v))
      <= (||lambda_u||_2+||lambda_v||_2)||d||_2^2
      <= ||d||_2^2/(2n^3),

where (9)-(10) were used. Therefore d=0. Rank two makes the multiplier
unique as well.

If a feasible vector satisfying (2) exists, maximize F on the compact
set g=0 in the closed ordered simplex. A maximizer has at least that
perimeter, hence its gaps satisfy (6). By Theorem 1 the equality Jacobian
has rank two. The usual equality-constrained first-order condition
therefore applies. Uniqueness just proved makes it the unique global
maximizer for that code. Low-perimeter stationary points are not excluded.

At this maximizer, or any stationary point in (2),

    Hess(f+lambda dot g) >= (1/n^3-2||lambda||_2)I
                         >= I/(2n^3).

Thus the full Lagrangian Hessian is positive definite. The block equality
KKT matrix [H J^T; J 0] has trivial kernel: Jv=0 and Hv+J^T mu=0 imply
v^T Hv=0, so v=0, followed by mu=0 since J has rank two. This proves
all claims of Theorem 2. It is a regularity statement, not a global
convergence claim for an unspecified numerical algorithm.

## 7. Explicit original-polygon consequence

Bingane's published construction B_n, for powers of two n>=8, satisfies

    p(B_n)=U_n cos(beta),
    beta=theta/2-(1/2)arcsin((1/2)sin(2theta)), theta=pi/n.

Since 0<theta<=pi/8, (sin(2theta))/2=sin(theta)cos(theta)<=sin(theta)
and hence beta>=0. From arcsin x>=x and sin x>=x-x^3/6 one obtains
beta<=theta^3/3. Using U_n<pi and 1-cos(beta)<=beta^2/2 gives

    U_n-p(B_n) <= pi^7/(18n^6).

Since 400(22/7)^7/18 < 2^17, every power of two n>=2^17 satisfies

    p(B_n) > U_n-1/(400n^5).

Every code capable of matching B_n has a unique global maximum by Theorem 2.
Every original global polygon maximum has perimeter at least p(B_n) and
satisfies the prior
saturation threshold 1/(100n^3), since 1/(400n^5)<1/(100n^3).
The committed saturation theorem and sign reconstruction then place it
in the circle-code model just studied. This proves the polygon consequence.

This is a reduction to comparing distinct code maxima, not uniqueness
across codes. Rotations are removed by phi_0=0; discrete shifts, reflections
and an overall code sign change may encode congruent polygons. No count
or classification of the remaining codes is asserted.

## Attribution and trust boundary

The qualitative rank statement is in Mulansky--Potschka, Lemma 3.
Guo--Luo and the reviewed graph fixed-code theorem already use the
strong-convexity/Taylor two-point uniqueness argument. Our quantitative
all-feasible conditioning bound, its sharp constant, and the all-code,
all-order threshold are the claimed new scope relative to searched sources.
The bound does not replace the sharper n=16 candidate-specific certificate.
The written proof carries all universal quantifiers. Exact Python checks
corroborate short-arc algebra, the half-circle cut convention, constants,
and boundary fixtures; they are not an enumeration proof or formalization.
