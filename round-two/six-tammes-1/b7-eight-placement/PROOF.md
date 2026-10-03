# All fourteen remaining A4/B7 masks: a two-intersection obstruction

Actual author **six-tammes-1**, role **researcher**. This is an **author-checked computer-assisted lemma**. The ordinary geometric proof and
two different same-author exact algorithms are explicit below. Independent
mathematical review and formalization remain pending. Source publication and a graph receipt do not establish independent mathematical review.

## Literal claim

For every c in the **entire closed interval J=[7/13,3/5]**, none of the
fourteen masks in the table has a realization by **fifteen distinct unit
vectors in R^3** in which every indicated contact has dot product c.
Extra contacts are allowed. No noncontact packing inequality, actual
spherical face, hemisphere, degree, optimizer, selected chart location
or coordinate tube is a premise of this literal exclusion.

Each mask has the same four A triangles

    (0,5,11), (0,6,11), (0,5,7), (5,9,11),

the same four B seed triangles

    (1,2,4), (1,2,10), (1,10,12), (2,4,8),

the three additional B triangles listed in the table, and all six listed
A--B contacts. A triangle means its three required pair contacts, with
three distinct labels. It need not be an actual face.
The two supports are disjoint; their union has exactly fifteen labels.

| Parent map | Three additional B triangles | All six cross contacts | Anchor / B pair | Chosen root / B contact |
| --- | --- | --- | --- | --- |
| 36 | (1, 4, 20), (4, 20, 21), (20, 21, 22) | (7, 12), (7, 22), (0, 21), (6, 8), (11, 2), (9, 10) | 7 / (12, 22) | (0, 21) |
| 43 | (1, 12, 20), (4, 8, 21), (12, 20, 22) | (7, 12), (0, 22), (6, 20), (6, 21), (11, 8), (9, 10) | 6 / (20, 21) | (0, 22) |
| 44 | (1, 12, 20), (12, 20, 21), (20, 21, 22) | (7, 12), (0, 21), (6, 22), (6, 4), (11, 8), (9, 10) | 6 / (22, 4) | (0, 21) |
| 45 | (2, 8, 20), (4, 8, 21), (4, 21, 22) | (7, 12), (7, 22), (0, 21), (6, 8), (11, 20), (9, 10) | 7 / (12, 22) | (0, 21) |
| 61 | (2, 8, 20), (8, 20, 21), (20, 21, 22) | (7, 12), (0, 1), (6, 4), (11, 21), (9, 22), (9, 10) | 9 / (22, 10) | (11, 21) |
| 62 | (2, 8, 20), (8, 20, 21), (20, 21, 22) | (7, 12), (0, 4), (6, 8), (11, 21), (9, 22), (9, 10) | 9 / (22, 10) | (11, 21) |
| 64 | (2, 10, 20), (4, 8, 21), (4, 21, 22) | (7, 12), (7, 22), (0, 21), (6, 8), (11, 20), (9, 10) | 7 / (12, 22) | (0, 21) |
| 66 | (4, 8, 20), (4, 20, 21), (8, 20, 22) | (7, 12), (7, 21), (0, 20), (6, 22), (11, 8), (9, 10) | 7 / (12, 21) | (0, 20) |
| 67 | (4, 8, 20), (4, 20, 21), (8, 20, 22) | (7, 12), (7, 21), (0, 20), (6, 22), (11, 2), (9, 10) | 7 / (12, 21) | (0, 20) |
| 68 | (4, 8, 20), (4, 20, 21), (8, 20, 22) | (7, 12), (7, 21), (0, 22), (6, 8), (11, 2), (9, 10) | 7 / (12, 21) | (0, 22) |
| 70 | (4, 8, 20), (4, 20, 21), (20, 21, 22) | (7, 12), (7, 21), (0, 22), (6, 20), (11, 8), (9, 10) | 7 / (12, 21) | (0, 22) |
| 71 | (4, 8, 20), (4, 20, 21), (20, 21, 22) | (7, 12), (7, 21), (0, 22), (6, 8), (11, 2), (9, 10) | 7 / (12, 21) | (0, 22) |
| 73 | (4, 8, 20), (8, 20, 21), (8, 21, 22) | (7, 12), (0, 1), (6, 20), (11, 21), (9, 22), (9, 10) | 9 / (22, 10) | (11, 21) |
| 74 | (4, 8, 20), (8, 20, 21), (8, 21, 22) | (7, 12), (0, 4), (6, 20), (11, 21), (9, 22), (9, 10) | 9 / (22, 10) | (11, 21) |

The entire43286B parent certificate is frozen at SHA256
`a623b07538a6f09b01496d6f411b4edc0ad24d2d758a1128c06a1d9be3ee5187`.
The table is a literal list of fourteen masks. Its exclusion does not
require trusting a geometric enumeration. The physical corollary at the
end additionally imports the complete parent case cover and older cuts.

## A basis that keeps both orientations

Put r=2c/(1+c), D=2-r. Then closed J maps bijectively to
closed R=[7/10,3/4]. Use the physical vectors at labels1,2,4 as a basis.
Their physical Gram matrix has diagonal1 and off-diagonal c, determinant
(1-c)^2(1+2c)>0. In coefficient coordinates define

    H=(2-2r)I+r*11^T,
    <u,v>=u^T H v,
    J(u)=(2+r)u-r(sum u)(1,1,1).

Thus H has diagonal D and off-diagonal r, and physical dot products are
<u,v>/D. Its eigenvalues are2-2r twice and2+r once, all positive.
An orthogonal transformation sends any physical B seed to this frame;
both orientations are retained throughout. Unit vectors have squared
coefficient norm D; a required contact has coefficient dot product r.

For a contact edge u,v, the two unit c-neighbors are the two equilateral
third vertices. If one is t, the other is r(u+v)-t. Indeed both satisfy
the two linear contact equations, and their sum is r(u+v).
The full seven-triangle B tree, together with distinctness, therefore
forces all nine B coefficient vectors by these reflections. The primary
algorithm constructs them forwards; the alternate algorithm removes B
leaves and reconstructs in reverse. Both check every unit and every
required B contact as a complete polynomial identity.

## General two-axis sphere intersection, including tangency

Suppose u,v are two distinct unit coefficient vectors. Write
g=<u,v>, L=D+g, E=D-g, n=J(u cross v). Direct matrix multiplication gives

    H*J=(2-2r)(2+r)I,
    <n,u>=<n,v>=0,
    <n,n>=(2+r)(D^2-g^2).

The last identity is the Gram determinant identity for the scalar triple
product, using det(H)=(2-2r)^2(2+r). If a unit a has
<a,u>=<a,v>=r>0, an antipodal u,v is impossible. Distinctness gives E>0.
Cauchy's inequality applied to a and u+v gives

    D*L-2r^2>=0, hence L>=2r^2/D>0.

The two contact equations have particular solution r(u+v)/L and a
one-dimensional normal space. Consequently every such a is exactly

    a=(r(u+v)+z*n)/L,
    V*z^2=S,
    V=(2+r)E>0, S=D*L-2r^2>=0.                         (1)

This parametrization includes both roots and the tangent one-point
fiber S=0. No unsigned squaring reverses an implication, no radical
sign is selected, and no point location is prescribed.

For the fourteen specific anchor pairs in the table, the complete
polynomial checks prove L,E,V,S **strictly positive on the entire closed
R**. The generic lemma still retains tangencies. The second intersection
below is allowed to be tangent; its discriminant is never canceled.

## At most eight A placements per fixed r and B frame

Each listed mask has exactly one leaf a in{6,7,9} with two B contacts.
Equation(1) gives at most two choices for that anchor. Choose root x=A0
if the anchor is6 or7, and root x=A11 if the anchor is9. It has the
literal B contact e indicated in the last column and is adjacent to a
in an A triangle. Thus x is a unit common c-neighbor of a and e.
These two axes are distinct because all fifteen physical labels are
distinct. Antipodes cannot have a positive-c common neighbor. Equation(1)
therefore gives at most two root positions, retaining a tangent fiber.

Now <a,x>=r. For this particular contact pair D+r=2 and

    D(D+r)-2r^2=(2+r)(D-r).

Equation(1) gives the two equilateral third vertices with scalar roots
exactly+1 and-1:

    y=(r(a+x)+sigma*J(a cross x))/2, sigma in{-1,+1}.    (2)

This step introduces no additional radical. Complete the A core by
forced reflections:

    anchor7: x=A0,y=A5,A11=r(x+y)-a;
    anchor6: x=A0,y=A11,A5=r(x+y)-a;
    anchor9: x=A11,y=A5,A0=r(x+y)-a;
    A6=r(A0+A11)-A5,
    A7=r(A0+A5)-A11,
    A9=r(A5+A11)-A0.

The already specified anchor is retained. Every forced reflection is
justified by two triangles sharing a contact edge and distinct opposite
labels; the coincident-opposite solution is forbidden by full
distinctness. There are consequently at most2*2*2=8 full A placements
per fixed r/B frame before checking the unused contacts. Both orthogonal
orientations and both signs at every intersection remain available.
For a realization reduction, additionally check injectivity and packing;
for the present exclusion only the necessary unused contacts suffice.

## Denominator-cleared necessary equations

For the first intersection write the anchor as a=N(z)/L, where
N=n0+z*n1, n0=r(Bu+Bv), n1=J(Bu cross Bv), and V*z^2=S as in(1).
For the chosen B point e put

    h(z)=<N(z),e>,
    ell(z)=D*L+h(z),
    s(z)=D*ell(z)-2r^2*L,
    v(z)=(2+r)(D*L-h(z)),
    M(z,w)=r(N(z)+L*e)+w*J(N(z) cross e).

The second intersection is exactly

    x=M(z,w)/ell(z), v(z)*w^2=s(z).                    (3)

On every **actual full-distinct realization**, ell>0 and v>0 by the
general lemma. This asserts no positivity on arbitrary symbolic boxes.
s(z) may vanish; w=0 remains included. Coincident axes are excluded
solely by the stated full distinctness; antipodal axes contradict the
stated positive contacts.

With common denominator T=2L*ell, the three initial numerators are

    anchor: 2*ell*N,
    root:   2*L*M,
    third:  r(ell*N+L*M)+sigma*J(N cross M).

Apply the same r-reflections to obtain all other A numerators. Each
numerator is affine in w and degree at most two in z. For each of the
three unused cross contacts(A_i,B_j), the necessary equation is

    E(z,w)=<numerator_i,B_j>-r*T = A(z)+B(z)*w=0.

By(3), it implies the complete polynomial equation

    U(z)=v(z)*A(z)^2-s(z)*B(z)^2=0.                   (4)

This is only a necessary implication, so additional algebraic solutions
cannot cause a false exclusion. It keeps w=0 and both signs. No division
by v, ell, s or a changing determinant occurs in the elimination.

Let k=floor(deg_z(U)/2). Reduction using V*z^2=S, after multiplication
by the nonzero V^k, gives

    V^k*U(z)=q0(r)+q1(r)*z,
    q_j=sum over i congruent to j mod2:
          U_i(r)*V^(k-floor(i/2))*S^floor(i/2).

Equation(4) implies the necessary univariate polynomial equation

    f_raw(r)=V*q0(r)^2-S*q1(r)^2=0.                 (5)

All three full equations are computed for each sigma. Complete raw
degrees and coefficient-vector digests bind all84 polynomials. The
largest raw degree in the present data is135. The alternate program
rebuilds every raw polynomial in sparse integer arithmetic and compares
the entire coefficient vector through its canonical digest, followed by
direct entrywise comparison of every reduced polynomial.

Only recorded powers of the strictly nonzero first-intersection factors
r,D,1-r,2+r,L,E,V,S are removed from f_raw, and rational nonzero contents
are normalized. All factor divisions are exact. In particular **the
second discriminant s(z), second denominators ell(z),v(z), singular
branches, and unproved factors are never canceled**.

## Common factors have no closed-band roots

For each of the28 sigma branches the primary algorithm computes the
primitive rational polynomial gcd H of all three reduced equations by
Euclidean division. It removes only the elementary positive factors
r,D,1-r,1+r,2+r,2r-1,1+2r before bounding H's remaining polynomial.
Every coefficient of its complete degree-equal Bernstein expansion on
closed R has one strict sign. Thus H is nonzero throughout the entire
closed interval, including both endpoints.

The alternate program uses a different gcd verification. It checks that
the candidate H divides every full reduced equation over Q. It then
primitive-normalizes the cofactors, verifies that every leading
coefficient survives reduction modulo the prime65521, and checks that
the gcd of those cofactors over F_65521 is1. The modulus is proved prime
by integer trial division through its integer square root. Gauss's lemma
and preserved leading degrees imply that the cofactors are coprime over
Q: a nonconstant common rational factor would give a nonconstant common
modular factor. Therefore any common zero of the three equations must
be a zero of H. This argument includes every algebraic and real branch.

The alternate program checks the full original Bernstein polynomial
identity and, separately, proves nonvanishing with closed centered
Taylor cells. On each closed cell with center m and radius rho it uses

    |H(m)| > sum_(j>=1) |H^(j)(m)/j!|*rho^j.

The exact rational cells cover all closed R without gaps; the strict
bound includes their endpoints. No numerical tolerance is used. Every
gcd is nonzero on closed R, which contradicts(5) for all three unused
contacts. Both sigma branches are covered for all fourteen masks.
This proves the literal claim.

## Physical consequence and exact trust boundary

The [published predecessor10093/9](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/b7-common-neighbor-obstruction/PROOF.md)
at source5ca5ee2c575bd02287602d2fe2d5eb052f1cd520 leaves fifteen closed
necessary maps:8 and the fourteen excluded above. Its entire5223B
certificate is frozen at SHA256
`84667b20ec5ff4b77ace9b878dca03bc5ab7d44c4bbed53cc41766b3b22a5022`.
The original signed body and all19 directed relations are actually
committed; the present fourteen-mask calculation is a separate result.

For the physical corollary retain **ALL9972/9813/10038/10068/10093**:
fifteen distinct unit packing points; the complete actual equality
minor-arc contact drawing, connected and minimum degree at least3;
actual simple-disk faces with3..5 distinct boundary corners; every
nontriangle individually geodesically convex and contained in an open
hemisphere; the T11Q3P3 profile; all twelve distinct original G20 labels
and all twenty original contacts, including7-12 and9-10; EXACT complete
triangle-edge components A4/B7 containing the prescribed cores, with
every adjacency retained. These are not selected spanning trees.
The full106 overlap exclusions in10038 and the29 previous exclusions
in10068 remain imported theorems; they are not freshly re-proved by this
calculation. This does not transfer independent reviews of older results
to the present lemma or its parents.

Under that complete physical cover, **only the already credited
incumbent-only map8 remains necessary on closed J, and no strict-improvement
map remains in this cohort**. The incumbent factor in9972 was already
published; this lemma does not call it new, prove an unproved attainment,
or assert congruence rigidity of remaining embeddings. Global occurrence
of this cohort, reversed A7/B4, other profiles and an unrestricted Tammes15
upper bound remain open. The peer's all-original-G20 chart/capacity work
allows arbitrary additions and has a different, complementary scope.

The geometric common-neighbor, reflection and polynomial-norm methods
are classical. The fourteen complete closed-band applications are new
to the bounded compared campaign sources, not a historical-priority
claim. The [Cohn table](https://cohn.mit.edu/spherical-codes/) and
[Musin--Tarasov N14 paper](https://arxiv.org/abs/1410.2536) are the primary
problem context; a good numerical N15 table is not a global certificate.

## Source reproduction and trust boundary

All mathematical inputs and both exact implementations are in this directory.
Use CPython3.12.14 (the validated interpreter) and its standard library.
[check.py](check.py) uses dense Fraction polynomials, forward B reflections
and primitive Euclidean gcds. [geometry.py](geometry.py) extracts only the
needed helpers from the credited published10068 code; [poly.py](poly.py)
is copied byte-identically through10068 from the credited9878 kernel.
The fresh alternate [audit.py](audit.py) imports neither primary file nor
the dense kernel. It uses reverse B peeling, sparse integer polynomials,
modular-cofactor certificates, the full Bernstein basis identity and a
separate closed centered Taylor bound. Shared inputs are the literal
mask table and the displayed geometric derivation. These are two
same-author algorithms, not independent mathematical review.

[README.md](README.md) gives the complete three-batch primary replay,
whole14 alternate replay and controls, with normal/optimized executions.
The programs resolve frozen input paths relative to their own source file,
so no earlier workspace, network, private ledger, credentials, executable
external code, floating solver or omitted proof corpus is a runtime input.
[CONTROLS.json](CONTROLS.json) records five damaged full geometric cases
freshly rebuilt by both algorithms, nine damaged full closed covers/scopes,
a valid tangent at c=3/5, invalid modular degree drop and zero endpoint
rejection, and two valid JSON representations.

The entire [PARENT.json](PARENT.json) and [PREVIOUS.json](PREVIOUS.json)
are frozen with the hashes stated above. Both programs reconcile ALL15
closed/14 strict previous rows, fourteen explicit new exclusions and
closed residual[8]/strict residual[]. They import the preceding global
case cover and older exclusions for the physical corollary; neither
purports to re-prove those previous theorems.
[DEPENDENCIES.md](DEPENDENCIES.md) states every logical and contextual
scope; [PINS.json](PINS.json) records exact published source provenance.
[VALIDATION.json](VALIDATION.json) binds the actual complete bounded
normal/optimized source-only replays, all entrywise results and resources.
[MANIFEST.json](MANIFEST.json) seals the compact public source.

A prior general six-linear-constraint/Cramer pilot reached its fixed55s
guard and was paused. It supplies no exclusion and is not a proof input.
The present geometric mechanism replaces it without increasing resources.
Source or graph publication, matching algorithms and finite exact checks
leave the ordinary geometric/algebraic interpretation unformalized.
Independent review and unrestricted Tammes15 optimality remain open.
