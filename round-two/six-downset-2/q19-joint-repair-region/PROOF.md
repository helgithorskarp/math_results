# The complete q19 joint repair region

six-downset-2 / researcher. Exact computer-assisted lemma with ordinary
affine, geometric, completeness and spectral bridges. Unformalized and
independently unreviewed. The completed reader run is recorded in
VALIDATION.json; source and graph delivery are separate provenance.

## Statement and normalization

Use the same fixed downset, signed comparison and individual-edge cost as
ACTUAL LEMMA10332/0, source58f9c6ab8b6ab58232cd275ddb4691d3430fb02f:
[published proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/q19-sharp-star-extension/PROOF.md)
and [physical completeness criterion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/q19-sharp-star-extension/STRUCTURAL.md).
Its H matrix is not an input to this new calculation. Only the defining143
comparison coefficients, openly reused exact model, and already proved
physical criterion are used; all new factors are freshly computed.

The core is a,b,c, with |X|=9, |Y|=10. Include all sets of size at most2
and all triples with at least two core points, except the triples bcX.
Keep the actual empty vertex and its loop. N=303, the unique largest
a-star has s=61, and h=N-s=242. A symmetric proper C has diagonal60,
intersecting off-diagonal entries -1, and C1_S=0. The original lift is

    L = [[1+sum_i r_i, (1-r_i)_i], [(1-r_i)_i, (1+C_ij)_ij]],
    r_i = sum_j C_ij,       M=(L-61I)/242.

Thus M has the original disjointness support and row sums1. Its entry
floor epsilon means every allowed original entry, including the empty
loop, is at least epsilon. Put tau=242epsilon and

    P0=8421443/65536,       P=P0+38tau.

The comparison free coefficients are exactly29u/32768, where the143
integers u are recovered from the defining published q17 fixture. No
q17/q18/q19 old factor, floor, review verdict or executable of a peer
is used as new spectral evidence.

Retain the following comparison-to-repair KK decrements per unordered edge:

    beta=(13379/16384+tau)/36               on YY/bcY,
    eta =(10683/32768+tau)/9               on bY/cY,
    alpha=(362147/32768+tau-8beta)/28       on YY/YY.

Throughout tau>=0 and pXX,pX,pY,d>=0 are the template domain premises.
Choose nonnegative total positive GG masses pXX,pX,pY with sum P, and
increase XX/XX, X/X and Y/Y respectively by pXX/378, pX/36 and pY/45.
Here X/X and Y/Y mean distinct singleton pairs. Retain the31 anchored
star-to-X trades from10332: for D of types aY,abY,acY,abc and each of
the9 X singletons, increase C_DX by (ell_D-tau)/9 and impose its opposite
change on C_aX by the required original star kernel. The comparison
empty values are

    ell_aY=18079/32768, ell_abY=ell_acY=-11507/16384,
    ell_abc=-66079/32768.

Finally, for each45 YY pair decrease C_abc,YY by d and increase C_a,YY
by d via forced anchor completion. Here d is a nonnegative real number.
All other independent coefficients retain the comparison values.
This defines a four-dimensional affine family in (tau,pXX,pX,d), with
pY=P-pXX-pX. The theorem is about this specified template only.

Define

    A(tau)=1043037/16384-18tau,
    B(tau)=1080063/16384-(9/2)tau,
    C(tau)=649645/16384-5tau,
    b=827/32768,             R=91211/16384,
    tau_max=19967/229376.

The following are equivalent within this four-coordinate template:

1. Its original matrix has every allowed entry at least tau/242.
2. The ten affine conditions hold:

       tau>=0,
       0<=pXX<=A(tau), 0<=pX<=B(tau), 0<=pY<=C(tau),
       d>=0, d>=tau-b, 32tau+45d<=R,
       pXX+pX+pY=P.   [The final equality eliminates pY; it is not
                       counted among the ten inequalities.]

3. It is an original entry-feasible H matrix with this cost and the
   stronger spectral comparisons

       T >= I/1024,       303G^-1-T >= I/1024,
       G=I+rr'+zz',   r=1_(a-star in Q), z=1-r, Q=D\{empty,a}.

The entire region projects onto EXACTLY0<=tau<=tau_max. It has dimension4
and sixteen vertices. For EVERY real point in it, both greatest original
ranks are302; M has simple minimum eigenvalue -61/242 and simple unit
eigenvalue, and each of its other301 eigenvalues has both gaps at least
1/247808. For tau>0 every allowed original entry is strictly positive.

Consequently, for ALL individual-real original H competitors, without a
symmetry or template restriction, and EVERY real

    0<=epsilon<=19967/55508992,

the minimum individual positive NN repair cost is

    min P = 8421443/65536 + 9196epsilon.

The constructed region attains that unrestricted necessary bound. Its
largest template floor is NOT asserted to be a largest possible floor,
largest unrestricted sharp-cost interval, or global H existence threshold.

## Necessity and the sharp template obstruction

The changed NN degrees still give all75 bad empty values and the actual
empty-loop value tau. Proper degree equations give

    E_empty,XX=ell_XX-pXX/18,
    E_empty,X =ell_X -2pX/9,
    E_empty,Y =ell_Y -pY/5,
    E_empty,abc=tau+45d,
    E_empty,a=R-31tau-45d,
    h M_a,YY=b+d,

where ell_XX=115893/32768, ell_X=120007/8192 and
ell_Y=129929/16384. Their floors give the stated three upper mass
capacities and two nontrivial release inequalities. Domain nonnegativity
gives the other conditions. Every retained KK decrement is positive over
the derived interval; all KG changes vanish and all GG changes are
nonnegative. Hence the individual-edge cost and equality signs are exact.

Two ORIGINAL entry surpluses yield a two-row Farkas certificate:

    45*(b-tau+d)+(R-32tau-45d)
           = R+45b-77tau
           = 77*(19967/229376-tau).

Thus no point of this specified template with larger tau can meet its
entry floor. At tau_max both rows are forced to zero and
d=7089/114688. This obstruction does not quantify arbitrary H matrices
or arbitrary cost optimizers, whose unpenalized star changes can differ.

## Ordinary vertex-completeness proof

Put u=A(tau)-pXX and v=B(tau)-pX. Let

    H(tau)=2669537/65536-(131/2)tau,
    J(tau)=70957/65536-(121/2)tau,
    U(tau)=(R-32tau)/45,
    t_mass=70957/3964928.

The two-row certificate and tau>=0 bound tau by tau_max. At both ends
of that interval A,B,C,H,A-H,B-H are strictly positive; all are affine,
so they remain positive throughout. In particular pXX,pX positivity
is automatic from the following moving polygon conditions:

    u>=0, v>=0, max(0,J(tau))<=u+v<=H(tau),
    max(0,tau-b)<=d<=U(tau).

This is equivalent to the ten inequalities. Also
0<t_mass<b<tau_max, J(t_mass)=0 and U(tau_max)=tau_max-b.
The mass slice is a quadrilateral before t_mass and a triangle afterward;
its vertices are the two coordinate-axis endpoints at sum H and, when
J>0, the two axis endpoints at sum J, otherwise the origin. The release
slice is the stated interval. On each of the three closed tau intervals
[0,t_mass], [t_mass,b], [b,tau_max], all these vertices and both release
endpoints are affine in tau. A product of a polygon and an interval is
the convex hull of products of its vertices and interval endpoints.
Interpolation therefore expresses every point as a convex combination
of products at these four transition slices.

There are23 such slice endpoint points before duplicates/redundancy:
8 at0,6 at t_mass,6 at b,3 at tau_max. Seven are redundant. The outer
axis vertices at upper d at t_mass and b interpolate directly between
0 and tau_max (four points); the outer axis vertices at lower d=0 at
t_mass interpolate between0 and b (two points); the origin mass vertex
at upper d at b interpolates between t_mass and tau_max (one point).
The program geometry.py checks every complete coordinate equality and
the exact rational convex weight. The remaining vertices are exactly:

    tau0: four mass-polygon vertices times d in {0,U(0)};       8
    tau=t_mass: origin (u,v)=(0,0), d in {0,U(t_mass)};          2
    tau=b: three mass-triangle vertices, d=0;                  3
    tau=tau_max: three mass-triangle vertices, d=tau_max-b.     3

Thus their convex hull is the complete region. They are actual vertices:
each has four independent active facets. A separate exact enumeration
checks all210 four-facet subsets:78 singular subsets have full rational
nonzero null witnesses;132 have verified inverse products, of which116
have an explicit negative facet and16 are feasible. The WHOLE resulting
vertex sets agree with the geometric construction. This is finite exact
coverage of the stated polyhedron, not a sampling/completeness inference.

The region is nonempty at both tau endpoints, so convexity gives every
real tau in between. Strict inequalities at the successful first test
tau1/12 with masses(5P/16,7P/16,P/4),d3tau/4 show dimension4.

## Entire entry sufficiency and both physical spectral comparisons

The180 original scalar entry rows consist of143 disjoint proper type
pairs,13 anchor/nonstar types,22 empty/residual types, the empty/anchor
row and the empty loop. Five rational affine generators (the origin
and four coordinate units) span the four-parameter recipe. They need
not be feasible. At EACH generator affine_check.py checks EVERY72817
allowed original position against its scalar affine surplus, with
complete row coverage. Separate literal-set and named-core-pair original
readers agree on every L and T entry before hashing them. The separate
reader verifies both full303-square physical lifts, both301-square
inverse-metric products, and all181202 original row/basis action images
at every generator. The complete301-dimensional basis and all90601
Gram positions are checked once, with identical sets at every generator.

Every entry row is affine. At all sixteen vertices every one of the180
original entry rows is nonnegative. Convex interpolation proves every
original entry floor throughout the full region. Conversely the ten
rows are actual original entry conditions or explicit domain premises.

At EVERY one of the sixteen vertices the program computes all twelve
weighted forms for both T and 303G^-1-T. They are the two22-dimensional
trivial forms, two8-dimensional X-standard forms, two9-dimensional
Y-standard forms and six scalar forms. Subtracting1/1024 times EACH
physical orbit metric gives freshly verified rational positive LDL
pivots and the complete factor identity at every matrix position.
Across all vertices this pays1344 positive pivots and20224 full factor
identity positions. The original physical actions at all affine
generators and the all-count ordinary completeness proof in10332 ensure
these are the entire original forms, not a sector census without its
action/completeness bridge. All matrices are affine, so their uniform
PSD comparisons persist throughout the convex hull. The full lift and
centered-star projector from10332 then give the stated ranks and gaps.

No positive-eigenvalue inference is made from floating point output;
all new factor identities and original-row tests use exact rationals.
The two implementations and two vertex algorithms are by the same
author and are not independent review or a formal proof assistant.

## Unrestricted sharp cost and trust boundary

The unrestricted individual-edge mass identity from10332 gives
P>=P0+38tau for EVERY original H competitor of entry floor tau/242.
All constructed points have nonpositive KK changes, zero KG changes,
nonnegative GG changes, all75 bad empty entries equal tau, and actual
empty-loop value tau. Thus equality holds with P=pXX+pX+pY. This proves
unrestricted sharpness on the stated interval, while the iff and upper
projection remain restricted to the four-coordinate template.

The primary research target remains Conjecture H in Ellis--Filmus--Friedgut,
[arXiv2609.28404v1 Section4](https://arxiv.org/html/2609.28404v1#S4), not
classical Chvatal/projection packing. No new general H/I, other-count,
largest possible floor, unrestricted optimizer classification, or
independent review is claimed. A full143-variable symmetry-averaging
reduction is a separate unwritten obligation; none is needed to certify
this explicit region and attain an already unrestricted lower bound.

The local source is self-contained: own same-author10332 mathematical
modules and the defining coefficient fixture are explicitly copied and
credited, with complete source seals before mathematical imports. No
published endpoint factor or old floor is loaded. verify.py regenerates
all new region mathematics in fourteen serial source-only normal and
optimized children, with22 actual mathematical damages in each mode.
The entire canonical mathematical record is compared before hashing;
only two explicit top-level runtime observation fields are removed.
VALIDATION.json records actual author completion, not independent review.
These checks do not supply the ordinary convexity, original completeness,
or all-real quantifiers proved above. Timeout, UNKNOWN, interruption and
process/resource limits imply no mathematical absence.
