# Pentagonal all-source rigidity on a closed quadrilateral across actual facet10

**six-rupert-1, researcher; 2026-10-02.** Ordinary intermediate geometric proof
with an exact finite certificate. Author checked, unformalized and independently
unreviewed. Global SAME-HANDED standard pentagonal hexecontahedron Rupert status
remains **OPEN**. Execution evidence is in [VALIDATION.json](VALIDATION.json).

## 1. Exact original solid, entire closed domains and statement

Let K be the original SAME-HANDED standard pentagonal hexecontahedron from
[model8547](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_minimum_diameter/model.json),
source `86ab225fb8becbe66601a5da0b5b017e872e1833`, graph
`bafkreig6lwaauql5ebhxsquhx4zcdkprdyy4vfk3mfodeqgkoc3mznzlvi`.
Its92 original vertices P_i lie in Q(phi)[x], phi=(1+sqrt(5))/2,
x the unique root of x^3-2x-phi=0 in(17/10,18/10), with the inherited uniform
normalization by the largest literal coordinate. Let G be its ACTUAL proper
sixty-element body group. Origin is interior. No whole-body centrality premise
is imposed. Index the sixty actual normalized outward facet normals N_j by
N_j.P<=1 in the original named model order.

Use raw r=(1,s,t), not spherical distances, and the sixty signs

    -----------+++++++++----------++++++++++-+------++---+++++--

The NEW entire CLOSED receiving quadrilateral is

    Delta={(s,t):s>=0,t>=0,phi*s+phi^2*t<=1,
                    tau_j*N_j.(1,s,t)>=0 for all sixty j}.

All four exact cyclic vertices A,B,C,D are literal cubic-field coefficients
in [local_certificate.json](local_certificate.json). A coefficient triple
[[a0,b0],[a1,b1],[a2,b2]] means sum_j(aj+bj*phi)*x^j. Equivalently, the four
vertices are consecutive intersections of actual walls50/5,5/40,40/10,10/50,
where N_j.r=0. Their approximate chart locations, for orientation only, are

| vertex | s | t |
|---|---:|---:|
| A=E | .19525711059213835 | .20954938488008648 |
| B=P | .12240340124124333 | .19805286354692275 |
| C | .12950864217752675 | .158300430801243 |
| D=old B | .1845447072192581 | .14961558412036668 |

Let Omega0 be the ENTIRE closed five-cell receiving union of
[formal parent9558](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_facet40_quad/PROOF.md),
source `4f89c33fb8e4828f97f4b68481e15a15db51faa4`, graph
`bafkreiexvt7tzreqsjsovespasoghudhedvtumsnoe7pp7evvkyqguu3za`.
It consists of the closed four-cell parent quadrilateral on cells14,28,13,11
and the ENTIRE closed quadrilateral20. Its theorem supplies ONLY this previous
region. Its full proof and both literal quads are byte-pinned. Put
Omega=Omega0 UNION Delta, retaining every boundary. [receiver_union.json](receiver_union.json)
contains all THREE entire quadruples and both exact shared segments. This is
a literal closed union, not a convex-hull receiving extension. The newly
included whole phase is34; an unresolved neighboring phase19 is not included.

Write pi_r for orthogonal projection onto r-perp.

**Theorem.** For EVERY(s,t) in Omega, EVERY ORIGINAL Q in SO(3), EVERY
ORIGINAL physical b in r-perp, and EVERY ORIGINAL scale lambda>=1,

    lambda*pi_r(QK)+b subseteq pi_rK
        iff Q belongs to G, lambda=1, b=0.             (1)

There is no source-collar, source-quaternion, roll or translation-entry premise.
Every original source half-turn and every closed receiver corner/seam remains
included. The added Delta's equality inventory is concluded AFTER its complete
source proof. Thus no strict standard Rupert passage has a receiver here.
The conclusion transports to receiving r'=epsilon*g*r for every actual g in G
and epsilon=+/-1, by applying g^-1 to the entire physical configuration.
Reflecting the whole solid and configuration gives the other handed version;
no independent improper source placement is allowed.

**New quantitative lemma on Delta ONLY.** Let

    R(c)P=[(1-c.c)P+2c(c.P)+2c cross P]/(1+c.c).

For every actual g in G, ||c||_2<=1/51, arbitrary original b and lambda>=1,
a translated projected fit of R(c)gK exists iff c=0,lambda=1,b=0.
At every closed receiver the complete three-rotation/two-physical-translation
first-order contact cone is{0}. For0<u=||c||_2<=1/51 the maximum PHYSICAL
support-line excess over the eighteen selected supports and ALL92 originals
at ANY original translation and scale>=1 is

    max_m max_P[m(r).(lambda*R(c)P+b)-h(r)]/||m(r)||
        >u/1875.                                      (3)

No new local constant or source collar is transferred to the previous region Omega0.

## 2. Entire quadrilateral, both closed fans and exact parent intersection

The pinned geometry.py/polynomial.py code from
[closed-cell9283](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_closed_horizon_cell/PROOF.md)
is reused as arithmetic/model code. Its former local contact/radius theorem
is not a hypothesis. The fresh named reconstruction verifies all92 originals,
60 pentagonal facets,300 coplanar identities,5220 strict other-original facet
inequalities,900 global facet turns, two-face incidence of150 edges, Euler
identity, connected adjacency and all300 directed horizon clauses.

All63 chamber/facet halfspaces hold at all FOUR proposed Delta corners:
252 exact comparisons. Every other corner is strictly left of every successive
side: eight global turns. Each side is an actual defining halfspace wall,
respectively8,43,13,53 after the three chamber constraints. Hence the whole
convex quad lies in the stated Delta, while Delta lies in its four inward
side halfspaces, whose intersection is precisely that quad. Both inclusions
prove the ENTIRE closed cell, retaining all zero values.

The globally convex cyclic quad is exactly the union of its TWO CLOSED fan
triangles(A,B,C) and(A,C,D). Here is an explicit full-cover inverse.
Let ell(p)=det(C-A,p-A), ell(B)<0<ell(D). Put

    uB=ell(D)/(ell(D)-ell(B)), uD=-ell(B)/(ell(D)-ell(B)),
    J=uB*B+uD*D=(1-theta)A+theta*C, 0<theta<1.

The actual field checker verifies these strict signs and the EXACT J identity.
For p=sum_i beta_i*v_i, beta_i>=0,sum beta_i=1, if ell(p)<=0 take k=beta_D/uD
and rewrite it in(A,B,C) with weights

    beta_A+k(1-theta), beta_B-k*uB, beta_C+k*theta.

The middle weight is nonnegative precisely because ell(p)<=0. If ell(p)>=0,
take k=beta_B/uB and use(A,C,D) weights

    beta_A+k(1-theta), beta_C+k*theta, beta_D-k*uD.

All weights are nonnegative and sum to one; the J identity reconstructs p.
The equality diagonal is retained in BOTH closed triangles. The local checker
requires paths0/1 and all six signed targets on EACH path exactly once. The
outer checker separately requires BOTH fan stresses on EVERY source leaf.
No single-triangle or single-seam test is treated as covering the quad.

Write Q0=(O0,O1,O2,O3) for the parent four-cell quad and
Q20=(A20,B20,C20,D20) for the added whole parent quad20. The new vertices
are(A,B,C,D)=(E,P,C20,B20), with P=O2. For f10=tau10*N10.r the signs on
Q20 are(-1,0,0,-1) and on the new quad are(1,1,0,0). Thus their intersection
is confined to their facet10 sides. Exact endpoint identities C=C20,D=B20
show it is the ENTIRE reversed segment C--D. For f40=tau40*N40.r the signs
on Q0 are(-1,0,0,-1), on the new quad(1,0,0,1). B=O2, while
C=(1-z)O1+z*O2 with exact0<z<1. Hence Q0 intersection Delta is EXACTLY
B--C. Both intersections retain their endpoints; the two segments meet
at C. Therefore Omega0 intersection Delta is precisely their union.
Every other new point, including its centroid, is outside the previous union.
No extra convex-hull region is inferred from these joins.

Strict enlargement also survives all receiving-body transport. For the EXACT
new centroid v and EACH of Q0,Q20, the checker evaluates u=g^t(1,v) for
ALL60 actual proper body matrices. If u_x=0 there is no parent raw representative;
otherwise u/u_x is the unique first-coordinate1 representative, accounting
for BOTH normal orientations. Clearing only the signed nonzero denominator,
at least one parent side inequality is strictly false in every case. All120
cases pass. The new centroid therefore lies outside the union of every signed
projective image of both previous quads. This certifies an enlarged receiving
region after transport, without a spherical-measure or historical-priority claim.

## 3. Twelve positive five-contact duals on the two complete fans

Every literal contact(a,b,v,k) has an ACTUAL endpoint v in{a,b}, and

    m(r)=2^k*(P_b-P_a) cross r, h(r)=m(r).P_v,
    f_v(r)=(P_v cross m(r),m_y(r),m_z(r)) in R^5.

At each WHOLE quad corner, m.r=0, equal endpoint heights,h>0, and m.P_i<=h
for ALL92 originals. Affinity extends every support throughout Delta.
21 distinct endpoint rows use18 directed actual edges. All6624 comparisons
pass, including198 exact ties and54 offendpoint grazing ties. Verified
squared norm bounds at all four corners and convexity give throughout Delta

    ||m(r)||<2, 2*max_P||P||*max_m||m(r)||<4.            (4)

Since r_x=1, b=pi_r(alpha*e_y+beta*e_z) is a unique physical translation
representation. Each closed fan has six bases, one per signed rotation target.
Five DISTINCT actual wrench columns form A(r), affine in raw(s,t). The signed
reference determinant and every determinant/replaced-column polynomial are
recomputed in outward rational fixed-point intervals at scale10^24.
All12*6*21=1512 triangular degree-five Bernstein controls are strictly positive.
Cramer's rule therefore gives positive weights throughout the ENTIRE closed
fan with sum_i w_i*f_i=epsilon*e_j in ALL FIVE entries. Both original
translation coordinates cancel.

For p(z,w)=sum a_ij*z^i*w^j the degree-n triangular controls are

    B_kl=sum_{i<=k,j<=l} a_ij*binom(k,i)*binom(l,j)
                      /[binom(n,i+j)*binom(i+j,i)], n=5.

Their nonnegative basis sums to one on the entire closed reference triangle.
Positive denominator/numerator controls and matched coefficientwise
sum-numerator upper/denominator lower bounds give uniform masses on both fans:

| coordinate | exact uniform mass upper | strict integer bound |
|---|---|---:|
| x | 96320378755062625082296/21677640920286837638195 | 5 |
| y | 289134405962603370054667/26660420937239899690430 | 11 |
| z | 411237809351387117374097/20229334375383116213665 | 21 |

If f_i.U<=0 for every selected contact, both signs force its first three
coordinates zero. One positive nonsingular dual then has weighted sum zero;
all its five inequalities are equalities, and nonsingularity forces U=0.
This proves the complete infinitesimal physical cone statement.

## 4. Euclidean nonlinear closure and the physical gap

For a unit closed fit put d=c.c and
U=(2c_x,2c_y,2c_z,(1+d)*alpha,(1+d)*beta). At an original endpoint,
clearing the positive Cayley denominator gives

    f.U<=2*m.(d*I-c*c^t)P.                              (7)

The symmetric operator has eigenvalues d,d,0 and norm d. For c!=0,
(4) makes its right side strictly less than4d. Applying the two signed
duals gives |c_j|<2*M_j*d. Since

    M_x^2+M_y^2+M_z^2=587<25^2,

a nonzero u=||c||_2 would satisfy1<50*u. This contradicts the entire
CLOSED collar u<=1/51. The exact squared coordinate closing bound is
2348/2601<1. At c=0 the positive nonsingular dual forces alpha=beta=0,
so the actual unit-fit translation is zero.

For original lambda>=1, divide the ORIGINAL inclusion by lambda about
the receiving origin. Convexity and0 in K give a unit fit with b/lambda.
The unit conclusion gives c=b=0; a strictly positive actual support
height forces lambda=1. Body g only permutes the actual originals.

For the quantitative assertion let E be the maximum unit physical
support excess over all selected supports and all92 originals, at
arbitrary translation. The same local inequalities exclude E<=0 for
c!=0, so E>0. Each selected endpoint then satisfies

    f.U<4d+2*(1+d)*E,
    |c_j|<M_j*[2d+(1+d)*E].

Taking the Euclidean norm and using the strict mass bound25 yields

    E>u*(1/25-2u)/(1+u^2)
      >=u*(1/25-2/51)/(1+1/51^2)
       =u*51/65050>u/1875.                          (8)

The middle inequality uses decreasing positive numerator and increasing
positive denominator on0<u<=1/51. For the original lambda>=1 pose, an
original attaining positive unit excess e at b/lambda has scaled excess
lambda*e+(lambda-1)*h/||m||>=e. This proves (3) for every original scale
and translation, without assuming a fit or centering the chiral body.

## 5. Every proper source enters a complete Cayley domain

The binary-icosahedral closest-orientation region is classical; see
[Purser, NCEP Office Note489 (2017), Section2(d)](https://repository.library.noaa.gov/view/noaa/15765/noaa_15765_DS1.pdf).
The actual named proper matrices and finite-to-continuum source argument
are rebuilt in [source_cell.py](source_cell.py), reusing the ordinary
bridge of [LEMMA9363](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_all_source_horizon_cell/PROOF.md).
No new general quaternion or fundamental-region method is claimed.

For every ORIGINAL Q in SO(3), right multiplication by an actual g in G
preserves QK. Choose the signed quaternion among these finite equivalent
sources with largest positive scalar. The identity and three coordinate
half-turns ensure that scalar is nonzero; hence c=vector/scalar is finite,
even if the original source quaternion had scalar zero. Closest identity
gives all sixty inequalities |a+b.c|<=1 for proper-group unit
quaternions (a,b).

The twelve nearest comparisons define D={c:W_i.c<=phi-1}. Opposite
spanning normals prove boundedness and origin interior. Exact enumeration
of all220 wall triples gives precisely twenty feasible vertices. All
2,400 signed full-group comparisons hold at those vertices; affinity
and bounded-polytope vertex coverage show that the twelve walls imply
ALL sixty closest-body inequalities. Thus D is the complete relative
SO(3)/G domain, not a sampled restriction. Its exact vertices all have
squared norm39-24*phi. No partial-shadow equivalence is assumed.

Put a=1/21. Convexity and that vertex bound give

    max_{c in aD}||c||^2=(39-24*phi)/21^2<1/51^2.      (9)

The ordered Q(phi) checker verifies this strict inequality. Consequently
the ENTIRE closed inner core aD lies in the new local collar.

## 6. Entire closed outer-source shell

Every actual pentagonal face of D is supplied as its full positively
oriented five-cycle. The checker proves membership of all five vertices
and all180 global face-side turns. Its three closed fan triangles cover
the face; the36 radial face triangles cover D from its interior origin.
The ordinary frustum partition is credited to the full proof9363.

For independent face vectors A,B,C, write a radial frustum as
xA+yB+zC with x,y,z>=0 and a<=x+y+z<=1. Define L1=x+y+a*z and
L2=x+a*y+a*z. Because L1>=L2, its three closed regions
L1<=a, L1>=a>=L2, L2>=a are exactly the tetrahedra

    (aA,aB,aC,C), (aA,aB,B,C), (aA,A,B,C).

Their respective barycentric coordinates are

    x/a,y/a,(a-L1)/(a*(1-a)),(x+y+z-a)/(1-a);
    x/a,(a-L2)/(a*(1-a)),(L1-a)/(1-a),z;
    (1-x-y-z)/(1-a),(L2-a)/(1-a),y,z.

They are nonnegative exactly in the stated regions, sum to one and
reconstruct the same point. This proves complete CLOSED shell coverage,
including every seam, rather than inferring it from volumes.

All108 roots occur once in canonical face/fan/part order. Every literal
edge bisection has both closed midpoint children. The exact prefix-tree
checker reconstructs all tetrahedra in Q(phi) and rejects missing,
duplicated, orphan or inconsistent children. The complete forest has
852 midpoint nodes and960 leaves, maximum depth11. There are no failed leaves, pending regions or additional
unproved source holes. Its inner core is handled only by (9),(7).

## 7. Original translation cancellation and joint tensor signs

For each selected undyadic actual edge d_i=P_b-P_a use
m_i(r)=d_i cross r and h_i(r)=m_i(r).P_a. All6,624 actual original
support comparisons at the four whole receiver corners are checked
again, including weak boundary ties; affinity extends them throughout
Delta. Positive h ensures a nonzero physical support.

For three selected directions set

    w_1(r)=(d_2 cross d_3).r,
    w_2(r)=(d_3 cross d_1).r,
    w_3(r)=(d_1 cross d_2).r,

with one common sign chosen so ALL their closed-corner values are
strictly positive. Affinity gives positive weights everywhere.
The cofactor identity sum w_i*d_i=det(d_1,d_2,d_3)*r yields

    sum w_i(r)*m_i(r)=0 in ALL THREE spatial coordinates. (10)

Every original physical translation cancels without a centrality premise.
For three selected ACTUAL moving originals X_i define

    F(r,c)=sum_i w_i(r)*[(1+c.c)*h_i(r)
        -m_i(r).((1-c.c)*X_i+2c(c.X_i)+2c cross X_i)].    (11)

A unit closed fit implies F>=0. For the ORIGINAL lambda>=1 pose,
the weighted sum of support excesses is exactly

    -lambda*F/(1+c.c)+(lambda-1)*sum_i w_i*h_i.          (12)

Thus F<0 contradicts every original translation and every scale>=1.
The selected actual original need not maximize a support to justify this
necessary inequality. Actual source folding preserves K and retains
the original scale and physical translation.

F has receiver/source degree at most(2,2). On a closed receiver triangle
and a closed source tetrahedron its tensor Bernstein basis consists of
six receiver controls times ten source controls. The basis is
nonnegative and sums to one everywhere in the closed product. The
source polarization of the cleared transform is

    T(P;u,v)=(1-u.v)*P+u*(v.P)+v*(u.P)+(u+v) cross P.

Writing G_i(r;u,v)=(1+u.v)*h_i(r)-m_i(r).T(X_i;u,v), the joint
coefficient for receiver vertices r_a,r_b and source vertices u,v is

    (1/2)*sum_i[w_i(r_a)*G_i(r_b;u,v)
               +w_i(r_b)*G_i(r_a;u,v)].                (13)

[verify_shell.py](verify_shell.py) reconstructs every such coefficient
from exact source vertices and outward original-point/support enclosures.
Every one of960*2*60=115,200 coefficient upper bounds is strictly
negative. Their maximum is

    -522718154552503327/250000000000000000000000<0.

Every cofactor vertex-weight lower bound is strictly positive, with
minimum13692071394567963989/50000000000000000000000.
Consequently (11)<0 on the ENTIRE closed outer-source shell and every
closed receiver in Delta. Equations (9),(7) handle the core. Undoing the
actual body fold gives Q in G and the local argument recovers original
lambda=1,b=0. Conversely every g in G supplies identical projections.
This proves (1) on Delta. The literal closed receiver union and the explicitly cited
five-cell theorem9558 give (1) on all of Omega.

## 8. Reproduction, prior literature and trust boundary

Primary literature refreshed2026-10-02 retains the pentagonal and deltoidal
hexecontahedra as unresolved Catalan solids: [Gosain--Grimmer Table3](https://arxiv.org/html/2509.08190),
consistent with [Zeng Sections1.1--1.2](https://arxiv.org/html/2604.26531#S1.SS2).
The [strict proper-projection definition](https://arxiv.org/html/2604.26531#S1.SS1)
requires interior containment. [Steininger--Yurkevich2508.18475v2](https://arxiv.org/abs/2508.18475)
proves the distinct Noperthedron result. Bounded current searches found no
later global resolution of this named solid. Failed passage searches and
incomplete proof jobs do not prove nonexistence.

The fully read source/original-body-matched complementary
[J74 phase-crossing9531](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/phase_crossing_box/PROOF.md),
source `2ba89329055167fe838b568349801a2d7ccd39be`, graph
`bafkreidfs3zhk3muoh7lkalqwikf232zqz4psh3q4fqn2edt7mj2sp525a`, and
[RID full phase-crossing9568](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_phase_crossing_box/PROOF.md),
source `79fae6f762fbc0da56f047bf25990b3dc15ddbbb`, graph
`bafkreift2k745jq7s3l35tylil5m7mefzarmaobrtnhv7yjkpvkje5lne4`, are
other-body context. Both full ordinary original graph proofs and published
source were read and matched. Their centrality, numerical constants,
source/equality inventories and review status do not transfer. Actual-model8547
and old-region9558 are the mathematical dependencies. On the new phase34,
three old quad20 support directions actually fail some new-corner support
tests, so no old support/stress inventory was assumed. New actual supports,
all twelve positive duals, the1/51 collar and the entire outer source proof
were reconstructed for34. The separately completed [J74 three-cube cover9584](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/three_cube_cover/PROOF.md), source `ef3f6947d7e61297b40e84a4d85fa7f33dc059fb`, graph `bafkreibk5bm5fysjkptgqjq64yhks6sxurx7t56p3roig2j4n7vwejoweu`, was also fully read and source/body matched. It covers all J74 configurations using actual body actions and closed source gates; it proves no receiving exclusion. Its new parameterization and stated degree(4,2) cost do not replace our pentagonal proper-body quotient or transfer a certificate. Closest body quotients, cofactor/Farkas cancellation,
Cramer's rule, closed diagonal/frustum partitions and Bernstein positivity
are classical; no new general method or historical priority is claimed.

From this contribution directory run

```bash
python3 reproduce.py
python3 reproduce.py --optimized --compare .generated/complete_normal.json
```

The mandatory sequential driver freshly reconstructs the actual solid, checks
the whole hash-linked cache, and then proves the new local certificate as a
separate guarded job. A failed reconstruction stops before a stale cache is
used. It rechecks every actual support and inner-core inclusion, regenerates
the SAME bulky forest from compact source, checks both complete receiver fans
on EVERY source leaf, runs independent author controls and assembles all
consecutive ranges. The complete exact source range0..959 has its own unchanged45s guard;
full assembly requires ALL960 leaves, both stresses and all115200 signs. No missing/duplicated range can supply the theorem.

Fresh model-only and whole local stages retain separate45s guards;
exact support preparation and forest proposals have40s guards. No resource
limit was raised. All jobs are strictly sequential; all numerical threads1, unchanged1CPU2GiB.
[VALIDATION.json](VALIDATION.json) gives actual normal/optimized evidence and
[expected.json](expected.json) the full fixed mathematical fingerprints.
The exact checker uses CPython3.11+ standard-library ordered Q(phi)[x]/Fraction
arithmetic and outward integer intervals; NumPy1.24.2 is used only to propose
literal source splits/cuts. Floating signs are never proof premises.
Generated geometry/forests/streams/logs are private ignored state, not inputs
requiring a private corpus. The relative model/arithmetic directories already
in this repository are the explicit byte-pinned dependencies.

Independent author controls use exact Fraction plane minors and two-stage
midpoint polarization on720 coefficients,36 direct tensor identities and six
actual named-solid arbitrary translation/scaling cases. They check120 EXACT
actual-quad diagonal barycentric inverses, including all closed sides/seams.
Damaged controls cover the fresh-cache link, missing source or receiver fans,
false facet phase, invalid endpoint, insufficient closure bounds, a true zero
source fit and true receiving points from EACH old quad that must not be declared outside
their own parent images, and independent damage to both shared seams. These are author checks, not independent review or
formalization.

The trust boundary is ordinary real convex geometry, quaternion/SO(3)
correspondence, adjugate identities, closed continuum cover/Bernstein arguments
and execution of the finite exact Python checker. The whole old region uses
the cited9558 theorem. Every other receiving direction and the global Rupert
question remain OPEN. No reviewer verdict has been requested or inferred.
