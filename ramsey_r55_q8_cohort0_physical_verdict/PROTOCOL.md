# One complete physical cohort, four exhaustive leaves

The target of this gate is the already prepared positive q8,r8 cohort 0:

    F = M8 AND A0 AND x119,
    A0 = (-810,-819,-824,-832,-833,-836,-842,-856).

M8 is the exact complete physical43 formula of h4149. The guard A0 matches
2,184 listed original core tasks. The h4161 theorem proves M8 entails x119,
the red physical edge {3,4}, using a checked propositional normalization and
the explicitly imported classical bound R(4,5)<=25. Its negative branch is
already closed and is not recomputed here. This is the first target solver
experiment on this positive cohort; the preceding passes only prepared
inputs and reviewed the mechanism.

## Physical decomposition

Two distinct cross-edge variables x,y are selected deterministically. In
the base simplified only by A0, x119 and the true constant, a clause of
remaining width w contributes integer weight 2^(10-w) to each of its
physical literals. Rank variables 2,...,801 by decreasing minimum of their
positive and negative weights, then decreasing total weight, then increasing
variable number. Select the first variable and then the first whose physical
edge has no endpoint in common with it. This is a search heuristic, with
no claim of optimality or a complexity bound. All four signs are retained,
so the heuristic cannot lose a model.

For the pinned input, x=39 is edge {0,41} and y=74 is edge {1,37}. The
complete four-worker family, in join order, is

    F AND x AND y,   F AND x AND NOT y,
    F AND NOT x AND y,   F AND NOT x AND NOT y.

Every assignment has exactly one of these four sign pairs. The children are
therefore pairwise disjoint and their disjunction is precisely F. Each has
the entire M8 formula, all eight core-guard units, the already justified
unit119, and the two branch units. Each input has 946 variables and
1,502,532 clauses; no residual-only approximation is solved. The independent
audit reconstructs the physical variable map, checks the four sign assignments,
and compares every full input byte against the previously frozen positive
input plus its two units. The existing root input checksum is pinned.

The core in M8 remains variable. Some assignments are not listed Ramsey(4,4)
core representatives. A SAT model nevertheless gives a physical good43 if
it passes the complete model checker; a refutation of F excludes every
listed original task matching A0. The experiment does not claim that every
listed original task has a distinct model or that a SAT model has a listed
core.

## Complete proof admission

For a leaf reported UNSAT, require all of the following:

1. CaDiCaL returns code20 with `s UNSATISFIABLE` on its exact full input.
2. The pinned independent drat-trim checker accepts its binary DRAT proof,
   using `-U` to permit RUP additions only, and emits LRAT.
3. The h4149 parser accepts the positive-hint LRAT subset. Its RUP checker
   verifies both the conditional refutation and its discharged consequences.

The solver runs with `--plain`, which disables its internal preprocessing
options. Unsupported proof steps or an unsuccessful checker are errors,
never certified task dispositions. Small actual solver calls exercise SAT,
UNSAT and UNKNOWN before any target invocation. The small UNSAT trace is
checked by drat-trim and again through the parent hinted-RUP implementation.

If all four leaves have checked refutations, use h4149's complementary joins
first on y and then on x. This produces a checked refutation of
M8 AND A0 AND x119. Combine that refutation with the separately checked
h4161 theorem M8 implies x119. Propositional case analysis gives

    M8 AND A0 implies false.

The new `mixed_cover` consumer checks both premises against the same exact
base identity, requires physical edge_cube exactly [119], checks the actual
core stream hash, and computes all matching original IDs and their digest.
The resulting cover explicitly retains the imported Ramsey premise. It is
not labeled as a pure-RUP original-task certificate and is not passed to the
parent's pure-RUP `as_cover` function.

A full-base protocol control uses an impossible core K4 and consequently
matches zero listed original tasks. It tests this admission rule, not the
target gate. Wrong physical cubes, wrong r, missing proof, a forged transfer
to the real nonempty guard, and a changed imported theorem are rejected.
No nonempty original cover is claimed without the four checked target
refutations and the exact 2,184-member ID digest.

For a leaf reported SAT, h4149's `worker.target` requires the complete
assignment to satisfy the exact formula and assumptions, reconstructs every
physical edge, and checks all 962,598 five-sets for both forbidden colors.
A verified target concludes the gate immediately; unneeded leaves are not
claimed solved. An unsupported solver status or failed model check is an
error, not a candidate.

## Resource and stopping contract

Each of the four leaves receives one CaDiCaL sc2021 call, with seed0,
100,000 conflicts and a 240-second wall safety limit. Calls are sequential
and use one solver process at a time. Conflict limits may be exceeded slightly
by the solver's reporting granularity; observed counts are retained.
The final outcome is a checked original-task cover, a verified target, or
UNKNOWN with every unresolved leaf and its exact input retained. There is
no root monolithic probe, retry, cap change, deeper split, alternate backend,
or neighboring cohort in this pass. A partial proof from an UNKNOWN call is
explicitly not an UNSAT certificate.

Exclusive STARTED markers and recorded process IDs prevent automatic duplicate
execution on recovery. A new invocation refuses an existing execution marker
or leaf directory. Recovery must reconcile the existing writer and completed
receipts rather than launch the whole script again.

Correctness relies on h4149's physical encoding and proof/model checker,
h4161's separately checked theorem with its imported R(4,5)<=25 premise,
the exact software transcriptions and pinned binaries, hashes, and ordinary
hardware. These checks are by the author and do not substitute for reviewer-1.
The 161 oriented q10 children and all frozen earlier search families remain
outside this experiment.
