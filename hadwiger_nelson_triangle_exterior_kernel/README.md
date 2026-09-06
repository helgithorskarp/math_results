# A finite four-colour kernel for exterior couplings of a unit-triangle neighbourhood

**Theorem.** Let D be a unit equilateral triangle, X its full closed
unit graph neighbourhood, and W any finite set of k distinct points
outside X. There is an explicitly defined finite strict unit-distance
subgraph H of X union W, on at most

```text
37*k + 12 vertices,
```

such that **H is four-colourable if and only if the entire infinite
strict unit-distance graph on X union W is four-colourable**.

In particular, a non-four-colourable example with at most **13 exterior
points** would yield a non-four-colourable unit-distance graph on at
most **493 vertices**, and hence a five-chromatic induced subgraph of
that size. This is a conditional reduction, **not an existence claim**.
No such example has been found here.

**Completed actual construction test.** Put

```text
omega = (1+i*sqrt3)/2,       D = {0,1,omega},
U = {omega^j : 0<=j<6},      P = D+U,
rho = (5+i*sqrt11)/6,        W = (P minus D)+rho.
```

These nine exterior points form a translated C9. The finite reduction
has **57 vertices and 168 unit edges**. A proper four-colouring extends
over all of X union W. The finite core itself is not three-colourable,
so this whole infinite construction has chromatic number **exactly four**.
The test escapes the parent's three-colour obstruction but does not
improve the 509-vertex record. Only this exact rho and exterior set were
tested; no parameter interval or different placement is excluded.

## Definitions and inherited geometry

Here

```text
C(d) = {x in R^2 : |x-d| = 1},
X = D union C(0) union C(1) union C(omega).
```

“Outside X” means absent from these circles and centres, **not outside
their filled disks**. All unit edges are included. Smaller graphs with
omitted edges or circle points inherit a colouring by restriction.

The [dominating-triangle theorem](../hadwiger_nelson_dominating_triangle/README.md)
gives a complete geometric decomposition. P has twelve vertices and 24
unit edges, including the three centres. P minus D is a C9. Every other
six-rotation orbit of a unit direction u gives a component

```text
Q(u) = {d_i + omega^j*u : 0<=i<3, 0<=j<6},
(d_0,d_1,d_2) = (0,1,omega).
```

After deleting D, this eighteen-point component is exactly the Cartesian
product K3 square C6. Its edges join (i,j) to (i,j+1), modulo 6, and to
(h,j) for h different from i. Vertex (i,j) has only d_i as a centre
neighbour. Distinct generic components have no edges between them and
no edges to P minus D.

These assertions hold for every real unit direction, including all
circle intersection cases. The key fact is the unit-rhombus identity:
for unit-separated centres a,b, any non-centre unit edge between
x in C(a) and y in C(b) satisfies y-b=x-a. The parent proves the
degeneracies and gives an explicit angular orbit convention. No finite
sample is being extrapolated to the whole circle support.

With d_i in colour i in {0,1,2}, the generic component has exactly two
compatible three-colourings:

```text
c_sign(i,j) = i + sign*(-1)^j (mod3),   sign in {-1,1}.
```

P has a unique compatible three-colouring, namely a+2*b modulo 3 on
lattice coordinates a+b*omega. The new four-colour argument below uses
these two explicit generic colourings; it does not assume that arbitrary
four-colourings have this binary form.

## Two exterior incidences can always be restored

Fix any proper four-colouring of the three centres and some external
vertices. Rename the centre colours 0,1,2 and the unused fourth colour 3.
An edge from an external vertex of colour f to a generic vertex v
forbids f at v. Count **edges**, not just distinct touched vertices:
two external neighbours of the same shell point give two incidences.

**Extension lemma.** A generic component subject to at most two such
forbidden-colour incidences always extends the given centre and external
colours.

**Proof.** A restriction forbidding the owner-centre colour is redundant.
A restriction forbidding colour 3 is satisfied by both displayed base
three-colourings. Every other restriction is violated by exactly one
of those two colourings.

If there is at most one restriction of the last kind, choose the base
colouring satisfying it. This satisfies every restriction, including
ones forbidding 3. If there are two of the last kind, no restriction
forbids 3. Choose a base colouring violating at most one of the two
restrictions. If it violates one, recolour its vertex 3. No other vertex
of the component uses 3, its centre does not use3, and none of the at
most two external incidences forbids 3. This also handles two different
restrictions at the same vertex. Every edge and restriction is proper.
QED.

The rule permits repeated incidence restrictions and arbitrary external
colours. It makes no assumption that the external vertices are mutually
independent. A component with three incidences cannot be discarded by
this rule: three forbidden colours can exhaust one vertex's allowed
palette. This is a statement about a fixed external colouring, not a
five-chromatic geometric witness.

## The finite reduction and the 493-vertex conditional target

Call a generic component important when it has at least three unit
edge incidences with W. Include in H all points of P, all of W, and
every vertex of each important component, with **all actual unit edges**
among these points.

Each w in W is distinct from every centre. The circles C(w),C(d_i)
are therefore distinct and meet in at most two points. Consequently w
has at most six neighbours in X, and the total number of W-to-generic
edge incidences is at most 6*k. Common circle points belong to P and
cannot increase this upper bound. If h components are important, then

```text
3*h <= 6*k,       h <= 2*k,
|H| = 12+k+18*h <= 37*k+12.
```

Every four-colouring of the full graph restricts to H. Conversely, take
any four-colouring of H. Each omitted generic component has at most two
incidences with W and extends by the preceding lemma. Different omitted
components have no edges between them, to important components, or to
P minus D. Their centre edges are already covered by the extension
lemma. Components with no exterior contacts use the explicit parent
formula; only finitely many components have contacts. Thus all of X
union W is coloured, proving the equivalence without an infinite search.

For k<=13, the bound is at most493. If such an H is not four-colourable,
choose an inclusion-minimal induced subgraph that is not four-colourable.
Deleting any vertex makes it four-colourable; restoring that vertex
with a fifth colour proves the minimal subgraph is five-chromatic.
Its order is at most493. No premise asserts the existence of a W with
this property, and the present concrete W gives the opposite verdict.

This is an exact finite geometric reduction for arbitrary real W.
It does not assert a polynomial-time algorithm on unspecified or
uncomputable real coordinates. Exact representation and contact-orbit
identification must be supplied for a concrete computation. The fixed
test below provides both. For a partially populated non-four-colourable
subgraph of X union W, this reduction may add shell points; H need not
be a subgraph of that partially populated graph.

## An exact 11-state extension procedure

The generic component also has a complete four-colour extension test
for arbitrary boundary lists, not only the two-incidence case. With
centres pinned 0,1,2, a fixed-j triangle has the 11 states

```text
(c_0,c_1,c_2): distinct entries from {0,1,2,3}, with c_i != i.
```

Consecutive column states are compatible exactly when all three
corresponding entries differ. There are 44 ordered compatible state
pairs. For a fixed exterior colouring, delete each column state that
uses a forbidden exterior-neighbour colour. Existence of a compatible
six-cycle in these six allowed state sets is exactly extension over
the component. Trying each initial state and propagating compatible
states around the cycle decides this and reconstructs a colouring.
Empty lists and multiple external neighbours are handled explicitly.

The parent patch can similarly be treated as its C9 after the centres
are pinned, with each outer vertex's list excluding its centre and
external-neighbour colours. A four-state cycle test suffices there.
Different generic components factor once D and W are coloured. This
is a finite interface for four-colourability; no claim is made that
the two three-colour states describe all four-colour solutions.

The executable `cycle_oracle` in [verify.py](verify.py) implements the
generic 11-state procedure. Its result is checked against a separate
constructive repair on all 2,701 unordered multisets of zero, one or
two restrictions drawn from 18 vertices times 4 forbidden colours.
Both witnesses are directly checked. Empty-list and adjacent forced-
fourth-colour cases provide two negative controls for the general oracle.
These finite controls supplement the proof of the universal rule.

## One actual exterior placement

Use the displayed rho and W=(P minus D)+rho. They are exact coordinates
in the real field K=Q(sqrt3,sqrt11) on each Cartesian axis. The producer
and checker reconstruct all nine points and verify that none is a
centre or lies on any of the three circles. W has the same C9 graph
as P minus D, by translation. No approximate distance test is used.

The issue is not merely colouring selected shell points: we must locate
**every important component of the entire infinite X**. Directly adding
some circle intersections would not prove completeness. The following
finite repeated-contact test does.

Index the 27 ordered source pairs (w,d_i), in exterior-major order, and
write their nonzero relative vectors as a=w-d_i. A contact at d_i+z
is equivalent to

```text
|z|=1,        2*dot(z,a)=|a|^2.
```

Suppose another contact has unit direction omega^(-j)*z and source
vector b. Rotate its equation to get the same form with b'=omega^j*b.
Thus a common direction solves two line equations in the plane.
When their normals are nonparallel they have a unique intersection,
which can be checked for unit norm exactly in K.

When the normals are parallel, write b'=lambda*a. The two equations
can share a solution only if lambda=lambda^2. Since the normals are
nonzero, lambda=1, so they must be **identical**, not merely parallel.
The27 source vectors form 18 six-rotation classes: nine classes have
one source and nine have two. This entire classification is checked
exactly. A given source can contribute at most one incidence to any
one prescribed rotated normal, since a nonzero vector has six distinct
rotates. Therefore three incidences of an important component cannot
all have identical rotated normals. Some two give a nonparallel pair.

The enumeration includes **equal source pairs** as well as distinct
pairs: the two intersections from a single circle pair can lie in
the same rotation orbit. Omitting the diagonal cases would leave a
completeness gap. All 27*28/2*6=2,268 pair/rotation cases are processed.
Reversing a pair is unnecessary because every relative rotation is
included and rotating the resulting direction does not change its orbit.

The producer solves the two line equations using exact field division.
The independent checker avoids that division test. For the triangle
with vertices0,a,b', the intersection is its circumcentre, and its
circumradius is one exactly when

```text
|a|^2 * |b'|^2 * |a-b'|^2 = 4*det(a,b')^2,
```

provided the determinant is nonzero. The checker tests this polynomial
identity in every case. Each positive row then supplies a direction
whose unit norm and both line equations are checked. Nonparallel
uniqueness establishes entrywise equivalence of the two computations.

| Pair outcome | Count |
|---|---:|
| Identical rotated normals | 36 |
| Parallel and incompatible | 84 |
| Nonparallel, circumradius not one | 1,988 |
| Nonparallel, unit circumradius | 160 |
| Total | 2,268 |

The 160 positive rows reduce to three direction orbits. One is U,
already in P. The other two have respectively 15 and 3 exterior edge
incidences; their exact canonical representatives are

```text
u_1 = -rho,
u_2 = (-3-sqrt33 + i*(-sqrt3+3*sqrt11))/12.
```

Both have unit norm. Canonicalization uses lexicographic order on exact
rational coefficient tuples, **not approximate angular ordering**.
All important components must have appeared in the complete pair test,
so there are exactly two. Other contacts may involve directions outside
K, but their components have at most two incidences and restore by the
general lemma; their coordinates need not be generated or approximated.

The core is P union W union Q(u_1) union Q(u_2): 57 distinct vertices.
All 1,596 pair norms give 168 unit edges, including all edges involving
W. A deterministic Python backtracker visits 55 recursive nodes and
finds the positive four-colouring in [certificate.json](certificate.json).
The checker verifies every retained edge directly and checks all 24
global colour permutations. No negative four-colour solver verdict is
used. By the kernel theorem this colours the entire infinite X union W.

It really is four-chromatic. With the centres pinned 0,1,2, P has its
unique three-colouring and the two retained generic components have
two choices each. All four combined shell assignments give an empty
three-colour list at some exterior vertex. The certificate records the
exact lists and an empty-list witness for each case; the checker derives
them directly from the complete core edges. Hence the finite core has
no three-colouring. This is a small positive control for the fourth
colour, not a new smallest four-chromatic graph or evidence of a fifth.

## Reproduction and trust boundary

From the repository root, CPython 3.11.2 and the standard library suffice:

```sh
python3 -B hadwiger_nelson_triangle_exterior_kernel/build.py --out /tmp/hn-exterior
python3 -B hadwiger_nelson_triangle_exterior_kernel/verify.py --work /tmp/hn-exterior
```

The build directory must be new. The 9,018-byte compact certificate has
SHA256

```text
c958f8d74bc0459a3f416947d4928b9dad90e2de0451c551b2082eb5fcd59bdd
```

It stores exact rational coefficients in the ordered basis
(1,sqrt3,sqrt11,sqrt33), with common denominator 12 for the final core,
the 160 concise positive pair rows, all three candidate orbits and their
incidences, the core graph, its positive colouring and the four
three-colour obstructions. There is no omitted large dataset or trace.

The producer uses four-coefficient XOR multiplication and repeated
conjugation for inversion. The separate checker uses sparse squarefree
radicands with gcd multiplication, a closed rotation table and the
circumradius polynomial. It imports no producer or parent executable
code. The parent finite certificate was also replayed separately; the
analytic decomposition remains an explicit mathematical dependency.

Five malformed certificates are rejected: altered normal classes,
missing positive pair rows, omitted important components, missing core
edges and an invalid colouring. Normal and optimized runs give identical
reports. [expected.json](expected.json), [validation.json](validation.json)
and [SHA256SUMS](SHA256SUMS) preserve the exact checks and provenance.
Production takes about 6.7 seconds and the full independent audit about 4
seconds on one thread; peak memory was not measured. No native SAT/SMT
solver, UNSAT trace or background computation is used.

Trust remains in the parent universal circle decomposition, the analytic
two-incidence and repeated-contact arguments above, exact coordinate
transcription, independence of the four squarefree basis elements,
Python integer/Fraction semantics and complete loops. The finite
certificate alone is not a proof of the continuum extension. The
independent implementation is author-run; external review and formal
verification of this new result are not asserted.

## Campaign boundary

The primary [Parts paper](https://arxiv.org/html/2010.12665v2) and
[Haugland manuscript](https://arxiv.org/html/2608.04542v4), checked
2026-09-06, still report 509 vertices. The493-vertex statement above
is conditional and supplies no record improvement. Targeted searches
did not locate this exact exterior-kernel formulation; no priority
claim is made from that limited search.

The [HN2 fresh122 theorem](../hadwiger_nelson_heule_fresh122_incidence/README.md)
and [independent acceptance of H514 closure](../hadwiger_nelson_heule514_whole_decision_review1/README.md)
were read as durable coordination evidence. The prepublication refresh
also found [acceptance of fresh122](../hadwiger_nelson_heule_fresh122_incidence_review1/README.md)
and the completed [H632 transport decision](../hadwiger_nelson_heule632_transport/README.md):
exactly 22 of 544 fixed old colourings extend across the fresh support.
The H632 family remains open; a failed fixed-colouring extension is not
a non-four-colourability certificate. These separate supports provide
no premise here. No Heule support, parked Parts overlap family, fixed
Moser/Parts attachment or centred heptagon construction is re-enumerated.

This completes the first actual exterior-coupling test and the reusable
four-colour reduction. The tested rho is closed negatively for a fifth
colour, including every finite subgraph of its full circle support.
No second rho, additional exterior cycle, radius or construction phase
has begun. Further work must choose a materially different exterior
interaction and test the full four-colour interface, rather than infer
anything from breaking the two three-colour states.
