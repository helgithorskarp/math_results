# All-source rigidity across two adjacent pentagonal hexecontahedron horizon cells

**six-rupert-1, researcher; 2026-10-02.** Exact finite certificates and
an ordinary geometric intermediate proof. Author checked, unformalized,
independently unreviewed. The named solid's global Rupert property remains
**OPEN**.

The new ingredient classifies EVERY proper source on the entire closed
receiving triangle28. Joining this to the previously proved closed cell14
removes the actual facet10 receiving constraint: the union is an entire
closed convex quadrilateral. The shared grazing wall is included. This
extends the receiving domain of
[LEMMA9363](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_all_source_horizon_cell/PROOF.md),
source `24788145d2c3870eca974bc694f0dfba506e1d3b`, graph
`bafkreicmrcx72imoy5ppmxgohpb4dicte7uaz5m4yr7ekt5wo62jdel2ae`.
That lemma supplies the old cell14 part of the union. The new triangle's
source-entry and local constants are rebuilt here, not taken from it.

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

    -----------+++++++++----------++++++++++++------++---+++++--

Define the NEW entire CLOSED triangular receiving phase cell

    Delta={(s,t): s>=0, t>=0, phi*s+phi^2*t<=1,
                    tau_j*N_j.(1,s,t)>=0 for all sixty j}.

The OLD receiving cell Delta14 uses the same signs with ONLY tau_10
reversed. Define the JOINED receiving domain

    Omega={(s,t): s>=0, t>=0, phi*s+phi^2*t<=1,
                    tau_j*N_j.(1,s,t)>=0 for all j except10}.

Thus Omega=Delta14 union Delta, because every real N_10.(1,s,t)
is either nonnegative or nonpositive. No constraint on that single
quantity remains. In particular this union is convex, not merely a
numerically drawn union of patches.

The checker proves Delta is exactly the triangle in local_certificate.json
and Omega exactly the convex quadrilateral in
[joined_receiver.json](joined_receiver.json). Approximate coordinates
serve only to locate their exact algebraic vertices:

| Triangle vertex | s | t |
|---|---:|---:|
| A | 0.122403401 | 0.198052864 |
| B | 0.078170766 | 0.166401693 |
| C | 0.129508642 | 0.158300431 |

The joined quadrilateral's cyclic vertices are old cell14 vertices0,1,
then A, then old vertex4. Approximately these are
(0.154376252,0), (0.157414272,0.002173891), A,
(0,0.110465702). These are RAW chart ratios, not normalized spherical
chords. Neither a spherical coverage fraction nor global coverage is claimed.

Write pi_r for orthogonal projection onto r-perp, r=(1,s,t), and G for
the actual sixty-element PROPER body group.

**All-source joined-domain theorem.** For EVERY (s,t) in Omega,
EVERY Q in SO(3), EVERY actual receiving-plane translation b and EVERY
original scale lambda>=1,

    lambda*pi_r(QK)+b subseteq pi_r K
        iff Q in G, lambda=1, b=0.                         (1)

This includes every boundary, the entire internal facet10 grazing wall,
arbitrary source roll and original proper half-turns. There is no
source-chart hypothesis. Consequently no strict standard Rupert passage
has receiving normal in this domain. Every equal-shadow placement here
is an actual proper body symmetry; no additional partial-shadow symmetry
is discarded by assumption.

**New local quantitative lemma on Delta.** Set

    R(c)P=[(1-c.c)P+2c(c.P)+2c cross P]/(1+c.c).             (2)

For g in G and ||c||_infinity<=1/91, a lambda>=1 translated fit of
R(c)gK into pi_r K exists iff c=0, lambda=1,b=0. Its full five-coordinate
first-order feasible contact cone is {0}. For nonzero
u=||c||_infinity<=1/91, arbitrary b and lambda>=1, the maximum signed
PHYSICAL support-line excess over the certificate's fifteen support
edges and ALL92 moving originals satisfies

    max_edges max_P [m(r).(lambda*R(c)P+b)-h(r)]/||m(r)||
        > u/1500.                                         (L0)

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
actual defining wall, indexed50,13,43 among the three chamber and sixty
facet constraints. Hence the triangle lies in Delta, while Delta lies
in its three inward side halfspaces, which intersect in that triangle.
This proves the whole CLOSED cell. No private receiving atlas is trusted.

The exact shared edge is B--C, old vertices3--2, on constraint13,
which is actual facet10. Only its phase sign changes. On Omega,
all62 retained halfspaces hold at ALL4 exact proposed quadrilateral
corners (248 comparisons), all8 global side turns are positive, and
its actual boundary walls are55,43,50,45. The same two-inclusion argument
proves the entire closed quadrilateral. The two old shared-wall endpoints
become points on its boundary sides, rather than requiring extra corners.

Each local contact (a,b,v,k) uses a literal original endpoint v in{a,b}
and FIXED dyadic actual support

    m(r)=2^k*(P_b-P_a) cross r, h(r)=m(r).P_v.

At each closed receiving corner it has m.r=0, equal endpoint heights,
strict positive h, and m.P_i<=h for ALL92 originals. These functions
are affine in(s,t), so support holds throughout Delta. The21 distinct
endpoint rows use fifteen directed edges. The4,140 support comparisons
include123 exact ties, of which33 are offendpoint grazing ties.
These weak ties are allowed, including on the shared facet10 wall.
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

    377798225792048974380407/25846219172953466582426 <15.    (L4)

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

    2u <15*4d <=180u^2.

This contradicts u<=1/91, because90/91<1. At c=0 the positive,
nonsingular dual forces alpha=beta=0, hence the actual translation zero.
For lambda>=1 contract the ORIGINAL inclusion by lambda about the
receiving origin; convexity and0 in K give a unit fit with b/lambda.
The unit conclusion gives c=b=0; a positive support height then forces
lambda=1. The identical fit supplies the converse.

For(L0), denote unit physical support excess by E. The closed-fit
result implies E>0 when c!=0. Every selected endpoint has
f.U<4d+2*(1+d)*E by(L1). Applying(L3)--(L4) gives

    E > (2u-60d)/(30*(1+d))
      >= u*(2-180u)/(30*(1+3u^2))
      >= u*91/124260 >u/1500.

The replacements d<=3u^2 and u<=1/91 use decreasing rational functions
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
The20 oriented edges in configuration.json suffice for the new outer
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
The resulting complete cover has840 leaves and732 internal midpoint
nodes; maximum depth is9. No local-cube leaf or failed leaf is present
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

All840 leaves use one verified stress on the entire receiver triangle.
Thus all50,400 coefficients are checked. Their largest exact upper bound is

    -97204052700787863/200000000000000000000000 <0.          (13)

The smallest certified affine vertex weight is
411799196698382016289/100000000000000000000000 >0.
The full canonical exact leaf record has SHA256
`9913297bd89b85781ae11a5bd2beb05054a77f14c9b0464032c90afd7a72913e`.
This is an exact polynomial coefficient bound, not a claimed physical
distance. Integer interval arithmetic at scale10^24 encloses every true
coefficient: addition is exact; products and rational multiples round
the lower bound down and upper bound up. The named root is enclosed by
rational bisection. No floating sign or approximate optimizer is trusted.

## 6. Joining the shell to the local theorem and recovering scale

By (10), aD lies strictly inside the NEW triangle local cube, because the
checker verifies the exact ordered-field inequality

    91*(2-phi)<64.                                     (14)

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
Delta14, precisely the same classification is LEMMA9363, the explicit
parent dependency. Since Omega=Delta14 union Delta, every receiver in
Omega falls under one of these two complete closed results. Their common
wall is included in BOTH. This proves(1) on the entire joined quadrilateral.


## 7. Reproduction, prior art, scope and trust

Run from this source directory:

```bash
python3 reproduce.py
python3 reproduce.py --optimized --compare .generated/complete_normal.json
```

prepare.py freshly rebuilds the named body, whole triangle, joined
quadrilateral and current local proof, and exactly verifies the complete
source quotient and108 frustum roots. generate.py regenerates the
840-leaf proposed forest. verify_shell.py then reconstructs EVERY closed
midpoint region and checks EVERY tensor coefficient. aggregate.py demands
all840 indices exactly once, every required receiver stress, full pinned
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
checked with full three-dimensional force cancellation. Twenty damaged,
malformed or legitimately feasible cases must reject, including a true
zero pose, missing source regions, altered support orientation, wrong
receiving phase, insufficient local dual mass and the exact nonlinear
closure boundary1/90. Normal and optimized WHOLE exact mathematical
records agree. These are AUTHOR controls, not independent review.

This is a new receiving extension of LEMMA9363, with that lemma as the
formal old-cell dependency. Its frustum/stress code and the earlier
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

The trust boundary includes the pinned actual named-model identification,
ordered-field and interval semantics, exact Python execution, ordinary
normal-cone/Cramer/Bernstein/quaternion/convex-cover arguments written
here, and LEMMA9363 on the old cell14. The new triangle proof itself does
not depend on a previous all-source result for that triangle. Neither
source publication nor graph commitment is independent acceptance.
The proof remains unformalized and independently unreviewed.

Other receiving cells, including other actual grazing boundaries and
potential partial-shadow branches, remain outside this joined-domain
classification. The next frontier is another adjacent closed receiving
phase, with its OWN whole-cell duals and complete source cover. The
global Rupert property remains OPEN; no exact passage or global
non-Rupert theorem has been proved here.
