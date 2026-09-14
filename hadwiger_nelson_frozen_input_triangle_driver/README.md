# Four frozen input vertices do not strengthen the coupler relation

The fixed construction here has **120 distinct plane points and 313 strict
unit edges**, with chromatic number **exactly four**. Four original input
vertices of the sixteen-point opposed-palette coupler are frozen: in every
proper four-colouring, each sees all three other colours among its neighbours.
Nevertheless, **every four-colouring of the original sixteen vertices extends**.
The full eight-terminal relation remains 2691 allowed and 104 forbidden
patterns out of 2795.

This was an explicit input driver with a declared total budget of 120 points.
It fails the required relation-strengthening gate and is retired. It gives
no five-chromatic graph, record improvement, or global exclusion of other
physical drivers. It makes no priority claim for the standard clique-gluing
argument below.

## Fixed geometry and budget

Let `G` be the exact
[opposed-palette source](../hadwiger_nelson_opposed_palette_cells/README.md),
mathematical commit `169a7bb32bd0cb28e992773199bea21d6c6f3c50`. Its original
point order is

```text
0,...,15 = A,B,D,C,E,X+,X-,Y+,Y-,-D,-C,-E,-X+,-X-,-Y+,-Y-
T = (5,6,7,8,12,13,14,15).
```

The coordinates are

\[
A=-\tfrac12,\ B=\tfrac12,\ D=\tfrac34+\tfrac{i\sqrt{15}}4,\
C=\tfrac{i(\sqrt{15}+\sqrt7)}4,\ E=-\tfrac34+\tfrac{i\sqrt{15}}4,
\]

\[
X_\pm=(D+C\pm i\sqrt3(C-D))/2,\qquad
Y_\pm=(E+A\pm i\sqrt3(A-E))/2.
\]

Let `F` be the 29-point, 75-edge
[F29 frozen-centre source](../hadwiger_nelson_frozen_centre_transfer/README.md),
mathematical commit `ef05942eeebba29628dc02f37a5792ac7d4122b8`. Its labels
`(0,28,25)` form the ordered unit triangle `(0,1,omega)`, where
`omega=(1+i sqrt3)/2`. If the centre is deleted, its fourteen marked neighbours
still cannot all use two colours in a proper four-colouring. Hence the centre
sees exactly three colours in every proper four-colouring of `F`.

The source coordinates are included literally in
[source_points.json](source_points.json). A coupler row consists of its eight
real and eight imaginary coefficients in
`(1,sqrt3,sqrt5,sqrt7,sqrt15,sqrt21,sqrt35,sqrt105)`, divided by 8. An F29 row
`(a,b,c,d)` denotes `(a+b sqrt33+i(c sqrt3+d sqrt11))/12`.
These exact coordinates define both sources without an external dataset.
The controls also reconstruct F29 from its original 43-point Polymath16
seven-coset pool and check every selected row.

Freeze the four ordered attachment triangles

```text
(t,a,b) = (5,2,3), (7,4,0), (12,9,10), (14,11,1).
```

For each triangle, use the single isometry

\[
\phi_{t,a,b}(z)=g_t+(g_a-g_t)z.
\]

The multiplier has norm one. Exact arithmetic checks
`phi(0)=g_t`, `phi(1)=g_a`, and `phi(omega)=g_b` in all four cases. The ordered
triangles therefore require no reflection or additional choice of phase.
Define `H` as the set union of `G` and these four images of `F`, including
**every** unit-distance edge after merging equal physical points.

Each source image already shares at least its three attachment points with
`G`, so the declared bound was

\[
|H|\le16+4(29-3)=120<509.
\]

The exact reconstruction attains this bound. Each image meets `G` in exactly
its three named triangle vertices. The four image sets are pairwise disjoint.
There are no additional unit edges outside the union of the five constituent
graphs. Since the four attachment triangles are disjoint, the edge count is
`25+4*(75-3)=313`.

This is a fixed combination of two demonstrated physical relation sources.
It is distinct from the retired 44-point common-neighbour pool and from the
earlier reflected-neighbour-chord pair test. It attaches sources to one member
of each of the four terminal pairs, not to both reflected ends of a pair.
No orientation search, extra copies, completion iteration or later host
enlargement is included.

## Universal extension and frozen inputs

Fix any proper four-colouring `c` of `G`. Also fix the proper four-colouring
`f` of F29 saved in [certificate.json](certificate.json). The three colours
on a unit triangle are distinct. There is therefore a unique permutation
of the four colour names carrying

```text
(f(0), f(28), f(25)) to (c(t), c(a), c(b)).
```

Use the permuted F29 colouring on the corresponding image. It agrees with
`c` at every shared point. The images have no other overlaps or cross edges,
so these four choices together extend `c` to a proper four-colouring of `H`.
Conversely, restricting an `H` colouring gives a `G` colouring.

Thus restriction is surjective on **all** original four-colourings, not just
one witness per terminal pattern. Every partial colour prescription on the
sixteen old points has the same feasibility before and after attachment.

At the same time, each image contains the entire F29 source. In every
four-colouring its centre sees the other three colours. Thus the original
terminals `5,7,12,14` really are frozen when all other vertex colours are held
fixed. This local property imposes no additional joint colour relation here.
The construction therefore supplies a concrete counterexample to treating
frozen inputs alone as a sufficient palette-amplification mechanism.

The F29 palette premise rules out a three-colouring of any source image:
its neighbours would then use at most two colours. The explicit extension
word supplies a four-colouring of `H`, so `chi(H)=4`.

For completeness, the checker also classifies the entire eight-terminal
relation. For a four-terminal word `w`, set `P={w0,w1}` and `Q={w2,w3}`.
The ordered colours `(a,b)` of a cell's shared edge are permitted exactly if
`a!=b`, `a` is outside `Q`, and some `d,c,e` satisfy

```text
d,c outside P; e outside Q; d!=c; c!=e; e!=a; d!=b.
```

Those constraints are precisely the original thirteen single-cell edges.
Intersect the first cell's endpoint relation with the transpose of the
second's. The checker produces a full original colouring for each of the
2691 permitted terminal patterns, extends it by the colour permutations,
and checks all 313 physical edges. The 104 forbidden patterns remain forbidden
by restriction to the original graph. No input bichromaticity or palette
repetition is assumed.

## Reproduction and trust boundary

Python **3.11.2**, standard library only. From the repository root:

```sh
python3 -B hadwiger_nelson_frozen_input_triangle_driver/verify.py --check-expected
python3 -O -B hadwiger_nelson_frozen_input_triangle_driver/verify.py --check-expected
python3 -B hadwiger_nelson_frozen_input_triangle_driver/controls.py
```

From this directory, run `sha256sum -c SHA256SUMS` for source integrity.
The package needs no sibling imports, SAT binary, network or omitted large
artifact. [expected.json](expected.json) includes the point, edge, map and
word-stream hashes and one full 120-letter four-colouring.

Coordinates of `H` have common denominator 96. Each axis lies in
`Q(sqrt3,sqrt5,sqrt7,sqrt11)`. The sixteen basis radicals are indexed by
prime-subset masks. Multiplication is
`sqrt(r_i)*sqrt(r_j)=r_(i&j)*sqrt(r_(i xor j))`. Their rational independence
gives exact coordinate equality and an exact all-pairs unit-distance test.
All 7,140 pairs are checked; no floating equality or numerical tolerance is
used.

The small F29 palette premise is rechecked by a complete, unsymmetrized search
on the centre-deleted graph, giving 39 nodes and 20 conflicts when its fourteen
neighbours are restricted to colours 0 and 1. Colour relabelling covers every
at-most-two-colour palette. The supplied positive F29 word is checked directly.
The main verifier then validates 2691 full composite words, totalling 842,283
edge inequalities.

Author controls reconstruct the F29 source from its cosets, compare every
one of the 7,140 complete norm coefficient vectors with a separate gcd-based
radical implementation, and normalize all `4^8` named terminal assignments.
A direct finite domain search on the full 120-point graph, without using
triangle gluing or cell elimination, independently obtains the same 2691/104
relation and validates its positive words. Seven corrupted certificates are
rejected. Normal and optimized runs agree; details are in
[VALIDATION.json](VALIDATION.json).

The trust base is the explicit exact coordinates, elementary colour-permutation
argument, finite domain-search implementation, and Python integer arithmetic.
This package is author evidence, not an independent-author review or a formal
proof-assistant result. The earlier coupler relation has a separate
[independent acceptance report](../hadwiger_nelson_opposed_palette_cells_review1/README.md);
that verdict does not automatically extend to this construction.

## Consequence for construction selection

The named driver is retired at its complete neutral-relation gate. A successor
must provide a genuine interaction beyond compatible triangle attachments,
with its own exact geometry, full-relation test and complete at-most-508 point
budget. Merely adding more independently compatible frozen-centre sources
cannot repair this mechanism. No successor geometry is supplied here, and
the coupler remains dormant pending one.

The frozen-centre idea and the seven-coset source originate in Polymath16;
related context is Frankl, Hubai and Pálvölgyi,
[Almost-Monochromatic Sets and the Chromatic Number of the Plane](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2020.47).
This package claims no new smallest source or historical priority. A bounded
primary-source refresh on 2026-09-14 still supports
[Parts' 509-point record](https://arxiv.org/abs/2010.12665), also identified in
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4). The present
negative driver result does not change that record comparison.
