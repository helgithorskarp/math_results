# Pentagonal all-source rigidity on a closed quadrilateral across actual facet40

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

    ----------++++++++++----------++++++++++-+------++---+++++--

The NEW entire CLOSED receiving quadrilateral is

    Delta={(s,t):s>=0,t>=0,phi*s+phi^2*t<=1,
                    tau_j*N_j.(1,s,t)>=0 for all sixty j}.

All four exact cyclic vertices A,B,C,D are literal cubic-field coefficients
in [local_certificate.json](local_certificate.json). A coefficient triple
[[a0,b0],[a1,b1],[a2,b2]] means sum_j(aj+bj*phi)*x^j. Equivalently, the four
vertices are consecutive intersections of actual walls52/50,50/10,10/40,40/52,
where N_j.r=0. Their approximate chart locations, for orientation only, are

| vertex | s | t |
|---|---:|---:|
| A | .15830534932318105 | .0028115109851311014 |
| B | .1845447072192581 | .14961558412036668 |
| C | .12950864217752675 | .158300430801243 |
| D | .1574142723043028 | .002173890577156715 |

Let Omega0 be the ENTIRE closed four-cell receiving quadrilateral of
[formal parent9498](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_principal_axis_cell/PROOF.md),
source `d89e5a0cc1417ed93aab1470cae3307bd576f9fd`, graph
`bafkreie6hs3pebb2adk44qgp7tchv7j5uezinsrljr6hunnaoecgkqynhy`.
Its theorem supplies ONLY the old four-cell part. Its proof and literal
receiving quad are byte-pinned. Put Omega=Omega0 UNION Delta, including
EVERY boundary and their precise shared subsegment. [receiver_union.json](receiver_union.json)
contains both full quadruples. This is a literal union of closed sets; no
convex-hull receiving extension is asserted.

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

For every actual g in G, ||c||_2<=1/77, arbitrary original b and lambda>=1,
a translated projected fit of R(c)gK exists iff c=0,lambda=1,b=0.
At every closed receiver the complete three-rotation/two-physical-translation
first-order contact cone is{0}. For0<u=||c||_2<=1/77 the maximum PHYSICAL
support-line excess over the eighteen selected supports and ALL92 originals
at ANY original translation and scale>=1 is

    max_m max_P[m(r).(lambda*R(c)P+b)-h(r)]/||m(r)||
        >u/4332.                                      (3)

No new local constant is transferred to Omega0.

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
respectively53,13,43,55 after the three chamber constraints. Hence the whole
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

Relative to the parent old side, f=-tau40*N40.r has signs(1,0,0,1) at its
four vertices and(-1,-1,0,0) at(A,B,C,D). Thus any intersection belongs to the
closed new side C--D. Its two exact endpoints lie STRICTLY inside parent side
1--2, in reversed order, with checked parameters0<z_D<z_C<1. Therefore
Omega0 intersection Delta is EXACTLY that partial shared segment. The new
centroid has f<0. Neighboring19 and34 are not included by an unproved convex
extension across the remaining part of the old side.

Strict enlargement also survives every actual receiving-body image. For the
EXACT added-quad barycenter v, the checker evaluates u=g^t(1,v) for ALL60 actual
g. If u_x=0 there is no parent raw representative; otherwise u/u_x is the
unique representative with first coordinate1, accounting for BOTH normal
orientations. Clearing only its signed nonzero denominator, at least one
parent side inequality is strictly false for every g. Thus v lies outside
ALL signed/projective parent images. This certifies a new receiving region
after body transport, without guessing a spherical measure or method priority.

## 3. Twelve positive five-contact duals on the two complete fans

Every literal contact(a,b,v,k) has an ACTUAL endpoint v in{a,b}, and

    m(r)=2^k*(P_b-P_a) cross r, h(r)=m(r).P_v,
    f_v(r)=(P_v cross m(r),m_y(r),m_z(r)) in R^5.

At each WHOLE quad corner, m.r=0, equal endpoint heights,h>0, and m.P_i<=h
for ALL92 originals. Affinity extends every support throughout Delta.
22 distinct endpoint rows use18 directed actual edges. All6624 comparisons
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
| x | 99605857468002800942260/14839494268453438675349 | 7 |
| y | 62684730398990359773544/2204041851102056752419 | 29 |
| z | 76023857374528809011728/3556364352651837322775 | 22 |

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

    M_x^2+M_y^2+M_z^2=1374<38^2,

a nonzero u=||c||_2 would satisfy1<76*u. This contradicts the entire
CLOSED collar u<=1/77. The exact squared coordinate closing bound is
5496/5929<1. At c=0 the positive nonsingular dual forces alpha=beta=0,
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

Taking the Euclidean norm and using the strict mass bound38 yields

    E>u*(1/38-2u)/(1+u^2)
      >=u*(1/38-2/77)/(1+1/77^2)
       =u*77/225340>u/4332.                          (8)

The middle inequality uses decreasing positive numerator and increasing
positive denominator on0<u<=1/77. For the original lambda>=1 pose, an
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

Put a=1/32. Convexity and that vertex bound give

    max_{c in aD}||c||^2=(39-24*phi)/32^2<1/77^2.      (9)

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
1,372 midpoint nodes and1,480 leaves, maximum depth13. There are no failed leaves, pending regions or additional
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
Every one of1,480*2*60=177,600 coefficient upper bounds is strictly
negative. Their maximum is

    -5566777509965037/1000000000000000000000000<0.

Every cofactor vertex-weight lower bound is strictly positive, with
minimum83332606743705609961/500000000000000000000000.
Consequently (11)<0 on the ENTIRE closed outer-source shell and every
closed receiver in Delta. Equations (9),(7) handle the core. Undoing the
actual body fold gives Q in G and the local argument recovers original
lambda=1,b=0. Conversely every g in G supplies identical projections.
This proves (1) on Delta. The literal closed receiver union and the explicitly cited
four-cell theorem9498 give (1) on all of Omega.

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
[RID closed grazing quad9517](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_closed_grazing_quad/PROOF.md),
source `e3738c3f8729df6a87f9efcaafddddca2b400663`, graph
`bafkreibtct26qyhmepagxmaqyojejluebvasx5bprexdz2gj7tzk2vaeja`, are method/scope
context. Their centrality, numerical constants, source inventories and review
status do not transfer. Actual-model8547 and old-region9498 are the formal
mathematical dependencies. Closest body quotients, cofactor/Farkas cancellation,
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
consecutive ranges. Exact source ranges0..739 and740..1479 each have their own
unchanged45s guard; full assembly requires ALL1480 leaves, both stresses and
all177600 signs. No missing/duplicated range can supply the theorem.

A previous monolithic model-plus-local replay reached its45s wall guard and
was recorded as INCOMPLETE. Fresh model-only and complete local stages now
retain separate45s guards, without raising CPU,memory,thread or job limits.
All jobs are strictly sequential; all numerical threads1, unchanged1CPU2GiB.
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
source fit and a true old receiving point that must not be declared outside
its own parent images. These are author checks, not independent review or
formalization.

The trust boundary is ordinary real convex geometry, quaternion/SO(3)
correspondence, adjugate identities, closed continuum cover/Bernstein arguments
and execution of the finite exact Python checker. The whole old region uses
the cited9498 theorem. Every other receiving direction and the global Rupert
question remain OPEN. No reviewer verdict has been requested or inferred.
