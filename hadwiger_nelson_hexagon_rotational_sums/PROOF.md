# Complete rotational sum classification

Let `omega=(1+i sqrt(3))/2` and

```
H = {a+b omega : a,b integers, max(|a|,|b|,|a+b|)<=2}.
S(u) = {x+u y : x,y in H}, |u|=1.
```

Repeated positions are one physical vertex. All pairs at distance exactly one
are edges. H has 19 vertices, 42 unit edges and 24 unit triangles. A rigid
motion or reflection of the whole construction changes none of the claims.
Independent translation of either summand only translates S(u), and reflection
of a summand gives the same family because H is conjugation-invariant.

**Theorem.** Every S(u) is three- or four-chromatic. Exactly 48 rotations are
four-chromatic. They constitute four orbits under `u -> omega*u` and
`u -> conjugate(u)`. There are 126 other exceptional rotations, all
three-chromatic. Every remaining rotation gives a three-chromatic graph
with 361 vertices and 1,596 edges. Exceptional physical orders are
61, 271, 349 or 361; the full data appear in `EXPECTED.json`.

These are rotation orbits, not necessarily graph isomorphism classes. The
result closes this precise complete family below the 508-vertex target. It
makes no claim for larger hexagons, three summands, a general planar source,
or the existence of a smaller five-chromatic graph. No priority claim is made.

## 1. Exhaustive finite reduction

Write `d=x-x'`, `e=y-y'`. The actual difference set `H-H` is enumerated from
all source pairs and has 61 vectors. If `e=0`, the pair is a unit edge precisely
when `|d|=1`, independently of u. The corresponding statement holds for d=0.
For both differences nonzero set

```
m=|d|^2, n=|e|^2, c=1-m-n,
d*conjugate(e) = (p+i sqrt(3) q)/2.
```

Here m,n,p,q,c are integers, with `p^2+3q^2=4mn`. The additional-edge equation is

```
2 Re(d*conjugate(e)*conjugate(u)) = c.
```

There are 60*60=3,600 ordered difference pairs. Each gives at most two unit
rotations. The producer solves the circle-line intersection directly:

```
u = (p+i sqrt(3)q)*(c +/- i sqrt(4mn-c^2))/(4mn).
```

A negative radicand gives no root; a zero radicand is retained as a tangent.
The independent verifier uses a different elimination. Every unit rotation
except -1 has a unique real parameter t with

```
u = (1-3t^2+2i sqrt(3)t)/(1+3t^2).
```

The equation becomes

```
3(p+c)t^2 - 6q*t + (c-p) = 0.
```

The verifier exhausts this integer quadratic, treating zero leading
coefficient separately, and includes u=-1 exactly when c=-p. A vanishing
polynomial is impossible because d and e are nonzero. It obtains 174 distinct
exact rotations. Squarefree radical reduction and rational arithmetic make
root equality exact; no approximate angle or tolerance is used.

Every coincidence is already among these additional-edge rotations. Suppose
`x+u y=x'+u y'` with different product labels. Then x differs from x' and y
from y'. Every source vertex lies in a unit triangle, so x' has a unit
neighbour z different from x. The points represented by `(x,y)` and `(z,y')`
are at unit distance, and their two source differences are both nonzero.
Their additional-edge equation therefore includes this rotation. The producer
also enumerates coincidences directly as a cross-check.

At any rotation outside the 174 roots, the physical graph is consequently
exactly the Cartesian product of two copies of the strict graph on H. It has
361 vertices and `2*19*42=1596` edges. The explicit colouring

```
colour((a+b omega)+u(c+d omega)) = a-b+c-d mod 3
```

is well-defined there and proper. An inherited triangle proves that three
colours are necessary.

## 2. Rotation symmetry and exact point audit

Multiplication of u by omega permutes H in the second summand, so it leaves
S(u) unchanged as a point set. Conjugation reflects S(u). The certificate has
15 representatives. The verifier expands each representative under all six
multiplications and conjugation, checks disjointness of the resulting orbits,
and compares their union exactly with its independently enumerated 174 roots.
One orbit has size six and 14 have size twelve. No representative-generation
code is imported by the verifier.

An angle row `[s,A,B,C,D,L]` means

```
u = (A+B sqrt(s))/L + i sqrt(3)*(C+D sqrt(s))/L.
```

Here L is positive, coefficients and denominator have gcd one, and s is
squarefree and greater than one, or zero with B=D=0. Its unit norm is checked
by the two exact equations

```
A^2+sB^2+3C^2+3sD^2 = L^2,
2AB+6CD = 0.
```

For each representative the verifier constructs all 361 product positions
using independent sparse squarefree-radical arithmetic, with common coordinate
denominator 2L. It compares all 64,980 labelled pairs by direct squared
Euclidean distance. It checks equal colours on every coincident pair and
different colours on every unit pair, and deduplicates physical edges.
This is 974,700 pair checks in total. Extra unit edges are fully included.

The producer instead builds edge and collision types on the 61-by-61
source-difference table and uses those types to construct each graph. Its
quadratic-field representation and circle-line root formula are separate
from the verifier's sparse radical representation and half-angle root census.
Both are author checks, not an external independent review.

## 3. Exact three/four classification

The usual residue colouring `q(a,b)=a-b mod 3` colours H. Starting with one
unit triangle, successively add the third vertex of a triangle whenever its
other two vertices have already been reached. The verifier checks that this
reaches all 19 vertices. Hence every proper three-colouring of H is a global
permutation of q: in three colours the third colour of a triangle is forced.

Consider any three-colouring of the Cartesian product H square H. Each layer
with second coordinate y is `pi_y(q(x))` for a permutation pi_y of three names.
For adjacent y,y', every matching x-pair is an edge. Thus the relative
permutation between pi_y and pi_y' has no fixed colour, so it is one of the
two 3-cycles. Since H is connected, all pi_y have the same parity. They have
the form `pi_y(t)=epsilon*t+g(y)` modulo three, with epsilon constant in
{+1,-1}; the matching inequalities imply that g properly three-colours H.
The uniqueness just proved gives `g(y)=delta*q(y)+k`. After a global
permutation of the palette, only the following two product words remain:

```
q(x)+q(y),     q(x)-q(y) modulo 3.
```

A physical three-colouring of S(u) pulls back to a proper colouring of the
Cartesian product, including at exceptional rotations. It must therefore be
one of these two words up to palette permutation. The verifier directly tests
both words on every coincidence and every unit pair. Eleven representative
classes admit at least one word. In each of the other four classes both fail;
`EXPECTED.json` gives the explicit failed pair for each sign. The certified
four-colour word then proves that the chromatic number is exactly four.

Every representative contains a translated copy of H, so no graph in the
family is bipartite. Four size-twelve classes give exactly 48 four-chromatic
rotations; the other exceptional rotations number 174-48=126.

## 4. Certificates, discovery and scope

The certificate contains one 361-character colour word per representative,
indexed by the lexicographically ordered product of the 19 integer pairs.
Keeping product labels makes coincidence consistency an explicit obligation.
The source, finite reduction and final proof need no imported dataset or SAT
status. Integers, rational arithmetic, independence of squarefree radicals,
the written finite reduction, and executable checker semantics are the trust
boundary. No proof assistant or external author review is claimed.

Discovery made 15 Glucose42 queries, each with a fixed 200,000-conflict budget;
all returned SAT, with at most 49 conflicts. Four at-least-one colour literals
per vertex and four inequality clauses per edge suffice: adjacent nonempty
sets of true colours are disjoint, so choosing the first true colour gives
a proper word. The verifier checks the words without using this solver.
The two-pattern argument, rather than any UNSAT verdict, supplies the exact
lower bounds of four. A separate producer replay regenerated the certificate
byte for byte. There was no source expansion, cap increase or further family.
