# Only equal-shadow containment on the whole closed J77 sector23 cap

**six-rupert-2, researcher; 2026-10-01.** Complete author-checked written
intermediate proof with exact finite hypotheses. The continuous proof is
**unformalized and independently unreviewed**. Historical priority and
optimality of constants are unasserted. Global J77 Rupert property remains
**OPEN**.

## 1. Exact original body, closed domain and theorem

Let K be the original unit-edge asymmetric55-vertex paragyrate diminished
rhombicosidodecahedron, Johnson solid J77, in the pinned source model.
Put s=sqrt(5)>0, e=(1,0,0), a=(0,(1+s)/2,1), c=(s-1)/4. The actual
proper body generator is

    Rv=cv+(1-c)(a.v)a/(a.a)+(a cross v)/2.

It has order5, permutes all55 originals, and generates the actual right
C5 gauges. The actual body mirror M_e permutes K. Write

    E={+/-R^j e:0<=j<5},
    M_v=I-2vv^t/(v.v), P_v=I-vv^t/(v.v).

The RECEIVING-sector rays and the closed physical domain are

    d0=(0,-2/3,1/3), d1=(0,-1,0), d=1/200,
    u=e+s0 d0+s1 d1, s0,s1>=0,
    n=u/||u||, delta=||n-e||<=d.                          (1)

There is no prescribed source orientation, source roll, translation or
scale beyond the quantifiers below. The nearest signed axis in E is e.
The sector walls, outer chord boundary and central axis are included.

**Theorem.** For every n in (1), Q in SO(3), physical planar t in n-perp
and lambda>=1,

    lambda P_n(QK)+t subseteq P_nK                        (2)

holds exactly when lambda=1, t=0 and there is an actual RIGHT C5 body
factor h such that

    Qh=I or Qh=M_n M_e.                                  (3)

Both rotations give equal shadows. Consequently strict Rupert passage
is excluded on the ENTIRE CLOSED domain (1). The theorem transfers to
its actual proper-body, actual body-mirror and receiving-sign images;
in (3) replace e by the image's nearest signed axis q in E.

This extends the [closed receiving-collar theorem](../rupert_j77_closed_collar_rigidity/PROOF.md),
source8557209a7f59ae37f3e51ab8bac2ebb7fe349b77, graph8309. Its old
patch was the normalization of

    conv((1,-1/450,1/900),(1,-1/300,0),(1,-1/225,1/450)),

with1/500<delta<1/200. All three old vertices belong to (1), as do
their convex combinations; exact barycentric inclusion and the old
whole-patch chord bound are checked. The present conclusion covers a
whole closed sector, including directions between that patch and its
central axis, rather than only that patch. It does not assert the
entire1/200 mirror cap, other receiving sectors or global non-Rupertness.

The direct parent fixes the original contact and signed-motion algebra.
Its theorem was expressly limited to its patch. We do not extrapolate
that theorem or modify its radius. We freshly establish the missing
whole-sector entry and contact-domain hypotheses, then apply its
general algebraic argument with its unchanged certified constants.

## 2. Enclose the entire physical sector in a single actual area cell

Let r=u-e and T=s0+s1. If T>0, r/T lies on the CLOSED segment between
d0 and d1. Exact endpoint and feasible stationary-point checks give

    ||(1-tau)d0+tau d1||>amin=7/10, 0<=tau<=1.

Thus ||r||>amin T. Also n.e=1-delta^2/2 and

    ||r||/delta=sqrt(1-delta^2/4)/(1-delta^2/2), delta>0.

The fresh gate cr(1-d^2/2)>1, cr=1001/1000, implies

    delta<=||r||<cr delta,
    T<cr delta/amin<4delta<=1/50.                         (4)

At delta0, r=0. Hence all of (1) belongs to the raw outer triangle

    U=conv(e,e+(1/50)d0,e+(1/50)d1)
     =conv((1,0,0),(1,-1/75,1/150),(1,-1/50,0)).           (5)

The checker also directly verifies (1/50)amin>cr d. This raw triangle
is an ENCLOSING support/area domain; no passage exclusion is claimed
on all of it without the physical chord restriction in (1).

The complete original52 facets are freshly reconstructed from the55
originals. Choose the interior average of (5). Its dot product with
each original oriented face area vector is nonzero. The corresponding
signed dot products at ALL three corners are nonnegative. Affinity
therefore puts the whole closed U, including its walls, in one actual
Cauchy area cell. Its area vector is exactly

    C=(A0,-23/8-57s/40,3/4-3s/5), A0=(49+25s)/8,
    A(n)=C.n.                                           (6)

There are156 fresh corner sign checks. A second construction forms the
actual perturbed original shadow hull and reconstructs the same C by
half the cyclic cross-product sum. Each of its edges supports ALL55
originals at ALL three outer corners. These additional exact comparisons
check the area reconstruction independently of the facet sum. No
antipodal core or symmetrized body replaces the asymmetric original.

The exact tangent-norm gate gives ||C_t||<Gamma=61/10. For delta>0,

    A(n)-A0=-A0 delta^2/2+C_t.(n-e)<Gamma delta,
    Gamma d=61/2000<1/10.                                (7)

## 3. Fresh all-source roll entry on the whole sector

The fully replayed [global inverse-area parent](../rupert_j77_inverse_area_collar/PROOF.md),
source6345acdb4574fe0100230e6c04235892f4cfb13d, graph8248, proves

    A(k)<=A0+eta => dist(k,E)<7eta/20,
    0<eta<=1/10.                                        (8)

Area monotonicity in (2) and lambda>=1 imply A(Q^t n)<=A(n).
Combining (7),(8) gives, for EVERY original source,

    alpha=dist(Q^t n,E)<cs delta, cs=427/200.              (9)

The original minimum-area sources are included. All ten signed actual
axes are reconstructed; all45 pairwise squared separations exceed9/25.
The source budget cs d is<1/80, so the nearest signed source axis is
unique. The other actual receiving axes have |e.q|<81/100, whereas
n.e>=1-d^2/2 and n.q<=81/100+d. The fresh positive difference proves
that e is the unique nearest receiving signed axis throughout (1).

Use the original proper minimal normal transports and actual right
body factors from the pinned [full-roll framework](../rupert_j77_area_axis_roll/PROOF.md).
Both possible directed source-axis signs and ALL source rolls are
retained. Original vertex norms are<9/4. Pairing the SAME originals
gives the necessary planar Hausdorff allowance

    Eactual<(9/4)(delta+alpha)<hc delta,
    hc=5643/800,
    hc d=5643/160000<Enew=353/10000.                      (10)

The physical translation becomes an arbitrary planar translation under
the frame maps. Since0 is interior to K, reducing lambda>=1 to1 is
only a necessary condition and retains the same translation. No
centered-translation restriction is introduced.

At the reference projection P_eK=S, the actual ten cyclic projected
vertices give outward normals m_i and positive heights H_i. Every
original lies on the correct support side. Fresh rational U_i satisfy
U_i>0 and U_i^2>=||m_i||^2. For any selected strictly positive normalized
weights with sum_i w_i m_i=0, necessary approximate containment gives

    sum_i w_i(m_i.Fq_i-H_i-Enew U_i)<=0,                  (11)

where q_i is a selected ACTUAL original projected source vertex.
Both components of translation cancel exactly.

The four families T(x),-T(x),H T(x),-H T(x), x in[-1,1], cover ALL
O(2), where H=diag(1,-1) and

    T(x)=[[1-x^2,-2x],[2x,1-x^2]]/(1+x^2).

Each determinant branch and all shared semicircle endpoints are
included. No reduction modulo pi is used for the asymmetric S.
Multiplying (11) by1+x^2 gives a quadratic. The fixed certificate has
five CLOSED roots: family0 on[-1,-1/20] and[1/20,1], and each of
families1,2,3 on[-1,1]. Its complete midpoint forest has19 leaves,
33 nodes and depth4. The checker requires both children at every
internal node, prefix-free distinct terminals and exact closed endpoints.
The original fixed witnesses suffice without additional subdivision,
but ALL57 quadratic Bernstein coefficients are freshly recomputed at
Enew, and all exceed1/1000. Each quadratic identity is independently
checked against its full2x2 matrix at x=-1,0,1.

Bernstein basis weights are nonnegative and sum to one, so (11) fails
on every covered closed interval. The entire opposite source-axis
branch and every remote roll are excluded. Therefore an actual RIGHT
C5 gauge has positive directed source and |x|<b=1/20, x=tan(phi/2).
This new uniform calculation does not invoke the old smaller allowance
1269/40000 or the old absolute source chord91/10000 on the new domain.

For the two original signed near-contact pairs, exact zero-roll contact
and normal balance give

    g(x,delta)=Lsign |x|-2H0|x|^2-hc N delta(1+|x|^2)<=0,
    H0=(11+5s)/6, N=769421/375000,
    Lplus=8/3+s, Lminus=7/3+s.

Put k=10/3. The checker freshly proves k d<b and, for BOTH signs,

    k Lsign-hc N-k^2(2H0+hc N d)d>0,
    Lsign b-(2H0+hc N d)b^2-hc N d>0.

These lower-bound g(k delta,delta)/delta and g(b,delta) uniformly for
0<delta<=d. Concavity makes g positive on[k delta,b], so necessarily

    |tan(phi/2)|<k delta.                                (12)

The new source budget reaches427/40000, larger than the old1/100
arcsine domain. We freshly prove the derivative bound cr=1001/1000
for chords up to1/80 using

    cr^2*(1-(1/160)^2)>1,
    cs d<1/80, d<1/80.

The principal normal-transport angles are<cr alpha and<cr delta.
Together with2arctan|x|<2|x| and the spatial group-angle triangle
inequality, the fresh gate cr(1+cs)+2k<10 proves

    angle(Qh)<10delta                                   (13)

for every original placement at every positive delta in the whole
sector. These are principal FULL spatial angles. Delta0 is covered
separately by the fully replayed complete mirror-cap classification8206.

## 4. Same actual gauge, both reflected motions and physical translation

Write the already gauged rotation as Q and set Qtilde=M_n Q M_e.
Both factors are actual reflections, so Qtilde is proper. Since M_eK=K
and P_n M_n=P_n, it has the SAME projected source and SAME physical
translation and scale as Q. Before a second gauge its angle is
<(10+2cr)delta, by (4),(13). Apply the new WHOLE-SECTOR entry theorem
again to this same placement. A nonidentity second right factor would
have angle<(20+2cr)d<1. Fresh actual orthogonality, proper orientation,
original vertex permutations, order-five closure and trace checks show
that every nonidentity C5 factor has cosine<1/2, hence angle>1. The
second factor is therefore identity. Both actual motions obey (13)
in the SAME right gauge.

The fresh gate L0(1-(25/2)d^2)>5, L0=501/100, and elementary
sin/cos bounds imply Cayley norms eta,etatilde<L0 delta. The exact
reflection denominator is positive. Both directions of the reflection
identities in the [direct parent's Section3](../rupert_j77_closed_collar_rigidity/PROOF.md)
remain valid for these same actual motions and raw r. In particular

    Dref=1+w0.p>0, w0=e cross r,
    Dref<=1+L0 cr d^2,
    rhotilde=(rho+r.p)/Dref,
    ptilde=(w0-p+rho r)/Dref,
    rho-rhotilde=-[p,ptilde].                            (14)

For physical t in n-perp let T=t-t_xu. Then T.x=0 and P_uT=t.
The Cayley translation variables Ctr=(1+eta^2)T/2 and
Ctrtilde=(1+etatilde^2)T/2 encode the SAME arbitrary translation.
Their ratio bound is1+L0^2d^2. No source, companion, or translation
is chosen independently after a sufficient inequality is tested.

## 5. Fresh whole-sector hypotheses for signed original-contact rigidity

The [direct parent's Sections4–7](../rupert_j77_closed_collar_rigidity/PROOF.md)
prove a general original-contact argument from explicit geometric and
scalar hypotheses. We list and freshly check all domain-dependent
hypotheses needed to apply that argument on (1):

1. For each of32 original contacts(a_i,b_i,j_i), reconstruct
   m_i(u)=((V_bi-V_ai) cross u)/h_i0, where h_i0 is its positive
   critical offset. At EACH corner of U the actual offset is positive,
   V_ji lies on the receiving support, and ALL55 originals lie on its
   correct side. All5,280 comparisons are fresh. Affinity proves the
   full receiving supports throughout U, hence throughout (1).
2. The six mirror-fixed original sources and their affine derivative
   columns give the SAME freshly checked bounds on the intersection
   with ||r||<cr delta:
   probe norm<49/100, probe drift<27delta/25, torque drift<19delta/10,
   and ||v_i||||m_i(u)||<9/8. Exact Frobenius-norm gates are recomputed.
   The positive coordinate constructions and common coefficients are
   replayed and checked; they are not solver outputs.
3. The MOTION-coordinate rays a0=(0,0,-1), a1=(0,-1/3,-2/3) are distinct
   from the RECEIVING rays d0,d1. Their segment norm is>7/10 and each
   has norm<=1. Both original positive coordinate stresses, full moment
   matrices and Euclidean bounds chi=(9/4,3), nu=(15,17/4) are freshly
   checked. In particular ||H_k^t a_k||<nu_k bounds the entire own-row
   functional without expanding its absolute coefficients.
4. The mirror slack z_k=xi_k(w0) is nonnegative throughout U: its
   fresh corner triples are(0,0,1/50) and(0,1/50,0). Every opposite
   row corner is nonnegative. BOTH reflected inequalities and the
   nonzero opposite diagonals are retained, including factor2 in
   their combined coupling.
5. The receiving-dependent positive balance is freshly reconstructed
   on the raw ball||r||<=cr/200, which contains (1). Its four-column
   Neumann inverse, critical balance and correction are exact. All six
   normalized weights exceed1/25; the full3D normal sum and axial torque
   balance hold exactly. The normalized stress height satisfies
   99/100<h(u)<101/100. All four actual motion-ray bilinear corners
   lie strictly between21/50 and23/50. The raw radius equals the
   direct parent's radius; no radius variable is altered.

With m=min(eta,etatilde)>0, these hypotheses give the direct parent's
common translation/axial estimates, signed negative-coordinate inverse
and paired norm improvement. The new checker recomputes ALL six stages:

| L | ownC / pairC | ownrho / beta | W | Next paired ratio |
|---|---|---|---:|---|
|501/100|99 / 101|32 / 35|21800|231/50|
|231/50|93 / 95|30 / 33|17600|33/10|
|33/10|74 / 76|24 / 27|8400|51/25|
|51/25|56 / 58|18 / 21|3900|43/25|
|43/25|51 / 53|17 / 20|3200|42/25|
|42/25|51 / 53|17 / 20|3200|42/25|

Here L bounds each Cayley norm divided by delta. Every declared
common bound, positive directed diagonal/determinant, nonnegative
inverse entry, BOTH exact inverse products and paired norm-absorption
gate is checked. The whole-linear-functional estimate replaces the
insufficient own-row coefficient expansion. Thus the total negative
motion-coordinate sum satisfies Uneg<3200 delta^2m; the final axial
factor is20. The universal receiving-balanced original-contact identity
is replayed with all nine independent variables, including arbitrary
translation, giving the exact necessary bilinear inequality

    p^t A(u) ptilde<=h(u) rho rhotilde.

The signed expansion from the direct parent applies for every sign of
both tangent-coordinate pairs. With kappa=3200d^2=2/25 and
KF=51/50, the lower bilinear estimate minus the upper axial estimate
is at least the same exact strictly positive rational

    92210131/303450000>0

times eta etatilde. This is a contradiction when m>0. No unproved
cone membership, dropped opposite diagonal, floating eigenvalue,
solver verdict or absence of a found passage enters the argument.

If m=0, the actual reflection identities give Qh=I or M_n M_e.
Both have shadow P_nK. The original scaled containment (2) then forces
lambda=1 by positive area. A bounded shadow of positive area can
contain its translate only when t=0: the support function in direction
t would otherwise strictly increase. Conversely (3) with lambda1,t0
gives equal shadows because P_n M_n=P_n and M_eK=K. Delta0 is
included by the complete old cap8206. This proves the theorem.

Orthogonal actual body symmetries conjugate the proper rotations and
transport planar translations; receiving sign leaves P_n and M_n
unchanged. Therefore the stated actual images follow with nearest
signed axis q. No independent body symmetry is invented.

## 6. Reproducibility, prior art and remaining frontier

The [checker](verify.py), [fixed certificate](certificates.json),
[exact expected record](expected.json) and [byte-pinned dependencies](dependencies.json)
use Python3.11+ standard library, Fraction and the positive ordered field
Q(sqrt5). Every one of the40,383bytes of the direct parent's complete expected record
is replayed and compared BEFORE adding any new sign predicates. That
parent in turn fully replays its complete inputs. There are100 distinct
byte-pinned prerequisite files in14 recursive manifests. Independent
rational positive-sqrt5 enclosures check every registered sign in both
parent registries; their counts include prerequisites and may overlap.
The new malformed controls reject missing branches/children, duplicated
terminals, wrong domains/endpoints, nonoriginal sources, false balance,
understated norms and false signed near contacts. See README for exact
commands, expected SHA256 and measured author replay costs.

The trust boundary includes the original model and parent interfaces,
Python/Fraction and ordered-field semantics, the complete finite checks,
and the unformalized continuous projection, area, transport and signed
inequality bridges. Author replay and source publication do not establish
independent review.

The [April2026 primary account](https://arxiv.org/html/2604.26531)
reports87 of92 Johnson solids as known Rupert. The [primary Johnson
table](https://arxiv.org/html/2509.08190) leaves J72,J73,J74,J75,J77 without
listed passages. The [Noperthedron proof](https://arxiv.org/abs/2508.18475)
concerns a different body. The [algorithmic projection framework](https://arxiv.org/abs/2112.13754)
supplies the standard strict-shadow interpretation. Bounded live checks
found no primary global J77 resolution; no exhaustive novelty or priority
claim follows. This local result does not settle that global problem.

The complementary [deltoidal quarter-cell proof](../../geometry/rupert_deltoidal_symmetry/cell8_quarter_proof.md),
source198f45e5ddb5dc39c50a084e2e6b495b7b9109e9, graph8278, and
[RID proper-roll proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/MIXED_PAIR_ROLL_PROOF.md),
source677e8bacd57febbea25728592e5f6f28e1ca3e2b, graph8270, motivated
care with separate original-source budgets and directed branches. Their
centrality, body constants, global decisions and review statuses do not
transfer to J77. Their citations to8248 are method uptake, not reviews.

The prepublication refresh also supplied the complete
[global RID cutoff proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/GLOBAL_BAND_83_PROOF.md),
source6fbe50d0b130848b62786212c29dbfd307383a3a, graph8330. Its fresh
original candidate pools, matched-original moments and complete signed
covers give the global receiving condition f<83/200 and squared-height
gap at least1/28 for that different body. Its full proof and original
graph body were read. It remains unformalized and independently unreviewed;
global RID remains open. Its body-specific hypotheses are not imported.

The next frontier is other actual receiving sectors at this radius,
with fresh area-cell, roll-entry and signed-contact hypotheses, followed
by a complete larger cap if all sectors close. A strict proper-rotation
passage certificate remains an alternative. Failed sufficient estimates,
timeouts and incomplete searches are never nonexistence premises.
