# E477 mandatory-core maximum-translation union stop

This package decides one exact multi-overlap/extra-contact construction under
the strict Hadwiger--Nelson sub-509 objective.  It is a scoped negative result,
not a record improvement.

Start with the independently reviewed **255-point mandatory core** `C` inside
the 477-point equal-terminal source E477.  Among all nonzero translations that
take one point of `C` to another, choose a translation maximizing
`|C intersect (C+t)|`; break ties lexicographically in the source coefficient
coordinates.  There are exactly two maximizers, each with 75 overlaps, and the
frozen choice is

```text
t = (-3,3,3,3).
```

The collision-merged complete strict unit graph on `C union (C+t)` has

```text
435 distinct physical points,
1,589 complete unit edges,
75 overlaps,
1,231 edges inherited from the two core copies, and
358 genuine contacts not inherited from either copy.
```

Thus this support is far outside the previously reviewed E477 family, whose
two copies have one overlap and one cross edge.  Nevertheless a literal
435-character word properly four-colours every one of the 1,589 edges.  The
union contains an exact seven-point Moser spindle; exhaustive checking of all
`3^7` words finds no proper three-colouring.  Its chromatic number is therefore
**exactly four**.

This fires the declared stop for the architecture.  No neighbouring
translation, second overlap objective, rotation, reflection, deletion order,
or enlargement is inferred or authorized by this result.

## Exact coordinates and complete graph

An E477 row `(a,b,c,d)` means

```text
((a*sqrt(3)+b*sqrt(11))/36, (c+d*sqrt(33))/36).
```

The verifier independently represents both coordinates in the radical basis
`1,sqrt(3),sqrt(11),sqrt(33)`, deriving multiplication from square-free gcds.
It reconstructs all 477 source points and the mandatory core from the pinned
source files, enumerates every nonzero core-to-core translation, proves the
maximum-overlap selection, collision-merges the two copies, and tests all
`binom(435,2)=94,395` physical pairs for unit distance.  No tolerance,
floating-point coordinate, selected edge list, or SAT verdict is used.

The coordinate-row and complete-edge streams have SHA-256 values

```text
points  9ad878b94cac336dff1a43e12eb1ad6fff956dc1d74612aac8715b441db86cfe
edges   75b40c0a3c6a62815ad4f40207a68ab3a4e9ec71b07e14c5d01457a2c1cb5d81
```

## Reproduction

CPython 3.11 or later and its standard library suffice.  From the repository
root run

```bash
python3 -B hadwiger_nelson_e477_core_translation_union_stop/verify.py
python3 -O -B hadwiger_nelson_e477_core_translation_union_stop/verify.py
python3 -B hadwiger_nelson_e477_core_translation_union_stop/controls.py
python3 -O -B hadwiger_nelson_e477_core_translation_union_stop/controls.py
sha256sum -c hadwiger_nelson_e477_core_translation_union_stop/SHA256SUMS
```

The controls compare the generic radical norm with the direct two-equation
source norm on all 94,395 union pairs and reject five certificate corruptions.
`certificate.json` contains only the positive four-colour word and compact
expected identities; all coordinates and edges regenerate from the pinned
sibling source.

## Scope and record comparison

The mandatory core is not asserted to force the E477 terminals equal.  It was
chosen because every equality-forcing subgraph of fixed E477 must contain it;
the global contacts and overlaps of this complete union were tested directly.
Four-colourability of this union says nothing about other translations,
isometries, optional E477 vertices, multi-copy assemblies, or arbitrary plane
unit-distance graphs.

Parts's 509-point/2,442-edge strict construction remains the supported
unrestricted record.  The present 435-point graph is explicitly
four-chromatic and is not a record candidate.
