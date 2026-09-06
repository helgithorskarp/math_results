# Geometric overlap of finite forcing gadgets

This package constructs an explicit five-chromatic Euclidean unit-distance
seed from overlapping copies of the [375-vertex small-triangle forcer](../hadwiger_nelson_small_triangle_forcer375/README.md).
It follows the Exoo–Ismailescu implication chain, with exact geometric overlap
and a bounded reduction of the equal-pair component. The result has **953 vertices
and 4,917 unit edges**, and chromatic number **exactly five**. The certificate
also proves that **every subgraph on at most 508 vertices is four-colourable**.
This seed is therefore closed for the target by deletion alone; it does not
improve the 509-vertex record. No smallest-gadget, minimality, or method-priority claim is
made.

## Mechanism

The earlier component T375 forbids its marked triangle of side 1/sqrt(3)
from being monochromatic. It itself has a proper four-colouring. The supplied certificate includes 11 proper four-colourings whose combined colour words
separate all 375 vertices: no distinct pair in T375 is always monochromatic.
Thus a direct equal-pair spindle cannot be obtained from T375 without
additional geometry.

Attach T375 to the 18 small triangles of the paper's G49. Exact coordinate
deduplication gives 2,536 points and 13,278 inherited unit edges. A single
selector-core and deletion pass gives I450, with 450 vertices and 2,290 unit
edges when all exact unit pairs are included. Every proper four-colouring
assigns different colours to its marked endpoints at distance sqrt(11/3).
A separate four-colouring proves the component is colourable. An exhaustive
checker proves the contrary endpoint query impossible in 1,485 nodes.

The paper's G40 has 40 points and 82 unit edges. Requiring its 59 pairs at
distance sqrt(11/3) to be bichromatic forces two marked endpoints at distance
8/3 to have the same colour. One constraint deletion pass retained 54 long
pairs. An exhaustive independent check of these 82+54 inequality constraints
rejects distinct endpoint colours in 72 nodes. These 54 constraints are
not unit edges: the copies of I450 realize them.

For each retained long pair, place I450 in each of the four possible ordered
endpoint/reflection frames and choose the frame with maximum overlap with
the accumulated support. Ties use the fixed enumeration order. This gives
9,581 vertices and 62,482 inherited unit edges, replacing the disjoint-copy
upper bound 40+54*(450-2)=24,232. There are 79,034 unit pairs in its full induced
graph. The component reduction uses inherited edges; extra geometric edges
are added when the final support is constructed. No omitted unit pair can
invalidate an obstruction proved with the inherited subgraph.

A selector-core reduction of the inherited-edge union was frozen after
1,193 decisions, giving **E477**. Its complete unit-distance graph has 477
vertices and 2,458 edges. It admits a proper four-colouring and forces its
marked endpoints O,V, at distance 8/3, to have the same colour. Its exhaustive
forcing proof visits **1,382,032 nodes**, with **691,060 conflicts**.

The spindle of two copies of E477 has 953 vertices and 4,917 unit edges.
There is exactly one cross edge, V to its rotated image, outside their shared
origin. This yields a direct five-colouring and the endpoint contradiction.
The geometric single-bridge structure supplied a sharper stopping criterion
than completing an optional minimality search: the target is excluded as
soon as every forcing half needs at least 255 vertices.

`mandatory_vertices.json` supplies **253 distinct nonterminal deletions** of
E477, each with a proper four-colouring assigning O colour 0 and V colour 1.
Any subgraph of E477 still forcing O,V equal must contain all 253 of those
vertices, plus O,V. Its order is therefore at least 255. The theorem below
then gives a lower bound of **509** on any non-four-colourable subgraph of
the full 953-vertex spindle. This is a bound for this support, not for arbitrary
Euclidean unit-distance graphs. No minimum order or criticality of E477 is
asserted.

## Coordinates and exactness

Each four-integer row [a,b,c,d], with the positive integer denominator D in
the certificate, denotes

    ((a sqrt(3)+b sqrt(11))/(36 D), (c+d sqrt(33))/(36 D)).

For a difference row, squared distance one is equivalent to

    3a^2+11b^2+c^2+33d^2 = 1296 D^2,
    ab+cd = 0.

The first sum has nonnegative terms, so it bounds each integer coefficient.
`lattice.py` enumerates all possible differences exactly; for D=1 there are
54 oriented unit vectors. This gives a complete edge generator by dictionary
lookup, without checking every pair.

Rotate a second copy of the equal-pair gadget about its endpoint O=0 by R,
where cos(R)=119/128 and sin(R)=3sqrt(247)/128. These values have squared sum
one, and the endpoints V,RV at radius 8/3 are unit distance apart because
2*(8/3)^2*(1-119/128)=1. The two gadgets force V and RV to have O's colour,
contradicting that unit edge. The two copies intersect only at O: the base
coordinates lie in F=Q(sqrt(3),sqrt(11)), and independence of sqrt(247) over F
forces any point in both copies to be zero.

For a cross pair p,Rq with p,q in F^2, unit distance implies det(p,q)=0 by the
same independence. Its remaining equation is

    |p|^2 + |q|^2 - (119/64) p dot q = 1.

`graph.py` expands these equalities in the two-dimensional coefficient spaces
and enumerates every cross edge. This calculation does not assume the only
cross edge is VV'.

The verifier imports neither `graph.py` nor `lattice.py`. It embeds each row
in the bit-indexed eight-element radical basis for
Q(sqrt(3),sqrt(11),sqrt(247)) and directly checks every squared distance.
Multiplying every coordinate by 128 keeps this check entirely in integers.
A row prefixed by side 0 is in the first copy; side 1 means apply R. Geometry
therefore uses no floating point or solver result.

## Colour proof and scope

`colour_check.py` and its native implementation `colour_check.cpp` exhaust
proper four-colourings by singleton propagation
and branching on a minimum-domain vertex. At each branch it tries every
already-used colour and one representative unused colour. Unused colour
names are interchangeable because the only constraints are inequalities
and the explicitly given pins. An empty domain rejects a branch; each branch
fixes another vertex; exhausting all branches proves impossibility. For an
equal-pin query the common colour may be fixed to 0. For a different-pin query
the two colours may be fixed to 0 and 1, by global colour permutation.

A supplied five-colouring is checked against every unit edge of the final
graph. It proves the upper chromatic bound; the checked obstruction proves
the lower bound. The written encoding and symmetry arguments, the exact
arithmetic code, and exhaustive search implementation are the trust boundary.
No proof-assistant formalization or external peer review is claimed.

The old 795,753-vertex composition bound remains valid for its own specified
union; this package changes the intermediate components and placements.
HN-2's [complete H560 deletion closure](../hadwiger_nelson_heule560_target508_review1/README.md)
is inspected context, not a premise. Its fixed-support search is separate.

## Reproduction

Python 3.11 or later and a GCC-compatible C++17 compiler suffice for the final
proof. Recorded verification versions: CPython 3.11.2 and GCC 12.2.0. From this
directory:

```sh
mkdir -p out
c++ -std=c++17 -O3 -Wall -Wextra -Wpedantic -Wconversion colour_check.cpp -o out/colour-check
python3 verify.py
python3 -O verify.py
python3 controls.py
python3 native_controls.py
python3 replay.py
sha256sum -c SHA256SUMS
```

`verify.py` prints `expected.json`. Ordinary and optimized Python outputs
agree. It reconstructs every pair in I450, E477, and the 953-point spindle,
checks the 253 deletion words, verifies the five-colouring, and exhausts the
contrary endpoint query on E477. The native search has exactly the reference
Python branching and propagation order. It matched both colour words and
search statistics on 5,120 complete small cases, which were also compared
against independent named-colour enumeration. Geometry has eight entry-level
controls and 400 cross-equation controls. Eighteen malformed Python-side
certificates and eight malformed native inputs are rejected.

The native checker matched a 500-point pilot's complete 1,737,376-node
reference search in 6.87 seconds, compared with 171.66 seconds in Python.
The final E477 search took about 5.6 seconds after exact geometry was built.
This is a performance translation, not a claimed new independent proof
algorithm. Address/undefined-behaviour sanitizer runs passed 30 representative
small cases and all eight malformed native inputs. The slow reference remains
available as `python3 verify.py --python`.

`replay.py` rebuilds both overlap unions and checks every retained coordinate
against the compact index lists. It also exhaustively rechecks the G40
54-constraint implication. This optional construction replay needs the sibling
`hadwiger_nelson_small_triangle_forcer375` package for its published coordinate
tables. Final proof verification is self-contained.

The point and unit-edge hashes of the final spindle use compact JSON:

```text
points c79c5c28004b3c4b1a244e46c029f9f658810babb61926c0ac6c98cce07c6d08
edges  8a567add3914071191e7846295676ac9be3f35bdc9f06c65bdc74e0d04c0c275
```

`validation.json` records the controls, complete proof statistics, source
provenance and independent SAT audit. Glucose3 also proved E477's contrary
query UNSAT, and drat-trim independently verified its trace. The audit used
1,908 Boolean variables and 13,173 clauses: one of four colours per vertex,
pairwise at-most-one clauses, four inequality clauses per exact unit edge,
and pins O=0,V=1. This encoding is equivalent to the endpoint query by direct
assignment/colouring conversion. Its CNF SHA-256 is
`926cd9032ce7c6e01261c928e5a19a87a2366c9abe580ef4677341a3942ec840`.
The 46,746,711-byte DRAT trace remains outside the repository; it is not needed
for the exhaustive proof. To regenerate this additional audit:

```sh
python3 -m pip install python-sat==1.9.dev15
python3 drat_audit.py --checker /path/to/drat-trim
```

The recorded checker is [drat-trim](https://github.com/marijnheule/drat-trim)
at commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Solver proof generation and
checking took about 41 seconds together. No unchecked SAT UNSAT outcome is a
premise of the final theorem, and the mandatory-vertex bound relies solely on
the directly verified positive words.

Optional `search.py` repeats discovery with `python-sat==1.9.dev15`, bundled
Glucose3 and CaDiCaL 1.9.5 (recorded discovery interpreter Python 3.12.14).
I450 took one complete reduction pass, about 56 seconds. The E477 reduction
stops after the recorded 1,193 decisions, about 2,378 seconds; this is a
reconstruction checkpoint, not a completeness or minimality claim. The target
census reused 132 valid deletion words, then obtained 121 more from 125 queries
in about 370 seconds. Three UNSAT outcomes and one UNKNOWN were unused.
Each new positive word is checked directly. It stops at 253 words, proving
exactly the required target exclusion. Running `python3 search.py` writes all
raw history under ignored `out/`; the exact-coordinate and proof certificates
above do not rely on the search path.

Source context: [Exoo and Ismailescu, arXiv:1805.00157v1](https://arxiv.org/abs/1805.00157v1).
The standing vertex record comparison is
[Parts, arXiv:2010.12665](https://arxiv.org/abs/2010.12665), also stated in
[Haugland, arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4), checked on
2026-09-06. This package is a constructive research seed, not a record claim.

## Exact reduction for every subgraph of a single-bridge spindle

Suppose A and B each admit a proper four-colouring, share exactly O, and the
only edge between their other vertices is XY, with X in A\{O} and Y in B\{O}. For
any induced subgraph H containing O,X,Y, H is not four-colourable if and only
if its A part forces O and X equal and its B part forces O and Y equal.
If any of O,X,Y is absent, H is four-colourable.

The forward implication follows by contrapositive: if one part admits
unequal endpoint colours, permute colour names in each part, fixing O's
colour, so that X and Y receive different colours. If O is absent the parts
can be permuted independently; if X or Y is absent there is no cross edge.
The reverse implication is the endpoint contradiction. Every such spindle
is at most five-chromatic: combine proper four-colourings with matching O,
then, if needed, give Y a fifth colour.

Consequently the minimum order of a non-four-colourable induced subgraph is
mu(A)+mu(B)-1, where mu is the minimum size of a terminal-containing subgraph
forcing equal terminal colours. If no forcing support exists, set mu to infinity; the spindle then has no
non-four-colourable subgraph. In the symmetric finite case the minimum is
2*mu(A)-1.
A target of at most 508 therefore requires mu(A)<=254 for this mechanism.
The statement is conditional on the complete single-cross-edge hypothesis;
additional cross edges change the decision problem. It is a general
spindle argument, not a claimed new principle.

The full coordinate support in this package is checked to meet that
hypothesis. The target exclusion therefore checks deletion colourings on one half with
all exact unit edges. This is the exact reduction of the unconditional
colouring query above. The non-four-colourability proof checks one half's
endpoint constraint and the unit bridge; the five-colouring is checked on
every unit edge of the entire spindle.
