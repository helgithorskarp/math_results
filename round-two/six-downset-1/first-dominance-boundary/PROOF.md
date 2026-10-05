# Exact cap plateau and FIRST-dominance boundary on the original repair line

Actual author **six-downset-1 / researcher**, 2026-10-05. Ordinary
author-complete argument, **UNFORMALIZED and independently UNREVIEWED**.
This source preserves the sealed private mathematical argument, with
only this status paragraph changed. VALIDATION.json records actual
source-delivery checks separately. Historical private/null fields in
regenerated evidence do not assert graph commitment or independent review.

Sole target: Spectral Chvatal Conjecture H, Ellis--Filmus--Friedgut,
[Section4](https://arxiv.org/html/2609.28404v1#S4). Live history and
actual Section4 were read on2026-10-05; the history still displays v1
of2026-09-23. Classical Chvatal is prior art; general H/I remain the
paper's proposed spectral questions. No global resolution is claimed.

The complete original construction, support/span, scalar positivity,
all sectors and lower repair line are credited to source
b7d26214d61e1aba86367ce2162ccf2a4e1aa749,
[unique-heavy proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/unique-heavy-triangle-cap/PROOF.md).
The exact upper endpoint, FIRST invariance, complete count projections,
shifted FIRST identities and non-FIRST norm are credited to source
6b95f73178cfbdfcac4ff993f4eb92970f5605ee,
[upper/FIRST proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/first-sector-repair/PROOF.md).
Both are ordinary/unformalized/independently unreviewed at this new scope.
Their source/math gates are closed and are not replayed. Rank-two
congruence and Woodbury themselves are standard tools. New content here
is the exact unique FIRST root, the singular-space bridge, the complete
cap plateau and the unique count-defined cap after the crossing.

## Scope, notation and conclusions

Use EVERY integer r>=3,n>=max(4,r),h>k_g>=2 for light g=1,...,r-1,
F=h+sum_light k_g>=9, and additionally q=2^(n-1)>=200h. Keep distinct
old marks, disjoint outside private pairs and ACTUAL empty. Put

    k0=h, L=sum_light k_g, m=3F, ell=m+1,
    s=q+3h, N=2q+6F, P=I-J/N.

Let U be the complete positive physical original row system of the
cited source, Q=UU', Q1=0, rankQ=N-3. Let F_row be the entire original
range of its FIRST sector, of dimension2q+r-2. Both original centered
repair vectors A=(-3,a),B=(-1,b) lie in F_row-perp, where a=1/h on
heavy private rows and b=mu_g/S_L on light private FULL rows. They
have zero sum, independent disjoint nonempty proper supports, and

    A.A=9+3/h, B.B=1+W_L/S_L^2, A.B=3.

Use the cited scalars mu_g,beta_g,c_g,S,S_L,W_L,kappa, without changing
their dependence on the actual original N,q,s or counts. The repair is

    R=AB'+BA', Q_delta=Q+delta R,
    L_delta=J+Q_delta, M_delta=(L_delta-sI)/(N-s).

The upper cap is rho(delta)=lambda_min((NI-L_delta)|1-perp)
=N-lambda_max(Q_delta|1-perp). It is not the least eigenvalue of M.
The source already gives the exact simultaneous lower/upper PSD domain
[0,delta_upper], with delta_upper<6/kappa, and the lower/upper ranks.

Define sigma(theta) by the explicit count formulas in Section1 below.
There is a UNIQUE root gamma in(0,6h). Set t=2s-gamma. Then t is the
SIMPLE largest FIRST eigenvalue and 2q<t<2s. For spectral level x>=t,
define abar(x),bbar(x),cbar(x) by Section2 and

    dminus(x)=x/[cbar(x)-sqrt(abar(x)bbar(x))]<0,
    dplus(x)=x/[cbar(x)+sqrt(abar(x)bbar(x))]>0.

These are well-defined complete original count resolvents. The ENTIRE
real cap plateau of this candidate is exactly

    dminus(t)<=delta<=dplus(t),  rho(delta)=N-t=6L+gamma.

On its strict interior the cap-attaining centered eigenvalue is simple;
at either endpoint it has multiplicity exactly2. Off this interval
rho(delta)<N-t. Define delta_FIRST=dplus(t). Then

    q/200<delta_FIRST<delta_upper=dplus(N)<6/kappa.

On the simultaneous PSD domain[0,delta_upper], the exact best cap is
constant on[0,delta_FIRST], then STRICTLY decreases to0. For EVERY
delta>delta_FIRST there is a UNIQUE x>t with dplus(x)=delta and
rho(delta)=N-x; this is a complete cap formula on the original line,
including parameters outside its simultaneous PSD domain. The top centered
eigenvalue x beyond the crossing is simple. Every positive
delta<delta_upper still has the source's two greatest ranksN-1 and
simple least/unit M eigenvalues; the new cap multiplicity2 at
delta_FIRST does not change either of those M extrema.

No entrywise nonnegativity, wider smaller-cube closure, overlapping
private pairs, arbitrary-matrix optimum, global H/I, or historical
priority assertion is made. Negative/outside parameters refer only to
this supported stochastic line. They do not rule out other H matrices.

## 1. Complete FIRST root, including parity multiplicities

Write A_first=A_old_full+sum_groups3k_g j_g j_g', with j_g=H_g/(3h)
+Bbar_g, W=sum_groups3k_g j_g, K=G+W. The entire physical FIRST frame is

    S_FIRST=A_first-GG'+KK'/ell.

At 0<=theta<6h let D_theta=(2s-theta)I-A_first and
B_theta=D_theta+GG'. The original complete sector decomposition pays
old even directions (q-1), old odd-perpendicular directions(q-r),
the heavy line, and every light plane. Their D eigenvalues are
6h-theta,2q-theta,q-theta, and the two eigenvalues of the light matrix

    [q(2-k_g/h)-theta   -sqrt(qs(k_g/h)(1-k_g/h))]
    [-sqrt(qs(k_g/h)(1-k_g/h))   s(1+k_g/h)-theta].

Both light diagonals are positive: the first>=q-theta>0 and the
second>=s-theta>0. Its determinant is

    Delta_g(theta)=2q^2+(6h-3theta)q+theta^2-3theta(h+k_g).

Its derivative is -3q+2theta-3(h+k_g)<0 on[0,6h], and
Delta_g(6h)=2q(q-6h)+18h(h-k_g)>0. Hence EVERY original D_theta
direction is positive, with all old/mean multiplicities retained.
B_theta>0 throughout the open endpoint range. No actual matrix at a
large q is used to establish this universal statement.

The cited original inverse products are, with all light groups counted,

    w=m+3h theta/(q-theta)
        +sum_light3k_g theta(2q+6k_g-theta)/Delta_g,
    z=-3h/(q-theta)
        -sum_light3k_g(2q+6h-theta)/Delta_g,
    g=(q-1)/(6h-theta)+3h(q-r)/[q(2q-theta)]
        +3h/[q(q-theta)]
        +sum_light3[(h+k_g)q+3h(h+k_g)-h theta]/[q Delta_g],
    sigma(theta)=ell-K'B_theta^-1K=m-w+(1-z)^2/(1+g).

At0, w=m,z=-m/q and sigma(0)=(1+m/q)^2/(1+g)>0. For theta->6h
from below, w,z have finite limits while g->+infinity. Every term
of w(6h)-m is strictly positive, since q>6h and2q+6k_g-6h>0.
Thus sigma(theta)->m-w(6h)<0. Continuity gives a root in(0,6h).

Crucially, this is the COMPLETE physical inverse, so differentiation
is a basis-independent identity:

    sigma'(theta)=-K'B_theta^-2K<0.

Indeed B_theta'=-I and K!=0: its even component equals G's nonzero
component, whose squared norm is q-1. This pays strict monotonicity
and UNIQUE root gamma without inferring it from finite sign sampling.

The full shifted FIRST matrix is B_theta-KK'/ell. At gamma its
positive-congruence rank-one test has exactly one zero direction and
is PSD. Before gamma it is PD and after gamma it has a negative
direction. Consequently t=2s-gamma is the largest FIRST eigenvalue,
simple, and lies strictly between2q and2s. The physical-to-original
row map is injective on the positive physical space; it carries this
eigenvalue and its multiplicity to F_row. In particular old parity
directions of eigenvalue2q do not contribute extra multiplicity at t.

## 2. Restricted resolvent at the singular FIRST level

Let E=1-perp intersect F_row-perp. It has original dimension6F-r+1.
All remaining original positive sectors have norm<=Cs,
C=1907/988, by the cited exhaustive decomposition; original zero
directions have eigenvalue0. Since s<=203q/200,

    Cs<=C(203/200)q<2q<t.

Thus V_x=xI_E-Q|E is PD for EVERY x>=t, even though tI-Q on the
whole original row space is SINGULAR on the FIRST top vector. We do
not invert that singular whole-space operator. A,B belong to E by
their original centered/FIRST annihilation, and remain independent.

Take the entire physical complement U_C. Its original row range is
in E because the FULL frame cross actions vanish and U'1=0. On E,
Q=U_C U_C'. The complete inverse identity is

    V_x^-1=(1/x)[I_E+U_C(xI_C-U_C'U_C)^-1U_C'].

It follows by direct multiplication. The physical complement has
dimension6F-r-1; the original E has TWO additional zero directions.
They are retained by I_E/x. This explicitly pays original null/empty
scores and avoids treating a physical quotient as the entire original
matrix. Every inverse is positive at x>=t.

Only the COMPLETE residual mean and light trace projections of A,B
are nonzero, as in the cited original projection identity. Redo the
same mean Sherman--Morrison and full light-trace inversion with free
spectral level x, not with a changed construction size. Define

    d_g=x-3mu_g, T=sum_groups k_gmu_g^2/d_g,
    T_L=sum_light k_gmu_g^2/d_g, Z=S/3+T,
    H_g=x^2-x[s(1+c_g^2)+3beta_g/2]+3s beta_g/2,
    E_g=k_g[beta_g(x-s)+(2x/3)c_g^2s]/H_g,
    abar=9+3x/(h d_0)-3xmu_0^2/(d_0^2 Z),
    bbar=1+2W_L/(3S_L^2)+x(T_L-T_L^2/Z)/(3S_L^2)
           +sum_light(mu_g^2/S_L^2)E_g,
    cbar=3-xmu_0T_L/(d_0 S_L Z).

These are O(r) scalar sums per evaluation. Every d_g>0 because
3mu_g<s<t; Z>0; every H_g>0 because x exceeds its entire trace
frame norm. The full original identity just proved yields

    A'V_x^-1A=abar/x, B'V_x^-1B=bbar/x, A'V_x^-1B=cbar/x.

This two-by-two Gram is PD, so abar,bbar>0 and abar*bbar>cbar^2.
This pays the count-substitution bridge AT the singular FIRST level;
no limiting pseudoinverse or unchecked full-space inverse is assumed.

## 3. Entire plateau and multiplicities

Conjugate xI_E-Q_delta|E by V_x^-1/2. It is the identity minus
delta times the original rank-two operator built from V_x^-1/2A,B.
The latter has exactly two nonzero eigenvalues

    (cbar+sqrt(abar*bbar))/x>0,
    (cbar-sqrt(abar*bbar))/x<0.

Therefore xI_E-Q_delta|E is PSD exactly for
dminus(x)<=delta<=dplus(x), PD in the strict interior, with exactly
one zero direction at either endpoint. Outside this interval it has
an original negative direction. Every original E direction is paid
by the invertible congruence, including the TWO zero seed directions.

At x=t the entire FIRST sector is unchanged, has largest eigenvalue t
and one such eigenvector. Combining the orthogonal original FIRST/E
spaces proves exactly the displayed whole real cap plateau. Inside
it E has no eigenvalue t, so the cap is simple. At either endpoint E
contributes one, giving multiplicity2. Outside E has an eigenvalue>t,
so the cap is strictly below N-t. These statements include EVERY
centered original row direction; J contributes only the constant
direction and is removed by restriction to1-perp.

## 4. Unique cap beyond the crossing and endpoint ordering

For x2>x1>=t, the difference V_x1^-1-V_x2^-1 is PD on E. Since A,B
are independent, its two-vector Gram increment is PD. For any PD
increment (u,w;w,v), w>-sqrt(uv), and for any positive a,b,

    sqrt((a+u)(b+v))>=sqrt(ab)+sqrt(uv).

It follows that phi(x)=c(x)+sqrt(a(x)b(x)), using the UNscaled
inverse Gram a=abar/x,b=bbar/x,c=cbar/x, is strictly decreasing.
It is positive and continuous; the full original resolvent asymptotic
V_x^-1=I_E/x+O(x^-2) gives

    x phi(x)->3+sqrt((9+3/h)(1+W_L/S_L^2))>0.

Hence dplus(x)=1/phi(x) is continuous, strictly increasing and tends
to infinity. For delta>dplus(t), it has a unique inverse x>t. At
that x the congruence in Section3 has one zero eigenvalue and is PSD,
so lambda_max(Q_delta|E)=x is simple and is the entire original
centered maximum. This proves rho=N-x and strict cap decrease.

At N>2s>t, the full NI-Q resolvent agrees with the restricted E
resolvent on A,B, so dplus(N) is precisely the cited delta_upper.
Strict monotonicity gives delta_FIRST<delta_upper<6/kappa. At
delta=q/200 the cited strict bound Cs+7delta<2q<t makes the ENTIRE
E upper matrix at t PD, not merely PSD. Thus q/200<delta_FIRST.
Cap/ranks throughout[0,delta_upper] follow, with floor0 at its upper
endpoint and the original constant kernel counted separately.

## Evidence and remaining delivery boundary

The universal real/integer scope and original/physical completeness
are supplied by this ordinary proof plus its expressly cited parents.
New exact controls should pay free-level count energies against full
original systems, full physical shifted FIRST derivatives, and count-
only isolation of gamma/plateau endpoints. The target large-cube
original matrices are never allocated. No finite count list or matching
digest is proof of all counts; no cold/O replay is independent review.
Final source binding, semantic/source adverse and cold/O delivery gates
are separate and may remain unpaid at a natural research checkpoint.

Keep existing1CPU2GiB128tasks/native1, ONE intensive child, each60s.
Literal geometry must enforce n<=6,h<=10,N<=80 BEFORE arrays;32MiB
and512 polynomial terms remain. Scalar count evaluations do not
construct their N-by-N target matrices. Never construct r5N98,
unequalr4N82,balanced-fourN88 or the q>=200h originals(minimumN2102).
Timeout/UNKNOWN/interruption is incomplete work, not nonexistence.
