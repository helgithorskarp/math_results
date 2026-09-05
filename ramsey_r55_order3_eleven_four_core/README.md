# Four-versus-seven minority cores: a complete 197-class cover

The four internally red moving triangles in the eleven-cycle
four-versus-seven branch reduce to **197 action classes**, covering all
115543 locally valid labeled twelve-vertex cores. The complete local
criterion uses 108 forbidden red-K5 bit patterns. Every catalog entry
has a representative compatible with the existing full-graph
normalization and an independently checked eighteen-unit assignment.

This is a solver-free local classification. **All 197 full extensions
are untested in this pass.** Neither eleven-cycle split is excluded,
and no target graph or Ramsey lower-bound improvement is established.

| exact census | count |
|---|---:|
| binary cross-word assignments | 262144 |
| assignments with no complete cross word | 117649 |
| locally invalid among the noncomplete assignments | 2106 |
| locally Ramsey-valid labeled cores | 115543 |
| valid cores satisfying anchor normalization | 3378 |
| normalizer action classes | 197 |
| full vertex maps / effective core maps | 3888 / 1296 |

[PROOF.md](PROOF.md) gives the occupancy argument, phase interpretation,
group action and full normalization bridge. [cover.json](cover.json)
contains all 197 representatives, orbit sizes, normalized counts,
membership hashes and primary units. These are classes of a specified
cyclic action; distinct entries are not asserted to be nonisomorphic
as unmarked graphs.

## Reproduction

CPython 3.11.2, standard library only. No solver, group package or
omitted input dataset is required. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B classify.py --work /scratch/new-r55-four-core/production
cmp cover.json /scratch/new-r55-four-core/production/cover.json
python3 -B check_cover.py --cover cover.json --work /scratch/new-r55-four-core/verification
cmp report.json /scratch/new-r55-four-core/verification/report.json
python3 -B controls.py --cover cover.json --report /scratch/new-r55-four-core/controls.json
cmp controls_report.json /scratch/new-r55-four-core/controls.json
python3 -B -O classify.py --work /scratch/new-r55-four-core/production-O
cmp cover.json /scratch/new-r55-four-core/production-O/cover.json
python3 -B -O check_cover.py --cover cover.json --work /scratch/new-r55-four-core/verification-O
cmp report.json /scratch/new-r55-four-core/verification-O/report.json
python3 -B -O controls.py --cover cover.json --report /scratch/new-r55-four-core/controls-O.json
cmp controls_report.json /scratch/new-r55-four-core/controls-O.json
```

The producer uses occupancy masks and an eight-generator orbit closure.
The checker imports no producer module. It reconstructs all 262144
literal graphs, checks both colors for K5s, then applies all 3888 actual
vertex maps to each representative. It compares complete per-class
membership and the entire labeled-to-representative assignment through
reproducible digests, with explicit disjointness and coverage checks.
It checks all full-action identities, 22 later normalization generators,
and every primary-unit meaning. [report.json](report.json) records the
deterministic result; [controls_report.json](controls_report.json)
records four malformed-cover and three direct graph controls.

The compact catalog is about 47 KB. The approximately 1.5 MB generated
membership table and operational logs remain outside Git. Measurements
are recorded separately in [measurements.json](measurements.json);
they are informational rather than byte-reproducible timing claims.
The entire bounded classification and verification are complete, with
no active background process.

## Application boundary

The [parent eleven-cycle formula](../ramsey_r55_order3_eleven_cycle_obstruction)
and its [independent review](../ramsey_r55_order3_eleven_cycle_obstruction_review1)
supply the full r=4 normalization and degree/counter bridge.
The method builds on the earlier
[three-triangle core reduction](../ramsey_r55_order3_eleven_minority_core),
but enumerates a different local domain. No three-versus-eight
refutation is used to exclude a four-versus-seven core.

The parent has 34280 variables and 615920 clauses. Each eventual full
extension cube must preserve the complete parent and append its
eighteen checked units, yielding 615938 clauses. The cubes form a
complete cover through graph relabeling. No new fixed graph, degree
profile, or automorphism is assumed. This pass generates no full
extension formula and supplies no SAT/UNSAT verdict.

The local theorem needs no external Ramsey value. Its application
imports the accepted parent, including R(4,5)=25 and the degree window
18 through 24. Ordinary unformalized reasoning, Python/runtime/hardware
and SHA256 remain trust boundaries. The new classification and
normalization bridge await independent review. This milestone stops
before fixed-vertex extensions or a full 197-case solver sweep.
