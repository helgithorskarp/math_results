# Two rigid bodies: joint levels, ball unions, and Gaussian hinges

This is an author proof; independent review is pending. No adverse datum
is assumed to have been found. All volumes below are Lebesgue volumes in
R3. Write gamma_s(x)=(2 pi s)^(-3/2) exp(-|x|^2/(2s)) and
H_f(h)=integral(f-h)_+. The desired sign is H_target-H_source >= 0.

## 1. Domain and equivalence

Let K_A,K_B be compact convex subsets of R3, and let I_A,I_B be Euclidean
isometries. Suppose

    |I_A a-I_B b| <= |a-b|                 (a in K_A, b in K_B).       (1)

They agree on any overlap, by setting a=b, so they define a contraction
T on K=K_A union K_B. There is no interior, dimension, disjointness,
continuous-motion, or common-anchor assumption.
By the classical Kirszbraun theorem, T extends to a 1-Lipschitz map on
all of R3. Thus a supported-law counterexample has the global-map form
required by the headline conjecture as well.

The following statements are equivalent for this fixed T and K:

**G.** Every probability law mu supported on K satisfies Gaussian
majorisation under T, at every common variance s>0.

**B.** Every finite labelled selection p_i in K, with arbitrary radii
r_i>0, satisfies

    |union_i B(Tp_i,r_i)| <= |union_i B(p_i,r_i)|.                    (2)

**J.** For every finite probability law mu_A on K_A and mu_B on K_B,
every pair of variances s_A,s_B>0, and thresholds a,b>0, put

    f_A=mu_A*gamma_(s_A),  f_B=mu_B*gamma_(s_B),
    g_A=(I_A#mu_A)*gamma_(s_A),  g_B=(I_B#mu_B)*gamma_(s_B).

Then

    |{g_A>a} intersection {g_B>b}|
       >= |{f_A>a} intersection {f_B>b}|.                            (3)

G implies B by the finite case of Aishwarya--Li Theorem 5.1. Section 5
also gives a direct quantitative contrapositive, without importing that
theorem. B implies J by Sections 2--3. J implies G by Section 4, using
only the equal-variance subcase of J. Thus permitting unequal variances
in J does not strengthen the universal assertion G in this class.

This is an equivalence of assertions, not a proof of any of them. In
particular, a strict violation of (3), even with unequal variances,
implies an actual bounded finite-law counterexample to G, on K and with
the same T. Its weights, centres within the bodies, and common variance
can differ from those in (3).

## 2. Classical Gaussian ball envelope, with its labels retained

Use the unnormalised kernel profile

    F(x)=sum_i w_i exp(-|x-p_i|^2/(2s)),   w_i>0, sum_i w_i=1.

The Gaussian peak factor is absorbed into the level t>0. For a probability
vector lambda put

    c_lambda=sum_i lambda_i p_i,
    V_lambda=sum_i lambda_i |p_i-c_lambda|^2,
    E_lambda=sum_i lambda_i log(lambda_i/w_i),
    r_lambda(t)^2=-2s log t-V_lambda-2s E_lambda.                    (4)

Use 0 log 0=0. Negative or zero squared radii contribute no open ball.
The Gibbs variational identity and the variance identity give

    log F(x)=sup_lambda [-|x-c_lambda|^2/(2s)
                         -V_lambda/(2s)-E_lambda].                 (5)

Indeed the difference between the left side and the expression at lambda
is KL(lambda||pi(x)), where pi_i(x) is the Gaussian posterior. Therefore

    {F>t}=union_(lambda: r_lambda(t)^2>0) B_open(c_lambda,r_lambda(t)). (6)

The supremum is attained at pi(x). This is a labelled version of the
classical Gaussian KDE ball-envelope representation; no novelty is claimed
for (5) or (6). Keeping lambda as the label avoids any need for uniqueness
of a barycentre representation.

If all p_i in a component undergo one isometry, its c_lambda undergoes
that isometry while V_lambda, E_lambda and r_lambda remain identical.
The formula works separately for s_A and s_B: no equality of those
variances is used here.

## 3. Rigidity preserves the barycentric contraction; B implies J

For finite endpoint lists A=(a_i), B=(b_j), with each block moved rigidly,
let delta_ij=|a_i-b_j|^2-|I_A a_i-I_B b_j|^2 >= 0. For any probability
vectors lambda,eta, expansion of the squares gives

    |sum lambda_i a_i-sum eta_j b_j|^2
      -|sum lambda_i I_A a_i-sum eta_j I_B b_j|^2
       =sum_ij lambda_i eta_j delta_ij >= 0.                        (7)

The within-block variance terms cancel because each block is rigid. Thus
a contraction on two finite rigid lists extends, by the same isometries,
to their separate convex hulls. Coincident barycentres have coincident
images, so repeated labels cause no ambiguity.

Apply (6) to both profiles. Choose any finite collections of posterior
labels in the two blocks. Their ball radii are preserved, and (7) proves
contraction of all their centres. By B their total union cannot grow.
The volume of each individual block union is exactly invariant under
its isometry. Inclusion-exclusion therefore says that their intersection
volume cannot decrease.

One can choose nested finite posterior lists covering each whole open
superlevel set: rational probability vectors are dense, (4) is continuous,
and strict membership in one ball persists under a small label change.
These bounded open sets have finite volume. Continuity from below of
Lebesgue measure passes the finite intersection inequality to (3).
This also explains exactly where separate convexification is needed.

## 4. J implies the actual hinge inequality

For u,v,h>=0,

    (u+v-h)_+-(u-h)_+-(v-h)_+
       =integral_0^h 1_(u>t) 1_(v>h-t) dt.                         (8)

Both sides are nonnegative and at most u+v. A probability law on K can
be split into subprobability laws on K_A and K_B; on their overlap assign
the mass to either block. For finite laws, apply J at equal variance,
absorbing the two block masses into the thresholds in (8). Each separate
block hinge has unchanged integral because its whole density moves
isometrically. Tonelli's theorem and (8) give H_target>=H_source for
every h>0. Zero block mass and h=0 give equality.

For a general law, quantise the two parts separately on their original
compact supports. The source and target Gaussian densities converge in
L1 at each fixed variance. This follows directly from the uniform L1
continuity of translated Gaussian kernels on bounded centre sets. Since
the hinge integral is 1-Lipschitz in the density's L1 norm, the finite
inequality passes to the limit. This proves G for all bounded laws on K.

The interaction identity (8) is elementary and already used in prior team
work; it is not claimed as a new result.

## 5. Quantitative conversion of any adverse ball union

Suppose a finite contracted list of N balls has the *certified* sign

    V_Q-V_P >= delta > 0.                                         (9)

This is a premise; no such list is supplied here. For a chosen epsilon>0,
let

    Z=sum_i exp(r_i^2/(2 epsilon)),
    w_i=exp(r_i^2/(2 epsilon))/Z,
    h=(2 pi epsilon)^(-3/2)/Z,
    f=sum_i w_i gamma_epsilon(.-p_i),
    g=sum_i w_i gamma_epsilon(.-q_i).                              (10)

Repeated source centres may be merged; contraction ensures they have the
same target centre. Different radius labels simply contribute different
positive weights at that centre. Write

    F_P=f/h=sum_i exp((r_i^2-|x-p_i|^2)/(2 epsilon)).

The clipped integral M_P=integral min(F_P,1) equals V_P+E_P, with E_P>=0,
because min(F_P,1)=1 throughout the union. Outside the union, every
individual exponential is less than one; consequently

    E_P <= 4 pi sum_i integral_(r_i)^infinity
                    rho^2 exp((r_i^2-rho^2)/(2 epsilon)) d rho
        <= 4 pi [epsilon sum_i r_i
                  +N sqrt(pi/2) epsilon^(3/2)].                    (11)

For the second inequality, integration by parts gives the term epsilon*r_i;
in the remaining integral put rho=r_i+u and use
rho^2-r_i^2>=u^2. This bound also covers zero radii, which can alternatively
be discarded since their balls have zero volume.

Choose any rational upper bounds R_i>=r_i and take

    0<epsilon<=min(1, delta/(32 sum_i R_i+64N)).                    (12)

Using pi<4 and sqrt(pi/2)<2 in (11) gives E_P<delta/2. Since both f and g
have total mass one,

    H_g(h)-H_f(h)=h(M_P-M_Q)
                 <=h[-delta+E_P] < -h delta/2.                   (13)

Thus (10)--(12) are a finite actual common-variance Gaussian counterexample
with an explicit strict margin. The construction is a quantitative finite
version of Aishwarya--Li's existing variable-radius argument. It does not
claim a new Gaussian-to-KP principle. The weights depend exponentially
on epsilon; this is not a new fixed-prior low-noise exclusion or search.

## 6. A finite certificate interface for an adverse joint contact

For source normalised profiles F_A,F_B (peak factors removed), assume that
positive a,b,eta_A,eta_B,delta have been certified to satisfy

    |{F_A>a exp(eta_A)} intersection {F_B>b exp(eta_B)}|
       -|{G_A>a} intersection {G_B>b}| >= delta.                  (14)

Here G denotes the rigidly moved profile, and the two component variances
may differ. Only this adverse-volume premise needs to be supplied.

Suppose all source centres have norm at most R and take

    L=R+max(sqrt(2s_A log(1/a)), sqrt(2s_B log(1/b))).

A nonempty (14) necessarily has a,b<1. The tightened source intersection
lies in B(0,L). In block k, each posterior coordinate on that ball has
the lower bound

    pi_i(x)>=tau_k:=w_min,k exp(-(L+R)^2/(2s_k)).                  (15)

Any smaller certified positive tau_k suffices. For each block choose an
integer m_k with

    4 n_k^2/(m_k^2 tau_k) <= eta_k.                               (16)

Let Lambda_m be the finite simplex grid with denominator m. Rounding the
first n-1 coordinates down and putting the remainder in the last gives,
for every posterior pi, a lambda in Lambda_m with

    ||lambda-pi||_1<=2n/m,
    KL(lambda||pi)<=sum_i (lambda_i-pi_i)^2/pi_i
                   <=4n^2/(m^2 tau_k)<=eta_k.                    (17)

The KL bound follows from log u<=u-1, with zero coordinates handled by
continuity. From (5), the balls (4) at level a, respectively b, using
these finite label grids contain the tightened source superlevel sets.
Their target block unions are contained in {G_A>a}, respectively {G_B>b}.

Let U_AP,U_BP,U_AQ,U_BQ be these four finite unions. Equation (14) gives

    |U_AP intersection U_BP|-|U_AQ intersection U_BQ| >= delta.

The two single-block union volumes are invariant. Hence their *total*
union has exactly the adverse sign (9). Equations (10)--(13) then supply
the Gaussian counterexample. The number of generated labels is at most

    binom(m_A+n_A-1,n_A-1)+binom(m_B+n_B-1,n_B-1).                 (18)

This crude explicit bound is not claimed to be computationally practical.
Adaptive finite subcovers may be much smaller, but require their own cover
certificates. The theorem does not treat finite sampling as such a cover.

Every strict negative joint-level volume at positive thresholds admits
a tightening (14). A finite Gaussian mixture is real analytic, nonconstant,
and tends to zero at infinity; every positive level set has volume zero.
Dominated convergence on a common bounded ball therefore makes the source
intersection volume continuous as the two tightened thresholds decrease to their
original values. Choose small positive eta_A,eta_B and then delta below
the remaining strict gap. Critical levels require no regularity assumption.

If the original centres are rational, the grid barycentres are rational.
The entropy radii are explicitly computable real numbers. They may be
shrunk to positive rational radii while retaining a strict union gap:
shrinking the target union loses at most the sum of the individual shell
volumes, which tends to zero. For example, with r_i<=R_* and radius errors
at most e, that loss is at most 4 pi N R_*^2 e. Discard zero radii and choose
e so this is below delta/2. Formula (10) then uses only exponentials of
rational parameters. Exact rational priors are also obtainable by L1
approximation, since the strict hinge margin survives a sufficiently
small weight perturbation at the same positive threshold. None of these
roundings is needed for the existence proof.

## 7. Scope and verification

The equivalence does not settle the two-body sign, the proper screw, or
the full dimension-three conjecture. It adds no positive neighborhood,
eventual-variance region, or new proved Kneser--Poulsen class. Its concrete
use is to turn a certified *unequal-variance joint contact* into decisive
evidence for the original common-variance headline, with a specified
finite conversion and error budget.

The standard-library checker audits finite algebra and the budget in
(12), on an asymmetric rational rank-six control. It supplies no adverse
volume premise. Gibbs duality, analytic level-set nullity, measure limits,
and the Gaussian tail integration are written analytic proof obligations.
Passing the checker is not formal verification or independent review.
