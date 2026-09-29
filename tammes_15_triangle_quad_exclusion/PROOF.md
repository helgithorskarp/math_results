# A dense triangle–quadrilateral branch is impossible for fifteen points

Author/role: **six-tammes-1, researcher**. Date: 2026-09-29.
Status: complete hand proof with auxiliary exact arithmetic checks;
not a formal proof or an independently reviewed result.

## Statement and scope

Let `X` consist of exactly fifteen distinct points on the unit sphere.
Let `d` be its minimum geodesic separation, and put `c = cos(d)`.
Suppose

\[
\tfrac12<c\leq\tfrac{119}{200}.
\tag{1}
\]

Join every pair at distance `d` by its shorter great-circle arc. Suppose
this contact graph is connected, all its vertices have degrees 3, 4, or
5, and it gives a cell decomposition of the sphere into strictly convex
triangles and quadrilaterals. Here a strictly convex face is a simple
geodesic polygon contained in an open hemisphere with all angles below
`pi`. Let `q` be its number of quadrilateral faces.

**Lemma.** Then

\[
q\geq7,\qquad e\leq32,\qquad f_3\leq12.
\tag{2}
\]

Equivalently, the branch with only triangular and quadrilateral faces
and at least 33 contacts is excluded throughout
`arccos(119/200) <= d < pi/3`. This is a necessary-condition reduction,
not an improved upper bound on the global Tammes separation.

For the application to an irreducible Tammes maximizer, use the classical
contact-graph structure described by Musin–Tarasov [1,2]: nonisolated
degrees are 3–5, faces are convex, and isolated vertices can occur only
in faces with at least six sides. Thus a maximizer in the branch with
only triangles and quadrilaterals has no isolated vertices and satisfies
the graph hypotheses. The geometric lemma itself does not require a
maximality or irreducibility assumption beyond the explicit hypotheses.

The exact rational check of the current fifteen-point coordinate table
in `check.py` supplies a packing with `cos(d) <= 119/200`. The cap-area
bound gives `d_15 <= 2 arccos(13/15) < pi/3`, because
`13/15 > sqrt(3)/2` (square both positive sides). Hence (1) covers the
global optimum. The coordinate check supplies only this threshold
prerequisite; it does not assert that the tabulated code is optimal.

## 1. Rhombus identities and strict bounds

Define

\[
\alpha=\arccos\frac{c}{1+c},\qquad
\rho(u)=2\arctan\frac{1}{c\tan(u/2)},\qquad
b=2\arctan\frac1{\sqrt c}.
\tag{3}
\]

Every triangular face has angles `alpha`. Every quadrilateral has equal
opposite angles and adjacent angles `u, rho(u)`, with

\[
\cot(u/2)\cot(\rho(u)/2)=c.
\tag{4}
\]

Both diagonals bisect their endpoint angles. These elementary spherical
rhombus facts are also in [1, Proposition 3.2]. To see the symmetry,
label a quadrilateral `P,Q,R,S`. The unit vectors `Q,S` both satisfy
`P dot Q = R dot Q = P dot S = R dot S = c`; the intersection of these
two planes with the unit sphere has precisely these two points.
Reflection in the plane spanned by `P,R` exchanges `Q,S`. The analogous
reflection exchanges `P,R`. Convexity makes the diagonals internal angle
bisectors. Applying spherical trigonometry to the resulting right
triangles gives (4).

Neither diagonal is a contact edge: such an edge would subdivide the
face. Consequently both diagonal lengths strictly exceed `d`. The law
of cosines at a quadrilateral corner gives

\[
c^2+(1-c^2)\cos u<c,
\]

so `u > alpha`. Since `rho` decreases strictly and
`rho(alpha) = 2 alpha`, the adjacent angle exceeding `alpha` gives

\[
\alpha<u<2\alpha
\quad\hbox{at every quadrilateral corner.}
\tag{5}
\]

We will also need

\[
u+\rho(u)\leq2b<2\pi-2\alpha.
\tag{6}
\]

For the first inequality set `p = tan(u/2)` and
`r = tan(rho(u)/2)`, so `pr = 1/c > 1`. The sum of their arctangents
lies in `(pi/2,pi)` and has tangent `(p+r)/(1-pr)`. The inequality
`p+r >= 2/sqrt(c)` shows that the sum is largest when `p=r`, proving
`u+rho(u) <= 2b`. For the second inequality,

\[
\cos b=\frac{c-1}{c+1}>
-\frac{c}{c+1}=\cos(\pi-\alpha)
\]

is exactly `c > 1/2`.

Throughout (1), `pi/3 < alpha < 2pi/5`. Indeed,
`cos(alpha) > 1/3 > cos(2pi/5) = (sqrt(5)-1)/4`.
The latter comparison follows from `sqrt(5) < 7/3`.
In particular,

\[
5\alpha<2\pi.
\tag{7}
\]

## 2. The equality case in the triangle count

Write `n_j` for the number of vertices of degree `j`, and `t_v` for
the number of triangular faces at `v`. Equations (5) and (7) give

\[
t_v=0\ (\deg v=3),\quad
t_v\leq2\ (\deg v=4),\quad
t_v\leq4\ (\deg v=5).
\tag{8}
\]

For example, one triangle at degree 3 gives a total angle below
`alpha+2(2alpha)=5alpha<2pi`. Three triangles at degree 4 give a total
below `3alpha+2alpha`, and five triangles at degree 5 give `5alpha`.
Additional triangles only decrease these bounds.

Euler's identity and face incidence give

\[
e=39-q,\quad f_3=26-2q,\quad
n_5-n_3=18-2q.
\tag{9}
\]

Summing (8) yields

\[
78-6q=3f_3\leq2n_4+4n_5=66-4q,
\]

so `q >= 6`. Suppose for contradiction that `q=6`. Equality forces
every degree-4 vertex to have exactly two triangles and every degree-5
vertex exactly four. Degree-3 vertices have three quadrilaterals.
In this case

\[
n_5=n_3+6,\qquad n_4=9-2n_3.
\tag{10}
\]

Put

\[
A=2\pi-2\alpha,\quad x=2\pi-4\alpha,\quad
y=\rho(x),\quad z=A-y,\quad w=\rho(z).
\tag{11}
\]

The sole quadrilateral corner at any degree-5 vertex equals `x`.
A degree-4 vertex cannot have a corner `x`, since its other
quadrilateral corner would have to be `A-x=2alpha`, contradicting (5).
A degree-3 vertex cannot have a corner `x`, since its other two corners
would have to sum to `4alpha`, again contradicting (5).

Thus every occurrence of `x` is at degree 5. Opposite corners are equal,
so degree-5 vertices occur in pairs on `n_5/2` distinct quadrilaterals
with angles `(x,y,x,y)`. Call these the **marked quadrilaterals** and
mark their `y` corners. Each degree-5 vertex supplies one marked `y`
corner elsewhere. The two angles are distinct by the bounds below.
The remaining quadrilaterals contain no `x` corner.

## 3. Exact inequalities used for corner propagation

In the interval (1),

\[
x<z<b<y<2\alpha,\qquad y>2\pi/3.
\tag{12}
\]

Here are exact verifications, avoiding decimal angle estimates.

Set `h = sqrt(1+2c)` and `D = 1+2c-c^2`. Half-angle identities give

\[
\tan(x/2)=\frac{2ch}{D},\quad
\tan(y/2)=\frac{D}{2hc^2},\quad
\tan(z/2)=\frac{c(1+3c)}{h^3(1-c)},\quad
\tan(w/2)=\frac{h^3(1-c)}{c^2(1+3c)}.
\tag{13}
\]

The formula for `z` follows from the tangent subtraction identity for
`A-y`; its displayed value is positive. More directly, (6) gives
`z=A-y>x>0`, and `A<4pi/3` together with the bound on `y` below gives
`z<2pi/3`, so its half-angle is on the branch used in (13).

The function `y(c)` decreases strictly with `c`: `alpha(c)` decreases,
`x(c)` increases, and `rho(u,c)` decreases in each argument. At
`c=119/200` the exact comparison is

\[
\tan^2(y/2)-3=
\frac{3081381928}{43916928699}>0.
\tag{14}
\]

It follows that `y>2pi/3`. Also `x<2pi/3`, so `x!=y`.
Equation (7) gives `x>alpha`; hence `y=rho(x)<2alpha`.
Since `b<pi-alpha<2pi/3`, we have `b<y`.

The inequality `z<b` is equivalent, by positive half-angle tangents,
to

\[
Q(c)=(1+2c)^3(1-c)^2-c^3(1+3c)^2>0.
\tag{15}
\]

Expansion gives

\[
Q(c)=1+4c+c^2-11c^3-10c^4-c^5.
\]

On `[1/2,3/5]`, its derivative is negative, since
`4+2c <= 26/5 < 33/4 <= 33c^2` and the other terms in
`Q'(c)=4+2c-33c^2-40c^3-5c^4` are negative.
Therefore `Q(c) >= Q(3/5)=32/3125>0`. This proves (12).

An occurrence of `y` at degree 4 requires a second quadrilateral corner
`z`. An occurrence of two `y` corners at degree 3 requires its third
corner to be

\[
T=2\pi-2y>z,
\quad\hbox{because }T-z=2\alpha-y>0.
\tag{16}
\]

There is at most one marked `y` corner per degree-4 vertex, since
`2y>4pi/3>A`. There are at most two per degree-3 vertex, since
`3y>2pi`. Thus

\[
n_5\leq n_4+2n_3.
\tag{17}
\]

By (10), (17) gives `n_3<=3`; pairing the `x` corners makes `n_5`
even, so `n_3` is even. The only possible degree profiles are

\[
(n_3,n_4,n_5)=(0,9,6)\quad\hbox{or}\quad(2,5,8).
\tag{18}
\]

## 4. Excluding the profile `(0,9,6)`

There are three marked `(x,y,x,y)` quadrilaterals and three remaining
quadrilaterals. Their six marked `y` corners occur at six distinct
degree-4 vertices, requiring six `z` corners.

The marked quadrilaterals contain no `z`. Each remaining quadrilateral
contains at most two `z` corners: opposite corners agree, and all four
corners could equal `z` only if `z=b`, which (12) excludes. Hence all
three remaining quadrilaterals have angles `(z,w,z,w)`.

The six `z` corners have all been used with the marked `y` corners.
At the three remaining degree-4 vertices the quadrilateral corners
are therefore both `w`, giving

\[
w=A/2=\pi-\alpha>\pi/2.
\tag{19}
\]

The three diagonals joining opposite `w` corners join exactly these
three vertices. Each vertex is incident with two diagonals; a diagonal
cannot be a loop because its face is simple. A loopless 2-regular
multigraph on three vertices is a triangle. Thus the diagonals give
an equilateral spherical triangle. Their common length `L` satisfies

\[
\cos L=c^2+(1-c^2)\cos z
=\frac{(2c-1)(1+c)^2}{1+c^2+2c^3}>0.
\tag{20}
\]

For (20), use `rho(z)=pi-alpha`, so
`tan(z/2)=1/(c sqrt(1+2c))`, and then the law of cosines.
Thus `L<pi/2`. At each vertex of this equilateral triangle its smaller
angle is

\[
\eta=\arccos\frac{\cos L}{1+\cos L}<\pi/2.
\tag{21}
\]

But the quadrilateral diagonals bisect the two `w` corners there.
Between them in either direction lie their two half-corners and
`k` triangular corners, where `k=0,1,2`. The two directional angles
are `w+k alpha` and `w+(2-k)alpha`; both are at least `w>pi/2`.
Their smaller angle therefore contradicts (21). This excludes the
first profile without enumerating any contact graph.

## 5. Excluding the profile `(2,5,8)`

There are four marked quadrilaterals and two remaining quadrilaterals,
with eight marked `y` corners. The capacity bounds in (17) leave only
two distributions, up to exchanging the two degree-3 vertices:

1. Four degree-4 vertices have one marked `y` each, and both degree-3
   vertices have two marked `y` corners each.
2. All five degree-4 vertices have one marked `y` each, and the two
   degree-3 vertices have respectively one and two marked `y` corners.

Distribution 2 requires five `z` corners in the two remaining
quadrilaterals, whose capacity is at most four by `z<b`; it is impossible.

Distribution 1 requires four `z` corners and two `T` corners from (16).
Both remaining quadrilaterals must consequently be `(z,w,z,w)`.
Because `T>z`, the two `T` corners must equal `w`. The only degree-4
vertex without a marked `y` corner has two remaining `w` corners.
Hence

\[
w=\pi-\alpha=2\pi-2y.
\tag{22}
\]

By (13), the first equality in (22) gives

\[
\frac{h^3(1-c)}{c^2(1+3c)}=h,
\]

so

\[
(1+c)(3c^2-1)=0,
\qquad c^2=1/3.
\tag{23}
\]

Using `c^2=1/3` in (13) gives `tan^2(y/2)=6c`, and thus

\[
\cos^2 y=\frac{13-12c}{13+12c}.
\tag{24}
\]

On the other hand (22) gives `y=(pi+alpha)/2`, so

\[
\cos^2y=\frac{1-\cos\alpha}{2}=\frac1{2(1+c)}.
\tag{25}
\]

Equating (24) and (25), clearing positive denominators, and using
`c^2=1/3` gives `5-10c=0`. This forces `c=1/2`, contradicting (23).
The second profile is excluded, completing the proof of (2).

## 6. What remains and a finite next reduction

This argument excludes `q<=6` in the triangle–quadrilateral branch.
It does **not** exclude `q>=7`, pentagonal or hexagonal faces,
rattlers, or a different graph with better separation. The actual
numerical contact pattern of the tabulated fifteen-point candidate includes
pentagonal faces, so this branch does not encompass that candidate. This
numerical scope comparison is not used in the proof.

The same triangle count gives an exact deficit identity throughout
this branch:

\[
\sum_v \bigl(m(\deg v)-t_v\bigr)=2q-12,
\quad m(3)=0,\ m(4)=2,\ m(5)=4.
\tag{26}
\]

At `q=7`, only one vertex with deficit two or two vertices with deficit
one can occur. This supplies a concrete next frontier: retain the
five ways to distribute those deficits between degree-4 and degree-5
vertices, then apply the marked-corner and diagonal arguments with
the exceptional vertices retained. No `q=7` case is claimed excluded.

## Sources, novelty boundary, and verification boundary

1. O. R. Musin and A. S. Tarasov, *The Tammes problem for N=14*,
   arXiv:1410.2536v2, particularly Propositions 3.1–3.2 and Section 3.
   <https://arxiv.org/abs/1410.2536>.
2. O. R. Musin and A. S. Tarasov, *Extreme problems of circle packings
   on a sphere and irreducible contact graphs*, arXiv:1410.0744,
   Propositions 2.1–2.6. <https://arxiv.org/abs/1410.0744>.
3. Henry Cohn, *Table of spherical codes*, the fifteen-point row and
   coordinate file, accessed 2026-09-29.
   <https://spherical-codes.org/>;
   <https://spherical-codes.org/data/3/15>.
   The table requests citation of its archived data:
   <https://hdl.handle.net/1721.1/153543>.
4. C. Bachoc and F. Vallentin, *New upper bounds for kissing numbers
   from semidefinite programming*, JAMS 21 (2008), 909–924, Table 5.3.
   <https://doi.org/10.1090/S0894-0347-07-00589-9>.
   Its approximately 55.03-degree N=15 bound is prior context; it is
   not needed by this proof, and no numerical SDP certificate is
   silently imported here.

The basic contact-graph and rhombus facts are classical. The contribution
is the explicit fifteen-point six-quadrilateral exclusion and its
resumable deficit reduction. Targeted searches and the checked primary
papers did not locate this exact lemma; no historical-priority claim
is made. General spherical tiling classifications that require all
rhombi to be congruent do not supply the present hypotheses.

The handwritten geometric proof is the evidence for the lemma.
`check.py` checks endpoint inequalities, polynomial identities, the
complete degree/corner distributions used above, and the small
rational coordinate prerequisite. Those checks are not a formalization
of convexity, spherical trigonometry, or the full proof. There is no
solver, floating-point step, omitted enumeration, large certificate,
or external download in reproduction. Only the standard Python
interpreter and the mathematical hand proof are trusted.
