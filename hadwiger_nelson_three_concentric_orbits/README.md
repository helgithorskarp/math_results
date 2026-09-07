# Three concentric regular orbits through the 508-vertex budget

Every full unit-distance graph on at most three concentric regular `n`-gons,
with distinct positive radii and arbitrary relative phases, is four-colourable
when its total order is at most 508. The common centre may also be included.
Every subgraph of such a host is consequently four-colourable.

This is an exact computer-assisted exclusion of a continuous geometric family,
not a search over a list of previously published graphs. The finite reduction
below and outward-rounded integer computation cover all radii and phases.
No five-chromatic graph was found, and no improved record is claimed.

The common polygon order is essential. Four or more circles, unequal polygon
orders, multiple distinct rotation orbits on the same circle, and partial
selections from larger hosts are not classified. In particular, this is not
a theorem about arbitrary point sets on three circles.

## Precise statement and scope

For `h` distinct positive radii `r_t` and phases `phi_t`, define

```
P_t = { r_t exp(i(phi_t + 2 pi v/n)) : v = 0,...,n-1 }.
```

Join every pair of distinct points at distance exactly one. The calculation
proves four-colourability of `P_0 union ... union P_(h-1) union {0}` for:

* `h <= 1`, every positive integer `n`, by an elementary argument;
* `h = 2`, every `n <= 254`;
* `h = 3`, every `n <= 169`.

The two-ring calculation includes a slightly stronger endpoint with 509
vertices. Thus both the cases with the centre and those without it cover
every host of the stated form of order at most 508. The cases `n=1,2` are
covered by the elementary argument, since at most one radius then supports
an internal unit edge. Distinct radii ensure all labelled polygon vertices
and the centre are different points.

The largest evaluated three-ring order is `3*169+1=508`. It contributes no
surviving case after the necessary degree tests. The largest orders among
the emitted graphs are `3*168+1=505` and `2*252+1=505`; this does not mean
that the larger polygon orders were omitted.

## Finite geometric reduction

**Elementary colouring case.** A point on a positive concentric circle has
at most two unit neighbours on any other circle, and its own circle has
maximum unit degree two. Suppose at most one of the occupied circles has
internal unit edges. Call that circle `A` (choose any occupied circle if
none does). Colour its finite degree-two graph with colours 0,1,2. Colour
an independent circle `B` entirely with colour 3. On the remaining
independent circle `C`, each vertex can choose a colour in 0,1,2 avoiding
its at most two neighbours on `A`. All edges to `B` are then proper.
If the centre is adjacent to `B`, give it colour 0; otherwise give it colour
3. It meets at most one occupied circle, the one of radius one. The same
argument with absent circles removed handles one or two circles.

**Internal radii.** A regular `n`-gon has an internal unit edge exactly when

```
r = r_k = 1/(2 sin(pi k/n)),   1 <= k <= floor(n/2).
```

The internal offsets are `+k,-k`, with only one neighbour if `2k=n`.
These radii are distinct. Radius one is among them exactly when `6` divides
`n`, at `k=n/6`. The centre is adjacent to precisely that ring, if present.

**Degree reduction.** All vertices of a ring have equal degree. If this
degree is at most three, delete the entire ring, colour the smaller-circle
case, and insert its vertices in any order. Each sees at most three
already coloured neighbours. Inductively it suffices to handle graphs in
which every ring has degree at least four. For two rings the smaller case
is elementary; for three rings the two-ring calculation has already been
covered. A disconnected graph of inter-ring contacts likewise reduces to
smaller-circle cases. The common centre meets only one ring and causes
no difficulty when palettes are reused across components.

**Two rings.** After the elementary case, both radii are in the finite
list `r_k`. If there are any cross edges, rotate the whole graph and
relabel the second polygon so that its representative has unit distance
from the representative of the first. Its phase is one of the two
solutions of the law of cosines. This is the complete two-ring loop in
`enumerate.cpp`. The case without cross edges is elementary to combine.

**Three fixed radii.** If each radius either is one of the `r_k` or equals
one, the radii range over a finite set. The remaining inter-ring graph is
connected, so it has a two-edge spanning tree. Choose its middle ring and
rotate its representative to phase zero. Each other representative can be
chosen to have unit distance from it and has at most two possible phases.
The enumeration tries all three choices of middle ring and both phase
signs on each edge, then retains every possible additional unit contact.
There are at least two internal rings; the elementary case covers the rest.

**One unfixed radius.** Otherwise exactly two rings `A,B` are internal,
with distinct fixed radii `r_a,r_b`, and the third ring `C` has no internal
edges and radius `s != 1`. Its degree is at most four. A surviving case
must therefore give each vertex of `C` two neighbours on each other ring.
If two regular `n`-gons have two contacts per vertex, their contact angles
are opposite and differ by an integer multiple of `2 pi/n`. Thus, after
relabeling,

```
phi_A = 0,  phi_C = m pi/n,  1 <= m <= n-1,
s = r_a cos(m pi/n) +/- sqrt(1-r_a^2 sin^2(m pi/n)).
```

Only positive real roots are relevant. Two contacts from `C` to `B`
likewise require an angle `j pi/n`, where `j` is neither 0 nor `n` modulo
`2n`. The phase of `B` can be chosen as `(m+j) pi/n`. The exact cross
offsets, with ring order `A,B,C`, are

```
A to C: {0,-m} modulo n;    B to C: {0,j} modulo n.
```

Every possible `A`-to-`B` contact is retained as well. When `r_a=1`, the
quadratic roots are zero and `2 cos(m pi/n)`; only the latter for `2m<n`
can be positive. This identity removes the exact zero boundary. In other
cases an interval straddling zero would stop the computation with an
error; none occurred. A negative discriminant is discarded only when
its entire enclosure is negative.

This proves completeness of the finite gate for arbitrary real radii and
phases. It also explains why arbitrary angular sampling is unnecessary.
The gate may retain unrealizable configurations, including coincident
radii in the auxiliary unfixed-radius loop. These only enlarge the list
of abstract graphs to colour; actual hosts have distinct radii and
distinct vertices.

## Certified contact enclosures

`tables.py` constructs enclosing rational intervals for all sines and
cosines used in the reduction. It uses no floating-point transcendental
functions. Machin's identity

```
pi = 16 atan(1/5) - 4 atan(1/239)
```

follows from the tangent addition formula and the quadrant of
`4 atan(1/5)-atan(1/239)`. Alternating arctangent sums bound the two terms.
Integer interval Taylor evaluation on `0 <= x <= pi/2 < 2` gives the sine
and cosine tables. The omitted terms are bounded by `2^-110`, since
`2^40/40! < 2^-110`. Evaluation uses scale `2^160`, then rounds outward
to scale `2^48`. Axial sine/cosine values are set to their exact values.

`enumerate.cpp` uses signed 128-bit intermediates and checked rounded
64-bit endpoints, with explicit integer floor and ceiling division.
Square-root endpoints are corrected until their integer squares certify
the result. A floating-point square root supplies only the initial guess.
Invalid division, unresolved positive-radius boundaries and overflow
raise errors instead of producing an exclusion.

For two radii the contact phase is enclosed as

```
q = (r^2+s^2-1)/(2rs),      q +/- i sqrt(1-q^2).
```

Clipping `q` to `[-1,1]` is conditional on a contact existing. A false
branch can add cases, never remove a real contact. Products of these
unit complex phases determine which roots of unity can be contacts.
For a unit phase `z`, a floating `atan2` suggests a grid index `k`.
The integer interval test

```
Re(z conjugate(w_k)) > cos(2 pi/N)
```

certifies that the only grid indices that could occur are within
`{k-1,k,k+1}` modulo `N`. If this test fails, every grid point is tried.
Coordinate interval disjointness can then exclude a point. Consequently
the soundness of contact exclusion does not depend on `atan2`, its
rounding, or choosing a correct nearest index. Controls also use an
intentionally constant-zero proposal and force the fallback path.

Every emitted graph is an upper bound on all contacts of the represented
actual geometry. Four-colouring that graph therefore suffices, without
having to prove that each retained contact is realizable.

## Compact colour certificate and independent check

The full run evaluates **28,057,092** phase/root states. **3,310** survive
the necessary ring-degree test and give **2,841** distinct emitted
graphs. There are **178,774,790** certified root-grid calls; the ordinary
proposal required no fallback on this run. Zero cases remain uncoloured.

The cyclic contact description allows a compact homomorphism. Shift
each ring's indices to make a selected contact spanning tree have offset
zero. Let `g` be the gcd of `n`, all internal offsets, and all shifted
cross offsets. Dividing by `g` identifies isomorphic cyclic components;
the common centre maps to the same centre. Reflection may be used as
well. This reduces the output to **215** colour words, with reduced
polygon orders at most **60**. `certificate.json` is **28,265 bytes**.

`verify.py` does not import the enumerator or the SAT producer. It checks
the words using a literal adjacency predicate, lifts each word to every
vertex of each emitted graph, and tests every same-colour pair again.
The latter check makes an erroneous quotient or lifting formula fail on
the original graph. It verifies **39,739,563** same-colour pairs in
graphs containing **1,907,552** edges in total. These are positive colour
witnesses; no SAT unsatisfiability result is a premise of the exclusion.

The certificate SHA-256 is
`b6ee1443bb2e0a3a8c1927ee61ba73587b1f85f0c964165073147b6bf671abd0`.
The emitted-case SHA-256 is
`7653a66567a18a9f6c15438744b2b923109cff8812f131bf5d831459f052ab70`.

## Reproduction

The proof check needs Python 3.11 or later (standard library) and GCC
with C++17 and `__int128` support. Tested with Python 3.11.2 and GCC 12.2.
Generated tables, executables and case streams stay outside the repository.

```
python3 reproduce.py --work-dir /tmp/hn-three-rings
```

This regenerates the integer tables, compiles and runs the complete
enumeration, checks the committed certificate, and compares the report
with `expected.json`. Expect several minutes for the enumeration.
The compact evidence can be checked against an existing generated stream:

```
python3 verify.py /tmp/hn-three-rings/cases.txt
```

For arithmetic and rejection controls:

```
g++ -O2 -std=c++17 arithmetic_harness.cpp -o /tmp/hn-three-rings/harness
g++ -O2 -std=c++17 -DGATE_ZERO_GUESS arithmetic_harness.cpp -o /tmp/hn-three-rings/zero-harness
python3 controls.py /tmp/hn-three-rings/harness /tmp/hn-three-rings/zero-harness /tmp/hn-three-rings/tables.txt
```

The controls compare **7,506** arithmetic cases with independent Python
`Fraction`/`isqrt` calculations, independently enclose **252** trigonometric
table entries with rational Taylor evaluation, check **97,650** grid cases in each of
two proposal modes, and reject **14** malformed arithmetic/graph/word
inputs. Expected results are in `controls_expected.json`.

A complete replay with undefined-behaviour sanitization produced the identical
100,298-byte case stream. Normal and optimized Python checks agree, and
the certificate was regenerated byte for byte. See `validation.json`.

The optional certificate producer needs `python-sat==1.9.dev15` and
CaDiCaL 1.9.5. Its output is independently checked; the solver is not a
proof dependency. To regenerate it in an external directory:

```
python3 produce_colours.py /tmp/hn-three-rings/cases.txt --output /tmp/hn-three-rings/certificate.json
```

The trust boundary consists of the written finite reduction, the table
generator and integer enumeration, ordinary compiler/runtime correctness,
and the explicit colour checker. This is not a proof-assistant result or
an external peer review. Compact controls validate important operations;
the all-parameter geometric completeness comes from the reduction above.

## Relation to existing work

The source problem is solely the smallest five-chromatic planar
unit-distance graph. Parts reports 509 vertices in
[Graph minimization](https://arxiv.org/abs/2010.12665), and
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4)
still identifies 509 as the overall comparison point. Both were checked
on 2026-09-07. This work does not improve that bound.

Haugland's Proposition 2.1 supplies a useful known geometric example:
three regular heptagonal orbits with unit internal steps 1,2,3 and seven
unit triangles. Its normalized contact graph occurs in this certificate.
An independent exhaustive three-colouring check rejects it in 709
search states, while its four-colour word is verified here. Thus the
four-colour upper bound is sharp within this family. The geometric
identification in this sharpness illustration uses the cited proposition;
the new family exclusion does not depend on it or on the paper's larger
2131-vertex construction and its numerical assertions.

The team's earlier Haugland metric-ball result concerns subsets of one
fixed 2131-vertex graph. The present gate varies all radii and phases of
three concentric regular orbits. The prior Mycielski and spherical-source
transfer gates are not premises, and no retired source was extended.
No priority claim is made for the elementary ingredients or the
heptagonal example. Targeted primary-source and Discovery Net searches
did not locate this complete bounded concentric-orbit classification.
