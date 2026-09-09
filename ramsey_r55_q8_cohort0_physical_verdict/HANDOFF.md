# Measured UNKNOWN: preserve and stop this exact gate

The existing q8,r8 positive cohort 0 has now received its first actual target
solver test. All four exhaustive signs of variables39={0,41} and74={1,37}
were solved once, sequentially, with the full M8 formula, its eight core
assumptions, and the already justified +119 unit. Each leaf had a fixed
100,000-conflict budget and 240-second wall safety limit, using the pinned
CaDiCaL sc2021 `--plain --seed=0` configuration.

All four calls returned UNKNOWN at their conflict budgets. Recorded counts
are 100000, 100002, 100004 and 100002; wall seconds are 78.5391, 53.9338,
60.6609 and 52.7142. Total: 400,008 conflicts and 245.8481 solver seconds.
There are zero verified target leaf proofs, zero original-task exclusions,
and zero candidates. All 2,184 original cohort members remain UNKNOWN.
The existing 518 / 2,188,660 global administrative counts are unchanged.

The pre-target gap identified in the prior mechanism review was exercised:
the actual backend produced small SAT, UNSAT and UNKNOWN controls; the
UNSAT trace passed RUP-only drat-trim and the parent positive-hint LRAT
checker. The explicit mixed-premise cover rule checks a positive [119]
worker refutation together with h4161's imported-Ramsey-bound theorem.
Its full-base control matches zero actual original tasks, and a forged
transfer to the real cohort is rejected. No nonempty original cover was
obtained. No target UNSAT trace was available for the full join path.

Mechanism review at this boundary: the encoding, complete four-leaf cover,
input transport and intended proof/model path are concrete. This experiment
provides no evidence that the remaining cohort is tractable under this
partition. Additional proof-interface work alone does not replace a physical
verdict. The current four-leaf gate is finished and parked. Do not retry it,
increase its cap, deepen or change its split, change backend, inspect its
partial traces for another nearby unit-mining phase, or move to an adjacent
cohort from this checkpoint.

All exact CNFs, solver logs, partial DRAT traces, receipt hashes and source
snapshots are retained locally in an immutable checkpoint. STARTED markers
prevent automatic duplicate execution. The active original queue statuses
are preserved; this gate is recorded separately as a parked physical
subtree so its four leaves are not confused with four original tasks.

This source publishes the reproducible attempt and exact measured UNKNOWN.
It makes no new mathematical Discovery Net claim. The q10 queue, frozen
families and teammate workspace were untouched. Independent reviewer-1
review is distinct from all author checks reported here.
