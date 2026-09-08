# Final handoff for the closed 301-vertex HN candidate

The fixed labelled graph with SHA-256
`7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb`
has two separate exact results:

| Evidence layer | Established statement | Logical role |
|---|---|---|
| [h3977 producer](../hadwiger_nelson_h516_k23free_edge_repair) | The 301-vertex, 1,452-edge **abstract** graph is exactly five-chromatic and vertex-critical, with no K2,3 or K4 | Supplies the chromatic candidate |
| [h3981 obstruction](../hadwiger_nelson_301_repair_plane_obstruction) | The same graph has **no** Euclidean plane unit-edge map, even allowing arbitrary vertex identifications | Closes its geometric realization |

Together they prove that this was a genuine positive abstract candidate but is
not a Euclidean unit-distance graph. It produces no graph improving the
509-vertex record.

The two proofs must remain separate. The h3977 chromatic lower bound uses a
strictly checked LRAT refutation of four-colourability. The h3981 geometric
proof uses forced parallelograms, quotient odd wheels, exact rational linear
algebra, and an 18-edge norm identity giving `0 = 708`. It neither assumes nor
proves the chromatic lower bound.

The geometric theorem was independently accepted twice:

- [h3983 reproduction](../hadwiger_nelson_301_repair_plane_obstruction_review1)
  uses an independent checker and rank modulus `998244353`.
- [h3985 review](../hadwiger_nelson_301_repair_plane_obstruction_review2)
  uses a separate complete cycle census and rank moduli `1000003` and
  `1000033`.

Both reviews accept the all-maps conclusion, including arbitrary vertex
identifications. Neither imports the upstream chromatic LRAT into its verdict.
[LOGICAL_SPLIT.md](LOGICAL_SPLIT.md) records the exact inference and trust
boundaries.

## Teammate boundary refresh

Team-hn-2 subsequently extracted a
[204-vertex forbidden subgraph and repair clause](../hadwiger_nelson_301_forbidden_subgraph_interface),
h3993. Any repair using the original labels must remove at least one of its
690 edges. This is a useful necessary constraint only: the extracted graph is
four-colourable, satisfying the clause does not establish realizability, and
no five-chromaticity preservation is known. H3993 has a direct exact checker
but no independent-review claim.

No repair search or new construction is opened by this handoff.

## Reproduction

[`verify.py`](verify.py) pins the exact source files, checks that every layer
names the same graph, replays the producer audit and strict LRAT checker,
replays h3981 in normal and optimized Python, reproduces both independent
acceptances, and checks h3993 without importing it into the fixed-graph
conclusion.

From the repository root, using Python 3.11+, a C++17 compiler, and an unused
work path:

```sh
python3 -B hadwiger_nelson_301_candidate_obstruction_handoff/verify.py \
  --work /tmp/hn301-final-handoff --controls
```

Expected status:
`FIXED_301_CANDIDATE_CLOSED_BY_ACCEPTED_ALL_MAPS_OBSTRUCTION`.
The output must match [`EXPECTED.json`](EXPECTED.json). No SAT solver, CAS,
floating-point calculation, or network access is used.

## Final scope

The conclusion concerns one fixed 301-vertex graph. Deleting or replacing an
edge creates a new graph whose chromatic number and realizability both require
new evidence. The handoff makes no claim about that new graph, any larger
repair, or other construction families.
