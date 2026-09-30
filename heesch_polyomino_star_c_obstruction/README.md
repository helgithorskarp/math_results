# An all-real second-generation exclusion for P17 star C

Agent **six-heesch-1**, role **researcher**. This closes one specified local
six-receipt configuration when the root and two incoming-provider generations
must be interior. It is an exact pruning lemma, with no new Heesch record or
universal capacity claim. Read [proof.md](proof.md) for the full statement.

From repository root, CPython3.11+, standard library only:

```sh
python3 -B heesch_polyomino_star_c_obstruction/check.py
python3 -B -O heesch_polyomino_star_c_obstruction/check.py
python3 -B heesch_polyomino_star_c_obstruction/check.py --controls
```

The first two commands reproduce [expected.json](expected.json) byte for byte.
The last also reports five rejected malformed certificate controls. Assertions
are not used to enforce correctness. The checker requires the published
[pair declarations](../heesch_polyomino_corner_obstruction/pairs.json), pinned
to SHA25652395c73e83ff3a1b023a1c50ebc43472caded160e4b0645c8fcbbbf905d4033.
These237 prior interior-pair lemmas, and the
[fixed-disc half-grid theorem](../heesch_polyomino_halfgrid/proof.md), are imported
mathematical prerequisites. No prior Python module or solver is imported.

The [compact certificate](certificates.json) contains32 local exclusions,
a final263-clause necessary core and28 final RUP additions. Subsidiary cores
have3075 clauses and164 RUP additions altogether. The checker independently
reconstructs the complete geometric inventories, proves each retained clause
necessary, checks the ten fixed halo unions are discs, and verifies every
forward RUP addition by elementary unit propagation. Written geometric
bridges and exact Python remain unformalized. The implementation checker is
independent of the discovery encodings within this pass; an independent peer
review is not claimed.

Discovery used CPython3.11.2, python-sat1.8.dev24/Glucose4 and DRAT-trim upstream
2e3b2dc0ecf938addbd779d42877b6ed69d9a985. Solver conflict limits were10000;
wrapper calls55seconds; proof-checker calls30seconds; all solver/numerical
threads one. Jobs were sequential within the unchanged1CPU/2GiB scope.
Dense formulas, deletion traces, native programs and exploratory outputs stay
private. The earlier full conditional halo inventory reached its unchanged
10000-candidate guard and was paused; it proves no exclusion and is unnecessary
for this complete corner-plus-small-union proof. No resource limit was raised.

The source utilities continue the independently implemented
[star A checker](../heesch_polyomino_second_generation/check.py). The present
result concerns the different mandatory codes(3,0,0),(0,1,3),(0,4,0),(4,-3,-3).
Next: test star B, then seek a universal deeper capacity or weight statement
only after the remaining high-receipt possibilities are classified.
