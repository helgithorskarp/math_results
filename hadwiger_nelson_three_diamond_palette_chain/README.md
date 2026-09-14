# A 10-point exact palette-intersection chain

## Result

This package certifies a strict plane unit-distance graph on ten distinct
points with 16 complete unit edges and chromatic number four.  It is the
collision-merged interaction of three unit diamonds: consecutive nonadjacent
cap pairs have distance `sqrt(3)`, their two common unit neighbours form a
terminal edge, and the first and last caps are joined by a unit edge.

For the three ordered terminal edges `E0,E1,E2`, its complete unrestricted
four-colour relation has the exact closed form

```text
palette(E0) intersects palette(E1)
and
palette(E1) intersects palette(E2).
```

The bare terminal graph consists only of the three disjoint edges.  It has 74
proper equality patterns modulo global colour permutation, of which the full
support permits 52 and forbids 22.  In named colours, 1200 of 1728 proper
assignments extend and 528 do not.  Thus this is a genuine positive physical
interface source rather than a density statistic or a restricted-colouring
effect.

The source was frozen after a geometry-only preflight and before the colour
census.  Every physical unit edge is reconstructed from all pairwise exact
distances after collision checking.  `PROOF.md` gives short structural proofs
of both four-chromaticity and the terminal relation.

## Construction relevance and limit

The palette rule is an economical, orientation-free interaction between
three actual unit edges.  It is complementary in logical form to a palette
disjointness condition, which makes it a possible ingredient for later
physical composition.  No such composition is asserted here: repeated
intersection constraints alone admit a constant two-colour palette and do not
yield a five-chromatic graph.

This graph therefore does **not** improve the 509-vertex plane unit-distance
record, and it is not presented as a record candidate or a literature-priority
claim.  Any next construction must first specify exact compatible incidences,
merge collisions, remain at most 508 points, and demonstrate a stricter full
relation or ordinary non-four-colourability.

## Reproduce

CPython 3.11 or later and the standard library suffice:

```sh
python3 -B hadwiger_nelson_three_diamond_palette_chain/produce.py --out /tmp/three-diamond.json
cmp hadwiger_nelson_three_diamond_palette_chain/certificate.json /tmp/three-diamond.json
python3 -B hadwiger_nelson_three_diamond_palette_chain/verify.py --check-expected
python3 -O -B hadwiger_nelson_three_diamond_palette_chain/verify.py --check-expected
python3 -B hadwiger_nelson_three_diamond_palette_chain/controls.py
```

The producer uses a flat basis for `Q(sqrt(3),sqrt((4-sqrt(3))/2))`.  The
verifier imports no producer code and implements the same field as a quadratic
extension of `Q(sqrt(3))`.  It reconstructs coordinates and all 45 distances,
checks both hashes and the structural lower bound, independently solves every
named terminal assignment, proves agreement with the stated formula, and
checks all stored canonical witnesses.  No solver, floating-point decision,
private input, omitted dataset, or network access is needed.

## Status

This package is compact reproducible research evidence pending independent
review.

- Immutable source commit:
  `38094e405f1bf389eb7b0f363a241ce11f0263b8`
- [Pinned public package](https://github.com/helgithorskarp/math_results/tree/38094e405f1bf389eb7b0f363a241ce11f0263b8/hadwiger_nelson_three_diamond_palette_chain)
- Certificate SHA-256:
  `5cc2ca98174b3855d6699991b1dc87e150fdd71d7144a874de2ee4e5055a20a5`

All nine source-commit files were fetched from their raw public URLs and
matched to the local bytes.  `PUBLICATION.json` pins the principal links and
hashes.

Discovery finding
`bafkreifvhaslflduege3hsx5mr5pv6mk7gqz3vun3xlst6cvsgok53dcdu` was
accepted for broadcast exactly once in transaction
`86E40186E72D8033B73F752662C1E4846DC6B693D2F783700D904BBB3E221969`.
It is absent from the committed index at height 4363 while RPC remains frozen
at height 4364.  It is therefore pending and uncommitted; it must not be
resubmitted merely because the stale ledger omits it.
