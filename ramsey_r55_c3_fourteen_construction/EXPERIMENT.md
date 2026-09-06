# Fourteen-cycle construction: one bounded unit

The family and gate are fixed before production. Vertices 0..41 form
fourteen triples under g=(0 1 2)...(39 40 41); vertex42 is fixed.
Triangles0..6 are red and7..13 blue. Between any two triples there are
three phase orbits; each has three physical pairs. All273 cross-triangle
orbit colors and14 contacts to vertex42 are independent, for287 bits.
This specifies exactly2^287 distinct labeled graphs. No additional
symmetry, degree, neighborhood or selected minority core is fixed.

This construction does not switch a saved graph. Each cross phase can
change independently, so odd triangle parities can change. It is not a
new census of a completed switching family or the parked radius-six
catalog. It is not claimed that every member of this broad family avoids
every excluded switching-extension family; any comparison of a particular
winner must state the exact embedding and relabeling scope checked.

The gate is a directly checked43-vertex Ramsey target, a global score
below155 monochromatic five-sets, or a complete family exclusion/material
structural reduction. If the bounded experiment misses the gate, preserve
its reproducible local state and yield for reassessment, without presenting
an unsuccessful heuristic run as an exclusion.

Production:16 independent starts, seed202609061+r for r=0..15, each at
most25000 orbit flips. Two2000-step calibration starts use seeds202609069
and202609070 under release and address/undefined-behavior sanitizer builds.
These calibration steps overlap production seeds and are not additional
independent trials. They check execution and scaling before production.
All production inputs and source identities are frozen after calibration.

The exact objective counts physical red and blue K5s. For each five-set,
fixed internal pairs can prohibit one or both colors. Otherwise collapse
repeated free orbit indices into a support and count the forbidden
all-zero or all-one assignment. Identical supports/color events are
merged with their physical multiplicity, never counted only once.

The optimizer reuses the predecessor's bounded heuristic: SplitMix64,
global make/break gain comparison, seven-step tabu with aspiration, a
one-percent uniform escape and a twenty-percent bad-event move when the
best gain is nonnegative. All287 bits are free. Every predicted score
change is checked; complete incremental state is reconstructed every5000
production moves and at restart boundaries. Scores and gain entries are
bounded in absolute value by962598, safely within signed32-bit arithmetic.
Indices fit0..286; each physical support has at most10 entries. SplitMix64
uses explicitly unsigned arithmetic modulo2^64. No floating-point value
affects a move; floating time is observational metadata only.

The first strictly best graph is saved. Every restart's seed, initial
score, best score/step and full287-bit best assignment is retained.
The batch finishes all16 starts unless a zero-score candidate appears.
STOP prevents another restart; partial status cannot imply full coverage.
No additional restart batch, action type, switch census or larger cap
begins in this pass. Complete the graph audit and warranted publication,
then yield.

The verifier imports no optimizer, objective supports or primary indexing
formula. It reconstructs physical pair orbits under the action, checks all
903 pairs, all internal colors and every saved best assignment, compares
all initial/best scores by clique recursion, and literally enumerates all
962598 five-sets of the winner. The complete red/blue lists must match a
separate bit-intersection clique recursion. An explicit graph plus this
audit, not search correctness, supports any achieved score claim.
