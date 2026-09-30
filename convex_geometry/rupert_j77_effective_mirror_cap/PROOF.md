# An effective complete mirror cap for J77

Author: **six-rupert-2**, role **researcher**, 2026-09-30.

Let K be the original unit-edge, 55-vertex paragyrate diminished
rhombicosidodecahedron, Johnson solid J77. Let s=sqrt(5),
e=(1,0,0), a5=(0,(1+s)/2,1), and let R be the actual proper body
rotation through 72 degrees about a5. Put

    E={+/-R^j e: j=0,...,4},  delta=dist(n,E),
    M_v=I-2vv^T/(v.v) for v!=0.

Here n is a physical unit receiving normal. P_n denotes orthogonal
projection onto n's perpendicular plane, and angle(Q) is the principal
full angle of an original spatial proper rotation.

**Theorem.** If delta<=10^(-23), Q is any original proper rotation,
lambda>=1, and t is any planar translation, then

    lambda P_n(QK)+t subset P_n(K)

holds if and only if lambda=1, t=0, and, for a nearest directed p in E,
there is an actual body rotation h in <R> such that

    Qh=I  or  Qh=M_n M_p.

Both cases give exactly equal shadows. In particular, no strict passage
has a receiving normal on this entire cap, with **all original source
orientations and translations** included. J77's global Rupert property
is **OPEN**. The much larger cap delta<=1/1000 is not excluded here.
The small printed cap results from deliberately conservative finite
error bounds; it is not an asserted sharp geometric threshold.

This is an author-checked, unformalized analytic proof with exact finite
hypotheses over Q(sqrt(5)). No independent review, formal verification,
historical priority, or floating-point proof is asserted.

## 1. Inputs and the actual unit mirror chart

The [complete full-angle reduction](../rupert_j77_area_axis_roll/PROOF.md),
source86dcf1e10d0eddbc26fc8343b6df4fcc642d47c6, includes every original
source orientation, full planar roll, scale and translation. On
0<delta<=1/1000 it gives an actual RIGHT body gauge with

    angle(Qh)<15delta.                                           (1)

At delta0 its full area parent classifies lambda1,t0,Q in <R>.
The checker replays every expected byte of this reduction, including
the full area prerequisite. No old diameter-region bisection is needed.

The [earlier qualitative mirror proof](../rupert_j77_uniform_local_exclusion/PROOF.md),
sourced23b45ee6e2d2704087e42b6a4faef698c53b14d, supplied seven incident
regions, persistent original contacts, tangent rays and coordinate-dual
bases. Its existential radii are **not** assigned numerical values here.
We reconstruct and check every finite fact used below in a new chart.
Its old critical corner u*=E0/20 satisfies

    R u*=-(5-s)e/10.

Each old parent corner v is transferred to -Rv/(-Rv)_x; all three
denominators are checked positive. Original indices are transferred by
the actual 55-vertex permutation of R. A contact (a,b,j) becomes
(R(b),R(a),R(j)): the edge is reversed along with the receiver ray.
The new vertices retain the original unit edge scale and ordering.
The old fixed-outer model.py and q5.py are byte-identical to the area
model's files; both loaded 55-vertex lists are also compared exactly.

The actual body reflection is M_e=diag(-1,1,1); its fixed vertices
are exactly22,23,24. The three radial exposure gaps satisfy

    v.(v-v_j)>=1/2  for every other original vertex v_j.          (2)

All162 comparisons are checked. Every vertex has norm less than
R0=9/4. Three independent antipodal core pairs certify 0 in int(K),
as replayed by the full-angle prerequisite.

Write a receiver near +e in the raw affine chart

    u=(1,y,z)=e+r_phys,   n=u/||u||.

The exact relation with its physical chord delta=||n-e|| is

    ||r_phys||/delta=sqrt(1-delta^2/4)/(1-delta^2/2)<1001/1000    (3)

for 0<delta<=10^(-9). In particular delta<=||r_phys||<2delta
and delta>||r_phys||/2. The square comparison in (3) is a rational
gate in the checker.

The transferred seven parents have corner e and outgoing rays d0,d1
normalized to ||d_k||_1=1, with d_k,x=0. Their actual other corners
are e+L_k d_k, with L_k>1/4. Their consecutive order is

    21,23,28,31,30,32,33.

Their eight successive boundary rays have positive adjacent determinants,
first and last are opposite, and all internal rays lie strictly in
a5.r<0. These exact tests give the whole closed half-plane a5.r<=0,
without a gap or a boundary omission. The two-ray cone of each parent
contains its points with coefficient sum Y<=1/4. In that cone write

    r_phys=gamma0 d0+gamma1 d1,  gamma_k>=0,  Y=gamma0+gamma1.

The inverse two-coordinate map gives Y=ell.r_phys with ||ell||_1<=2.
Consequently Y<4delta in (3). Conjugation by the actual reflection
M_e, with receiver representative -M_e n, sends r_phys to -r_phys,
preserves properness and full angle, and covers the other half-plane.
It also preserves the final classification. Thus the seven closed
strata cover an explicit full neighborhood, not just an unspecified
neighborhood from the qualitative proof.

## 2. Exact common rows, positive drift and duals

For each stratum the same32 persistent contacts are reconstructed on
the actual original vertices. If its edge is (v_a,v_b) and its source
preimage is v_i, put

    h_i=((v_b-v_a) cross e).v_i>0,
    m_i(u)=((v_b-v_a) cross u)/h_i,
    g_i(u)=v_i cross m_i(u).

The offset is the fixed **critical** offset. At all three transferred
parent corners the selected edge and v_i tie for support, and all55
original vertex inequalities hold. This is36,960 original support
comparisons. Linearity extends them throughout each closed parent.

At e exactly six rows have g_i parallel to e. The new compact fixture
supplies positive weights w_i with

    w_i>=1/20,  sum w_i=1,  sum w_i(g_i(e),m_i(e))=0             (4)

in all six coordinates. The weights were found by a private exact
linear-feasibility search; optimality is neither needed nor claimed.
The published checker simply verifies their feasibility and drift.
The common three-coordinate matrix in (alpha_x,b_y,b_z) has a
checked inverse with each row's l1 norm less than9. Its other two
columns vanish. This establishes exactly rank three.

The two independent tangent rays a0,a1 have x coordinate0 and l1
norm1. All32 first-order inequalities are nonpositive on both rays.
Two oriented facet rows have

    g_i(e).a_k<-1/16,  g_i(e).a_(1-k)=0,
    ||(g_i,x(e),m_i,y(e),m_i,z(e))||_1<1.                        (5)

The inverse tangent-coordinate map has row l1 norms less than4.
The following bounds are all checked on the actual coefficients:

    ||m_i(e)||_1<1,
    ||m_i(d_k)||_1<3/2,  ||g_i(d_k)||_1<4;
    ||g_i(d_k)||_1<3 on each of the six common rows.

Define the common weighted derivatives G_k=sum w_i g_i(d_k) and
N_k=sum w_i m_i(d_k). Then ||G_k||_1<3, ||N_k||_1<2 and all28
drift corners satisfy

    1/100<a_j.G_k<3.                                            (6)

For tau in the **whole closed interval** [0,1], set
a(tau)=tau a0+(1-tau)a1. The degree-two Bernstein coefficients of
||a(tau)||^2 are greater than1/4, so ||a(tau)||>1/2. Also ||a||<=1.

The checker regenerates102 polynomial rows A(tau)X<=B(tau), described
in section4. Exactly41 are universally tight on the mirror point

    X_m=(r_m,0,0,0),  r_m,0 d0+r_m,1 d1=-e cross a(tau).        (7)

For each receiver coordinate k=0,1 and sign sigma=+/-1, a checked
nonnegative dual supported on these tight rows satisfies

    sum mu_i A_i=sigma unit_k,
    sum mu_i B_i=sigma r_m,k,  sum mu_i<100.                    (8)

Every Cramer identity is checked in all five unknown coordinates;
its determinant is independently replayed at three points. Strictly
positive denominator and nonnegative numerator Bernstein coefficients
prove (8) on the entire interval, including both endpoints. Polynomial
conversion is independently reconstructed in the power basis. No
limiting inequality is applied to a finite motion without a remainder.

## 3. An explicit closed-containment receiver rate

We first prove a reusable rate. Suppose

    0<delta<=10^(-9), Q!=I, angle(Q)<=18delta,
    P_n(QK)+t subset P_n(K).                                    (9)

The receiver may be folded as in section1. Let the actual Cayley vector
be w=eta alpha, eta=tan(angle(Q)/2)>0, ||alpha||=1.
The elementary sin x<=x, cos x>=1-x^2/2 bounds give eta<10delta.
Support in the physical translation's unit direction gives

    ||t||<=R0||Q-I||<=2R0 eta.

Lift it to T=(0,t_y-y t_x,t_z-z t_x), so P_u T=t and
||T||<=||u|| ||t||. Put b=T/(2eta); thus ||b||<3.
Every persistent contact gives the exact necessary inequality

    g_i(u).alpha+(1+eta^2)m_i(u).b
       +eta[(alpha.v_i)(alpha.m_i(u))-m_i(u).v_i]<=0.            (10)

Subtract its critical linear row. For Y,eta<=1/100, the absolute
nonlinear/receiver error is at most

    B0=9Y+5eta.                                                 (11)

Indeed the torque drift costs at most4Y, normal drift at most(9/2)Y,
and the remaining terms at most
eta(9/2+3eta)(1+2Y)<5eta. The common-row bound is no larger.

The positive balance (4) bounds every common critical row in absolute
value by20B0. The rank inverse therefore gives, with s0=Y+eta,

    Z=max(|alpha_x|,|b_y|,|b_z|)<180B0<=1620s0.                (12)

Write exactly alpha_t=xi0 a0+xi1 a1. From (5),(10),(11),(12),

    xi_k>=-26100s0.

Let p=xi0^++xi1^+. Unit alpha and ||a_j||<=1 give
p>=1-53820s0>9/10, since s0<14delta<=14*10^(-9).
For each receiving direction, the coefficient in the weighted left
side of (10) is bounded below by

    alpha.G_k+(1+eta^2)b.N_k
      >9/1000-168000s0>1/200.                                  (13)

Here the possible negative xi coefficients cost at most156600s0,
the normal rotation component at most4860s0, and the translation
at most6480s0. All these estimates retain arbitrary translation.
The weighted last term in (10) has absolute value less than5eta.
It follows that

    delta<=||r_phys||<=Y<=1000eta.                               (14)

This is an explicit rate for **nonidentity closed** containments, not
a strict-containment limit argument. Combining (11),(12),(14) gives

    |alpha_x|,|b_y|,|b_z|<2*10^6 eta,
    xi_k^-<27*10^6 eta.                                        (15)

The numerical absorptions in (11)--(15) are rational checker gates.
Identity is deliberately excluded from (9); it need not satisfy a
receiver-to-angle bound.

## 4. Finite-scale forms of the coordinate system

Now assume the cap in the theorem and apply (1). If Qh=I we already
have an equality shadow. Otherwise suppress its actual right gauge
and receiver fold in the notation and apply (14),(15). Define

    p=xi0^++xi1^+, epsilon=eta p,
    tau=xi0^+/p in [0,1], a=a(tau).

The inverse tangent map gives p<8. Hence

    eta/2<=epsilon<=8eta<=80delta<=8*10^(-22).

There are **exact**, finite variables with

    w=epsilon a+epsilon^2 k,
    k=z e+d, d.e=0,
    u=e+epsilon r, r=r0 d0+r1 d1, r0,r1>=0,
    T=2epsilon^2 c, c=(0,c_y,c_z).

By (14),(15) and epsilon>=eta/2 they satisfy

    r0+r1<=2000, ||r||<=2000,
    |z|<8*10^6, ||d||<216*10^6, ||k||<L=4*10^8,
    ||c||<C0=2*10^7.                                          (16)

The small tangent correction d accounts for clipping negative xi
coefficients. It is not dropped or silently identified with zero.
Let X=(r0,r1,z,c_y,c_z). For every one of the102 rows regenerated
by the checker we prove the actual finite necessary inequality

    A_i(tau)X<=B_i(tau)+H epsilon,  H=10^13.                    (17)

Here is the full row construction and error estimate. Put Arot=w/epsilon;
||Arot||<=2. The exact Cayley formula is

    Qv-v=2[w cross v+w cross(w cross v)]/(1+||w||^2).            (18)

For every persistent edge include **all** original vertices v tying
its critical support, and let v_out be its endpoint. With
m(u)=m0+epsilon m_r, its necessary inequality divided by epsilon
has leading terms

    m_r.(v-v_out)<=-2 a.(v cross m0).                           (19)

We have ||m0||<1, ||m_r||<=3000, ||m(u)||<2, and

    ||Qv-v-2epsilon a cross v||<=2*10^9 epsilon^2.

The last bound follows from (18), (16), ||v||<9/4 and
epsilon<=10^(-12). After dividing by epsilon the error in (19)
is at most

    [4*10^9+2(9/4)3000+4C0]epsilon < H epsilon.                (20)

For each of the six common persistent contacts v, multiply its
necessary inequality by (1+||w||^2)/(2epsilon^2). Its leading row is

    a.(v cross m_r)+z g_x(e)+m0.c
                    <=||a||^2-(a.v)(a.m0).                    (21)

The tangent correction d disappears from g(e).k **exactly**, since
g(e) is parallel to e. It remains in higher-order errors. Expanding
(18) bounds the residual in (21) by

    [R0*3000L+3R0 L+4R0*3000+4C0+2*3000C0]epsilon
                                                      <H epsilon. (22)

For each actual fixed mirror vertex v use the physical perpendicular
probe m_v(u)=v-u(u.v)/||u||^2. It continues exposing v: from (2)
and (16), ||m_v(u)-v||<=R0*2000epsilon, and its change in any
support comparison is at most2R0^2*2000epsilon<1/2.
Its exact necessary inequality, multiplied by the same positive factor,
has leading row

    -(v.r) a.(v cross e)+v.c
                     <=||a||^2||v||^2-(a.v)^2.                (23)

For clarity, the exact first rotation term in this normalized inequality is

    -(r.v)[(e+epsilon r).(a cross v)
                   +epsilon(e+epsilon r).(k cross v)]
                                     /(1+epsilon^2||r||^2).

Its departure from the leading term in (23), together with the quadratic
rotation and translation departures, is at most epsilon times

    (R0*2000)[R0*2000+R0 L+epsilon R0*2000L]
    +(R0*2000)R0*2000^2 epsilon+3R0^2 L
    +(R0*2000)4R0+4R0 C0 epsilon+2(R0*2000)C0 < H.             (24)

This is evaluated at the upper epsilon=8*10^(-22) for the monotone
terms. Finally include -r0<=0,-r1<=0. Equations (19),(21),(23)
and these two cone constraints are precisely the102 polynomial rows.
All finite remainder bounds (20),(22),(24) are strictly positive
rational margin checks. No little-o assumption is used.

Apply each nonnegative dual (8) to (17). It gives both signs of

    |r_k-r_m,k|<=100H epsilon=10^15 epsilon, k=0,1.

Using ||d_k||<=1 and (7),

    ||r_phys+epsilon e cross a||<=2*10^15 epsilon^2.            (25)

Since ||a||>1/2, (25) and epsilon<=8*10^(-22) give
||r_phys||>epsilon/4, and (3) gives

    delta>epsilon/8.                                          (26)

## 5. Effective reflection bootstrap and full classification

The exact equal-shadow proper rotation Q0=M_n M_e has Cayley vector

    w0=e cross u/(e.u)=e cross r_phys.

From (16),(25),

    ||w-w0||<3*10^15 epsilon^2.                                (27)

Let Qtilde=M_n Q M_e. Because M_e K=K and P_n M_n=P_n,

    P_n(Qtilde K)=P_n(QK).

It is an actual proper rotation with the **same** translated closed
containment. For real skew W=[w]_cross, the Cayley representation is
Q(w)=2(I-W)^(-1)-I. The inverses have operator norm<=1, so
||Q(w)-Q(w0)||<=2||w-w0||. Orthogonal multiplication gives
||Qtilde-I||=||Q-Q0||. Since (27) is less than1/2,
sin(angle(Qtilde)/2)<=||w-w0|| and arcsin x<=2x give

    angle(Qtilde)<2*10^16 epsilon^2.                            (28)

Independently, the rotation-angle triangle inequality and (3) give

    angle(Qtilde)<=angle(Q)+2angle(n,e)<18delta.

Indeed angle(n,e)=2arcsin(delta/2)<(1001/1000)delta on the
larger1/1000 cap. Therefore, if Qtilde!=I, the explicit closed rate
(14) applies to Qtilde at the same receiver. Its Cayley norm is at
most its full angle on this small cap. By (26),(28),

    epsilon/8<delta<=1000 angle(Qtilde)<2*10^19 epsilon^2.

This would require 16*10^19 epsilon>1, whereas
epsilon<=80*10^(-23) gives 16*10^19 epsilon<=0.128<1.
This strictly positive final absorption is checked exactly. Hence
Qtilde=I, and Q=M_n M_e. Together with the earlier identity case,
these are the only unit-scale motions after the actual gauge and fold.

For either motion its shadow equals the receiver shadow. A bounded
convex set C satisfying C+t subset C has t=0, by support in t's
direction. To handle original lambda>=1, shrink the original closed
containment by1/lambda about0 in P_nK. It gives a unit-scale containment
with translation t/lambda. The classification therefore gives t=0 and
equal shadows at unit scale. Positive projection area then forces
lambda=1. Conversely the two stated rotations with lambda1,t0 give
equal shadows exactly.

A proper receiver body frame carries the nearest p=+/-R^j e to
+/-e. Conjugating the above conclusion back yields M_n M_p and
the same actual RIGHT body gauges. Reflection signs do not change M_p.
The separately replayed delta0 parent handles the exact axes.
This proves the stated all-source closed classification and strict exclusion.

## 6. Reproducibility and limitations

Run from the repository root, Python3.11+ standard library:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
      timeout 55s python3 -B convex_geometry/rupert_j77_effective_mirror_cap/verify.py --self-test

The same command with `python3 -B -O` is also required to match every
expected byte. All mathematical validation uses explicit exceptions.
Each recorded Q(sqrt(5)) sign is independently checked by rational
sqrt(5) enclosures; determinant and Bernstein conversion identities
have separate replays. Nine malformed fixtures exercise missing/duplicate
strata, a larger unproved cap, negative weight, missing sign, duplicate
row, invalid determinant coordinate, invalid sign and wrong author role.
At each stratum's parameter midpoint,385 direct original-vertex identities
compare the Cayley rotation with the matrix reflection product, and714
direct finite normalized row evaluations check the remainder convention.
These samples validate the encoding; the continuous error bounds are
proved by (20),(22),(24), not inferred from the samples.

The checker byte-pins15 direct parent files and34 transitive files,
replays the full roll/area expected output, reconstructs the44-parent
partition and checks the entire explicit seven-stratum fan, and verifies
all new support/rank/drift/dual/remainder gates. It does not rerun the
old global fixed-receiver bisection or use its existential angle as a
numeric premise. The polynomial/continuous bridges in this text remain
unformalized; exact arithmetic alone is not claimed to verify them.

The final gate with the same coarse estimates fails at delta=10^(-22):
its upper product is1.28. This is a failure of these bounds, not a
passage witness. Likewise no whole1/1000-cap result is asserted.
Sharper finite errors, or direct support certificates farther from the
mirror axis, are needed for a useful expansion of the receiving domain.

Standard strict projection equivalence and current named-solid status
are external literature, not new results:
[projection framework](https://arxiv.org/abs/2112.13754),
[algorithmic status table](https://arxiv.org/html/2509.08190),
[Nopert](https://arxiv.org/abs/2508.18475),
[unresolved-solid seed](https://arxiv.org/html/2604.26531).
These primary sources were refreshed in this pass; no J77 resolution
was located. This is a bounded status check, not an exhaustive priority claim.
