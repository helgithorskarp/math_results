# Pegg12 commutative triple-sum four-colour stop

This package exactly decides one predeclared, materially non-reflection
whole-composition gate for the strict Hadwiger--Nelson sub-509 campaign.  It
does **not** produce a five-chromatic graph or improve the 509-vertex record.

Let `P=(p_0,...,p_11)` be the reviewed symmetric exact realization of the
12-point, 21-edge, four-chromatic Pegg/Shibuya graph `UD12-2`, with `p_0=0`.
Before doing any colouring computation, the complete construction was frozen
as the commutative triple Minkowski sum

```text
T = {p_i+p_j+p_k : 0 <= i <= j <= k < 12}.
```

There are `C(14,3)=364` formal addresses, so the entire construction is below
the campaign's 508-point cap even before collisions.  Exact collision merging
leaves **175 distinct points**.  Reconstructing every physical unit pair gives
**813 edges**.  Of these, 729 occur in one of the 78 translated source fibres
`p_i+p_j+P`; the other **84** are genuine complete-graph contacts.  Thus the
calculation is on the actual physical graph, not only the edges inherited from
the summands.

## Complete-input decision

The fibre `p_0+p_0+P=P` is distinguished.  Up to colour permutation, `P` has
756 complete proper four-colourings.  The verifier decides extension to the
same 175-point complete graph for every one of them:

```text
blocked     340
surviving   416
```

The first surviving source word is `011022011332`; `certificate.json` contains
its literal 175-character extension.  The verifier checks that word against
all 813 physical edges.  Conversely, deterministic exhaustive DSATUR proves
that each of the 340 blocked inputs has no extension.  Since `T` contains the
four-chromatic source and has a proper four-colouring, its chromatic number is
exactly four.

This surviving complete input fires the predeclared stop.  The triple-sum is
not a record candidate, and Pegg12 is retired as an active campaign source.
That operational retirement is not a theorem about arbitrary Pegg12
compositions.  The exact mathematical scope is only this displayed
realization and this commutative triple sum; no claim is made about other sums,
coefficients, phases, isometries, partial supports, or realizations.

## Exact arithmetic and reproduction

All coordinates lie in `Q(sqrt(3),sqrt(11))`.  `model.py` represents a field
element by four rational coefficients in the basis
`1,sqrt(3),sqrt(11),sqrt(33)`.  Coordinate equality, collision merging, and
unit-distance tests are exact coefficient comparisons; no floating-point
tolerance is used.

CPython 3.11 or later and only the standard library are required:

```sh
python3 -B verify.py
python3 -B controls.py
python3 -O -B verify.py
python3 -O -B controls.py
```

The normal and optimized runs reconstruct the geometry, enumerate all 756
source inputs, reproduce the relation hash and validate the literal witness.
The controls test the radical multiplication rules and reject four corrupted
certificates.  `SHA256SUMS` pins the compact package.

## Provenance and evidence boundary

The exact source formulas are reproduced self-contained here from the earlier
author package `hadwiger_nelson_pegg12_reflection_completion_stop`, commit
`beab314a6e106e524d6cbdcd26d26e785e0c5e7f`.  Their source geometry and the
756-colouring census were independently reproduced in
`hadwiger_nelson_pegg12_reflection_completion_review1`, commit
`9bb103a`.  This triple-sum computation is new author-side evidence and is not
presented as an independent review or formal proof-assistant result.

The original coordinate provenance is the MIT-licensed
[`shibuya/graphs/pegg.py`](https://github.com/Parcly-Taxel/Shibuya/blob/218097c9971db2b60ab94a0b8dae20d76741cc43/shibuya/graphs/pegg.py)
at pinned commit `218097c9971db2b60ab94a0b8dae20d76741cc43`.
