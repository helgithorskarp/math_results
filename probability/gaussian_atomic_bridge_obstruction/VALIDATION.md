# Validation and trust boundary

The checker uses Python integers and `fractions.Fraction`. There are no
floating-point operations, package dependencies, random choices, or solver
calls. CPython 3.11.2 was used, both normally and with `-O` to ensure that
no mathematical check depends on removable assertions.

`python3 verify.py --check` must return
`ATOMIC_BRIDGE_OBSTRUCTION_EXACT_AUDITS_PASS` and exactly match EXPECTED.json.

The finite obligations are:

* all 36 labeled squared-distance losses, and distinct positive atom masses;
* definition-level enumeration of all `9! = 362880` support bijections,
  compared entry by entry with the independent square-symmetry description;
* exact paired ranks for all 64 contracting bijections;
* exact permutation mass norms, the separating margin `1/8464`, and an
  attaining rank-five reflection;
* the rank-eight linear projection constraint, moving circuit, and Gram
  minor 16 used in the prior geometric obstruction;
* both centered covariance matrices recomputed directly from the weights,
  LDL reconstruction and signs, independently cross-checked using integer
  leading principal minors;
* the L1 perturbation and approximate-output constants;
* a repeated-weight rank-four fold as a boundary control, a noncontracting
  permutation rejected, and a zero-pivot inertia certificate rejected.

The checker does not enumerate continuous motions or all weight vectors.
Their treatment is the written linear-algebra and perturbation proof.
Its finite enumeration is complete only for bijections between the two
specified nine-point supports. It does not classify the full motion status
of all 24 paired-rank-six bijections.

The universal atomic rigidity statement and the square-cone motion obstruction
are explicitly credited prior results; their proofs are repeated for clarity.
Successful checking, source publication, and graph commitment are not
independent peer review or a proof-assistant verification.
