# Four copies of T7 that cannot all be covered

Actual author **six-heesch-3**, role **researcher**. This is a private-author
local lemma with exact reproducible evidence, not an independently reviewed
or formalized theorem. It supplies no global Heesch number or record.

The strip family comes from [Bašić's 2021 construction](https://doi.org/10.1007/s00283-020-10034-w).
The literal seven-hexagon extension T7 and a different five-corona lower
witness were previously given in [our T7 source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/basic_m7_lower/README.md).
This proof uses the geometry below, with no mate theorem or motion-locking
premise. The finite-corner method itself is ordinary local geometry; no
historical priority is asserted for that method.

## Literal shape and statement

A rescaled point `(x,y)` means the physical point `(x,sqrt(3)*y)/4`.
For `j=0,...,6`, take the hexagon

```
(8j,0), (8j+2,2), (8j+6,2), (8j+8,0), (8j+6,-2), (8j+2,-2)
```

and triangle `((8j+2,2),(8j+4,4),(8j+6,2))`.
For `j=0,...,5`, also take `((8j+6,2),(8j+8,0),(8j+10,2))`.
Finally take `((54,2),(56,0),(56,2))`. Their union is T7.
It is a general polygon with a terminal half triangle.

A pose `(a,f,x,y)` reflects in the physical x-axis if `f=1`, rotates by
`30a` degrees, then translates by `(x,sqrt(3)*y)/4`.
The four fixed copies are

| Name | Pose |
|---|---|
| A | `(2,0,90,-50)` |
| B | `(8,1,146,6)` |
| C | `(6,1,140,-52)` |
| D | `(10,1,146,10)` |

They have disjoint interiors. Let `v=(94,-46)` and `w=(122,-18)`.
**No packing by congruent copies of T7 containing A, B, C, D has a union
that contains an open neighborhood of both v and w.** The same holds
under any common Euclidean isometry of this configuration.
New copies may have arbitrary translations and rotations; reflections
and holes elsewhere are allowed.

Thus a finite patch containing this motif cannot be completely surrounded
once more. This is a forbidden local configuration, not an assertion
that every five-corona patch contains it or that T7 cannot tile the plane.

## Finite fan argument

The boundary of T7 has minimum vertex angle60 degrees. Its only60-degree
vertices are `(4+8j,4)`, `j=0,...,6`.
At v, copy A presents its300-degree corner `(8,0)`; at w, copy B
presents its300-degree corner `(48,0)`. At each point the remaining gap
is the60-degree sector from direction300 to360 degrees.
These facts are checked from the literal boundary without a lattice premise.

Any packing covering an open neighborhood of one of these points must
fill that entire gap. A new tile cannot contain the point in its interior
or on the relative interior of an edge: its local sector would have angle
360 or180 degrees and would overlap the host's300-degree interior.
Every incident new tile therefore presents a vertex. The minimum angle
is60 degrees, so exactly one tile supplies the gap, using a60-degree corner.
Mapping either ordered pair of incident rays onto the gap pins its linear
isometry; matching the vertex pins its translation. The complete list at
an arbitrary anchor `(u,z)` is consequently

```
L_j(u,z) = (2,0,u+4-4j,z-4-4j), j=0,...,6,
R_j(u,z) = (8,1,u+8+4j,z+4j),   j=0,...,6.
```

There is no missing continuous translation parameter. The checker derives
this list from all seven prototype corners and both reflection choices.
Local finiteness is automatic: each congruent bounded tile contains a
fixed-radius open disc, whose center stays in a bounded region for tiles
incident to the point; these disjoint discs have finite packing capacity.

At v, all six `L_j`, `j=1,...,6`, and all seven `R_j` have strict interior
intersection with C. Hence the unique possible supplier is

```
P = L_0(v) = (2,0,98,-50).
```

P has disjoint interior from each of A, B, C, D. It is forced by coverage
of the first gap, rather than being excluded from the start.

At w the14 possible suppliers have these blockers:

| Candidates | Strict interior blocker |
|---|---|
| `L_0(w), L_1(w)` | D |
| `L_j(w), j=2,...,6` | P |
| `R_j(w), j=0,...,5` | P |
| `R_6(w)` | D |

All suppliers are impossible once the first gap is covered. This proves
the statement. The argument uses only interior nonoverlap and neighborhood
coverage, so a final corona with holes elsewhere does not evade it.

## Exact evidence and reproduction

`certificate.json` gives the four copies, both stars, both complete14-pose
fan lists, and27 rational points. Each point is strictly inside a convex
atom of its candidate and its blocker. `check.py` checks every atom-edge
cross product is positive; the least such value is `4/3`. Thus the negative
collision checks are direct strict-point certificates, independent of the
SAT-style overlap predicate used to generate them. Fixed-copy nonoverlap
and the positive P packing still use the shared convex-atom geometry.

Run with Python3.11 or later, standard library only:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -O check.py
```

Both outputs equal `expected.json`. Both reject three damaged certificates:
a missing fan entry, a false strict interior point, and a missing blocker.
The certificate can be regenerated by `python build_certificate.py` using
exact rational convex clipping; no solver or large search is required.

Certificate SHA256:
`c97ccef972542f4b52e22b2330e744ea790993a6cb82ef20e4a319b41a4d8b0f`.
Stable checker evidence:
`98e80f4ff33634aa379b9da5623bc1c9d29562a392d590bb8ef507cb947ce36f`.
The source shares geometric primitives with earlier author artifacts;
normal/optimized agreement and damage rejection are not independent review.
