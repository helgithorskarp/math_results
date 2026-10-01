# Sharp 69 for the two-fixed-point involution family

six-code-2, researcher. 2026-10-01. Author-checked exact computation and
ordinary unformalized reductions. Independent review of this joint result
and historical priority are unassessed.

Every family of distinct five-subsets of 18 points, with distinct members
intersecting in at most two points, that is preserved by an involution
with eight transpositions and two fixed points has **at most 69 members**.
The included previously published 69-word construction attains the bound.
There is no added degree or pair-multiplicity hypothesis.

The new finite ingredient is a sharp **56** bound when that involution
exchanges two degree-20 points whose pair multiplicity is three. Together
with explicitly imported low-multiplicity and previously published
multiplicity-four/five bounds, it closes the whole involution family.
[PROOF.md](PROOF.md) gives the reduction, complete finite domain and exact
dependencies. The unrestricted campaign interval remains 69..71.

Python 3.11+ and g++ with C++17 are required; only standard libraries are
used. From this directory, use distinct initially empty work directories:

```sh
python3 -B check56.py WITNESS56.json
python3 -B check_witness.py WITNESS69.json
python3 -B reproduce.py --work /tmp/two-fixed69-normal
python3 -B -O reproduce.py --sanitized --work /tmp/two-fixed69-optimized-sanitized
```

All runtime inputs are included. No network access or other checkout is
needed. [RUNTIME.json](RUNTIME.json) pins 12 reused files and preserves
earlier audit/kernel/fixture credits in [runtime/INPUTS.json](runtime/INPUTS.json).
[DEPENDENCIES.json](DEPENDENCIES.json) pins 13 included files for the
reviewed point-cap20, absent-pair56 and pair-two60 validators. The full
upper57 census, generic23-star classification and published exchanged
multiplicity-four/five bounds are mathematical premises; their entire
censuses are **not** rerun here. Byte matching does not prove those premises.
[LOWER69_INPUT.json](LOWER69_INPUT.json) credits the unchanged 69-word
witness and standalone checker from the earlier one-cap Steiner result.

The driver sequentially checks both complete actual-map generators,
actual point transports, all nine weighted completion graphs and separate
literal native upper searches. The optimized command sanitizes all nine
native cases. It also replays all three small prerequisite validators and
checks both literal witnesses. The three-multiplicity domain comprises
23 fixtures, 13 eligible mates, 73,710 raw maps, 44 compatible 37-word
anchors and nine positively covered roots. Their full maxima are
[56,56,56,55,54,55,56,55,52]. The largest residual weight is 19.

[EXPECTED.json](EXPECTED.json) was frozen from the preceding sealed
experiments before either cold run. Stable evidence must agree exactly,
including all 23 raw-file hashes and all nine upper/lower records.
[VALIDATION.json](VALIDATION.json) records actual cold runs. Generated
inventories, graphs, binaries and logs remain in the work directory.

Validation includes 1,099 weighted brute-force cases, 6,144 native small
graph/target cases, nine coverage/witness/point-guard damages, three
bound-record damages and corruption of each of the 25 pinned runtime and
prerequisite files. Literal checks examine all 1,540 pairs for the sharp56
witness and all 2,346 for the existing lower69 witness. These controls are
validation and do not replace the ordinary completeness arguments.

All numerical-library/OpenMP threads are one, with one expensive stage at
a time. Guards stay at 100,000 nodes/5s per point-map call, 30s per mate,
3,000,000 nodes/30s per weighted root, and 3,000,000 nodes/200,000 leaves/
30s per native query; native outer timeout35s and compilation timeout60s.
Each prerequisite subprocess has its unchanged 60s deadline. A timeout,
guard hit, failed process or incomplete return gives no absence claim.
