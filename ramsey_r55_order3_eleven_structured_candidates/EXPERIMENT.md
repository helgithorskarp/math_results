# Bounded C3 structured-construction experiment

Population: the seventeen surviving eleven-cycle, four-red/seven-blue core
representatives listed in cores.tsv. These are representatives inherited
from the complete core cover and the subsequent whole-core exclusions;
this experiment does not prove or extend that cover. For each representative,
fix exactly its eighteen cross-triangle orbit values, the eleven internal
triangle colors, and the C3 action on 43 vertices. All other 302 orbit bits
may change, including every fixed-vertex incidence and edge. No degree
profile, fixed-empty condition, opposite graph or further symmetry is imposed.

Objective: the literal number of monochromatic five-sets, counting each
physical set once. The search enumerates all 962,598 five-sets. Those already
containing both fixed internal colors cannot be monochromatic and contribute
zero. For each remaining possible color, form the sorted distinct set of
variable orbits whose edges must have that color. Equal (color,support)
constraints are combined, with weight equal to their number of physical
five-sets. This weight is essential: the objective is not the number of
unsatisfied distinct clauses. The resulting exact weighted objective has
529,157 supports, 756,777 possible red sets and 842,952 possible blue sets.

For a constraint, sat is the number of its variables differing from its
forbidden color. A zero-sat constraint contributes its weight to the score
and to make for every member; a one-sat constraint contributes its weight
to break for its unique differing member. Flipping v changes the objective
by break[v]-make[v]. Every incident count and XOR of differing IDs is updated.
Every chosen move checks this gain identity. Full reconstruction checks occur
every 5,000 steps and at every restart boundary. Signed quantities are bounded
by the sum of all weights (1,599,729), far below 32-bit limits. Randomness uses
specified SplitMix64 unsigned operations modulo 2^64 and modulo selection;
this deterministic selection is not a uniform sampling claim.

Protocol fixed before production: four restarts per core, 25,000 orbit flips
per restart, two worker processes; 68 restarts and at most 1,700,000 flips.
Seed for (core,r) is 20260906+1000003*core+r. Initialization uses successive
generator bits on all 320 variables and then restores the eighteen core bits.
The first pilot seed is intentionally included in this deterministic batch;
pilots are calibration, not additional independent production restarts.

Move rule: when next()%100 is zero, choose any free variable by modulo sampling.
Otherwise compare exact gains over all free variables, excluding those flipped
in the last seven steps unless the move improves the restart best. Select
by modulo among minimum-gain ties. If that gain is nonnegative,
when the next residue modulo 100 is below 20, override it by a variable in a modulo-selected
currently violated distinct support. This focused escape can ignore the tabu
condition. No empirical uniformity or optimality is asserted. Preserve the
first occurrence of every strict best and its explicit sorted edge list.

The initial focused-only pilot and a second global-gain pilot each used Core92,
one restart and 2,000 steps. Their best scores were 396 and 199; this is a
single-seed algorithm calibration, not a comparative performance theorem.
Their release/sanitizer outputs agree, and the physical literal and recursive
audits agree on both scores. The production source uses the global-gain rule.

The independent verifier imports no search/model/primary-index code. It checks
all physical pairs under the action, the core and internal colors, and every
literal five-set. A separate bit-intersection clique recursion reproduces the
entire list of defects in both colors. It also discovers the physical orbit
moves and can enumerate all 302 one-orbit neighbors of a saved coloring.
That optional census proves only a neighborhood statement for that coloring,
never minimality of the family. Malformed edge lists/action/core are rejected.

Stopping: finish this entire fixed batch and its candidate audits, or stop
queued work if a zero-score candidate appears. Every candidate target requires
the independent literal audit and a compact edge list before any existence
claim. Production emits atomic per-restart records and per-core completion
state. A STOP between restarts preserves completed work; interrupted cores
can be deterministically reproduced while retaining their partial outputs.
No second parameter sweep, radius, core family, or solver proof phase belongs
to this pass. No failed heuristic run or nonzero best proves nonexistence.
