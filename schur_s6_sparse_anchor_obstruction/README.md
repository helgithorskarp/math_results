# A 15-entry forbidden partial colouring for classical Schur 6 at 537

## Claim

Fix the colours of just the 15 positions in [`anchors.txt`](anchors.txt),
using colours `1,...,6`. There is **no** way to colour the other 522 positions
of `[1,537]` without a monochromatic solution of `x+y=z`. This is an
unconditional exclusion of one partial assignment, with no fixed prefix,
unchanged colour class, or distance restriction. It does **not** prove that
`[1,537]` is uncolourable and gives no new numerical bound for `S(6)`.

Equivalently, every valid six-colouring must disagree with at least one of
these 15 colour assignments. The 15 positions all lie between 449 and 515.
The certificate uses only triples with `x<y`, so it also excludes this
partial assignment under the weaker distinct-summand convention.

## Human-readable proof

The 15 anchors rule out each colour `1,3,4,5,6` at all three positions
`5`, `41`, and `46`. The table lists the forcing triple for each elimination.
For example, `5+469=474`, with 469 and 474 both anchored colour 1, excludes
colour 1 at 5. All other entries work the same way.

| Excluded colour | At 5 | At 41 | At 46 |
|---|---|---|---|
| 1 | `5+469=474` | `41+474=515` | `46+469=515` |
| 3 | `5+490=495` | `41+449=490` | `46+449=495` |
| 4 | `5+452=457` | `41+457=498` | `46+452=498` |
| 5 | `5+492=497` | `41+451=492` | `46+451=497` |
| 6 | `5+504=509` | `41+463=504` | `46+463=509` |

Consequently all of 5, 41, and 46 must have colour 2. Then `5+41=46` is
monochromatic, a contradiction. [`trace.txt`](trace.txt) gives the same
16 deductions in replay order. No search result is trusted in this proof.

## Independent check

Run from this directory with Python 3.8 or later; there are no dependencies:

```sh
sha256sum -c SHA256SUMS
python3 -B check.py
```

Expected output:

```text
PASS anchors=15 deductions=16 contradiction_at=5 final_triple=5+41=46
```

`check.py` starts every unanchored position with all six possible colours.
For each certificate row it checks the arithmetic, range, and that the other
entries of the triple are already forced to the forbidden colour. It then
deletes that colour from the target. The final deletion empties position 5's
domain. The checker does not use a SAT package, a heuristic score, or the
source word. A reader can also verify the table directly.

## Provenance and scope

The anchors came from the previously published
[`best3.txt`](../schur_s6_nonlocal_doubling_search/best3.txt), SHA-256
`73e5780b9163f79d0bba3a63bfb327561b83e944cb0b8f3064c140d2dacdbf49`.
Its last 89 entries first produced a unit-propagation contradiction in our
contiguous-suffix scan; deleting redundant fixed positions left these 15.
That discovery path is not needed to check the 16-step proof. The anchor
set is a concrete global search nogood, independent of the earlier
three-class trade exclusion around the external two-defect seed.

The published construction remains `S(6)>=536` ([Fredricksen–Sweet,
2000](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)).
A valid colouring of `[1,537]` would still improve that bound.
