# The full terminal-circle driver leaves the palette relation unchanged

Adding **every common unit neighbour of every pair of the eight fixed
terminals** of the opposed-palette coupler gives a strict plane unit-distance
graph with **44 distinct points and 85 unit edges**. Every proper four-colouring
of the original sixteen points extends to this graph. Thus this physical input
driver does not strengthen the coupler's relation or supply its missing palette
premise. The graph is exactly three-chromatic.

This closes one explicit construction gate within the 508-point budget. It
does not improve the five-chromatic record, exclude other drivers, or make a
claim about arbitrary unit-distance graphs. The driver and all of its subsets
are retired; no iteration of circle completion is proposed here.

## Exact support

The original [sixteen-point source](../hadwiger_nelson_opposed_palette_cells/README.md)
has mathematical source commit `169a7bb32bd0cb28e992773199bea21d6c6f3c50`.
In complex notation put

\[
 A=-\tfrac12,\quad B=\tfrac12,\quad
 D=\tfrac34+\tfrac{i\sqrt{15}}4,\quad
 C=\tfrac{i(\sqrt{15}+\sqrt7)}4,\quad
 E=-\tfrac34+\tfrac{i\sqrt{15}}4.
\]

Define

\[
 X_\pm=\tfrac12(D+C\pm i\sqrt3(C-D)),\qquad
 Y_\pm=\tfrac12(E+A\pm i\sqrt3(A-E)).
\]

The ordered points of `G` are
`(A,B,D,C,E,X+,X-,Y+,Y-,-D,-C,-E,-X+,-X-,-Y+,-Y-)`.
The terminals have labels `T=(5,6,7,8,12,13,14,15)`. All sixteen coordinates
belong to the real radical basis
`(1,sqrt3,sqrt5,sqrt7,sqrt15,sqrt21,sqrt35,sqrt105)` on each axis.

For every unordered terminal pair `u,v`, set `d=v-u` and `n=|d|^2`.
When `0<n<4`, add both exact points

\[
 z_\pm=\frac{u+v}{2}\ \pm\frac{i d}{2n}\sqrt{n(4-n)},
\]

where the square root is positive. These are precisely the two intersections
of the unit circles about `u` and `v`: the midpoint displacement is
perpendicular to `d`, and its squared length is `(4-n)/4`. The other ten
terminal pairs have `n>4`. No coincident centres or tangencies occur.

There are 18 intersecting pairs and 36 root occurrences. Eight roots are
exactly the eight nonterminal points of `G`, each occurring once. The remaining
28 roots are new and distinct. Consequently the entire arrangement `H` is
`T` together with those 36 roots, and contains `G`. The a priori budget was
`8+2*binomial(8,2)=64`; the collision-merged support costs only 44 points.

Labels `0,...,15` retain the original order. Enumerate terminal pairs in
lexicographic label order, positive root first, and append each new point.
[certificate.json](certificate.json) records all 36 root-to-point assignments,
the full 85-edge graph, and a checked proper three-colouring. These root
formulas and labels specify exact coordinates, including the nested radicals;
there is no imported floating coordinate dataset.

## Neutrality proof

The complete unit graph has the original 25 edges and 60 added edges. The
new 28 points form an independent set. Of these, 24 have exactly two neighbours
in `G` and four have exactly three. The latter neighbour sets are

| New label | Neighbours in the original graph |
|---|---|
| 32 | 1, 7, 15 |
| 33 | 0, 7, 15 |
| 36 | 1, 8, 14 |
| 37 | 0, 8, 14 |

All other new points are adjacent only to their two defining terminal centres.
The four exceptional points come from the two pairs of squared distance `5/2`;
their square root `sqrt(n(4-n))=sqrt15/2` lies in the original radical field.
The four terminal pairs of squared distance `3` give the eight original core
points, using `sqrt(n(4-n))=sqrt3`.

Now fix **any** proper four-colouring of all sixteen original vertices. Each
new point sees at most three colours. Choose any unused colour independently
at every new point. Since no two new points are adjacent, this extends the
given colouring to `H`.

Conversely, a colouring of `H` restricts to a colouring of `G`, since all
original unit edges are retained. Restriction is therefore surjective onto the
entire set of four-colourings of `G`. This proves more than equality on the
eight chosen terminals: every partially prescribed colouring of the original
sixteen vertices extends to `H` if and only if it extends to `G`. The same
argument covers every one of the `2^28` choices of added points.

In particular, the eight-terminal relation still allows 2691 and forbids 104
of the 2795 partitions into at most four colours. The existing conditional
palette obstruction remains valid, but this driver forces none of its missing
premises. The supplied three-colouring and the unit triangle on labels
`(2,3,5)` establish `chi(H)=3`.

The count can also be reproduced without importing the old certificate. For a
four-terminal word `w`, put `P={w0,w1}` and `Q={w2,w3}`. The endpoint relation
`R(w)` consists of all ordered `(a,b)` for which `a!=b`, `a` is outside `Q`,
and some `d,c,e` satisfy

```text
d,c outside P; e outside Q; d!=c; c!=e; e!=a; d!=b.
```

These are exactly the thirteen single-cell edges. An eight-terminal word
extends to `G` if and only if `R(w[:4])` intersects the transpose of
`R(w[4:])`. Enumerating these finite relations gives the stated count; the
extension argument transfers it to `H`.

## Verification and reproduction

Python **3.11.2**, standard library only. From the repository root:

```sh
python3 -B hadwiger_nelson_palette_terminal_circle_gate/verify.py --check-expected
python3 -O -B hadwiger_nelson_palette_terminal_circle_gate/verify.py --check-expected
python3 -B hadwiger_nelson_palette_terminal_circle_gate/controls.py
```

From this directory, `sha256sum -c SHA256SUMS` verifies the source manifest.
No solver, network, earlier package, or external data is needed for replay.

The verifier performs all 28 terminal-pair intersection decisions and all
**946** unordered point-pair checks after merging. It establishes 37 unit
contacts by exact rational radical multiplication and 48 by the defining
circle-intersection identity. It excludes all remaining 861 pairs with
rational interval bounds. Every squared distance between distinct points is
proved greater than `2^-20`; every nonunit squared distance differs from one
by more than `2^-20`.

All interval endpoints are Python `Fraction` values. Arithmetic is exact;
positive square roots are enclosed between dyadic bounds proved by integer
squaring, with 80 fractional bits by default. The positive branch, reciprocal
domains, circle existence, root merging, and edge classification are checked
explicitly. Any unresolved equality or overlap makes verification fail.
No float participates in a mathematical decision. This combines exact contact
identities with certified rational separation, rather than treating a small
residual as an edge.

Author-side controls replay at 48, 80 and 128 bits, compare all 190 distances
among the twenty base-field points using a separate prime-mask multiplication,
test interval boundary cases, and reject eight corrupted certificates. A
separate complete domain search on the **full 44-point graph** checks all
2795 terminal patterns against the path-elimination relation, validates 2691
positive words, and exhausts the 104 negative cases. Colour-permutation
coverage is checked by normalizing all `4^8` named assignments. These are
author checks, not independent-author review or proof-assistant verification.
See [VALIDATION.json](VALIDATION.json) for timings and hashes.

## Construction consequence and scope

This was a declared driver for the existing eight-terminal geometry, not a
larger sum of cells. Its complete common-neighbour pool cannot provide new
four-colour information. A useful successor needs a different physical
mechanism that escapes the proved independent, degree-at-most-three extension
structure. No such successor or smaller five-chromatic construction is claimed.
The opposed-palette source remains dormant pending a concrete driver and a
complete at-most-508 point budget. The retired H421 attachment and F29 chord
transfer are not reopened.

A bounded live literature refresh on 2026-09-14 found no smaller unrestricted
record than [Parts' 509-point graph](https://arxiv.org/abs/2010.12665), also
identified as the record in
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4). This finite
negative gate does not change that comparison. No historical priority is
claimed for the elementary extension lemma or circle-intersection construction.
