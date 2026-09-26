# A common Gaussian set transfer and the limit of atomic localization

Complete author proof, 26 September 2026; independent review is pending.
The unrestricted three-dimensional Gaussian-majorisation question remains
open. The result exchanges its quantifier over input measures with a
deterministic set-transfer condition. A sphere example then rules out an
exact finite-support optimizer reduction for the resulting minimax problem.
It does not rule out finite witnesses of a strict failure.

## 1. The measure-side minimax problem

Let K be a nonempty compact subset of R3, T:K -> R3 continuous, and s>0.
Write gamma_s for the probability density with covariance s I_3. For
mu in P(K), put

    f_mu = mu * gamma_s,        g_mu = (T#mu) * gamma_s.

For an integrable density p and 0<v<infinity define its concentration

    C_p(v) = sup { integral_E p : E measurable, |E|=v }.

If A is a measurable set of volume v, set

    a_A(x) = integral_A gamma_s(z-x) dz,
    b_B(x) = integral_B gamma_s(z-Tx) dz,
    q_B(x) = b_B(x)-a_A(x),

and define

    m(A) = min_{mu in P(K)} [ C_{g_mu}(v) - integral_A f_mu ].       (1)

The contraction assumption is unnecessary for the duality. It enters the
open sign question m(A)>=0 and, below, the quantitative approximation.

**Theorem 1 (deterministic transfer and contact set).** The minimum in (1)
exists, and

    m(A) = max_{B measurable, |B|=v} min_{x in K} q_B(x).           (2)

The maximum also exists. One can take

    B = { g_mu* > t },      |B|=v,                                (3)

where mu* minimizes (1) and t>0. For a maximizing B of this form,

    q_B(x) >= m(A)                 for every x in K,
    supp(mu*) subset {x : q_B(x)=m(A)}.                           (4)

Thus B is one ordinary measurable set that works simultaneously at every
input centre. No randomized selector is needed. Conversely, a probability
mu*, a superlevel set B as in (3), and (4) certify the exact value in (1).
The measure in (3) is not asserted to have finite support.

### Proof, including compactness and removal of randomization

Use the convex selector space

    V_v = { psi in L_infinity(R3) : 0<=psi<=1, integral psi<=v }.

It is compact in the weak-star topology sigma(L_infinity,L1): it is a
closed subset of the unit ball. The integral constraint is closed because
it is equivalent to integral_{B(0,j)} psi<=v for every positive integer j.
Those indicator functions belong to L1. Positivity and the upper bound
are also weak-star closed. This argument allows mass to escape to infinity
with a decrease of the integral; it does not incorrectly impose equality
on a noncompact ambient space.

The probability space P(K) is weakly compact. On these two convex compact
spaces consider the separately continuous affine payoff

    L(mu,psi) = integral psi(z) g_mu(z) dz - integral a_A(x) dmu(x).

For fixed mu, g_mu belongs to L1, giving weak-star continuity in psi.
For fixed psi, Gaussian convolution of psi is continuous, and its
composition with T is continuous on K. The same holds for a_A. Thus weak
continuity in mu follows. The bilinear case of Sion's minimax theorem gives

    min_mu max_psi L(mu,psi) = max_psi min_mu L(mu,psi).             (5)

Both extrema are attained: a supremum of continuous functions is lower
semicontinuous, and an infimum is upper semicontinuous. The inner minimum
on the right is the minimum of its continuous integrand over K.

Every bounded-centre Gaussian mixture p is positive, real analytic,
nonconstant, and tends to zero at infinity. Analyticity follows by locally
uniform integration of the entire Gaussian kernel over a compact support.
A nontrivial real analytic function has a null zero set. Therefore all
level sets {p=t}, t>0, are null. The function |{p>t}| is continuous and
strictly decreasing from infinity to zero for 0<t<max p. Finiteness for
t>0 follows from t|{p>t}|<=1. Positivity of p gives the limit at zero;
continuity, connectedness of R3 and nonflat levels give strict decrease.

There is consequently a unique t>0 with |{p>t}|=v. The unique maximizing
selector, up to null sets, is 1_{p>t}. Indeed, with B={p>t},

    integral (1_B-psi)p
      = integral (1_B-psi)(p-t) + t(v-integral psi) >= 0.           (6)

Equality forces psi=1_B off the null level set. This also proves that
the relaxed maximum equals C_p(v), and that the maximizing set is bounded.

Choose a minimizing mu* and a maximizing psi* in (5). They form a saddle
pair: L(mu*,psi*) equals the common value, so psi* maximizes the payoff
at mu*. By the uniqueness just proved, psi*=1_B with B given by (3).
This proves (2). Since q_B is continuous, its minimum is m(A), and
integral q_B dmu*=m(A), its value equals m(A) on the entire support of mu*.
The converse follows by integrating (4) against any competing probability
and using C_g(v)>=integral_B g. This proves the theorem.

## 2. Exact connection to the full conjecture

For the fixed K,T,s, the following are equivalent:

1. f_mu is majorised by g_mu for every mu in P(K).
2. m(A)>=0 for every measurable A with finite positive volume.
3. For each such A there is a B with |B|=|A| and

       integral_B gamma_s(z-Tx) dz >= integral_A gamma_s(z-x) dz
                                                        for all x in K. (7)

The set B may depend on A,K,T,s; it does not depend on a subsequently
chosen input law. It can have the form (3). This quantifier exchange is
stronger than selecting an optimizing target set separately for every mu.

To check the equivalence, for probability densities let

    H_p(a)=integral(p-a)_+.

The elementary superlevel-set formulas are

    H_p(a)=sup_{v>=0}[C_p(v)-av],
    C_p(v)=inf_{a>=0}[H_p(a)+av].                                 (8)

For the Gaussian mixtures here, the threshold selecting volume v proves
the second equality directly. The first follows by integrating p-a over
its positive set. These show that hinge order is equivalent to concentration
order. Taking all A of volume v and then applying Theorem 1 proves (7).

There is also an equality of defects, with the normalization used by the
team's [global criterion](../gaussian_majorisation_global_criterion/PROOF.md):

    sup_mu sup_{a>=0}(H_{f_mu}(a)-H_{g_mu}(a))_+
      = sup_A (-m(A))_+.                                         (9)

For a fixed pair, an upper bound delta on either all hinge differences or
all concentration differences transfers to the other by (8), with the same
additive delta. Hence their positive suprema agree. Finally the two suprema
over A and mu commute. Formula (9) retains every possible violation; it is
not a new proof that the defect vanishes.

This criterion is a set-compression obligation for the geometric lane.
One sufficient certificate is a target Gaussian-mixture superlevel set
whose kernel masses satisfy (7). Constructing such sets for all contractions
is still open. No convexity, spherical shape, finite component count, or
finite number of contact points is implied by the theorem.

## 3. The fixed dominant atom has its own exact dual

Take a nonempty compact K with 0 not in K, and suppose T is defined on
K union {0}, with T(0)=0. Fix 0<epsilon<1. Restrict the input class to

    mu_rho=(1-epsilon)delta_0+epsilon rho,       rho in P(K).       (10)

This fixes the atom's mass exactly. Define m_epsilon(A) by replacing mu
in (1) with mu_rho. The same argument, with the fixed term retained, gives

    m_epsilon(A) = max_{|B|=v} [(1-epsilon)q_B(0)
                                  + epsilon min_{x in K}q_B(x)]. (11)

An optimizing B is a superlevel set of

    (1-epsilon)gamma_s + epsilon (T#rho*)*gamma_s,

and the rare measure rho* is supported on the minimum set of q_B in K.
The exact condition for the fixed-atom class to obey all hinges is
m_epsilon(A)>=0 for every A. In particular, the pointwise target condition is

    q_B(x) >= -(1-epsilon)q_B(0)/epsilon          for all x in K. (12)

Requiring q_B(x)>=0 separately would discard the permitted compensation
by the fixed atom and would be a stronger test. Formula (11) supplies the
correct common-set version of the [fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md).
That reduction still requires arbitrary bounded rare packets. Nothing
here restricts them to the team's ordered rays or motion domains.

## 4. A unique nonatomic optimizer, even with a dominant fixed atom

The next theorem disproves a natural exact extremal step: minimizing (1)
or (11) cannot always be done on a finite number of atoms, even if that
number is allowed to depend on the particular problem.

**Theorem 2 (spherical obstruction).** Let

    K=R S^2,       R>0,       0<c<=1,       (cR)^2<=3s,
    T(x)=cx,      T(0)=0,    A=B(0,r),     r>0,

and let sigma_R be uniform probability measure on K. Allow epsilon=1
for the unanchored problem, or 0<epsilon<1 for (10). Define

    Phi(r,d) = integral_{B(0,r)} gamma_s(z-d e_1) dz.

Then

    m_epsilon(A)=epsilon[Phi(r,cR)-Phi(r,R)],                     (13)

and the unique minimizing rare law is rho*=sigma_R. The optimizing set
is A itself. The value is strictly positive for c<1 and is zero for c=1.
For every fixed positive integer N, restricting rho to at most N atoms
gives a strictly larger minimum than (13).

These are genuine contractions on the original three-dimensional support.
The theorem is not a Gaussian-majorisation counterexample. It concerns
exact attainment of the measure-side optimization, including examples
where the desired comparison is already true by an ordinary radial motion.

### The radial optimizer

For every rho on K, rotational invariance gives

    integral_A f_mu = (1-epsilon)Phi(r,0)+epsilon Phi(r,R),
    integral_A g_mu = (1-epsilon)Phi(r,0)+epsilon Phi(r,cR).       (14)

Since C_g(v)>=integral_A g, their difference is a lower bound in (13).
We show uniform rho attains it. A uniform spherical Gaussian mixture with
centres at radius d=cR has radial density, with t=|z|,

    h_d(t)=(2 pi s)^(-3/2) exp[-(t^2+d^2)/(2s)]
                                      sinh(dt/s)/(dt/s).         (15)

This follows by integrating exp((dt/s)u) over u uniform on [-1,1].
For z>0,

    coth z - 1/z < z/3.                                         (16)

One elementary proof expands

    (z^2+3)sinh z - 3z cosh z
       = sum_{k>=2} 4k(k-1) z^(2k+1)/(2k+1)! > 0.

Thus for t>0 the logarithmic derivative of (15) satisfies

    h_d'(t)/h_d(t)
      = -t/s + (d/s)[coth(dt/s)-s/(dt)]
      < -t/s + d^2 t/(3s^2) <= 0.                              (17)

The central Gaussian is also strictly decreasing in radius. Their mixture
in (10) is therefore strictly radially decreasing, so its volume-v top
set is precisely A. This proves (13) and attainment.

For c<1, Phi(r,cR)>Phi(r,R). For completeness, condition on the two
coordinates perpendicular to e_1. At each perpendicular position inside
the ball the permitted first coordinate is [-a,a], a>0. Differentiating
the Gaussian mass of this interval with respect to d>0 gives
gamma_{1,s}(a+d)-gamma_{1,s}(a-d)<0. Integration proves the strict claim.

### Why every finite law fails to attain the optimum

Equality in the lower bound from (14) means A is a maximizing set for
g_mu. The unique-superlevel-set argument in (6), followed by continuity
from inside and outside the sphere, forces g_mu to be constant on |z|=r.
The central component is constant there. Write the rare law as a probability
lambda on the unit sphere. Since c,R,r,epsilon are positive, the condition is

    omega -> integral_{S^2} exp(kappa omega.u) dlambda(u)
                  is constant on S^2,       kappa=cRr/s>0.       (18)

We prove directly that (18) forces lambda to be uniform. Subtract uniform
surface probability sigma and write tau=lambda-sigma. Averaging the left
side against sigma(omega) shows its constant difference is zero: the inner
spherical integral is independent of u and tau has total mass zero. Thus

    integral exp(kappa omega.u) dtau(u)=0       for all omega in S^2.

Integrate against tau(omega) and expand the uniformly absolutely convergent
exponential series. For each multi-index alpha=(alpha_1,alpha_2,alpha_3),
put M_alpha=integral u^alpha dtau(u). The multinomial formula yields

    0 = double_integral exp(kappa omega.u) dtau(omega)dtau(u)
      = sum_{k>=0} kappa^k/k!
                     sum_{|alpha|=k} (k!/alpha!) M_alpha^2.      (19)

Every summand is nonnegative. All polynomial moments of tau vanish.
Polynomials restricted to the sphere are dense in continuous functions
by Stone--Weierstrass, so tau=0. This proves uniqueness without assuming
any symmetry of the competing measure.

Finally the probabilities with at most N atoms form a compact subset of
P(K), as the image of K^N times the closed probability simplex. Gaussian
smoothing maps weak convergence of compactly supported laws to L1
convergence, and C_p(v) is continuous under L1 convergence. The restricted
minimum is attained. Its minimizer cannot be sigma_R, so uniqueness makes
the gap strictly positive. This completes Theorem 2.

## 5. What finite approximation does preserve

Let T be L-Lipschitz and let K_delta subset K be a finite delta-net.
Restricting the minimizing measure in (1) to this net gives a value m_delta.
Then

    0 <= m_delta(A)-m(A) <= (1+L)delta/sqrt(2 pi s).               (20)

For the anchored problem the upper bound is multiplied by epsilon.
The estimate is uniform over A and its volume.

Indeed Gaussian translates obey

    TV(gamma_s(. - x),gamma_s(. - y))
                               <= |x-y|/sqrt(2 pi s).            (21)

Integrate the directional derivative of the Gaussian along the segment;
its L1 norm is sqrt(2/(pi s)), and TV is half L1. Project a minimizing law
to a nearest net point. The resulting source and target density changes
have TV at most delta/sqrt(2 pi s) and L delta/sqrt(2 pi s), respectively.
Both integral_A p and C_p(v) change by at most TV for equal-mass densities.
This proves (20). In (10) only the rare fraction moves, giving epsilon.

Consequently a strictly negative m(A) always has a finite-prior witness
once this error is smaller than -m(A). The contact set need not be finite,
and exact minimizers need not be atomic; these facts are compatible.
This quantitative boundary complements, without replacing, the earlier
[finite strict rational-witness reduction](../gaussian_majorisation_rank_abel/PROOF.md).
No universal atom bound for detecting all possible failures is claimed or
disproved by Theorem 2. What it disproves is exact optimizer localization.

## 6. Scope of the handoff

The primary geometric object is a volume-constrained Gaussian superlevel
set. Compactness and minimax give a common set; analytic nonflatness makes
it deterministic; the equality set of its Gaussian mass potential localizes
the optimizing measure. The spherical example shows that this equality
set can genuinely support a unique diffuse optimizer. Dimensional
Caratheodory reasoning cannot be applied to the infinite family of target
selection constraints merely because the centres lie in R3.

The fixed-atom theorem, axial motion benchmark and ordered-weight orbit
theorem keep their original quantifiers. Our common-set condition is
necessary for an all-law positive result on an axial domain; its proof
does not construct a new motion or extend the ordered-ray weight cone.
For all compact domains, contractions and variances, proving (7), or its
anchored form (12), remains as strong as the full open question. A rigorous
negative value in (1) supplies an actual violating law. No such value for
a contraction is supplied here, and there is no new Kneser--Poulsen class.

The proof uses standard minimax, analytic zero-set, Gaussian rearrangement,
and polynomial-density facts, credited in SOURCES.md. No priority claim is
made for these general tools or for abstract comparison-of-experiments
duality. The exact finite checks in verify.py audit algebra and distinguish
the analytic setting from a finite model with tied levels. The universal
theorems rely on the written argument, not on numerical Gaussian integration.
