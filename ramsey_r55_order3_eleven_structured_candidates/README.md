# Seventeen C3 construction fixtures: best observed defect count 155

A bounded construction experiment produced seventeen explicit 43-vertex
colorings, one for each surviving four-versus-seven core in the eleven-cycle
action. **None is a Ramsey(5,5) graph.** The best observed coloring has
155 monochromatic five-sets: 74 red and 81 blue. No core was excluded and
the Ramsey lower bound is unchanged. No family optimum or search record
is claimed.

The useful exact certificate is local: every saved coloring has no improving
single-orbit flip **with its prescribed core fixed**. Three are strict local
minima. For the best coloring, every one of those 302 neighbors has at least
156 defects. This gives explicit starting objects and a checked limitation
of single-orbit descent, not a proof that larger moves or other initial
colorings cannot succeed.

## Objects and exact scope

[graphs/core186.edges](graphs/core186.edges) is the best fixture. The first
line is `43`; each later line is a red edge `u v`, with `0 <= u < v < 43`.
Every omitted pair is blue. Its edge-list SHA-256 is recorded in
[verification.json](verification.json). All seventeen compact edge lists
are in [graphs](graphs).

Every coloring is invariant under `(0 1 2)...(30 31 32)`, fixing `33..42`.
The first four moving triangles are internally red and the remaining seven
internally blue. The eighteen cross-triangle orbit values among the first
four triangles are fixed to the corresponding word in [cores.tsv](cores.tsv).
The remaining 302 orbit values are free. There is no frozen neighborhood,
degree profile, empty-signature requirement, or additional automorphism.
These are seventeen labeled fixtures; no claim of pairwise nonisomorphism
is made.

The best fixture has 457 red edges and degree histogram
`20^7 21^20 22^14 23^2`. Its defects consist of 29 action-invariant five-sets
and 42 orbits of size three. The complete defect representatives, degrees
and neighbor-score histogram are in
[best_verification.json](best_verification.json).

| Core | Red K5 | Blue K5 | Total | Minimum neighbor | Neutral moves |
|---:|---:|---:|---:|---:|---:|
| 92 | 79 | 96 | 175 | 175 | 2 |
| 97 | 87 | 95 | 182 | 182 | 1 |
| 118 | 91 | 68 | 159 | 160 | 0 |
| 119 | 88 | 74 | 162 | 163 | 0 |
| 124 | 80 | 96 | 176 | 176 | 1 |
| 155 | 77 | 97 | 174 | 174 | 2 |
| 164 | 93 | 77 | 170 | 170 | 3 |
| 168 | 71 | 98 | 169 | 169 | 2 |
| 180 | 61 | 103 | 164 | 164 | 2 |
| 182 | 70 | 105 | 175 | 175 | 1 |
| 185 | 88 | 89 | 177 | 177 | 1 |
| 186 | 74 | 81 | 155 | 156 | 0 |
| 190 | 80 | 100 | 180 | 180 | 2 |
| 191 | 112 | 73 | 185 | 185 | 1 |
| 192 | 104 | 77 | 181 | 181 | 3 |
| 193 | 93 | 80 | 173 | 173 | 4 |
| 194 | 64 | 97 | 161 | 161 | 1 |

The neighbor census freezes all eighteen prescribed core bits. It does not
cover core-changing flips, neutral paths, multiple-orbit moves, or arbitrary
single-edge changes that break C3. No full color-family closure follows.

## Experiment and validation

[EXPERIMENT.md](EXPERIMENT.md) was frozen before production. The exact
objective counts physical monochromatic five-sets, using weighted identical
orbit-support constraints. Four fixed-seed restarts per core, each with
25,000 orbit flips, completed all 68 restarts and 1,700,000 moves. A global
gain comparison with a seven-step tabu window and specified random escapes
chooses moves; this is heuristic search, not an exhaustive family enumeration.
The two-worker batch finished in 226.100212 seconds. Each restart's seed,
initial and best scores, best step and complete 320-bit best assignment are
preserved in [restarts.csv](restarts.csv). Pilot calibration is recorded
separately and is not counted as additional independent production restarts.

[verify.py](verify.py) imports no optimizer, clause generator, or primary-index
code. It checks every physical pair under the action and every core/internal
color. It visits all 962,598 literal five-sets of each graph; a separate
bit-intersection recursion reproduces the entire list of red and blue defects.
The verifier then discovers the physical pair orbits and checks all 302 allowed
neighbors by clique recursion. All 5,134 neighbors across the seventeen
fixtures were counted. The best fixture's entire audit is identical under
normal and optimized Python.

Strict GCC 12.2.0 release and AddressSanitizer/UndefinedBehaviorSanitizer
builds match the two 2,000-step calibration runs. Incremental gains are checked
on every production move, with full state reconstruction every 5,000 steps
and at each restart boundary. Seven malformed edge-list/action/core inputs
are rejected. Empty and complete graph controls recover exactly 962,598
monochromatic five-sets. The control reports match under normal and optimized
Python. All seven frozen production-source identities remain unchanged.

The search algorithm is not part of the trust base for the explicit graph
and local-neighbor claims. Those claims still trust the displayed elementary
argument, physical indexing in the independent checker, exact Python,
compiler/runtime for reproducibility, and hardware. These are author-run
independent algorithms, not external peer review or formalization.

## Reproduce the certificates

With Python 3.11.2 and its standard library, from the repository root:

```bash
bash ramsey_r55_order3_eleven_structured_candidates/reproduce.sh
```

This checks the manifest, input identities, all seventeen literal graphs,
all 5,134 physical one-orbit neighbors, and the complete best-fixture report.
It does not rerun the heuristic search. A direct audit of just the best is:

```bash
python3 -B ramsey_r55_order3_eleven_structured_candidates/verify.py \
  --edges ramsey_r55_order3_eleven_structured_candidates/graphs/core186.edges \
  --word 100110110011011101 --neighbors --output /tmp/core186-audit.json
cmp /tmp/core186-audit.json ramsey_r55_order3_eleven_structured_candidates/best_verification.json
```

To reproduce the fixed construction experiment at fresh external paths:

```bash
c3_run=$(mktemp -d)
c++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror \
  ramsey_r55_order3_eleven_structured_candidates/search.cpp -o "$c3_run/search"
python3 -B ramsey_r55_order3_eleven_structured_candidates/run.py \
  --binary "$c3_run/search" --work "$c3_run/full"
```

The C++ generator uses fully specified SplitMix64 arithmetic and modulo
selection. Compare each core's `restarts.tsv` and edge list with the matching
records and public fixture; elapsed times are not deterministic outputs.
The actual run binary and source identities are in [result.json](result.json).
`--resume` retains completed cores under the same frozen source/binary
contract; interrupted cores are explicitly retried from their original seeds,
preserving prior output directories. `STOP` prevents queued cores from
starting; a per-core `STOP` prevents its next restart. No background process
or pending certificate remains at this checkpoint.

## Dependencies and next direction

The selected words come from the
[complete four-core cover](../ramsey_r55_order3_eleven_four_core) and the
[17-core handoff](../ramsey_r55_order3_eleven_local_bound_propagation), with
input hashes in [inputs.json](inputs.json). The cover source is
`764720edff3c6cf2525ed9a070bee1de113e07f6`; the 17-core handoff source is
`da899a73c6719d81b61d6ab4edc6f74ca8bcdf3b`. The final Core159 exclusion has
[independent acceptance](../ramsey_r55_order3_eleven_core159_review1).
These exclusions guide where to search; their completeness is not required
to verify any graph or any finite neighbor count here.

This is the method change following the
[three UNKNOWN red-clique decisions](../ramsey_r55_order3_eleven_core194_red_clique).
It neither reopens the independently accepted BLUE closure nor adds another
Core194 SAT subdivision. The whole frontier remains 17 classes / 9,153 labels;
the three-versus-eight branch and other residual action types remain open.

New shared content was inspected through height 3294. The teammate's fixed-H92
backend now has external pointwise auxiliary-equivalence acceptance at 3287,
source `7e2118e9a77a64d264a14bc81e1c220905bb06ee` in
`math_source_code_open/ramsey_r55_antipodal_backend_review`. This does not give
a SAT verdict or a whole Ramsey-branch closure. The external M214 pair-cell
lift at 3274 and R46 cycle-shift construction at 3285 were also inspected;
none is imported into this experiment. The teammate's nonsymmetric
realization lane remains separate.

The next unstarted test is a simultaneous fixed-vertex incidence move on
the best fixture: optimize its eleven moving-triangle contacts together,
keeping all other edges fixed. There are only 2^11 assignments per fixed
vertex, and an exact subset-sum transform can evaluate the conditional
objective. This can test whether a larger structured move escapes the
certified single-orbit minimum. It is not a new parameter sweep or a claim
that the target is close; 155 remaining defects are substantial. This pass
ends with the completed batch and its explicit local certificates.
