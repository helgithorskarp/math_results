# Immutable interface for team-r55-1

Start from the h3887 complete physical task registry. Remove exactly the 518
indices in `TASKS.json`'s `excluded_core_indices` from its `q7,r5` class.
Keep the other 122 indices in that class, and keep every index in the other
17 macro classes. The resulting complete cover has 2,188,660 tasks.

Every removed task is a complete 43-vertex family. Its required induced
23-vertex tail has a checked UNSAT certificate after an equisatisfiable
normalization that fixes the catalog core. The physical embedding is
checked against every applicable clause of the pinned h3873 generator by
`check_bridge.py`. The source proof explains why these clauses occur in
the complete h3887 formula.

Every retained q7,r5 tail has a saved literal witness in
`TAIL_WITNESSES.json`. These witnesses certify residual feasibility only.
They are not an exhaustive list of residual completions, are not good43s,
and must not be fixed as the entire retained physical search. The receiving
emitter preserves the parent's full free-edge space and all parent clauses.
It adds no new labeling convention to the complete physical formula.

To verify the whole physical connection, using the source closure and four
hash-pinned catalog inputs from the handoff:

```sh
python3 -B ramsey_r55_q7r5_tail_decisions/check_bridge.py \
  --parent-root /path/to/source --cache /path/to/data
```

For a receiving emission check, `bo1-q7-r5-c000000` is excluded and must not
produce a CNF. Retained `bo1-q7-r5-c000004` emits the original direct formula
with 817 variables, 873,254 clauses and 36,958,253 bytes, SHA-256
`8f0b26b37d628022ad771d698871c443d363029795a310eaf256879c74d64af7`.
Its original parent auditor checks every literal. No physical solver call
was made on this retained formula in this contribution.

An included 8,722-addition RUP certificate independently closes complete
task `bo1-q7-r5-c000145` without running a SAT solver. The other negative
proofs are reproduced by the full 640-case replay; all original proof
digests and all positive witnesses are published. The recorded primary
proof streams remain private, outside Git. Compact encoding verification
alone does not re-establish the negative decisions.

The snapshot's separately pinned manifest records the exact source commit,
Discovery Net reference, complete parent source closure, graph inputs and
receiving receipt. The common delivery notice provides that immutable path
and its manifest SHA-256. A handoff notice is not an acknowledgement.

The independent q10 accounting remains 99 closed children and 161 UNKNOWN
children under h3987, with both middle-degree parents UNKNOWN. Those are
subtasks of a different macro class; their counts are not subtracted from
the h3887 task total here. No good43 is established.
