# One-point augmentations of the Heule 516-core are closed throughout the plane

**Theorem.** Let B be the fixed 516-point, 2,538-edge Heule core in
[`SOURCE.json`](../hadwiger_nelson_h516_degree4_surgeries/SOURCE.json).
For every point q in the Euclidean plane, every subgraph of the unit-distance
graph on `B union {q}` with at most **508 vertices is four-colourable**.

The new computation closes every q **outside H632**, extending beyond the
finite pool covered by [h3991](../hadwiger_nelson_heule516_single_point_h632_closure).
The whole-plane corollary imports h3991 for the 116 points of H632 outside B.
No colouring query on that previously closed pool was repeated.

This excludes every one-point augmentation followed by arbitrary vertex
and edge deletions reaching the target order, for this fixed placement of B.
It does not cover two or more added points, other base supports, or other
placements of the abstract base graph. No record improvement is established.

## Complete geometric and colouring reduction

If q has at most three unit neighbours in B, any four-colouring of a proper
subgraph of B extends to q. A point with at least four neighbours is the
unique circumcentre of some base triple on a unit circle. Enumerating all
such triples therefore gives a complete finite candidate set, without
assuming beforehand that q belongs to any coordinate field.

The exact census finds 1,726 centres with at least three base neighbours.
Exactly **558 centres outside H632** have at least four neighbours:

| Degree into B | Outside points |
|---:|---:|
| 4 | 192 |
| 5 | 188 |
| 6 | 111 |
| 7 | 30 |
| 8 | 25 |
| 9 | 10 |
| 10 | 2 |

For each of these 558 points, the certificate verifies at least 508 distinct
vertices v of B for which `B-v+q` has a four-colouring. Any target subgraph
containing q omits at least nine base vertices; at most eight base vertices
lack such a colouring. One omitted vertex is therefore covered, and its
colouring restricts to the target subgraph. See [PROOF.md](PROOF.md).

The [82,664-byte certificate](certificate.json) adds 411 packed base-deletion
colourings to the 664 already supplied by h3991. A word covers `(q,v)` when
q's remaining neighbours use at most three colours. The verifier checks
every base edge and recomputes every extension. There are 33 points with
coverage exactly 508; the minimum is attained, not rounded.

## Reproduction

Use a full repository checkout, Python 3.11 or later, and a C++20 compiler:

```sh
python3 -B hadwiger_nelson_heule516_all_plane_onepoint_closure/verify.py \
  --work /tmp/hn516-plane-onepoint --controls
```

Choose an unused work directory. The command reconstructs the complete
geometric census, audits it with separate exact field arithmetic, and
checks the supplied colouring certificate. No SAT solver is needed.
It produces [EXPECTED.json](EXPECTED.json), with status
`ALL_PLANE_ONE_POINT_AUGMENTATIONS_OF_H516_CLOSED_THROUGH_508`.
Local verification takes roughly 80 seconds.

An existing census may be reused, including under optimized Python:

```sh
python3 -B -O hadwiger_nelson_heule516_all_plane_onepoint_closure/verify.py \
  --work /tmp/hn516-plane-onepoint --reuse-census --controls
```

This still freshly enumerates all base triples and checks every centre
incidence. Cached counts alone are never accepted as completeness evidence.
The normal and optimized results match byte for byte.

All large generated centre tables, triple streams, binaries and logs stay
in the specified work directory. Input identities are pinned in
[INPUTS.json](INPUTS.json). See [VALIDATION.md](VALIDATION.md) for controls,
arithmetic bounds, the discovery command and trust boundaries.

Certificate SHA256:
`8713d2af4f8e02bbd873bdb01f671a4630c3b946e5f65e810b2361a4a6dd06cb`.

The source's exact five-chromaticity is established by the prior Heule-core
certificates and supplied the positive physical starting point. It is not
needed as a premise of the colouring-based exclusion. This new closure is
author-verified; no independent-author review is claimed.
