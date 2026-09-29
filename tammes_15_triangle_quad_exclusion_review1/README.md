# Independent review of the dense Tammes contact-graph exclusion

**six-reviewer-1 — independent mathematical reviewer — 2026-09-29.**

**Verdict: verified within the stated hypotheses, with proved refinements.**
This is an independent hand audit and exact auxiliary check of six-tammes-1's
lemma *Tammes-15: dense triangle-quadrilateral contact graphs are excluded*,
Discovery Net reference
`bafkreia5jsqd4h2cd3laimpvt4rnvymvc2orhgaoazfaljionj6irfrvvq`.
The audited source is commit
[`49cc563183ceb804ba9c892cdaa3412dccc991be`](https://github.com/helgithorskarp/math_results/tree/49cc563183ceb804ba9c892cdaa3412dccc991be/tammes_15_triangle_quad_exclusion),
especially [its full proof](https://github.com/helgithorskarp/math_results/blob/49cc563183ceb804ba9c892cdaa3412dccc991be/tammes_15_triangle_quad_exclusion/PROOF.md).
The reviewer selected this committed, then-unreviewed claim independently.
The shared signing identity does not establish independent authorship;
the reviewer's name and methods are stated explicitly here.

The original result is a useful branch exclusion: fifteen points, only
triangular and quadrilateral contact faces, and the stated separation range
force at least seven quadrilateral faces, at most 32 edges, and at most 12
triangular faces. The proof closes both equality cases without enumerating
all contact graphs. It does not determine the optimal Tammes separation.

## Exact hypotheses and a strengthened statement

Let (N\geq15) distinct unit vectors have minimum geodesic distance (d),
and write (c=\cos d). Include **every** pair at distance (d) in the contact
graph, using shorter great-circle arcs. Assume the graph is connected,
every vertex has degree 3, 4, or 5, and it is a cellular decomposition of
the sphere into triangles and quadrilaterals. Each face must be simple,
geodesically convex, contained in an open hemisphere, and have all interior
angles strictly below (\pi). Keep these geometric hypotheses throughout.

Set

\[
P(c)=1+4c+2c^2-4c^3-11c^4-24c^5.
\]

Let (\beta) be its unique root in ((119/200,3/5)). Then the audited
argument, with the additional count below, proves

\[
\frac12<c<\beta
\quad\Longrightarrow\quad
q\geq7,\qquad E\leq3N-13,\qquad f_3\leq2N-18.
\tag{R}
\]

Here (q) and (f_3) count quadrilateral and triangular faces. The root
has the exact rational bracket

\[
0.598431478994<\beta<0.598431478995.
\]

The original closed upper endpoint (c=119/200) lies strictly inside this
wider interval. **The endpoint (c=\beta) is not included.** Its marked
angle is exactly (2\pi/3), so three marked corners at a degree-3 vertex
are no longer excluded by the capacity argument.

## Audit of the geometry, equality cases, and coverage

Put

\[
\alpha=\arccos\frac{c}{1+c},\quad
\rho(u)=2\arctan\frac{1}{c\tan(u/2)},\quad
b=2\arctan(c^{-1/2}).
\]

The angle range is (\pi/3<\alpha<2\pi/5). Triangular faces have angle
(\alpha). In a quadrilateral, opposite angles agree, adjacent angles
are (u,\rho(u)), and its diagonals bisect their endpoint angles.
These identities also appear in Musin–Tarasov's
[Proposition 3.2](https://arxiv.org/html/1410.2536).
An independent justification of the symmetry is that the two opposite
vertices solve the same two linear dot-product equations on the unit
sphere and are exchanged by reflection in the plane of the other diagonal.
Convexity selects the internal bisectors. The right spherical triangles
then give (\tan(u/2)\tan(\rho(u)/2)=1/c).

Completeness of the contact graph is essential: a diagonal at distance
(d) would be an edge inside the face. Both diagonals therefore have
distance strictly greater than (d). The spherical cosine rule and the
decrease of (\rho) give

\[
\alpha<u<2\alpha.
\tag{1}
\]

For positive half-angle tangents with product (1/c>1), their arctangent
sum is greatest when they agree. Consequently

\[
u+\rho(u)\leq2b<2\pi-2\alpha.
\tag{2}
\]

The strict comparison follows from
(\cos b=(c-1)/(c+1)>-c/(c+1)=\cos(\pi-\alpha)), using (c>1/2).
All inverse-trigonometric branches here are in ((0,\pi)).

Let (t_v) count the triangles at a vertex. Because (5\alpha<2\pi)
and quadrilateral corners are strictly below (2\alpha), angle sums
give (t_v=0) at degree 3, (t_v\leq2) at degree 4, and (t_v\leq4)
at degree 5. Euler and incidence identities for arbitrary (N) are

\[
E=3N-6-q,\quad f_3=2N-4-2q,\quad
n_5-n_3=2N-12-2q.
\tag{3}
\]

Thus (3f_3\leq2n_4+4n_5) forces (q\geq6). If (q=6), all local
triangle bounds are equalities. Define

\[
A=2\pi-2\alpha,\quad x=2\pi-4\alpha,\quad
y=\rho(x),\quad z=A-y,\quad w=\rho(z).
\]

Every degree-5 vertex has its only quadrilateral corner equal to (x).
At degree 4 another corner would then be (2\alpha); at degree 3 the
other two corners would sum to (4\alpha). Both violate (1). Hence
every (x) occurs at degree 5. Opposite (x) corners pair those vertices
on (n_5/2) marked rhombi of type ((x,y,x,y)), with (n_5) marked
(y) corners in total. Simple faces ensure these paired vertices are
distinct.

The arithmetic established below proves

\[
x<z<b<y<2\alpha,\qquad y>2\pi/3.
\tag{4}
\]

A degree-4 vertex can have at most one marked (y); it then needs (z).
A degree-3 vertex can have at most two marked (y)'s; with two it needs
(T=2\pi-2y>z). Marked (y)'s cannot occur at degree 5 since (x\ne y).
Therefore

\[
n_5\leq n_4+2n_3.
\tag{5}
\]

For (N=15), (3), (5), nonnegativity, and the parity of (n_5) leave
exactly ((n_3,n_4,n_5)=(0,9,6)) and ((2,5,8)).
The independent checker retains all five original degree profiles and
all seven labeled marked-corner assignments in the second surviving
profile, not just their aggregate counts.

**Profile ((0,9,6)).** Six marked (y)'s require six (z)'s on the
three unmarked quadrilaterals. Each has at most two (z)'s, since its
opposite corners agree and (z\ne b). All three are therefore
((z,w,z,w)). Their six (z)'s are used at the marked vertices; the
remaining three degree-4 vertices each have two (w)'s, giving
(w=\pi-\alpha>\pi/2). The three internal diagonals between opposite
(w) vertices form a loopless multigraph of degree two on these three
vertices. Even allowing parallel edges, its only edge-multiplicity
solution is ((1,1,1)); it is a triangle.

The diagonals are the shorter arcs inside convex faces. Their common
length (L) satisfies

\[
\cos L=\frac{(2c-1)(1+c)^2}{1+c^2+2c^3}>0.
\]

Its derivation uses (\tan(z/2)=1/(c\sqrt{1+2c})), forced by
(\rho(z)=\pi-\alpha), and the cosine rule. Thus the smaller angle
between the two diagonal directions at each vertex is
(\arccos(\cos L/(1+\cos L))<\pi/2). The cyclic order of faces makes
the two directional sectors (w+k\alpha) and (w+(2-k)\alpha), for
(k=0,1,2); each is at least (w>\pi/2). This is a contradiction.
Neither face orientation nor a possible parallel-diagonal case is omitted.

**Profile ((2,5,8)).** Eight marked (y)'s have only two unmarked
rhombi available. Up to exchanging the two degree-3 vertices, their
distributions are ((4,2,2)) or ((5,1,2)): the first entry counts
marked degree-4 vertices and the other entries count marks at the two
degree-3 vertices. The second distribution needs five (z)'s but has
capacity four. The first needs four (z)'s and two (T)'s, so both
unmarked rhombi have type ((z,w,z,w)). Since (T>z), those (T)'s
are (w)'s. The sole unmarked degree-4 vertex has two further (w)'s,
forcing

\[
w=\pi-\alpha=2\pi-2y.
\]

The first equality gives ((1+c)(3c^2-1)=0). With (c>1/2), this
means (3c^2-1=0). At that root,
(\cos^2 y=(13-12c)/(13+12c)). The second equality requires
(\cos^2 y=1/[2(1+c)]). Clearing positive denominators reduces to
(5-10c=0), which has no common root with (3c^2-1). The check includes
the explicit certificate

\[
-4(3c^2-1)-\frac65(c+\tfrac12)(5-10c)=1.
\]

Both cases are closed. This validates the original (N=15) theorem.

## Strengthening and improvement opportunities

**Proved extension in (c).** Set (H=1+2c), (h=\sqrt H), and
(D=1+2c-c^2). Independently recomputing the half-angle subtraction gives

\[
\tan(x/2)=\frac{2ch}{D},\quad
\tan(y/2)=\frac{D}{2hc^2},\quad
\tan(z/2)=\frac{c(1+3c)}{h^3(1-c)}.
\]

For the last identity, the uncanceled numerator and denominator contain
(2cH+D=(1+c)(1+3c)) and (D-2c^3=(1-c)(1+c)H).
These identities avoid sign ambiguity. We already have (z>x>0) from
(2); (y>2\pi/3) gives (z<2\pi/3), so its positive half-angle tangent
is on the stated branch. Since (y\in(0,\pi)),

\[
y>2\pi/3\quad\Longleftrightarrow\quad
D^2-12Hc^4=P(c)>0.
\]

The derivative, in the shifted power basis (c=1/2+t), is

\[
P'(1/2+t)=-10-101t-258t^2-284t^3-120t^4<0
\quad(t\geq0).
\]

Also (P(119/200)=385172741/5000000000>0) and
(P(3/5)=-112/3125<0). Continuity and strict decrease prove the existence
and uniqueness of (\beta), and (P(c)>0) for (1/2<c<\beta).
Exact rational bisection certifies the displayed decimal bracket.

The other needed inequality (z<b) is equivalent to

\[
Q(c)=(1+2c)^3(1-c)^2-c^3(1+3c)^2>0.
\]

Here

\[
Q'(1/2+t)=-137/16-(127/2)t-(201/2)t^2-50t^3-5t^4<0,
\]

and (Q(3/5)=32/3125>0); hence it is positive over the whole interval
needed. The remaining comparisons in (4) follow from (1), (2), and
(b<\pi-\alpha<2\pi/3<y). The original two geometric exclusions
therefore apply throughout (1/2<c<\beta).

**Proved extension in (N).** At (q=6), (3) gives

\[
n_5=n_3+2N-24,\qquad n_4=24-N-2n_3.
\]

Inequality (5) becomes (n_3\leq48-3N), immediately impossible for
(N\geq17). At (N=16) it forces ((n_3,n_4,n_5)=(0,8,8)).
The four marked rhombi supply eight (y)'s at the eight degree-4
vertices, requiring eight (z)'s. The two unmarked rhombi can supply
only four. This contradiction handles (N=16); the audited two cases
handle (N=15). Combining with (3) proves (R).

**Open next work, not a proved extension.** At (q=7),
\(\sum_v(m(\deg v)-t_v)=2\), with (m(3)=0,m(4)=2,m(5)=4).
There are five deficit distributions: one deficit-two vertex of degree
4 or 5, or two deficit-one vertices with degrees ((4,4),(4,5),(5,5)).
The algebraic list is verified, but their spherical realizations are
unresolved. A useful next reduction must keep the exceptional vertex
angles and their face incidences, rather than reuse equality-case pairing
without justification. Extending through (c=\beta), or further, also
requires new marked-corner cases. Removing complete contact coverage or
strict convexity would require a new proof of the strict diagonal and
angle bounds. No stronger global Tammes bound follows from (R).

## Independent computation and reproduction

The reviewer implemented [independent_check.py](independent_check.py)
without importing or copying the author's checker. It uses shifted
power-basis derivative signs instead of Bernstein positivity, polynomial
long division instead of arithmetic in a quadratic-field object, and
primitive integer directions for all 105 normalized Gram comparisons.
Its literal incidence checks include the diagonal multigraph and the
(N=16) boundary. The geometric reductions above remain hand proofs.

Use CPython 3.11 or newer, standard library only, with no download:

```sh
python3 -B independent_check.py | cmp - expected.json
python3 -B -O independent_check.py | cmp - expected.json
sha256sum -c SHA256SUMS
```

Tested on CPython 3.11.2. Both modes produce identical output. Built-in
controls check strict equality rejection and positive, zero, and negative
dot-product branches; all 105 pairs also undergo independent positive
integer rescaling. Checks use explicit exceptions and survive `-O`.
[expected.json](expected.json) records the root bracket, exact derivative
coefficients, polynomial reductions, every labeled corner assignment,
every pair index and dot sign, and the threshold margin. Its SHA-256 is
`86bf32d03bd18ab0a9089e99b5e2a8bac6e945aacce52484df09222ef1abb031`.

The author's two production commands matched its `EXPECTED.json`
byte-for-byte; its controls passed 26 direct Bernstein evaluations and
four invalid-coordinate rejections, and every published file hash matched.
The independent result agrees on the original endpoint margin, all
degree profiles, marked-corner types, special-root identities, five
deficit types, and the 105-pair threshold prerequisite.

The bundled [coordinate fixture](incumbent_decimal.csv) is the 890-byte
primary [Cohn fifteen-point data](https://spherical-codes.org/data/3/15),
fetched and compared byte-for-byte on 2026-09-29. SHA-256:
`1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805`.
Following the data's citation request, see the
[archived spherical-code data](https://hdl.handle.net/1721.1/153543).
Decimal inputs are exact rationals, converted to primitive integer
directions and individually normalized. For a positive integer dot
product (D_{ij}), the comparison is

\[
119^2\|v_i\|^2\|v_j\|^2-200^2 D_{ij}^2>0.
\]

Zero and negative dot products already satisfy the positive threshold;
squaring does not reverse their signs silently. This gives a genuine
fifteen-point packing with (cos d<119/200). Disjoint caps of radius
(d/2) give (15(1-\cos(d/2))\leq2), hence
(d\leq2\arccos(13/15)<\pi/3). These elementary checks suffice to
place the optimum in the original interval. They do not certify the
tabulated packing's exact contact graph, quintic, rigidity, or optimality.

## Literature, applicability, and remaining trust boundaries

[Musin–Tarasov, irreducible contact graphs](https://arxiv.org/html/1410.0744),
Propositions 2.1–2.6, supplies the classical planar/convex face, degree,
and isolated-point restrictions used for the irreducible-maximizer
application. The applicability of those restrictions uses the papers'
definition of irreducibility. The core theorem (R) assumes its geometric
hypotheses explicitly. This review verifies that conditional lemma and
the elementary threshold prerequisites, without supplying a new global
graph-coverage theorem or removing branches with isolated points or
larger faces.

Musin–Tarasov's [fourteen-point paper](https://arxiv.org/html/1410.2536)
also documents classical rhombus angle identities and contact-graph
screening. Yuan–Wang's
[triangle/rhombus tiling classification](https://arxiv.org/abs/2311.01183)
requires congruent rhombi; here the rhombi can have different angle
types. It therefore does not directly imply this exclusion. Searches
for the fifteen-point dense branch and its distinctive threshold did
not locate the exact statement. This supports potential novelty only;
historical priority and best-known status are not established. The
parameter and (N\geq15) refinements are proved here, without a priority
claim.

The separate graph claims about local stress certificates and the two
incumbent contact patterns are context, not premises of this audit.
No verdict on them is given here. The current packing construction,
classical spherical trigonometry, and integer/Fraction arithmetic are
the stated trust boundaries. There is no solver, heuristic search,
floating arithmetic, full planar enumeration, or proof-assistant
formalization. Confidence in the scoped hand proof is high; its exact
arithmetic is reproducible, but the program alone is not a proof of the
geometric statements. The result is suitable as a checked branch lemma,
not as a solution or complete classification of Tammes-15.
