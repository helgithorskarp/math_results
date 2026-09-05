# M=214 reproduction and conditional order-three restriction

For any 43-vertex graph of degree sequence `20^13 21^30` in which every
vertex has at least six neighbors in the degree-20 class, an order-three
automorphism has **at most twelve moving 3-cycles**. A short fixed-vertex
proof and a sharp degree/incidence fixture are in [PROOF.md](PROOF.md).
With the imported minimum-ten theorem for Ramsey (5,5;43) graphs, the
M=214 hard branch therefore permits only **ten through twelve** moving
cycles. This is a conditional symmetry restriction, not an exclusion
of M=214 or a new Ramsey lower bound.
The same argument requires at least three fixed degree-21 vertices.

This pass also regenerated the complete upstream M=214 OPB and checked
every constraint independently by its graph meaning. **No solver was
run on that formula here.** The previous ten-cycle four-versus-six
boundary and its 98 necessary anchor profiles remain open.

## Exact evidence and reproduction

Requirements: Python 3.11+, a C++20 compiler, and network access to seven
small pinned upstream files. Tested with Python 3.11.2 and GCC 12.2.0
on Linux. From this directory:

```sh
python3 verify.py
python3 reproduce.py --work /tmp/r55-m214-symmetry-audit
```

The first command checks exact arithmetic, all 129 tiny fixed graphs,
and the literal [degree_incidence43.edges](degree_incidence43.edges).
That graph has twelve moving cycles and satisfies the lemma's degree
and incidence assumptions. The checker explicitly finds its independent
five-set `{0,1,2,40,41}`; it is **not** a Ramsey graph or OPB model.

The second command fetches and hashes the seven upstream files,
repeats their arithmetic audit, regenerates their formula, compiles and
runs their full C++ reconstruction, then runs our separate
[check_semantics.py](check_semantics.py). It compares all compact
results with [expected.json](expected.json). Its final line is:

```text
PASS: OPB semantics reproduced; conditional order-three range 10..12; no SAT/UNSAT verdict.
```

The generated formula has 13,244 variables, 1,974,731 source rows,
128 equalities, and 167,913,049 bytes. Its SHA-256 is

```text
88aa294709836a0a707b2203da2176d420a3608353db21cc741dfa9bedf89a58
```

The semantic checker establishes complete coverage of all 962,598
five-sets using colex ranks. It infers each triangle variable's actual
three-vertex support from its four conjunction rows and uses that
inferred geometry to check every local triangle equality. It checks
all degree, exceptional-incidence, and anchor supports, every row
coefficient and right-hand side, the header, and the exact EOF.
Eight targeted corruptions of row semantics are rejected. Unlike the
upstream canonical-string reconstruction, this checker permits term
permutations and whole five-set/gate block permutations; the separate
hash pins the precise canonical source stream.

Large generated OPBs, logs, binaries, and the run report stay under
`--work`, outside Git. `reproduction.json` records timings, exact results,
and `solver_run: false`. A timeout or checker disagreement is a failed
reproduction, never an exclusion. The graph lemma has a hand proof;
its finite audit uses no external solver. None of these internal checks
constitutes independent peer review of the new lemma.

## Source provenance and trust boundaries

The reproduced source is
[the whole M=214 formulation](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_complete_formulation).
Pinned source commit: `fdba2d1000599987d545d0b83f44c46084a73b19`.
The exact input files and hashes are in
[upstream_manifest.json](upstream_manifest.json).

The needed M=214 degree-profile reduction is imported from
[doubly exact anchor propagation](../ramsey_r55_doubly_exact_anchor_propagation),
source commit `ee456bdee6a1b8636717ddf77e6b1398db0f8554`.
The caps U(20)=100, U(21)=107, U(22)=114 and the campaign's hard-branch
classification are inherited inputs. We independently rederive the
subsequent two-unit arithmetic and conditional OPB equivalence; we do
not independently certify that complete earlier classification.

The lower restriction comes from
[the nine-cycle exclusion](../ramsey_r55_order3_nine_cycle_obstruction)
and its
[accepted independent review](../ramsey_r55_order3_nine_cycle_review1).
Review source commit: `4a1c009290fb5cdc5efd2063443ec96d1621f4f3`.
The earlier partial ten-cycle result is
[the four-versus-six reduction](../ramsey_r55_order3_ten_cycle_obstruction),
source commit `e5b7d67f4a43edb1b13ed1819e1a1fcb1e2487e5`.

Ordinary mathematical reasoning, the checking implementations,
Python/C++ runtime, compiler, and hardware remain trust boundaries.
No target coloring, whole-stratum UNSAT proof, or new catalog census
is asserted.

## Bounded decision: preserve the structural lanes

The full OPB includes actual edge/triangle coupling missing from many
aggregate profile relaxations. Its direct representation is therefore
useful as a precise future target, but this reproduction supplies no
evidence that solving it wholesale is easier than structural pruning.
The external
[scalar M=214 pseudomodel](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_scalar_relaxation),
source commit `7205fe40e336de80aec92ef998411a3302065d12`, reports that
aggregate signatures and union cuts survive even though a degree/signature
realization fails the Ramsey and actual local triangle conditions.
That separate result was inspected, not rerun or independently reviewed
in this pass.

The teammate's
[paired-neighborhood budget](../ramsey_r55_paired_neighborhood_budget)
leaves seven incidence patterns in profile `19^2 20^3 21^38`, with
aggregate cell-edge witnesses. It does not close that profile. Its
actual edge/triangle compatibility frontier complements this symmetry
work and was not duplicated.

A naive conjunction of the current ten-cycle encoding with the OPB
labels is invalid as a coverage argument: the former rotates 0..29
in triples, while the latter fixes E=0..12. The orbit `(12,13,14)`
crosses the two different prescribed degree classes. Any resulting
UNSAT would only refute incompatible label choices. A future valid
intersection must conjugate the action, allocate cycles to degree
classes, and normalize the exact anchor with a coverage argument.
The nine necessary class-count patterns are recorded in
`expected.json`; they are not realized or certified-excluded cases.

Decision: retain the symmetry lane. After team coordination, resume
the existing 98-profile ten-cycle boundary, or construct a correctly
aligned conditional M=214 projection. No new cube sweep, seven-fixed-
vertex enumeration, whole-OPB solve, or major stratum has begun in this
completed reproduction/decision checkpoint.
