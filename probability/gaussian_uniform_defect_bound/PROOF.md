# A certified uniform bound on the dimension-three Gaussian defect

Complete author proof, 26 September 2026. Independent correctness and
historical priority review are pending. The unrestricted majorisation
conjecture remains open. This result bounds its possible failure, uniformly
over all bounded laws, contractions, variances and thresholds.

## 1. Statement

Let mu be a probability measure with bounded support in R3, let T be
1-Lipschitz on its support, and let s>0. Write

    f = mu * gamma_s,       g = (T#mu) * gamma_s,
    H_f(a) = integral (f-a)_+,       a>=0,

where gamma_s has covariance s I3. Then

    H_f(a) - H_g(a) <= 7/50                                      (1)

for every a>=0. Consequently the unrestricted supremal positive defect
D from [the compact localization](../gaussian_prior_localization/DEFECT_LOCALIZATION.md)
satisfies

    0 <= D <= 7/50.                                              (2)

This is an absolute bound for unit-mass laws. It is not a proof that D=0,
nor a claim that 7/50 is optimal. It has no dependence on atom count,
minimum atom mass, diameter, pairwise slack, or noise variance.

For the concentration function

    M_f(v) = sup_{Leb(A)=v} integral_A f,       v>=0,

the same conclusion gives M_f(v)<=M_g(v)+7/50 at every v. Indeed
M_f(v)=inf_{a>=0}[H_f(a)+av], and applying (1) before the infimum proves
the assertion. The hinge/profile duality also follows directly by filling
superlevel sets and, if necessary, a level set. Gaussian densities cause
no difficulty at the endpoint a=0.

The constant does not have the vanishing, threshold-dependent scale needed
for a new small-variance Kneser--Poulsen consequence. No such consequence,
new exact positive class, or full solution is claimed.

## 2. The retained Gamma comparison

For t>=0 let

    F(t) = (2/sqrt(pi)) integral_0^t sqrt(u) exp(-u) du,

and put F(t)=0 for t<0. This is the Gamma(3/2,1) distribution function.
For a probability density h put

    R_h(a) = integral h(x) F(log(h(x)/a)) dx,       a>0,           (3)

with zero integrand at h(x)=0. The team's
[rank/Abel result, Theorem B](../gaussian_majorisation_rank_abel/PROOF.md)
establishes

    R_f(a) <= R_g(a)       for every a>0.                        (4)

Here is the reduction to the external theorem, to make this dependency
explicit. Choose x0 in the closed support and form
v(x)=(x-x0,T(x)-T(x0)) in R6. On its linear span let P,Q be the two
coordinate projections, A=P*P and B=Q*Q. The trajectories

    c_t(x) = ((1-t)A+tB)^(1/2) v(x),       0<=t<=1,

are continuous, and their pairwise squared distances are

    |c_t(x)-c_t(y)|^2
       = (1-t)|x-y|^2 + t|T(x)-T(y)|^2.

They therefore give a continuous contraction in at most six dimensions.
Pad to dimension six. The endpoints are congruent to the original input
and output embedded in R6. Apply
[Aishwarya--Li, Theorem 1.4(i)(a)](https://arxiv.org/html/2609.07041v2):
the convolved density value, sampled according to its own density, increases
in stochastic order under this motion. Only continuity of the trajectories
is required for this part of the theorem. No differentiable lift or
volume-contracting transport is assumed.

At the endpoints these densities are f(x) gamma_s^(3)(z) and
g(x) gamma_s^(3)(z), up to Euclidean isometries. If Z is sampled from the
auxiliary Gaussian, then

    log gamma_s^(3)(Z) = log C - G,
    C=(2 pi s)^(-3/2),       G~Gamma(3/2,1).

The upper-tail probability of the sampled product density at a C is
exactly (3). Stochastic order gives (4), with the same threshold factor
at both endpoints. This proof applies to arbitrary bounded probability
laws, including diffuse laws. A contraction extends continuously to the
compact closure of its support if needed.

Neither (4) nor the lifting mechanism is new here. The rank/Abel packet
also gives normalized step densities satisfying all of (4) with a strict
adverse hinge. Thus cancellation of (4) alone is not a valid proof of
the full conjecture. Those step densities are not Gaussian-contraction
counterexamples.

## 3. One global scalar envelope

Put

    h(t)=(1-exp(-t))_+,
    q=17/50,       w=57/50,       c=w-1=7/50,
    d(t)=h(t)-w F(t+q).

The exact finite certificate proves

    -c <= d(t) <= 0       for every real t.                     (5)

The reduction of the whole real line to the finite checks is as follows.

For t<=-q, d(t)=0. On [-q,0], d(t)=-w F(t+q) is nonincreasing.
Thus its only relevant finite minimum there is d(0). For t>0,

    d'(t)=exp(-t) [1-(2w exp(-q)/sqrt(pi)) sqrt(t+q)].            (6)

The bracket is strictly decreasing. The unique zero occurs at

    t* = pi exp(2q)/(4w^2)-q.

It lies in the certified rational interval

    85289/100000 < t* < 8529/10000.                             (7)

Consequently d increases up to t*, decreases afterwards, and tends to
1-w=-c at positive infinity. Its positive-half-line maximum is d(t*);
its infimum is the smaller of d(0) and -c. This analysis includes every
point of the real line, rather than a numerical grid or truncation.

The two remaining certified enclosures are

    -139197/1000000 <= d(0) <= -139196/1000000,
    -419/1000000 <= d(t*) <= -409/1000000.                       (8)

The first is strictly above -7/50 and the second strictly below zero.
Together with the derivative signs and endpoint limits, these establish
(5). There is substantial rational slack in both checks. No precision
decision depends on an unvalidated floating-point result.

## 4. From the envelope to every compact-frontier row

For any probability density p and a>0, substitute t=log(p(x)/a) into (5),
multiply by p(x), and integrate. Since p h(log(p/a))=(p-a)_+,

    H_p(a) <= w R_p(a exp(-q)) <= H_p(a)+c.                    (9)

Both sides integrate bounded functions against the probability measure
p(x) dx. Zeros of p have zero contribution. Combining (9) and (4) gives

    H_f(a) <= w R_f(a exp(-q))
           <= w R_g(a exp(-q)) <= H_g(a)+c,

which proves (1). At a=0 both hinge integrals are one.

For explicit comparison with the R3--R8 finite frontier, use their original
definitions: K_k has k^6 labeled atoms, zero weights and repetitions allowed,
matched anchor at zero, both supports within radius 2k, and all pairwise
contraction constraints. D_k is its maximal variance-one hinge defect.
Let H(u)=H_g(Cu)-H_f(Cu), C=(2 pi s)^(-3/2), and let

    b_(N,j) = E H(Beta(j+1,N-j+1)),       0<=j<=N,
    D_N = max(0,-min_j b_(N,j)).

The [uniform moment frontier](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md)
uses N_k=2^16 k^8-2 and B_k=max_(Q in K_k) D_(N_k)(Q). Equations (1)--(2)
give, simultaneously,

    b_(N,j)(Q) >= -7/50       for every Q, N>=0 and 0<=j<=N,
    0 <= D_k <= 7/50,       0 <= B_k <= 7/50,       D<=7/50.    (10)

Thus this is an actual signed bound on every coefficient and both compact
maxima, including their collision, zero-weight and isometry boundaries.
It does not require enumerating K_k, expanding alternating moment sums,
or increasing N to a supplied sufficient degree. It applies directly to
the unrestricted law, so no localization or truncation error is added to
7/50. In particular it is stronger than merely taking B_k<=7/50 and then
adding the existing error below 5/k.

The sign sought by the conjecture is still H>=0, equivalently D=0. A
positive universal upper bound leaves that question unresolved. The
certificate supplies a rigorous bounded conclusion, not a finite
decision procedure or a claim of progress from sampled positive examples.

## 5. Exact arithmetic and trust boundary

[CERTIFICATE.json](CERTIFICATE.json) contains just q,w,c, a rational critical
bracket, three rational enclosure claims, and small precision parameters.
[verify.py](verify.py) reconstructs every numerical premise using integers
and fractions. Its analytic enclosure rules are recorded here in full.

For x>=0 the even and odd Taylor polynomials S_20(x), S_21(x) for exp(-x)
satisfy S_21(x)<=exp(-x)<=S_20(x), by the sign of the Lagrange remainder.
Integrating these inequalities against sqrt(u) gives

    F(x) between (4x sqrt(x)/sqrt(pi)) times
       sum_(j=0)^m (-x)^j / [j! (2j+3)],       m=21,20.         (11)

All required lower partial sums are checked positive before interval
multiplication or division. Square roots are enclosed on the dyadic grid
of denominator 2^80 using integer square roots, and every resulting
interval is checked by squaring both endpoints exactly.

For pi, use pi=16 atan(1/5)-4 atan(1/239). The finite geometric expansion
of 1/(1+u^2), integrated from zero, bounds atan(x) by its alternating sums
through indices 21 and 20. The Machin identity follows by the tangent
double-angle formula: tan(4 atan(1/5))=120/119 and
tan(4 atan(1/5)-atan(1/239))=1. The angle is between zero and pi/2, so it
is pi/4. The checker also verifies the rational tangent identity. Its
pi interval is contained in

    [3.141592653589793, 3.141592653589794].

The derivative-root tests square positive quantities in (6): at the left
endpoint w^2 exp(-2q)(t+q)<pi/4, and at the right it is greater. To enclose
d(t*) throughout (7), monotonicity of h and F gives the lower bound
h(t_lo)-w F(t_hi+q) and the upper bound h(t_hi)-w F(t_lo+q).
Their exact enclosures imply (8).

The floating LP used in discovery has no role in the proof; its suggested
two-shift fit was replaced by this single rational shift and multiplier.
The public result claims neither optimality of the scalar approximation
nor sharpness for Gaussian mixtures. All proof inputs are public, and
the replay uses only the Python standard library. Checks use explicit
exceptions and remain active with Python -O. The damaged-certificate
controls include a nearby rational shift whose critical maximum is positive.

The separate [polynomial checker](independent_check.py) imports no primary
code and reads no certificate file. It uses the wider root bracket
[0.8528,0.853], the coarser pi interval [3.14159,3.1416], and exp Taylor
degrees 8 and 9. Put P_m(x)=sum_(j=0)^m (-x)^j/[j!(2j+3)]. It eliminates
square roots by checking the positive rational margins

    c^2 pi_lo - 16w^2 q^3 P_8(q)^2 > 0,
    16w^2 (t_lo+q)^3 P_9(t_lo+q)^2
       - pi_hi [1-S_9(t_hi)]^2 > 0,

together with the two derivative signs. The factors being squared are
checked positive. These are respectively d(0)>-c and an upper bound
d(t*)<0, using the same global derivative reduction. This second exact
implementation corroborates the critical finite inequalities with different
precision and an algebraic elimination, but is not an independent review.

The analytic reduction, external continuous-contraction theorem, and Python
integer/rational implementation remain trusted. This is not proof-assistant
formalization, independent mathematical review, or acceptance of the open
conjecture. A separate human or program can reconstruct the entire finite
certificate from (6)--(11); no large search corpus is being hidden.
