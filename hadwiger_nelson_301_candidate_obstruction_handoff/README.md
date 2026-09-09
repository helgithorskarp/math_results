# Terminal handoff for the closed 301-vertex HN candidate and direct repairs

The fixed labelled graph with SHA-256
`7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb`
has four linked exact results:

| Evidence layer | Established statement | Logical role |
|---|---|---|
| [h3977 producer](../hadwiger_nelson_h516_k23free_edge_repair) | The 301-vertex, 1,452-edge **abstract** graph is exactly five-chromatic and vertex-critical, with no K2,3 or K4 | Supplies the chromatic candidate |
| [h3981 obstruction](../hadwiger_nelson_301_repair_plane_obstruction) | The same graph has **no** Euclidean plane unit-edge map, even allowing arbitrary vertex identifications | Closes its geometric realization |
| [h3993 interface](../hadwiger_nelson_301_forbidden_subgraph_interface) | A 204-vertex, 690-edge subgraph already has an all-map obstruction | Gives a necessary edge-deletion clause |
| [h4007 classification](../hadwiger_nelson_301_norm_edge_repairs), [h4023 review](../hadwiger_nelson_301_norm_edge_repairs_review1) | All 18 deletions from the h3993 norm support are classified: six are four-colourable and twelve are exactly five-chromatic but geometrically obstructed; h4023 independently accepts this exact bounded scope | Closes the distinguished direct-repair family |

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

## Terminal direct-repair closure

H3993 identifies 18 source edges used by its exact norm contradiction. H4007
classifies deletion of each one. Six repaired graphs have checked proper
four-colourings. A combined 1,227-variable, 6,145-clause CNF and strict
RUP-only LRAT replay prove that the other twelve remain exactly
five-chromatic; twelve fresh all-map certificates then exclude every plane
unit-edge map of those graphs. No case is a physical five-chromatic graph.

H4023 independently accepts this complete 18-case statement. Its separate
standard-library checker reconstructs the support and repair clause, checks
the six colourings, all 3,300 certified four-cycles and 6,600 diagonal
witnesses, recomputes ranks 242--246 modulo the fresh prime 998244353, checks
the twelve norm identities and combined CNF semantics, and rejects two
semantic corruptions. Normal and optimized runs agree.

The 7,544,256-byte generated compressed LRAT for the twelve chromatic lower
bounds is intentionally absent from Git pending explicit human approval. Its
compressed and raw hashes, size, and strict replay receipt are published in
the h4007 omitted-artifact manifest. The public compact replay checks the CNF,
all case metadata, the six colourings, and all twelve geometric certificates,
but cannot independently replay those twelve lower bounds without the exact
omitted archive. H4023's reviewer did replay that byte-identical local archive
with a separate Python RUP implementation: 66,120 additions, 72,205 deletions,
4,202,594 used hints, and 98,052 lines. The headline 18-case closure itself
does not require the archive: the six colourable cases fail chromatically and
the other twelve fail geometrically. The LRAT is needed only for the stronger
description of those twelve as exactly five-chromatic.

## Teammate boundary refresh

The newest published team-hn-2 boundary inspected for this consolidation is
h4005: every rotational sum of two 19-point triangular hexagons is three- or
four-colourable. Its later private Kiteck--Payne copy pilot and post-pilot
source gate also produced no positive candidate or concrete bridge request.
Those closed or gated mechanisms are disjoint from this chain. No repair
search or new construction is opened by this handoff.

## Reproduction

[`verify.py`](verify.py) pins the exact source files, checks that every layer
names the same graph, replays the producer audit and strict LRAT checker,
replays h3981 in normal and optimized Python, reproduces both independent
acceptances, checks h3993 without importing it into the fixed-graph
conclusion, and audits the entire 25-entry public checksum manifest plus the
normal and optimized compact h4007 replay. It additionally pins all three
h4023 review files and reproduces that independent checker in normal and
optimized Python.

From the repository root, using Python 3.11+, a C++17 compiler, and an unused
work path:

```sh
python3 -B hadwiger_nelson_301_candidate_obstruction_handoff/verify.py \
  --work /tmp/hn301-final-handoff --controls
```

Expected status:
`FIXED_301_CANDIDATE_AND_DIRECT_NORM_SUPPORT_REPAIRS_CLOSED`.
The output must match [`EXPECTED.json`](EXPECTED.json). No SAT solver, CAS,
floating-point calculation, or network access is used.

## Final scope

The conclusion concerns the fixed 301-vertex graph and exactly the 18
one-edge deletions supported by the h3993 norm identity. The other 672 edges
of the h3993 repair clause, multi-edge deletions, replacements, and different
construction families remain outside scope. No graph improving the
509-vertex record is produced.
