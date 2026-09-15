# Translated pointwise-Galois collision gate for I450

The exact 450-point I450 source has marked endpoints `O,V` which receive
different colours in every proper four-colouring.  Identifying them through
an edge-preserving plane map would therefore give a non-four-colourable image
on at most 449 points, comfortably inside the 508-point construction target.

This package closes one exact coordinate-producing mechanism:

> Translate I450 by half its marked displacement, and independently apply to
> each vertex one of the four real embeddings of
> `Q(sqrt(3),sqrt(11))`.  No choice preserves every inherited unit edge while
> identifying the marked endpoints.

The obstruction is already present on the source unit path
`0--10--16--1`.  Of its `4^4=256` embedding assignments, exactly 16 preserve
all three unit edges and none identifies vertices 0 and 1.  The checker also
reconstructs all 2,290 source unit edges and classifies their complete
four-by-four embedding transition tables.

This is a scoped exact realization failure, not a plane graph, a non-four
certificate, a record candidate, or evidence that I450 has no other
edge-preserving realization.  In particular it does not extend the earlier
ordinary reflection-fold gate into a sequence of deformation exclusions.
The completion architecture is stopped here.

## Reproduce

CPython 3.11 or later and the standard library suffice.  From the repository
root:

```bash
python3 -B hadwiger_nelson_i450_translated_galois_collision_gate/verify.py --check-expected
python3 -O -B hadwiger_nelson_i450_translated_galois_collision_gate/verify.py --check-expected
python3 -B hadwiger_nelson_i450_translated_galois_collision_gate/verify.py --controls
(cd hadwiger_nelson_i450_translated_galois_collision_gate && sha256sum -c SHA256SUMS)
```

No SAT result is used.  Two exploratory four-state CNFs first returned UNSAT,
but the published theorem is the exhaustive 256-case path calculation above.
The exact source certificate is pinned by SHA-256 and is not copied.

See [PROOF.md](PROOF.md) for the coordinate formula, path transition table,
scope, and construction consequence.  [VALIDATION.json](VALIDATION.json)
records the author-side replay boundary.
