# Exact rigid-atom two-coincidence isometry closures
This package gives an exact negative construction result for three physical
Hadwiger--Nelson attachment families built from the seven-point Moser spindle
`M` and the ten-point Golomb graph `G`.

For a seed point set `B` and an atom `A`, let `C_A(B)` be the set of all
congruent or reflected copies `T(A)` with at least two distinct points in
common with `B`.  Every plane isometry, every possible pair of shared points,
and every additional coincidence and unit edge is included.  Define the full
closure

```
U(B; atoms) = B union union { T(A) : A in atoms, T(A) in C_A(B) }.
```

## Exact computer-assisted result

Each complete strict unit-distance graph below has the published proper
four-colouring.

| Seed and allowed attached atoms | Copy point sets | Closure vertices | Strict unit edges |
|---|---:|---:|---:|
| `B=M`, atoms `{M}` | 152 | 302 | 1,341 |
| `B=G`, atoms `{G}` | 251 | 700 | 3,531 |
| aligned `B=M union G`, atoms `{M,G}` | 343 Moser + 363 Golomb | 971 | 5,092 |

Consequently every graph made by retaining an arbitrary subcollection of the
listed copies is four-colourable, as is every vertex or edge subgraph of such
a graph.  This includes every member having at most 508 vertices.  No
five-chromatic graph or improvement to the 509-vertex record is produced.

The mixed seed aligns the two atoms on their common unit triangle.  The field
representation is exact:

```
(a,b,c,d) = a + b*sqrt(33) + i*c*sqrt(3) + i*d*sqrt(11),  a,b,c,d in Q.
```

All copy placements, point coincidences, and squared distances are decided in
this field.  `certificate.json` contains only three colour words and compact
counts/hashes.  `verify.py` reconstructs every copy and every strict edge and
checks the words without invoking a SAT solver.  The solver is used only by
`produce.py` to discover positive certificates.

## Scope

This is a restricted but complete family exclusion, not a global vertex
lower bound.  It does not cover:

- a copy sharing fewer than two seed points;
- a copy anchored only on points created by earlier moved copies;
- flexible or deformed atoms;
- atoms other than the specified Moser and Golomb embeddings.

An exploratory second Moser closure (allowing the second bullet) had 11,647
vertices and a checked numerical-geometry four-colouring, but that experiment
is deliberately not part of the exact theorem.  Repeating that expansion is
not a credible sub-509 route.

The published unrestricted benchmark remains Parts' 509-vertex, 2,442-edge
strict plane unit-distance graph.  Haugland's 2,131-vertex construction is an
improvement under the additional Moser-spindle-free restriction, not in
unrestricted order.  Primary sources are pinned in `SOURCE_PINS.json`.

## Files

- `PROOF.md`: completeness and certificate argument.
- `arithmetic.py`, `geometry.py`: exact construction.
- `certificate.json`: positive four-colour certificates and stream hashes.
- `verify.py`: solver-free exact verifier and mutation controls.
- `produce.py`: optional certificate regeneration with a SAT solver.
- `EXPECTED.json`, `VALIDATION.md`, `REPRODUCE.md`: compact evidence.
