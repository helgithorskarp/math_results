# Pre-computation gate: all rank-four row tasks, support at most eight

Date: 2026-09-07

Use the independently reviewed h3825 table of all 10,959 canonical A20 row
tasks.  Build one physical K43 formula in which the task selector, all B23
factor labels, and all 443 internal edges remain variables.  Restrict only the
total number of distinct B labels (including zero) to at most eight.  Preserve
the exact h3825 factor caps, both-color cut-rank condition, every physical
five-set, h3579 equal-label pair distances, h3771 tripled-row contacts, and the
degree interval 18--24.

This is one broad support stratum across the entire canonical row cover.  Do
not split by a hand-picked row multiplicity profile or move to support nine in
this pass.

After independent encoding controls and a frozen CNF hash, make one production
CaDiCaL call with a 900-second wall limit.  A SAT result must decode to an
independently verified 43-vertex graph.  An UNSAT result counts only after an
independent DRAT check.  UNKNOWN is a reproducible boundary result and must not
be followed by another solver, cap increase, support ladder, or task shard in
this pass.

Large CNF, proof, and transcript files stay in this private scratch directory.
Only compact source and evidence are candidates for publication.
