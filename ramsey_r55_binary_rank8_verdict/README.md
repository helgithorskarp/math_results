# Binary-rank-eight physical branch: unresolved bounded attempt

**Status: UNKNOWN. The predeclared gate was not met.** One complete global
branch was encoded and audited, but the single solver run reached its
600-second limit without a target or an UNSAT verdict. No rank-eight
exclusion, stronger rank bound, candidate effect, or registry reduction is
claimed. No new mathematical result is submitted to Discovery Net.

The family consists of **every simple 43-vertex graph with adjacency rank
at most eight over GF(2)**. There is no prescribed automorphism, historical
source graph, fixed neighborhood, or host symmetry quotient. The exact
coverage argument in [PROOF.md](PROOF.md) uses an alternating-form
factorization. Under the good43 hypothesis its coordinates are distinct
and nonzero, so the complete branch becomes a selection of at least 43
of the 255 nonzero vectors of GF(2)^8. All pairings are retained.

The selected labels must contain no five-set whose ten alternating
pairings are all zero or all one. A feasible selection would give a
literal good43; independently checked UNSAT would exclude this entire
branch. Neither occurred. The previous rank-six obstruction is preserved;
the present result does not raise its lower bound of eight.

## Complete input and validation

There are 6,409,935 blue forbidden five-sets and 8,773,632 red forbidden
five-sets. With an exact prefix-threshold cardinality encoding, the CNF
has 10,317 variables and 15,223,518 clauses. It is 378,449,132 bytes and is
regenerated in scratch rather than stored in Git.

CNF SHA256:

    a5e64575f563ab25c7d3368dd9e9aff9155bb68ec0a2f66ca1e30e9355b42174

The producer enumerates common-neighbor intersections and independently
checks the total by four-set faces. A reverse auditor uses algebraic
counts, checks every literal five-set with a separate pairing
implementation, and rejects duplicates. The complete release and
ASan/UBSan audits pass. Six corrupted formula inputs are rejected.

The cardinality encoding is checked on all 16 local Boolean states and
3,586 small prefix/threshold assignments. Alternating factorization is
checked against independent Gaussian elimination on all 33,867 labelled
graphs of orders one through six, in both Python modes, and on a rank-eight
control containing zero and repeated coordinates. These are encoding
controls, not physical Ramsey candidates.

The integrated solver-free replay took 27.873 seconds and reproduced the
exact CNF hash. It validates the encoding, not the requested physical
verdict. Detailed scope is in [VALIDATION.json](VALIDATION.json).

## Single target run

CaDiCaL `sc2021`, one thread, was capped at 1,000,000 conflicts,
600 real seconds, 12 GiB address space, and a 4 GiB proof file.
It returned code 0 after 600.772 seconds measured by the launcher.
The solver reported 153,037 conflicts, 241,904 decisions, 121,146,798
propagations, and peak resident memory 2,998.24 MB.

[RESULT.json](RESULT.json) records UNKNOWN. The 20,852,892-byte unfinished
DRAT stream is preserved locally with SHA256

    2dfbe89f361001522fa65191d4702449092fc5d82bda043b1cda09d44617ee6f

It is **not an UNSAT certificate** and was not submitted for UNSAT proof
verification. Positive and deliberately false DRAT tool controls were
checked before the target run. No target solver was rerun. The published
launcher additionally checks the exact input SHA256 before starting a
solver; this guard was added after the original audited run and tested
with a wrong input that was rejected before any solver launch. The original
driver source is frozen in the local checkpoint.

## Reproduce the input without solving it

Python 3.11.2 standard library and g++ 12.2.0 suffice. From the repository
root, select a fresh scratch output path:

```sh
python3 -B ramsey_r55_binary_rank8_verdict/reproduce.py \
  --out /tmp/r55-rank8-input
```

This regenerates and verifies the complete CNF and runs the algebraic and
Boolean controls. It does not run a target solver or download graph data.
An existing output path is refused. The expected final status is
`COMPLETE_BRANCH_ENCODING_REPRODUCED_NO_PHYSICAL_VERDICT`.

For provenance, the original bounded command is represented by:

```sh
python3 -B ramsey_r55_binary_rank8_verdict/run_once.py \
  /tmp/r55-rank8-input /path/to/cadical /path/to/drat-trim
```

This is a record of the experiment, not an instruction to reopen it under
the current campaign mandate. The launcher refuses a second invocation in
the same output directory. Both an actual solver UNSAT result and successful
independent DRAT verification would be required for a whole-branch
exclusion. A SAT result requires literal physical verification on all
962,598 five-subsets. The declared limits are in [GATE.json](GATE.json).

## Boundary and preserved work

The accepted h4059/h4069/h4081 structural base and the completed h4089
negative residual test remain intact. The separate q7,r5 result remains
518 whole-task exclusions; 2,188,660 original whole tasks remain undecided.
Team-r55-1 retains its 161 q10 children, with no input access or ownership
transfer in this attempt. Child redirects are not task exclusions.

The pass stops at the unresolved declared gate. No larger cap, alternate
backend, coordinate pinning, orbit quotient, neighboring rank, or nearby
follow-on search is launched. [CONTEXT.json](CONTEXT.json) records the
structural predecessor and source scope. No historical priority,
independent peer review, or proof-assistant formalization is claimed.
