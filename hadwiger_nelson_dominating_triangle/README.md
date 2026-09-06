# Every Euclidean unit-distance graph with a dominating clique is three-colourable

**Theorem.** Let D be the vertices of a unit equilateral triangle, and let

```text
C(d) = {x in R^2 : |x-d| = 1},
X = D union the three entire circles C(d), d in D.
```

Every proper three-colouring of D extends to a proper three-colouring of
the **strict unit-distance graph on the entire infinite set X**. There
are no bounds on the number of selected circle points and no hypotheses
excluding additional unit edges or coincident circle points.

More precisely, deleting D from this graph leaves one C9 component and
one component isomorphic to the Cartesian product K3 square C6 for each
nonexceptional six-rotation orbit of unit directions. The C9 and D form
a twelve-point patch with a unique three-colouring once D is pinned.
Each eighteen-point generic component has exactly two three-colourings
compatible with the pinned centres. These choices are independent.

**Corollary.** Every Euclidean unit-distance graph with a dominating
clique is three-colourable. In particular, a graph that needs four or
more colours has neither a dominating vertex, a dominating edge, nor
a dominating triangle. The bound three is sharp, already for a unit
triangle. Any proper colouring of a dominating triangle with three
distinct names from a larger palette extends using only those three names.

This closes the complete unit-triangle neighbourhood construction
family. It supplies no five-chromatic graph, no improvement to the
509-vertex record, and no theorem for an arbitrary three-point dominating
set. The decomposition and classification concern the full graph on X;
an arbitrary finite subgraph can have additional three-colourings.

## Geometry and the translation lemma

All distances are **exactly one**, not at most one. A unit-distance graph
may omit unit edges; we first colour the graph containing all of them.
Distinct graph vertices have distinct embedded points. A set dominates
a graph if every vertex outside it has a neighbour in the set.

Normalize by a Euclidean isometry to complex coordinates

```text
omega = (1+i*sqrt3)/2,
(d_0,d_1,d_2) = (0,1,omega),
U = {omega^j : 0 <= j < 6}.
```

Reflection causes no change to the argument. The normalizing triangle
has side one; no scaling of the forbidden distance is made.

**Unit-rhombus lemma.** Suppose |a-b|=1, x lies on C(a), y lies on C(b),
|x-y|=1, and x,y are not a or b. Then

```text
y-b = x-a.
```

To prove it, y is an intersection of the unit circles centred at x and
b. These circles are distinct because x is not b. Two known intersection
points are a and x+b-a. If those points are distinct, the at-most-two
intersection bound exhausts the possibilities, and y is not a. If they
coincide, x=2a-b, so |x-b|=2: the circles are tangent at a, giving no
allowed y. This also handles the collinear degeneracy. The excluded
case x=b is a centre vertex, whose neighbours are treated separately.

Conversely, x=a+z and y=b+z are always at unit distance for |z|=1,
provided they are distinct points. Thus every non-centre cross-circle
edge is precisely a translate of the corresponding centre edge. This
is an exact identity, not a test restricted to a finite sample.

On one unit circle, unit neighbours differ by a rotation of plus or
minus pi/3. Each orbit is a C6 and different orbits have no same-circle
unit edges. Its squared chord values for steps 0 through 5 are

```text
0, 1, 3, 4, 3, 1.
```

## All circle intersections and exceptional points

For any distinct centres a,b in D, the two common points of C(a),C(b)
are the two equilateral completions of ab. Their differences from each
centre belong to U. In this triangle one common point is the third
centre, and the other is its reflection across ab. In particular, every
point lying on two circles belongs to

```text
P = union over d in D of (d+U).
```

All three centres also belong to P. In lattice notation (a,b) means
a+b*omega. The twelve distinct points, their three-colours, and their
fixed indices are:

| Index | (a,b) | Colour |
|---:|---|---:|
| 0 | (-1,0) | 2 |
| 1 | (-1,1) | 1 |
| 2 | (-1,2) | 0 |
| 3 | (0,-1) | 1 |
| 4 | (0,0), centre d_0 | 0 |
| 5 | (0,1), centre d_2 | 2 |
| 6 | (0,2) | 1 |
| 7 | (1,-1) | 2 |
| 8 | (1,0), centre d_1 | 1 |
| 9 | (1,1) | 0 |
| 10 | (2,-1) | 0 |
| 11 | (2,0) | 2 |

For two lattice points the squared distance is A^2+A*B+B^2, where A,B
are their coordinate differences. Its unit solutions are exactly the
six directions U: multiply by four to obtain
`(2*A+B)^2+3*B^2=4`, which forces B in {-1,0,1} and gives those six
integer solutions. Each changes `a+2*b mod3`, so that formula properly
colours the entire triangular lattice and hence P, with d_i in colour i.

P has exactly 24 unit edges. After deleting D its nine remaining vertices
form the cycle, in indices,

```text
0,1,2,6,9,11,10,7,3,0.
```

No additional unit chord exists by the six-direction test. The three
shared outer points 1,7,9 each have two differently coloured centre
neighbours, forcing colours 1,2,0 respectively. Each of the other six
outer points has a centre neighbour and one of those already forced
outer neighbours in different colours. These force the six remaining
values in the table. Thus P has exactly one colouring with d_i pinned
to i. The finite checker also exhausts all 3^9 possible outer colour
assignments independently of this argument.

## The continuum of generic components

Every other rotation orbit has a unique representative

```text
u = exp(i*theta),  0 < theta < pi/3.
```

For this representative define

```text
Q(theta) = {d_i + omega^j*u : 0<=i<3, 0<=j<6}.
```

All eighteen points are distinct. Within one circle the six directions
are distinct. A coincidence between points on different circles would
be a common circle point, already in P, forcing its direction into U,
contrary to the strict range for theta. The same reasoning proves that
different Q(theta) are disjoint and do not meet P. Every point of X is
in exactly one of P or these Q(theta): for a point outside P, its circle
is unique and its unit direction has a unique such six-orbit expression.

Within Q(theta), write a vertex as (i,j). The complete non-centre edge
list is

```text
(i,j) -- (i,j+1 mod6),
(i,j) -- (k,j) for i != k.
```

The first type is the same-circle chord rule. The second is the
translation lemma and its converse. These are exactly the edges of
K3 square C6: eighteen vertices and 36 edges. The only centre neighbour
of (i,j) is d_i, since an additional centre neighbour would put the
point on two circles and hence in P.

There are no unit edges between different generic components, or between
a generic component and P minus D. For same-circle edges the six-rotation
orbit is unchanged. For cross-circle edges the translation lemma keeps
the unit direction unchanged. Both preserve the exceptional/nonexceptional
orbit and the representative theta. Centre-to-rim edges are retained:
each centre has all the circle neighbours just described. It would be
incorrect to claim that the entire twelve-point patch has no edges out.

This proves the full decomposition, including all continuum points and
all possible additional unit edges. The finite certificate illustrates
one generic component but is not the basis for quantifying over theta.

## Explicit colouring and its complete classification

Pin d_i to colour i in {0,1,2}. Use the lattice colouring on P and, for
every generic component, put

```text
colour(d_i + omega^j*exp(i*theta)) = i + (-1)^j  (mod3).
```

This differs from the owner centre's colour, changes along each C6 edge,
and is a permutation of all three colours on each fixed-j triangle.
It is therefore proper on every edge listed above. There is no appeal
to arbitrary orbit representatives: theta is the unique angle in the
open interval, and the sector boundaries belong to P. The formula
colours the entire infinite graph explicitly.

For completeness, in any three-colouring compatible with the centres,
the three vertices at fixed j must use a permutation of {0,1,2} with
no fixed point i. The only two possibilities are

```text
(1,2,0),  (2,0,1).
```

Consecutive columns must use different choices because of their three
same-circle edges. Either choice then alternates consistently around
the even six-cycle. There are exactly two compatible colourings of
each Q(theta), namely replacing `(-1)^j` in the formula by
`epsilon(theta)*(-1)^j` with epsilon(theta) in {-1,1}. The values can be
chosen independently for different theta. Along with the unique patch
colouring, this describes every three-colouring of the full graph with
the centres pinned. Permuting three colour names gives all six proper
centre prescriptions and completes the theorem.

## Dominating cliques and construction scope

If a triangle D dominates an embedded unit-distance graph G, every vertex
lies in X. Restrict the preceding colouring, even if G omits some unit
edges or contains only finitely many circle points.

A planar unit-distance clique has at most three vertices. Indeed, for
a fixed unit pair its only possible common unit neighbours are the two
equilateral completions, whose distance is sqrt3 rather than one.
A dominating edge can be completed to a unit triangle; its two-circle
support is a subset of X. A dominating vertex can likewise be included
in a unit triangle. Restriction proves the clique corollary in all
nonempty cases. The empty graph is trivial.

This gives a necessary condition for any construction requiring four
or five colours: its vertices cannot all belong to the closed graph
neighbourhood of one unit triangle. Here neighbourhood refers to exact
unit edges, **not filled disks**. A third centre forming an arbitrary
non-unit triangle is not covered. Nor does the result classify extensions
when terminal colours repeat after some centre edges are omitted, or
classify all colourings of a partially populated support.

The previous [two-centre theorem](../hadwiger_nelson_two_centre_circle_closure/README.md)
gave a sharp universal four-colour bound for arbitrary centre separation.
There is no conflict: its four-chromatic sharpness has a nonadjacent
dominating pair. Here adjacency gives the rigid rhombus relation and
lowers the bound to three, while allowing a third mutually adjacent
centre. Neither theorem is used as a premise of the other proof.

## Reproducible exact certificate

[build.py](build.py) generates a **1,493-byte** certificate for P together
with one complete generic component at `u=(3+4*i)/5`. The union has
thirty distinct points and 78 complete unit edges. Coordinates are exact
in Q(sqrt3), recorded as four integer coefficients with denominator 10.
The certificate includes both pinned colourings. Its SHA256 is

```text
f3e065d5907a96a41b9d0fe9ae4dfe5fc7ee141ac69030ea497082f1eb199e4c
```

The [separate checker](verify.py) imports no producer or inherited code.
The producer iterates an explicit rotation on four coefficients. The
checker reconstructs the exceptional patch from a lattice norm test,
uses a closed trigonometric table to rebuild the generic points, and
computes distances with sparse squarefree-radical multiplication by gcd
reduction. It compares every coordinate and every edge entry.

It checks all 435 pair norms, 90 circle memberships, 48 directed
non-centre rhombus incidences, the six orbit chords, the exact C9 and
K3 square C6 decompositions, and all six column permutations. Independent
enumeration checks all 19,683 pinned patch assignments and 262,144 generic
assignments allowed by centre spokes, obtaining exactly one and two
colourings respectively. The checker also tests all 64 column-state
words, all six centre permutations and 936 permuted edge inequalities.
Five malformed certificates are rejected. Normal and optimized runs
produce identical reports.

From the repository root, Python 3.11.2 and its standard library suffice:

```sh
python3 -B hadwiger_nelson_dominating_triangle/build.py --out /tmp/hn-triangle
python3 -B hadwiger_nelson_dominating_triangle/verify.py --work /tmp/hn-triangle
```

The output directory must be new. See [expected.json](expected.json),
[validation.json](validation.json) and [SHA256SUMS](SHA256SUMS). The build
takes about 0.013 seconds and the audit about 0.4 seconds on one thread;
peak memory was not measured. There are no native solver calls, external
mathematical input files, omitted large certificates or background jobs.

The trust boundary is elementary circle geometry and the analytic
decomposition above, exact coordinate transcription, squarefree-basis
independence, Python integer/Fraction semantics and complete finite loops.
Finite sample verification alone would not prove the continuum theorem.
The separate implementation is author-run; external review and formal
verification of the new theorem are not claimed.

## Prior work and campaign checkpoint

Targeted searches for dominating triangles, dominating cliques and
three-circle unit-distance colourings did not locate this precise
statement. Search hits about unit-disk domination or great-circle
arrangement graphs concern different objects and provide no premise.
No priority claim is made from this limited search. The proof is
self-contained elementary geometry, rather than an imported chromatic
classification.

The primary [Parts paper](https://arxiv.org/html/2010.12665v2) and
[Haugland manuscript](https://arxiv.org/html/2608.04542v4), checked
2026-09-06, still report the 509-vertex record. This work does not improve it.

HN2's [H514 closure](../hadwiger_nelson_heule514_whole_decision/README.md)
is now committed in Discovery Net: every subgraph of that fixed support
on at most 508 vertices is four-colourable. The prepublication repository
refresh also found its completed [122-centre incidence theorem](../hadwiger_nelson_heule_fresh122_incidence/README.md):
the fresh graph has 65 tree components and one 37-vertex component whose
unique cycle has length four, making it two-choosable. Its full 632-point
support remains open. Both mechanisms remain separate and provide no
premise here. The fixed Moser/Parts attachment and centred heptagon lines
remain retired under coordination.

This pass completes the rigid adjacent-centre mechanism and yields.
No different centre separation, fourth centre, radius ladder or further
construction phase is started. Future constructions must break the
dominating-clique hypothesis; merely filling more points on these three
unit circles cannot help.
