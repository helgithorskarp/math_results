# A bilinear mirror obstruction and a larger complete cap for J77

Author: **six-rupert-2**, role **researcher**, 2026-09-30.

Let K be the original unit-edge, 55-vertex paragyrate diminished
rhombicosidodecahedron, Johnson solid J77. Write s=sqrt(5), e=(1,0,0),
a5=(0,(1+s)/2,1), and R for the actual proper body rotation through
72 degrees about a5. Define

    E={+/-R^j e: j=0,...,4},  delta=dist(n,E),
    M_v=I-2vv^T/(v.v),  P_v=I-vv^T/(v.v).

Here n is a physical unit receiving normal. Distances and rotation
angles are physical Euclidean chords and principal full spatial angles,
with angles in radians.

**Theorem.** Suppose delta<=1/100000, Q is any original proper rotation,
lambda>=1, and t is any translation in n's perpendicular plane. Then

    lambda P_n(QK)+t subset P_n(K)

holds if and only if lambda=1, t=0, and, for a nearest directed p in E,
there is an actual RIGHT body rotation h in <R> such that

    Qh=I  or  Qh=M_n M_p.

These are exactly equal shadows. Therefore strict passage is excluded
on the entire stated receiving cap, with **all original source
orientations, planar rolls and translations** included.

J77's global Rupert property is **OPEN**. The larger receiving cap
delta<=1/1000 is also not excluded here. The new radius is 10^18 times
the radius in the [previous effective cap](../rupert_j77_effective_mirror_cap/PROOF.md).
The mechanism is a new exact common-contact bilinear identity involving
the actual motion and its reflected companion. The previous second-order
rescaling, radial probes and limiting coordinate duals are not used in
this continuous argument.

This is an author-checked, unformalized analytic proof with exact finite
hypotheses and universal polynomial identities over Q(sqrt(5)). No
independent review, historical priority or proof-assistant verification
is asserted. The finite checker and the written continuous estimates
are distinct parts of the evidence.

## 1. Original sources, chart coverage and inputs

The [full-angle reduction](../rupert_j77_area_axis_roll/PROOF.md),
source86dcf1e10d0eddbc26fc8343b6df4fcc642d47c6, treats every original
source orientation. If 0<delta<=1/1000, it supplies an actual RIGHT
body gauge with

    angle(Qh)<15delta.                                           (1)

At delta0 its area prerequisite classifies lambda1,t0,Q in <R>.
The [finite-input parent](../rupert_j77_effective_mirror_cap/PROOF.md),
sourceedef7ccfb5e2b89d9a781aa70ff178d70521490b, reconstructs and
checks the following facts in the original vertex model. The new
checker pins all seven parent files and replays **every expected output
byte** of its checker, including the full-angle and area prerequisites.
Its tiny-radius conclusion and receiver-rate estimates are not needed
in this proof. No existential radius is assigned a new numerical value.

By an actual body rotation and a choice of sign for the receiving
representative, put the nearest directed axis at +e. The body reflection
M_e=diag(-1,1,1) permutes the original vertices. Use

    u=e+r=(1,y,z),  n=u/||u||,  r=(0,y,z),  w0=e cross r.

With delta=||n-e|| and c_r=1001/1000,

    delta<=||r||<c_r delta.                                      (2)

Indeed ||r||/delta=sqrt(1-delta^2/4)/(1-delta^2/2). The stronger
rational gate c_r(1-d^2/2)>1, d=1/100000, proves (2) throughout
the stated cap.

There are seven transferred closed receiving triangles, with parents
21,23,28,30,31,32,33. Their two outgoing rays d0,d1 have x coordinate0,
l1 norm1 and actual corner lengths greater than1/4. Their fan order
21,23,28,31,30,32,33 covers the entire half-plane a5.r<=0, including
all boundary rays. In each cone,

    r=gamma0 d0+gamma1 d1, gamma_k>=0, Y=gamma0+gamma1<4delta.

This follows from the checked coefficient-sum functional having l1 norm
at most2 and (2). Since Y<1/4, the point lies in the actual closed
parent triangle. Conjugating Q by M_e and replacing the receiving
representative by -M_e n changes r to -r, preserves properness and the
full angle, and covers the other half-plane. It also preserves both
motions in the stated classification. Thus no open-wall assumption is
made. The original 55 vertices are used throughout; every vertex has
norm less than R0=9/4, and 0 is in int(K).

For each parent, 32 persistent original contacts have an edge (v_a,v_b)
and a source preimage v_i. Write

    h_i=((v_b-v_a) cross e).v_i>0,
    m_i(u)=((v_b-v_a) cross u)/h_i,  g_i(u)=v_i cross m_i(u).

The denominator is fixed at e. At all three parent corners m_i(u)
is perpendicular to u, exposes the selected edge, and also exposes
v_i. All 55 vertices satisfy its support inequality. The parent checks
36,960 support comparisons; linearity extends them over each closed
triangle. In particular, m_i(e).v_i=1. The exact derivative bounds are

    ||m_i(e)||_1<1,
    ||m_i(d_k)||_1<3/2,  ||g_i(d_k)||_1<4,
    ||g_i(d_k)||_1<3 on the six common rows.                      (3)

The common rows are exactly those for which g_i(e) is parallel to e.
Their source preimages have x coordinate0. The replayed positive
weights omega_i satisfy

    omega_i>=1/20, sum omega_i=1,
    sum omega_i g_i(e)=sum omega_i m_i(e)=0.                      (4)

The two critical tangent motion rays a0,a1 have x coordinate0 and
l1 norm1. Every critical contact inequality is nonpositive on them.
Their oriented facets f_k satisfy

    g_(f_k)(e).a_k<0,  g_(f_k)(e).a_(1-k)=0.

The degree-two Bernstein coefficients certify

    ||tau a0+(1-tau)a1||>1/2 for the whole closed tau in[0,1].   (5)

All these finite facts are rechecked in the parent. The new fixture
freezes only small dual basis indices and bounds, and the same positive
common weights. The duals below are verified directly, not inferred
from a solver's optimality or from a numerical fit.

## 2. Reflection and a universal common-contact identity

After the right gauge in (1), abbreviate Qh by Q. Put

    Qtilde=M_u Q M_e,  Q0=M_u M_e.

These are proper rotations, and

    P_u(Qtilde K)=P_u(QK),  P_u(Q0 K)=P_u(K).                    (6)

They use the same receiving plane and the same physical translation.
The principal angle of Q0 is twice the angle from n to e. For
delta<=1/1000, arcsin( delta/2 )<=c_r delta/2, as certified by the
rational derivative gate in the checker. Hence

    angle(Qtilde)<(15+2c_r)delta<18delta.

Both Q and Qtilde have Cayley norms eta,etatilde less than10delta:
tan(9delta)<=9delta/(1-81delta^2/2)<10delta. All denominators below
are positive.

Lift the planar translation t to T=t-t_x u, so T_x=0 and P_u T=t.
If w is Q's Cayley vector, define

    w=(rho,p), p=(w_y,w_z), eta=||w||,
    C=(1+eta^2)T/2, C_x=0,
    D=1+w0.p,  1-10c_r delta^2<=D<=1+10c_r delta^2.

Vectors r and w0 are identified with their two tangent coordinates
where needed. The proper product of the Cayley rotation w0 and the
reflection-conjugated rotation (rho,-p) gives the exact map

    rhotilde=(rho+r.p)/D,
    ptilde=(w0-p+rho r)/D.                                     (7)

The checker verifies, as polynomial identities in independent variables,

    D^2+||(rho+r.p,w0-p+rho r)||^2
       =(1+||r||^2)(1+||w||^2),
    rho=D(rhotilde+r.ptilde)/(1+||r||^2),

and the involution obtained by applying (7) twice. The Cayley product
formula establishes its correspondence with the actual Qtilde in (6).

For each common contact put k_i=(v_b-v_a)_x/h_i, and let

    S=sum omega_i (v_i)_t (m_i(e))_t^T,
    A=I_2-S,  B=sum omega_i k_i v_i,  Kc=sum omega_i k_i.

The trace of S is1. Its symmetry follows from the e coordinate of
the torque balance (4). Thus J S=A J, where J is the tangent quarter
turn J(y,z)=(-z,y). Directly from the cross product,

    m_i(u)=m_i(e)-e(m_i(e).r)+k_i w0.

For a unit translated closed containment, each contact gives the exact
necessary Cayley inequality

    F_i=m_i(u).(w cross v_i+w cross(w cross v_i)+C)<=0.          (8)

This is just its original support inequality multiplied by
(1+eta^2)/2>0. Let F=sum omega_i F_i. For tangent vectors write
[a,b]=a_y b_z-a_z b_y. Then the following identity is exact:

    F = D{p^T A ptilde-[p,ptilde][p,B]}
        +rho{B.r-p.r+[p,r][p,B]}
        -rho^2(1+w0.B)+Kc w0.C.                               (9)

For clarity, before using (7) the weighted expansion is

    p^T A(w0-p)+rho B.r-rho p^T S r-rho^2(1+w0.B)
       +(p.B)(w0.p)-||p||^2(w0.B)+Kc w0.C.

Use A+S=I and
(p.B)(w0.p)-||p||^2(w0.B)=-[p,w0][p,B] to obtain (9).
For each of the seven parents, the checker also expands the left side
from the actual original edges and vertices and compares every
coefficient with (9), clearing ptilde's D denominator. These are seven
universal identities in (r_y,r_z,w_x,w_y,w_z,C_y,C_z), each with
22 nonzero monomials and total degree3. This is not a sample-point check.

The four numbers b_jk=a_j^T A a_k are strictly positive in every
parent, including both endpoints. Their actual minimum in parents30/31
is about0.0107568; decimal values here are explanatory only. Exact
Q(sqrt5) values and positive rational sign enclosures are in the output.

## 3. Direct normal and translation bounds from common contacts

Set L_i=g_i(e).w+m_i(e).C. By (3), Y<4delta and eta<10delta,

    |F_i-L_i|<=39delta eta+6delta||C||,
    |F_i-L_i|<=35delta eta+6delta||C|| on common rows.           (10)

Indeed the torque drift costs at most4Y eta, or3Y eta on common
rows; the translation drift costs at most(3/2)Y||C||. The quadratic
cross product costs at most

    R0(1+(3/2)Y)eta^2 <(23/10)eta^2<=23delta eta.

The rational gate R0(1+6d)<23/10 proves this throughout delta<=d.
No preliminary bound on t or C is assumed.

On common rows L_i has only coordinates (rho,C_y,C_z), and their
weighted sum is0. The fixture supplies nonnegative representations of
both signs of each coordinate as a combination of these six rows.
The checker solves the frozen three-row basis, adds a nonnegative
multiple of the balance (4) to make all coefficients nonnegative,
and checks the full identity. The coefficient sums are strictly below

    mu_C=807/100 for each C coordinate,
    mu_rho=374/100 for rho.                                    (11)

Since each L_i<=35delta eta+6delta||C||, (11) gives

    ||C||<(3/2)mu_C(35delta eta+6delta||C||).

The exact gates 1-9mu_C d>0 and
424(1-9mu_C d)>(3/2)mu_C35 therefore give

    ||C||<424delta eta,  |rho|<131delta eta.                    (12)

Apply the same common-contact argument to Qtilde, whose projection
and physical t agree by (6). Its translation variable is
Ctilde=(1+etatilde^2)T/2. Since both Cayley norms are less than10delta,
(7) and the positive rational gates give the stronger simultaneous bounds

    ||C||<425delta min(eta,etatilde),
    |rho|<133delta min(eta,etatilde).                           (13)

For C use ||C||/||Ctilde||=(1+eta^2)/(1+etatilde^2)<=1+100d^2
(or handle T=0 directly). For rho, its own bound is in (12); its
inverse formula in (7) bounds it by
(1+10c_r d^2)(131+c_r)delta etatilde<133delta etatilde.

There is also a useful receiver-to-motion comparison with c_l=2001/1000:

    delta<=||r||<c_l max(eta,etatilde).                         (14)

From w0=p+Dptilde-rho r and |rho|<=eta<10delta,
||r||(1-10delta)<=(2+10c_r delta^2)max(eta,etatilde).
The printed rational gate c_l(1-10d)>2+10c_r d^2 proves (14).

## 4. Keep both critical cones, including clipped coordinates

Write p=xi0 a0+xi1 a1. For each k a nonnegative combination of the
two-ray facet f_k and the six common critical rows is exactly -xi_k,
including cancellation of all three normal/translation coordinates.
The checker verifies the identity in all five coordinates
(rho,xi0,xi1,C_y,C_z). From (10) and (12), it proves

    xi_k^-:=max(0,-xi_k)<=H_k delta eta.                        (15)

The printed constants, in the original ray ordering, are

| Parent | H0 | H1 |
|---|---:|---:|
| 21 | 254 | 1726 |
| 23 | 1660 | 1799 |
| 28 | 1033 | 2170 |
| 30 | 433 | 836 |
| 31 | 433 | 836 |
| 32 | 2460 | 507 |
| 33 | 179 | 1780 |

Explicitly, if the positive common coefficient sum is c and the facet
coefficient is f, the exact checked bound is

    H_k >35c+39f+6*425*d*(c+f).

The same H_k apply to ptilde, with eta replaced by etatilde. This
uses the same closed parent, not a different cone or a limit direction.
Let N=H0+H1, xi_k^+=max(0,xi_k), and P=xi0^++xi1^+.
The negative part of p has norm at most Ndelta eta. By (13),
||p||>=eta-|rho|. Together with (5) and ||a_k||<=1, this gives

    (1-(133+N)delta)eta<=P<=2(1+Ndelta)eta,                    (16)

with positive left coefficient throughout the cap. The corresponding
bounds hold for Ptilde. Thus the negative coefficients are retained
and bounded; they are not silently set to zero.

Put beta=min b_jk>0 and W=sum_j H_j max_k b_jk. Since every b_jk
is positive and b_jk=b_kj, expanding both clipped coordinate vectors
and dropping only the nonnegative product of their negative parts yields

    p^T A ptilde >= L eta etatilde,
    L=beta(1-(133+N)d)^2-4(1+Nd)Wd>0.                          (17)

The mixed terms are at most Wdelta eta Ptilde and Wdelta etatilde P.
Use (16) and delta<=d. The checker verifies L>0 separately for
every closed parent. Positive-corner tests alone would not establish
(17) without the retained negative-part bounds.

## 5. Finite bilinear contradiction and equality classification

Suppose Q is neither I nor Q0. Then eta>0 and etatilde>0 by the
involution (7). Let B1=||B||_1, K1=|Kc|, D_+=1+10c_r d^2,
D_-=1-10c_r d^2. Bounds (13), (14), eta<10delta and the elementary
|[a,b]|<=||a||||b|| give the following rigorous lower bound for (9):

    F >= (D_- L - E_err) eta etatilde,

    E_err = D_+ 10d B1
            +133 c_r c_l B1 d
            +133 c_r d^2
            +133 c_r B1 10d^3
            +133^2 d^2(1+c_r B1 d)
            +425 c_r c_l K1 d.                                (18)

The six terms respectively bound:

1. D[p,ptilde][p,B], using ||p||<=eta<=10delta;
2. rho B.r, using delta min(eta,etatilde)<=c_l eta etatilde;
3. rho p.r, using eta min(eta,etatilde)<=eta etatilde;
4. rho[p,r][p,B], using eta^2 min(eta,etatilde)<=10delta eta etatilde;
5. rho^2(1+w0.B), using min(eta,etatilde)^2<=eta etatilde;
6. Kc w0.C, using (13) and (14).

All are absolute-value estimates, so no sign of rho or translation is
assumed. The final exact gates D_- L-E_err>0 hold in all seven
parents. The smallest gap is in parents30/31, about0.00079004.
These decimal displays are diagnostics; the checked exact field signs
and independent rational sqrt5 enclosures prove the strict gates.

Thus F>0, contradicting (8) and the positive weights (4). Therefore
Q=I or Q=Q0. By (6) both motions have exactly the receiving shadow.
A compact convex set of positive area cannot contain a nonzero
translate of itself: take support in the translation's direction.
This proves t=0 for unit closed containment.

Finally 0 in int(K) and convexity imply QK subset lambda QK for
lambda>=1. An arbitrary scaled closed containment therefore implies
unit closed containment with the same Q and t, to which the argument
applies. Once t0 and equal unit shadows are known, positive projected
area forces lambda=1. At delta0 the full-angle parent's exact
classification supplies the same result. Undo the actual right gauge,
body-coordinate rotation and reflection fold to obtain the theorem
as stated. Conversely the two displayed motions give equal shadows
directly, so the asserted equivalence holds.

## 6. Evidence boundary and remaining frontier

The new checker verifies42 positive common-coordinate duals,14 full
five-coordinate cone combinations,28 positive bilinear corners,
seven universal original-contact identities, three universal reflected
Cayley identities, all new rational gates, and every complete finite
parent output byte. It also independently audits all collected
Q(sqrt5) signs using rational enclosures for the positive sqrt5.
The fixture contains feasible combinations; no optimality is claimed.
The continuous support, norm, angle, clipping and scale bridges are
the written proof above, not a formal proof-assistant certificate.

The candidate1/90000 fails these conservative final stress gates in
parents30/31. This is a bound failure, not a passage and not a
nonexistence theorem. No claim is made outside the printed cap.
The next frontier is the remaining band from1/100000 to1/1000,
followed by receiving directions beyond the full-angle parent's cap.
The weak cross-corners in parents30/31 and their facet-error costs
are concrete targets for sharper exact stress combinations.

The current primary [status table](https://arxiv.org/html/2509.08190)
lists J72,J73,J74,J75,J77 as unresolved. The current
[Rupert literature](https://arxiv.org/html/2604.26531) reports87 of92
Johnson solids as Rupert and treats the rhombicosidodecahedron's
non-Rupert status as conjectural. The
[Nopert construction](https://arxiv.org/abs/2508.18475) concerns a
different body. The [projection criterion](https://arxiv.org/abs/2112.13754)
provides the standard fixed-hole Rupert formulation. These are bounded
literature checks, not an exhaustive priority or absence claim.

Related current team context includes
[deltoidal sharp source budgets](../../geometry/rupert_deltoidal_symmetry/source_extrema_proof.md)
and the [three-quarter deltoidal wedge](../../geometry/rupert_deltoidal_symmetry/rank_transport_wedge_proof.md),
which also retains a necessary full-angle reduction on the whole
prospective wedge. The new
[coupled rhombicosidodecahedron proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/COUPLED_NONWINNING_PROOF.md)
combines with its [winning-band exclusion](../../rhombicosidodecahedron_mirror_cluster_obstruction/WIDER_WINNING_BAND_PROOF.md)
to force squared axial height below beta-1/150 for every strict
passage. Both global named-solid problems remain open. Their different
bodies, central-symmetry arguments and numerical constants are not
transferred to J77.
