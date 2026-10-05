# Exact upper repair endpoint, unchanged FIRST sector and large-cube caps

Actual author **six-downset-1 / researcher**, 2026-10-05. Ordinary
author-complete argument, **UNFORMALIZED and independently UNREVIEWED**.
This source release preserves the private mathematical proof. Fresh
source-only, adverse-input and isolated-reader observations are recorded
in VALIDATION.json. Creation-time evidence fields with null source/graph
references remain historical; they do not assert graph commitment.
No large original matrix has been constructed.

The sole target is Spectral Chvatal Conjecture H, Ellis--Filmus--Friedgut,
Section4, https://arxiv.org/html/2609.28404v1#S4. The primary v1/history and actual Section4 were live reverified on
2026-10-05: the displayed history still contains only v1,2026-09-23.
No global H/I or historical priority conclusion is claimed here.

The construction, original support/span/decomposition, all-count
scalar bounds and exact LOWER repair interval are credited to
[the complete source-first predecessor proof](https://github.com/helgithorskarp/math_results/blob/b7d26214d61e1aba86367ce2162ccf2a4e1aa749/round-two/six-downset-1/unique-heavy-triangle-cap/PROOF.md)
and its [scalar proof](https://github.com/helgithorskarp/math_results/blob/b7d26214d61e1aba86367ce2162ccf2a4e1aa749/round-two/six-downset-1/unique-heavy-triangle-cap/SCALAR-BOUNDS.md).
That source is ordinary/unformalized and independently unreviewed;
its graph packet is unsigned/unsubmitted. Existing two/three-mark
reviews do not review this new result. Standard rank-one/rank-two
inverse identities are tools, not themselves novelty claims. The new
content is the complete original count reduction, boundary ordering,
FIRST invariance, growing repair interval and sharp cap asymptotics.

## Family and exact scalar definitions

Use integers r>=3,n>=max(4,r),h>k_g>=2 for g=1,...,r-1 and
F=h+sum_light k_g>=9. The downset consists of the full old n-cube
and h triangles at its heavy mark, k_g at each distinct light mark,
with all private pairs disjoint outside the cube. Retain ACTUAL empty.
Set k0=h and

    q=2^(n-1), L=sum_light k_g, F=h+L,
    m=3F, ell=m+1, s=q+3h, N=2q+6F, P=I-J/N.

The predecessor's functions are

    c0=[q ell+9sum_light k_g(h-k_g)+3h-6F-1]/ell^2,
    R_g=[ell+1-q-3(h-k_g)]/ell,
    mu_g=(s-3)/3-c0-9R_g^2/[2s(k_g-1)],
    beta_g=2s/3-3(k_g+3)R_g^2/[s(k_g-1)],
    c_g=9R_g/(2s), S=sum_groups k_gmu_g,
    S_L=sum_light k_gmu_g,
    kappa=1/(hmu_0)+1/S_L
          +4sum_light k_gmu_g^2/(S_L^2 beta_g).

All these denominators are positive. In particular mu_g>s/5,
mu_g<s/3, beta_g>s/2, L>=4, s>=17. The original seed is
L0=J+Q, where Q is the Gram of the COMPLETE centered row system U,
including empty, and Q1=0. Its positive physical frame is U' U,
dimension N-3. The original supported stochastic line has

    L_delta=L0+delta(AB'+BA'),
    M_delta=(L_delta-sI)/(N-s),
    A=(-3,a), B=(-1,b),
    a=1/h on each heavy PRIVATE row, zero elsewhere,
    b=mu_g/S_L on each light PRIVATE FULL row, zero elsewhere.

Both vectors have zero sum, their proper supports are disjoint, and

    A.B=3, A^2=9+3/h,
    B^2=1+W_L/S_L^2,  W_L=sum_light k_gmu_g^2.

Support and row sums hold for every real delta. Rational delta gives
a rational matrix. The already-proved lower PSD interval is exactly
[0,6/kappa], with lower ranks N-2 at its endpoints and N-1 inside.

For the new upper endpoint define the following count scalars:

    d_g=N-3mu_g,
    T=sum_groups k_gmu_g^2/d_g,
    T_L=sum_light k_gmu_g^2/d_g,
    Z=S/3+T,
    H_g=N^2-N[s(1+c_g^2)+3beta_g/2]+3s beta_g/2,
    E_g=k_g[beta_g(N-s)+(2N/3)c_g^2s]/H_g,

    Abar=9+3N/(h d_0)-3Nmu_0^2/(d_0^2 Z),
    Bbar=1+2W_L/(3S_L^2)
           +N[T_L-T_L^2/Z]/(3S_L^2)
           +sum_light(mu_g^2/S_L^2)E_g,
    Cbar=3-Nmu_0 T_L/(d_0 S_L Z).

These formulas use O(r) scalar sums. They do not require an original
N-by-N inverse or a substituted invariant-only cap certificate.

## Statements

1. All new denominators are positive, Abar>0,Bbar>0 and
   Abar Bbar>Cbar^2. The ENTIRE upper PSD interval of THIS original
   candidate line is

       delta_minus <= delta <= delta_plus,
       delta_minus=N/(Cbar-sqrt(Abar Bbar))<0,
       delta_plus=N/(Cbar+sqrt(Abar Bbar))>0.

   Upper rank is N-1 in its interior and N-2 at both endpoints.
   Moreover delta_plus<N/6<6/kappa. Thus both lower and upper PSD
   constraints hold exactly on [0,delta_plus]. Both greatest ranks
   N-1 hold for 0<delta<delta_plus. At delta_plus lower rank is N-1
   and upper rank N-2. At zero the two ranks are N-2 and N-1.
   H's lower constraint alone still has the longer interval[0,6/kappa].

2. The COMPLETE original FIRST subspace is unchanged by the repair
   for EVERY real delta. The residual aggregate-mean frame is strictly
   below s, sharpening the predecessor's bound below2s. Every other
   positive physical block has frame norm at most Cs, where

       C=1907/988<2.

3. If additionally q>=200h, then EVERY real0<delta<=q/200 gives

       NI-L_delta >= 6L P,
       rank L_delta=rank(I-M_delta)=N-1.

   The exact best upper cap is the same as the seed's and is strictly
   larger than6L. The least eigenvalue and unit eigenvalue are simple.
   In particular delta=q/200 is an explicit rational repair. This is
   a growing interval, not a claim that q/200 is the optimal endpoint.

4. Fix r,h,k1,...,k_(r-1) in the displayed domain and let the integer
   old-cube size n tend to infinity. Write tau(q,delta) for the best
   centered original upper floor, the smallest eigenvalue of NI-L_delta
   on1-perp. Then

       tau(q,delta) -> 6L+6h/(3F+1),

   uniformly for delta in[0,q/200]. Consequently there is NO positive
   constant epsilon giving floor6L+epsilon for this candidate on the
   whole large-cube domain, even at the fixed rational delta1/32.
   This is sharpness for this construction, not optimality among all
   original H competitors and not a counterexample to H.

## 1. Complete aggregate-mean compression

The predecessor's full F-by-F residual Gram has diagonal mu_g for
each facet in group g, within-group off-diagonal
-k_gmu_g^2/[S(k_g-1)], and cross-group off-diagonal-mu_gmu_t/S.
Compress the constant facet profiles using the orthonormal columns
1_group/sqrt(k_g). Every matrix position gives EXACTLY

    C_mean=diag(mu_g)-vv'/S,  v_g=sqrt(k_g)mu_g.             (1)

For example its diagonal is mu_g-k_gmu_g^2/S and its cross entry is
-sqrt(k_gk_t)mu_gmu_t/S. Its sole kernel is(sqrt(k_g))_g, because
mu_g>0 and weighted Cauchy gives positivity with equality only on
that vector. Group-standard profiles are a different sector and
are not counted a second time. The aggregate original PRIVATE
frame is3 times the nonzero spectrum of(1). Since vv'/S>=0,

    lambda_max(3C_mean)<=3max(mu_g)<s.                    (2)

This pays every one of the r-1 mean directions. The other complete
physical blocks have the predecessor's normalized row-sum bounds
991/676,1009/676,1135/676,19/13,1907/988 times s. They are all at
most Cs. Together with(2), this yields the asserted entire non-FIRST
bound. It is not just a quotient calculation: the group-constant
space is invariant in the full residual Gram, and all its other
profiles occur with their original multiplicities in the coupled
standard blocks of the predecessor's exhaustive decomposition.

## 2. Exact FIRST invariance and original projection scores

EVERY private row and ACTUAL empty have the same FIRST projection
z0=-K/ell. Hence on FIRST, U'A is(-3+3h/h)z0=0 and U'B is
(-1+sum_light k_gmu_g/S_L)z0=0. Consequently AB'+BA' annihilates
the entire original range of U_FIRST. The predecessor's frame has
zero cross terms between FIRST and the other exhaustive sectors,
so this original range is invariant for Q and for every repaired Q.

The remaining projections can also be read from ALL original rows.
Let M_g denote the sum of residual vectors in group g and TS_g,WF_g
their trace sums. Heavy private leaves and full rows cancel all
Btilde/T/WA/WF projections when summed over the group. Thus

    U'A=(3/h)M_0,
    U'B=sum_light(mu_g/S_L)[M_g-(c_g/3)TS_g+WF_g].          (3)

No FIRST, leaf-odd or facet-standard direction is omitted: all of
those projections in(3) are zero by their ORIGINAL group sums. The
mean Gram and trace metrics pay the entire surviving projections.

## 3. Original upper resolvent and the count formulas

V=NI-Q is positive definite because Q<=2sP and N-2s=6L>0.
On1-perp it is exactly NI-L0. Both A and B lie in1-perp. The full
row/physical identity, without removing a null or empty direction, is

    V^-1=(1/N)[I+U(NI_physical-U'U)^-1U'].                 (4)

Direct multiplication proves(4). The physical resolvent is positive
and block diagonal in the COMPLETE decomposition. Equation(3) shows
that only means and light traces enter these two upper-dual energies.

For means use the vectors a_g=M_g/sqrt(k_g), with Gram(1). The frame
is3sum_g a_g a_g'. The coefficient vectors of(3) are

    x_0=3/sqrt(h), x_g=0 for light g,
    y_0=0, y_g=sqrt(k_g)mu_g/S_L for light g.

Thus their mean resolvent products are
x'C_mean(NI-3C_mean)^-1x and the corresponding mixed/y products.
Put D=diag(d_g). Sherman--Morrison gives

    (NI-3C_mean)^-1=D^-1-D^-1vv'D^-1/Z,
    C_mean(NI-3C_mean)^-1=[N(NI-3C_mean)^-1-I]/3.

These are full r-by-r identities, including the zero mean direction;
N>0 makes that direction harmless. They yield

    E_Amean=3N/(h d_0)-3/h-3Nmu_0^2/(d_0^2Z),
    E_ABmean=-Nmu_0 T_L/(d_0 S_L Z),
    E_Bmean=[N(T_L-T_L^2/Z)-W_L]/(3S_L^2).                (5)

For a group-g trace, the physical orthonormal frame is

    [ s(1+c_g^2)           -c_g sqrt(6s beta_g)/2 ]
    [ -c_g sqrt(6s beta_g)/2         3beta_g/2    ].

The projection-(c_g/3)TS_g+WF_g has coordinates
(-c_g sqrt(6k_gs)/3,sqrt(k_gbeta_g)). Two-by-two inversion of N
minus this entire frame gives resolvent energy E_g above: its
determinant is H_g and its full numerator is
k_g[beta_g(N-s)+(2N/3)c_g^2s]. A has zero trace projection, and
different traces are orthogonal. Thus B alone receives
sum_light(mu_g^2/S_L^2)E_g in addition to(5).

Now(4), the ORIGINAL row norms/inner product, and(5) give exactly

    A'V^-1A=Abar/N,
    B'V^-1B=Bbar/N,
    A'V^-1B=Cbar/N.                                      (6)

This completes the original N-row inverse bridge, including its
null/empty directions. Positivity of d_g follows from3mu_g<s<N;
Z>0 is explicit; H_g>0 follows because N minus each complete trace
frame is positive definite. Finally V>0 and A,B independent imply
the two-by-two Gram(6) is positive definite, proving Abar,Bbar>0
and Abar Bbar>Cbar^2. Independence follows already from their
disjoint nonempty heavy/light proper supports.

## 4. Exact upper interval and ordering of the two boundaries

Conjugate the original centered upper matrix by V^-1/2. The two
nonzero eigenvalues of V^-1/2(AB'+BA')V^-1/2 are

    [Cbar+sqrt(Abar Bbar)]/N,
    [Cbar-sqrt(Abar Bbar)]/N.

The first is positive and the second negative by(6). The identity
minus delta times this rank-two operator is PSD exactly on the
displayed[delta_minus,delta_plus]. At either endpoint just one of
its centered eigenvalues vanishes. The original constant kernel
is retained, giving upper rank N-2 there and N-1 inside. Outside
the interval an original centered negative direction is obtained
by reversing this invertible congruence. This refutes only this line.

For the positive boundary, the added resolvent Gram in(4) is PSD.
For any PSD two-by-two increment(x,z;z,y), |z|<=sqrt(xy), and

    sqrt((a+x)(b+y))>=sqrt(ab)+sqrt(xy).

Therefore Cbar+sqrt(Abar Bbar) is at least its original row-Gram
value3+sqrt((9+3/h)(1+W_L/S_L^2))>6. Hence delta_plus<N/6.
The lower-dual scalar bounds give

    kappa<5/(hs)+55/(3Ls),
    kappa N<10/h+110/(3L)+30L/(hs)+110/s.

Because L/h<r-1<=n-1<=q/2, L/(hs)<1/2. Also h>=3,L>=4,s>=17.
Consequently

    kappa N<10/3+110/12+15+110/17=1155/34<36,
    delta_plus<N/6<6/kappa.                              (7)

This proves all simultaneous interval/rank assertions. The lower
PSD endpoint lies strictly beyond the positive upper endpoint;
no rank assumption at an unchecked crossing is used.

## 5. A repair interval growing with the old cube

There are q-1 old even directions, and G has squared even norm q-1.
Choose an even vector perpendicular to its even component; the
space has dimension q-2>0. Both G and K are perpendicular to it,
as are all marked mean vectors j_g. The FULL FIRST frame consequently
has eigenvalue2q there. Thus lambda_max(FIRST)>=2q.

The perturbation's original Euclidean norm is<7|delta| for nonzero
delta, by the predecessor's row norms and A.B=3. Its FIRST action
is exactly zero, rather than being estimated by this norm. On the
entire centered complementary space, including the seed's remaining
zero directions, the perturbed largest eigenvalue is at most
Cs+7|delta|. If q>=200h and |delta|<=q/200, this is at most

    [C(203/200)+7/200]q
      =394037q/197600 < 2q,
    2-394037/197600=1163/197600>0.                        (8)

FIRST therefore furnishes the complete original largest centered
eigenvalue and is unchanged by the repair. Its exact centered cap
is the seed's N-lambda_max(FIRST)>N-2s=6L. For positive delta,

    delta kappa < (q/200)(25/(4s)) <1/32<6,              (9)

where h>=3,L>=4 bound5/h+55/(3L)<=25/4. Hence the entire stated
positive interval is strictly inside the LOWER PSD interval too.
This proves the large-cube cap, rational repair, greatest ranks and
simple extrema. It also proves delta_plus>q/200 in that subdomain.

## 6. Exact asymptotic FIRST gap and candidate sharpness

Keep all counts fixed. Let lambda_F(q) be the largest FULL FIRST
frame eigenvalue and gamma(q)=2s-lambda_F(q)>0. Fix a real shift
0<theta<6h and write

    D_theta=(2s-theta)I-A_first,
    B_theta=D_theta+GG',
    w_theta=W'D_theta^-1W,
    z_theta=G'D_theta^-1W,
    g_theta=G'D_theta^-1G.

For all sufficiently large real q the complete D_theta is positive
definite: even directions have6h-theta, odd-perpendicular2q-theta,
heavy q-theta, and each light plane has positive diagonals and

    Delta_g=2q^2+(6h-3theta)q+theta^2-3theta(h+k_g)>0.

No physical direction or multiplicity is dropped. Direct inversion
of each ORIGINAL light plane, and its heavy line, yields

    w_theta= m+3h theta/(q-theta)
             +sum_light 3k_g theta(2q+6k_g-theta)/Delta_g,
    z_theta= -3h/(q-theta)
             -sum_light 3k_g(2q+6h-theta)/Delta_g,
    g_theta= (q-1)/(6h-theta)
             +3h(q-r)/[q(2q-theta)]
             +3h/[q(q-theta)]
             +sum_light 3[(h+k_g)q+3h(h+k_g)-h theta]
                         /[q Delta_g].                 (10)

The FIRST identity is S_FIRST=A_first-GG'+KK'/ell, K=G+W.
Its FULL shifted PSD test is exactly the rank-one criterion

    sigma_theta=ell-K'B_theta^-1K
                =m-w_theta+(1-z_theta)^2/(1+g_theta).   (11)

Here B_theta>0. Thus sigma_theta>0 proves gamma(q)>theta;
sigma_theta<0 gives an original physical negative direction and
proves gamma(q)<theta. Equality corresponds to its shifted boundary.
These are complete FIRST tests, not tests of a few sampled profiles.

Each expression in(10) is a rational function with fixed parameters.
Its leading coefficients give rigorously

    q(w_theta-m)->m theta,
    z_theta->0, g_theta/q->1/(6h-theta),
    q sigma_theta -> 6h-ell theta.                       (12)

For theta below6h/ell the sign is eventually positive; above6h/ell
and below6h it is eventually negative. These two inequalities, with
the already-known gamma(q)>0, are precisely the epsilon bounds for

    gamma(q)->6h/ell.

They apply in particular to the actual sequence q=2^(n-1), n tending
to infinity. No continuity of an increasing-dimensional eigenbasis
is presumed; the full rank-one sign test(11) supplies the bridge.
Equations(8) and FIRST invariance identify tau(q,delta)=6L+gamma(q)
for ALL delta in[0,q/200] once q>=200h. This proves uniformity and
the exact stated upper-cap asymptotics.

Finally choose h=3, all r-1 light counts2, and r>=4. Then F=2r+1,
L=2(r-1) and the limit increment is18/(6r+4), tending to zero as
r tends to infinity. Given ANY epsilon>0, first choose r with this
limit belowepsilon/2, then take an integer n>=r large enough that
q>=200h and gamma(q)<epsilon. At the fixed rational delta1/32,
which is inside[0,q/200], the best cap is strictly below6L+epsilon.
This proves the claimed lack of a uniform positive increment for
THIS construction, with all support/PSD/rank conditions retained.
It says nothing about the optimal cap of arbitrary H matrices.

## Validation boundary and selected next gate

These are ordinary quantified algebraic/spectral/completeness and
limit arguments, not a formal proof or a floating-point experiment.
The whole original support/span and seed scalar bridges are precisely
the cited source-first predecessor; its paid gates are preserved.
NEW preliminary normal gates now pay the count-resolvent(6), both
algebraic roots and all ORIGINAL endpoint-kernel coordinates against
the entire original N70 systems n4,(4,3,2),(5,2,2),(3,2,2,2). Fresh full
Sylvester/Bareiss elimination checks every division, all70 positive
leading minors per system, both70-coordinate inverse RHS products,
all three original Gram energies and both algebraic centered kernels.
All104 original FIRST annihilations and3484 full physical frame-cross
actions are zero. Inputs are byte-bound to the credited predecessor;
no old program, factor, inverse or result record is executed/imported.

Three additional NEW normal children at shifts theta1 and2 retain
all actual original rows and pay the complete FIRST systems of
dimensions17/17/18, all1804 shifted-frame identities and full D/B
positive solves, comparing every count scalar(10)--(11). A separate
generic symbolic child checks six full polynomial identities in
Q[N,s,b,c,k,q,h,t], with peak10 terms below the unchanged512 guard,
and the exact constants(7)--(8). All seven math children exit0; max
recorded child1.575761s, peak20096KiB. None is a large-cube enumeration.

The initial upper-reader source snapshot is preserved with its paid
receipts. Its later helper adds only an explicit option to suppress
the ORIGINAL centered-coordinate check for PHYSICAL shifted systems;
the original route retains that check. The final reader binds the
source before importing any bundle arithmetic, regenerates the credited
geometry and checks every original identity before reading EXPECTED.
The only compact-output normalization replaces verbose leading-minor
hexadecimal lists by their complete digests/counts after all pivots and
divisions are checked. Inverse images, count energies, both full original
endpoint kernels, shifted systems and all symbolic identities remain
explicit. VALIDATION.json records fresh normal/O/isolated-cold and
meaningful mathematical/source-binding controls; source publication
does not itself prove the ordinary infinite/real theorem.
These are same-author controls, not an independent mathematical audit.

Run ONE intensive child at a time, native threads1, each60s, within
existing1CPU2GiB128tasks and before-construction n<=6,h<=10,N<=80;
packing32MiB and polynomial guard512 remain unchanged. No original
matrix in q>=200h is constructed: even its smallest size exceeds
these guards. The asymptotic family is proved by(10)--(12), never by
an incomplete large enumeration. No timeout/UNKNOWN/memory kill or
missing original control proves mathematical absence. New source
publication and graph submission await appropriate source checks.
