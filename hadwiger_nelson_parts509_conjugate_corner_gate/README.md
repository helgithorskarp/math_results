# A redundant conjugate a=7 corner inside the fixed Parts a=8 decision

An exact algebraic transfer identifies 147,232,800 physical 508-point
selections in the fixed Parts/L374 a=8 cohort that map to the already closed
a=7 family. **Every one is already excluded by the frozen residual R0.**
Only 64 of R0's existing proper-colouring witnesses suffice to demonstrate
this redundancy. There is no new cut, strictly smaller residual, a=8 closure,
or record candidate. The full a=8 decision remains open.

This is a completed construction preflight and an explanation of why the
proposed transfer does not justify restarting the retired selector search.
No SAT solver was run. The corner is retired at this boundary; this package
does not license enlarging the pool or advancing to a=9.

## Exact physical transfer and budget

Use the existing 677-point ambient `L union S union Q5`, with `|L|=374`,
`|S|=135`, `|Q5|=168`, and all 3,400 strict unit edges. The exact coordinates
have denominator 288 in the bit-mask basis of
`K=Q(sqrt(3),sqrt(5),sqrt(11))`.

Let `sigma5` change the sign of sqrt(5), fixing sqrt(3) and sqrt(11), and put

```
T(x,y) = (-sigma5(x), sigma5(y)).
```

This is an involution on `K^2`. It is not asserted to be a Euclidean isometry.
It gives exact real coordinates, preserves distinctness, and preserves unit
distance in both directions: the squared-distance expression is sent to its
field conjugate, and `sigma5(z)=1` if and only if `z=1`.

The map preserves L setwise. It exchanges the following sixteen-point sets:

```
B subset S:
374 375 376 389 391 392 393 412 413 415 453 455 457 458 493 496

C subset Q5:
536 548 552 560 563 565 569 597 598 623 647 741 796 829 1054 1063
```

It also maps `S minus B` onto itself. Of the whole 677-point ambient, 662
images lie back in the ambient; the other fifteen are images of Q5 points
outside C. They are not selected in the declared corner.

For every `R subset B`, `|R|=9`, and `A subset C`, `|A|=8`, define

```
H = L union (S minus R) union A.
```

There are `C(16,9)*C(16,8)=147232800` distinct such supports. Each has exactly
508 distinct physical points. Its image has all L, `119+8=127` S points and
`16-9=7` Q5 points: also exactly 508 points. Thus the
[accepted a=7 closure](../hadwiger_nelson_parts509_pool_shape7_review1/README.md)
proves each H four-colourable. This is a transfer of an existing theorem,
not a new coloring principle.

## Why this cannot shrink the current residual

R0 is the exact fixed decision recorded in
[the residual package](../hadwiger_nelson_parts509_a8_residual_decision/README.md):
select 126 S points and eight Q5 points, hit all 17,269 positive cuts, and
give every selected Q5 point degree at least four. A positive cut D has a
literal proper four-colouring on `L union (U minus D)`, where `U=S union Q5`.
Consequently every non-four selection X must intersect D.

The 64 rows in `certificate.json` are all already members of these 17,269
cuts. Their domains and full colourings are checked directly against the
complete physical edge list. This package needs no solver verdict or complete
L-terminal-relation theorem to establish their validity.

On the corner, a cut is automatically hit if it contains an S point outside B.
Otherwise, put `D_B=D intersect S` and `D_C=D intersect C`. Its condition is

```
D_B is not a subset of R, or A intersects D_C.
```

Among the selected certificate rows, 56 have `|D_C|=1`. For each of the 11,440
choices of R, these clauses force a set F(R) of additions. For 10,885 choices,
`|F(R)|>=9`, contradicting `|A|=8`. The remaining choices have:

| Forced additions | Choices of R | Completions to eight additions |
|---|---:|---:|
| 6 | 13 | 585 |
| 7 | 94 | 846 |
| 8 | 448 | 448 |

For every one of these 1,879 remaining completions, one of eight additional
old cuts is disjoint from the selected X. The checker performs those literal
set-intersection checks. This exhausts the entire corner and shows that the
positive cuts alone already exclude it; the degree constraints are unnecessary.

An earlier author implementation projected all 1,391 distinct applicable R0
cut clauses, with the degree conditions, and exhaustively filtered all 12,870
addition masks for each R using integer bit sets. It likewise found zero
survivors. The compact public explanation uses forced additions and individual
remaining completions, not that bit-set implementation.

## Reproduce and scope

From the repository root, with Python 3.11 or later and only its standard
library:

```
python3 -B hadwiger_nelson_parts509_conjugate_corner_gate/verify.py
python3 -B hadwiger_nelson_parts509_conjugate_corner_gate/controls.py
python3 -O -B hadwiger_nelson_parts509_conjugate_corner_gate/verify.py
```

The normal and optimized verification outputs agree byte for byte with
`EXPECTED.json`. The verifier reconstructs all 228,826 ambient pairs and all
228,826 transformed pairs, obtains the same labelled strict unit graph,
checks all 64 positive words over 212,327 edge incidences, establishes
membership in the pinned R0 cut family, and verifies the exhaustive argument
above. It also checks the exact exchanged sets and collision-free involution.

Controls check all 64 products of field basis elements under sigma5, all
9,207 positive-clause projections on a small universe, and rejection of five
deliberately corrupted or incomplete certificates. The two author enumeration
methods agree. This is author validation, not independent review or formal
proof-assistant certification. The exact geometry reader and its primitive
source files are explicit hash-pinned imported dependencies.

The a=7 theorem explains the initial transfer proposal. The final 64-word
redundancy proof is self-contained relative to the exact geometry and the
literal colour strings; it does not import the a=7 UNSAT proof. Bulky prior
colouring caches, old solver traces, and exploratory scripts are not copied
into this package. No previous evidence or pending Discovery receipt is
replaced.

As checked on 14 September 2026, Parts's published vertex record is still
[509 points and 2,442 strict unit edges](https://arxiv.org/abs/2010.12665),
also identified as the current vertex record in
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4).
This restricted redundancy result does not improve that record.
