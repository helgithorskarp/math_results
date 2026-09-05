# Complete full-extension formulas for the 79 residual core classes

Consider a hypothetical Ramsey (5,5;43) graph with an order-three
automorphism having eleven moving triangles and ten fixed vertices.
In the four-versus-seven branch, four triangles are internally red
and seven internally blue. The reviewed blue-K4 obstruction leaves
exactly 79 possible minority-core action classes. This package gives
one bounded full-extension decision attempt for every one of them.

The precise exclusions and open cases are recorded in `result.json`.
A timeout is an open case. It is not a nonexistence certificate, and
completion of a bounded sweep is not the exclusion of every case.

## Reviewed cover and normalization

The [197-class core cover](../ramsey_r55_order3_eleven_four_core) gives
representatives for all locally valid twelve-vertex red-triangle cores.
The [full-extension blue-K4 theorem](../ramsey_r55_order3_eleven_blue_k4_exclusion)
excludes 118 classes, leaving the 79 entries in its `retained` list.
Both the exclusion and the load-bearing full-parent normalization of
the catalog now have an
[accepted independent review](../ramsey_r55_order3_eleven_blue_k4_exclusion_review1).

These classes concern a marked cyclic action. Any full graph in the
branch can be relabeled so its four-red-triangle core is one of the
listed representatives, its blue-cycle anchor words are normalized
and sorted, and its ten full eleven-bit fixed rows are sorted. The
minority normalizer uses permutations, independent rotations, and
inversion extended to ALL eleven moving triangles. Later blue-cycle
and fixed-vertex normalizations leave the selected minority core
unchanged. The prior review checks this complete coverage bridge.

The new sweep adds no further symmetry restriction. In particular it
assumes no fixed signature counts, fixed-only edge pattern, hard
degree profile or selected additional core. It imports none of the
three-versus-eight two-empty-signature or pair-color constraints.
Catalog indices in this package are four-versus-seven indices; they
must not be confused with the two open three-versus-eight cores.

## Exact complete formulas

The accepted r=4 parent from
[the eleven-cycle reduction](../ramsey_r55_order3_eleven_cycle_obstruction)
has 34,280 variables and 615,920 clauses, SHA256

```text
c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f
```

It retains all 43 vertices, all monochromatic-five-set restrictions,
the local moving-triangle constraints, both color-degree bounds,
counters and justified normalization. It has 320 primary variables,
331 edge orbits including constant internal colors, and 529,157
Ramsey clauses before its additional constraints. The external input
R(4,5)=25 gives the full degree window 18 through 24; that theorem
and the parent's normalization/counter bridge are inherited.

For core bits in word order 01,02,03,12,13,23, with offsets 0,1,2
within each word, append exactly eighteen units to the ENTIRE parent:

```text
01: 1,2,3       02: 4,5,6       03: 7,8,9
12: 31,32,33    13: 34,35,36    23: 58,59,60.
```

A red bit appends a positive unit and a blue bit a negative unit.
Each final formula has 34,280 variables and 615,938 clauses. No
parent clause is replaced, weakened, or removed. Every source graph
in a selected core class has, after the reviewed relabeling, a
satisfying assignment of its complete formula. Consequently a valid
UNSAT certificate excludes that entire full-extension class.

The generator copies the complete parent body and appends the units.
The independent cube auditor reconstructs primary meanings by literal
unordered-pair orbits of the full 43-vertex action, including all
moving-cross, fixed-fixed and fixed-to-moving primary variables. It
then checks the exact new header, every byte of the full parent
prefix, all eighteen units and final EOF. At preparation the full
parent is regenerated from source and independently reconstructed
clause by clause by the inherited C++ checker. It must match the
reviewed parent hash before any solver case begins.

## Solver outcomes and certificate obligations

The reference sweep uses two workers, a ten-second Kissat solver
limit per core, and a 300-second DRAT-check limit. The finite domain
is the entire reviewed list of 79 residual classes. Solver timeouts
do not extend automatically or trigger a second search phase.

An UNSAT solver exit is accepted only after `drat-trim` verifies its
complete proof against the exact audited formula. General DRAT is
used, including RAT steps when present; a RUP-only substitute is
not sufficient for such traces. A fresh verification run regenerates
the entire parent and every one of the 79 complete formulas, checks
their hashes and unit meanings again, and replays every successful
proof a second time.

A SAT exit must decode to a compact 43-vertex red edge list and pass
the inherited independent literal graph inspector. Any validated
target stops further cases from beginning. Unexpected exits, invalid
proofs, malformed candidates or source drift are errors and cannot
be recorded as exclusions. An open case requires both solver exit
zero and an explicit `s UNKNOWN` log entry.

Thus the mathematical exclusions consist exactly of the rows whose
complete proofs pass verification. Each reported open row remains
unresolved, regardless of the amount of search performed. Solver
wall-time variation can affect a rerun's timeout outcomes. Different
traces or verdicts must satisfy the same certificate obligations;
timing or a saved hash alone never proves UNSAT.

## Controls, checkpoints and limits

Five malformed full-formula controls are rejected: a missing unit,
reversed unit polarity, an inserted empty clause, a changed parent
prefix and an extra trailing clause. Normal and optimized Python
controls agree. The parent also reruns its inherited local arithmetic,
counter and normalization controls before the sweep.

Each completed case is saved atomically. The fixed contract records
source/input hashes, Python, solver/checker binary hashes, two-worker
execution and both time limits. A `STOP` file prevents additional
cases from starting while active cases finish. Resume requires the
same contract; completed open cases retain their original limit and
are not rerun. A stopped or failed sweep is explicitly incomplete.
Partial UNKNOWN traces are not solver checkpoints or proof certificates.

Full CNFs, traces, logs and binaries remain outside Git. The compact
source and outcome manifests reproduce the formulas and proof run.
No raw bulk output is part of the default public artifact. The
published trace hashes identify the local checked evidence, but are
not a substitute for generating or obtaining traces and replaying them.

The cover and imported parent are independently reviewed. The new
case refutations have internal full replay and fresh reconstruction;
their own independent review status is stated in the README. Remaining
trust includes the imported R(4,5) theorem, unformalized reduction and
normalization reasoning, the exact generator/auditor sources, Python,
C++ compiler/runtime/hardware, SHA256 and the external DRAT checker.
There is no proof-assistant formalization or historical-priority claim.

This package is one bounded milestone. It does not authorize a larger
timeout, a further core subdivision, another radius or another internal
color split within the same pass. The three-versus-eight branch remains
outside its search domain.
