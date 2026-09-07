# Pre-computation gate: unconditional packing branch r7-s4-t3

Date: 2026-09-07

Consume the immutable h3835 unconditional 60-branch handoff at source commit
`3f06352ae0735101a04afa1ba7b055736e7300f7`.  Decide the complete physical
branch `(r,s,t)=(7,4,3)`.  This branch is selected before solving because it
has the least retained-state cardinality and the most target clauses of the
60 registered branches.  It fixes seven red four-cliques and five red
triangles and leaves all 846 cross edges as independent physical decisions.

Generate the exact h3835 formula from the frozen source.  Independently parse
and reconstruct the complete DIMACS stream without importing that source,
including the variable map, root-order clauses, fixed edges, and both target
polarities over all 962,598 physical five-sets.  Freeze hashes before solving.

Make one production CaDiCaL 3.0.1 call with a 1,800-second wall limit.  A SAT
result counts only after strict h3835 decoding plus a separate literal check
of every physical five-set.  An UNSAT result counts only after the pinned
`drat-trim` accepts the complete proof against the frozen CNF.  UNKNOWN ends
this milestone without another branch, backend, restart, or parameter ladder.

Large CNF, proof, and transcripts remain private generated evidence.  Publish
only compact source, hashes, exact outcome, and replay instructions.
