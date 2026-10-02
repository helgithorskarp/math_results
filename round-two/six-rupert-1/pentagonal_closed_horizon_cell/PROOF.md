# Six coordinate duals on a complete closed pentagonal hexecontahedron horizon cell

**Actual author: six-rupert-1. Role: researcher. 2026-10-02.**
Ordinary geometric intermediate proof with exact finite certificates.
Author checked, unformalized, independently unreviewed. The standard
pentagonal hexecontahedron's global Rupert property remains **OPEN**.

## Solid, receiving cell and precise conclusions

Let K be the SAME-HANDED standard pentagonal hexecontahedron in the
normalized coordinates of the published
[exact named model](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_minimum_diameter/model.json),
source **86ab225fb8becbe66601a5da0b5b017e872e1833**. Its 92 originals,
60 actual pentagonal facets and 150 edges are reconstructed here, rather
than replaced by a centrally symmetric surrogate. Put phi=(1+sqrt(5))/2.
The coordinates lie in Q(phi)[x], where x is the unique positive root of
x^3-2x-phi=0, with 17/10<x<18/10. The inherited normalization divides by
the largest literal coordinate. Scaling the whole configuration changes
neither containment nor the Rupert property.

Index the actual outward facet normals N_0,...,N_59 in the literal
model's face order, each normalized to N_j.P<=1. Let sigma be the
following sixty signs, supplied without ambiguity also as an integer
array in [certificate.json](certificate.json):

    ----------++++++++++----------++++++++++++------++---+++++--

The receiving domain is the ENTIRE CLOSED facet-phase cell

    Delta = {(s,t): s>=0, t>=0, phi*s+phi^2*t<=1,
                       sigma_j*N_j.(1,s,t)>=0 for all sixty j}.

All its boundaries and grazing facets are included. The checker proves
that this halfspace intersection is precisely the convex pentagon whose
five EXACT algebraic vertices are in certificate.json. Approximate
coordinates, used only to help locate it, are

| Vertex | s | t |
|---|---:|---:|
| 0 | 0.154376252 | 0 |
| 1 | 0.157414272 | 0.002173891 |
| 2 | 0.129508642 | 0.158300431 |
| 3 | 0.078170766 | 0.166401693 |
| 4 | 0 | 0.110465702 |

These are raw chart ratios. No spherical area or receiving-sphere coverage
fraction is asserted. The certificate and exact field, not this table,
define the theorem's domain.

Write pi_r for orthogonal projection onto r-perp, r=(1,s,t), and let G
be the actual sixty-element PROPER body group. For ordinary Cayley vector
c, define the proper rotation

    R(c)P = [(1-d)P+2c(c.P)+2c cross P]/(1+d), d=c.c.

**Closed-fit theorem.** For every real (s,t) in Delta, every g in G,
every c with ||c||_infinity<=1/163, every lambda>=1 and every ACTUAL
receiving-plane translation b,

    lambda*pi_r(R(c)gK)+b subseteq pi_r(K)
        iff c=0, lambda=1, b=0.                       (1)

The source chart restriction is a HYPOTHESIS. No all-source localization
has been proved for this receiving cell. Other proper source poses remain
unclassified. Consequently (1) excludes strict standard passages only
within this tube and does not prove global non-Rupertness.

**Infinitesimal theorem.** For the actual selected support endpoints,
the five-coordinate first-order feasible cone is {0} throughout the
whole closed cell, with both physical translation coordinates retained.

**Quantitative physical theorem.** For 0<u=||c||_infinity<=1/163,
lambda>=1 and arbitrary actual b, let E_r(lambda,c,b) be the maximum
signed physical support-line excess of the moved original vertices,
over the fifteen actual supporting directions used in the certificate:

    max_edges max_P [m_edge(r).(lambda*R(c)P+b)-h_edge(r)]/||m_edge(r)||.

Then

    E_r(lambda,c,b) > u/4500.                         (2)

This is a distance in the model's physical coordinates. It is neither
an unnormalized polynomial residual nor an automatic error bound for
approximate poses outside the source chart. The source group g disappears
from the maximum because g permutes all actual originals.

Proper receiving images and negative normals follow by transporting the
whole configuration. Precisely, for r'=epsilon*A*r, A in G, reduce a
source Q by A^-1*Q=R(c)g and express c in THAT folded coordinate system.
Both (1) and (2) then hold unchanged after the common isometry. Negating
r leaves its physical projection unchanged. No independent reflection of
the source, or opposite-handed passage, is introduced. Reflecting the
whole solid and configuration gives the analogous theorem for its other
handed version; every moving placement is still proper.

## Exact whole-cell and actual-support verification

geometry.py byte-pins the three inherited named-model source files.
It rebuilds the unique named root, its positive parameters, the complete
proper group orbit and the literal 92-original palette. It checks all
60 normalized facets: 300 coplanar identities, 5,220 strict other-original
inequalities, 900 global pentagon turn tests, the complete two-facet
incidence of 150 edges, Euler identity and connected facet adjacency.
Its extra 300 directed horizon identities reproduce the same complete
named geometry; none is a global containment decision.

For each of the five proposed receiving vertices, every one of the
63 defining halfspaces is checked exactly. For every polygon side, ALL
other vertices lie strictly to its left. This global convexity test
does not accept a self-intersecting star merely because consecutive
turns have one sign. Each side is an actual defining halfspace wall:
the indices among the three chamber and sixty facet inequalities are
55,43,13,50,45 in cyclic order. Therefore the polygon lies in Delta,
and Delta lies in the intersection of its five inward side halfspaces,
which is the polygon. This proves the ENTIRE closed cell, not just a
subpolygon or the finite proposed vertices.

Each contact (a,b,v,k) uses actual originals P_a,P_b and endpoint
v in {a,b}, with FIXED dyadic raw normal

    m(r)=2^k*(P_b-P_a) cross r, h(r)=m(r).P_v.

At every closed receiving vertex m.r=0 and the two endpoint values
agree exactly. The height is strictly positive. ALL 92 originals satisfy
m.P<=h, weakly. These quantities are affine in (s,t), so support and
positive height hold at every real point of the entire closed pentagon.
Ties at grazing facets are preserved; strict offendpoint gaps are not
assumed. The 6,900 comparisons contain 204 exact ties, including 54
offendpoint grazing ties.

The checker uses 21 distinct endpoint rows on fifteen directed support
edges. The squared norms are convex in (s,t), so their upper bounds at
the five vertices control the whole cell. Exact rational enclosures
prove

    ||m(r)||<2,
    2*max_original||P||*max_selected_support||m(r)||<4. (3)

Every support is an actual nonzero support of the named solid's shadow.
At a boundary it can expose a larger original face, which is harmless.
A complete inventory of ALL shadow edges is unnecessary: containment
must satisfy every one of these actual support inequalities.

## Six positive Cramer families, including exact translation cancellation

Since r_x=1, every actual b in r-perp can be written uniquely as

    b=pi_r(alpha*e_y+beta*e_z).

Indeed a vector alpha*e_y+beta*e_z parallel to r must have alpha=beta=0;
the injective map between two-dimensional spaces is onto. For an actual
endpoint P_v, the raw wrench is

    f_v(r)=(P_v cross m(r), m_y(r), m_z(r)) in R^5.    (4)

It is exactly affine in (s,t). The last two entries encode ACTUAL
translation, which cannot be removed by centering this chiral body.

For each j=0,1,2 and sign epsilon=+/-1, take the five contact columns
listed in certificate.json and form a five-by-five matrix A(r). If
D=det A and D_i replaces column i by epsilon*e_j in R^5, Cramer's rule
gives the actual real functions w_i(r)=D_i(r)/D(r) and the exact identity

    sum_i w_i(r)*f_i(r)=epsilon*e_j.                  (5)

The target's last two entries are zero. Thus (5) cancels both actual
translation coordinates identically, for every real receiving parameter.

The closed convex pentagon is triangulated by (0,1,2),(0,2,3),(0,3,4).
On each triangle write (s,t) as its affine image of z,w>=0,z+w<=1.
Every D and D_i is a polynomial of total degree at most five. An exact
common orientation sign makes the denominator and all five numerators
strictly positive throughout every triangle, by the following bounds.

For p(z,w)=sum a_ij*z^i*w^j, its degree-n triangular Bernstein coefficients
are

    B_kl = sum_{i<=k,j<=l} a_ij*binom(k,i)*binom(l,j)
                        /[binom(n,i+j)*binom(i+j,i)], k+l<=n.

The corresponding basis functions are
n!/(k!l!(n-k-l)!)*z^k*w^l*(1-z-w)^(n-k-l). They are nonnegative and sum
to one on the ENTIRE closed triangle. Therefore positive lower bounds
for all coefficients prove strict polynomial positivity everywhere,
including vertices and shared seams. Vertex signs alone would not suffice.

polynomial.py propagates rational enclosures using integer scale10^24.
Each multiplication divides endpoint products by that scale with floor
for the lower endpoint and ceiling for the upper endpoint. Rational
coefficient multiplication is likewise rounded outward. Named-coordinate
intervals enclose the actual fixed root. Consequently every coefficient
bound encloses the true polynomial coefficient, despite cancellations.
No floating sign, approximate determinant or solver result is trusted.

For the mass sum_i w_i, denominator and sum-numerator use the SAME
degree-five Bernstein basis. Comparing each sum-numerator upper bound
with the corresponding positive denominator lower bound bounds the
whole rational function. The six certified uniform sums are less than
approximately 9.973,10.298,14.829,26.279,24.340,22.089 respectively;
the EXACT record proves each is **strictly less than27**. These decimal
values are descriptive only.

Thus at every receiving point six positive five-contact duals satisfy
(5), each with mass<27 and nonzero determinant. Positivity and Cramer's
algebraic identity prove the continuum; the displayed coefficient bounds
and whole-record hashes provide compact reproducible finite evidence.

For the infinitesimal assertion, suppose f_i.U<=0 for all selected rows.
Applying both signs of (5) forces the first three entries of U to vanish.
One positive dual now has weighted sum of its five inequalities zero,
so all those five inequalities are equalities. Its invertible A forces
U=0. This proves the full five-coordinate first-order cone is {0}.

## Actual nonlinear containment, scale and recovery

First consider unit scale. Put d=c.c and write the arbitrary physical
translation in the coordinates above. Define

    U=(2c_x,2c_y,2c_z,(1+d)*alpha,(1+d)*beta).

At an actual support endpoint m.P=h, clearing the positive Cayley
denominator gives the exact support inequality

    f.U <= 2*d*h-2*(m.c)*(P.c)
         =2*m.(d*I-c*c^t)P.                          (6)

The symmetric operator d*I-c*c^t has eigenvalues d,d,0, so its norm is d.
Equation(3) makes the right side STRICTLY less than4*d for nonzero c,
and it is zero for c=0. With u=||c||_infinity>0, choose its largest signed
coordinate and apply that positive dual in(5):

    2*u < 27*4*d <=324*u^2.

Thus 1<162*u, contrary to u<=1/163. Nonzero motion is impossible in the
entire stated closed chart. At c=0 all row inequalities have nonpositive
left sides. The positive, nonsingular dual argument used above forces
U=0, hence alpha=beta=0 and the ACTUAL translation vanishes.

For the ORIGINAL lambda>=1 translated fit, divide the entire receiving-
plane containment by lambda. Because 0 is interior to pi_r K and K is
convex, (pi_r K)/lambda is contained in pi_r K. Therefore the same R(c)
has a unit fit with actual translation b/lambda. This is contraction
about the receiving origin, not a central-symmetry centering assertion.
The unit theorem gives c=0 and b/lambda=0. Then any positive support
height in the original fit forces lambda*h<=h, hence lambda=1.
The converse is the identical fit. Body g acts only by permuting K.
This proves(1), with ALL original translation and scale quantifiers.

## Physical support error, without assuming containment

For a unit pose with arbitrary actual translation, let E be the maximum
physical excess over the selected actual supports and ALL source originals.
If c is nonzero in the chart, E<=0 would give all inequalities(6), already
shown impossible. Hence E>0. Every selected endpoint then satisfies

    f.U <4*d+2*(1+d)*E,

because its raw support excess is at most ||m||*E and ||m||<2. Applying
the dual for the largest signed c coordinate gives

    E > (2*u-108*d)/[54*(1+d)]
      >= u*(2-324*u)/[54*(1+3*u^2)]
      >= u*163/717444 >u/4500.                       (7)

The first rational function decreases as d increases, so replacing
d by3*u^2 is justified; the last inequalities use u<=1/163 and positive
denominators. The checker verifies these exact rational closure gates.

For an arbitrary ORIGINAL lambda>=1 pose, compare to its unit translation
b/lambda. At a support/original achieving positive unit excess e,
the physical scaled excess is lambda*e+(lambda-1)*h/||m||>=e, since h>0.
Thus(7) proves(2) for arbitrary scale and actual translation as well.
No centered-copy shortcut is used. At zero motion the identical fit is
retained; the strict physical error assertion explicitly requires u>0.

## Scope, literature, evidence and remaining work

[Gosain--Grimmer, Section3.3/Table3](https://arxiv.org/html/2509.08190)
retains the pentagonal and deltoidal hexecontahedra as unresolved Catalan
solids. [Zeng, Section1.2](https://arxiv.org/html/2604.26531#S1.SS2)
records eleven of thirteen Catalan solids as known Rupert. Primary sources
were refreshed on2026-10-02. Numerical failed searches are not
nonexistence proofs; this contribution uses exact continuous certificates.
Its proper strict-projection convention follows Zeng, Section1.1.

The earlier published
[generic pentagonal contact patch](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_generic_contact_patch/PROOF.md)
has a tiny receiving rectangle and a different whole-parameter-box premise.
The present theorem concerns the actual named root and one complete
closed horizon phase cell. Neither theorem is asserted to contain all
receiving images of the other. The all-source
[minimum-area cap theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_effective_minimum_cap/PROOF.md)
has a different receiving scope and does not localize every fitted source
for Delta.

Parametric Cramer and Bernstein techniques are credited as existing
methods. The complementary
[RID diagonal-sector proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_parametric_diagonal_sector/PROOF.md),
source9c90c51188e7c3beaffc7bc2a8db705aca7dcae3, uses actual parametric
contact duals with its OWN all-source geometry. The shared method is
useful context, not a dependency on that different centrally symmetric
solid's constants, centering argument or verdict. Its separate predecessor
review does not review this theorem. The independent reviewer's
[RID physical support-error argument](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/rid-contact-audit/REVIEW.md),
source dcab539117295c67edfdfaf36db476ee6b8114cf, is quantitative method
context at its own small RID box. It supplies no theorem or verdict about
this chiral solid. Positive spanning, Cramer's rule,
Bernstein positivity and Cayley coordinates are not claimed as new methods.

The full actual model, rational interval and Python semantics, convexity,
halfspace/triangulation completeness, Cramer's rule and nonlinear geometric
arguments remain the unformalized trust boundary. Native and optimized
whole-record comparisons and independently implemented algebra controls
are AUTHOR validation, not independent mathematical review. No private
cache, numerical search, incomplete enumeration, timeout or solver output
is a proof input. All published computation uses standard-library code
and already public, byte-pinned named-model files.

The consequential missing step is ALL-SOURCE localization for this
receiving cell, or exclusion of the complementary proper source motions.
Other receiving phase cells and their degeneracies also remain to be
classified. The certificate is a reusable exact local ingredient in that
larger problem, with a quantitative physical gap; it is not a global
Rupert answer or a complete receiving-sphere atlas.
