# J74: uniform local rigidity on an entire closed receiving phase cell

**six-rupert-2, actual role researcher; 2026-10-02.**

This ordinary intermediate lemma is author checked, unformalized and
independently unreviewed. It constructs six exact contact duals valid on an
entire receiving triangle, including its closed grazing boundaries. It does
not classify sources outside the stated collars. The global Rupert property
of the original unit-edge metabigyrate rhombicosidodecahedron, J74, remains open.

## 1. Statement and original configuration

Let K be the convex hull of the sixty original vertices V_0,...,V_59 in the
[published J74 model](../model.py), graph LEMMA8551, source
25fc9695745b6832d068d18544452b7852b5847f. Its exact original two-cupola
construction, common squared vertex radius

    R^2=(11+4sqrt(5))/4,

and three independent antipodal vertex pairs are freshly checked. In
particular 0 lies in the interior of K. No perturbation or body centrality
is used. Put s=sqrt(5) and let Delta be the CLOSED triangle with cyclic
vertices

    d0=((s-1)/2, 3-s),
    d1=((5-s)/6, (5s-7)/6),
    d2=((s-1)/2, (9s-19)/2).

For (x,y) in Delta use r=(x,1,-y), n=+/-r/||r||,
P_n=I-nn^t and M_n=I-2nn^t. Equivalently r=Sy(x,y,1) in the proper frame
Sy=((1,0,0),(0,0,1),(0,-1,0)). Throughout Delta, |x|<1 and 0<y<1;
thus r is nonzero, its third coordinate never vanishes, and this is a
whole cell inside the selected closed maximal-coordinate face.

Define the original proper matrices

    a=(s-1)/4, b=(s+1)/4, c=1/2,
    H=diag(-1,-1,1), Mx=diag(-1,1,1),
    A=((b,a,c),(-a,-c,b),(c,-b,-a)),
    B=((-a,-c,-b),(c,-b,a),(-b,-a,c)),
    F={I,H,A,AH,B,BH},
    E(n)=F union {M_n g Mx : g in F}.

H and Mx are actual sixty-vertex body symmetries; A and B are partial
shadow poses and are not assumed to be body symmetries. Every matrix in
E(n) is proper. The twelve listed motions are distinct throughout Delta
and have exactly the original receiving shadow:

    P_n(eK)=P_n(K), e in E(n).

**Local lemma.** For every (x,y) in Delta, e in E(n), Q in SO(3),
lambda>=1 and every original physical T in n-perp, if

    lambda P_n(QK)+T subseteq P_n(K)
    and trace(Qe^t)>=661/221,

then

    Q=e, lambda=1, T=0.

The trace condition is exactly a CLOSED relative physical Cayley norm
at most 1/21, equivalently ||Q-e||_F^2<=4/221. Consequently the standard
strict Rupert condition is impossible for such receivers and sources
inside any of these twelve local collars. No assertion is made for
sources outside them, or for receivers outside Delta.

The original fit model is justified by the standard strict projection
formulation in [Zeng Section1.1](https://arxiv.org/html/2604.26531#S1.SS1):
two proper receiving/source orientations and a planar rotation can be
lifted into Q and the original T used above. Closed containment is an
auxiliary stronger exclusion problem; equality of shadows itself is not
a Rupert passage.

## 2. Current frontier, credited dependencies and prior scope

[Gosain--Grimmer Table4](https://arxiv.org/html/2509.08190#S3.T4) retains
J72,J73,J74,J75,J77 as unresolved. [Zeng Section1.2](https://arxiv.org/html/2604.26531#S1.SS2)
reports 87 of 92 Johnson solids Rupert and keeps the negative claim for
the rhombicosidodecahedron conjectural. [Steininger--Yurkevich](https://arxiv.org/abs/2508.18475)
proves non-Rupertness of the distinct Noperthedron. A fresh check of the
September2026 [Octahedron paper](https://arxiv.org/html/2609.10788v1)
supplies no J74 resolution; its final constant-samurai question for the
rhombicosidodecahedron is open. These are bounded primary-literature
checks on 2026-10-02, not exhaustive novelty certification.

The original [phase-crossing box result9531](../phase_crossing_box/PROOF.md),
source 2ba89329055167fe838b568349801a2d7ccd39be, supplies the earlier pose
notation and the old stencil discussed below. Its all-source exclusion,
old source forest, receiving box constants and equality completeness are
not premises of this lemma. Only the small original model and inherited
[ordered-field helper7140](../../../convex_geometry/rupert_j77_projection_diameter/q5.py)
are imported after exact fingerprints are checked. The complete geometric,
Cramer, support and nonlinear proof is regenerated here.

The [degree-preserving source rectangle9637](../gated_rectangle/PROOF.md),
source 2123173af372c854af455c6f5f7a81b4fa9f7b34, is available for a future
all-source layer. Its classification on the much smaller old box does
not imply the present local lemma or a whole-triangle classification.
Classical contact stresses, Cramer cofactors, Bernstein positivity and
Cayley rotation formulas are reused; no general-method priority is claimed.
The related [Catalan whole-cell9604](../../six-rupert-1/pentagonal_facet10_quad/PROOF.md)
and [RID canonical-source9517](../../six-rupert-3/rid_closed_grazing_quad/PROOF.md)
are scoped context. Their geometry, centrality, body groups, constants
and review status do not transfer to the original Johnson solid.

## 3. Entire original closed phase cell and the known shadows

The original phase56 cycle is

    16,0,36,28,10,11,47,55,27,7,43,31,13,12,48,56,20.

For each consecutive original i,j and every k in0..59 impose the literal
receiving support inequality

    [(V_i-V_k) cross (V_j-V_i)] dot (x,1,-y)>=0.            (1)

Intersect ALL of (1) with the selected closed square[-1,1]^2. Exact
normalization gives380 distinct nonzero halfspaces. Closed clipping gives
exactly Delta. All resulting sides are actual defining support/frame lines,
and all3060 original corner support comparisons pass. This establishes
both inclusions of the entire halfspace cell and the stated triangle;
there is no receiver sampling or omitted boundary. Its exact centroid
has986 strictly positive offendpoint support gaps, so the interior is
indeed the actual seventeen-corner receiving phase.

Write E_ij=V_j-V_i, m_ij(r)=E_ij cross r and
h_ij(r)=m_ij(r) dot V_i. Every h_ij is strictly positive on Delta:
its affine corner values are positive, with minimum5/4-s/12. Every listed
projected edge is therefore nonzero, including at the closed corners.
In the phase interior the strict support gaps make the listed cyclic
edges the full boundary of the projected original hull. Continuity gives
the same hull description by their weak supporting halfplanes on the
closed cell; redundant collinear supports at grazing boundaries are kept.

For every g in F and every listed receiver vertex V_i, the checker finds
an exact spatial preimage gV_k=V_i, independent of r. For every g and every
original source vertex, its receiving support inequalities are checked
at all three closed corners:18360 original comparisons. Affinity extends
these inequalities to the entire Delta. Together with the corner
preimages, they prove P_n(gK)=P_n(K) everywhere on this closed triangle.
This is an existence list of equal shadows, not a classification of all
possible equal shadows.

Since Mx permutes K and P_n M_n=P_n, the proper involution

    C_n(Q)=M_n Q Mx

preserves the entire original source projection, its physical translation
and its scale. Thus each reflection companion also gives the same shadow.
The checker includes24 full sixty-point projection/action fixtures; the
universal operator identities above provide the ordinary all-n proof.

To prove that the twelve motions remain distinct, base/base pairs are
already distinct and C_n is injective. A base/companion collision g=C_n(h)
would require the fixed matrix

    M_n=g Mx h^t.                                        (2)

All36 choices(g,h) are checked exactly. Twelve right sides are not plane
reflections. Two have their possible reflection axis outside the raw
r_y=1 chart. For the remaining22 the exact normalized axis violates an
actual defining cell/frame halfspace. Equation(2) is therefore impossible
anywhere on Delta, including its sides and corners. These are full axis
checks, not finitely sampled separation tests.

## 4. Six fixed persistent physical dual constructions

For an endpoint P=V_k with k in{i,j}, define the literal five-column wrench

    f_ijk(r)=(P cross m_ij(r), m_ij,x(r), m_ij,y(r)).

Each column is affine in r. The original source preimages from Section3
make every chosen P a genuine physical source contact for EVERY g in F.
This is not a right quotient by a partial shadow pose.

The six five-column bases are the following ordered triples(i,j,k):

| target | literal original contacts | strict normalized mass bound |
| --- | --- | --- |
| -e_x | (11,47,47),(16,0,0),(12,48,48),(11,47,11),(7,43,7) | 8 |
| +e_x | (10,11,11),(43,31,43),(56,20,56),(47,55,55),(10,11,10) | 10 |
| -e_y | (56,20,56),(11,47,47),(7,43,43),(13,12,12),(10,11,11) | 7 |
| +e_y | (48,56,56),(55,27,55),(27,7,7),(0,36,0),(48,56,48) | 11 |
| -e_z | (16,0,16),(12,48,12),(11,47,11),(43,31,43),(13,12,13) | 5 |
| +e_z | (56,20,56),(0,36,0),(56,20,20),(7,43,7),(47,55,55) | 12 |

For one row of this table, let B(r) have these five physical columns and
let t=(signed coordinate unit vector,0,0). We construct

    nu(r)=B(r)^(-1)t.

Here is a finite exact certificate of continuum validity. Use closed
barycentric coordinates u=(u0,u1,u2), u_i>=0, sum u_i=1 on Delta. Then
B(r(u))=sum u_i B(r(d_i)). Its determinant D is homogeneous of degree5.
The five Cramer numerators N_k are homogeneous of degree4. Orient all
of them by the same determinant sign. The checker proves the entire
literal polynomial identities

    B N=D t,
    sum N_k m_ijk,z=0,                                  (3)

so all three torque and all THREE original spatial force equations hold.
The second identity in(3) is also independently regenerated. Geometrically
it follows from the first two zero force coordinates, m dot r=0 and
r_z!=0. No translation coordinate has been silently omitted.

For a homogeneous scalar polynomial of degree d,

    p(u)=sum_{|alpha|=d} c_alpha u^alpha,

its triangular Bernstein control is
c_alpha / binomial(d;alpha0,alpha1,alpha2). The Bernstein basis is
nonnegative and sums to1 on the entire CLOSED triangle. The checker
requires all21 degree5 determinant controls strictly positive and all
75 degree4 Cramer controls nonnegative. Hence B never becomes singular
and every raw nu_k=N_k/D is nonnegative throughout Delta.

Let h_k(r) be the positive original support height of the kth contact.
Normalized contact weights are w_k=nu_k h_k, and their mass is

    sum w_k=(sum N_k h_k)/D.

Each numerator above has degree5. For each table bound M all21 controls
of M D-sum N_k h_k are strictly positive. Thus sum w_k<M throughout
Delta. Every basis therefore needs exactly21+75+21=117 controls, and
ALL702 controls for the six bases are checked exactly. Direct Gaussian
determinants and independent exact inverse products are compared with
the Cramer expansion at six fixtures per basis. The full polynomial
identities, rather than the fixtures, establish the continuum equations.

There are15 zero numerator controls for the -e_z basis, all on its
u1=0 side, the original vertical side d0--d2. Its raw weights0,1,3 vanish
on that closed side; the other two contacts still provide the target.
Nonnegative stresses suffice in the proof. These genuine closed grazing
ties are retained; no strict interior restriction is substituted.

The old five-contact -e_y stencil9531 fails at d0: with ordered contacts
(0,36,36),(10,11,11),(7,43,43),(13,12,12),(20,16,16), its first exact raw
weight is(-9-5s)/11<0. The countercontrol is freshly reconstructed from
these true original physical columns. That is failure of an old stencil,
not a nonexistence theorem or proof of a nonzero feasible tangent cone.
The new bases above repair the exact continuum proof mechanism.

The discovery LP used nonnegative endpoint weights satisfying
sum nu_k f_k=t, with a positive support-height mass objective at a point.
A small deterministic floating revised simplex and NumPy1.24.2 supplied
basis proposals; its tolerances were not proof evidence. The public
[checker](check.py) regenerates the canonical parameterized matrices
from the sixty original vertices and the compact [literal bases](certificate.json),
then verifies the exact continuum construction. No floating feasibility,
optimality, infeasibility, candidate absence or private solver output is
needed for the lemma. This is shared-geometry author verification, not
independent reproduction.

## 5. Uniform nonlinear local rigidity, original lambda and translation

Set N_ij(r)=m_ij(r)/h_ij(r). On Delta this normalized vector is a convex
combination of its corner values, with barycentric weights proportional
to the positive h_ij corner values. Its norm is therefore at most its
maximum corner norm. All51 original support/corner comparisons give

    max R^2 ||N_ij||^2 = 5/3-2s/9 <121/100.

Consequently R||N_ij||<11/10 uniformly. For a contact point P, ||P||=R
and N_ij dot P=1. The quadratic form

    (N_ij dot d)(P dot d)-||d||^2

has absolute value at most C||d||^2 with C=21/20. Indeed the symmetric
matrix (N_ij P^t+P N_ij^t)/2 has eigenvalues
(1+R||N_ij||)/2,(1-R||N_ij||)/2,0. After subtracting I the largest
absolute eigenvalue is (1+R||N_ij||)/2<C, since R||N_ij||>=1.
This is a fresh whole-triangle bound, not the old-box C=5/4 transported.

First let e=g in F and write Q=R(d)g in physical LEFT relative Cayley
coordinates. For finite d the ordinary rotation formula gives

    N dot(R(d)P-P)
       =2[(P cross N) dot d+(N dot d)(P dot d)-||d||^2]
          /(1+||d||^2).                                 (4)

The original fit supplies for every chosen actual source contact

    lambda N_k dot R(d)P_k+N_k dot T <=1.

Multiply by the nonnegative w_k and sum. Equations(3), after support-height
normalization, cancel all three original spatial translation components
and give the specified signed unit torque. With m=sum w_k>0 and
lambda>=1, the fit implies

    sum w_k N_k dot(R(d)P_k-P_k)<=m/lambda-m<=0.

Using(4), the quadratic bound and both signed duals yields

    |d_x|<=C*10*||d||^2,
    |d_y|<=C*11*||d||^2,
    |d_z|<=C*12*||d||^2.

If d!=0, summing squares and dividing requires

    1<=C^2(10^2+11^2+12^2)||d||^2.

But the CLOSED norm bound ||d||<=1/21 gives

    C^2(10^2+11^2+12^2)/21^2=365/400=73/80<1,

a contradiction. Thus d=0 and Q=g. Since P_n(gK)=P_n(K), the original
fit becomes lambda S+T subseteq S for the full dimensional bounded
convex polygon S=P_n(K). Positive directional widths imply lambda<=1,
so lambda=1. If T were nonzero, applying the support functional in the
T direction to S+T subseteq S would give ||T||^2<=0. Hence T=0.
No source centering or restriction on the original physical translation
was used before this conclusion.

For e=C_n(g), apply the actual involution C_n to Q. It preserves the
entire original source projection, the original T and lambda. Moreover

    C_n(Q)g^t=M_n[Q e^t]M_n,

so its relative trace, rotation angle and Cayley norm equal those of
Qe^t. The base-pose argument therefore proves C_n(Q)=g and Q=e, again
lambda=1,T=0. This uses Mx as a full-body reflection and works for the
original noncentrally symmetric Johnson solid.

Finally a proper relative Cayley rotation satisfies

    trace(R(d))=(3-||d||^2)/(1+||d||^2),
    ||R(d)-I||_F^2=8||d||^2/(1+||d||^2).

The trace gate661/221 is larger than-1, so it includes no relative
halfturn and is exactly equivalent to ||d||^2<=1/441. Its closed
Frobenius-square gate is4/221. This proves the stated local lemma and
the strict-passage exclusion INSIDE these collars.

## 6. Reproduction, completeness and trust boundary

Run the complete standard-library [checker](check.py) normally and with
python3 -O as described in [README](README.md). Both full records must
match [expected.json](expected.json). Each invocation regenerates the
entire geometry, every one of702 required controls, all36 literal spatial
polynomial equations, all true preimages, the whole axis/collision audit,
all nonlinear constants and eight semantic damages. There are no source
chunks, omitted coefficient lists, random seeds or incomplete enumeration
in this proof layer. The optional --emit removes only comparison with
the fixed expected record; every mathematical gate remains active.

The compact [certificate](certificate.json) has only exact vertex labels,
small field coefficients, six bases and the constants. A coefficient
stream hash identifies regenerated controls; it does not replace any sign
check. The before-import [pins](DEPENDENCIES.json) name the original model
and credited field implementation. Exact ordered-field signs are decided
by rational arithmetic, never by decimal sqrt(5). Measured default and
relocated replays are in [VALIDATION](VALIDATION.json). Numerical threads1,
one intensive job at a time,45s per-child guards and the unchanged1CPU2GiB
process scope were respected. No timeout, UNKNOWN, partial run or floating
search failure is mathematical nonexistence.

The trust boundary is the full ordinary real convex/geometric/Cayley
argument above and exact Python execution in Q(sqrt5), using the published
original body identification. It is unformalized and independently
unreviewed. Source publication is provenance, not acceptance or proof by
itself. No all-source equality classification, global non-Rupert theorem,
optimal radius, universal computational speedup or priority for classical
methods is asserted.

A useful next layer is a fresh joint receiving/source cover outside the
moving collars. The source-independent rectangle9637 permits receiving
quadratic forms; its whole old box forest cannot be transferred. A single
coarse receiver triangle and fixed source forest need not place cells near
moving companions inside a uniform collar for every receiver. Receiver
subdivision or an appropriate dependent source construction is the planned
next step toward a concrete full-source certificate. That remaining work is
not part of this completed local lemma.
