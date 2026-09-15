# A specified Golomb graft is an already closed one-point addition

This package records an exact construction identity, not a new chromatic
exclusion or a record candidate. Place the ten-point Golomb graph by the
unique orientation-preserving isometry taking its inner edge `(7,8)` to
Parts509's edge `(0,149)`. Nine of its points already belong to Parts509.
The whole union is exactly

```text
Parts509 union {q},    q = 2/3 + i*sqrt(11)/3.
```

It has **510 distinct points and 2,451 complete unit edges**. The only new
point has the nine original neighbours
`39,42,69,91,136,216,264,297,347`.

Consequently every support of at most 508 points contained in this union is
four-colourable by the existing
[one-point swap closure](../hadwiger_nelson_parts509_swap_closure/README.md).
If it contains q, it omits at least two original points and falls under that
closure; if it omits q, it is a proper subgraph of the independently certified
[vertex-critical parent](../hadwiger_nelson_parts509_criticality/README.md).
These chromatic facts are **imported**, not newly proved or replayed here.
The degree-9 instance is also explicitly covered by the older
[completion census](../hadwiger_nelson_parts509_completion_census_degree9/README.md).
The point is entry16 of the existing external completion list.

## Exact placement

Use the ten Golomb rows in the fixed order of the earlier
[Golomb source](../hadwiger_nelson_golomb_rotation_sum/README.md). A row
`(a,b,c,d)` represents `(a+b*sqrt33)/36 + i*(c*sqrt3/36+d*sqrt11/12)`:

```text
(0,0,0,0), (36,0,0,0), (18,0,18,0), (-18,0,18,0),
(-36,0,0,0), (-18,0,-18,0), (18,0,-18,0),
(6,0,0,2), (-3,-3,3,-1), (-3,3,-3,-1).
```

For Parts points p and Golomb points g, the map is

```text
u = (p149-p0)*conjugate(g8-g7),
T(g) = p0 + u*(g-g7).
```

Both anchor differences have norm one, so u has norm one. Labels are native
zero-based labels in the pinned Parts coefficient table. The exact overlaps
are:

| Golomb label | Parts label |
|---:|---:|
| 0 | 69 |
| 1 | 166 |
| 2 | 46 |
| 3 | 91 |
| 5 | 297 |
| 6 | 272 |
| 7 | 0 |
| 8 | 149 |
| 9 | 168 |

Only g4 maps to q. The inner triangle's third point lands at p168.
No second orientation or alternative anchor was tested.

## Reproduction and trust boundary

From the repository root, CPython3.11 or later with the standard library:

```sh
python3 -B hadwiger_nelson_parts_golomb_graft_identity/verify.py
python3 -O -B hadwiger_nelson_parts_golomb_graft_identity/verify.py
sha256sum -c hadwiger_nelson_parts_golomb_graft_identity/SHA256SUMS
```

[inputs.json](inputs.json) pins the existing exact Parts table. The verifier
uses sparse squarefree-radical dictionaries and rational arithmetic to
construct the map, checks all45 preserved atom distances, merges every
collision, and evaluates all129795 unordered squared distances of the union.
No floating threshold or inherited edge list decides an edge. The computed
ordered mapped-point and complete edge lists agree entrywise with the initial
dense-field producer. Normal and optimized runs agree. This is author-side
checking, not independent-author review.

The older swap-closure review accepted its mathematical statement while
identifying a defective historical checker pin. The author reply acknowledged
the defect and confirmed the repaired independent implementation. This package
uses the accepted theorem; it does not claim that the defective old version
passes or re-review the closure. The graph references and repaired-source
provenance are recorded in [inputs.json](inputs.json).

## Research decision

This was a failed attempt to specify a repair replacing several parent
vertices together. Exact reconstruction showed that the selected graft adds
only one point, so it falls back into a prohibited, already closed repair
regime. It was rejected before any capped deletion selection or ordinary
colour query. There is no new proper-five check, non-four signal or sub-509
physical construction. The 510-point union contains the intact positive
parent and supplies no new obstruction carrier.

Retire precisely this placement and do not respond by changing anchors,
orientation, copy count or deletion choices as a nearby sweep. The identity
is preserved to prevent repeating this proposal; it does not meet the
campaign's positive whole-candidate milestone or exclude other Golomb uses.
