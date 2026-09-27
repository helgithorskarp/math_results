# Input and certificate boundary

The JSON input has exactly `source` and `target`, each a nonempty list of
three-coordinate lists. Coordinates are integers or rational strings such
as `"-3/4"`; floating values and booleans are rejected. Source coordinates
must be distinct and targets must contract every pair. Repeated source
atoms can first be merged with their weights; noncontractive or malformed
input raises an exception. Target collisions are supported.

The producer emits one record, with status:

- `CERTIFIED`: the displayed component chain proves the positive conclusions
  of PROOF.md, subject to its credited analytic inputs.
- `NOT_COVERED`: a component fails both specified sufficient primitives.
  This is neither a Gaussian counterexample nor a continuous-motion
  obstruction. In other endpoint frames it may be certified.

`precedence_edges` use zero-based labels and mean **not later than**.
`minimum_maximum_switch_batch` is the exact smallest maximum batch size
in the specified endpoint-switch chains. `blocks` are in topological order.
The identity has no blocks and minimum size0.

A positive block contains `indices` and one of:

- `kind: COMMON_ANCHOR`, with a rational3-vector `anchor` c satisfying
  |p_i-c|^2=|q_i-c|^2 for its switched labels;
- `kind: DISPLACEMENT_PLANE`, with a nonzero rational3-vector `normal`
  perpendicular to all its displacements.

A failed block contains the displacement and augmented ranks3,4 and four
`minor_indices` with a nonzero `augmented_minor`. This algebraic certificate
concerns the displayed rows [q_i-p_i | (|q_i|^2-|p_i|^2)/2] only.

The supplied-record checker accepts positive records only. It reconstructs
each stage and checks its contraction and primitive directly. The graph,
ranks, status text and minimum-size claims are not trusted by this positive
checker; they belong to the producer's classification and the written proof.
It also accepts a valid coarsening into larger certified batches. A damaged
chain, false anchor, zero normal, incomplete label partition or expanding
pair is rejected. Producer and checker use exact `fractions.Fraction`.

The full audit validates graph optimality by a different algorithm, all weak
orders, and validates displayed inconsistent minors by permutation expansion.
It does not supply a proof-assistant formalization or independent peer review.
