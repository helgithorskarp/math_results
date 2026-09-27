# Polynomial margins for norm-preserving Gaussian comparisons

Complete author argument, 27 September 2026; independent review pending.
The unrestricted R3 question remains open. This is a quantitative handoff
for R2/R3/R8: the threshold dependence exp(-O(tau^-2)) in R8's strictness
bound is replaced by a fixed power. It does not enlarge the already signed
norm-preserving class, add a neighborhood, or prove a new KP consequence.

## 1. Whole-curve theorem

Let mu be a bounded probability law in R3, T a contraction on its support,
and s>0. Suppose independent anchors a,b and an integer R>=1 satisfy

    |x-a|=|T(x)-b| <= R sqrt(s).

Put f=mu*gamma_s, g=T#mu*gamma_s, C_s=(2pi s)^(-3/2), and

    H(u)=integral(g-C_s u)_+ - integral(f-C_s u)_+,
    d=E[|X-X'|^2-|T(X)-T(X')|^2]/s,
    m=||g||_infinity/C_s,        A_R=2^-(40R^2+9R+38).

The loss is ORDERED and dimensionless. Then, simultaneously for 0<=u<=1,

    H(u) >= d A_R u^3 (m-u)_+^8.                           (1)

Thus any certified 0<p<=m gives the explicit lower envelope

    H(u) >= d A_R u^3 (p-u)_+^8.                           (2)

The choice p=2^-R^2 always works. There is no minimum mass, atom count,
covariance or positive loss floor. The estimate is uniform in the stated
parameters, including d tending to zero. The d=0 case is isometric equality.
Neither the coefficient nor the endpoint powers are claimed optimal.

The nonnegative sign itself is already independently accepted in the
[norm-preserving theorem](../gaussian_norm_preserving_majorisation/PROOF.md).
The new information is a polynomial quantitative lower envelope through
both threshold boundaries. The prior bound may be stronger on some bands
at large R and remains available.

## 2. Shorter radial localization of the positive kernel

We import the reviewed spherical kernel, equation (11) of that theorem.
The cap construction, radial-crossing method and diffuse passage are
credited to R8's [strictness proof, Sections 3--4](../gaussian_norm_preserving_strictness/PROOF.md),
now independently accepted at graph6556. Here are all constants needed
with the new cutoff.

Normalize s=1 and both anchors to zero. First take a finite positive prior.
For independent uniform theta,eta in S2 and t in [0,1], set

    v_i=C w_i exp[-rho^2/2-|p_i|^2/2
                       +rho((1-t)theta.p_i+t eta.q_i)],
    F=sum_i v_i,            delta_ij=|p_i-p_j|^2-|q_i-q_j|^2.

For the smooth convex hinges below, the exact nonnegative identity is

    integral U(g)-integral U(f)
      =4pi integral rho^4 integral_0^1 t(1-t)
          E sum_(i<j)delta_ij v_i v_j U''(F) dt drho.       (3)

The radius and common norms give

    F<=C,   |F_t|<=2rho RC,   |F_rho|<=(rho+R)C,
    |F(eta)-F(eta')|<=rho RC|eta-eta'|,
    sum_(i<j)delta_ij v_i v_j >=(d/2)C^2 exp[-(rho+R)^2]. (4)

Suppose 0<tau,epsilon<=1 and C tau<=h<=max(g)-C epsilon.
A mode z_* of g has |z_*|<=R by its posterior mean identity. Move
outwards by epsilon/4 to z_0=rho_0 eta_0. The gradient bound ||grad g||<=C
gives epsilon/4<=rho_0<=B=R+1 and g(z_0)>=max(g)-C epsilon/4.
Restrict to

    1-a_0<=t<=1-a_0/2,   a_0=epsilon/(16BR),
    |eta-eta_0|<=b_0,    b_0=epsilon/(8BR).

Each change from t=1,eta=eta_0 costs at most C epsilon/8, uniformly in
theta. Thus F(rho_0)>=h+C epsilon/2. The t weight integrates to at least
a_0^2/8, and the cap probability is b_0^2/4.

Replace the prior cutoff R+2/tau by

    ell=log(2/tau),   L=R+sqrt(2ell),   W=L+R.              (5)

It exceeds rho_0, since sqrt(2log2)>1>epsilon/4. The Gaussian envelope
gives F(L)<=C exp[-(L-R)^2/2]=C tau/2. If U'' is a smooth probability
density sufficiently close to h, its antiderivative U'(F) changes from
one to zero along the ray. The fundamental theorem and (4) give

    integral_(rho_0)^L U''(F) drho >=1/(CW).

This needs neither a monotone ray nor a regular level. Restrict (3) to
these rays, use rho>=epsilon/4, and multiply the lower bounds:

    4pi*(epsilon/4)^4*(d/2)C^2 exp(-W^2)
                         *(a_0^2/8)*(b_0^2/4)/(CW).

Consequently

    H(h/C) >= [pi C epsilon^8 exp(-W^2)/(2^26 B^4 R^4 W)]d. (6)

The smooth hinges obey 0<=U(v)<=v, so domination by each probability
density justifies their limit over all R3. Quantize a diffuse law on its
original support, preserving the exact geometric hypotheses. Densities
converge uniformly and in L1, losses and peaks converge. On a closed upper
band edge use epsilon_n=min(epsilon,(max(g_n)-h)/C), positive eventually
and tending to epsilon. The coefficient in (6) is continuous there.
This retains (6) for arbitrary bounded laws with the same constants.

## 3. The polynomial estimate

Completion of a square gives

    W^2 <=20R^2+(5/2)ell,
    20R^2+(5/2)ell-W^2=(4R-sqrt(ell/2))^2.                (7)

Also log(2/tau)<=1/tau for 0<tau<=1: x-log(2x) is nondecreasing for
x>=1 and positive at one. Therefore

    W<=2(R+1)/sqrt(tau),
    exp(-W^2)/W >=exp(-20R^2) tau^3/[2^(7/2)(R+1)].        (8)

Combining (6) and (8) yields the real-parameter bound

    H(h/C) >=[pi C exp(-20R^2)/(2^(59/2)(R+1)^5 R^4)]
                                                    d tau^3 epsilon^8. (9)

Use pi C>1/8, e<4, 2^(59/2)<2^30, and
(R+1)^5 R^4<=2^5 R^9<=2^(5+9R) for integer R>=1.
The coefficient in (9) is at least A_R. Set tau=u and epsilon=m-u
for 0<u<m. Continuity includes the endpoints; above m both hinges vanish
by the reviewed comparison. Scaling restores variance s and proves (1).
Finally g(b)/C_s>=exp(-R^2/2)>=2^-R^2 proves the supplied peak choice.

## 4. Positive rational beta margins

With the existing normalization

    b_(N,k)=(N+1)binom(N,k) integral_0^1 u^k(1-u)^(N-k)H(u)du,

equation (2) gives, for every N>=0 and 0<=k<=N,

    b_(N,k)>=d A_R J_(N,k)(p),                            (10)
    J_(N,k)(p)=(N+1)binom(N,k) p^(k+12)
       *sum_(r=0)^(N-k) binom(N-k,r)(1-p)^(N-k-r)p^r
                            *(k+3)!(r+8)!/(k+r+12)!.      (11)

Substitute u=pt in the integral of u^(k+3)(1-u)^(N-k)(p-u)^8,
and expand (1-pt)^(N-k)=[(1-p)+p(1-t)]^(N-k). The remaining integral
is B(k+4,r+9), giving (11). Every summand is nonnegative. At p=1 only
r=N-k survives. Thus J>0, with exact rational values for rational p,
without alternating Gaussian replica sums. This supplies explicit margins
for all rows of an already signed class, not new unrestricted beta signs.

The accepted [loss cubature](../gaussian_prior_localization/LOSS_CUBATURE.md)
bounds same-row error by d B_(N,q)(R^2) in the present normalization.
Thus a reference row with margin (10) absorbs that specific error if

    B_(N,q)(R^2)<A_R min_(k in tested indices) J_(N,k)(p).  (12)

This degree budget is independent of d. The cubature must preserve the
moments and loss required by the cited theorem. The statement concerns
row errors; matching finitely many moments does not transfer anchors,
endpoint signs, or the full hinge curve. This is a conditional consumer,
not a new cubature theorem.

## 5. Middle-band degree improvement and the remaining join

On a band 2^-j<=u<=m-2^-k, with integers j,k>=0, (1) supplies margin
d*2^-B, where

    B=40R^2+9R+38+3j+8k.                                (13)

The previous supplied exponent was
2(2R+2^(j+1))^2+(2R+2^(j+1))+8R+8k+33.
Its dependence on j is exponential; (13) is linear.
For R=1,j=3,k=2 the exponent improves from723 to112.
The checker records larger j comparisons exactly.

For the old all-radius absolute beta-localization test, let L bound its
one-half modulus and d>=2^-ell_d>0. Its error E_N<=L(N+2)^(-1/4)
satisfies 2E_N<d*2^-B whenever

    N+2>(2L*2^(ell_d+B))^4.                              (14)

One may use L<=2[R^3/3+2R^2+4R+4]. With other parameters fixed, this
changes the supplied degree dependence to O(2^(12j+32k)), polynomial in
the reciprocal threshold separations. A loss floor is still needed here:
there is no new all-radius loss-proportional modulus.

If the actual source fits a radius-r ball with r^2/s<=1/2, the accepted
[loss-normalized modulus](../gaussian_loss_normalized_hinges/PROOF.md)
gives ||P_N-H||<=d K(N+2)^(-1/4). Its original polynomial sign test succeeds
at N+2>(2K*2^B)^4 independently of d. The actual radius controls K; the
anchor radius used in (1) remains a separate hypothesis. No automatic
recentring at means is used.

For K<=2^20, R=1,j=3,k=2, the safe compressed budget N+2=2^533
replaces2^2977. These remain enormous degrees; no practical enumeration
is claimed. The checker's compressed budgets do not construct them.
For completeness, the bound K<2^20 is valid whenever the actual
radius ratio epsilon=r^2/s<=1/4. In the cited modulus write
kappa=1-epsilon and c=4sqrt(2epsilon/kappa). Its factors satisfy

    kappa^-3<3, c<=10/3, 5epsilon+c^2/2<=245/36<7,
    (4+sqrt(2pi))/(16sqrt(pi))<1/4,
    (c+2)^2<=256/9, 4+c(c+2)<=196/9.

Using e<3 gives K<(1/4)*3*3^7*(256/9)*(196/9)=1016064<2^20.
The finite checker's half-scale fold has anchor radius at most3/8,
so this extra premise really holds there. It does not hold by that
radius guard for the unscaled calibration.
The earlier localization tests and their separate signed endpoints remain
the source of these implications; no new finite-test completeness theorem
is asserted.

For a different nonanchored input, low-threshold signs and a source-peak
upper bound remain separate obligations. A positive absolute error cannot
preserve the endpoint zeros in (1). No finite collection of nonnegative
beta tests by itself proves full majorisation. No proper-screw sign,
ambient stability extension, new KP limit, or improvement of7/50 follows.

## 6. Evidence boundary

The standard-library checker verifies finite rational geometric hypotheses,
ordered loss and variance scaling, square completion, two different exact
integrations for (11), degree schedules and damaged-record rejection.
The familiar coordinate fold is reused with attribution only as a control.
There is no numerical Gaussian integration, solver, or hidden certificate.

The spherical kernel, radial crossing, smoothing and diffuse-law passage
remain written mathematics. Finite controls are neither formalization nor
independent review of this argument or R8's strictness proof. See
[SOURCES.md](SOURCES.md) and [INPUTS.json](INPUTS.json) for exact dependencies.
