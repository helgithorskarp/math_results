# Validation and exact scope

The complete-class decision rests on the proof in PROOF.md, Fouquet's
decomposition theorem, and the Strong Perfect Graph Theorem. The external
theorems are imported from the linked primary sources. The weighted
replication argument and the reduction from all 43-vertex class members
are given explicitly. No theorem is inferred from random graphs or from
the order of a saved graph. No proof-assistant formalization or independent
peer review of this contribution is claimed.

Tested with CPython 3.11.2 and its standard library. Computation uses only
unbounded integers and exact rational numbers. The independent checker
uses integer cross multiplication instead of the producer's Fraction
objects. Assertions, SAT status, external graph catalogs, and floating-point
rounding are not proof premises.

The independent checks are:

- All 16 cap rows, complete domains, monotonicity, all rational envelopes,
  and the strict parameter decrease needed for induction.
- A single 59,049-vector enumeration using every literal clique and
  independent set of C5. It finds 3,249 vectors admitted at caps (4,4)
  and compares all 4,761 incidences with cap rows, including every
  maximizing vector rather than only the maximum values.
- Direct verification of all 16 attaining graphs: 151,278 tests of clique
  and independent-set sizes and 62,875 five-sets. The order-25 graph alone
  contributes 53,130 five-sets; it has 150 edges and degree 12 everywhere.
  Exact substitution trees and packed edge words are compared literally.
- All 1,024 five-vertex graphs checked against a separate set of 60
  permuted P5 edge words and their complements. This distinguishes a path
  from a disconnected graph with the same degree sequence.
- The weighted perfect-quotient inequality on all 64 four-vertex graphs
  and all 256 pairs of positive binary weightings, 16,384 cases. C5 with
  unit weights explicitly fails the inequality when perfection is omitted.
- Four corrupt table mutations and three corrupt witness mutations are
  rejected, including the false asymmetric bound 15 and the false top
  bound 24.
- Sixteen full 43-vertex interface controls, using both colors and
  permuted labels. Twelve have a path/complement-path-free 26-core and
  a checked physical monochromatic five-set; four contain a supplied-core
  path and receive no target verdict. Each admitted core checks all
  65,780 five-sets for membership. The exterior contacts are arbitrary
  deterministic fixtures, not candidate construction runs.
- Six malformed family inputs and six corrupted five-vertex certificates
  are rejected. The certificate verifier checks all ten physical pairs
  using a closed-form pair index instead of the interface's pair table.

The source replay regenerates TABLE.json and WITNESSES.json and compares
CHECK.json and CONTROLS.json byte-for-byte in normal and optimized Python.
All files are hashed first. It executes zero solvers and zero target
searches. The later receiving-copy replay checks the same pinned source
without changing any earlier frozen handoff.

The finite controls support implementation correctness. They do not
enumerate every graph in the infinite hereditary class. The universal
coverage is the structural argument with the stated imported premises.
No extrapolation to extensions of C5[C5], solver tractability, removal of
entire h3887 tasks, or existence/nonexistence of a general good43 is made.
