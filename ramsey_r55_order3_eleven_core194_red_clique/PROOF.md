# Exact RED empty-clique cardinality cover for Core194

In the eleven-cycle four-red/seven-blue Core194 family, the independently
accepted BLUE-pair closure and multiplicity theorem imply that the set E
of fixed vertices blue to all twelve red-core vertices is a red clique,
with |E| in {2,3,4}. This proof uses that reviewed corollary. It does not
transfer the BLUE-pair no-BB contact theorem to a RED pair.

The action is (0 1 2)...(30 31 32), fixing 33,...,42. Moving triangles
0,...,3 are internally red and induce Core194 word 100110110110110100;
the other seven moving triangles are internally blue. Choose two members
of E as u=33,v=34. The accepted complete RED direct base already fixes
their red edge and their eight negative primary incidences to the four
red moving triangles. It has 320 primary variables and 364,095 clauses,
including all no-monochromatic-K5 constraints under the fixed action/core.
It has no fixed-row order and no extra BLUE-pair consequences.

For q=2,3,4, relabel the remaining eight fixed vertices so that the other
q-2 empty ones occupy 35,...,32+q. Every such permutation fixes the entire
moving set and the ordered marked pair, commutes with C3 and preserves
all literal Ramsey constraints and base fixed colors. This is a family
relabeling, not an automorphism claim for individual graphs. It covers
every graph up to relabeling. Several choices of marked pair can give
several representatives; this is not an isomorphism census.

The q-th complete case imposes exactly:

1. Four negative fixed-core units for each f=35,...,32+q, making it empty.
2. Positive units for every edge within {33,...,32+q}, except the already
   fixed edge (33,34), making the whole empty set a red clique.
3. For each f=33+q,...,42, a positive four-literal clause consisting of
   its four fixed-core incidence variables, making that prefix nonempty.

The added clause counts are

    4(q-2) + binom(q,2)-1 + (10-q) = 8,13,19.

Thus the complete formulas have 320 variables and respectively
364,103; 364,108; 364,114 clauses. No moving attachment or unmentioned
fixed edge is set by this tail. In particular, moving triangles and fixed
vertices outside E are not forbidden from being BLUE to both u and v.
All RR,RB,BR,BB contacts are left to the complete Ramsey constraints.
The BLUE nine-type attachment cover is inapplicable to these RED cases.

Conversely, any Ramsey coloring satisfying the q-th formula has exactly
the stated empty set and that set is a red clique. Hence the three
cardinalities are disjoint intrinsic cases, and their normalized formulas
cover every hypothetical Core194 extension using the reviewed corollary.
No selected degree sequence, M stratum, opposite neighborhood, further
automorphism, maximality assumption or other local relaxation is imposed.

The independent physical auditor imports no clause producer. It visits
all 256 zero/nonzero patterns of the eight other fixed-core prefixes.
Exactly 1,8,28 patterns have q=2,3,4. Every corresponding stable-partition
permutation is checked on the 43 vertices, C3 action and 320 primary
orbits, and transports the entire physical tail to the canonical case.
The prefix predicates are checked on all 16 possible four-bit values at
each of eight vertices in each case (384 truth assignments). The red
clique predicates are checked on all 1+4+32=37 assignments of their added
edge variables. Tail support is disjoint from all marked-pair contacts
to blue moving triangles and to fixed vertices outside E. The seven
adjacent fixed transpositions preserve all 364,095 complete RED clauses,
giving 2,548,665 checked clause images.

The producer uses direct arithmetic primary indices; the auditor derives
them from physical unordered-pair C3 orbits. Every complete child retains
every base byte and has the independently reconstructed tail, header and
EOF. Eight malformed full children, including missing nonempty guards,
wrong clique/empty signs and an extra no-BB clause, are rejected. The
direct base itself is regenerated and independently reconstructed using
different full-five-set and possible-clique algorithms.

A checked UNSAT excludes exactly its entire q-cardinality stratum. Only
three checked refutations would exclude whole Core194. A SAT requires all
320 values, explicit complete-clause evaluation, a compact edge list and
separate literal five-set/action/core/RED-pair checking, followed by exact
empty-set and clique checks. UNKNOWN, timeout or a partial proof trace
establishes no exclusion or realization.

The bounded contract uses two workers and one 90-second solve per new case.
Every actual UNSAT requires full DRAT including RAT in production and
again against freshly reconstructed formulas under optimized Python.
Source and file hashes are identity checks, not proof substitutes.
Pending proofs are saved before checking; same-contract resume retains
UNKNOWN and rechecks evidence. STOP prevents queued starts while active
bounded work finishes. Malformed statuses and a false refutation of a
satisfiable fixture are rejected under normal and optimized Python.

The base equivalence and the corollary |E| in {2,3,4}, including the full
BLUE closure, now have independent accepted reviews. The new red exact-
cardinality cover, physical bridge and computational outcomes remain an
author-checking boundary until independently reviewed. Trust remains in
the imported proofs, ordinary relabeling and finite reasoning, exact
Python/hardware, physical indexing and the full DRAT checker. Internal
cross-checks and two proof replays are not independent peer review or
formalization. R(4,5)=25 is upstream of the reviewed corollary; no degree
constraint or new Ramsey bound is imposed in these three formulas.

This pass stops after the complete three-case decision checkpoint. If all
cases remain UNKNOWN, preserve that outcome and change approach before
another Core194 variant, as required by the principal's stopping boundary.
No subsequent attachment radius or proof phase is part of this contract.
