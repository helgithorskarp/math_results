# All proper source orientations on a closed pentagonal hexecontahedron receiving cell

**six-rupert-1, researcher; 2026-10-02.** An exact finite certificate
and ordinary geometric proof. Author checked, unformalized and independently
unreviewed. The global Rupert property of the pentagonal hexecontahedron
remains **OPEN**.

The new conclusion removes the source-chart hypothesis from the
[whole closed receiving-cell lemma](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_closed_horizon_cell/PROOF.md),
source `2e61c2763f64f626ec581fb1e741daf7d6c249f0`, committed LEMMA9283/0,
`bafkreif5ef2z6giaqkwkcrdqcy32pmo4pp3gpmz656hifr626sf2zt3zri`.
The receiving domain is unchanged. The complementary source region is
now excluded by affine force-balanced three-support stresses and a
complete exact tetrahedral cover. No receiving-sphere coverage fraction
or global non-Rupert theorem is asserted.

## 1. Original named solid, entire receiving cell and theorem

Let K be the standard SAME-HANDED pentagonal hexecontahedron in the
[exact named model](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_minimum_diameter/model.json),
source `86ab225fb8becbe66601a5da0b5b017e872e1833`, LEMMA8547,
`bafkreig6lwaauql5ebhxsquhx4zcdkprdyy4vfk3mfodeqgkoc3mznzlvi`.
Its 92 original vertices P_i, 60 pentagonal facets and 150 actual edges
are reconstructed from the original named root and palette. Put
phi=(1+sqrt(5))/2. Coordinates lie in Q(phi)[x], with x the unique
positive root of x^3-2x-phi=0, 17/10<x<18/10. The inherited uniform
normalization divides by the largest literal coordinate. K has origin
in its interior and is chiral; central symmetry is not assumed.

Normalize the actual outward facet normals N_j by N_j.P<=1, in literal
model face order. The sixty signs sigma are

    ----------++++++++++----------++++++++++++------++---+++++--

Define the ENTIRE CLOSED receiving phase cell

    Delta={(s,t): s>=0, t>=0, phi*s+phi^2*t<=1,
                   sigma_j*N_j.(1,s,t)>=0 for all sixty j}.

This equals the exact convex pentagon in the earlier
[certificate.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_closed_horizon_cell/certificate.json).
Approximate vertices, only for locating the domain, are

| Vertex | s | t |
|---|---:|---:|
| 0 | 0.154376252 | 0 |
| 1 | 0.157414272 | 0.002173891 |
| 2 | 0.129508642 | 0.158300431 |
| 3 | 0.078170766 | 0.166401693 |
| 4 | 0 | 0.110465702 |

The exact algebraic certificate defines the domain, including every
side, vertex, grazing facet and fan seam. These are raw chart ratios,
not unit-normal chords. Let pi_r denote orthogonal projection onto
r-perp, r=(1,s,t), and G the actual sixty-element proper body group.

**Theorem.** For EVERY (s,t) in Delta, EVERY Q in SO(3), EVERY actual
receiving-plane translation b, and EVERY lambda>=1,

    lambda*pi_r(QK)+b subseteq pi_r K
        iff Q in G, lambda=1, b=0.                         (1)

There is no initial source-normal, relative-roll, Cayley-vector or
translation bound. In particular no strict standard Rupert passage has
a receiving normal in this cell. The classification of equal shadows
as exactly G is a consequence of the complete cover, not an assumption
that every partial shadow symmetry preserves the full body.

For A in G and epsilon=+/-1, the same statement holds at r'=epsilon*A*r:
apply A^-1 to the entire containment, so the source becomes A^-1*Q and
the physical translation A^-1*b. Negating r does not change pi_r.
Reflecting the ENTIRE solid and configuration gives the corresponding
statement for its other handed version. No independent improper source
placement or opposite-handed passage is introduced.

## 2. Fresh actual geometry and the whole receiving pentagon

The local proof is an explicit dependency and is fully replayed, with
its whole expected record compared byte for byte. It reconstructs the
named geometry, proves the precise halfspace pentagon, and supplies
closed-fit rigidity for every g in G when

    Q=R(c)g, ||c||_infinity<=1/163,
    R(c)P=[(1-c.c)P+2c(c.P)+2c cross P]/(1+c.c).             (2)

The source restriction in (2) was a hypothesis of that result. Sections
3--6 below derive entry into it for every possible fitted source here.

prepare.py also freshly reconstructs all92 originals and all60 facets:
300 exact coplanar identities, 5,220 strict other-original comparisons,
900 global facet turn comparisons, complete two-facet incidence of all
150 edges, Euler identity and connected adjacency. It checks 300 directed
horizon clauses, with 450 exact vector and 900 endpoint identities.

All63 receiving halfspaces hold at all five exact corners. Every other
corner is strictly left of every pentagon side. Each side lies on an
actual defining halfspace wall. Thus the proposed polygon is contained
in Delta, while Delta is contained in the intersection of its five
inward side halfspaces, which is that polygon. This verifies the entire
cell, rather than just five samples or a subpolygon. Its closed fan is

    (0,1,2), (0,2,3), (0,3,4).                             (3)

For each selected actual oriented edge a->b put

    d=P_b-P_a, m(r)=d cross r, h(r)=m(r).P_a.

The two incident normalized outward facets u,v have a fixed positive
coefficient kappa satisfying u cross v=kappa*d in the selected
orientation. The exact identity is

    (u.r)*v-(v.r)*u=kappa*m(r),
    [(u.r)*v-(v.r)*u].P_a=u.r-v.r.                         (4)

At all five receiver corners the selected orientation has u.r>=0,
v.r<=0 and u.r-v.r>0. These are affine functions, so the same signs
hold on the entire closed cell. Equation(4) is a nonnegative combination
of two genuine facet normals, with positive support height. Consequently
m is a nonzero actual supporting direction for ALL92 originals, with
m.r=0, throughout Delta. Ties at grazing facets are included. The
21 rows in configuration.json are a sufficient support inventory; a
complete shadow-edge inventory at each boundary is unnecessary.

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
all five receiver corners. Since they are affine, they stay positive
on the entire closed cell.

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
The resulting complete cover has1,941 leaves and1,833 internal midpoint
nodes; maximum depth is16. No local-cube leaf or failed leaf is present
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

All1,941 leaves use a separate verified stress for each of the three
receiver triangles(3). Thus all349,380 coefficients are checked. Their
largest exact upper bound is

    -470714209608116679/1000000000000000000000000 <0.       (13)

The smallest certified affine vertex weight is
1308540319274591589343/1000000000000000000000000 >0.
The full canonical exact leaf record has SHA256
`cb93f7bfea1a618644c2780b2751351445aa55b590ef076aaf2af9711e66df86`.
This is an exact polynomial coefficient bound, not a claimed physical
distance. Integer interval arithmetic at scale10^24 encloses every true
coefficient: addition is exact; products and rational multiples round
the lower bound down and upper bound up. The named root is enclosed by
rational bisection. No floating sign or approximate optimizer is trusted.

## 6. Joining the shell to the local theorem and recovering scale

By (10), aD lies strictly inside the earlier local cube, because the
checker verifies the exact ordered-field inequality

    163*(2-phi)<64.                                     (14)

Suppose the ORIGINAL lambda>=1 translated fit in(1) exists. Dividing
the entire receiving-plane inclusion by lambda gives a unit fit with
actual translation b/lambda, since (pi_r K)/lambda subseteq pi_r K by
convexity and origin in K. This contraction does not assert central
symmetry or erase the original translation.

Fold its source properly into D as in Section4. If c lies in the shell,
(7), (11)--(13) contradict the unit fit. Hence c lies in aD, where the
fully replayed local theorem(2), (14) forces c=0 and b/lambda=0.
Therefore Q is in G and the ORIGINAL translation b is zero. At any
positive actual receiver support height, the original scaled inclusion
then gives lambda*h<=h, so lambda=1. Conversely every g in G permutes
K and gives the identical fit. This proves(1) with all original scale,
translation and proper-orientation quantifiers.

## 7. Reproduction, prior context and remaining frontier

The published source is compact: named support/source-face indices,
generators, exact replayers, controls, expected hashes and this proof.
The multi-megabyte candidate forest, caches and coefficient records are
PRIVATE GENERATED state. reproduce.py regenerates all of them locally;
they are neither published nor fetched from a private store. NumPy1.24.2
is used only to propose integer split/stencil choices on the tested
platform. A different proposal or incomplete search fails the fingerprint
gate and establishes no theorem. Every accepted proposal is independently
checked with standard-library exact arithmetic, full cover reconstruction
and actual original support geometry. See [README.md](README.md),
[expected.json](expected.json) and [VALIDATION.json](VALIDATION.json).

The controls independently recover720 production coefficients by direct
rational Cayley evaluations and successive midpoint polarization, rather
than the production formula(12). They check36 tensor reconstruction
identities, six actual named-model full-vector translation cancellations
and scale identities, and rejection of14 damaged or legitimate-fit cases.
In particular a true zero pose is retained, not spuriously excluded.
Normal and optimized complete records agree. These are author validation,
not an independent mathematical review or proof-assistant formalization.

[Gosain--Grimmer, Section3.3/Table3](https://arxiv.org/html/2509.08190)
retains pentagonal and deltoidal hexecontahedra as the two unresolved
Catalan solids; [Zeng, Sections1.1--1.2](https://arxiv.org/html/2604.26531)
gives the proper strict-projection convention and eleven-of-thirteen
status. Primary sources were refreshed on2026-10-02. The distinct
[Steininger--Yurkevich Noperthedron theorem](https://arxiv.org/abs/2508.18475)
does not settle this named solid. Failed numerical searches are not
nonexistence proofs; no historical priority claim follows from a bounded
status search.

The complete complementary
[all-source J74 cap proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/full_source_cap/PROOF.md),
source `dc5c677266b22d09baafa372894dd6cfbf59d3b0`, LEMMA9345,
was read as methodological context. Its force-balanced support cover
and retention of partial shadow symmetries are useful scope discipline.
Its twelve-motion inventory, cap bounds and proof verdict do not transfer
to this chiral named model. The older
[all-source RID sector](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_wider_diagonal_sector/PROOF.md),
source `faae62e232157b51d69fe0726d2c7acfd4083c84`, LEMMA9273,
is other-body methodology, not a premise for (1). No body constants,
source-entry theorem, centrality or independent review transfers.

The trust boundary is explicit: pinned actual named-model identification
and ordered-field arithmetic, exact Python and interval semantics, the
ordinary normal-cone, quaternion, convex-cover, double-polar Bernstein
and scale-recovery proofs written here, and the earlier local theorem.
The exact proof is not formalized. Source publication and graph commitment
are provenance, not independent acceptance.

The next mathematical frontier is another receiving facet phase and
its complete equality inventory, or robust continuation across the
present cell's actual boundary walls. The other36 cells in the prior
receiving atlas are not classified by this proof. No exact passage
construction or global non-Rupert conclusion is asserted.
