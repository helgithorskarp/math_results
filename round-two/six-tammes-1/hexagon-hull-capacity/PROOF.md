# Nine robust six-boundary hull-capacity certificates

Actual author **six-tammes-1**, role **researcher**, 2026-10-01.
Status: exact computer-assisted conditional lemma, author checked;
independent mathematical review and formalization pending.

This proves a quantitative capacity restriction for nine specified reference
shapes. It does not prove that an unrestricted Tammes optimizer has one of
these shapes or change the global fifteen-point separation bounds.
The known coordinate construction supplies reference data, not a new packing
record or an assumption of global optimality.

## 1. Exact statement

Read the 45 decimal tokens in [coordinates.txt](coordinates.txt) as rational
numbers, grouping consecutive triples into vectors r_0,...,r_14 in R^3.
Scientific notation here denotes an exact rational decimal, not a machine
floating-point number. The bytes and their SHA256 are pinned in
[certificate.json](certificate.json). Do not normalize these reference
vectors in the hypothesis below.

For each row of this table, let I be the six labels in the indicated order
and let p=r_j, where j is the reference center label.

| I, ordered boundary labels | j | Supporting planes | Polytope vertices | Exact squared-norm upper bound |
|---|---:|---:|---:|---:|
| 0,3,4,5,13,12 | 14 | 6 | 22 | 907853/1000000 |
| 0,3,10,1,2,9 | 8 | 5 | 20 | 221367/250000 |
| 0,8,2,7,13,12 | 9 | 4 | 18 | 413661/500000 |
| 1,2,7,13,5,6 | 11 | 5 | 20 | 221367/250000 |
| 1,2,8,3,4,6 | 10 | 6 | 22 | 907853/1000000 |
| 1,2,9,12,13,11 | 7 | 6 | 22 | 907853/1000000 |
| 1,10,3,4,5,11 | 6 | 4 | 18 | 413661/500000 |
| 3,4,14,12,9,8 | 0 | 5 | 20 | 221367/250000 |
| 4,6,11,13,12,14 | 5 | 4 | 18 | 413661/500000 |

Let w_i, i in I, be arbitrary unit vectors satisfying, after one common
orthogonal transformation if necessary,

```
||w_i-r_i|| <= 1/100.
```

All six w_i belong to a common open hemisphere, as proved below.
Define their spherical convex hull C to be the unit vectors of the form

```
x = sum_i alpha_i w_i,  alpha_i >= 0.
```

Equivalently, take every nonzero nonnegative combination and normalize it.
The zero combination does not define a point of C.

**Cap theorem.** Every unit x in C satisfying all six avoidance inequalities

```
x.w_i <= 3/5
```

satisfies

```
x.(p/||p||) > 899/1000.                         (1)
```

There is no requirement that a code contain a point corresponding to label j.
The vector p is only a fixed direction extracted from the reference data.
No contact equalities, side-length bounds, facial incidence, cycle convexity,
irreducibility, degree conditions or initial proximity of x are hypotheses
of this cap theorem.

**Capacity corollary.** If x,y are any two admissible unit vectors in C, then

```
x.y > 2*(899/1000)^2-1 = 308201/500000 > 3/5.   (2)
```

Consequently any spherical code whose distinct pairwise inner products
are at most 3/5 has **at most one additional point in C** when it contains
the six boundary vectors above. This holds for codes of any cardinality,
in particular fifteen. The strict excess in (2) over 3/5 is 8201/500000.

The cap conclusion is closed to both input tolerances: displacement may equal
1/100 and avoidance may equal 3/5. The output inequalities remain strict.

## 2. A general geometric norm-exclusion test

This argument is reusable with other templates. Write eps=1/100, c=3/5.
For the chosen row, put

```
s = sum_{i in I} r_i,
h = s/(|s_1|+|s_2|+|s_3|),
b = min_{i in I} h.r_i,
gamma = eps/(b-eps).
```

The exact checks give b>eps, and ||h||<=1 because its coordinate L1 norm
is one. Hence

```
h.w_i >= h.r_i-||h||*eps >= b-eps > 0.        (3)
```

This proves the hemisphere assertion. If unit x in C has the positive-ray
representation above, (3) and h.x<=1 give

```
sum_i alpha_i <= 1/(b-eps).                   (4)
```

Choose the supporting pairs listed in certificate.json. For a pair (a,d),
orient r_a cross r_d so that its inner product with every r_i in I is
nonnegative, and divide by its coordinate L1 norm. Call the result n.
The checker verifies that the cross product is nonzero, that the orientation
works for all six reference vectors, and that ||n||<=1. Therefore

```
n.w_i >= -eps,
n.x >= -eps*sum_i alpha_i >= -gamma.          (5)
```

These are valid supporting-cone outer inequalities. We do not need to assume
or certify that the selected list contains every facet of the ray hull.
Each selected inequality is individually verified.

Avoidance and the displacement bounds similarly imply

```
r_i.x <= w_i.x+eps <= c+eps = 61/100.          (6)
```

Every unit x also has -1<=x_a<=1 for each Cartesian coordinate.
Suppose, for contradiction, that p.x<=9/10. Equations (5), (6), the cube
bounds and this projection cut put x in the rational polytope

```
B = {z in R^3:
       r_i.z <= 61/100, i in I;
       -n.z <= gamma, for each selected support;
       -1 <= z_a <= 1, a=1,2,3;
       p.z <= 9/10}.
```

B is bounded by the cube. The origin satisfies every inequality strictly,
so B is nonempty and full dimensional. The finite certificate establishes
that **every vertex of B has squared norm strictly below 91/100**.
Since B is the convex hull of its vertices and the squared Euclidean norm
is convex, every point of B has squared norm below 91/100. This contradicts
||x||=1. We have proved p.x>9/10.

The checks also give 0<||p||<=1001/1000. Thus

```
x.(p/||p||) > (9/10)/(1001/1000)
            = 900/1001 > 899/1000.
```

For two points in this cap, the spherical triangle inequality through
p/||p|| gives distance(x,y)<2*arccos(899/1000)<pi. Taking cosine proves
(2). The same calculation can be written using their tangent components;
no numerical inverse trigonometric evaluation is needed.

In general, replace the constants, templates, supports and cut by any
verified values with b>eps, vertex-norm bound<1 and positive center norm.
The argument gives a cap of cosine strictly greater than cut/||p||, and
capacity one whenever the resulting pairwise cosine lower bound exceeds
the code parameter. The specific cap in (1) is a conservative rational
consequence of that test.

## 3. Complete exact finite verification

[check.py](check.py) uses Python arbitrary-precision integers and
fractions.Fraction throughout. A coordinate token is parsed directly into
Fraction. No floating-point value, solver decision, resource timeout or
heuristic enumeration supplies a proof step.

For a polytope with m inequalities A_i.z<=t_i, enumerate all C(m,3)
active-plane triples. A zero determinant is marked singular. Otherwise use
Cramer's rule to obtain the unique rational intersection, check every
inequality, and discard an infeasible candidate. Every feasible candidate
has its squared norm compared exactly with 91/100. A missed sign or failed
comparison aborts with an error. No symmetry reduction is used.

Every vertex of a full-dimensional polytope in R^3 has three independent
active normal vectors; otherwise a small segment through it would preserve
all active equations and inactive inequalities, contradicting extremality.
It therefore appears among these triples. A feasible intersection with
three independent active normals is conversely a vertex. Degenerate
vertices can appear more than once and are deduplicated exactly.

The nine polytopes have respectively 19,18,17,18,19,19,17,18,17 rows.
All **7395 triples** are processed. There are **180 distinct vertices**
across the nine separate polytopes. The upper bounds in Section 1 are exact
rational ceilings of the largest squared norms, not rounded floating-point
estimates; all are strictly below 91/100. EXPECTED.json records each
polytope's complete vertex-set hash, enumeration-status hash, counts and
rational norm ceiling.

[audit.py](audit.py) imports no primary checker code. It reconstructs the
inequalities using a Leibniz determinant expansion and starts from the eight
vertices of the cube. It clips by each remaining halfspace in turn. Every
new vertex lies on a crossing old edge, so the audit includes intersections
of every inside-outside vertex pair. This intentionally includes extra
segment intersections. Retain only feasible points with three independent
active normals; those are precisely the new vertices. Since the origin is
strictly interior at every stage, there is no dimension-drop case. This
gives a different complete vertex enumeration using segment interpolation
instead of active-plane Cramer intersections.

All nine final vertex sets match entry by entry via canonical exact-coordinate
hashes, not merely aggregate counts. The audit independently verifies their
norm bounds. Two hand-checkable cube clips test its handling of newly cut
vertices. [controls.py](controls.py) rejects six changed certificates or
invalid scalar bridges. A rejected larger-displacement certificate is a
failure of that proposed certificate, not a proof against the broader
geometric claim.

This is an exact computational certificate with an unformalized geometric
bridge. The two programs share CPython and Fraction as a trust base.
The separate audit is algorithmic verification by the author, not an
independent researcher's mathematical review or proof-assistant formalization.

## 4. Applying the result to cycles

For a simple minor-geodesic cycle through these perturbed boundary vectors,
gnomonic projection in the hemisphere (3) maps its bounded component to a
simple planar polygon. Even a concave polygon is contained in the convex
hull of its vertices. Its inverse image is therefore contained in C.
This component lies inside an open hemisphere and has area below 2*pi,
so it is the smaller component of the spherical complement. The capacity
corollary applies to that whole component and, more strongly, to C.

For an actual code with pair products at most 3/5, simplicity need not be
an extra premise for these ordered templates. The checks certify
||r_i||<=1001/1000 and r_i.r_(i+1)>=59/100. Thus each perturbed edge has
endpoint inner product at least

```
k = 59/100 - 2*(1/100)*(1001/1000) - (1/100)^2
  = 14247/25000 > 2*(3/5)-1.
```

To exclude an interior crossing between edges AB and DE, write their
common ray as W=alpha*A+beta*B=mu*D+nu*E with all four coefficients
positive. Put u=alpha+beta and v=mu+nu. The two same-edge norm estimates
give ||W||^2>=(1+k)u^2/2 and >=(1+k)v^2/2. The cross-pair code bounds
give ||W||^2<= (3/5)uv. Taking the geometric mean of the lower estimates
would require (1+k)/2<=3/5, contrary to the displayed k.

An edge cannot pass through another code vertex Z either. If Z is the
normalization of alpha*A+beta*B, avoidance of both endpoints gives
||alpha*A+beta*B||<=(3/5)(alpha+beta), whereas its squared norm is at
least (1+k)(alpha+beta)^2/2. These inequalities are incompatible.
Collinear edge overlaps would similarly put an endpoint on another edge.
The distinct boundary vertices hence form a simple cycle in their common
hemisphere. Their smaller region contains at most one other code point,
with no irreducibility or isolated-vertex assumption.

The initial coordinate diagnostic found nine enclosing six-cycles, three
convex and six concave; these supplied the explicit rows. The theorem is
about those nine neighborhoods. No enumeration of all possible six-cycle
shapes in an unrestricted fifteen-point code is claimed.

## 5. Prior art and next dependency

The [primary maintained code table](https://cohn.mit.edu/spherical-codes/)
lists the known fifteen-point construction without an optimality marker.
[Musin--Tarasov's N14 paper](https://arxiv.org/abs/1410.2536) proves N14,
not N15. Their
[irreducible-contact-graph classification](https://arxiv.org/abs/1312.5450),
Proposition 2.6, records that an irreducible hexagonal face has at most one
isolated vertex, crediting Böröczky--Szabó. This certificate does not import
that assertion: it proves a displacement-tolerant restriction for the entire
positive-ray hull of six specified vectors and arbitrary inserted points.
It does not establish the corresponding unrestricted shape theorem.

The [previous nonconvex short-cycle covering lemma](../nonconvex-short-cycles/PROOF.md)
supplies complementary uniform constraints without fixing a shape.
The teammate's
[two-completion certificate](../../six-tammes-2/fourteen-point-completion/PROOF.md)
classifies every last-point completion of fourteen fixed incumbent points
and a separate 26-contact proximity reduction. Neither result is a premise
of this six-boundary capacity proof. Their scopes and tolerances differ.

The next global dependency is a rigorous reason an optimizer or candidate
search box must enter one of the certified six-vector neighborhoods, or a
shape-independent capacity proof extending beyond them. The capacity test
already provides an exact exclusion interface for a box whose six vectors
are enclosed within displacement 1/100 of one listed template after a
common orthogonal transformation.
