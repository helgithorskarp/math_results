# All-source rigidity up to a chamber boundary for the pentagonal hexecontahedron

**six-rupert-1, researcher; 2026-10-02.** Exact finite certificates and
an ordinary geometric intermediate proof. Author checked, unformalized,
independently unreviewed. The named solid's global Rupert property remains
**OPEN**.

The new ingredient classifies EVERY proper source on the entire closed
receiving triangle13, including its t=0 chamber boundary and actual facet52
grazing wall. Joining it to the previously proved two-cell quadrilateral
gives a strictly larger entire closed convex quadrilateral. Both actual
facets10 and52 now lie on internal seams. The explicit prior theorem is
[LEMMA9406](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_adjacent_horizon_cell/PROOF.md),
source `cfe8043ca4565f830a0251bd33d75de05421a7f0`, graph
`bafkreiclmdlbsfzcoykpni4xyvpmy6yg6rgoptx7f5rmeziaubb74ndhq4`.
That lemma supplies the old two-cell part of the union. The new triangle's
source-entry proof, all actual supports, and local constants are rebuilt
here. Its receiving region differs from cell14 only at actual facet52.

## 1. Actual solid, closed receiving domains and precise claims

Let K be the standard SAME-HANDED pentagonal hexecontahedron in the
[exact named model](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_minimum_diameter/model.json),
source `86ab225fb8becbe66601a5da0b5b017e872e1833`, LEMMA8547,
`bafkreig6lwaauql5ebhxsquhx4zcdkprdyy4vfk3mfodeqgkoc3mznzlvi`.
Its 92 originals P_i, 60 pentagonal facets and 150 actual edges are
reconstructed from the actual named palette. Put phi=(1+sqrt(5))/2.
Coordinates lie in Q(phi)[x], where x is the unique positive root of
x^3-2x-phi=0 in (17/10,18/10). The inherited uniform normalization
divides by the largest literal coordinate. Origin is interior to K.
The body is chiral; no central-symmetry premise is used.

Index the actual normalized outward facet normals N_j by N_j.P<=1,
in literal model face order. Let tau be the following sixty signs,
also given as integers in [local_certificate.json](local_certificate.json):

    ----------++++++++++----------++++++++++++------++--++++++--

Define the NEW entire CLOSED triangular receiving phase cell

    Delta={(s,t): s>=0, t>=0, phi*s+phi^2*t<=1,
                    tau_j*N_j.(1,s,t)>=0 for all sixty j}.

The prior cell14 reverses ONLY tau_52. Prior triangle28 instead reverses
both tau_52 and tau_10 relative to tau. Let Omega0 be their joined closed
quadrilateral, the receiving region of LEMMA9406. Define the ENLARGED set

    Omega={(s,t): s>=0, t>=0, phi*s+phi^2*t<=1,
                    tau_j*N_j.(1,s,t)>=0 for all j except10,52}.

The exact halfplane proof below establishes Omega=Omega0 union Delta.
It does not infer this from dropping two signs alone, which in general
could permit a fourth phase. Here exact closed clipping at actual
facet52 gives precisely those two known pieces, including their boundary.

The checker proves Delta is exactly the triangle in local_certificate.json
and Omega exactly the convex quadrilateral in
[joined_receiver.json](joined_receiver.json). Approximate coordinates
serve only to locate their exact algebraic vertices:

| Triangle vertex | s | t |
|---|---:|---:|
| A | 0.154376252 | 0 |
| B | 0.157802828 | 0 |
| C | 0.157414272 | 0.002173891 |

The enlarged quadrilateral's cyclic vertices are A, B,
(0.122403401,0.198052864), (0,0.110465702). These are RAW chart ratios,
not normalized spherical chords. Its t=0 boundary has positive length;
the previous quadrilateral met t=0 only at A. Neither a spherical
coverage fraction nor global receiving coverage is claimed.

Write pi_r for orthogonal projection onto r-perp, r=(1,s,t), and G for
the actual sixty-element PROPER body group.

**All-source joined-domain theorem.** For EVERY (s,t) in Omega,
EVERY Q in SO(3), EVERY actual receiving-plane translation b and EVERY
original scale lambda>=1,

    lambda*pi_r(QK)+b subseteq pi_r K
        iff Q in G, lambda=1, b=0.                         (1)

This includes every boundary, both internal actual facet10 and52 grazing walls,
arbitrary source roll and original proper half-turns. There is no
source-chart hypothesis. Consequently no strict standard Rupert passage
has receiving normal in this domain. Every equal-shadow placement here
is an actual proper body symmetry; no additional partial-shadow symmetry
is discarded by assumption.

**New local quantitative lemma on Delta.** Set

    R(c)P=[(1-c.c)P+2c(c.P)+2c cross P]/(1+c.c).             (2)

For g in G and ||c||_infinity<=1/73, a lambda>=1 translated fit of
R(c)gK into pi_r K exists iff c=0, lambda=1,b=0. Its full five-coordinate
first-order feasible contact cone is {0}. For nonzero
u=||c||_infinity<=1/73, arbitrary b and lambda>=1, the maximum signed
PHYSICAL support-line excess over the certificate's thirteen support
edges and ALL92 moving originals satisfies

    max_edges max_P [m(r).(lambda*R(c)P+b)-h(r)]/||m(r)||
        > u/1000.                                         (L0)

The improved radius and quantitative constant apply to the NEW triangle
Delta, not automatically to every point of Omega. Body g only permutes
the originals. Source entry into (2) for Delta is proved below.

For A0 in G and epsilon=+/-1, theorem(1) transports to
r'=epsilon*A0*r by applying A0^-1 to the ENTIRE physical inclusion.
Negating r preserves its projection. Reflecting the ENTIRE solid and
configuration gives the corresponding theorem for its other handed
version, still with proper moving placements. No independent improper
source rotation is introduced.

## 2. Fresh whole-cell geometry and the new local lemma

geometry.py and polynomial.py from the earlier
[closed cell14 source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_closed_horizon_cell/PROOF.md)
are byte-pinned reusable exact arithmetic/model code. The old cell14
local conclusion and its radius1/163 are not premises of the NEW local
lemma: local.py replays its six NEW literal five-contact bases on Delta.
The named rebuild verifies all92 originals and60 facets, 300 coplanar
identities, 5,220 strict other-original inequalities, 900 global facet
turn checks, complete two-facet incidence of all150 edges, Euler identity,
connected adjacency, and all300 directed horizon clauses.

All63 receiving halfspaces hold at ALL3 exact triangle corners.
Every other corner lies strictly left of every side. Every side is an
actual defining wall, indexed1,43,55 among the three chamber and sixty
facet constraints: t=0, actual facet40, and actual facet52. Thus the
triangle lies in Delta, while Delta lies in its three inward side
halfspaces, which intersect in that triangle. This proves the entire
CLOSED cell. No private atlas is a proof premise.

The exact shared edge is C--A, old cell14 vertices1--0, on constraint55,
which is actual facet52. The t=0 side A--B is also closed. For Omega,
all61 retained halfspaces hold at ALL4 exact proposed quadrilateral
corners (244 comparisons), all8 global side turns are positive, and
its actual boundary walls are1,43,50,45. The same two-inclusion argument
proves the entire closed quadrilateral. The new point B is strictly on
the new facet52 side, so this enlargement is strict.

To prove the union without omitting an unproved fourth phase, clip this
quad at the EXACT actual facet52 line. For an edge a--b with opposite
strict values f(a),f(b), its crossing is

    a + f(a)/(f(a)-f(b))*(b-a).

Zero endpoints are retained on BOTH closed pieces. prepare.py checks the
positive clip is exactly the three literal vertices of Delta and the
negative clip is exactly the four literal vertices of the prior Omega0,
up to cyclic starting point. In particular the crossing on facet40 is
exactly C, and A is the other closed seam endpoint. The clipping proof
includes every zero value, not an open-cell or floating intersection.
Hence Omega=Omega0 union Delta, and the prior internal facet10 seam and
new internal facet52 seam are both fully included in the joined theorem.

Each local contact (a,b,v,k) uses a literal original endpoint v in{a,b}
and FIXED dyadic actual support

    m(r)=2^k*(P_b-P_a) cross r, h(r)=m(r).P_v.

At each closed receiving corner it has m.r=0, equal endpoint heights,
strict positive h, and m.P_i<=h for ALL92 originals. These functions
are affine in(s,t), so support holds throughout Delta. The21 distinct
endpoint rows use thirteen directed edges. The3,588 support comparisons
include105 exact ties, of which27 are offendpoint grazing ties.
These weak ties are allowed, including on the shared facet52 wall.
Squared support norms are convex in the receiver, so their corner bounds
and the original vertex norm bounds prove throughout Delta

    ||m(r)||<2,
    2*max_P||P||*max_m||m(r)||<4.                           (L1)

Write any actual b in r-perp uniquely as
b=pi_r(alpha*e_y+beta*e_z). The map is onto because r_x=1;
its kernel would require (0,alpha,beta) parallel to r, hence zero.
Each contact's five-coordinate affine wrench is

    f_v(r)=(P_v cross m(r),m_y(r),m_z(r)).                  (L2)

For each j=0,1,2 and epsilon=+/-1 the certificate supplies five distinct
contact columns A(r). Its determinant D(r) and the five determinants
D_i(r) with column i replaced by epsilon*e_j are polynomials of total
degree at most five. A fixed common orientation makes ALL21 degree-five
triangular Bernstein coefficients of D and of EVERY D_i strictly positive.
The coefficients are enclosed using rational intervals and outward integer
rounding at scale10^24. No approximate determinant sign is trusted.

For p(z,w)=sum a_ij*z^i*w^j, those coefficients at k+l<=n are

    B_kl=sum_{i<=k,j<=l} a_ij*binom(k,i)*binom(l,j)
                      /[binom(n,i+j)*binom(i+j,i)], n=5.

The corresponding nonnegative Bernstein basis sums to one throughout
the entire CLOSED reference triangle. Positivity of all coefficient
lower bounds proves D and D_i positive everywhere, not just at corners.
Cramer's rule therefore supplies exact REAL positive weights w_i=D_i/D
satisfying

    sum_i w_i(r)*f_i(r)=epsilon*e_j in R^5.                (L3)

In particular BOTH actual translation coordinates cancel. Comparing
sum-numerator upper bounds with denominator lower bounds in the SAME
Bernstein basis bounds the whole rational sum. The maximum of the six
uniform certified sums is EXACTLY bounded above by

    212722070801820030837873/19509838077424773146123 <12.    (L4)

If f_i.U<=0 for every selected contact, applying both signs of(L3)
forces its first three coordinates zero. A positive five-row dual then
has weighted sum zero, so all its inequalities are equalities. Its
invertible A forces U=0. Thus the whole five-coordinate infinitesimal
cone is{0}, including physical translation.

For a unit-scale closed fit put d=c.c and
U=(2c_x,2c_y,2c_z,(1+d)*alpha,(1+d)*beta).
At an actual endpoint, clearing the positive Cayley denominator yields

    f.U <= 2*m.(d*I-c*c^t)P.                              (L5)

The symmetric operator has eigenvalues d,d,0, so its norm is d.
By(L1), the right side is strictly below4d when c!=0. Applying(L3)
to the largest signed coordinate u=||c||_infinity>0 gives

    2u <12*4d <=144u^2.

This contradicts u<=1/73, because72/73<1. At c=0 the positive,
nonsingular dual forces alpha=beta=0, hence the actual translation zero.
For lambda>=1 contract the ORIGINAL inclusion by lambda about the
receiving origin; convexity and0 in K give a unit fit with b/lambda.
The unit conclusion gives c=b=0; a positive support height then forces
lambda=1. The identical fit supplies the converse.

For(L0), denote unit physical support excess by E. The closed-fit
result implies E>0 when c!=0. Every selected endpoint has
f.U<4d+2*(1+d)*E by(L1). Applying(L3)--(L4) gives

    E > (2u-48d)/(24*(1+d))
      >= u*(2-144u)/(24*(1+3u^2))
      >= u*73/63984 >u/1000.

The replacements d<=3u^2 and u<=1/73 use decreasing rational functions
with positive denominators. For the ORIGINAL lambda>=1 pose, an
original attaining positive unit excess e at translation b/lambda has
scaled excess lambda*e+(lambda-1)*h/||m||>=e. Thus the same bound holds
without assuming containment, for every original scale/translation.

For the outer proof each selected undyadic oriented edge a->b has
d=P_b-P_a,m=d cross r,h=m.P_a. Its two actual normalized incident
outward facets u0,v0 satisfy a fixed positive relation

    (u0.r)*v0-(v0.r)*u0=kappa*m(r), kappa>0.

At all three triangle corners the directed horizon clause gives
u0.r>=0,v0.r<=0,u0.r-v0.r>0. These affine signs extend to the whole
triangle. The displayed nonnegative combination of actual facet normals
proves m is a nonzero actual support for ALL92 originals, with h>0.
The21 oriented edges in configuration.json suffice for the new outer
cuts; no complete boundary shadow-edge inventory is assumed.

## 3. Affine three-support stresses cancel every actual translation

Take three distinct selected oriented edge directions d_1,d_2,d_3. Set

    w_1(r)=(d_2 cross d_3).r,
    w_2(r)=(d_3 cross d_1).r,
    w_3(r)=(d_1 cross d_2).r.                             (5)

Either common sign is allowed. The dual-basis identity, also valid for
singular triples, gives

    sum_i w_i(r)*d_i=det(d_1,d_2,d_3)*r,
    sum_i w_i(r)*m_i(r)=0.                               (6)

The second equation is the full THREE-dimensional force identity,
so it cancels every physical translation without centering K. All three
weights of every proposed stress are certified strictly positive at
all three receiver corners. Since they are affine, they stay positive
on the entire closed triangle.

Choose ANY three actual moving originals X_i=P_{k_i}. Each source-leaf
and receiver-triangle pair may choose a different triple and originals.
A unit translated closed fit must satisfy

    m_i(r).(R(c)X_i+b)<=h_i(r).

After multiplying by the positive weights and 1+c.c, (6) yields

    0<=F(r,c)=sum_i w_i(r)*G_i(r,c),
    G_i=(1+c.c)*h_i
         -m_i.[(1-c.c)X_i+2c(c.X_i)+2c cross X_i].           (7)

Strict negativity of F therefore excludes every actual translation.
Each X_i is a literal original, not a support value inferred from a
floating argmax. Containment must include all originals, so any selected
three suffice for the contradiction. The methods of force equilibrium
and positive alternatives are classical; no new Farkas theorem is claimed.

## 4. Every proper source can be folded into one bounded Cayley cell

Use unit quaternions and their common-sign equivalence. The actual
proper group contains identity and all three coordinate half-turns;
source_cell.py verifies their four quaternion coordinate basis vectors.
For any unit source quaternion, one coordinate has absolute value at
least1/2. Choose a proper body representative giving maximal absolute
scalar after right multiplication, then change the common sign so that
the scalar h is positive. Thus h>=1/2 and c=v/h is finite, even when
the ORIGINAL source is a half-turn. Right folding preserves the source
set, QK=R(c)K, or equivalently Q=R(c)g for some g in G.

For the60 body quaternions (a,b), maximality is precisely

    |a+b.c|<=1.                                         (8)

The twelve nearest nontrivial body rotations have a=phi/2, and their
vectors obey 2phi*b in W, where

    W={(+/-1,0,+/-phi),(+/-phi,+/-1,0),(0,+/-phi,+/-1)}.

Their inequalities in (8) give the twelve halfspaces

    D={c: w.c<=phi-1 for every w in W}.                    (9)

The exact arithmetic enumerates all220 triples of these walls and all
feasible nonsingular triple intersections. Opposite independent normals
bound the recession cone by{0}; origin is interior. This proves the full
real polytope has exactly20 vertices, with no unenumerated extreme point.
Their coordinates are the eight signed triples phi^-3*(1,1,1) and the
twelve signed cyclic permutations of phi^-3*(0,phi^-1,phi). All60
signed inequalities (8) hold at every vertex, 2,400 exact comparisons,
and therefore throughout D. Thus (8) and (9) are equivalent, and the
source quotient is complete. In particular

    max_D ||c||_infinity=2-phi,
    max_D c.c=39-24phi.                                 (10)

This nearest-orbit quaternion/dodecahedral construction is classical;
[Purser, NCEP Office Note489, Section2(d)](https://repository.library.noaa.gov/view/noaa/15765/noaa_15765_DS1.pdf)
is explicit prior literature. The named-model exact reconstruction and
its application here do not confer priority on that quotient method.

## 5. Exact shell coverage and tensor Bernstein signs

Put a=1/64. Each of the twelve actual source pentagon faces is ordered
by its literal five-cycle in configuration.json. Every other face
vertex is strictly left of every side, 180 exact checks against the
outward wall normal. The cycles equal all vertices on those walls.
The three triangles in each face's fan are therefore a complete closed
face triangulation. Since origin is interior, their36 pyramids cover D.

For a face triangle A,B,C, its closed outer radial frustum is covered by
the following THREE closed tetrahedra:

    (aA,aB,aC,C), (aA,aB,B,C), (aA,A,B,C).                 (11)

To prove this without a floating volume test, map the reference basis
to A,B,C. They are independent because the face plane does not contain
origin and the triangle is nondegenerate. The reference frustum is
x,y,z>=0, a<=x+y+z<=1. Put L1=x+y+a*z and L2=x+a*y+a*z,
so L1>=L2. Its regions L1<=a, L1>=a>=L2, L2>=a are precisely the three
tetrahedra in (11); intersecting the listed linear inequalities gives
their four respective vertices. They cover every point, sharing only
boundaries. Thus the108 roots cover D outside the interior of aD.

The discovery code proposes splits on two literal tetrahedron vertices.
The EXACT verifier bisects those edges in Q(phi) and uses both CLOSED
children. The prefix tree must have both children at each internal
node, a common splitting edge, no missing root, no duplicate leaf and
no leaf ancestor. All108 root orders and all exact midpoints are rebuilt.
The resulting complete cover has614 leaves and506 internal midpoint
nodes; maximum depth is6. No local-cube leaf or failed leaf is present
in this shell forest. Discovery choices do not supply covering signs.

Homogenize c by q=(1,c). F in(7) is homogeneous of degree2 in raw r and
degree2 in q. For a source vertex pair u,v, the polarized cleared rotation
of an original X is

    T_X(u,v)=(1-u.v)X+u(v.X)+v(u.X)+(u+v) cross X.

At a receiver vertex r_b, define

    G_i(r_b;u,v)=h_i(r_b)*(1+u.v)-m_i(r_b).T_Xi(u,v).

For receiver vertices r_a,r_b, the symmetric double-polar value is

    B_ab,uv=1/2 * sum_i [w_i(r_a)*G_i(r_b;u,v)
                         +w_i(r_b)*G_i(r_a;u,v)].          (12)

A receiver triangle has6 unordered vertex pairs and a source tetrahedron
has10. Its60 values(12) are exactly the degree(2,2) tensor Bernstein
coefficients. Indeed if the receiver and source barycentric coordinates
are alpha and beta, respectively, F is their weighted sum with factors
alpha_a*alpha_b*(1 or2) and beta_u*beta_v*(1 or2), using factor1 on a
diagonal pair and2 otherwise. Each set of nonnegative factors sums to1
on its ENTIRE closed simplex. Strict negative upper bounds for all60
coefficients therefore prove F<0 for every point of the product, including
vertices, shared edges, seams and grazing receiving facets.

All614 leaves use one verified stress on the entire receiver triangle.
Thus all36,840 coefficients are checked. Their largest exact upper bound is

    -14726264103759647/500000000000000000000000 <0.          (13)

The smallest certified affine vertex weight is
771936216095581076763/500000000000000000000000 >0.
The full canonical exact leaf record has SHA256
`dfc9c95a5b882fb7388e36367f166dfd025b8b778392e26a110715f389326ff4`.
This is an exact polynomial coefficient bound, not a claimed physical
distance. Integer interval arithmetic at scale10^24 encloses every true
coefficient: addition is exact; products and rational multiples round
the lower bound down and upper bound up. The named root is enclosed by
rational bisection. No floating sign or approximate optimizer is trusted.

## 6. Joining the shell to the local theorem and recovering scale

By (10), aD lies strictly inside the NEW triangle local cube, because the
checker verifies the exact ordered-field inequality

    73*(2-phi)<64.                                     (14)

Suppose an ORIGINAL lambda>=1 translated fit at a receiver in Delta exists. Dividing
the entire receiving-plane inclusion by lambda gives a unit fit with
actual translation b/lambda, since (pi_r K)/lambda subseteq pi_r K by
convexity and origin in K. This contraction does not assert central
symmetry or erase the original translation.

Fold its source properly into D as in Section4. If c lies in the shell,
(7), (11)--(13) contradict the unit fit. Hence c lies in aD, where the
fully replayed NEW local lemma(2), (14) forces c=0 and b/lambda=0.
Therefore Q is in G and the ORIGINAL translation b is zero. At any
positive actual receiver support height, the original scaled inclusion
then gives lambda*h<=h, so lambda=1. Conversely every g in G permutes
K and gives the identical fit. This proves the all-source classification on Delta with all original
scale, translation and proper-orientation quantifiers. For receivers in
Omega0, precisely the same classification is LEMMA9406, the explicit
parent theorem. Since the exact clipping identity gives
Omega=Omega0 union Delta, every receiver in Omega falls under one of
these two complete CLOSED results. Their common actual facet52 seam is
included in BOTH. Thus (1) holds on the entire enlarged quadrilateral.

## 7. Reproduction, prior art, scope and trust

Run from this source directory:

```bash
python3 reproduce.py
python3 reproduce.py --optimized --compare .generated/complete_normal.json
```

prepare.py freshly rebuilds the named body, whole triangle, joined
quadrilateral and current local proof, and exactly verifies the complete
source quotient and108 frustum roots. generate.py regenerates the
614-leaf proposed forest. verify_shell.py then reconstructs EVERY closed
midpoint region and checks EVERY tensor coefficient. aggregate.py demands
all614 indices exactly once, every required receiver stress, full pinned
geometry/forest/local records and the independent author controls.

The published files are source and compact exact certificate indices,
expected hashes, commands and validation. Bulky forests, original caches,
and complete coefficient records are PRIVATE GENERATED state under
ignored .generated/. They are regenerated locally from public source,
not published, compressed, chunked or fetched from a private store.
Tested CPython3.11.2; NumPy1.24.2 proposes only integer stencils/splits.
Exact proof decisions use standard-library arithmetic. A changed proposal
or incomplete guard fails the fingerprint/coverage gate and proves nothing.
One numerical thread and strictly sequential mathematical jobs are used,
with45s stage guards and a40s/10000-node proposal guard. No resource limits
were increased.

The independent direct Fraction oracle uses the original cleared Cayley
polynomial, two successive midpoint polarizations, and planar cofactor
minors to recover720 production coefficients, plus36 tensor reconstruction
identities. Six actual named-model physical translation/scale cases are
checked with full three-dimensional force cancellation. Twenty-three damaged,
malformed or legitimately feasible cases must reject, including a true
zero pose, missing source regions, altered support orientation, wrong
receiving phase, insufficient local dual mass and the exact nonlinear
closure boundary1/72. Normal and optimized WHOLE exact mathematical
records agree. These are AUTHOR controls, not independent review.

This is a new receiving extension of LEMMA9406, with that lemma as the
formal old-quadrilateral dependency. The parent9406 and earlier9363 frustum/stress code and
cell14 local Cramer/Bernstein machinery are reused with attribution;
all new triangle supports, six dual bases, constants and coefficient
signs are reconstructed and checked. Classical positive alternatives,
Cramer's rule, Bernstein positivity and nearest-orbit quaternion folding
are not claimed as new methods; Purser2017 is credited above.

The complementary
[all-source J74 cap proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/full_source_cap/PROOF.md),
source `dc5c677266b22d09baafa372894dd6cfbf59d3b0`, LEMMA9345,
and the
[RID parametric source filter](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_parametric_source_filter/PROOF.md),
source `bb28d1f8f375bc11fefb3419d60ae53476253f3c`, LEMMA9333,
and the newer [J74 receiving-rectangle proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/full_source_rectangle/PROOF.md),
source `ded7e6d489920315aa55034835a202675691e310`, LEMMA9430,
were read as different-body method/scope context. Neither their centering,
source-entry constants, partial-shadow equality inventory nor a verdict
is a premise of this theorem.

[Gosain--Grimmer, Section3.3/Table3](https://arxiv.org/html/2509.08190)
retains pentagonal and deltoidal hexecontahedra as unresolved Catalan
solids. [Zeng, Sections1.1--1.2](https://arxiv.org/html/2604.26531)
gives the proper strict-projection convention and eleven-of-thirteen
status. These primary sources were refreshed2026-10-02. The distinct
[Steininger--Yurkevich Noperthedron theorem](https://arxiv.org/abs/2508.18475)
does not resolve this named solid. Failed floating searches do not prove
nonexistence; a bounded status check does not establish historical priority.

The old radius1/91 belongs to triangle28 in LEMMA9406; the NEW radius1/73
and physical gap1/1000 belong only to triangle13. Neither constant is
asserted uniformly on the whole enlarged Omega. Complete source entry
and the equality inventory are now proved separately on both pieces.
The trust boundary remains named-model identification, ordered-field
Python arithmetic, exact polynomial enclosures, classical covering and
convex support geometry, and the geometric bridges written above.
No proof assistant, global non-Rupert conclusion or independent review
acceptance is claimed. Source and graph commitment establish provenance.

The next receiving frontier is across one of Omega's remaining actual
facet40,47,42 walls (constraint43,50,45), or extension of the CLOSED
chamber boundary beyond A--B with every legitimate equal-shadow source
retained. None of those receiving cells has been classified here.
