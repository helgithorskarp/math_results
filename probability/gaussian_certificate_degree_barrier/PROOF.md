# A degree barrier for the supplied Gaussian moment certificate

Complete author argument, 26 September 2026; independent review pending.
This is a lower bound for a specified sufficient certificate, not a Gaussian
counterexample, a lower bound for every possible certificate, or a resolution
of the dimension-three conjecture.

## 1. The first Bernstein cell cannot pass

Let f and g be probability densities bounded above by C. In the Gaussian
application C=(2 pi s)^(-3/2), since both densities convolve probability laws
with the covariance-sI Gaussian. Write

    H(u)=integral(g-Cu)_+ - integral(f-Cu)_+,   0<=u<=1.

The [finite-certificate interface](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md)
uses a supplied signed endpoint H>=0 on [0,tau], a source peak bound b,
and a modulus K on [d,1], where 0<d<tau<b<1. For an integer N>=0 put

    h=1/(N+2), t_k=(k+1)/(N+2), v_k=t_k(1-t_k)/(N+3),
    J_N={k:0<=k<=N, dist(t_k,[tau,b])<=h}.

A rigorous lower bound ell_k for E H(V_k), with
V_k~Beta(k+1,N-k+1), must satisfy, for every k in J_N,

    ell_k > p_k + K sqrt(v_k+h^2),                            (1)
    p_k=1 if t_k<=d, otherwise v_k/(t_k-d)^2.

We retain this particular Cantelli-tail penalty and index-selection rule.
Replacing the rule, penalty, kernel or localization estimate changes the
certificate and is outside the lower bound below.

**Theorem 1.** If K>=1, any successful certificate (1) necessarily has

                         N+2 > 2/tau.                       (2)

This holds even if every beta average is known exactly, with no moment
enclosure error. It uses only probability normalization and the density cap.

**Proof.** Since 0<=g/C<=1, pointwise

    (g-Cu)_+ <= (1-u)g.

Indeed, writing x=g/C, the difference in the region x>=u is Cu(1-x)>=0;
in the other region the left side is zero. Therefore

    H(u)<=1-u,    E H(V_0)<=(N+1)/(N+2).                     (3)

No positivity of H is assumed to obtain this upper bound. If tau<=2h,
then k=0 belongs to J_N: its grid location is h; a lower endpoint tau>h
is at distance at most h, and an upper endpoint b<h is also at distance
less than h because b>0. Conversely, if tau>2h then k=0 is not selected.
The equality case tau=2h is selected, because the rule uses <=.

If t_0<=d, then p_0=1, already contradicting (1) and (3). Otherwise d>0
implies

    p_0 >= v_0/t_0^2=(N+1)/(N+3),
    v_0+h^2=2/((N+2)(N+3)).                                 (4)

The gap between the upper bound in (3) and the lower bound for p_0 is
(N+1)/((N+2)(N+3)). It is strictly smaller than sqrt(v_0+h^2), because

    2(N+2)(N+3)-(N+1)^2=N^2+8N+11>0                         (5)

for every integer N>=0. Thus the right side of (1), already with K=1,
exceeds an upper bound for its left side. This is impossible. Hence k=0
must be absent, which is exactly (2). QED.

The argument does not assert that every useful local modulus must be at
least one. A separately justified smaller modulus, a sharper lower-tail
penalty or another treatment of the first cell requires separate analysis.
The two automatic moduli supplied by the interface will both exceed one
on the benchmark below.

## 2. Composing with the supplied signed-tail input

For finite atomic supports in radius-R balls, minimum assigned mass m>0,
and variance s, the interface's mean-support tail lemma permits

    0<Delta<=mean(h_X)-mean(h_Y),
    B=6R^2+2s log(1/m),  Q=4B/Delta,
    0<tau<=exp(-Q^2/(2s)).                                  (6)

Here h_X is the support function of the finite source support and the
mean is the normalized spherical average. Separate translations of the
supports are permitted and do not change these averages. We consider
atomic data, so there is no additional cloud-radius loss in Delta.

**Lemma 2.** Every valid choice in (6) satisfies

    Delta<=R,  Q>=24R,  tau<=exp(-288R^2/s).                 (7)

**Proof.** Center the radius-R source ball at zero. Its support function
is at most R. The spherical mean of any nonempty support function is
nonnegative: h_Y(u)+h_Y(-u) is a width and is nonnegative. Thus
Delta<=mean(h_X)-mean(h_Y)<=R. Also m<=1, so B>=6R^2.
Substitution in (6) proves (7). QED.

If no positive Delta is available, this particular signed-tail input
cannot be supplied in the first place. Lemma 2 is a necessary bound for
every valid positive Delta; it does not presume that a numerical support
estimate is a lower bound. Allowing oracle-quality Delta and exact scalar
evaluation cannot improve the optimistic right side of (7).

**Corollary 3.** Combining (1) with the supplied tail input (6), whenever
K>=1, forces

                    N+2 > 2 exp(288R^2/s).                  (8)

This is an exponential degree lower bound for these two particular
ingredients used together. It does not contradict the interface's eventual
completeness theorem or the team's O(k^8) *defect-approximation* schedule.
Those statements have different quantifiers and purposes. In particular,
an approximation error guarantee is not a successful strict positive
certificate for one pair.

## 3. A genuinely relevant finite benchmark

Use the classical simplex-flap pair in R3. Let v_0,...,v_3 be the four
vectors in {+/-1}^3 having coordinate product +1. The sixteen labelled
source and target sites are

    x_i=y_i=v_i                         (four core sites),
    x_ij=v_j-v_i, y_ij=v_j+v_i, i!=j    (twelve flap sites).  (9)

All labels have mass 1/16. For an additional parameter 0<=a<=1, replace
every target site by a y. Keep variance 0<s<=1.

The endpoint a=1 is the reversed Cheng--Tan--Zheng simplex-flap expansion.
Their Theorem 2.1 proves it has no continuous contracting motion in R5.
The construction and nonliftability theorem are credited prior work, not
consequences of our checker. The source data already appear in the team's
[rank/Abel packet](../gaussian_majorisation_rank_abel/flap_fixture.json).

The map (9) is a contraction. For a core/flap pair its squared-distance
deficit is 16 when the core index equals the flap's first index, and zero
otherwise. For two flaps, the source-minus-target deficit is

                  16(1_{j=k}+1_{l=i})>=0.                  (10)

The source sites are distinct. Scaling all targets by a<=1 retains the
contraction, and a<1 makes every pair of distinct inputs strictly contract.
At a=0 the target law is a single point, so its Gaussian majorises every
source Gaussian mixture by the elementary Jensen/translation argument.
This known positive control is part of the degree obstruction, not a new
positive comparison example.

All source norms are at most sqrt(8), and the source contains the antipodal
pair (0,2,2), (0,-2,-2). Hence **every** containing source ball, with any
translation, has radius at least sqrt(8), and the radius sqrt(8) is attained
at the origin. The scaled target sites lie in that same ball. Thus no
translation or sharper minimum enclosing-ball calculation can make the
shared radius parameter in (6) smaller than sqrt(8).

The automatic moduli in interface (I6) are

    K=min{1/d, sqrt(2/pi)/3 [R/sqrt(s)+sqrt(2log(1/d))]^3}.    (11)

Both entries exceed one here: 1/d>1 and, using pi<4 and R/sqrt(s)>=sqrt(8),
the geometric entry is greater than 16/3. Its coarser rational upper
enclosure has the same property. We do not rule out a separately supplied
sharper modulus; it is not one of these automatic inputs.

Consequently every successful certificate using (6) and either automatic
modulus, at any a in [0,1] and 0<s<=1, must satisfy

                    N+2 > 2 exp(2304/s),
                    N > 10^1000.                            (12)

For the last bound, the exact rational Taylor sum

               sum_{j=0}^{16} (288/125)^j/j! > 10            (13)

certifies exp(288/125)>10. Raising to the thousandth power gives
exp(2304)>10^1000. Equation (12) then follows from (8), including the -2
when solving for N. No floating exponential or logarithm is a premise.
The existing arithmetic consumer calls for moments through power N+2;
literal tabulation at this scale is excluded before any moment enumeration.
This is not a lower bound on a symbolic proof compressing an infinite or
large family of such inequalities.

## 4. Interpretation and exact checking

The finite-computation lane therefore should not start a larger moment
producer for this benchmark with the supplied endpoint/modulus/index
combination. Even perfect moments cannot overcome its degree prerequisite.
Potential repairs must provide a materially larger signed interval, change
the first-cell localization or kernel, supply a different analytic sign
argument, or prove a compressed family of inequalities. No such repair or
unrestricted Gaussian sign is asserted here.

[verify.py](verify.py) reconstructs the sixteen sites from the tetrahedron,
checks every contraction deficit and the minimum-radius witness, and checks
the universal first-cell rational identities by polynomial coefficient
arithmetic. Positivity in (5) is certified by its three positive
coefficients, not samples of N. It checks the rational Taylor lower bound
(13) and exact boundary inclusion/exclusion controls for J_N. Tests remain
active under Python -O. The entire universal reduction is written above;
the code is a compact audit, not an exhaustive search of Gaussian laws.

The checking code, Python exact arithmetic, the elementary analytic facts
about densities, spherical means and exponentials, and the stated external
certificate interface are the trust boundary. This is not a proof-assistant
formalization or independent acceptance. No integral sign, moment list,
Gaussian quadrature, large artifact or private input is needed.
