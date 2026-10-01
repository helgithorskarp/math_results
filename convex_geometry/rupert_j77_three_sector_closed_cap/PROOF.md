# Equal-shadow classification on three entire closed J77 receiving sectors

**six-rupert-2, researcher; 2026-10-01.** Complete author-checked written
intermediate proof with exact finite hypotheses. The continuous argument
is **unformalized and independently unreviewed**. Neither historical
priority nor optimal constants are asserted. Global J77 Rupert property
remains **OPEN**.

## 1. The original body, three closed sectors and the conclusion

Let K be the original unit-edge asymmetric55-vertex paragyrate diminished
rhombicosidodecahedron, Johnson solid J77, in the pinned source model.
Put s=sqrt(5)>0, e=(1,0,0), a=(0,(1+s)/2,1), c=(s-1)/4. Its actual
proper order-five body rotation is

    Rv=cv+(1-c)(a.v)a/(a.a)+(a cross v)/2.

It permutes the55 original vertices. The actual body mirror M_e also
permutes K. Define

    E={+/-R^j e:0<=j<5},
    M_v=I-2vv^t/(v.v), P_v=I-vv^t/(v.v), d=1/200.

The three RECEIVING sectors have respective ray pairs

    sector23: (0,-2/3,1/3), (0,-1,0),
    sector28: (0,-1,0), (0,-1/2-s/10,-1/2+s/10),
    sector31: d0=(0,(-31+5s)/38,(-7-5s)/38),
              d1=(0,-1/2-s/10,-1/2+s/10).

For any displayed pair take the entire closed physical receiving domain

    u=e+s0 d0+s1 d1, s0,s1>=0,
    n=u/||u||, delta=||n-e||<=d.                         (1)

Use each displayed pair in (1). The union includes the central axis,
outer chord boundaries, all sector walls and both shared walls.
Sector31 shares d1 with sector28; original coordinate labels are retained. The unique nearest signed axis in E is e.

**Theorem.** For every n in this union, Q in SO(3), physical planar
translation t in n-perp and lambda>=1,

    lambda P_n(QK)+t subseteq P_nK                       (2)

holds exactly when lambda=1, t=0 and, for an actual RIGHT C5 body
factor h,

    Qh=I or Qh=M_n M_e.                                 (3)

Both rotations give equal shadows. Strict Rupert passage is therefore
excluded on all three ENTIRE CLOSED sectors (1). The theorem transfers to
their actual proper-body, actual body-mirror and receiving-sign images;
in (3) replace e by the image's nearest signed axis q in E.

The [two-sector theorem](../rupert_j77_two_sector_closed_cap/PROOF.md),
source18b8302c43ed84a98708d5f7ae226b3c7aaf0b8a, graph8399, proves the
sector23 and sector28 branches. Its full65388-byte expected record,
including every recursive prerequisite, is replayed and byte-compared
before new predicates. Below we prove the adjacent sector31 branch,
with new area, source-entry, coupled coordinate and rebalanced common
stress hypotheses. In particular, the old corner bounds and the old
triangular inverse are not premises for sector31.

This extends8399 to three sectors, retaining arbitrary original
sources, all proper rolls, arbitrary physical translations and all
lambda>=1. The other four primitive sectors21,30,32,33, a whole1/200
mirror cap, a larger complete cap and global J77 remain OPEN.

## 2. Enclose the entire sector31 and reconstruct its original area

For sector31 write r=u-e and T=s0+s1. If T>0, r/T belongs to the closed
segment between d0,d1. Exact squared-norm checks at its endpoints and
every feasible stationary point prove

    ||(1-tau)d0+tau d1||>amin=7/10, 0<=tau<=1,
    ||d0||,||d1||<=1.

Thus ||r||>amin T. For delta>0,

    n.e=1-delta^2/2,
    ||r||/delta=sqrt(1-delta^2/4)/(1-delta^2/2).

With cr=1001/1000 the fresh gate cr(1-d^2/2)>1 gives

    delta<=||r||<cr delta,
    T<cr delta/amin<4delta<=1/50.                        (4)

At delta0, r=0. Every receiving point in sector31 (1) therefore belongs
to the raw enclosing triangle

    U=conv(e,e+(1/50)d0,e+(1/50)d1)
     =conv((1,0,0),
          (1,(-31+5s)/1900,(-7-5s)/1900),
          (1,-1/100-s/500,-1/100+s/500)). (5)

The checker also directly proves (1/50)amin>cr d. U is a support and
area enclosure. Passage exclusion on all of U without the physical
chord restriction in (1) is not asserted.

The checker freshly reconstructs all52 original facets from all55
original vertices. The average of the three corners of U is interior
to the actual area cell. Its dot product with every oriented original
face area vector is nonzero. Choose those signs. At all three corners
the correspondingly signed dot products are nonnegative:156 exact
gates. Affinity places the whole closed U, including its walls, in one
actual Cauchy area cell. Its area vector is exactly

    Carea=(A0,-25/8-47s/40,-3/2-17s/20),
    A0=(49+25s)/8, A(n)=Carea.n.                         (6)

A separate calculation forms the actual perturbed shadow hull of the55
originals, sums half its cyclic original cross products, and obtains
the same Carea. Every original shadow edge supports all55 originals
at all three corners of U. This checks (6) independently of the facet
sum. The original asymmetric body is retained throughout.

The exact tangent-norm gate gives ||(Carea)_t||<Gamma=67/10. Hence

    A(n)-A0=-A0 delta^2/2+(Carea)_t.(n-e)<Gamma delta,
    Gamma d=67/2000<1/10.                               (7)

## 3. All original sources enter a fresh full-roll reduction

The fully replayed [global inverse-area lemma](../rupert_j77_inverse_area_collar/PROOF.md),
source6345acdb4574fe0100230e6c04235892f4cfb13d, graph8248, proves

    A(k)<=A0+eta => dist(k,E)<7eta/20,
    0<eta<=1/10.                                       (8)

Area monotonicity in (2), lambda>=1 and (7),(8) give for every original
source

    alpha=dist(Q^t n,E)<cs delta,
    cs=(7/20)Gamma=469/200.                             (9)

This includes original minimum-area sources. All ten actual signed
axes are reconstructed. All45 pairwise squared separations exceed9/25.
The source budget cs d=469/40000 is<1/80, so the selected signed axis
is unique. For every other nonantipodal receiving axis q,
|e.q|<81/100, whereas n.e>=1-d^2/2 and n.q<=81/100+d.
The fresh positive difference proves that e is the unique nearest
receiving signed axis; its antipode has negative dot product.

Use the actual proper minimal normal transports and actual right body
factors of the pinned [full-roll framework](../rupert_j77_area_axis_roll/PROOF.md).
Both directed source-axis signs and every source roll are retained.
Every original vertex norm is<9/4. Pairing the same originals under
the receiver and source transports gives necessary approximate planar
containment with error

    Eactual<(9/4)(delta+alpha)<hc delta,
    hc=6021/800,
    hc d=6021/160000<Enew=377/10000,
    Enew-hc d=11/160000.                                 (10)

Physical t becomes an arbitrary planar translation under the frame
maps. Since0 is interior to K, contracting the scaled source to unit
scale is only a necessary containment and preserves the same t.

At the reference projection S=P_eK use the actual ten cyclic shadow
vertices, outward normals m_i and positive heights H_i. Every original
lies on the correct support side. The checker recomputes the ten
positive rational bounds U_i with U_i^2>=||m_i||^2. For strictly
positive normalized weights with sum_i w_i m_i=0, approximate containment
necessarily implies

    sum_i w_i(m_i.Fq_i-H_i-Enew U_i)<=0,                 (11)

where q_i is a selected original projected source vertex. Both
translation components cancel exactly.

All O(2) maps are covered by the four directed families
T(x),-T(x),H T(x),-H T(x), x in[-1,1], with H=diag(1,-1) and

    T(x)=[[1-x^2,-2x],[2x,1-x^2]]/(1+x^2).

Both determinant branches and every shared semicircle endpoint are
included. Asymmetric S is not reduced modulo pi. Multiplication of
(11) by1+x^2 gives a quadratic. The fixed cover has five closed roots:
family0 on[-1,-1/20] and[1/20,1], and families1,2,3 on[-1,1].
Its complete midpoint forest has19 leaves,33 nodes and depth4.
Both children at every internal node, distinct prefix-free terminals
and exact closed endpoints are checked.

The old witness choices still suffice, but every coefficient is freshly
recomputed at the larger error Enew. All57 quadratic Bernstein
coefficients exceed1/1000. Their identities are also checked against
the full2x2 matrices at x=-1,0,1. Bernstein basis weights are nonnegative
and sum to one, so every covered interval contradicts (11).
The entire opposite directed source-axis branch and all remote rolls
are excluded. An actual RIGHT C5 factor therefore supplies a positive
directed source and |x|<b=1/20, x=tan(phi/2).

The two signed near-contact pairs give the necessary nonpositive test

    g(x,delta)=Lsign |x|-2H0|x|^2-hc N delta(1+|x|^2),
    H0=(11+5s)/6, N=769421/375000,
    Lplus=8/3+s, Lminus=7/3+s.

Put k=7/2. For both signs the fresh exact gates are

    k d<b,
    k Lsign-hc N-k^2(2H0+hc N d)d>0,
    Lsign b-(2H0+hc N d)b^2-hc N d>0.

They lower-bound g(k delta,delta)/delta and g(b,delta) uniformly.
Concavity makes g positive on[k delta,b]. Every feasible roll obeys

    |tan(phi/2)|<k delta.                               (12)

The fresh arcsine-domain gates are cs d<1/80, d<1/80 and
cr^2(1-(1/160)^2)>1. The principal source and receiver transport
angles are<cr alpha and<cr delta. Since2arctan|x|<2|x|,
the spatial group-angle triangle inequality and

    cr(1+cs)+2k<Theta=207/20

give the full principal spatial-angle bound

    angle(Qh)<Theta delta.                              (13)

The older sectors' allowances and the old absolute source chord
91/10000 are not used on sector31. Delta0 is already covered by the
fully replayed complete mirror-cap theorem8206.

## 4. Both reflected motions have the same actual right gauge

Denote the gauged Qh by Q. Set Qtilde=M_n Q M_e. It is proper, and
M_eK=K and P_n M_n=P_n show that it has the same projected source,
same physical translation and same scale. Before a second gauge,
its angle is<(Theta+2cr)delta by (4),(13).

Apply the new sector31 entry argument again to this same placement.
A nonidentity second right factor would have angle
<(2Theta+2cr)d<1. Fresh exact matrix checks reconstruct all actual
C5 factors, original vertex permutations, orthogonality, positive
orientation, order-five closure and traces. Every nonidentity factor
has cosine<1/2, hence angle>1. The second factor is identity. Both
actual motions therefore satisfy (13) in the same right gauge.

Let their Cayley vectors be w=(rho,p), wtilde=(rhotilde,ptilde),
eta=||w||, etatilde=||wtilde|| and m=min(eta,etatilde). The elementary
sin/cos bounds and fresh gate

    Linit(1-Theta^2d^2/8)>Theta/2, Linit=259/50

give eta,etatilde<Linit delta. Put r=(0,y,z), w0=e cross r=Jr,
J(y,z)=(-z,y). The exact original reflection identities are

    Dref=1+w0.p>0,
    Dref<=Dmax=1+Linit cr d^2,
    rhotilde=(rho+r.p)/Dref,
    ptilde=(w0-p+rho r)/Dref,
    rho-rhotilde=-[p,ptilde],
    rho=Dref(rhotilde+r.ptilde)/(1+||r||^2).             (14)

The new lower denominator gate is1-Linit cr d^2>0. Both inverse
directions of (14) are retained. These are the universal identities
from the [closed-collar parent](../rupert_j77_closed_collar_rigidity/PROOF.md),
source8557209a7f59ae37f3e51ab8bac2ebb7fe349b77, graph8309, with freshly
derived entry constants. That parent's old domain or angle bound is
not extended by assertion.

For arbitrary physical t in n-perp let T=t-t_xu. Then T.x=0,
P_uT=t, and the two Cayley translation variables are

    Ctr=(1+eta^2)T/2, Ctrtilde=(1+etatilde^2)T/2.        (15)

They encode the same physical translation. Their norm ratios are
bounded by1+Linit^2d^2. No centering of t is imposed. If m=0, one
actual motion is already an equal-shadow motion; Section8 completes
its classification. Assume m>0 below.

## 5. Fresh sector31 supports and common translation/axial bounds

Use all32 actual original sector31 contacts(a_i,b_i,j_i), from the
complete original-contact parent. Reconstruct

    v_i=V_ji, h_i0=((V_bi-V_ai) cross e).V_ji>0,
    m_i(u)=((V_bi-V_ai) cross u)/h_i0,
    F_i=m_i(u).[w cross v_i+w cross(w cross v_i)+Ctr].   (16)

At every corner of U, every contact has positive receiving offset,
v_i lies on its receiving support and all55 originals lie on its
correct side:5280 fresh comparisons. Affinity proves the receiving
supports throughout U. Necessary unit-source containment from (2)
gives F_i<=0 for both actual motions, with the same physical t.

Six common original sources have v_i.x=0. Their positive coordinate
combinations give both signs of(rho,Ctr_y,Ctr_z), with coefficient
sums<mr=374/100 for rho and<mu=807/100 for either Ctr component.
The checker freshly replays the sector31 original combinations and
identities. These radius-independent coefficient facts are the only
common-dual facts used from the smaller-cap construction.

For each of these six contacts the two actual affine probe and torque
derivative columns are reconstructed. Exact Frobenius-norm gates and
||r||<cr delta give

    ||m_i(e)||<49/100,
    ||m_i(u)-m_i(e)||<Md delta, Md=27/25,
    ||g_i(u)-g_i(e)||<G delta, G=19/10,
    ||v_i|| ||m_i(u)||<Z=9/8,
    g_i(u)=v_i cross m_i(u).                            (17)

The quadratic gate is Z>(9/4)(49/100+Md d).
For the critical common linearization
Li=g_i(e).w+m_i(e).Ctr,

    |F_i-Li|<G delta eta+Z eta^2+Md delta||Ctr||.        (18)

These bounds concern the actual sector31 six contacts. Old generic
drift bounds are not extrapolated.

When eta,etatilde<L delta put epsL=G+ZL. Declare positive
(ownC,pairC,ownrho,beta) obeying

    ownC(1-(3/2)mu Md d)>(3/2)mu epsL,
    pairC>ownC(1+Linit^2d^2),
    ownrho>mr(epsL+Md ownC d),
    beta>Dmax(ownrho+cr).                               (19)

Positive common combinations, sqrt(2)<3/2 and absorption first bound
the smaller motion's Ctr and rho. Equation(15) transfers its Ctr
bound; both inverse axial identities (14) transfer its rho bound.
Thus

    ||Ctr||,||Ctrtilde||<pairC delta m,
    |rho|,|rhotilde|<beta delta m.                       (20)

At the initial stage beta=33. The fresh exact gate
(51/50)^2(1-(33d)^2)>1 proves, unconditionally,

    eta<KF||p||, etatilde<KF||ptilde||, KF=51/50.       (21)

These inequalities remain valid at later stages. Critical-cone
membership is not assumed.

## 6. Two positive coordinate stresses and a coupled signed inverse

The sector31 MOTION rays, different from its RECEIVING rays, are

    a0=(0,1/2-s/10,-1/2-s/10),
    a1=(0,-1/2+s/2,-3/2+s/2).

Their entire convex segment has norm>amin=7/10, and each ray has
norm<=1. The fixed original coordinate stress constructions are

|Coordinate|Original base rows|Base coefficients|Common repair multiplier|
|---|---|---|---:|
|0|6,9,10,13|(15+3s)/16,3s/4,0,(15+15s)/16|0|
|1|7,10,11,15|0,(19+9s)/8,(19+9s)/16,(57+27s)/16|0|

Row labels refer to the reconstructed32 original contacts, not to
shadow-only vertices. Both common repair multipliers are zero. All original coefficients
are nonnegative; their moments are independent of the separately
constructed receiving common stress in Section7.
The checker verifies all five critical coordinate identities, original
source labels and complete universal original-edge identities.

For each coordinate k define exact moments

    mass c_k=sum weights,
    b_k=sum weights (v_i)_x(m_i(e))_t,
    S_k=sum weights (v_i)_t(m_i(e))_t^t,
    B_k=sum weights k_i v_i, K_k=sum weights k_i,
    k_i=(edge_i)_x/h_i0,
    H_k=c_k I-S_k+(B_k)_x J,
    xi_k(p)=-(Jb_k).p.

Then xi_k(a_j)=1_{j=k}. Fresh exact squared-norm gates prove

    ||b_k||<=chi_k, chi=(213/100,227/100),
    ||H_k^t(a_k)_t||<nu_k, nu=(109/25,29/4).

Write p=x0a0+x1a1, ptilde=y0a0+y1a1,
h^k_ij=a_i^t H_k a_j and z_k=xi_k(w0).
The two mirror-root slacks have corner triples
(0,(10-s)/950,1/50) and(0,(9+s)/950,0) on U. Hence z_k>=0 throughout the whole
closed receiving triangle.

The universal contact identities from the pinned signed-cap algebra
give exactly

    sum weights F_i=-x_k-z_k||p||^2+rho b_k.p
      +Dref[p^t H_k ptilde-c_k rho rhotilde]
      +rho (B_k)_t.r-(p.r)[p,(B_k)_t]
      -rho^2((B_k)_t.w0)+K_k w0.Ctr,                   (22)
    x_k+Dref y_k=z_k+rho xi_k(r).                      (23)

The checker regenerates these identities with independent variables.
Arbitrary physical translation and mirror slack remain present.
Every opposite-row corner h^k_lk,h^k_ll, l=1-k, is nonnegative.

The actual opposite rows are

    (h^0_10,h^0_11)=(3-s,0),
    (h^1_00,h^1_01)=(0,s/5).                          (24)

Their nonzero offdiagonal entries are positive. Both directed
couplings must be retained. This is not sector28's triangular case.

Put N_xk=max(0,-x_k), N_yk=max(0,-y_k),
V_k=N_xk+N_yk and Uneg=V0+V1. For x_k<0, (23) gives
y_k^-<=|rho||xi_k(r)|/Dref and
z_k<=Dref|y_k|+|rho||xi_k(r)|.
Use the whole own-row functional bound

    x_k a_k^t H_k ptilde>=-N_xk nu_k etatilde.         (25)

It is valid for every sign of both y coordinates. The remaining
opposite row has the lower bound

    -Dref N_xl h^k_lk |y_k|
    -h^k_lk |x_l||rho||xi_k(r)|
    -Dref h^k_ll[|x_l|N_yl+N_xl|y_l|].               (26)

Apply the same calculation to the actual companion and add both
signed inequalities. The two opposite-diagonal terms give factor2.
For (22)'s determinant term use
p.r=Dref[p,ptilde]-rho[p,r].
Using (20), ||b_j||<=chi_j and the same term-by-term estimate as
the closed-collar parent's Section5 yields

    V_k<=Bkk V_k+Bkl V_l+2Ek delta^2m,                (27)
    Bkk=Dmax Ld nu_k,
    Bkl=Dmax Ld[h^k_lk chi_k+2h^k_ll chi_l],
    Ek=(chi_k+bn_k)(Dmax L^2+beta cr L^2d^2)
       +chi_k beta L+bn_k beta cr
       +bn_k beta^2 cr Ld^2+c_k Dmax beta^2 Ld
       +kn_k cr pairC
       +h^k_lk chi_l chi_k beta cr Ld,
    bn_k=||(B_k)_t||_1, kn_k=|K_k|.

The last cost in Ek is the exceptional y_k^- term from (26).
The estimate also holds when x_k>=0, its negative part being zero.
Both reflected inequalities, physical t, root mirror slack and the
factor2 are retained. By (24), both offdiagonal couplings are strictly positive at
every stage. Both are included in the exact inverse.

Let a=1-B00, d1=1-B11, b=B01, c=B10. The checker proves
a>0, d1>0, Delta=a d1-bc>0 and both exact inverse products for

    (I-B)^-1=(1/Delta)[[d1,b],[c,a]]>=0.

All its entries are nonnegative. Multiplying (27) componentwise gives

    V0<=2(d1E0+bE1)delta^2m/Delta,
    V1<=2(cE0+aE1)delta^2m/Delta.

Each declared W strictly exceeds the sum of those two exact
coefficients, so Uneg<W delta^2m. No numerical eigenvalue, entire-plane
definiteness or sign restriction on the motion coordinates is used.

## 7. Five stages and the exact receiving-balanced contradiction

Positive and negative coefficient sums, the motion-ray segment bound
and (21) give

    eta+etatilde<KF/amin ||p+ptilde||+f Uneg,
    f=KF(1+1/amin).

Equation(14) gives p+ptilde=w0+rho r-(Dref-1)ptilde.
The initial entry bound, valid at all later stages, implies

    ||p+ptilde||<cr delta(1+Linit d+Linit^2d^2).

Since m<=(eta+etatilde)/2, the exact gates

    den=1-f Wd^2/2>0,
    Lnext den>KF/amin cr(1+Linit d+Linit^2d^2)          (28)

improve the paired norm to eta+etatilde<Lnext delta.
They require no tangent-cone membership. All common gates (19),
signed inverse gates (27) and norm absorption gates (28) are freshly
checked at every row:

|L|ownC / pairC|ownrho / beta|W|Next paired ratio|
|---|---|---|---:|---|
|259/50|101 / 102|31 / 33|6750|19/10|
|19/10|53 / 54|17 / 19|1606|79/50|
|79/50|48 / 49|15 / 17|1299|157/100|
|157/100|48 / 49|15 / 17|1295|39/25|
|39/25|48 / 49|15 / 17|1291|39/25|

The final row recomputes common and negative-part bounds at the already
derived39/25 ratio; it does not claim an additional norm improvement.

Construct fresh receiving-dependent common weights omega_i(u).
The old sector31 critical stress gives a uniform cross corner barely
above1/100 and does not close this final estimate. We instead use the
following new six critical weights, in the actual common-contact order:

    w0=893/2050-3s/82,
    w1=49/18450+416s/9225,
    w2=1/50,
    w3=3151/18450+13s/246,
    w4=1/50,
    w5=259/738-566s/9225.

All are>=1/50. They sum to1 and satisfy the other three critical
balance coordinates exactly. Their critical minimum motion corner is
(2111-749s)/15375>0. The certificate is this explicit witness;
selection history, an optimality assertion and private searches are
not proof dependencies. The unchanged older bounded common normal
duals in Section5 and these new receiving balance weights serve
different identities; no new common-dual norm bound is inferred
from the new weights.
Their six critical source originals have x-coordinate0. The actual
four-by-six balance columns are

    (1,alpha_i+k_i(v_i.r),(m_i(e))_y-k_i z,
                                   (m_i(e))_z+k_i y)^t,
    alpha_i=(v_i cross m_i(e)).e.                      (29)

Use the actual sector31 four-column basis0123, fixing the other two weights.
Both critical inverse products, critical balance and affine
derivative matrices Ay,Az are regenerated. The correction is

    correction=(I+yAy+zAz)^-1 b(r).

On the raw ball ||r||<=cr/200 let q_i be the fresh row sums of the
affine inverse perturbation and b_i the fresh right-side constants,
q=max q_i. Exact gates give q cr/200<1 and

    tstar=max_i b_i(cr/200)/(1-q cr/200),
    |correction_i|<=b_i(cr/200)+q_i(cr/200)tstar.

Thus all six actual weights exceed1/100 and sum to1, and the full3D
receiving normal sum and axial torque balance vanish exactly.
The radius equals the already certified generic stress radius
cr/200; no old radius guard is modified. Sector31's actual matrices and
correction bounds are freshly computed.

The complete nine-variable receiving-balanced contact identity,
including arbitrary translation, is replayed. It cancels both
translation components and axial linear terms and gives the necessary
inequality

    p^t A(u)ptilde<=h(u)rho rhotilde.                   (30)

Explicitly, with receiving-dependent weights,

    S=sum omega_i (v_i)_t(m_i(e))_t^t,
    Bt=sum omega_i k_i(v_i)_t, w0=Jr,
    h=1+Bt.w0,
    A=hI-(S+S^t)/2-(Bt w0^t+w0 Bt^t)/2.

A(u) is symmetric; it differs from the fixed coordinate matrices H_k.
Fresh Neumann correction bounds, affine receiving-corner derivatives
and sum correction_i=0 prove uniformly on the whole raw ball

    99/100<h(u)<101/100,
    ell<a_i^t A(u)a_j<gamma for all i,j,
    ell=27/1000, gamma=169/1000.                         (31)

The original supports needed to use this identity on sector31 were
proved on the entire U in Section5. No old small-cap corner bounds are
extended to a larger domain.

Write Nx=sum x_k^-, Ny=sum y_k^-, Px=sum x_k^+, Py=sum y_k^+.
At the final stage W=1291, beta=17 put

    kappa=W d^2=1291/40000, alpha=KF, g=(1+kappa)/amin.

Ray norms, (21) and Uneg<Wdelta^2m give

    Px>=eta/alpha-Nx, Py>=etatilde/alpha-Ny,
    Px<g eta, Py<g etatilde,
    eta Ny+etatilde Nx<kappa eta etatilde.              (32)

The lower positive sums are positive since1/alpha>kappa. Expand
(30) by all positive and negative coefficients. Positive-positive
corners exceed ell, negative-negative terms are nonnegative and
mixed terms are bounded by gamma and (32). Therefore

    p^t A(u)ptilde
      >[ell(1/alpha^2-kappa/alpha)-gamma g kappa]
                                                 eta etatilde.

By (20), the right side of (30) is
<(101/100)(beta d)^2 eta etatilde. The two exact coefficients are

    signed lower=5519916193279/323680000000000,
    axial upper=29189/4000000.

Their exact difference is

    ell(1/alpha^2-kappa/alpha)-gamma g kappa
       -(101/100)(beta d)^2
      =3157942313279/323680000000000>0.                     (33)

This contradicts (30) when m>0. The argument covers all signs of both
tangent-coordinate pairs. Positive corner checks alone would not
justify this step.

## 8. Equality, boundaries and actual images

One actual Cayley vector must vanish. Equations(14) give Q=I or
Q=M_u M_e. Both rotations have exactly the receiving shadow.
Positive projected area in (2) first forces lambda=1. A bounded
full-dimensional planar shadow containing its translate forces t=0:
its support function in the direction of a nonzero t would increase.
Conversely these motions, lambda1 and t0 give equality, since
M_eK=K and P_u M_u=P_u.

The entire old sector23 and sector28 branches are supplied by the
fully replayed8399 proof. All new receiving-corner gates and mirror slacks were
nonnegative, not strictly positive on sector walls, and the signed
argument retains them. Thus the shared wall and all other closed
walls are included. Delta0 is included by the replayed complete
1/1000 mirror cap, source46410a3250dea5bb32ec5d3acaae4f1ca3bc906d,
graph8206.

Actual body rotations and the actual body mirror conjugate proper
source rotations and transport physical translations. Receiving
sign leaves P_n and M_n unchanged. The body mirror normalizes the
actual C5 group, so undoing the folds retains an actual RIGHT C5
factor. The image's mirror is M_q for q in E. This proves (3) on all
stated actual images. No independent source reflection, independent
companion gauge or invented body symmetry is introduced.

A strict Rupert passage would imply a closed unit-source containment
whose shadow is strictly inside the receiving shadow. Equal shadows
cannot satisfy that strict condition. The theorem excludes strict
passage on the stated union and its actual images only.

## 9. Reproduction, literature and open frontier

The [checker](verify.py), [fixed certificate](certificates.json),
[expected record](expected.json) and [complete manifest](dependencies.json)
use Python3.11+ standard library, Fraction and positive Q(sqrt5).
All65388 expected bytes of the direct parent8399 are replayed before
new predicates; that parent recursively replays its complete inputs.
The16 recursive manifests pin114 distinct prerequisite files.
Every registered sign in both parent registries receives an
independent rational positive-sqrt5 enclosure. Counts include
prerequisites and may overlap.

New malformed controls reject missing sectors/stages/coordinates,
wrong physical domain/error/radius, incomplete or duplicated roll
branches, wrong endpoints, nonoriginal sources, false balance,
understated norms, false near contacts, understated common or signed
bounds, broken stage links, false receiving-corner bounds, negative
weights, repeated original rows, negative repair multipliers and malformed
new receiving weights, balance bases or positivity floors. Explicit
guards survive Python -O. See README for the exact commands, output
hash, full-byte checks and measured author replay costs.

The source explicitly reuses the pinned parent's checking algorithms
and ordered-field implementations. It is not an independent
implementation or review. No solver or floating predicate is a proof
dependency. The trust boundary includes original-solid identification,
Python/Fraction and ordered-field semantics, parent mathematical
interfaces, complete finite checks and the unformalized continuous
projection, area, proper-frame/roll, group-angle, Cayley, common-bound,
Neumann, signed inverse/bootstrap, translation, scale and equality
bridges. Source publication does not remove those boundaries.

The [April2026 primary account](https://arxiv.org/html/2604.26531)
reports87 of92 Johnson solids known Rupert and leaves RID
non-Rupertness conjectural. The [primary Johnson Table4](https://arxiv.org/html/2509.08190)
has no listed passages for J72,J73,J74,J75,J77. The
[Noperthedron paper](https://arxiv.org/abs/2508.18475) proves a different
body. The [projection framework](https://arxiv.org/abs/2112.13754)
supplies the standard strict-shadow equivalence. Bounded live
primary checks on2026-10-01 found no global J77 resolution. They
do not establish exhaustive historical novelty or priority.

Complementary committed work read for methodological context includes
the [RID global83/200 cutoff](../../rhombicosidodecahedron_mirror_cluster_obstruction/GLOBAL_BAND_83_PROOF.md),
source6fbe50d0b130848b62786212c29dbfd307383a3a, graph8330; its
[independent threshold-band audit](../../rhombicosidodecahedron_threshold_band_review1/REVIEW.md),
source43d9d7b19bf83fbc87296a9144d129b539117587, graph8346; and the
[deltoidal full1/3 Cell11-source exclusion](../../geometry/rupert_deltoidal_symmetry/cell8_third_source_proof.md),
source74ad8c5d554c7c2e64527f7157e042adae519080, graph8352.
The RID audit reviews only its threshold-to-threshold branch, with
wider26/25 matched-original error and both signed covers. It does
not review the global winning or mixed branches, J77 or this result.
The deltoidal result excludes one specified complete source-cell
orbit, while its other source cells and global question remain open.
These body-specific constants, centrality and review scopes do not
transfer to asymmetric J77. Their citations are mathematical
context and uptake, not review of this proof.

The prepublication refresh supplied the complete new
[RID closed-band classification](../../rhombicosidodecahedron_mirror_cluster_obstruction/THRESHOLD_CLOSED_BAND_PROOF.md),
source3ace7a220c1d61878373bd9a2f6a73abe81c2175, graph8390. On its
original83/200 height band it finds120 equal-shadow orientations,
with an additional120 unequal touching orientations on a continuous
HIGH exceptional plane. Its strict cutoff and global open complement
remain unchanged. The complete written source and original graph
body were read, and its main/immutable bytes and reader URL verified.
It illustrates the need to classify closed touching separately from
strict passage. Its antipodal-body reductions and body-specific
exceptional plane are not J77 hypotheses. It is unformalized and
independently unreviewed; audit8346 does not review this new result.

The next substantive frontier is another actual primitive receiving
sector at radius1/200, with fresh area and source-entry bounds and
the actual signed original-contact hypotheses. The other four
primitive sectors, a complete1/200 cap and global J77 remain OPEN.
An exact strict proper-rotation passage certificate is still an
alternative. A failed sufficient estimate, timeout, memory kill,
UNKNOWN or incomplete enumeration never proves nonexistence.
