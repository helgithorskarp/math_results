# Exact four-triangle recoloring unit

For each of the1001 unordered four-subsets of the fourteen moving triples,
free all18 cross-triple phase orbits within it and all4 contacts to vertex42.
All other pairs retain the published123-defect parent. Internal triangles
remain fixed. There are22 independent bits and2^22 assignments per block.
Blocks overlap. The1001*2^22=4198498304 assignment slots are not claimed
as that many distinct graphs. All blocks use the same original parent;
there is no iterative reanchoring on an intermediate winner.

A toggled orbit is a Boolean variable y. For each physical five-set/color,
a frozen pair of opposite color makes the event impossible. Otherwise its
remaining requirements are y_i=1 on P and y_i=0 on Q, with P,Q disjoint.
Repeated physical orbit indices are collapsed, and identical events may
be merged only with physical multiplicity retained. The score polynomial
is the sum of w*y_P*product_(i in Q)(1-y_i). Expanding Q contributes
(-1)^|T| w to coefficient P union T for every T subset Q. The subset
zeta transform evaluates this polynomial at every Boolean assignment.
Thus its minimum is the exact minimum of the global physical score in
the block, not merely the score of five-sets wholly inside the13vertices.

Each table uses signed64-bit integers. A coefficient's absolute value is
at most twice962598, and any partial zeta sum has at most2^22 coefficients;
2^22*2*962598 < 2^63. A final score lies in[0,962598]. Each expected
first moment is bounded by2^22*2*962598. No decision uses floating arithmetic.
All bit shifts use unsigned types and positions below22. The physical
weighted model has at most10 distinct variables per event. Serial iteration,
sorted blocks/variables and first strict minima specify determinism.

Each table checks its unmodified123 entry, nonnegative bounded scores,
three-divisibility, and total score against the independent conjunction
cardinality sum w*2^(22-|P union Q|). Each reported minimum witness is
also evaluated directly by the model, without the transform. An independent
physical audit discovers pair orbits under g, reconstructs every reported
argmin, and literally scans the winner's962598five-sets. It uses the
previous published physical.py implementation (copied verbatim), not the
native Model or native var formula. The physical audit does not by itself
prove all unsampled production table entries/minima.

Calibration: all256 entries of the first block restricted to8bits checked
against direct physical graph clique counts; all1093 ternary event patterns
through6variables checked against literal conjunctions. First3 full22-bit
blocks match in release and ASan/UBSan rows and edge list. Eight malformed
input/scope/output cases rejected. Normal/-O physical controls match.
Calibration overlaps production and is not extra family coverage.

Freeze source after calibration, then one production run of1001blocks.
Each block completes before STOP is observed; partial status is explicit.
A zero-score witness can stop the range and must be verified physically.
Otherwise complete allblocks before the normal checkpoint. No new block
size, radius, switching census, reanchoring or follow-up batch in thispass.
Gate: a checked graph below123, a target, or a material obstruction;
otherwise preserve local reproducible results and yield for reassessment.
