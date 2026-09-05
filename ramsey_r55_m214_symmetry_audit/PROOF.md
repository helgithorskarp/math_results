# A sharp degree/incidence obstruction to thirteen moving 3-cycles

## Standalone lemma

Let G be a simple graph on 43 vertices with degree sequence `20^13 21^30`.
Let E be its thirteen degree-20 vertices, and suppose every vertex has at
least six neighbors in E. Every automorphism of order three then has at
most twelve moving 3-cycles. This statement does **not** assume that G is
a Ramsey graph.

Write `a(v)=|N(v) intersect E|` and `s(v)=a(v)-6`. Double counting gives

```text
sum_v s(v) = sum_{e in E} d(e) - 43*6 = 260-258 = 2.
```

The set E is invariant because it is a degree class. Therefore a and s are
constant on each automorphism orbit. Since s is a nonnegative integer and
its total is two, it vanishes on every moving 3-cycle. All two units occur
on fixed vertices.

Let F be the fixed vertices, H=G[F], and `b(v)=|N_H(v) intersect E|` for
v in F. Every moving cycle contributes either zero or three neighbors to
a fixed vertex. Hence

```text
d_H(v) = 2 mod 3  if v is in E,
d_H(v) = 0 mod 3  otherwise,
b(v)   = s(v) mod 3.
```

Because `0 <= s(v) <= 2`, the last congruence identifies s(v) with the
least nonnegative residue of b(v). Thus

```text
sum_{v in F} (b(v) mod 3) = 2.                         (1)
```

There must be at least three fixed vertices outside E. Indeed, if F
were contained in E, then b(v)=d_H(v)=2 mod 3 for every fixed vertex.
Equation (1) would force |F|=1, whose H-degree zero contradicts the
required residue two. Thus F has a vertex outside E; the number of
such vertices is a positive multiple of three because the entire
degree-21 class has size thirty.

There are at most fourteen moving cycles on 43 vertices. If there are
fourteen, F has one vertex. Since `|E intersect F| = 13 mod 3`, that vertex
is in E. Its H-degree is zero, contradicting the required residue two.

If there are thirteen moving cycles, F has four vertices and contains
either one or four vertices of E.

* With one E vertex, that vertex has H-degree two. Each of its two
  neighbors is outside E and must have H-degree three. Both are adjacent
  to the remaining, third non-E vertex. That third vertex is not adjacent
  to the E vertex, so its H-degree is two, a contradiction.
* With four E vertices, all four H-degrees equal two. Then every b(v)=2,
  and the left side of (1) is eight, a contradiction.

This excludes thirteen and fourteen cycles, proving the lemma. The
enumeration in `verify.py` is a redundant, exact audit of these tiny
fixed graphs: it scans 1+64+64=129 labeled graphs. Degree congruences
leave zero, zero, and three graphs, respectively. The last three are
the labeled 4-cycles, all with residue sum eight.

## Sharpness for these assumptions

`degree_incidence43.edges` is a literal 445-edge graph on vertices 0..42.
Its degree-20 class is `{0,...,11,36}`. All a(v)=6 except a(37)=a(42)=7.
The permutation rotating each of the twelve triples
`(0,1,2),...,(33,34,35)` and fixing 36..42 is an automorphism.

The constructor starts with the quadratic-residue graph on Z/13Z,
acted on by multiplication by three. Its four nonzero orbits label the
four moving E triples and zero labels vertex 36. The six fixed non-E
vertices correspond to pairs of those four triples. The eight moving
non-E triples carry a 12-regular circulant on Z/24Z, in coordinates where
addition by eight rotates each triple. Explicit balanced inter-block
incidences and a fixed K_3,3 with one edge removed complete the graph;
all choices are in `construct_fixture.py`.

The direct edge-list verifier establishes the degrees, all incidences,
and preservation of every edge by the permutation. It also verifies
that `{0,1,2,40,41}` is an independent five-set and that all 43 local red
triangle equalities of the M=214 formulation fail. This graph proves
sharpness only for the stated degree/incidence lemma. It is neither an
M=214 graph nor a Ramsey witness.

## Conditional application to the M=214 hard branch

Here the hard branch means both local color deficiencies are at least
seven. The upstream M=214 classification supplies red degree sequence
`20^13 21^30` and local bounds

| red degree | red local triangle cap | blue local triangle cap |
|---|---:|---:|
| 20 | 93 | 107 |
| 21 | 100 | 100 |

These are the caps from U(20)=100, U(21)=107, U(22)=114 after subtracting
seven. The reduction to this degree sequence and those extremal inputs
are imported dependencies; this package does not rerun their catalog
or whole-profile classification.

The remaining arithmetic can be derived directly. The graph has m=445
red edges. Counting mixed wedges, the total number of monochromatic
triangles is

```text
C(43,3) - (13*20*22 + 30*21*21)/2 = 2866.
```

The red cap sum is 4209 and the blue cap sum is 4391. Their excess over
three times 2866 is two. The total red excess is a nonnegative multiple
of three, so it is zero. Thus every red local count equals its cap;
there are 1403 red and 1463 blue triangles.

For any simple graph, writing t_R(v) and t_B(v) for its incident
monochromatic triangles, counting edges across the two neighborhoods
gives

```text
t_R(v)+t_B(v) = C(42-d(v),2) - m + sum_{w in N_R(v)} d(w).
```

For this degree profile the final sum is `21*d(v)-a(v)`, and the
right side is `206-a(v)` in both degree cases. Subtracting the exact
red count shows that the blue excess is precisely `a(v)-6`.
Consequently all a(v)>=6, and the standalone lemma applies.

The previously certified, independently reviewed global restriction
requires at least ten moving 3-cycles in any Ramsey (5,5;43) graph.
Combining it with this new conditional upper bound leaves **10, 11, or
12 moving cycles** in the M=214 branch, with **13, 10, or 7 fixed
vertices**, respectively. This does not exclude any of those three
types and does not constrain the maximum outside this branch.

For later valid symmetry projections, let q be the number of moving
cycles in E and k the total. The fixed class sizes are
`13-3q` and `30-3(k-q)`. The latter is at least three by the additional
fixed-vertex conclusion above. These class sizes and the imported
minimum k>=10 leave these nine necessary count patterns:

```text
k=10: q=1,2,3,4
k=11: q=2,3,4
k=12: q=3,4.
```

These are arithmetic possibilities, not a classification of realizable
actions. In particular, no enumeration on seven fixed vertices is
claimed here.

## Formula equivalence under the stated imported branch inputs

At least 28 of the 30 degree-21 vertices have a(v)=6, since all excess
units sum to two. Choose one as vertex 13. Relabel E to 0..12, then
permute within E and within the other degree-21 vertices to give the
anchor red neighborhood `{0,...,5} union {14,...,28}`. These choices
preserve existence. No assumption that this anchor is fixed by a
prospective automorphism is justified or imposed.

The OPB has all two-color K5 inequalities on every five-set, exact
conjunction gates for red triangles, degree and red local equalities,
the a(v)>=6 inequalities, and the anchor units. A branch graph extends
to its triangle bits and satisfies every row after this normalization.
Conversely, the conjunction rows identify actual triangles of any
Boolean model. The rows enforce the stated degree sequence and all
Ramsey constraints; the identity above supplies the blue caps. At the
anchor, the red edge counts in its red and blue neighborhoods are 100
and 110, respectively, so the red cross count is `445-21-100-110=214`.
This checks the encoding equivalence **conditional on the imported
branch definition and degree-profile reduction**. No SAT/UNSAT verdict
is supplied, and this is not a new independent review of all upstream
classification results.
