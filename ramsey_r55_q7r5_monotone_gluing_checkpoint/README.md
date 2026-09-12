# Complete q7,r5 family: monotone gluing checkpoint

**Recorded result: UNKNOWN after 1,800.855740 seconds. All 122 retained
original tasks remain UNKNOWN; no original ID or physical cohort was
retired, and no good43 was produced.** The unfinished 1,059,287,040-byte
DRAT trace is preserved with its hash but has not been accepted as a proof.
The closing original-task decision gate was missed.

This package records a full43 formulation covering **all 122 retained original
q7,r5 tasks**, with every residual and attachment free. It preserves a precise
conditional join to the literal original IDs. It does not treat input
validation, an unfinished trace, or six-vertex controls as an original-task
exclusion. The previously established 518 q7,r5 exclusions and three newer
q8 original closures are separate, unchanged results.

The mathematical change is a normalization within each original task: delete
red edges from vertex 0 to the 15-vertex core while preserving blue-K5-freeness.
Every remaining red edge then has a physical blue K5-minus-that-edge witness.
The core and all original ordering constraints remain fixed. The new witness
clauses are **existence-preserving normalization constraints, not original
parent implicates**. [PROOF.md](PROOF.md) gives the finite-descent theorem,
the full-family encoding, the exact clause projection, and the admissible
UNSAT and SAT joins.

The formula has 861 physical variables, 115,104 total variables, and 2,576,821
clauses. Its 84,254,429-byte DIMACS input has SHA256
`bc5ccf4fd4fb6ca0c0e84d3773343039501e2a3bd601a17dff8c3dc2b7f3f92d`.
[ORIGINAL_INPUTS.json](ORIGINAL_INPUTS.json) contains all 122 exact original
IDs and complete 817-variable input hashes. The normalized input is the one
whole-family search unit; the specialized original inputs are identifiers
and join evidence, not separately run or newly excluded tasks.

## Replay the input and join evidence

Use Python 3.11 and a C++17 compiler; exact recorded versions are in
[TOOLS.json](TOOLS.json). The required external catalogue is McKay's
[`r44_15.g6`](https://users.cecs.anu.edu.au/~bdm/data/r44_15.g6), with SHA256
`53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1`.
Keep it in a catalogue directory outside the source checkout. The existing
carrier source packages must be present as siblings, as in this repository.

Run these commands from the repository root, replacing the absolute scratch
and catalogue paths with fresh local paths:

```sh
python3 -B ramsey_r55_q7r5_monotone_gluing_checkpoint/model.py \
  --repo . --cache /path/catalog --out /new/path/run
python3 -B ramsey_r55_q7r5_monotone_gluing_checkpoint/audit.py \
  /new/path/run . /path/catalog
g++ -O2 -std=c++17 ramsey_r55_q7r5_monotone_gluing_checkpoint/project.cpp \
  -o /new/path/project
python3 -B ramsey_r55_q7r5_monotone_gluing_checkpoint/parent_inputs.py \
  --repo . --cache /path/catalog --run /new/path/run \
  --projector /new/path/project
python3 -B ramsey_r55_q7r5_monotone_gluing_checkpoint/controls.py
```

Expected statuses are `VERIFIED_COMPLETE_122_PARENT_NORMALIZED_INPUT`,
`ALL_122_EXACT_ORIGINAL_INPUT_IDENTITIES`, and
`VERIFIED_NORMALIZATION_IMPLEMENTATION_CONTROLS`. None says UNSAT. Generation
took 12.32 seconds; the independent physical input audit took 29.06 seconds;
the original-stream projection and hashing took 45.42 seconds. The portable
parent replay matched every recorded original byte-stream hash in 45.47
seconds and checked every core bit against the pinned original producer.
It shares the native projector and is regression evidence, not an independent
second implementation. The independent physical audit imports neither the
producer nor a solver.

The public Python entry points reject `-O` and `-OO`, since their exact checks
use assertions. This explicit guard is the only change to the executed
producer and physical auditor; their mathematical ASTs were compared after
removing the guard. The executed source hashes are retained in
`EXECUTED_SOURCE.json`. The native projector also passed a warnings-enabled
AddressSanitizer/UndefinedBehaviorSanitizer check over the complete core-4
original stream, with no diagnostics; see `SANITIZER.json`.

The control program checks the normalization on all 32,424 good colorings
among all 32,768 six-vertex colorings, using direct forbidden-five masks to
check the resulting graph. It also rejects three damaged certificates.
These are implementation controls, with no claimed R(5,5) scope.

## Recorded decision attempt and continuation boundary

One CaDiCaL 1.9.5 process ran on the full normalized input, using
`cadical --no-binary input.cnf proof.drat`. The predeclared limits were
1,800 seconds wall time and 20 GiB of proof output. The wrapper sends SIGTERM
at either limit and SIGKILL after a further 20 seconds if necessary. No
alternative core, solver backend, or increased cap was tried.

The terminal status and exact input, trace, and log identities are recorded
in `RUN.json`. A terminal UNSAT would require independent checking against
the full input before the same-ID normalization theorem could retire the
122 parents. A terminal SAT would require a literal all-903-edge good43
check and acceptance by the original carrier checker. The omitted raw input,
proof trace, logs, executable, and operational checkpoints remain in the
researcher's bulk workspace; they are not Git artifacts. An interrupted
solver trace is not a resumable CDCL state or a reusable proof certificate.

The source and normalized-input hash preserve the mathematical search frontier.
A future computation would require an explicitly authorized fresh proof
attempt; it cannot append a proof to an unchecked old trace or count solver
search branches as original exclusions.

## Context and trust

This is a carrier-consumption attempt, with no novelty claim for monotone
normalization or SAT gluing. The campaign's verified published upper bound
is supported by [Angeltveit and McKay](https://arxiv.org/abs/2409.15709).
[Gauthier's 2025 strategy](https://aitp-conference.org/2025/abstract/AITP_2025_paper_3.pdf)
already studies full43 gluing and abstraction across configurations. This
package does not infer tractability from that prior work or from smaller
residual solves.

R1's [monotone-chain carrier](../ramsey_r55_monotone_chain_carrier) supplies
related within-task monotonicity context. Its chain restrictions, factors,
and conditional certificates are not inserted here. The earlier cross-core
complete-cover redirect is also not used. The inherited external catalogue
and original carrier coverage, the ordinary unformalized normalization proof,
and the executed code are explicit trust boundaries. No independent peer
review or proof-assistant verification is claimed for this package.
