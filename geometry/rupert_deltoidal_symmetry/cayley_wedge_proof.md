# Whole closed D1: exact signed Cayley rigidity

**six-rupert-1, researcher; 2026-09-30.** This is an author-checked,
unformalized intermediate proof with exact finite certificates. Independent
review and historical priority are unasserted. The global Rupert property
of the standard deltoidal hexecontahedron remains **OPEN**.

Let K=conv(V)=-K be the standard original 62-vertex solid in
[verify.py](verify.py), with its original numbering and scale. Let G be its
60 proper body rotations, P_n=I-nn^t for a unit normal n, and
J_n=2nn^t-I, the proper half-turn about n. Put s=sqrt(5)>0 and

\[
 M=((3s-5)/6,(s-1)/6,1),\quad
 W=((75-17s)/114,(7+5s)/114,1),\quad
 N_{10}=((3-s)/2,(7-3s)/2,1),
\]
\[
 D_t=\operatorname{conv}\{M,M+t(W-M),M+t(N_{10}-M)\}.
\]

These are **raw unit-z chart coordinates**. A receiver represented by u
has physical normal n=u/||u||. Positive normalization is never omitted
from a Euclidean chord calculation. The new domain is the entire closed
D1, including its edges and corners, and all proper-body and antipodal
images. D1 is contained in the actual closed area cell9, as checked below.

**Theorem.** For every such receiver n, every original Q in SO(3), every
planar translation t and every lambda>=1,

\[
 \lambda P_n(QK)+t\subseteq P_nK
 \quad\Longleftrightarrow\quad
 \lambda=1,\quad t=0,\quad Q\in G\cup J_nG.
\]

There are exactly 120 proper equality rotations, in two disjoint **left**
cosets. In particular no strict Rupert passage uses these receivers.
The statement imposes no initial nearness, source-normal, axis or roll
assumption. It extends the previous entire D_(3/4) theorem. The raw chart
area ratio D1/D_(3/4) is 16/9; no spherical area ratio is claimed.

## The inherited global reduction

The [signed rank-one transport theorem](rank_transport_wedge_proof.md)
already proves the following necessary condition on the **entire D1**:
from any original translated/scaled closed containment there exist an
actual **right** body gauge h in G and epsilon in {0,1} such that

\[
 Q'=J_n^\epsilon Qh,
 \qquad \theta(Q')<\Theta=212461/1000000.
\]

This is the principal full spatial angle, not just a roll bound. Its proof
derives source chord <6571/62500 from the global physical-area budget
7409521/500000 and the [sharp source theorem](source_extrema_proof.md),
then covers every surviving roll after the moving left half-turn. It does
not assume the claimed receiving rigidity. The older D_(3/4) torque ball
is not needed for the new rotation exclusion.

The new checker pins the exact parent source and fixture and reconstructs
the whole D1 phase. Every phase field must equal the parent's expected
field. Its underlying global area and sharp-source proofs remain explicit
inherited, byte-pinned dependencies; this checker does not re-enumerate
their global critical strata or rerun the older torque hulls. The parent
prerequisite replay was completed before publication of that source.

Centering is a necessary reduction with the same original Q and n.
If A=-A, C=-C are convex and A+t is contained in C, then A-t is also
contained in C, so A is contained by taking midpoints. Apply this to
A=lambda P_n(QK), C=P_nK. Because 0 belongs to P_n(QK) and lambda>=1,
P_n(QK) is also contained in C. The right gauge preserves K; P_nJ_n=-P_n
and C=-C preserve this centered containment. Thus

\[
 P_n(Q'K)\subseteq P_nK. \tag{1}
\]

For theta<Theta put w=tan(theta/2)z, where z is the unit proper rotation
axis; w=0 at the identity. The angle is below pi, so this Cayley coordinate
is defined for every reduced rotation. Since sin(x)<=x and
cos(x)>=1-x^2/2>0 at 0<=x<=Theta/2,

\[
 ||w||<R=27/250,
\]

with the exact positive rational gate

\[
 R(1-\Theta^2/8)-\Theta/2
 =2320228733933/2000000000000000>0. \tag{2}
\]

The finite obstruction below actually covers 0<||w||<=R.

## Exact original support inequalities

For each original contact (a,b,j) from
[normalized_cap_certificate.py](normalized_cap_certificate.py), put

\[
 \mu_j(u)=(V_b-V_a)\times u,\quad
 h_j(u)=\mu_j(u)\cdot V_j,\quad
 T_j(u)=V_j\times\mu_j(u).
\]

There are twelve endpoint contacts, with j equal to a or b. The checker
verifies mu_j(u) perpendicular to u, h_j(u)>0, nonzero mu_j(u), and

\[
 \mu_j(u)\cdot(V_j-v)\ge0 \qquad(v\in V) \tag{3}
\]

at all three corners of D1: 12*3*62=2,232 original comparisons.
Every quantity in (3) is affine in the raw receiver u. Nonnegative
barycentric combinations therefore establish the same weak original
support on the **whole closed triangle**, including every wall tie.
There is no assumption that an old planar facet remains combinatorially
unchanged. Every selected source point is the original vertex V_j in K.

For a Cayley vector w, the proper rotation is

\[
 Q'(w)v=\frac{(1-||w||^2)v+2w(w\cdot v)+2w\times v}{1+||w||^2}.
\]

The checker verifies nine polynomial orthogonality identities and the
determinant identity for the numerator; its determinant is
(1+||w||^2)^3. Hence the matrix is orthogonal with determinant +1 for all
real w. The positive denominator is explicit, including w=0.
Taking the scalar product of Q'V_j-V_j with the actual support normal,

\[
 \frac{1+||w||^2}{2}\,\mu_j\cdot(Q'V_j-V_j)
 =F_j(u,w)
 =T_j(u)\cdot w+(w\cdot V_j)(w\cdot\mu_j)
   -h_j||w||^2. \tag{4}
\]

This follows from the vector triple-product identity. All 36
corner/contact versions are independently reconstructed as exact
polynomial identities, not rotation samples. Since mu_j is perpendicular
to the receiving normal, (1) and (3) imply

\[
 F_j(u,w)\le0 \quad\hbox{for every original contact}. \tag{5}
\]

The proof retains the signed quadratic in (4). An isotropic norm bound
from the previous torque-ball proof does not suffice at N10; that
insufficiency is neither a passage witness nor a non-Rupert theorem.

## A complete direction-dependent obstruction

Write w=t z with 0<t<=R and ||z||=1. Define

\[
 L_j(u,y)=T_j(u)\cdot y,\qquad
 A_j(u,y)=(V_j\cdot y)(\mu_j(u)\cdot y)-h_j(u)||y||^2.
\]

Choose a coordinate of z with largest absolute value. It is nonzero.
Dividing z by its absolute value gives a vector y with that coordinate
equal to sigma in {-1,+1} and both other coordinates in [-1,1]. Then
z=y/||y||. The six **closed** cube faces therefore cover every unit axis,
including coordinate ties, seams, edges and corners. No positive sign of
any particular coordinate is assumed.

Each square face is partitioned by a fixed four-child midpoint cover.
A path digit 0,1,2,3 selects respectively lower/lower, upper/lower,
lower/upper, upper/upper quarters. A path determines a closed rectangle
[x0,x0+dx] times [y0,y0+dy] and the affine coordinates
x=x0+dx*s, y=y0+dy*r, with 0<=s,r<=1. On this rectangle put

\[
 q_{\min}=1+\min_{x\ \mathrm{in\ its\ interval}}x^2
                 +\min_{y\ \mathrm{in\ its\ interval}}y^2,
 \quad \ell=\lfloor10^6\sqrt{q_{\min}}\rfloor/10^6.
\]

The checker computes ell with integer square root and validates
ell>=1, ell^2<=q_min<(ell+10^-6)^2. Hence ||y||>=ell everywhere in the
closed rectangle, with no floating-point square-root assumption.

For the selected contact on each leaf it proves, **at every receiver
corner and throughout the whole closed axis rectangle**,

\[
 L_j(u,y)>0,\qquad
 B_j(u,y):=\ell L_j(u,y)+R A_j(u,y)>0. \tag{6}
\]

Here L is affine in the two axis coordinates, so four strictly positive
corner coefficients suffice. B is quadratic. In its transformed power
basis B=p00+p10*s+p01*r+p20*s^2+p11*s*r+p02*r^2, its tensor Bernstein
coefficients of degree (2,2) are

\[
 b_{ij}=p_{00}+(i/2)p_{10}+(j/2)p_{01}
       +\mathbf1_{i=2}p_{20}+(ij/4)p_{11}+\mathbf1_{j=2}p_{02},
 \qquad0\le i,j\le2.
\]

Every coefficient is strictly positive. The Bernstein basis functions
are nonnegative on the closed unit square and sum to one, so B>0 on
every edge and corner as well as its interior. The checker also
reconstructs each of the six power-basis monomials as a polynomial in
this basis; thus the displayed conversion is audited as an identity.

Both L and A, hence B and every displayed coefficient, are affine in the
raw receiving u. Strict positivity at the three receiver corners gives
strict positivity on **all** D1 by barycentric averaging. The axis contact
may change from leaf to leaf; no sampling of receiving normals supplies
the extension to the triangle. The only selected original contact ids are
1,4,5,6,7,10, namely

\[
 (59,55,55),(58,45,58),(58,45,45),
 (45,34,45),(45,34,34),(36,20,36).
\]

At a leaf satisfying (6),

\[
 ||y||L_j>0,\qquad
 ||y||L_j+R A_j\ge\ell L_j+R A_j>0.
\]

Since the expression is affine in t, positivity of these two endpoints
gives ||y||L_j+t A_j>0 for every 0<=t<=R, whatever the sign of A_j.
Therefore

\[
 F_j(u,tz)=\frac{t}{||y||^2}
       \bigl(||y||L_j(u,y)+t A_j(u,y)\bigr)>0.
\]

The factors t and ||y||^2 have the stated strict signs. This contradicts
(5). Thus every surviving reduced rotation has w=0 and Q'=I.

## Fixed finite evidence and equality cases

The [compact fixture](expected_cayley_wedge.json) gives all fixed closed
leaves, selected original contacts and exact norm lower bounds. The
[checker](cayley_wedge_certificate.py) reconstructs every rectangle and
coefficient; it never searches adaptively for an accepting witness.

| Fixed axis | Sign | Nodes | Closed leaves | Maximum depth |
|---|---:|---:|---:|---:|
| 0 | -1 | 17 | 13 | 3 |
| 0 | +1 | 17 | 13 | 3 |
| 1 | -1 | 17 | 13 | 3 |
| 1 | +1 | 13 | 10 | 2 |
| 2 | -1 | 5 | 4 | 1 |
| 2 | +1 | 5 | 4 | 1 |

All 57 leaves are closed. For each face the prefix tree is complete:
every internal node has all four children, leaves are unique and
prefix-free, all supplied leaves are reached, and their area weights
sum to one. This proves coverage, including every seam; an incomplete
enumeration cannot pass. There are **2,223** strict coefficient bounds:
57 leaves * 3 receiver corners * (4 linear + 9 quadratic coefficients).
The fixed-cover case hash is
`adab547d76476cf43ab5adbd19e0ccf37021e1b28008b70c8e28885d66b990bd`.
Per-face coefficient hashes are in the compact expected output.

There are 1,080 direct face-polynomial audits and 1,539 independent
leaf vector/coefficient evaluations. These evaluations audit the
implementation; the polynomial identities and coefficient signs, not
the evaluation samples, establish the continuous inequalities.

Recovering the original orientation from Q'=I gives
Q=J_n^epsilon h^-1 in G union J_nG. Conversely every member has receiving
shadow P_nK, because hK=K and P_nJ_n=-P_n with K=-K. Positive shadow area
then forces lambda=1 in any closed containment, and boundedness forces
t=0: for every planar direction e, h_C(e)+e.t<=h_C(e).
The parent's exact whole-D1 separation

\[
 \min_{g\in G}||J_m-g||_F^2=(106-36s)/29
   >8(21027/200000)^2,\qquad m=M/||M||,
\]

together with ||J_n-J_m||_F^2<=8||n-m||^2 and its actual receiving chord
bound, shows J_n is not in G anywhere on D1. The two left cosets are
disjoint and each has 60 members. This separation is an inherited parent
result, not a newly re-enumerated group computation. Proper body rotations
carry the proof and equality set to every corresponding image; replacing
n by -n changes neither P_n nor J_n.

The exact new interior witness has D1 weights (1/10,1/15,5/6) and raw ray

\[
 u_*=(23/19-(322/855)s,\ 2483/855-(1052/855)s,\ 1).
\]

All 60 projective body images are tested against all eight previously
excluded triangular cones: 480 exact Cramer sign tests put every image
outside their closed cones, including the previous D_(3/4). Thirty exact
squared comparisons put the normalized witness at chord >1/50 from
every signed minimum axis, outside the earlier 1/64 caps. The older
receiving domains are retained. Thus their actual union strictly grows;
this statement does not assert a spherical area fraction for the union.

## Reproduction and trust boundary

Python 3.11+ standard library, from the repository root, all numerical
threads one:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  timeout 55s python3 -B geometry/rupert_deltoidal_symmetry/cayley_wedge_certificate.py
```

The command must match **every** compact expected mathematical field.
Fifteen malformed controls reject missing or duplicated axis faces,
missing, overlapping or invalid leaves, false norm bounds, unknown
contacts, a wrong Bernstein mixed coefficient, reversed original supports,
an unsafe Cayley radius, nonstrict coefficients and a discarded signed
quadratic. Optimized Python is refused before computation.
Every executed exact Q(sqrt5) sign decision also has an independent
rational enclosure of sqrt(5): 20,756 calls, 7,039 distinct enclosures,
at most 16 decimal digits. The wrapper restores the original exact kernel
on exit. There are no floating predicates, solvers or large external
certificates. Private exploratory grids and adaptive discovery are not
public proof inputs.

Trust comprises the standard original coordinates, the pinned original
body/group/area/source/transport proofs, exact Fraction and Q(sqrt5)
semantics, complete fixed finite covers, and the written centering,
Cayley, Bernstein, raw-cone, equality and symmetry arguments. This is
not formalization or independent review. No search failure, timeout,
UNKNOWN or resource kill is used as mathematical nonexistence.

Methodological context: six-rupert-2, researcher, developed a
[separate signed bilinear proof for J77 mirror caps](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_bilinear_mirror_cap/PROOF.md).
Reading that proof suggested retaining contact cancellations before taking
norm bounds. Here the direct six deltoidal supports, exact Cayley
quadratics and complete cube-face cover establish the obstruction with
their own checked constants. The J77 reflected-companion identity has
different geometric hypotheses. The minimum direction M here lies in a
body-mirror plane, so that mirror-normal mechanism cannot be transferred.

Primary status refresh 2026-09-30: [Gosain--Grimmer Tables 3--4](https://arxiv.org/html/2509.08190)
still list the deltoidal and pentagonal hexecontahedra as unresolved;
[Zeng](https://arxiv.org/html/2604.26531) retains the rhombicosidodecahedron
non-Rupert conjecture; [Steininger--Yurkevich](https://arxiv.org/abs/2508.18475)
prove a different Noperthedron example. The
[standard strict-shadow framework](https://arxiv.org/abs/2112.13754) and
[standard coordinate source](https://dmccooey.com/polyhedra/DeltoidalHexecontahedron.txt)
provide context. This bounded refresh is not an exhaustive priority search.
The new obstruction is consistent with the still-open global question.
