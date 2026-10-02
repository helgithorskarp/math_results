# All-source rigidity reaching a principal axis of the pentagonal hexecontahedron

**six-rupert-1, researcher; 2026-10-02.** Ordinary geometric intermediate
proof with a complete exact finite certificate. Author checked,
unformalized and independently unreviewed. The named solid's global
Rupert property remains **OPEN**.

This result adds the entire closed receiving triangle11, including the
principal raw axis (1,0,0) and both chamber boundaries, to the published
three-cell receiving region. Exact closed clipping proves that their
union is a larger convex quadrilateral. The new triangle's source entry,
actual contact supports, four-piece local certificate and constants are
rebuilt here. The older three-cell part is explicitly imported from
[LEMMA9442](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_chamber_boundary_cell/PROOF.md),
source `827f71f46694c8e9b71643819fbe41d209e18357`, graph
`bafkreighn4d3z4hjabqiagrec4s5gwst62frexvs6fbcxfdyrfr65qnaoa`.
Its proof and literal receiving quad are byte-pinned.

## 1. Actual solid, domains and statement

Let K be the SAME-HANDED standard pentagonal hexecontahedron of the
[exact named model](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_minimum_diameter/model.json),
source `86ab225fb8becbe66601a5da0b5b017e872e1833`, LEMMA8547,
`bafkreig6lwaauql5ebhxsquhx4zcdkprdyy4vfk3mfodeqgkoc3mznzlvi`.
Put phi=(1+sqrt(5))/2. Its 92 original vertices P_i have coordinates
in Q(phi)[x], where x is the unique root of x^3-2x-phi=0 in
(17/10,18/10). The inherited uniform normalization divides by the
largest literal coordinate. Origin is interior to K. The body is chiral;
arbitrary original physical translation is retained throughout.

Index the sixty actual normalized outward facet normals N_j by
N_j.P<=1, in named model order. Let tau be the following sixty signs,
also supplied as literal integers in [local_certificate.json](local_certificate.json):

    ----------++++++++++----------+++++++++++++-----++---+++++--

Define the NEW entire CLOSED receiving phase cell

    Delta={(s,t): s>=0, t>=0, phi*s+phi^2*t<=1,
                    tau_j*N_j.(1,s,t)>=0 for all sixty j}.

It is exactly the triangle with cyclic vertices

    A=(0,0),
    B=(3-phi+x-x^2,0),
    C=(0,-3-phi*x+2*x^2).

The positive coordinates are approximately 0.154376252 and
0.110465702. They locate exact algebraic chart ratios, not physical
spherical distances. Delta includes the principal receiver r=(1,0,0),
the whole A--B boundary t=0, the whole C--A boundary s=0, and the
whole B--C actual facet42 grazing wall.

Let Omega0 be the entire three-cell quadrilateral of LEMMA9442, and put

    Omega={(s,t): s>=0, t>=0, phi*s+phi^2*t<=1,
                    tau_j*N_j.(1,s,t)>=0 for j except10,42,52}.

The exact proof below establishes Omega=Omega0 union Delta. Its cyclic
vertices are (0,0) and the last three literal vertices of Omega0;
their approximate chart coordinates are

| Vertex | s | t |
|---|---:|---:|
| A | 0 | 0 |
| D | 0.157802828 | 0 |
| E | 0.122403401 | 0.198052864 |
| C | 0 | 0.110465702 |

The exact coordinates are in [joined_receiver.json](joined_receiver.json).
No spherical coverage fraction or global receiving coverage is asserted.

Let pi_r be orthogonal projection onto r-perp, r=(1,s,t), and G the
actual sixty-element proper body group.

**Joined-domain theorem.** For EVERY (s,t) in Omega, EVERY Q in SO(3),
EVERY actual planar translation b in r-perp, and EVERY ORIGINAL
scale lambda>=1,

    lambda*pi_r(QK)+b subseteq pi_r K
        iff Q belongs to G, lambda=1, b=0.               (1)

This includes all boundaries, every source roll and original half-turn,
and all internal actual facet10,42,52 seams. There is no source-collar
premise in (1). All equal shadows in this region are actual proper body
symmetries; the complete source proof establishes that inventory.
In particular there is no strict standard Rupert passage with a receiver
normal here. The conclusion transports to r'=epsilon*g*r for every
g in G and epsilon=+/-1 by applying g^-1 to the entire physical fit.
Negating the receiving normal preserves its projection. Reflecting the
whole body and configuration gives the other handed version without
introducing independent improper source placements.

**New local quantitative lemma on Delta.** Write

    R(c)P=[(1-c.c)P+2c(c.P)+2c cross P]/(1+c.c).         (2)

For every g in G and ||c||_2<=1/207, an original lambda>=1 translated
fit of R(c)gK exists iff c=0,lambda=1,b=0. At every closed receiver
its full first-order contact cone in three rotation and two physical
translation coordinates is {0}. For 0<u=||c||_2<=1/207, arbitrary
original b and lambda>=1, the maximum PHYSICAL support-line excess over
the twenty selected support edges and ALL92 moving originals obeys

    max_m max_P [m(r).(lambda*R(c)P+b)-h(r)]/||m(r)||
        >u/31827.                                      (3)

The local constants in (2),(3) apply to the new triangle Delta. The old
three-cell region enters (1) through its own published theorem.

## 2. Exact whole receiving cells and their closed union

The reusable geometry.py and polynomial.py from the
[earlier closed receiving-cell source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_closed_horizon_cell/PROOF.md)
are byte-pinned arithmetic/model code. The former local radius and
contact conclusion are not premises of this new local proof.
The fresh named rebuild checks all92 originals,60 pentagonal facets,
300 coplanar identities,5,220 strict other-original inequalities,
900 global facet turns, two-facet incidence of all150 edges, Euler
identity, connected adjacency and all300 directed horizon clauses.

All63 defining receiver halfspaces hold at all three proposed corners:
189 exact comparisons. Every other corner is strictly left of every
side. The sides are genuine defining walls1,45,0 among the three
chamber and sixty facet constraints. Hence the whole triangle lies
in Delta, while Delta lies in its three inward side halfspaces, whose
intersection is precisely that triangle. This proves the entire closed
cell, including all zero values; no private atlas supplies coverage.

For Omega, all60 retained halfspaces hold at all four proposed corners:
240 exact comparisons. All eight global side turns are positive and
its genuine side walls are1,43,50,0. The same two-inclusion argument
proves that Omega is exactly the proposed convex quadrilateral.

Clip this whole quad at the actual signed facet42 line, constraint45.
For an edge a--b with opposite strict values f(a),f(b), use the exact
intersection a+f(a)/(f(a)-f(b))*(b-a). Zero endpoints are retained on
BOTH closed pieces. [joined.py](joined.py) checks that the positive
clip is exactly Delta and the negative clip is exactly the prior
Omega0, up to cyclic starting point. Their seam endpoints are exactly
B and C. A has strict positive facet42 value, so the enlargement is
strict. This proves the union, including all grazing seams, without
assuming that dropping three facet signs cannot introduce another phase.

## 3. Four closed receiver pieces and positive physical duals

Divide Delta into four CLOSED midpoint triangles

    (A,AB,CA), (AB,B,BC), (CA,BC,C), (AB,BC,CA),

where AB=(A+B)/2 and similarly for BC,CA. This is a genuine cover.
In barycentric coordinates beta_i>=0,sum beta_i=1, a corner piece
applies whenever beta_i>=1/2: its corner coordinate is2*beta_i-1
and its other two coordinates are twice the corresponding beta_j.
If all beta_i<=1/2, the central triangle has barycentric coordinates
(1-2*beta_C,1-2*beta_A,1-2*beta_B). These formulas are nonnegative,
sum to one and reconstruct the original point. All equality seams
remain in the closed pieces. The checker requires all four paths and
all six signed rotation targets on every path, exactly once.

Each local contact (a,b,v,k) uses an actual endpoint v in{a,b} and
a fixed dyadic original support

    m(r)=2^k*(P_b-P_a) cross r, h(r)=m(r).P_v.

At each of the three WHOLE Delta corners it has m.r=0, equal endpoint
heights, strictly positive h and m.P_i<=h for all92 originals. These
affine inequalities extend throughout Delta. The 37 distinct endpoint
rows use twenty directed edges. All5,520 original-support comparisons
pass, including144 exact ties and24 off-endpoint grazing ties; such
weak ties are retained. Corner convexity of squared support norms and
the original vertex bounds establish throughout Delta

    ||m(r)||<2, 2*max_P||P||*max_m||m(r)||<4.            (4)

Every original physical b in r-perp has a unique representation
b=pi_r(alpha*e_y+beta*e_z), since r_x=1. An endpoint's affine wrench is

    f_v(r)=(P_v cross m(r),m_y(r),m_z(r)) in R^5.       (5)

For each receiver piece, coordinate j=0,1,2 and sign epsilon=+/-1,
the certificate gives five distinct columns A(r). Cramer's rule solves
A(r)w=epsilon*e_j. A common determinant orientation makes the degree-five
triangular Bernstein coefficients of det A and all five replaced-column
determinants strictly positive throughout that CLOSED receiver piece.
There are24 bases and24*6*21=3,024 strict positive coefficients. All
coefficient enclosures use rational intervals and outward integer
rounding at scale10^24; floating determinant signs supply no proof.

For p(z,w)=sum a_ij z^i w^j the degree-n triangular controls are

    B_kl=sum_{i<=k,j<=l} a_ij*binom(k,i)*binom(l,j)
                      /[binom(n,i+j)*binom(i+j,i)], n=5.

The corresponding nonnegative Bernstein basis sums to one on the entire
closed reference triangle. Positive denominator and numerator controls
therefore give real positive weights w_i(r) with

    sum_i w_i(r)*f_i(r)=epsilon*e_j in ALL FIVE entries. (6)

Both original translation coordinates cancel. Comparing sum-numerator
upper bounds with denominator lower bounds in the SAME Bernstein basis
gives the following uniform raw dual-mass bounds over all four pieces
and both signs:

| Coordinate | Exact uniform upper bound | Strict integer bound M_j |
|---|---|---:|
| x | 10061776203991809635513/1469960184084391499709 | 7 |
| y | 105990048588149448113249/2848877361047893119529 | 38 |
| z | 34827054245660729904214/368066778722138902213 | 95 |

If f_i.U<=0 for all selected contacts, both signs of (6) force its first
three coordinates zero. One positive nonsingular five-contact dual then
has weighted sum zero, so all five inequalities are equalities and
U=0. This proves the complete infinitesimal physical cone assertion.

## 4. Euclidean nonlinear closure and the physical gap

For a unit closed fit put d=c.c and
U=(2c_x,2c_y,2c_z,(1+d)*alpha,(1+d)*beta). At an original endpoint,
clearing the positive Cayley denominator gives

    f.U<=2*m.(d*I-c*c^t)P.                              (7)

The symmetric operator has eigenvalues d,d,0 and norm d. For c!=0,
(4) makes its right side strictly less than4d. Applying the two signed
duals gives |c_j|<2*M_j*d. Since

    M_x^2+M_y^2+M_z^2=10518<103^2,

a nonzero u=||c||_2 would satisfy1<206*u. This contradicts the entire
CLOSED collar u<=1/207. The exact squared coordinate closing bound is
14024/14283<1. At c=0 the positive nonsingular dual forces alpha=beta=0,
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

Taking the Euclidean norm and using the strict mass bound103 yields

    E>u*(1/103-2u)/(1+u^2)
      >=u*(1/103-2/207)/(1+1/207^2)
       =u*207/4413550>u/31827.                          (8)

The middle inequality uses decreasing positive numerator and increasing
positive denominator on0<u<=1/207. For the original lambda>=1 pose, an
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

Put a=1/85. Convexity and that vertex bound give

    max_{c in aD}||c||^2=(39-24*phi)/85^2<1/207^2.      (9)

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
2,104 midpoint nodes and2,212 leaves, maximum depth13. There are no failed leaves, pending regions or additional
unproved source holes. Its inner core is handled only by (9),(7).

## 7. Original translation cancellation and joint tensor signs

For each selected undyadic actual edge d_i=P_b-P_a use
m_i(r)=d_i cross r and h_i(r)=m_i(r).P_a. All5,520 actual original
support comparisons at the three whole receiver corners are checked
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
Every one of2,212*60=132,720 coefficient upper bounds is strictly
negative. Their maximum is

    -25705563724726623/100000000000000000000000<0.

Every cofactor vertex-weight lower bound is strictly positive, with
minimum762014185124199532801/125000000000000000000000.
Consequently (11)<0 on the ENTIRE closed outer-source shell and every
closed receiver in Delta. Equations (9),(7) handle the core. Undoing the
actual body fold gives Q in G and the local argument recovers original
lambda=1,b=0. Conversely every g in G supplies identical projections.
This proves (1) on Delta. Exact receiver union and the explicitly cited
three-cell theorem9442 give (1) on all of Omega.

## 8. Prior status, reproducibility and limits

Primary literature refreshed on2026-10-02 still lists pentagonal and
deltoidal hexecontahedra as the unresolved Catalan solids:
[arXiv2509.08190, Table3](https://arxiv.org/html/2509.08190), consistent
with the eleven-of-thirteen statement in
[Zeng, arXiv2604.26531, Section1.2](https://arxiv.org/html/2604.26531#S1.SS2).
The [strict projection definition](https://arxiv.org/html/2604.26531#S1.SS1)
requires interior containment. The non-Rupert theorem in
[arXiv2508.18475v2](https://arxiv.org/abs/2508.18475) concerns the
Noperthedron. Failed passage searches do not prove nonexistence; no later
global resolution of this named solid was found in the bounded refresh.

The full published complementary
[J74 rectangle9430](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/full_source_rectangle/PROOF.md),
source `ded7e6d489920315aa55034835a202675691e310`, and
[RID triangle9459](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_high_area_full_source_triangle/PROOF.md),
source `b80366e395725934a83c5d0d5d0825939de60c83`, and their original
committed bodies were read. Their ordinary contact/Euclidean closure,
whole-source and receiving-boundary interfaces are relevant method
context. Their different bodies, centrality premises, equality branches,
constants and review status do not transfer to this chiral solid.
Quaternion folding, adjugate/Cramer identities, Farkas cancellation,
midpoint coverage and Bernstein positivity are classical mechanisms;
no new general method priority is asserted.

[README.md](README.md) supplies sequential reproduction commands. The
standard-library exact code freshly rebuilds the named solid, all local
duals, actual supports, source quotient, complete closed cover and every
finite sign. The small NumPy proposal program regenerates the bulky
ignored forest; only its literal outputs after complete exact checking
enter the proof. Floating decisions and longest-edge choices supply no
mathematical inequalities. [expected.json](expected.json) records full
mathematical fingerprints, and [VALIDATION.json](VALIDATION.json) records
normal/optimized replay, resources and independent author controls.
Generated forests, coefficient streams and caches remain private.

The author controls use a separate exact Fraction double-midpoint
polarization oracle with plane cofactor minors,720 coefficient checks,
36 direct tensor identities and six actual physical translation/scale
cases. They also check rational receiver-cover inverse identities and
reject damaged coverage, contacts, phases, piece inventories, closure
bounds, hashes, clipping and a true zero source pose. They are not an
independent reviewer verdict or a formal proof assistant.

The remaining trust boundary is ordinary real convex geometry,
SO(3)/quaternion correspondence, adjugate identities, closed Bernstein
coverage and execution of the finite exact Python checker. A timeout,
undecided sign or incomplete forest supplies no theorem. The global
Rupert question and receiving directions outside the stated body images
remain unresolved by this artifact.
