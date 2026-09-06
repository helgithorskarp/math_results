# A common colouring closes one Moser–Parts terminal connector class

**Computer-assisted theorem.** Fix the seven-point Moser spindle M below.
Let F consist of every equilateral triangle of side sqrt7 with one vertex
at unit distance from at least two distinct points of M, and a different
vertex at unit distance from at least one point of M. There is a single
four-colouring of M together with every vertex of every triangle in F that
is proper on **all** unit edges and makes **every** triangle in F
non-monochromatic.

Consequently every terminal-only assembly of the full archived Parts A159
gadget around M, with each designated terminal triangle in F, is
four-colourable. The number of copies is unrestricted subject to the
assembly conditions below. In particular this closes the proposed
`7+3*159=484` raw-vertex construction in this precise placement class and
all its subgraphs. This is a negative construction result; it supplies no
five-chromatic graph or record improvement.

The theorem does not cover terminal triangles outside F, new contacts with
gadget interiors, overlapping interiors, reduced gadgets, other connectors,
or arbitrary full-gadget placements. It does not require an unverified
claim that monochromatic terminal assignments are impossible in A159.

## Fixed geometry and complete finite reduction

Use complex coordinates

```text
u = 1,  v = (1+i*sqrt3)/2,  rho = (5+i*sqrt11)/6,
M = [0, u, v, u+v, rho*u, rho*v, rho*(u+v)].
```

Indices are zero-based in this order. Reflections and rotations of a terminal
triangle are both included. The entire construction may also undergo one
common Euclidean isometry without changing the conclusion.

Write J for rotation by +pi/2. For each of the 21 pairs p,q of distinct
spindle points, put d=q-p and D=|d|^2. The two common unit-circle centres are

```text
a = (p+q)/2 +/- J(d)*sqrt(4/D-1)/2.
```

Certified inequalities give `0<D<4` for every pair, so neither a coincident
centre nor a tangent case is omitted. Keep all 42 labelled points a; exact
deduplication is unnecessary.

For each a and each m in M put z=m-a, R=|z|^2 and

```text
H = -R^2 + 16*R - 36.
```

If H<0, the circles of radii sqrt7 and 1 centred at a and m do not meet.
This also handles R=0, when the two radii differ. If H>0, R>0 and the two
intersections are

```text
b = a + ((R+6)/(2*R))*z +/- (sqrt(H)/(2*R))*J(z).
```

For each such b take both

```text
c = a + (b-a)*(1/2 +/- i*sqrt3/2).
```

Then {a,b,c} is an equilateral sqrt7 triangle. Conversely, every triangle
in F appears: select a qualifying double-contact vertex, its two distinct
spindle neighbours, a second contacting terminal and its spindle neighbour;
the two circle formulas and one of the two final orientations recover it.
All inequalities in this argument are decided by outward rational
intervals. In particular **none of the 294 second-circle cases has H=0**:
240 are strictly negative and 54 strictly positive. Thus the enumeration
has 216 labelled triangles and 655 labelled point occurrences including M.
Repeated labels or alternative representations of one point are retained.
No floating-point equality, generic-position assumption, or unexamined
circle tangency is used in this coverage proof.

## Positive certificate and conservative geometry

The [producer](build.py) uses [outward dyadic intervals](intervals.py) at
128 bits after every operation. Endpoints are integers divided by 2^128;
products and quotients round outward with integer floor/ceiling, and square
roots use integer `isqrt`. Every labelled exact coordinate is enclosed.

Any pair of point boxes intersecting in both coordinates is merged, with
transitive closure, into one of **189 enclosure clusters**. Each cluster's
bounding box has diameter strictly less than one. For every pair of cluster
boxes, the producer includes an edge if the squared-distance interval
contains one. There are **239 such conservative edges** and **128 distinct
triples of cluster indices** represented by the 216 labelled triangles.
The colour certificate satisfies every edge inequality and every triangle's
non-monochromatic constraint.

These numbers are counts of certified boxes and constraint objects. They
are **not claimed to prove** that there are exactly 189 distinct geometric
points or 128 distinct geometric triangles. Merging boxes may impose extra
constraints; equality of exact algebraic coordinates is never inferred
from overlapping intervals. Exact coincidences are necessarily merged,
and no actual unit edge is omitted. A proper colouring of this conservative
graph therefore gives a well-defined proper colouring of every represented
point. Since every triangle in F appears, it proves the stated simultaneous
colouring theorem.

The [small certificate](certificate.json) additionally lists one colour for
each of the 655 labelled occurrences. The separate [direct checker](verify.py)
uses only this positive witness and freshly computed coordinate enclosures
for the mathematical colour proof. For all **214,185** labelled pairs it
checks one of two implications:

- The same colour implies a squared-distance interval excluding one.
- Different colours imply a coordinate-difference interval excluding zero,
  so the two exact points cannot coincide.

It also checks all 216 labelled triangles are non-monochromatic. These
checks directly prove a proper, well-defined colouring, without trusting
the producer's graph edges, point merging, or distinct-triple count.

The direct checker imports no producer or inherited arithmetic module. It
uses `Fraction` intervals rounded outward to multiples of 10^-45 and different
circle formulas. It classifies second-circle existence by
`sqrt7-1 < distance(a,m) < sqrt7+1`, and constructs intersections from the
along-line distance `(distance(a,m)^2+6)/(2*distance(a,m))` and perpendicular
height `sqrt(7-along^2)`. The branch decisions and all coordinate enclosures
are compared with the producer. Thus the two implementations use different
scalings, algebraic expressions, and final validation obligations.

## Lifting to the full 159-point gadget

Let A be the complete unit-distance graph of the
[archived 159 coordinates](../hadwiger_nelson_nonmono159_214_lowden2/points159.tsv),
with designated terminals at file indices `[141,142,144]`. They form an
equilateral sqrt7 triangle. The
[preceding positive extension theorem](../hadwiger_nelson_long_terminal_gluing/README.md)
certifies that **all 60 non-monochromatic assignments of four colours** to
these terminals extend to A. Four canonical equality patterns
`001,010,011,012` and palette renaming suffice. The earlier exact positive
certificates were replayed for this result. Only this positive extension
fact is imported; the earlier at-most-three degree argument is not needed.

For finitely many isometric copies Vi of A, with terminal triangles Ti in F,
let Ei be their internal strict unit edges and let EM be those of M. On the
complete unit graph G of `M union (union Vi)`, require:

1. For i distinct from j, `Vi intersection Vj` is contained in
   `Ti intersection Tj`, and `Vi intersection M` is contained in Ti.
2. Every unit edge of G outside `EM union (union Ei)` has both endpoints in
   `M union (union Ti)`.

These conditions make gadget interiors private and place all new
interactions in the certified interface. Use the common colouring on M and
all Ti, then independently extend each non-monochromatic terminal assignment
to Vi. The extensions agree at every shared point. Inherited edges are
proper inside M or their copy, and every remaining edge is proper in the
common interface colouring. This proves the full assembly statement.
It also handles arbitrary choices of the isometry mapping A's ordered
terminal set to a candidate triangle.

The raw order of M and three full A copies is at most 484. Conversely, under
the stated private-interior conditions four copies contain at least
`4*(159-3)=624` distinct private vertices, so an assembly on at most 508
vertices has at most three copies. Every such covered assembly is therefore
four-colourable. Actual arrangements with contacts to interiors are outside
the theorem even if their terminal triangles occur in the enumeration.

## A falsified geometric shortcut

A double-contact terminal does not force another terminal to miss M. For
example the exact triangle

```text
(1/2,-sqrt3/2), (0,sqrt3), (5/2,sqrt3/2)
```

has all squared side lengths seven. Its first point is unit adjacent to
M[0] and M[1], its second to M[2], and its third to M[3]. Seven elementary
rational norm identities are checked as a separate fixture. The common
colouring proof includes these cases and does not use the false shortcut.

## Reproduction and trust boundary

With Python 3.11.2 and the standard library, from the repository root:

```bash
python3 -B hadwiger_nelson_moser_terminal_connector/build.py --out /tmp/hn-moser-ports
python3 -B hadwiger_nelson_moser_terminal_connector/verify.py --work /tmp/hn-moser-ports
python3 -B hadwiger_nelson_long_terminal_gluing/build.py --out /tmp/hn-positive-ports
python3 -B hadwiger_nelson_long_terminal_gluing/verify.py --work /tmp/hn-positive-ports
```

Both output directories must be new; assertions must be enabled. The first
two commands verify the connector theorem. The last two replay the imported
positive gadget extensions, including their exact coordinate reconstruction.
The B214 portion of that older audit is not needed by this result.
[Expected counts](expected.json), [validation and input hashes](validation.json),
and [file hashes](SHA256SUMS) accompany the source. Generated point boxes,
graphs and operational files remain outside Git.

Optional witness rediscovery requires `python-sat==1.8.dev24` with CaDiCaL
1.9.5:

```bash
python -B hadwiger_nelson_moser_terminal_connector/discover.py --out /tmp/hn-moser-witness
```

It uses 756 Boolean variables and 2,791 clauses: exactly one of four colours
per cluster, unequal colours across conservative edges, and four clauses
forbidding each cluster triple from being monochromatic. The single call is
capped at 100,000 conflicts. A SAT model is decoded and directly checked.
UNSAT or UNKNOWN would not prove a geometric obstruction, since the graph
is conservative. A public-entry-point replay reproduced the certificate
byte for byte. The one original exact query and its one validation replay
were SAT; the earlier floating prototype made one separate heuristic query.
Proof replay needs no solver and no negative certificate.

Generation takes about 0.36 seconds and the rational all-pairs audit about
16 seconds, using one thread; peak memory was not measured. The checker
also passes 17 arithmetic boundary controls, four malformed-colour or alias
rejection controls, and the seven exact all-contact fixture identities.
The inherited extension replay checks all 60 relevant A terminal assignments
on all 646 internal edges (38,760 colour inequalities).

Trust remains in the analytic circle-intersection and gluing arguments,
faithful transcription of the fixed coordinates and archived A, integer
and rational arithmetic including `isqrt`, complete finite loops, and
certificate decoding. There is no floating-point predicate, large omitted
proof trace, SAT soundness premise, or claimed algebraic-identity census.
The distinct checker is author-run; external review of this new theorem is
pending.

## Decision and shared context

This fixed connector and contact class admits one colouring for every
candidate simultaneously. Enumerating triples from it cannot supply the
required contradiction. This bounded milestone is complete.

A concrete next direction, **unstarted**, is the separate placement class
where each of the three terminals has one spindle contact and none has two.
Its coverage needs a new geometric derivation; no enumeration or assertion
about it is included here. Alternatively, interior contacts would require
constructing and checking full gadgets. Neither next phase is started by
this package.

HN-2's [37-clause H514 path projection](../hadwiger_nelson_heule514_path_projection/README.md)
is a separate exact-certification frontier; its 258,914 residual graphs
remain unresolved in the inspected durable handoff. The newly
[accepted review of the 483-point heptagon sum](../hadwiger_nelson_heptagon_two_triangle_sum_review1/README.md)
confirms the older fixed family and does not reopen it. Neither result is a
premise for this connector theorem. The parked Parts overlap, H574 and
centered heptagon construction families are not re-enumerated.

Primary-source calibration on 2026-09-06: Parts'
[paper, Table 1](https://arxiv.org/html/2010.12665v2) supplies the gadget context
and the 509-vertex record; [Haugland's current manuscript](https://arxiv.org/html/2608.04542v4)
also reports 509. No graph improving that record has been established here.
