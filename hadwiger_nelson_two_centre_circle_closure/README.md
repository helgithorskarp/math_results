# Two-centre unit-circle constructions are four-colourable

**Theorem.** For arbitrary points a,b in the Euclidean plane, let

```text
C(a)={x: |x-a|=1},
X(a,b)={a,b} union C(a) union C(b).
```

The strict unit-distance graph on the **entire set X(a,b)** is
four-colourable. If a and b are distinct, **every prescribed pair of
different colours at a,b extends** to a proper four-colouring of X(a,b).
There is no restriction on their separation, the number of selected circle
points, or the cross-circle unit edges.

Consequently, every Euclidean unit-distance graph with a dominating set
of at most two vertices is four-colourable, and a dominating pair cannot
be forced monochromatic in all four-colourings. Every five-chromatic
unit-distance graph therefore has domination number at least three.
The bound of four colours for this family is sharp: the classical
seven-vertex Moser spindle has a dominating pair and is four-chromatic.

This is a complete construction-family exclusion, not a graph below the
509-vertex record. It changes the mechanism from the retired fixed
Moser/Parts attachment line to arbitrary two-centre geometry. No Parts
gadget, fixed support, residue colouring, SAT result or earlier extension
theorem is a premise.

## Definitions and use in construction

Distances are **exactly one**, not at most one. This is a unit-distance
statement, not a unit-disk graph statement. All vertices in an embedding
are distinct. A set D dominates a graph if every vertex outside D has
a neighbour in D. If D={a,b} dominates a unit-distance graph G, every
embedded vertex is a centre or lies on one of these two unit circles.
Thus the theorem colours G by restriction, even when G omits some unit
edges. A singleton dominating set is handled by the one-centre case below.

The theorem permits arbitrary additional unit edges among all selected
points, circle intersections, and a centre lying on the other circle.
It also covers configurations with arbitrarily many points. A finite
search confined to two closed unit neighbourhoods cannot find the target,
and cannot produce an equality gadget whose designated pair dominates it.
It makes no assertion for three centres, arbitrary circle radii, or a
configuration with points outside the two neighbourhoods.

## The six-cycle geometry

Let R be rotation by pi/3 around a. Two points of C(a) are at unit distance
exactly when one is R or R-inverse applied to the other: their angular
difference is pi/3 or minus pi/3 modulo 2pi. Every R-orbit has exactly six
points, and its complete unit graph is C6. Different orbits have no unit
edges on the same circle.

It follows that the whole unit circle is two-colourable, independently on
each six-cycle. This can be made explicit without selecting arbitrary
orbit representatives: for angle theta in `[0,2*pi)`, the parity of
`floor(3*theta/pi)` is a proper binary colouring. Half-open sectors handle
their boundary points. Flipping all colours on a whole six-point orbit
preserves propriety.

Two specified points in one orbit can receive the same binary colour
exactly when they differ by an even number of rotation steps. Points in
different orbits can always be made the same colour by independent flips.
In particular, at most two orbit flips suffice to make two compatible
points both colour 0.

Write d=|a-b|. When the two distinct unit circles intersect in distinct
points p,q, elementary circle geometry gives

```text
|p-q|^2 = 4-d^2.
```

For points of one six-cycle, the exact possibilities are:

| Rotation steps j | Parity | Chord squared | Corresponding d squared |
|---:|---|---:|---:|
| 0 | even | 0 | 4 |
| 1 | odd | 1 | 3 |
| 2 | even | 3 | 1 |
| 3 | odd | 4 | 0 |
| 4 | even | 3 | 1 |
| 5 | odd | 1 | 3 |

Therefore, for **distinct centres**, the only separation at which p,q
cannot be made monochromatic in a binary colouring of C(a) is **sqrt3**.
The odd three-step case would require d=0, when the circles coincide and
the two-intersection discussion does not apply. Tangency has only one
common point and creates no compatibility obstruction.

## All nonexceptional separations

If a=b, colour C(a) with two colours and a with a third. Now assume a,b
are distinct and d is not sqrt3. Let I=C(a) intersection C(b). It is
empty, a singleton, or a pair compatible with a binary colouring of C(a).
Choose a proper colouring of C(a) in colours 0,1 with every point of I
in colour 0. If I is empty there is no constraint.

Colour `C(b) minus C(a)` in colours 2,3 by restricting any binary colouring
of the full circle C(b). This colours every circle point exactly once.
All edges within C(a) are proper; all edges within `C(b) minus C(a)` are
proper; and edges between these two sets have disjoint palettes. This
includes edges from a common point, which belongs to C(a).

If b does not lie on C(a), give b colour 1. Its neighbours on C(a) are
exactly I, all in colour 0, and its remaining circle neighbours have
colours 2,3. If b lies on C(a), then d=1. The two common points are the
equilateral completions of segment ab, each one rotation step from b
around a. Hence the chosen colouring already assigns b colour 1.

If a does not lie on C(b), give a colour 2. Its neighbours on the other
circle are precisely I and already have colour 0, while its own circle
uses 0,1. If a lies on C(b), then d=1 and it belongs to
`C(b) minus C(a)`; retain its existing colour 2 or3. Every neighbour of a
is on C(a), so either colour is safe.

The two centres have different colours. If they are adjacent, d=1 and
the preceding assignments already handle their edge. This proves the
claim for every nonexceptional separation, including disjoint circles
d>2, tangent circles d=2, and intersecting circles with d=1. A global
permutation of four colour names gives any prescribed distinct colours
on the centres.

## The exceptional separation sqrt3

By an isometry take `a=(0,0)` and `b=(sqrt3,0)`. For compactness write

```text
[s,t] = (s*sqrt3/2,t/2).
```

The common points are p=[1,1] and q=[1,-1], at unit distance. Take the
six-cycle A obtained from p by successive pi/3 rotations around a:

```text
A=([1,1],[0,2],[-1,1],[-1,-1],[0,-2],[1,-1]).
B=A+[2,0].
```

B is a six-cycle on C(b), also containing p,q. The two cycles share
exactly their edge pq. Let `P={a,b} union A union B`. It consists of the
following twelve distinct points. The displayed four-colouring pins
a to 2 and b to 0.

| Index | [s,t] | Colour |
|---:|---|---:|
| 0 | [0,0] | 2 |
| 1 | [2,0] | 0 |
| 2 | [1,1] | 1 |
| 3 | [0,2] | 0 |
| 4 | [-1,1] | 1 |
| 5 | [-1,-1] | 0 |
| 6 | [0,-2] | 1 |
| 7 | [1,-1] | 3 |
| 8 | [3,1] | 1 |
| 9 | [2,2] | 2 |
| 10 | [2,-2] | 1 |
| 11 | [3,-1] | 2 |

All 66 pair distances give exactly23 unit edges, and the displayed
colouring is proper on all of them. This is two six-rim wheels sharing
one rim edge, but the complete distance check also rules out overlooked
unit edges.

The crucial additional fact is that every unit neighbour of a point of
A or B on either circle lies in A union B. Same-circle neighbours are
already the two rotation neighbours. For x in A, its squared distance
to b is 1, 4, or 7. The corresponding unit circles centred at x and b have
exactly two, one, or zero common points respectively. The following table
gives all their intersections, in the indices above:

| x in A | Distance squared to b | Unit neighbours on C(b) |
|---:|---:|---|
| 2 | 1 | 7,9 |
| 3 | 4 | 2 |
| 4 | 7 | none |
| 5 | 7 | none |
| 6 | 4 | 7 |
| 7 | 1 | 2,10 |

Reflecting across the perpendicular bisector of ab gives the analogous
claim for B. The certificate also lists and checks those six cases
explicitly. Distinct unit circles have at most two intersections; at
centre distance two they are tangent; at distance sqrt7>2 they are
disjoint. Thus this positive witness table is a complete continuum
boundary check, not merely a check against the twelve listed vertices.

Keep the displayed colouring of P. Colour every remaining six-cycle of
`C(a) minus A` in 0,1 and every remaining six-cycle of `C(b) minus B` in 2,3.
The two residual sets are disjoint, because the only circle intersections
p,q belong to A and B. Residual same-circle edges are proper, and
residual cross-circle edges have disjoint palettes. There is no edge from
a patch **rim** vertex to a residual circle point by the boundary check.
The centres themselves do have infinitely many rim neighbours: a has
colour 2 and its residual neighbours use0,1; b has colour 0 and its
residual neighbours use2,3. A centre has no residual neighbour on the
other circle, since those neighbours are p,q.

Every unit edge on X(a,b) is now covered. The centre colours differ, and
permuting colours again permits any ordered pair of distinct prescribed
colours. This completes the universal theorem.

## Sharpness and a useful limitation

For sharpness use the classical Moser spindle, with complex coordinates

```text
u=1, v=(1+i*sqrt3)/2, rho=(5+i*sqrt11)/6,
M=[0,u,v,u+v,rho*u,rho*v,rho*(u+v)].
```

Vertices0 and3 dominate this graph and are at distance sqrt3. Its exact
strict unit graph has eleven edges. The colour string0123132 is proper.
In any three-colouring, the diamonds on `{0,1,2,3}` and `{0,4,5,6}` force
vertices 0,3,6 to have the same colour. The unit edge 3–6 contradicts this.
Hence the example is four-chromatic and the universal upper bound is sharp.
The code also refutes all 2187 labelled three-colour assignments directly.
This familiar example is a control, not a new graph or a resumed fixed
Moser attachment construction.

The theorem guarantees **distinct** prescribed centre colours. It does
not claim that an arbitrary same-colour prescription extends for distinct
nonadjacent centres. No complete classification of that different extension question
is established here. In particular, four-colourability alone must not be
used to assert every prescribed centre pattern.

## Reproducible finite certificate

[build.py](build.py) produces a **1,134-byte** certificate containing the
twelve-point patch and colour row, all twelve directed cross-circle
closure cases, the six orbit chord cases, and the sharpness example.
Its SHA256 is

```text
3287f25e437473da4684cf80982294fa87c7999adfb22e9c2a4b1685ba17b3c2
```

The [separate checker](verify.py) imports no producer or inherited code.
The producer describes the patch in integer triangular coordinates and
uses the quadratic form `3*delta_s^2+delta_t^2`. The checker reconstructs
the hexagons by exact complex rotations over Q(sqrt3), using rational
coefficients, and compares every coordinate, unit edge and closure row.
For the sharpness graph it separately expands squarefree radicals by
gcd reduction. No floating-point equality or external algebra package
is used.

The checker verifies66 patch pair norms, all 23 patch edges, all twelve
circle-completion cases and their twelve intersection witnesses. It
checks all 24 colour permutations, covering all twelve ordered distinct
centre-colour pairs. It derives the six orbit chord values by rotation,
exhausts all 64 binary assignments to C6, reconstructs all 21 sharpness
pair norms, verifies domination and the positive four-colouring, and
refutes all 2187 three-colour assignments. Five malformed certificates
are rejected. These finite checks validate the explicit ingredients;
the proof over arbitrary real separations and all circle points is the
analytic construction above.

From the repository root, with Python 3.11.2 and the standard library:

```bash
python3 -B hadwiger_nelson_two_centre_circle_closure/build.py --out /tmp/hn-two-centres
python3 -B hadwiger_nelson_two_centre_circle_closure/verify.py --work /tmp/hn-two-centres
```

The build output directory must be new. Normal and optimized checker
executions give identical results. [expected.json](expected.json),
[validation.json](validation.json) and [SHA256SUMS](SHA256SUMS) preserve
the checks and provenance. Generation takes about 0.001 seconds and the
independent audit 0.06 seconds on one thread. Peak memory was not measured.
There are zero native solver calls and no omitted large proof artifact,
placement census or background job.

The trust boundary is elementary circle geometry, the explicit colouring
argument, exact coordinate transcription and squarefree-basis independence,
Python integer/Fraction semantics, complete finite loops and certificate
parsing. There is no imported chromatic theorem, negative solver trace
or assumption about the colourings of a large gadget. The independent
implementation is author-run; external review and formalization of this
new family proof are not claimed.

## Literature and campaign boundary

This is a construction-family result within the named Hadwiger–Nelson
record problem. Targeted searches for two-circle and domination formulations
found related primary work: Guldan's [1991 paper](https://www.dml.cz/bitstream/handle/10338.dmlcz/126170/MathBohem_116-1991-3_8.pdf)
studies colourings of two unit-circle arcs, and Voronov's
[bicycle theorem](https://arxiv.org/html/2304.10163) concerns a positive
interval of forbidden distances. Neither is used as a premise here;
the latter constraint differs from forbidding exactly distance one.
No priority claim for the two-centre formulation is made on the strength
of these targeted searches.

The current primary [Parts paper](https://arxiv.org/html/2010.12665v2)
and [Haugland manuscript](https://arxiv.org/html/2608.04542v4) still report
the 509-vertex record, checked 2026-09-06. This result does not improve it.

The [previous terminal-only family](../hadwiger_nelson_moser_terminal_coincidences/README.md)
is preserved. The coordination brief explicitly retired further interior
variants of that fixed gadget/connector line, so its proposed interior
alignment was left unstarted. The two-centre theorem has no dependency
on that line. HN2's new [complete H514 closure](../hadwiger_nelson_heule514_whole_decision/README.md),
read in the prepublication repository refresh, proves every subgraph of
that support on at most 508 vertices four-colourable. Its direct proof uses
503 mandatory vertices and 462 omission cases. H514 deletion-only work is
finished. The result remains separate and supplies no premise here.

This completes the new two-centre mechanism. Any further circle-based
construction must use points beyond two closed unit neighbourhoods;
three-centre compatibility is one unstarted possibility. No third-centre
configuration, radius ladder or new construction phase begins in this pass.
