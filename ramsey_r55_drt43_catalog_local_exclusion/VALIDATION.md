# Validation and trust boundary

## Input audit

`audit.py` checks the exact SHA-256 digest and all 2,178 distinct 903-bit
records.  Under the documented upper-triangle decoding, it verifies every
outdegree is 21 and every pair of vertices has exactly 10 common
outneighbors.  These are the DRT(43) identities used by the family statement.

The Python audit separately reconstructs the complete CNF byte stream for
four spread-out `(record,root)` controls.  Their hashes match the C++ emitter.
The production C++ compiler flags include `-Wall -Wextra -Werror -pedantic`.

## Proof checks

The complete run covers exactly the Cartesian product
`{0,...,2177} x {0,...,42}`.  Every local proof is accepted by `drat-trim`
before its row contributes to the summary.  A `SAT`, solver-limit `UNKNOWN`,
malformed catalog record, missing proof, or rejected proof stops the shard and
retains the current CNF/proof/log files for diagnosis.  The merge script
rejects incomplete, overlapping, or out-of-range shards.

The ten production shards completed in 2,462.023472 seconds of wall time.
They generated 548,087,198 CNF clauses and 2,482,356,972 proof bytes in total;
the proof files were counted after successful checking and then removed.

The fixed policy is 100,000 conflicts for each of the 21 local-first
assumptions and another 100,000 conflicts for the final solve.  No cap was
extended and no result was inferred from a timeout.

Development controls included:

* byte-for-byte agreement between the C++ and independent Python CNF
  generators on records/roots `0:0`, `1:0`, `1089:21`, and `2177:42`;
* a separate 93,654-instance CaDiCaL screen using direct comparison variables
  and fixed-first assumptions, which also returned zero SAT and zero UNKNOWN;
* a 1,849-variable combined-root CNF for record 1, solved by Kissat and
  independently verified from a 58,638,905-byte DRAT proof by `drat-trim`;
* an AddressSanitizer plus UndefinedBehaviorSanitizer proof-producing run,
  strict-warning release compilation, malformed-input rejection, and an
  explicit truncated-proof control for which `drat-trim` returned
  `s NOT VERIFIED`.

The combined-root proof was a control only.  It is not needed by the theorem
or retained as a published premise.

The direct screen can be replayed independently of the proof-producing
selector encoding.  After compiling `direct_screen.cpp` against the same
CaDiCaL library, its interface is

```text
direct_screen CATALOG FIRST_RECORD RECORD_COUNT MAX_ROOTS
```

The eight deterministic ranges and complete transcript hashes are recorded in
`DIRECT_SCREEN.tsv`; production used `MAX_ROOTS=43`.

## What is and is not certified

The checked computation certifies every formula generated from the pinned
2,178-record file.  `RESULT.tsv` is a compact execution transcript rather
than a replacement for the transient DRAT streams; `run_full.py` regenerates
and checks those streams.

The external classification boundary is explicit: McKay's source page says
the order-43 DRT list is incomplete.  No inference is made about omitted
DRT(43)s.  Trust otherwise comprises the mathematical encoding argument,
source inspection, the pinned input bytes, CaDiCaL's proof production,
`drat-trim`'s DRAT checker, the compiler and Python runtimes, operating system,
and hardware.  This is author-side computer-assisted certification, not
independent peer review or formal proof-assistant verification.
