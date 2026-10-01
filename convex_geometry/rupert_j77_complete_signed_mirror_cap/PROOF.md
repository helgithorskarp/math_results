# A complete signed-motion exclusion on J77's physical 1/1000 mirror cap

Author **six-rupert-2**, role **researcher**, 2026-10-01. This is a complete
author-checked written intermediate proof with exact finite hypotheses.
It is **unformalized and independently unreviewed**. Historical priority
is unasserted. Global Rupert property of J77 remains **OPEN**.

## 1. The original body, receiving domain and theorem

Let K be the original unit-edge, asymmetric 55-vertex paragyrate diminished
rhombicosidodecahedron, Johnson solid J77, in the byte-pinned original
model. Put s=sqrt(5)>0, e=(1,0,0), a5=(0,(1+s)/2,1), c=(s-1)/4, and
use the actual proper body rotation

    Rv=cv+(1-c)(a5.v)a5/(a5.a5)+(a5 cross v)/2.

Let E={+/-R^j e:0<=j<5}, M_v=I-2vv^T/(v.v), P_v=I-vv^T/(v.v).
Receiving normals n are PHYSICAL UNIT vectors. Delta=dist(n,E) is their
Euclidean chord distance; all spatial angles are principal full angles.

**Theorem.** If delta<=1/1000, then for every original Q in SO(3), every
planar t in n-perp and lambda>=1,

    lambda P_n(QK)+t subseteq P_nK                           (1)

holds exactly for lambda=1, t=0 and, up to an ACTUAL RIGHT C5 body factor h,

    Qh=I or Qh=M_n M_q,                                     (2)

where q is the nearest signed axis in E. Both motions give equal shadows.
Consequently strict Rupert passage is excluded on the ENTIRE CLOSED
physical 1/1000 mirror cap, including all receiving walls and all signed
motions of the two actual reflected source rotations.

This extends the [two-sector signed result](../rupert_j77_signed_mirror_sectors/PROOF.md),
source 843712820fd1ee1496cc82228794a8d7fe4f0fa3, graph8136, to the other
five sectors, and the preceding complete 1/100000 cap, graph7988, by a
factor100 in its uniform physical radius. It removes the two cone
hypotheses in the [whole-cap necessary receiving-balanced reduction](../rupert_j77_receiving_balanced_stress/PROOF.md),
graph8086, on ALL seven sectors. **The global receiving complement,
larger complete caps and global J77 decision remain OPEN.**

We use the original receiving body/sign/reflection folds from those
parents. They preserve all original placements and the physical t,
not a centered or surrogate body. They put the nearest axis at +e,
the raw normal at u=e+r=(1,y,z), n=u/||u||, and r in one of the seven
CLOSED original sectors21,23,28,30,31,32,33. The physical cap gives

    delta<=||r||<cr delta, cr=1001/1000,                     (3)

and the positive coefficient sum in each receiving triangle is<4delta<1/4.
Thus the complete closed sector supports from the finite parent remain
applicable. The replay includes55original vertices, the actual body
and mirror, interiority of0, allseven closed strata and36,960 original
support comparisons. No central symmetry or source-coordinate sign
is assumed. The axis delta0 is already classified by the full-angle
parent; assume delta>0 until the equality conclusion below.

## 2. Both actual rotations use the SAME small right gauge

The [all-source full-angle theorem](../rupert_j77_area_axis_roll/PROOF.md),
source86dcf1e10d0eddbc26fc8343b6df4fcc642d47c6, graph7867, supplies an
actual right h in <R> with angle(Qh)<15delta. Use Q to denote that gauged
rotation in the receiving frame. Define

    Qtilde=M_u Q M_e.

Because M_e permutes the ORIGINAL K and P_u M_u=P_u, Qtilde is proper
and has EXACTLY the same projected source body and the same physical t
as Q. This is an involution; no new independent placement is substituted.

The triangle inequality for principal SO(3) rotation angles gives

    angle(Qtilde)<=angle(Q)+angle(M_uM_e)
                 <15delta+2||r||<18delta.                  (4)

Here angle(M_uM_e)=2arctan||r||, and conjugation by M_e preserves the
principal angle. Apply the full-angle theorem AGAIN to this SAME
placement, represented by Qtilde. There is h_t in <R> with
angle(Qtilde h_t)<15delta. If h_t were nonidentity, the group-angle
triangle inequality would give angle(h_t)<33delta<=33/1000<1.
Every actual nonidentity R^j instead has principal angle>1: the checker
reconstructs its full matrix and original vertex permutation and proves
its cosine=(trace(R^j)-1)/2<1/2. Since cos(1)>=1-1/2=1/2, this gives
the asserted angle gap. All five original permutations and order-five
closure are rechecked. Therefore h_t=I and

    angle(Q),angle(Qtilde)<15delta.                         (5)

Crucially no second right gauge is applied to the reflected Cayley vector.
For actual Cayley vectors w=(rho,p), wtilde=(rhotilde,ptilde), put
eta=||w||, etatilde=||wtilde||. From sin x<x and cos x>=1-x^2/2,

    eta,etatilde < L0 delta, L0=151/20.                     (6)

Indeed tan((15/2)delta)<(15/2)delta/(1-(225/8)delta^2), and the strict
rational gate L0(1-(225/8)d^2)>15/2 holds at d=1/1000.

Let J(y,z)=(-z,y), w0=e cross r=Jr and D=1+w0.p. The already replayed
reflection identities, in the SAME gauge, give

    D>0, D<=Dmax=1+10cr d^2,
    rhotilde=(rho+r.p)/D, ptilde=(w0-p+rho r)/D,
    rho-rhotilde=-[p,ptilde], [a,b]=a_yb_z-a_zb_y.           (7)

The denominator bound10 is retained as a valid conservative parent
bound, not confused with the sharper L0. Both inverse directions are
included. Define T=t-t_xu, so T.x=0 and P_uT=t, and

    C=(1+eta^2)T/2, Ctilde=(1+etatilde^2)T/2.               (8)

The two C vectors encode the same arbitrary PHYSICAL translation. If
eta*etatilde=0, equation(7) already identifies an equal-shadow motion;
handle its translation and scale as in Section7. Henceforth assume
eta*etatilde>0 and put m=min(eta,etatilde)>0.

The parent's unconditional positive common-coordinate combinations have
total coefficients<mu=807/100 for either translation component and
<mr=374/100 for rho. Their residual error is bounded by

    12delta eta+(23/10)eta^2+6delta||C||.                   (9)

This uses the common mirror-fixed originals, not critical-cone membership.
Use(6) in(9). The fresh whole-radius scalar gates establish ownC385,
ownrho119, and then, using(8) and BOTH inverse axial directions,

    ||C||,||Ctilde||<386delta m,
    |rho|,|rhotilde|<121delta m.                            (10)

Explicitly the gates are

    385(1-9mu d)>(3/2)mu[12+(23/10)L0],
    386>385(1+100d^2),
    119>mr[12+(23/10)L0+6*385d],
    121>Dmax(119+cr).

The last bound uses rho=D(rhotilde+r.ptilde)/(1+||r||^2) and its reversed
counterpart. Also KF=51/50 satisfies KF^2[1-(121d)^2]>1. Thus throughout
the nonzero branch,

    eta<KF||p||, etatilde<KF||ptilde||.                    (11)

These initial bounds are unconditional. No cone-dependent bootstrap from
graph8086 or smaller-radius normal constant is imported.

## 3. Construct positive original-contact coordinate stresses

Each sector has32 persistent original contacts(a,b,j). Set

    v_i=V_j, edge_i=V_b-V_a, h_i0=(edge_i cross e).v_i>0,
    m_i0=(edge_i cross e)/h_i0, k_i=(edge_i)_x/h_i0,
    m_i(u)=m_i0-e(m_i0.r)+k_iw0,
    F_i=m_i(u).[w crossv_i+w cross(w crossv_i)+C].           (12)

These are original receiving supports on the entire CLOSED sector.
Interiority of0 first reduces(1) to NECESSARY unit-source containment
with the SAME t. The exact Cayley formula then gives F_i<=0.
The full affine normal is rederived from each selected original edge;
noncommon source vertices can have nonzero x-coordinate and are retained.

Let a0,a1 be the sector's actual critical tangent rays, normalized to
l1norm1. The fixture freezes a feasible four-row nonnegative coordinate
dual for each k=0,1, satisfying ALL five critical identities

    sum c_i m_i0=0,
    sum c_i(v_i crossm_i0).e=0,
    sum c_i(v_i crossm_i0).a_j=-1_{j=k}.                   (13)

Add sigma_k times the parent's POSITIVE normalized critical common stress
omega0, on its six original mirror-fixed contacts. The multipliers are

| Closed sector | sigma0 | sigma1 |
|---|---:|---:|
|21|0|0|
|23|0|0|
|28|3|0|
|30|0|0|
|31|0|0|
|32|0|5|
|33|1|0|

All common originals have v_i.x=0, and their stress balances normal and
ALL critical torque coordinates. Thus this explicit addition preserves
(13) and the coordinate covector while changing the signed quadratic
moments. It does NOT assert that the fixed omega0 balances receiving
normals away from0. Its surviving receiving translation is retained.
Every augmented weight is nonnegative; positivity does not depend on
a numerical optimizer or an optimality assertion.

For each augmented dual put

    c=sumc_i, b=sumc_i(v_i)_x(m_i0)_t,
    S=sumc_i(v_i)_t(m_i0)_t^T,
    B=sumc_i k_i v_i FULL3D, Kd=sumc_i k_i,
    H_k=cI-S+B_xJ, chi_k=||b||_1,
    xi_k(p)=-(Jb).p.

Then S is symmetric with tracec by critical axial balance, while H_k
can be NONSYMMETRIC. With p=x0a0+x1a1, xi_k(p)=x_k exactly.
Use the prior universal original-contact algebra, independently replayed
on ALL14 augmented duals in seven independent variables. It gives

    sumc_i F_i=-x_k-c_k||p||^2+rho b.p
      +D[p^T H_k ptilde-c rho rhotilde]
      +rho B_t.r-(p.r)[p,B_t]-rho^2(B_t.w0)+Kd w0.C,
    c_k=xi_k(w0)>=0.                                      (14)

The receiving-ray sign checks prove c_k>=0 throughout each CLOSED sector.
The direct original edges agree with both moment and reflected-bilinear
expansions. Identity w0 and mirror-root slack are preserved: at
w=(0,w0),C0 the expression is -(1+||r||^2)c_k. No spurious zero or
centering is introduced. The actual constants c,b,S,B,Kd, original
labels, coefficient lists and polynomial hashes are in expected.json.

Define h^k_ij=a_i^T H_k a_j. The additions in the table repair every
unfavorable opposite row. The checker proves

    h^k_lk>=0, h^k_ll>=0, l=1-k.                          (15)

The opposite diagonal h^k_ll is generally NONZERO, including sector23
without augmentation. It is not discarded. All other signed corner
entries are retained, and actual chi_k are used instead of a rounded
common covector norm.

## 4. A directed two-coordinate negative-part estimate

Write ptilde=y0a0+y1a1. Let N_xk=max(0,-x_k), N_yk=max(0,-y_k),
V_k=N_xk+N_yk, U=V0+V1. Equation(7) implies EXACTLY

    x_k+D y_k=c_k+rho xi_k(r).                             (16)

If x_k<0 then y_k^-<=|rho||xi_k(r)|/D and
c_k<=D|y_k|+|rho||xi_k(r)|. These inequalities preserve mirror slack.

Assume for this step eta,etatilde<Ldelta, both axial components
<beta delta m and both C norms<cc delta m. Put bn=||B_t||_1, kn=|Kd|.
The nonbilinear terms in(14), together with the exceptional negative y_k
term in the opposite row, are bounded below by -E_k delta^2m, where

    E_k=(chi_k+bn)(Dmax L^2+beta cr L^2 d^2)
      +chi_k beta L+bn beta cr+bn beta^2 cr L d^2
      +c Dmax beta^2 L d+kn cr cc
      +h^k_lk chi_l chi_k beta cr L d.                    (17)

All c,bn,kn,h,chi here are ACTUAL exact constants of that augmented dual.
For completeness, -c_k||p||^2 costs
chi_k(Dmax L^2+beta cr L^2d^2); rho b.p costs chi_k beta L;
the axial product costs c Dmax beta^2 L d; rho B_t.r costs bn beta cr.
The determinant identity

    p.r=D[p,ptilde]-rho[p,r]

bounds -(p.r)[p,B_t] by bn(Dmax L^2+beta cr L^2d^2).
The rho^2 term costs bn beta^2 cr Ld^2, and the surviving translation
costs kn cr cc. These use eta^2etatilde<=L^2delta^2m and m<=Ldelta.
The last term in(17) is precisely the cost of y_k^- when x_l>=0.

For x_k<0, the signed bilinear expression in(14) is bounded below by

    -D N_xk sum_j |h^k_kj||y_j|
    -D N_xl h^k_lk|y_k|
    -h^k_lk |x_l||rho||xi_k(r)|
    -D h^k_ll[|x_l|N_yl+N_xl|y_l|].                     (18)

The last line is valid for every sign of x_l,y_l; if both are negative
it is conservative, since their actual product is nonnegative. This
retains the EXTRA opposite-diagonal coupling missing from the earlier
zero-diagonal special case. When x_k>=0, N_xk=0 and the resulting upper
bound remains nonnegative. Apply the SAME contacts and calculation to
the actual companion (with the same physical t), then add the two bounds.
Since |x_j|<=chi_j eta and |y_j|<=chi_j etatilde,

    V_k <= B_kk V_k+B_kl V_l+2E_k delta^2m,               (19)

with the NONNEGATIVE matrix

    B_kk=Dmax Ld sum_j |h^k_kj|chi_j,
    B_kl=Dmax Ld[h^k_lk chi_k+2h^k_ll chi_l].             (20)

The factor2 in the opposite-diagonal term comes from the two reflected
inequalities. No scalar column-sum bound or entire-plane definiteness
is assumed. Some initial column sums exceed1 while this directed inverse
still exists and is nonnegative.

Put a=1-B00, d1=1-B11, b1=B01, c1=B10. On every sector, the exact gates

    a>0, d1>0, Delta=a d1-b1 c1>0                       (21)

give

    (I-B)^-1=(1/Delta)[[d1,b1],[c1,a]]>=0.

Multiplying the COMPONENTWISE inequalities(19) by this actual nonnegative
inverse gives

    V0 <= 2(d1E0+b1E1)delta^2m/Delta,
    V1 <= 2(c1E0+aE1)delta^2m/Delta.                      (22)

The declared integer W in the next table is STRICTLY above the sum
of these two exact coefficients. Consequently U<Wdelta^2m.
Both exact matrix inverse products, all signs and all bound margins are
recomputed. This is a finite exact inverse certificate, not a numerical
spectral-radius or solver assertion.

## 5. Unconditional bootstrap and fresh common bounds

The checker reconstructs the minimum of ||(1-t)a0+t a1||^2 on0<=t<=1,
testing both endpoints and any feasible quadratic stationary point.
On allseven sectors this gives norm>amin=7/10. The individual ray norms
are <=amax in the table; some are EXACT unit endpoints. They need not
share an orthant, so this direct segment check is necessary.

Let P_x=sum x_k^+, P_y=sum y_k^+. The sum of positive vectors and the
sum of negative vectors give

    amin(P_x+P_y)<=||p+ptilde||+amax U,
    eta+etatilde<KF(amax/amin)||p+ptilde||
                  +KF(amax+amax^2/amin)U.                 (23)

This applies to actual signed source vectors; it imposes no cone
membership. From(7), p+ptilde=w0+rho r-(D-1)ptilde, so initial(6) gives

    ||p+ptilde||<cr delta(1+L0d+L0^2d^2).

Use initial(10) and the directed bound with L=L0, beta121, cc386.
Writing f=KF(amax+amax^2/amin), m<=(eta+etatilde)/2, the strict gates

    1-f W d^2/2>0,
    Ls[1-f W d^2/2]>KF(amax/amin)cr(1+L0d+L0^2d^2)

prove eta+etatilde<Ls delta UNCONDITIONALLY. Then each individual norm
is below Ls delta. Recompute(9), with epsilon=12+(23/10)Ls. Fresh bounds
in the table satisfy

    ownC(1-9mu d)>(3/2)mu epsilon,
    pairC>ownC(1+100d^2),
    ownrho>mr(epsilon+6 ownC d),
    pairrho>Dmax(ownrho+cr).                              (24)

The pair bounds hold in BOTH directions for the SAME physical T.
Repeat the directed calculation(17)-(22) with Ls,pairrho,pairC and
the refined W. Every gate is recomputed at the whole physical radiusd.

| Sector | amax | Initial W | Ls | ownC / pairC | ownrho / pairrho | Refined W | Actual A-corner interval |
|---|---|---:|---|---|---|---:|---|
|21|3/4|416000|33/20|207 / 208|64 / 66|12400|(21/50,23/50)|
|23|1|76000|163/100|206 / 207|64 / 66|9400|(21/50,23/50)|
|28|1|31000|153/100|203 / 204|63 / 65|4000|(3/25,23/50)|
|30|39/50|26000|59/50|193 / 194|60 / 62|4100|(1/100,13/100)|
|31|39/50|26000|59/50|193 / 194|60 / 62|4100|(1/100,13/100)|
|32|23/25|145000|161/100|205 / 206|64 / 66|13800|(1/10,43/100)|
|33|23/25|224000|179/100|211 / 212|66 / 68|11300|(43/100,12/25)|

## 6. A signed bilinear contradiction on every sector

The receiving-balanced parent graph8086 supplies, for ALL actual signed
motions, the necessary translation-free inequality

    p^T A(u)ptilde<=h(u)rho rhotilde, h(u)<101/100.         (25)

Here A(u) is SYMMETRIC and RECEIVING dependent; it is distinct from the
constant generally nonsymmetric H_k of the coordinate stresses. Its
positive receiving weights and its exact nine-variable factorization
are fully replayed. The parent's critical ray corners plus its uniform
receiving loss bounds prove EACH of the four actual corners is strictly
inside the sector's displayed interval (ell,gamma). This is a bound
on the ENTIRE closed cap, not evaluation only at r0.

Write N_x=N_x0+N_x1, N_y=N_y0+N_y1 and alpha=KF amax. With the sector's
refined W, put kappa=W d^2 and g=(1+amax kappa)/amin. Ray norms give

    P_x>=eta/alpha-N_x, P_y>=etatilde/alpha-N_y,
    P_x<g eta, P_y<g etatilde,
    eta N_y+etatilde N_x<=U max(eta,etatilde)
                           <kappa eta etatilde.          (26)

The last identity uses m*max(eta,etatilde)=eta etatilde. The two lower
bounds on positive sums are positive by the exact gate1/alpha>kappa.
For the upper bound, amin P_x<=||p||+amax N_x<=eta+amax N_x, and
N_x<Wdelta^2m<=kappa eta; likewise for the companion.

Expand(25) using every positive and negative coefficient. Positive-positive
products have corners>ell. The negative-negative products are nonnegative;
the mixed terms have magnitude bounded by gamma times the corresponding
positive/negative sums. Thus

    p^T A(u)ptilde
      > [ell(1/alpha^2-kappa/alpha)-gamma g kappa]
           eta etatilde.                                (27)

Meanwhile (24) bounds the right side of(25) above by

    (101/100)(pairrho d)^2 eta etatilde.                   (28)

For EACH sector the checker proves the exact rational difference

    ell(1/alpha^2-kappa/alpha)-gamma g kappa
        -(101/100)(pairrho d)^2 > 1/100 >0.                (29)

All seven differences are recorded exactly in expected.json. This
contradicts(25) whenever eta*etatilde>0. There is no unsupported
assumption that either source tangent lies in the critical cone.

## 7. Equality, reproduction and proof boundary

One actual Cayley vector must therefore be zero. Equation(7) and the
reflection involution give Q=I or Q=M_uM_e in the folded gauge; both
have precisely the receiving shadow. Necessary unit containment of this
bounded shadow with its translate forces t=0 by planar support functions.
Positive projected area in the original(1) then forces lambda=1. Undo
the ACTUAL receiving folds and RIGHT body factor to obtain(2). For delta0
the existing exact full-angle classification gives the same conclusion.
The mirror M_q permutes K and P_nM_n=P_n, so BOTH motions in(2) indeed
give equality, including their coincidence at the axis. Strict passage
is excluded on the full stated closed cap.

From the repository root run these commands separately, with all
solver/BLAS/OpenMP threads1, Python3.11+ standard library only:

    python3 -B convex_geometry/rupert_j77_complete_signed_mirror_cap/verify.py --self-test
    python3 -B -O convex_geometry/rupert_j77_complete_signed_mirror_cap/verify.py --self-test

Both must compare EVERY byte of expected.json. The direct signed-sector
parent's entire12972expected bytes are replayed and compared, along
with its full receiving-balanced69495byte, bilinear31456byte, finite32804byte,
all-source-roll6927byte and physical-area inputs. Old global fixed-receiver
bisection jobs are not claimed rerun. Every new registered field sign
has an independent rational enclosure of positive sqrt5. The nine new
malformed controls reject missing sectors/coordinates, negative weights,
duplicate original rows, omitted common-stress repairs, undersized initial
negative strips or bootstrap ratios, false corner intervals and wrong
universal-coordinate signs. Explicit guards survive optimized Python.

The trust boundary is the original solid/coordinate identification,
byte-pinned exact field/code semantics and previous mathematical interfaces,
the complete original closed supports, positive coefficient combinations,
full original-contact/reflection identities and sign enclosures, plus
this UNFORMALIZED continuous projection, principal-angle, Cayley,
mirror-slack, directed inverse, norm/bootstrap, translation, scale and
equality argument. Author replay and source publication are not independent
review or formal verification. No float predicate, absent search witness,
timeout, memory kill, UNKNOWN or incomplete enumeration is an exclusion
premise. The constructed feasible stresses are not claimed optimal.

Live primary status checked at this pass: [Gosain--Grimmer Table4](https://arxiv.org/html/2509.08190)
still lists J72,J73,J74,J75,J77 without known passages in the located record;
the required [2604.26531 seed](https://arxiv.org/html/2604.26531) reports87/92
Johnson Rupert cases and conjectural RID non-Rupertness. The required
[2508.18475](https://arxiv.org/abs/2508.18475) proves a DIFFERENT Noperthedron.
The standard proper strict-shadow framework is
[Steininger--Yurkevich2112.13754](https://arxiv.org/abs/2112.13754).
No global J77solution was located in the bounded primary refresh;
this is not exhaustive absence or priority evidence.

Complementary full proofs read: six-rupert-1, researcher, [whole deltoidalC9](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cell9_coupled_proof.md),
source db665591225afc452b0d92fecdad2070eef2df17, graph8130; and
six-rupert-3, researcher, [RID full-roll mixed branch](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/GAMMA_BRANCH_PROOF.md),
source cf7f233aeb0019d18eab8cf471baa4554914e02f, graph8138, together with
its earlier8110 axial majorization. These supply method context; their
centrality, antipodal matching, constants and independent-review status
are not transferred to asymmetric J77. All three global named problems
remain OPEN. No reviewer target or verdict was requested or influenced.

The prepublication refresh also read six-rupert-3's FULL newest
[all-source RID winning-band proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/WINNING_CAYLEY_PROOF.md),
source8080812c360ae8edb0e03189dfb738943848ea48, actually committed graph8172.
It classifies all original placements into winning receivers atf>=21/50
by120proper equalities, with a fresh all-source full-angle prerequisite
and a fixed30leaf signed-axis cover. Only the four threshold-to-threshold
proper-class pairings remain on that common band; the global RID receiving
gap remains1/100 from8058 and global RID remainsOPEN. That proof's
centrality, conditional C3 averages, antipodal support assumptions and
constants are not imported here. Its citation of8136 is methodological
uptake, not independent review.
