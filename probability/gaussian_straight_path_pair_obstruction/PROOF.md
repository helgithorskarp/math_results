# Negative pair contributions after straight-path time averaging

Author proof, 27 September 2026; independent review pending.
The unrestricted Gaussian-majorisation problem remains open.

The precise failed strengthening is: after joining contracted endpoints
by a straight path, each unordered pair's contribution to a Gaussian
hinge is nonnegative after integration over both space and time.
We prove that this fails on **every nontrivial member of the connected
tight-mesh test class with a fixed root tetrahedron**. A separate rational
ten-site control has strictly contracting, injective endpoints, paired
affine rank six, and a negative pair contribution even after optimal
orthogonal Procrustes alignment. Its full Gaussian comparison is positive.

The conclusion is about the canonical posterior-velocity decomposition
specified below. It does not exclude a different decomposition, a different
path, or an argument using compensation between pairs.

## 1. The pair decomposition and its normalization

Let x_i,y_i be finitely many labelled points in R3, with weights w_i>0
summing to one. Fix s>0. Put

    z_i(t)=(1-t)x_i+t y_i,       h_i=y_i-x_i,
    f_t(u)=sum_i w_i gamma_s(u-z_i(t)),        0<=t<=1,
    d_ij(t)=|z_i(t)-z_j(t)|^2,
    l_ij=|x_i-x_j|^2-|y_i-y_j|^2,
    v_ij=|h_i-h_j|^2.

Here d is a SQUARED distance. Direct expansion gives

    d_ij(t)=d_ij(0)-t l_ij-t(1-t)v_ij,
    d_ij'(t)=-l_ij+(2t-1)v_ij.                         (1)

Set pi_i(u,t)=w_i gamma_s(u-z_i(t))/f_t(u). The classical posterior
velocity V_t=sum_i pi_i h_i satisfies the continuity equation and

    div V_t = (1/s) sum_(i<j) pi_i pi_j
                              (z_i-z_j).(h_i-h_j)
            = (1/(2s)) sum_(i<j) pi_i pi_j d_ij'(t).    (2)

For H_f(a)=integral (f-a)_+, the pressure is a times the indicator of
f>a. Thus define the canonical time-integrated pair contribution by

    A_ij(a) = -a/(2s) integral_0^1 d_ij'(t)
                      integral_(f_t>a) pi_i(u,t)pi_j(u,t) du dt.       (3)

Then

    H_(f_1)(a)-H_(f_0)(a) = sum_(i<j) A_ij(a).            (4)

This is the usual continuity-equation identity
partial_t integral U(f_t)=-integral P(f_t) div V_t.
For completeness, positive levels of a finite Gaussian mixture have
zero Lebesgue measure. Smooth convex approximations to the hinge,
followed by dominated convergence on its bounded positive superlevel
sets, justify (3)--(4), including critical levels. Collision of some
centers along the path causes no singularity: f_t is strictly positive
and its posterior weights are smooth.

The cube satisfies u^3=6 integral_0^infinity a(u-a)_+ da. Therefore the
corresponding pair contribution for integral f_t^3 is

    B_ij := 6 integral_0^infinity a A_ij(a) da
           = -w_i w_j/s integral_0^1 d_ij'(t)
                              integral_R3 f_t gamma_i gamma_j du dt, (5)

where gamma_i=gamma_s(u-z_i(t)). Indeed, integrating a^2 from zero to
f_t in (3) gives f_t^3/3, and pi_i pi_j=w_i w_j gamma_i gamma_j/f_t^2.
The interchange is valid absolutely: the right side with |d_ij'| and
positive integrand bounds 6 integral a|A_ij(a)| da and is finite.

Gaussian square completion gives, with repeated labels permitted,

    integral gamma_i gamma_j gamma_k
        = C_(3,s) exp[-S_ijk(t)/(6s)],
    C_(3,s)=(2 pi s)^(-3) 3^(-3/2),
    S_ijk(t)=d_ij(t)+d_ik(t)+d_jk(t).                    (6)

Writing

    L_ijk=l_ij+l_ik+l_jk,    W_ijk=v_ij+v_ik+v_jk,

we have

    S_ijk(t)=S_ijk(0)-t L_ijk-t(1-t)W_ijk.               (7)

Equations (5)--(7) retain the entire spatial integral, every third label
with its prior weight, and the complete time interval. There is no
conditional replica tuple or sampled-time sign in the conclusion.

## 2. A moving tight pair has a negative cubic contribution

Assume y is a contraction of x, so every l_ab>=0. Fix i<j with

    l_ij=0,    v_ij>0,
    l_ik+l_jk>0 for at least one k of positive mass.      (8)

**Proposition 1.** At every s>0,

    B_ij <= -C_(3,s) w_i w_j v_ij/(36 s^2)
              sum_k w_k L_ijk exp[-S_ijk(0)/(6s)] < 0.  (9)

Consequently A_ij(a)<0 for some positive hinge threshold.

Proof. Put E_k(t)=exp[-S_ijk(t)/(6s)]. For 0<=t<=1/2,

    E_k(1-t)/E_k(t)=exp[(1-2t)L_ijk/(6s)].

Since L_ijk,W_ijk>=0, E_k(t)>=exp[-S_ijk(0)/(6s)].
Using exp(u)-1>=u and reflecting half the integral yields

    integral_0^1 (2t-1)E_k(t) dt
      = integral_0^(1/2) (1-2t)[E_k(1-t)-E_k(t)] dt
      >= L_ijk/(36s) exp[-S_ijk(0)/(6s)],                (10)

because integral_0^(1/2)(1-2t)^2 dt=1/6. Substitute
d_ij'=(2t-1)v_ij into (5)--(6). At least one summand is
strictly positive in (9). If all hinge pair contributions were
nonnegative, (5) could not be negative. QED.

The mechanism is explicit. The tight pair shrinks and subsequently
re-expands along the straight path. Contracted distances to other
positive-mass centers give its later expansion a larger overlap weight.
The resulting adverse pair action survives all the integrations in (5).

## 3. Application to every nontrivial reduced tight-mesh map

**Corollary 2.** Suppose a nontrivial finite contraction in R3 fixes four
affinely independent root labels. Suppose its common tight-edge graph is
connected, and every label has positive weight. At every variance, some
pair has B_ij<0, and hence A_ij(a)<0 at some positive threshold.

Proof. If h_i=h_j on every common tight edge, connectivity makes h
constant on all labels. It is zero at the fixed roots, so the map would
be the identity. Choose a tight edge with h_i-h_j nonzero.

At least one endpoint, say i, moves. It cannot preserve all four
distances to the fixed roots: subtracting one squared-distance equality
from the other three would force y_i-x_i to be orthogonal to three
independent root differences, and hence zero. Therefore l_ik>0 for
some root k. All other losses are nonnegative and w_k>0, so (8) holds.
Proposition 1 applies. QED.

The [accepted indecomposable reduction](../gaussian_indecomposable_contractions/PROOF.md)
has a fixed root tetrahedron and a facet-connected system of nondegenerate
common tetrahedra covering every label. Their edge graph is connected.
Corollary 2 therefore applies to EVERY nontrivial step in that test class,
with exactly its strictly positive weight convention. Indecomposability
itself is not needed for the corollary.

This gives sign information about the proposed route, not a negative
endpoint hinge. The reduction remains valid. Any proof of its unknown
Gaussian sign based on (3) must exploit cancellation between pairs or
modify the path/decomposition; termwise nonnegativity cannot hold even
after complete time integration. A different adverse threshold may arise
at each variance. No universal threshold is asserted.

An existing positive control makes the corollary concrete without a new
geometric classification. Use the accepted reduction's seven-site fixture

    x=((0,0,0),(-1,-1,0),(-1,0,1),(0,-1,1),
                           (1,-2,5),(-2,-5,-1),(-5,1,2)).

Keep the first four sites fixed, and subtract (8/3) times, respectively,
(1,1,1), (1,-1,-1), (-1,1,-1) from the last three sites.
This is the previously classified positive indecomposable three-cap
example, not a new family. For uniform weights and edge (0,4), take k=1:

    l_04=0, v_04=64/3, S_041(0)=62, L_041=32/3.

Consequently its pair contribution at every variance satisfies

    B_04 <= -C_(3,s) [512/(27783 s^2)] exp[-31/(3s)] < 0.

The small check here only verifies these new adverse-edge ingredients,
the 21 contractions, root rank and tight connectivity. The existing
indecomposability classification and positive motion are not replayed.

## 4. A strict, injective control with optimal global alignment

The tight-pair argument might be dismissed as a boundary effect or an
avoidable target rotation. The following concrete positive control
removes both explanations.

Let b=(3,3,3), e_1,e_2,e_3 be the coordinate basis, and take ten sites

    x_0=b,
    x_(r,+)=b+e_r,
    x_(r,1)=b-4e_r,   x_(r,2)=b-5e_r,       r=1,2,3.     (11)

Use uniform mass 1/10 and variance s=1. Put

    lambda=9999/10000,
    F(x)=(|x_1|,|x_2|,|x_3|),
    y_i=b+lambda(F(x_i)-b).                              (12)

Both endpoint configurations have ten distinct sites. The global map
in (12) is lambda-Lipschitz, so all 45 nontrivial pair distances strictly
decrease. Their minimum squared loss is 1-lambda^2=19999/100000000.
At lambda=1 the four anchors b,b+e_r are fixed and the moving-site
displacements span R3. Thus the paired affine rank is 3+3=6.
The affine invertible change on the second coordinate block in (12)
preserves that rank for every lambda>0.

Let X,Y denote the uniform endpoint laws. A direct centered calculation is

    E[(X-E X)(Y-E Y)^T]
          = lambda[(7/5)I-(4/25)11^T].                  (13)

Its eigenvalues are lambda*23/25 once and lambda*7/5 twice, all
strictly positive. Hence the unique orthogonal Procrustes alignment
is the identity after centering. To see uniqueness without a numerical
SVD, diagonalize this positive matrix: maximizing tr(O M) over
orthogonal O requires all three positive-eigenvalue diagonal entries
of O to equal one, and hence O=I.

The optimal translation only adds a common linear translation to the
straight path; every pair action in (3) is invariant under this change.
Thus the calculation below already uses the optimally aligned geometry.

Distinguish i=(1,1), j=(1,2). In the notation of (1),

    d_ij(0)=1,
    l_ij=1-lambda^2 < 1/5000,
    v_ij=(1+lambda)^2 > 3.                              (14)

For the third label k=0 at b,

    S_ij0(0)=42,
    L_ij0=42-6lambda^2 >= 36.                           (15)

For every k, L_ijk,W_ijk>=0. Also E_k(t)<=1 since S_ijk(t)
is a sum of squared distances. Keeping the one useful term k=0
in (10) and summing the negative -l_ij term over all k gives

    sum_k w_k integral_0^1 d_ij'(t)E_k(t) dt
       >= (v_ij/36) sum_k w_k L_ijk exp[-S_ijk(0)/6]-l_ij
       > (3/10)exp(-7)-1/5000.                         (16)

The elementary estimate

    e <= 1+1+1/2+1/6+1/24+(1/120)/(1-1/6)
      = 1631/600 < 11/4

therefore shows that (16) is larger than the exact positive number

    D=(3/10)(4/11)^7-1/5000
      =5088829/97435855000 > 0.                         (17)

Combining (5)--(6) proves the quantitative strict bound

    B_ij < -C_(3,1) D/100 < 0.                         (18)

Since f_t<=C_1=(2 pi)^(-3/2), A_ij(a)=0 for a>=C_1.
Equations (5) and (18) even imply that some 0<a<C_1 satisfies

    A_ij(a) < -D/(300*3^(3/2)).                         (19)

Indeed, if all these A_ij were at least the displayed negative constant,
then 6 integral_0^(C_1) a A_ij(a) da would be at least
-C_(3,1)D/100, contrary to (18). This proves existence, with a
quantitative negative value, without locating the threshold.

## 5. The control's full Gaussian comparison is positive

Coordinatewise absolute value is a composition of three hyperplane
folds. A single fold has a contracting motion in R4: rotate the
negative half-space through angle theta from 0 to pi in the plane
of its normal and one auxiliary coordinate, keeping the positive
half-space fixed. Pairs in either half-space keep their distances;
for an opposite-side pair the squared distance decreases with
cos(theta). The endpoints lie in the original R3.

Aishwarya--Li's continuous-contraction theorem and the at-most-two-
auxiliary-coordinate consequence give full Gaussian majorisation for
each fold, for every prior and variance. The subsequent homothety
in (12) has a continuous contracting motion in R3. Apply these
comparisons successively at the same variance. Consequently

    H_(sum_i w_i gamma_s(. - y_i))(a)
       >= H_(sum_i w_i gamma_s(. - x_i))(a)

for every probability weight vector, s>0 and a>=0. These are known
positive mechanisms, not a new positive class or KP consequence.
Equation (19) is compensated by other pairs in (4).

The ten-site strict control is not asserted to be indecomposable:
its displayed factorization is intentional. Corollary 2 supplies
the separate universal obstruction on the actual indecomposable
test class. No minimum number of sites for this obstruction is claimed.

## 6. Exact checks, attribution and scope

The standard-library checker reconstructs (11)--(12), all 45 strict
pair constraints, paired rank six, the centered cross covariance and
its positive eigenvalues, every triple's distance polynomial, and
the rational margin (17). It separately compares all coefficients
from the 1000 ordered Gaussian-cubic triples with the unordered-pair
expansion to check the factor in (5). Controls cover the undamped
tight edge, point collapse, identity, and an expansive parameter.
It also verifies the new pair-action data on the prior seven-site
positive indecomposable control, without reclassifying its interval.

The checker evaluates no Gaussian integral and selects no hinge
threshold. The posterior identity, square completion, time-reflection
inequality, tight-root argument, layer-cake implication and fold
comparison are written mathematical premises. Exact finite checks
do not constitute independent review or formalization.

The posterior method is classical and is already used in the team's
accepted local contact estimate. That estimate signs an inward
variation and controls its remainder; it does not assert pairwise
positivity along the entire path. The present obstruction does not
contradict it. R2's conditional-kernel obstruction concerns a different
decomposition before its replica/time averages. Here a single physical
pair remains negative after both of those operations in the cubic
stress formula; only the sum over pairs is left.

The [sources and handoff](SOURCES.md) distinguish these dependencies.
No historical-priority claim, negative total hinge or beta, full
dimension-three theorem, or new Kneser--Poulsen result is asserted.
