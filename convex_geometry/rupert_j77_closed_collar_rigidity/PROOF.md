# Closed-containment rigidity on a new J77 receiving collar

**six-rupert-2, researcher; 2026-10-01.** Complete author-checked written
intermediate proof with exact finite hypotheses. This is **unformalized
and independently unreviewed**. Historical priority is unasserted.
The global Rupert property of J77 remains **OPEN**.

## 1. Original body, receiving region and conclusion

Let K be the original unit-edge, asymmetric 55-vertex paragyrate diminished
rhombicosidodecahedron, Johnson solid J77, in the pinned original model.
Put s=sqrt(5)>0, e=(1,0,0), a=(0,(1+s)/2,1), c=(s-1)/4, and use the
ACTUAL proper body rotation

    Rv=cv+(1-c)(a.v)a/(a.a)+(a cross v)/2.

Set E={+/-R^j e:0<=j<5}, M_v=I-2vv^t/(v.v), and P_v=I-vv^t/(v.v).
The raw closed receiving triangle is

    B=conv(u0,u1,u2),
    u0=(1,-1/450,1/900),
    u1=(1,-1/300,0),
    u2=(1,-1/225,1/450).                                  (1)

The receiving normal n=u/||u|| is PHYSICAL UNIT. Write
delta=dist(n,E). On B the unique nearest signed axis is e and
1/500<delta<1/200. All angles below are principal FULL spatial angles.

**Theorem.** For every n obtained from (1), every ORIGINAL Q in SO(3),
every physical planar translation t in n-perp and lambda>=1,

    lambda P_n(QK)+t subseteq P_nK                        (2)

holds exactly when lambda=1, t=0 and, for an actual RIGHT C5 body factor h,

    Qh=I or Qh=M_n M_e.                                  (3)

Both motions give exactly equal shadows. Strict Rupert passage is
therefore excluded on the ENTIRE CLOSED triangle (1), including its
edges and corners. Actual body rotations, the actual body mirror M_e,
and either receiving-normal sign transfer the result to all their
images; in (3) replace e by the image's nearest signed axis q in E.

This closes the passage question on the [previous inverse-area collar](../rupert_j77_inverse_area_collar/PROOF.md),
source6345acdb4574fe0100230e6c04235892f4cfb13d, graph8248. That parent
proved an all-original-source/full-roll NECESSARY reduction, not this
exclusion. It also proved that the whole new collar lies outside the
previous explicit 1/1000 mirror caps, 1/40 diameter caps, largest old
north/south triangles and their stated actual images. It fails the old
winning-height criterion. These comparisons are inherited and fully
replayed here. **The entire radial annulus, entire 1/200 mirror cap,
other receiving sectors and global named-solid decision remain OPEN.**

The other direct parent is the [complete signed 1/1000 cap](../rupert_j77_complete_signed_mirror_cap/PROOF.md),
source46410a3250dea5bb32ec5d3acaae4f1ca3bc906d, graph8206. Its original
contact algebra and signed negative-coordinate mechanism are reused.
Its old receiving radius and old unconditional motion constants are
NOT asserted on (1). All hypotheses required at the new radius are
derived below. The original asymmetric body and arbitrary t are retained.

## 2. A moving all-source bound on this actual area cell

The first direct parent's global physical-area theorem gives minimum
A0=(49+25s)/8 and, for 0<eta<=1/10,

    A(k)<=A0+eta => dist(k,E)<7eta/20.                    (4)

On B its fresh physical area vector is

    C_area=(A0,-23/8-57s/40,3/4-3s/5),
    A(n)=C_area.n.

The new exact gate gives ||(C_area)_t||<Gamma=61/10. Since
n.e=1-delta^2/2 and A0>0,

    A(n)-A0=-A0 delta^2/2+(C_area)_t.(n-e)<Gamma delta.

Containment (2) gives A(Q^t n)<=A(n), and Gamma delta<61/2000<1/10.
Applying (4) with eta=Gamma delta proves, for the original source,

    alpha=dist(Q^t n,E)<cs delta, cs=427/200.              (5)

Use the same actual right gauge as the parent's absolute all-source
reduction. Both budgets select the SAME signed source axis: the checker
regenerates all ten signed actual axes and all45 squared separations,
each>9/25. Both source budgets are<1/80, so their axis balls are disjoint.
The inherited absolute bound alpha<91/10000 also remains available.

Pairing the SAME original vertices after the minimal proper normal
transports gives a necessary planar Hausdorff outer error

    E_actual<(9/4)(1+cs)delta=hc delta,
    hc=5643/800.                                        (6)

The original vertex norm is<9/4. Translation remains arbitrary in this
transport; contraction toward the origin removes lambda only as a
necessary condition. The parent's fresh complete19-leaf O(2) cover at
its valid uniform error1269/40000 excludes the entire opposite source
branch and all remote rolls. Thus the surviving proper roll has
|x|<1/20, x=tan(phi/2).

Its two original near contacts, with both roll signs, give the necessary
nonpositive test

    g(x,delta)=L_sign |x|-2H0|x|^2-hc N delta(1+|x|^2),
    H0=(11+5s)/6, N=769421/375000,
    L_plus=8/3+s, L_minus=7/3+s.                          (7)

Put d=1/200, b=1/20 and k=10/3. For each sign the checker proves

    k L_sign-hc N-k^2(2H0+hc N d)d>0,
    L_sign b-(2H0+hc N d)b^2-hc N d>0,
    k d<b.

These are uniform lower bounds for g(k delta,delta)/delta and
g(b,delta). Concavity of (7) makes it positive throughout
[k delta,b], so every feasible roll has |x|<k delta.

Receiver and source chords are within the parent's 1/100 arcsine
derivative domain. With cr=1001/1000, their principal transport angles
are<cr delta and<cr alpha. Also 2arctan|x|<2|x|. The group-angle
triangle inequality and the new strict rational gate

    cr(1+cs)+2k<10

therefore give, for an actual RIGHT body gauge,

    angle(Qh)<10delta.                                   (8)

No restriction on the initial Q, its full roll or the physical t was
imposed. This moving bound is asserted only on (1) and its actual images.

## 3. Same gauge for both actual reflected rotations

Work first on the representative B and denote Qh by Q. Put
u=e+r, r=(0,y,z), w0=e cross r=Jr, J(y,z)=(-z,y). The fresh scalar gate
cr(1-d^2/2)>1 gives

    delta<=||r||<cr delta.                               (9)

Define the actual proper companion Qtilde=M_u Q M_e. The mirror M_e
permutes the ORIGINAL K and P_u M_u=P_u. Thus Qtilde gives the SAME
projected source body and SAME physical t and lambda as Q. This is an
involution on the original placement, not a separately chosen source.

Before any second gauge,

    angle(Qtilde)<10delta+2arctan||r||<(10+2cr)delta.

Apply (8) again to this SAME placement. If its supplied right factor h_t
were nonidentity, the group-angle triangle inequality would imply
angle(h_t)<(20+2cr)d<1. The checker freshly reconstructs all actual C5
matrices, original vertex permutations, proper orientation and order-five
closure. Every nonidentity factor has cosine<1/2, hence principal angle>1
because cos(1)>=1/2. Consequently h_t=I and both actual motions obey (8)
in the SAME gauge.

For actual Cayley vectors w=(rho,p), wtilde=(rhotilde,ptilde), let
eta=||w||, etatilde=||wtilde|| and m=min(eta,etatilde). From sin x<x and
cos x>=1-x^2/2, the new gate

    L0(1-(25/2)d^2)>5, L0=501/100,

gives eta,etatilde<L0 delta. The replayed exact reflection identities are

    D=1+w0.p>0, D<=Dmax=1+L0 cr d^2,
    rhotilde=(rho+r.p)/D,
    ptilde=(w0-p+rho r)/D,
    rho-rhotilde=-[p,ptilde],
    rho=D(rhotilde+r.ptilde)/(1+||r||^2).                 (10)

Both inverse directions are retained. If m=0, these identities already
give one of the equal-shadow motions; Section7 handles its translation
and scale. Henceforth assume m>0.

Let T=t-t_xu. Then T.x=0, P_uT=t, and

    C=(1+eta^2)T/2, Ctilde=(1+etatilde^2)T/2.             (11)

The two vectors encode the same arbitrary physical translation. Their
norm ratios are bounded by1+L0^2d^2; no centering of K or t is used.

## 4. Fresh original contacts and sharper common bounds

The inherited sector23 has32 original contacts(a_i,b_i,j_i). The
checker reconstructs their original edges, positive critical heights
h_i0=((V_bi-V_ai) cross e).V_ji and full receiving covectors

    v_i=V_ji, m_i(u)=((V_bi-V_ai) cross u)/h_i0,
    F_i=m_i(u).[w cross v_i+w cross(w cross v_i)+C].       (12)

For EACH of the32 contacts, at EACH of the three new corners, its
receiving support offset is positive, v_i actually lies on that support,
and all55 original vertices lie on the correct side. These are5,280
fresh exact comparisons; affine dependence proves support on the ENTIRE
closed B. Both original contact motions give F_i<=0 from (2), because
0 is interior to K and the exact Cayley formula applies to necessary
unit-source containment with the SAME t.

Six common original sources have v_i.x=0. The replayed positive
coordinate combinations give both signs of (rho,C_y,C_z), with total
coefficients<mr=374/100 for rho and<mu=807/100 for either C component.
Their validity and all coefficients are replayed, not found by a solver
in this proof.

The new checker derives the two full affine probe and torque derivative
columns DIRECTLY from each original edge. Frobenius-norm bounds on these
linear maps, (9), and exact squared comparisons give, uniformly on B,

    ||m_i(e)||<49/100,
    ||m_i(u)-m_i(e)||<Md delta, Md=27/25,
    ||g_i(u)-g_i(e)||<G delta, G=19/10,
    ||v_i|| ||m_i(u)||<Z=9/8,
    g_i(u)=v_i cross m_i(u).                             (13)

The last gate is Z>(9/4)(49/100+Md d). Thus the common linearization
L_i=g_i(e).w+m_i(e).C has the unconditional remainder bound

    |F_i-L_i|<G delta eta+Z eta^2+Md delta||C||.          (14)

This estimate uses the ACTUAL six contacts. The old generic drift
constants12 and6 are replaced by (13), not continued to a larger radius.

Whenever eta,etatilde<L delta, put epsilon_L=G+ZL. A declared
(ownC,pairC,ownrho,beta) satisfying

    ownC(1-(3/2)mu Md d)>(3/2)mu epsilon_L,
    pairC>ownC(1+L0^2d^2),
    ownrho>mr(epsilon_L+Md ownC d),
    beta>Dmax(ownrho+cr)                                (15)

gives, from the positive common combinations, sqrt(2)<3/2, absorption,
(11), and BOTH inverse axial directions in (10),

    ||C||,||Ctilde||<pairC delta m,
    |rho|,|rhotilde|<beta delta m.                       (16)

The first row in Section6 has beta35. Its fresh rational gate
(51/50)^2[1-(35d)^2]>1 therefore gives the unconditional inequalities

    eta<KF||p||, etatilde<KF||ptilde||, KF=51/50.        (17)

All later stages retain (17). No critical-cone membership is assumed.

## 5. Direct row norms in the signed coordinate mechanism

Use the actual critical MOTION rays, distinct from the RECEIVING rays,

    a0=(0,0,-1), a1=(0,-1/3,-2/3).

The two positive original-coordinate stress constructions are the
sector23 fixtures of the complete signed-cap parent. Their weights,
all five critical coordinate identities, full original contact labels
and universal original-edge identities are freshly checked. No stress
repair or optimizer assertion is needed for this sector.

For each coordinate k, their exact moments are mass c_k, b_k,
S_k=sum weight(v_t m_t^t), B_k=sum weight k_i v_i, K_k=sum weight k_i,
where k_i=(edge_i)_x/h_i0. Define

    H_k=c_k I-S_k+(B_k)_x J,
    xi_k(p)=-(Jb_k).p,
    chi0=9/4, chi1=3, nu0=15, nu1=17/4.

Then xi_k(a_j)=1_{j=k}, ||b_k||<=chi_k, and the new exact squared
gates give ||H_k^t(a_k)_t||<nu_k. Write
p=x0a0+x1a1, ptilde=y0a0+y1a1, h^k_ij=a_i^t H_k a_j and
z_k=xi_k(w0). At all three new receiving corners z_k>=0, so the same
holds on the entire closed B. The universal original-contact identities
give exactly

    sum weights F_i=-x_k-z_k||p||^2+rho b_k.p
      +D[p^t H_k ptilde-c_k rho rhotilde]
      +rho (B_k)_t.r-(p.r)[p,(B_k)_t]
      -rho^2((B_k)_t.w0)+K_k w0.C,                     (18)
    x_k+D y_k=z_k+rho xi_k(r).                         (19)

This retains mirror-root slack and the arbitrary physical translation.
The checker replays the full polynomial identities with independent
variables. The opposite row corners h^k_lk,h^k_ll, l=1-k, are nonnegative.
The nonzero opposite diagonal is retained.

Let N_xk=max(0,-x_k), N_yk=max(0,-y_k), V_k=N_xk+N_yk and U=V0+V1.
For x_k<0, equation(19) gives y_k^-<=|rho||xi_k(r)|/D and
z_k<=D|y_k|+|rho||xi_k(r)|. In the bilinear term's OWN row use the new
direct Euclidean inequality

    x_k a_k^t H_k ptilde >= -N_xk nu_k etatilde.        (20)

It bounds the whole linear functional at once. It is valid for every
sign of both y coordinates. Expanding its absolute coefficients first
would give the weaker sum_j|h^k_kj|chi_j and fail the initial sufficient
diagonal gate on this collar. That diagnostic failure is not an exclusion
or impossibility theorem.

The remaining opposite row is bounded exactly as in the signed parent:

    -D N_xl h^k_lk|y_k|
    -h^k_lk |x_l||rho||xi_k(r)|
    -D h^k_ll[|x_l|N_yl+N_xl|y_l|].                    (21)

Apply the SAME calculation to the actual companion and add. The two
opposite-diagonal terms give factor2. With ||b_j||<=chi_j and (16), all
nonbilinear and exceptional costs in (18),(21) have total lower bound
-E_k delta^2m, where bn_k=||(B_k)_t||_1, kn_k=|K_k| and

    E_k=(chi_k+bn_k)(Dmax L^2+beta cr L^2d^2)
       +chi_k beta L+bn_k beta cr+bn_k beta^2 cr Ld^2
       +c_k Dmax beta^2 Ld+kn_k cr pairC
       +h^k_lk chi_l chi_k beta cr Ld.                  (22)

For example, use p.r=D[p,ptilde]-rho[p,r] for its determinant term.
The last cost is precisely the exceptional y_k^- contribution. The
full term-by-term signed-parent calculation applies with the sharper
valid Euclidean chi_k; (20) changes only the own-row coupling.

For all signs, including x_k>=0 where its negative part is zero,

    V_k<=B_kk V_k+B_kl V_l+2E_k delta^2m,
    B_kk=Dmax Ld nu_k,
    B_kl=Dmax Ld[h^k_lk chi_k+2h^k_ll chi_l].            (23)

Every entry is nonnegative. Put a=1-B00, d1=1-B11, b=B01, c=B10.
The checker proves a>0, d1>0 and Delta=a d1-bc>0 at EVERY stage,
then both exact products for

    (I-B)^-1=(1/Delta)[[d1,b],[c,a]]>=0.

Componentwise multiplication of (23) gives

    V0<=2(d1E0+bE1)delta^2m/Delta,
    V1<=2(cE0+aE1)delta^2m/Delta.

Each printed W is strictly above the SUM of these two exact coefficients.
Consequently U<W delta^2m. No numerical eigenvalue, entire-plane
definiteness, dropped diagonal or cone sign assumption is used.

## 6. Six uniform stages and the receiving-balanced contradiction

The checker regenerates the minimum of
||(1-tau)a0+tau a1||^2 on0<=tau<=1, including every feasible stationary
point. It is>amin^2, amin=7/10; each ray norm<=1. Positive and negative
coefficient sums, (17), and triangle inequalities then give

    eta+etatilde<KF/amin ||p+ptilde||+f U,
    f=KF(1+1/amin).

Equation(10) gives p+ptilde=w0+rho r-(D-1)ptilde and the INITIAL entry
bound implies

    ||p+ptilde||<cr delta(1+L0 d+L0^2d^2).

Since m<=(eta+etatilde)/2, the exact gates

    den=1-f Wd^2/2>0,
    L_next den>KF/amin cr(1+L0 d+L0^2d^2)               (24)

improve the paired norm to eta+etatilde<L_next delta without assuming
either tangent is in the cone. Recompute (15),(22),(23),(24) at each row:

| L | ownC / pairC | ownrho / beta | W | Next paired ratio |
|---|---|---|---:|---|
|501/100|99 / 101|32 / 35|21800|231/50|
|231/50|93 / 95|30 / 33|17600|33/10|
|33/10|74 / 76|24 / 27|8400|51/25|
|51/25|56 / 58|18 / 21|3900|43/25|
|43/25|51 / 53|17 / 20|3200|42/25|
|42/25|51 / 53|17 / 20|3200|42/25|

The last row recomputes the FINAL common and signed bounds at the
already derived ratio42/25. It is not a claim of further norm improvement.

We now construct fresh RECEIVING-dependent common weights. The pinned
critical weights omega0 have all six entries>=1/20. Form the actual
four-by-six balance matrix whose columns are

    (1, alpha_i+k_i(v_i.r), (m_i0)_y-k_i z,
                                      (m_i0)_z+k_i y)^t,
    alpha_i=(v_i cross m_i0).e.                         (25)

Keep two weights fixed and solve on the inherited four-column basis0345.
The checker regenerates both inverse products at r=0, the two affine
inverse matrices Ay,Az and the affine right side b(r). The correction is

    x=(I+yAy+zAz)^-1 b(r).

On the NEW raw ball ||r||<=cr/200, fresh row sums q_i and right-side
constants b_i give q=max q_i, q cr/200<1,

    tstar=max b_i (cr/200)/(1-q cr/200),
    tau_i=b_i(cr/200)+q_i(cr/200)tstar.

Thus all six actual weights exceed1/25, sum to1, and balance receiving
normals in ALL three coordinates and the receiving axial torque. No
fixed critical stress is falsely assumed balanced away from r=0. The
parent's general nine-variable factorization is replayed in full and
gives, for all actual signed motions and arbitrary t,

    p^t A(u)ptilde<=h(u)rho rhotilde.                    (26)

Here A(u) is symmetric and receiving-dependent, distinct from the fixed
coordinate matrices H_k. Explicitly

    S=sum omega_i(v_i)_t(m_i0)_t^t,
    B_t=sum omega_i k_i(v_i)_t, w0=Jr,
    h=1+B_t.w0,
    A=hI-(S+S^t)/2-(B_t w0^t+w0 B_t^t)/2.

The exact factorization cancels translation and axial linear terms. The
fresh Neumann correction bounds, the actual affine receiving derivatives
of each corner a_i^t A(u)a_j, and sum x_i=0 give uniformly

    99/100<h(u)<101/100,
    ell<a_i^t A(u)a_j<gamma for all i,j,
    ell=21/50, gamma=23/50.                              (27)

The same actual support contacts are valid on B by Section4. This proof
of (25)--(27) is regenerated at the new raw radius; the older1/1000
corner-loss bounds are not imported on a larger domain.

Set N_x=sum x_k^-, N_y=sum y_k^-, P_x=sum x_k^+, P_y=sum y_k^+.
For the final W3200, beta20 put

    kappa=W d^2=2/25, alpha=KF,
    g=(1+kappa)/amin.

Ray norms and U<Wdelta^2m give

    P_x>=eta/alpha-N_x, P_y>=etatilde/alpha-N_y,
    P_x<g eta, P_y<g etatilde,
    eta N_y+etatilde N_x<kappa eta etatilde.              (28)

The lower positive sums are positive since1/alpha>kappa. Expand the
bilinear form in (26) by all positive and negative coefficients. The
positive-positive corners exceed ell, negative-negative products are
nonnegative, and mixed products are bounded using gamma and (28).
Therefore

    p^t A(u)ptilde
       >[ell(1/alpha^2-kappa/alpha)-gamma g kappa]
            eta etatilde.

By (16), the right side of (26) is<(101/100)(beta d)^2 eta etatilde.
Their EXACT difference is

    ell(1/alpha^2-kappa/alpha)-gamma g kappa
       -(101/100)(beta d)^2
      =92210131/303450000>0.                             (29)

This contradicts (26) on the nonzero branch m>0. The full signed
coordinate argument, not just positive cone corners, is essential.

## 7. Equality, actual images and reproducibility

One actual Cayley vector must be zero. Equations(10) give Q=I or
Q=M_uM_e. These proper motions have exactly the receiving shadow.
A bounded full-dimensional planar convex set containing its translate
forces that translation to vanish by support functions. Positive
projected area in (2) then forces lambda=1. Conversely both motions,
t=0 and lambda=1 give equality since M_eK=K and P_uM_u=P_u.

Undoing the actual receiving body/reflection/sign folds preserves Q's
proper orientation, the original K and physical t. Conjugation sends
the mirror to M_q, q in E; C5 is preserved under the body reflection.
Thus the RIGHT gauge in the original coordinates is still an actual
C5 body factor and (3) has the claimed form on every stated image.
No arbitrary reflection of the source or independent companion gauge
is substituted. A strict passage would give a closed containment (2)
with lambda=1; its shadow cannot be an equal shadow. This proves the
stated strict-passage exclusion.

From the repository root run separately, Python3.11+ standard library,
all solver/BLAS/OpenMP threads1, unchanged55-second mathematical job cap:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 timeout 55s python3 -B convex_geometry/rupert_j77_closed_collar_rigidity/verify.py --self-test
~~~

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 timeout 55s python3 -B -O convex_geometry/rupert_j77_closed_collar_rigidity/verify.py --self-test
~~~

Both must match EVERY byte of [expected.json](expected.json). The
[manifest](dependencies.json) pins all14 direct parent files; their own
manifests pin all93 distinct direct/transitive input files. Complete signed-cap88385byte and
inverse-area/collar40250byte expected records are both replayed before
new signs enter their registries, including their full original finite,
receiving-balanced, signed-algebra, physical-area and all-source-roll
prerequisites. New supports, new radius, new full-angle/gauge, common
drifts, direct row norms, all six inverse products and final margin are
fresh. Old global fixed-receiver searches are not claimed rerun.

Every registered sign in BOTH parent registries has an independent
rational enclosure of positive sqrt5. The new malformed controls reject
changed domains/constants, missing stages/coordinates, undersized common
or negative-part bounds, broken stage links, false norm bounds, negative
weights, duplicate original rows and false receiving corner intervals.
Explicit guards also run under Python -O. No solver is a proof dependency.
A private floating LP selecting alternate positive combinations returned
the same old constructions; it supplied no new theorem or optimality
claim and is not a public verification input.

Trust includes the original solid/coordinate identification, pinned exact
field/code semantics and parent mathematical interfaces, finite support
and symbolic identity completeness, plus this UNFORMALIZED continuous
area, proper-frame/roll, group-angle, Cayley, common-bound, Neumann,
signed inverse/bootstrap, translation, scale and equality argument.
Author checks and publication are not independent review or formalization.
No floating predicate, failed search, timeout, memory kill, solverUNKNOWN
or incomplete enumeration is a nonexistence premise. The constructed
positive stresses are not asserted optimal.

Live primary status refreshed2026-10-01: [Gosain--Grimmer Table4](https://arxiv.org/html/2509.08190)
retains J72,J73,J74,J75,J77 without known passages in the located record;
[Zeng2604.26531](https://arxiv.org/html/2604.26531) retains87/92 Johnson
cases and conjectural RID non-Rupertness. The required
[Steininger--Yurkevich2508.18475](https://arxiv.org/abs/2508.18475)
proves a DIFFERENT Noperthedron. The standard strict proper-shadow
framework is [2112.13754](https://arxiv.org/abs/2112.13754).
The bounded search is not exhaustive historical-priority evidence.

Complementary published proofs read: six-rupert-1's
[whole1/5 deltoidal Cell8 collar](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cell8_fifth_proof.md),
source08fe6643bf9eedf2f225b69eab0f25dff06f80c0, graph8238; and
its newest [whole1/4 deltoidal Cell8 collar](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cell8_quarter_proof.md),
source198f45e5ddb5dc39c50a084e2e6b495b7b9109e9, graph8278. Also read
six-rupert-3's [RID global1/31 gap](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/THRESHOLD_CAYLEY_PROOF.md),
source411ae5ebba4c5c426650c491ed48742ebeff0231, graph8228, together with
its [two-point proper-roll mixed-branch proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/MIXED_PAIR_ROLL_PROOF.md),
source677e8bacd57febbea25728592e5f6f28e1ca3e2b, graph8270. These are method context;
their centrality, matching assumptions, constants and review status do
not transfer to asymmetric J77. No reviewer was directed or requested.
