# Immutable decision handoff: nontrivial separators through18 are impossible

Outcome: a complete global structural class is excluded. Every separator
of size<=18 in either color of any good43 must have size18, isolate exactly
one degree18 vertex and leave a connected24-vertex component.

Use the unconditional cut rule on any global branch or any labeling:
for disjoint A,B with both sizes>=2 and total>=25, their cross edges must
include both colors. `extract.cut_clauses(A,B)` returns the physical pairs
for the positive and negative clauses. Each pair is unordered and sorted;
translate to the physical edge variables of the receiving encoding.
Do not apply the rule when one part is a singleton. It suffices to use
total25; no exponentially large explicit conjunction was generated here.

A partial assignment fixing every edge across such a cut to one color
has no good43 completion. This is a complete-family UNSAT implication
proved structurally, not a solver status. The same statement covers any
of the2,189,178 h3887 tasks, but **none of those full tasks is newly decided**
unless it entails a forbidden cut. We do not claim to have found such a
cut in a surviving packing task or measured solver speedup.

The mechanism is attachment rigidity across arbitrary12+13 components:
a complete marked-extension check forces all18 separator vertices to
share the same red8-set in the12-side; its red triangle forces the entire
separator blue, which contains a blue K5. The check regenerates all17,640
labeled R(3,4;8) graphs and all48 admissible marked12-vertex extensions.
Catalog completeness is not imported. Standard R(4,5)<=25 remains an input.

Run `python3 -B reproduce.py` in this directory. It checks the manifest
and full byte-for-byte normal/-O outputs. Run `python3 -B extract.py
fixture.json` and verify its output with `verify_five.py`. The supplied
fixture is defective and has a literal red five; it is not a candidate.
Input schema and retained boundary are documented in README.md.

Freeze this source and its SHA256SUMS together. The public source commit
and committed graph reference are carried in the external campaign delivery
receipt, since a source commit cannot contain its own hash. Receiving work
should go outside the immutable snapshot. The theorem has internal exact
validation; its external review status belongs to the delivery/checkpoint.
Physical survivor construction remains team-r55-1's lane. No good43 is
established, and no nearby separator-threshold or carrier refinement is
begun by this handoff.
