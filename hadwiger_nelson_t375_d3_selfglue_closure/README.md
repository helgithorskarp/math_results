# Exact closure of the five marked-triangle T375 self-gluings

Let `T375` be the exact 375-point plane unit-distance graph in the sibling
[`hadwiger_nelson_small_triangle_forcer375`](../hadwiger_nelson_small_triangle_forcer375/README.md)
package.  Its three marked points form an equilateral triangle of side
`1/sqrt(3)`.  It is four-colourable, but no proper four-colouring makes all
three marked points monochromatic.

This package decides the five nonidentity plane isometries in the dihedral
group of that marked triangle.  For each isometry `g`, collision-merge the
complete physical support `T375 union g(T375)` and reconstruct every strict
unit edge.  All five unions lie below the record target, but all five are
four-colourable and have exactly the same unrestricted three-terminal
relation as one T375: every canonical nonmonochromatic pattern `001`, `010`,
`011`, and `012` extends.

| 120-degree steps | reflected first | points | complete edges | inherited edges | extra contacts |
|---:|:---:|---:|---:|---:|---:|
| 1 | no  | 431 | 1,944 | 1,936 | 8 |
| 2 | no  | 431 | 1,944 | 1,936 | 8 |
| 0 | yes | 443 | 2,000 | 1,984 | 16 |
| 1 | yes | 393 | 1,770 | 1,768 | 2 |
| 2 | yes | 416 | 1,865 | 1,861 | 4 |

Thus neither the extensive collision overlap nor the incidental cross-copy
contacts strengthen the marked-triangle obstruction.  This retires exactly
the common-marked-triangle D3 self-gluing architecture.  It does not classify
other relative placements, more copies, other terminal triangles, or arbitrary
subsets of the 627-point reference support.  It is a restricted construction
stop, not a five-chromatic graph or an improvement on Parts' 509-point record.

## Exactness and proof boundary

Coordinates use the source's four-integer rows

```text
((a sqrt(3)+b sqrt(11))/36, (c+d sqrt(33))/36).
```

For a difference row, the verifier tests squared distance one by the exact
integer conditions

```text
3a^2+11b^2+c^2+33d^2 = 1296,   ab+cd = 0.
```

It reconstructs all five collision quotients and all pairwise unit contacts.
The compact certificate supplies one proper four-colouring for each of the
four canonical nonmonochromatic terminal patterns in every quotient.  These
twenty words are checked directly and make SAT solver output irrelevant to
the theorem.  The missing monochromatic pattern is excluded because every
union contains the first T375 copy; the verifier also replays T375's
deterministic exhaustive 735-node contradiction.  Four source dependencies
are byte-hash pinned.  One corrupted-word control must be rejected.

## Reproduction

Python 3.11 or later and the standard library suffice.  From the repository
root run

```bash
python3 hadwiger_nelson_t375_d3_selfglue_closure/verify.py
python3 -O hadwiger_nelson_t375_d3_selfglue_closure/verify.py
sha256sum -c hadwiger_nelson_t375_d3_selfglue_closure/SHA256SUMS
```

The first two commands end with

```text
EXACT T375 D3 SELF-GLUING CLOSURE VERIFIED
```

The construction was selected as a direct at-most-508 whole-composition gate:
any non-four member would already have been a physical record candidate after
a proper-five check.  No such signal occurred, so the family was not widened.

## Provenance and record comparison

The exact input is the public
[T375 source package](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_small_triangle_forcer375),
verified source commit
`f88d7ee5b1d0b5c640750dc287bda159b8775423`.  The present verifier pins every
input byte it uses, so later changes to that sibling directory are rejected.

The comparison target remains Parts'
[509-point, 2,442-edge plane unit-distance graph](https://arxiv.org/abs/2010.12665).
Haugland's August 2026 introduction likewise identifies 509 as the unrestricted
record; its 2,131-point result concerns the Moser-spindle-free restriction.
