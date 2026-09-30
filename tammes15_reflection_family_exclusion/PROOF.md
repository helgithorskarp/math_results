# Reflection-gluing exclusion for Tammes-15

**six-tammes-2 — researcher — 2026-09-30.** Complete author-audited hand
reduction with a reproducible exact finite certificate. Independent review
is pending. No global numerical bound or optimality claim is made.

## Statement and graph family

Write

\[
F(t)=13t^5-t^4+6t^3+2t^2-3t-1,
\]

and let \(\tau\) be its unique root in \((1/2,3/5)\). It is the known
incumbent cosine, with the exact bracket

```
0.59260590292507377809642492233275 < tau
    < 0.59260590292507377809642492233276.
```

Define a graph family on thirteen labels as follows.

* A is a combinatorial triangulation of an octagon on labels 0 through 7:
  its eight boundary edges and five pairwise noncrossing diagonals are
  prescribed contacts. This gives thirteen edges and six triangles.
* B has labels 8 through 12 and the seven prescribed edges
  `(8,9) (8,10) (9,10) (9,11) (10,11) (8,12) (9,12)`.
  It is a triangulated pentagon: an anchor triangle with two ears 11,12.
* Add contacts from 11 to an A pair `(i,j)`, and from 12 to an A pair
  `(k,l)`. Each pair has at least one common neighbor using **prescribed
  A edges**. The pairs may share vertices. All thirteen labels are distinct.

Combinatorial noncrossing describes the octagon triangulation, not an
assumed geometric embedding of the packing. All cyclic orders, label
injections, additional contacts and arbitrary other two points are allowed.
The B form represents every triangulated pentagon with its two ears.

**Theorem.** No packing of fifteen distinct points on the unit sphere in
\(\mathbb R^3\), with minimum geodesic separation strictly larger than
the incumbent's, contains a member of this family in its contact graph.

Equivalently, the thirteen prescribed labels of such a packing cannot
satisfy these twenty-four contacts at its minimum distance. This is a
conditional family exclusion; no claim forces every better packing into
this family. It includes the cyclic incumbent core after vertices 3,14 are
removed, with its A boundary order `(0,6,11,13,9,5,12,7)` in the preceding
incumbent labeling. Its arbitrary-Gram classification is a different claim.

## Parameter range and finite graph cover

Let \(d\) be the minimum separation of a hypothetical better packing and
\(t=\cos d\). Strict improvement gives \(t<\tau<3/5\). Fifteen
disjoint open caps of radius \(d/2\) give

\[
15(1-\cos(d/2))\le2,\qquad t\ge113/225>1/2.
\]

Every contact vertex has at most five neighbors. Indeed write its contact
neighbors as \(q=t p+\sqrt{1-t^2}u\), with u on the tangent unit circle.
Packing inequalities imply pairwise tangent angular separation at least
\(\arccos(t/(1+t))>\pi/3\). Six cyclic gaps cannot sum to \(2\pi\).
This applies to all actual contacts, hence also the prescribed subgraph.

A common-neighbor pair of distinct unit points has at most two unit common
neighbors with positive contact cosine t. The pair cannot be antipodal.
If its prescribed A graph already gives two old neighbors, neither B ear
can be a further distinct neighbor. Thus any realizable case has exactly
one old A neighbor for each attached pair. The two attached pairs must
differ: otherwise both B ears are forced to the same second common neighbor.

There are 132 labeled octagon triangulations. The checker verifies the
full sets, using two constructions: a Catalan triangle recursion, and all
\(\binom{20}{5}=15504\) five-diagonal subsets retained when noncrossing.
It compares edge masks, rather than aggregate counts. Maximum degree five
retains 84 triangulations in eight disjoint dihedral orbits. For each
representative list all A pairs with exactly one old common neighbor, then
all unordered pairs of these choices for which adding the cross edges
keeps A degrees at most five. There are 355 cases.

Octagon dihedral relabeling preserves all hypotheses. Interchanging B
anchors 8 and 10 interchanges the two ears, so using unordered gluing
choices loses no orientation or realization. The eight orbit representatives
are chosen deterministically by `family.py`; case numbers refer to its
lexicographically ordered gluing choices. Every survivor also has its own
ear-removal and reconstruction audit. These operations cover this specified
schema, not all contact graphs.

## Forced coordinates and scalar residual

Let \(H=(1-t)I+tJ\). It is positive definite on our interval. Three
equilateral anchors form a basis P with \(P^TP=H\). Given an old
equilateral triangle \((i,j,o)\), a distinct common neighbor of i,j is
forced to be

\[
p_n=\frac{2t}{1+t}(p_i+p_j)-p_o. \tag{1}
\]

An octagon triangulation can be reduced to one triangle by removing ears.
At each removal its base becomes a boundary edge with one old triangle
on the remaining side. Reverse this process using (1). The checker verifies
the old triangle and every reconstructed edge. Thus every distinct A
realization has the resulting exact coefficient vectors \(p_i=Pa_i\);
no symmetry, proximity, planarity or generic-rank assumption is used.
The unit and prescribed contact identities are checked in \(\mathbb Q(t)\).

For B use the analogous anchor basis with coefficients

\[
b_8=e_0,\ b_9=e_1,\ b_{10}=e_2,\qquad
b_{11}=(-1,r,r),\ b_{12}=(r,r,-1),\quad r=\frac{2t}{1+t}.
\]

Their required inner product is

\[
\kappa=b_{11}^THb_{12}=\frac{t(9t^2-2t-3)}{(1+t)^2},
\qquad -1<\kappa<1. \tag{2}
\]

For an A pair `(i,j)` with old neighbor o set \(w=a_i^THa_j\).
Its new B neighbor, distinct from o, is forced to have coefficient

\[
v=\frac{2t}{1+w}(a_i+a_j)-a_o. \tag{3}
\]

There is no lost antipodal or tangent case: Cauchy applied to the old
neighbor gives \(1+w\ge2t^2>0\). If the old neighbor lies in the pair's
plane, it is the only unit solution and a distinct new neighbor is
impossible. Formula (3) still gives that old point, so such cases are
retained and rejected by packing inequalities. All actual divisions are
by \(1+t,1-t,1+2t,1+w\), or \(1-\kappa^2\), which are nonzero;
the checker additionally certifies the symbolic signs of the last two.

Let u,v be the two forced ear coefficients. The necessary scalar condition
is

\[
R(t)=u^THv-\kappa=0. \tag{4}
\]

For all 355 cases the generator derives R independently in SymPy's
rational-function field and compares it exactly with the custom kernel.
The standard-library checker reconstructs R and uses signed exact Sturm
sequences. Roots at the endpoints 1/2,3/5 are explicitly removed before
open-interval counting. Multiple roots are counted distinctly.

The resulting complete partition is:

| Cases | Exact conclusion |
|---:|---|
| 322 | Nonzero residual with no root in `(1/2,3/5)` |
| 7 | Residual identically zero; both Gram branches fail packing uniformly |
| 2 | Only relevant root exceeds tau |
| 1 | Only relevant root is tau, so strict improvement is impossible |
| 23 | One root below tau; check both orientations |

There are nine distinct active root polynomials. The certificate lists
their exact rational brackets and all 26 nonzero cases using them. The
checker verifies one root in the full interval and in each bracket,
opposite endpoint signs, the exact residual/factor gcd, and no omitted
cases. Factorization by the optional CAS is not trusted by the checker.

## Completeness of both B orientations

At a residual root the forced ears have the same Gram matrix as B's ears,
namely \(\begin{pmatrix}1&\kappa\\\kappa&1\end{pmatrix}\), which is
positive definite. Fix the A anchor frame. There are precisely two
H-isometries placing the B anchor frame with these two ears fixed; they
differ by reflection in the ear plane. This includes both physical
handedness choices.

Explicitly put \(\beta_{1j}=b_j^THb_{11}\),
\(\beta_{2j}=b_j^THb_{12}\), and

\[
\lambda_j=\frac{\det(H)\det(b_{11},b_{12},b_j)}{1-\kappa^2}.
\]

The two B coefficients are

\[
x_j^\epsilon=
\frac{\beta_{1j}-\kappa\beta_{2j}}{1-\kappa^2}u+
\frac{\beta_{2j}-\kappa\beta_{1j}}{1-\kappa^2}v+
\epsilon\lambda_j H^{-1}(u\mathbin\times v),\qquad \epsilon=\pm1. \tag{5}
\]

The normal's squared H norm is \((1-\kappa^2)/\det(H)\); projection
of b_j onto its B normal gives the displayed lambda. Under an H-isometry
the metric cross normal transforms with its determinant sign. This proves
(5) gives every relative placement. The checker independently checks the
B anchor Gram identities and the two fixed ears at every relevant root.

The fourteen branches of the seven zero cases each have an unprescribed
pair with dot product strictly greater than t on the full open interval.
Their exact rational witnesses have numerator and denominator Bernstein
coefficients of one sign, allowing zero endpoint coefficients when strict
positivity holds in the interior. The forty rejected branches of the
twenty-three lower-root cases have exact positive witnesses in quotient
arithmetic and certified rational root intervals.

The other six branches are distinct thirteen-point packings, checked with
all norms, all 24 prescribed contacts and all remaining pair inequalities.
The coefficients are derived, rather than imported as a coordinate table.
Their two cosine values are the positive root of \(3t^2-1\), and the
unique interval root of

\[
119t^5+95t^4-14t^3-30t^2-9t-1.
\]

Being valid thirteen-point packings does not give fifteen points. The next
step excludes every two-point extension exactly.

## Exact extension certificates

For each remaining packing, an additional point y=Pc must satisfy

\[
a_i^THc\le t\quad(0\le i\le12),\qquad c^THc=1.
\]

Let D be the thirteen-halfspace polytope defined by the inequalities.
Four core vectors have a strictly positive convex combination equal to
zero, with rank three; their labels are in the certificate and their exact
weights are regenerated and checked. The recession cone of D is therefore
zero: the four nonpositive dot constraints and their positive relation
force all four dots to vanish, then rank three forces the recession vector
to vanish. D is bounded and contains zero in its interior.

Every vertex of a bounded full-dimensional three-dimensional polytope has
three independent active constraints. Enumerate all \(\binom{13}{3}=286\)
triples, solve exactly, and check every remaining inequality. Singular
triples are skipped only after their determinant is exactly zero; vertices
with four or more active facets remain included through independent
triples. Deduplication uses exact quotient coefficients. Thus no generic
facet-position assumption is made. The squared H norm is convex, so its
maximum over a polytope occurs at a vertex.

| Patch, case, sign | Contact count | Extension proof | Vertices |
|---|---:|---|---:|
| 0,7,-1 | 24 | All D vertices have squared norm `<9/10` | 22 |
| 0,24,+1 | 26 | Small admissible cap | 24 after cut |
| 4,5,+1 | 26 | Small admissible cap | 24 after cut |
| 4,7,-1 | 25 | Exactly one unit D vertex; all others inside | 22 |
| 4,12,-1 | 25 | Exactly one unit D vertex; all others inside | 22 |
| 6,7,+1 | 26 | Small admissible cap | 24 after cut |

For the first row D contains no unit point, so even one additional point
is impossible. In each of the two unit-vertex rows convexity shows D is
inside the closed unit ball. Any convex combination using an interior
vertex has norm strictly below one. The sole admissible unit point is
therefore that unique unit vertex: at most one point can be added.

For the other three rows let q be the exact vertex of D given by active
triples `(2,3,4)`, `(1,2,3)` and `(0,5,6)`, respectively. Direct quotient
identities give

\[
q^THq=1+2t.
\]

Cut D by \(q^THc\le4/3\). The cut polytope remains bounded and contains
zero in its interior. Enumerate every \(\binom{14}{3}=364\) active triple.
All 24 distinct vertices have squared norm strictly below \(91/100\).
Consequently every admissible additional unit point satisfies
\(q^THc>4/3\). At \(t=1/\sqrt3\) the exact diameter guard is

\[
2(4/3)^2-(1+t)(1+2t)=\frac{17-27t}{9}>0. \tag{6}
\]

After normalizing q, this places every additional unit point in a cap of
angular radius strictly less than \(d/2\). Any two such points have
separation strictly less than d. At most one point can be added. This
argument uses a checked empty cut polytope, rather than an approximate
covering radius or an unvalidated search for additional points.

All six thirteen-point branches admit at most one additional separated
point. A fifteen-point extension needs two. Together with the complete
355-case partition this proves the stated family exclusion.

## Computation, trust and prior work

The directory is self-contained. `check.py` uses only Python integer and
Fraction arithmetic. It regenerates the entire graph cover, symbolic
residuals, signed Sturm counts, both coordinate branches and every extension
polytope. `certificate.json` supplies only nine root brackets, case/root
assignments, pair witnesses and six tetrahedron/cap seeds. It supplies no
unchecked coordinate fixture, solver verdict, enumeration dump or hidden
external input. `generate_certificate.py` uses SymPy1.14.0 with an
independent rational-function representation and exact root isolation.
The hand reduction and ordinary exact software execution remain
unformalized trust boundaries. Independent mathematical review is pending.

The [Cohn table](https://cohn.mit.edu/spherical-codes/) and
[current coordinate archive](https://spherical-codes.org/data/3/15) supply
the known incumbent and quintic; its fifteen-point entry has no optimality
asterisk. [Musin–Tarasov](https://arxiv.org/abs/1410.2536) solves fourteen
points. Buddenhagen–Kottwitz,
[*Multiplicity and Symmetry Breaking in (Conjectured) Densest Packings of
Congruent Circles on a Sphere*](https://web.archive.org/web/20210507001707/http://www.buddenbooks.com/jb/pack/sphere/toggles7.pdf),
Section4 pp7–11, gives the known exact construction and quintic, with an
eighteen-point antecedent. Kottwitz's earlier paper is
[Acta Crystallographica A47 (1991)](https://doi.org/10.1107/S0108767390011370).
[Hars](https://www.hars.us/Papers/Numerical_Tammes.pdf), Section10.15,
computes separation under a full displayed contact graph. Targeted primary
searches found no identical finite-family exclusion; no historical-priority
claim or new packing record is made.

This develops the packing consequence of the preceding
[cyclic core](../tammes15_contact_pattern_obstruction/CYCLIC_CORE.md),
source249f243e7f760356a8a52f853bc0808d657914b0, graph
`bafkreieiqtjocindaj2xyalzxkwxqtofs3tevz26aot3copveubprk4pd4`,h7270.
It neither reproduces nor generalizes that core's arbitrary two-Gram
classification. The
[asymmetric core review](../tammes15_contact_core_review1/README.md),
by six-reviewer-1, source0abefdfef65b4e4b5c084d7ab6070e7478c39221,
graph`bafkreidxvqlsmk3qfmfnebcvcil4dpx4lcsjq7sycsbzha6us346vkq36e`,h7288,
confirms the different asymmetric motif and proves all 24 edges locally
essential. It does not review the present family.

Complementary six-tammes-1's
[one-five geometry](../tammes15_eight_quad_reduction/ONE_FIVE.md),
source8d1d15f72e8dbb2e42dabb0f805562aee7203c2d, graph
`bafkreiccuvl35qft57dmihk74ptzusddogzysnrqsmjnih3zkw46x4xndi`,h7300,
leaves 23 necessary profiles and 16 auxiliary types in its explicitly
complete connected convex triangle/quadrilateral branch. Its conditions
are not assumptions of this theorem, and it is context rather than a
premise. A future complete geometric or graph reduction detecting the
present motifs remains necessary for global coverage.
