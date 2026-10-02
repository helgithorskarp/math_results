# Pentagonal all-source rigidity on ten literal closed receiving cells

**six-rupert-1, researcher; 2026-10-02.** Ordinary intermediate geometric proof
with a complete exact finite certificate. Author checked, unformalized and
independently unreviewed. The standard SAME-HANDED pentagonal hexecontahedron's
global Rupert status remains **OPEN**.

## 1. Original statement and exact receiving domains

Let K be the standard SAME-HANDED pentagonal hexecontahedron in the actual
92-original normalization of [model8547](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_minimum_diameter/model.json),
source `86ab225fb8becbe66601a5da0b5b017e872e1833`, graph
`bafkreig6lwaauql5ebhxsquhx4zcdkprdyy4vfk3mfodeqgkoc3mznzlvi`.
Let G be its actual proper sixty-element body group, and N_j its sixty actual
normalized outward facet normals, in the published literal order. Origin is
interior. The ordered field is Q(phi)[x], phi=(1+sqrt(5))/2,
x^3=2x+phi at the isolated positive root in(17/10,18/10).
A coefficient triple [[a0,b0],[a1,b1],[a2,b2]] denotes
sum_i(ai+bi*phi)*x^i; the normalization and palette are the cited model's.

For each k in{19,18,16,33}, [certificates.json](certificates.json) supplies
its sixty signs tau_j and ALL exact cyclic receiving vertices. Define

    C_k={(s,t): s>=0, t>=0, phi*s+phi^2*t<=1,
                    tau_j*N_j.(1,s,t)>=0 for every actual j}.

The literal sixty-sign strings in original facet order are:

    19: ----------++++++++++----------++++++++++-+------++--++++++--
    18: ----------++++++++++----------++++++++++-+------+++--+++++--
    16: ----------++++++++++----------++++++++++-+------+++-++++++--
    33: -----------+++++++++----------++++++++++-+------+++--+++++--

These are the ENTIRE closed triangle19, quadrilateral18, quadrilateral16 and
pentagon33. Their literal names are fixed by these exact signs/vertices; a
native atlas index is only a label. After the three chamber inequalities,
side-wall constraint i>=3 is actual facet i-3. The complete cyclic side walls are

| cell | corners/fans | defining constraint indices | actual facet walls |
|---|---|---|---|
| 19 | 3/1 | 53,55,43 | 50,52,40 |
| 18 | 4/2 | 13,53,55,62 | 10,50,52,59 |
| 16 | 4/2 | 1,62,55,53 | t=0,59,52,50 |
| 33 | 5/3 | 12,8,53,13,62 | 9,5,50,10,59 |

Let Omega6 be ONLY the literal six-cell receiving union14,28,13,11,20,34 of
[lemma9604](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_facet10_quad/PROOF.md),
source `9d69be73ed1e121ed53701d6c21843f0fc7c4649`, committed graph
`bafkreibjv2ro5vhr7ggonpnjsrbxuh7vero7ythgvlbt4ooenrt6uzlipa`.
Its full ordinary proof and literal receiver union are explicit dependencies.
Put Omega=Omega6 UNION C19 UNION C18 UNION C16 UNION C33.
This is a LITERAL closed union, not its convex hull or a measure fraction.
No earlier local constants are transferred to the four new regions.

For r=(1,s,t), n=r/||r|| and pi_r=I-nn^T:

**Lemma.** For EVERY(s,t) in Omega, EVERY ORIGINAL Q in SO(3), EVERY
ORIGINAL physical b in r-perp, and EVERY ORIGINAL lambda>=1,

    lambda*pi_r(QK)+b subseteq pi_r(K)
        IFF Q belongs to G, b=0, lambda=1.                 (1)

Thus none of these receiving directions admits a strict standard Rupert
passage. Every original roll/half-turn, every receiving roll, all polygon
sides/corners/diagonals, all original facet ties, the full physical translation
and enlargement are retained. There is no assumed source localization or
assumed complete equal-shadow list. Equality is the CONCLUSION of the proof.
The conclusion transports to every signed/projective proper G receiving image.
No source reflection, centrality or left moving H_n quotient is used for K.

The four new quantitative local lemmas use the following separate constants:

| cell | strict coordinate masses M | N, sum M_j^2<N^2 | closed Cayley rho | squared closure | physical gap >u times | source core a |
|---|---|---|---|---|---|---|
| 19 | (4,9,8) | 13,161<169 | 1/27 | 644/729 | 1/507 | 1/12 |
| 18 | (9,21,12) | 26,666<676 | 1/53 | 2664/2809 | 1/2028 | 1/22 |
| 16 | (7,18,11) | 23,494<529 | 1/47 | 1976/2209 | 1/1587 | 1/20 |
| 33 | (6,9,9) | 15,198<225 | 1/31 | 792/961 | 1/675 | 1/13 |

Here u=||c||_2 and R(c)P=[(1-c.c)P+2c(c.P)+2c cross P]/(1+c.c).
For any actual g in G and u<=rho, a fit of R(c)gK exists iff c=0,b=0,
lambda=1. For0<u<=rho, at EVERY physical b and lambda>=1 the maximum
physical supporting-line excess over the selected supports and all originals
is strictly larger than the table's positive coefficient times u.

## 2. Actual geometry, complete closed fans and the local certificate

The reproduction driver FIRST rebuilds all actual originals and facets from
pinned public source. [geometry.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_closed_horizon_cell/geometry.py)
and [polynomial.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_closed_horizon_cell/polynomial.py)
are code dependencies with hashes in [configuration.json](configuration.json).
Their prior local-radius result is not assumed. The complete named model
checks92 originals,60 facets,300 coplanar identities,5220 strict remaining
facet-original inequalities,900 strict facet turns,150 edges with two-face
incidence, Euler identity, connected adjacency and all300 directed horizon
clauses. Its whole fresh cache has SHA256
`ce7fb43061b5dc692b1824a0e41bec539026c75ae041faa9264a64b8e8b8283f`.

For each C_k, all63 defining halfspaces hold at every literal corner; every
other corner is strictly left of every successive oriented side. Every side
is exactly the stated defining wall, and area is positive. Hence its entire
convex polygon lies in C_k, while C_k lies in the polygon's inward side
halfspaces, whose intersection is precisely the polygon. Both inclusions
prove the entire closed domain, including every zero/tie.

The closed fan is(0,i,i+1), 1<=i<=m-2, for m=3,4,5 cyclic corners. Every
point of a convex polygon lies in this fan: the ray from corner0 through the
point meets the opposite polygon chain in one of its edges, so the point is
a convex combination of corner0 and that edge's endpoints. Corner0 itself
belongs to every fan. Shared diagonals are retained by both closed triangles.
This geometric argument supplies continuum coverage; finite point tests alone
do not supply it. Independent exact area/closed-point controls complement it.

For a selected directed original edge(A,B), dyadic gamma>0, and original
endpoint P in{A,B}, put

    m=gamma*(B-A) cross r, h=m.A=m.P>0,
    f=P cross m, W=(f_x,f_y,f_z,m_y,m_z).

All92 originals satisfy m.V<=h at EVERY closed receiving corner. Since m,h
are receiver-affine, this holds throughout the whole polygon. Both exact
identities m.r=m.(B-A)=0 are checked. Grazing off-endpoint ties are retained.

| cell | actual endpoint rows | directed edges | full support comparisons | off-endpoint ties | five-wrench duals | positive degree5 controls |
|---|---|---|---|---|---|---|
| 19 | 21 | 16 | 4416 | 36 | 6 | 756 |
| 18 | 21 | 16 | 5888 | 42 | 12 | 1512 |
| 16 | 19 | 14 | 5152 | 36 | 12 | 1512 |
| 33 | 29 | 19 | 8740 | 54 | 18 | 2268 |

On EACH entire closed fan and EACH signed rotation-coordinate target,
five distinct actual wrench columns have a strict determinant orientation
and five strictly positive replaced-column Cramer numerators. Their degrees
are at most5. The21 common degree5 triangular Bernstein coefficients are
recomputed with outward integer intervals at denominator10^24. ALL denominator
and numerator controls are strictly positive. Cramer therefore gives positive
weights w_i with sum_i w_i W_i=+/-e_j in ALL FIVE entries. Neither physical
translation coordinate is omitted. Coefficientwise upper numerator-sum/lower
denominator ratios bound sum w_i strictly by the corresponding M_j, because
the nonnegative Bernstein basis sums to one.

Every physical B in r-perp has B=pi_r(alpha e_y+beta e_z), with
alpha=B_y-B_x*s, beta=B_z-B_x*t; indeed(0,alpha,beta)=B-B_x*r.
Thus m.B=m_y alpha+m_z beta. A fit with lambda>=1 gives, at each endpoint,
necessary unit-copy inequalities for B=b/lambda:

    m.R(c)P-h+m.B <= -(1-1/lambda)h <= 0.

After multiplication by1+c.c, the EXACT Cayley endpoint identity is

    2 f.c+(1+c.c)(m_y alpha+m_z beta)+q_P(c)<=0,
    q_P(c)=2(m.c)(P.c)-2h(c.c).                         (2)

The checked bounds give ||m||<2 and ||P||||m||<2 uniformly on the polygon.
For h=m.P, the symmetric matrix(mP^T+Pm^T)/2-hI has norm at most
||P||||m||: the two nontrivial eigenvalues before subtracting h are
(h+/-||P||||m||)/2, and the orthogonal eigenvalue is0. Hence for c!=0,
|q_P(c)|<4||c||^2. This is the uniform quadratic remainder constant4;
it is not inferred from sampled rotations.

Apply each signed five-wrench dual to(2). Its last two entries cancel
EVERY physical translation, giving |c_j|<2 M_j||c||^2 for c!=0.
Since sum M_j^2<N^2, a nonzero c in the CLOSED collar would imply
1<2N||c||<=2N rho<1, a contradiction. The table also records the stronger
checked squared closure4 sum M_j^2*rho^2<1. Therefore c=0.
Now lambda*pi_rK+b subseteq pi_rK. Every positive planar width forces
lambda<=1, so lambda=1. Comparing supports in all planar directions gives
v.b<=0 for every v, so b=0. Conversely every actual g gives equality.

The same duals give the physical gap without assuming a fit. Let E be the
maximum unit-copy physical line excess over all selected supports and ALL
originals, at arbitrary translation. The same signed-dual local closure rules out
E<=0 when c!=0 in the collar, so E>0. Equation(2) and ||m||<2 now imply
|c_j|<M_j[2u^2+(1+u^2)E]. Taking the norm yields

    E>u*(1/N-2u)/(1+u^2)
      >=u*(1/N-2rho)/(1+rho^2)>u*gap_k.               (3)

The exact four intermediate lower coefficients are respectively27/9490,
53/73060,47/50830,31/14430. They exceed the table's gaps. An original scaled
pose at translation b has, on a support attaining a positive unit-copy
excess at b/lambda, excess lambda*e+(lambda-1)h/||m||>=e. Thus(3) retains
EVERY original enlargement and translation.

The first-order contact cone in all five physical entries is also{0}:
if W_i.U<=0, both signed duals force the first three entries of U to zero.
One strictly positive nonsingular dual then forces all five selected
inequalities to be equalities, and nonsingularity gives U=0.

## 3. All original source rotations and the complete proper source cover

[source_cell.py](source_cell.py), copied unchanged from
[parent9558](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_facet40_quad/PROOF.md),
source `4f89c33fb8e4828f97f4b68481e15a15db51faa4`, graph
`bafkreiexvt7tzreqsjsovespasoghudhedvtumsnoe7pp7evvkyqguu3za`, is freshly run
for EACH new cell/mode. It uses only actual proper G, never a reflection,
centrality gauge or an assumed equality inventory. Classical icosahedral
quaternion Voronoi context is [Purser2017 section2(d)](https://repository.library.noaa.gov/view/noaa/15765/noaa_15765_DS1.pdf);
the actual group, coordinates and source fold here are model-specific checks.

For ANY original unit quaternion q, maximize its absolute scalar over the
right orbit by the actual binary120 lifts of G, and choose its sign to make
that scalar nonnegative. Actual coordinate-unit lifts belong to the orbit,
so the maximum scalar is at least1/2. Consequently EVERY original scalar-zero
source/half-turn has a finite folded Cayley c=q_vec/q_0. Right multiplication
is an ACTUAL body symmetry and changes no source body. No left H_n operation
is used.

The nearest binary lifts give twelve affine bounding halfspaces. Opposite
independent normals force a bounded recession cone. All feasible active
normal-triple intersections are the twenty literal vertices of D. EVERY
full binary absolute comparison is two affine inequalities, checked at all
vertices. Thus these twelve halfspaces give the full closest-body cell.
The fresh exact layer checks20 vertices,12 pentagonal faces,2400 signed
comparisons and180 strict complete face-cycle turns. Each vertex has squared
norm39-24phi. Convexity of squared norm and the four independently checked
strict inequalities

    a_k^2*(39-24phi)<rho_k^2

put the ENTIRE closed core a_k D inside its CURRENT proved local collar.

Each source pentagonal face is fanned into three CLOSED triangles(A,B,C),
giving36 face triangles. The radial frustum between a_k times that triangle
and the face is covered by the THREE closed tetrahedra

    (aA,aB,aC,C), (aA,aB,B,C), (aA,A,B,C).              (4)

Here is coverage independent of volume or sample points. Write
c=xi A+eta B+zeta C, xi,eta,zeta>=0, a<=mu=xi+eta+zeta<=1.
Put L1=xi+eta+a*zeta, L2=xi+a*eta+a*zeta, so L1>=L2. The exhaustive cases
L1<=a, L1>=a>=L2, L2>=a have respectively the following barycentric coordinates
in the three displayed vertex orders:

    xi/a, eta/a, (a-L1)/(a*(1-a)), (mu-a)/(1-a);
    xi/a, (a-L2)/(a*(1-a)), (L1-a)/(1-a), zeta;
    (1-mu)/(1-a), (L2-a)/(1-a), eta, zeta.

They are nonnegative, sum to one and reconstruct c in their cases. Closed
equalities belong to both adjacent tetrahedra. Thus108 exact roots cover
every D source outside the local core, including all seams.

Each literal source split edge is bisected at its EXACT midpoint. BOTH
closed children cover the parent. [expand.py](expand.py) and
[verify_shell.py](verify_shell.py) require all108 canonical roots, both
children at every internal node with the same edge, every terminal address
exactly once, and no orphan, duplicate or terminal ancestor. All tree depths
are<=18. The tree labels originate from discovery, but no floating edge
comparison or sampled exclusion is needed to check the published input.

| cell | exact roots | internal nodes | source leaves | receiving products | strict negative joint controls |
|---|---|---|---|---|---|
| 19 | 108 | 477 | 585 | 585 | 35100 |
| 18 | 108 | 1634 | 1742 | 3484 | 209040 |
| 16 | 108 | 3334 | 3442 | 8180 | 490800 |
| 33 | 108 | 791 | 899 | 2697 | 161820 |

Each row satisfies leaves-nodes=108. The total new joint-control count is
896760; these are new four-region controls, not a recheck count for Omega6.

## 4. Physical stress on every complete receiver/source product

For three actual directed receiver support edges d_i=P_bi-P_ai set

    m_i=d_i cross r, h_i=m_i.P_ai,
    w_i=epsilon*(d_j cross d_k).r, epsilon in{+1,-1}.

For EVERY selected stress the three affine w_i are strictly positive at ALL
closed corners of its entire polygon. Hence they remain positive everywhere
in it. The exact cofactor identity gives sum_i w_i*m_i=0 in ALL three spatial
entries. With r_x=1 the weights equal the minors of the two physical planar
normal entries(m_y,m_z): cross(m_j,m_k)=r*((d_j cross d_k).r).

For original moving vertices X_i, with NO premise that they remain support
maximizers on a product, define

    F(r,c)=sum_i w_i[(1+c.c)h_i-m_i.R_hom(1,c)X_i],
    R_hom(1,c)X=(1-c.c)X+2(c.X)c+2(c cross X).           (5)

A fit implies lambda*sum_i w_i*m_i.R(c)X_i<=sum_i w_i*h_i, because the FULL
original translation cancels. The right side is positive. Thus F<0 implies
the left unscaled support sum is larger than that positive right side,
contradicting lambda>=1. Original enlargement/translation are retained
directly; the source need not be centrally symmetric or artificially centered.

F has receiving/source bidegree(2,2). For closed receiver triangle vertices
r_a and closed source tetrahedron vertices c_u, its controls are

    g_i(r;u,v)=h_i(r)(1+c_u.c_v)-m_i(r).[
        (1-c_u.c_v)X_i+(X_i.c_u)c_v+(X_i.c_v)c_u
        +(c_u+c_v) cross X_i],
    B_abuv=(1/2)*sum_i[w_i(r_a)g_i(r_b;u,v)
                       +w_i(r_b)g_i(r_a;u,v)].         (6)

The six receiver pairs a<=b and ten source pairs u<=v give60 controls.
The nonnegative quadratic bases alpha_a^2,2alpha_a alpha_b and
beta_u^2,2beta_u beta_v each sum to one on their ENTIRE CLOSED simplices.
Therefore strict negativity of ALL60 outward upper controls proves F<0
throughout the complete product.

Every source leaf covers EVERY receiver fan. For19,18,33 all fans are used
whole. For16,3010 source leaves use both whole fans. The other432 source
leaves use ALL FOUR exact midpoint children of fan0 and the WHOLE fan1:
(00,01,02,03,1). For a receiver triangle(A,B,C) with midpoint vertices
AB,BC,CA, the children are(A,AB,CA),(AB,B,BC),(CA,BC,C),(AB,BC,CA).
They cover the closed parent: in parent barycentric coordinates a point
with some coordinate>=1/2 lies in that corresponding corner child; if all
coordinates<=1/2 it lies in the central child, whose weights are
1-2alpha_C,1-2alpha_A,1-2alpha_B in(AB,BC,CA) order. These are nonnegative,
sum to one and reconstruct the point. Every equality seam remains included.
The checker requires whole OR all four ordered children on each fan,
rejecting holes, duplicates, unrecognized paths and parent-child overlap.
No source branch or receiving region was dropped to repair16.

Every one of896760 controls passes. Exact outward margins are in
[expected.json](expected.json). Every outer D source is thereby excluded;
every source in the closed inner core enters Section2's proved collar.
Undoing the actual proper-body fold gives Q in G. Positive widths/supports
then give lambda=1,b=0, and conversely actual G equality copies fit. This
proves(1) on the four new polygons. Cited9604 supplies ONLY Omega6, completing
the literal ten-cell union. For r'=epsilon*g*r, apply g^-1 to the entire
physical configuration, using pi_{-r}=pi_r and gK=K, to transport the result
to all signed/projective receiving G images.

## 5. Compact literal source, fresh replay and trust boundary

The four public forest files are ordinary labelled mathematical certificates,
not compressed proof corpora. An internal node[edge,left,right] names one
of the six tetrahedral edges01,02,03,12,13,23 and BOTH closed children.
A negative integer-1-i names terminal leaf i. A seven-integer stress row
is[orientation,edgeID0,edgeID1,edgeID2,movingOriginal0,movingOriginal1,movingOriginal2].
A leaf row names its receiving-path pattern and one stress row per piece.
Supports are original directed endpoint pairs in the literal edge dictionary.
All definitions are transparent in expand.py; no coefficients are supplied
as premises. Expansion preserves EVERY original discovered source address,
actual support/moving original/orientation and receiving piece. The exact
checker reconstructs the model and recomputes EVERY coefficient sign.

From this directory, with CPython3.11+ and the pinned public relative source:

    python3 reproduce.py
    python3 reproduce.py --optimized --compare .generated/normal/complete.json

All numerical children are sequential, threads1, unchanged1CPU2GiB scope.
Model guards45s, local/preparation/author-control guards40s, and exact source
batch guards45s. Batches are consecutive disjoint source leaf ranges of at
most1000 and all are mandatory; aggregate.py reparses EVERY index, source
address, receiver path, actual support/moving original and all60 interval
entries. A failed, timed-out, incomplete or undecided run yields no theorem.
Generated models, expanded forests and full coefficient streams stay in
ignored .generated; no private workspace input or proposal solver is needed.

[VALIDATION.json](VALIDATION.json) records FRESH complete normal and optimized
runs from an isolated relocated source tree containing only this packet and
its declared small public dependencies, starting with EMPTY generated state.
Both modes separately rebuild the named geometry. All complete actual
model, local, support/source geometry, author control and source leaf records
agree BYTE FOR BYTE, including EVERY positive Cramer and negative joint
coefficient interval entry. The compact expected hashes supplement full
recomputed signs and this comparison; hashes alone are not a proof.

Author local controls use independent Gaussian Fraction column-polarization
of all126 denominator/Cramer controls,30 direct degree5 reconstructions,
actual cubic-field five-wrench centroid solves, physical Cayley/translation/
scale identities, exact closed-fan locations and midpoint quarter-area
identities. Source controls use720 Fraction double-midpoint coefficients,
36 direct tensor reconstructions,2880 refined-child Fraction coefficients,
144 refined tensor identities, six actual physical translation/enlargement
cases per cell, and actual named midpoint decoders. Semantic damages cover
missing roots/leaves/fans/children, bad originals/supports/orientations,
inconsistent source edges, duplication/ancestors, invalid collars/masses,
wrong model fingerprints and attempted exclusion of the true zero pose.
They are author controls, not independent review. CPython/Fraction, explicit
integer outward rounding, pinned small checker/model sources, literal
mathematical inputs and the ordinary finite-to-continuum arguments written
here are the trust boundary; no proof-assistant formalization is claimed.

## 6. Primary literature, attribution and open complement

[Zeng2604.26531 sections1.1–1.2](https://arxiv.org/html/2604.26531) defines
proper SO(3), physical translation and STRICT projected-interior passage.
[Gosain–Grimmer2509.08190 Table3](https://arxiv.org/html/2509.08190#S3.T3)
keeps the deltoidal and pentagonal hexecontahedra unresolved. A floating
best fit .999999999999 is not a non-Rupert theorem. The distinct
[Steininger–Yurkevich2508.18475](https://arxiv.org/abs/2508.18475)
Noperthedron theorem does not resolve this named chiral solid. These primary
statuses were refreshed live2026-10-02 with bounded named-target search;
no exhaustive priority claim is made.

The earlier actual-body/closed-horizon/closed-cell lemmas8547/8735/9192/9283
and proper-source/receiving lemmas9558/9604 are credited proof/code premises
or method context as stated above. Complementary
[J74 local9677](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/whole_phase56_collar/PROOF.md),
[whole-source J74 lemma9768](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/joint_phase56/PROOF.md)
and [RID lemma9737](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_inner_phase_triangle/PROOF.md)
are physical translation, closed boundary and joint-domain method context
only. Their body symmetries/equal-shadow inventories/constants/centrality,
RID's moving H_n branch and any former reviewer conclusions do not transfer
to this chiral K or establish independent acceptance of this lemma.

The remaining receiving complement, including neighboring whole pentagon32,
and the GLOBAL Rupert classification remain OPEN. No spherical-area fraction,
whole-atlas certificate or global non-Rupert proof is asserted.
