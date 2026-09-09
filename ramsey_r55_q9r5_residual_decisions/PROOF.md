# Physical meaning of the residual decision

Let `bo1-q9-r5-c%06d`, for `c=0,...,361`, denote the original ordered
maximal-packing task with five red four-cliques on vertices 0 through 19,
four blue four-cliques on vertices 20 through 35, and catalogue core C on
vertices 36 through 42. The catalogue order and labels are retained. No
automorphism quotient or new source graph is used.

The inherited task requires the red four-clique packing to be maximal.
Consequently the induced graph on vertices 20 through 42 has no red K4.
The target requires this induced graph to have no blue K5. Thus every
solution of the complete physical task restricts to a solution of the
residual formula below. This implication is all an exclusion needs.
It does not say that a residual solution extends to a good43.

Write residual vertex i for physical vertex 20+i. Its four prescribed
blue blocks are [0,3], [4,7], [8,11], [12,15], and its core is [16,22].
There are 253 pairs: 24 prescribed blue block pairs, 21 prescribed core
pairs, and 208 free pairs. Give the free pairs variables 1 through 208
in lexicographic pair order; true means red. For every four-subset put
the disjunction of the negated edge variables. For every five-subset put
the disjunction of the positive edge variables. Substitute all fixed
edges. Discard a clause already made true, and delete false fixed
literals from the other clauses. No symmetry-breaking or additional
constraint is added.

This CNF is equivalent to the literal residual problem: a truth assignment
and its physical 23-vertex graph have identical values for every free
edge, and each surviving clause excludes exactly its specified forbidden
four- or five-set. This includes every constraint wholly contained in
the residual that was studied through blue contacts, three-blue-block
events, and residual maximality in h4059, h4069, and h4081. It does not
include constraints involving any of the first twenty physical vertices.

An independently checked UNSAT certificate for this CNF would exclude
the entire corresponding original 43-task. A SAT model proves only the
existence of a feasible residual. UNKNOWN proves neither. The declared
gate requires at least one whole-task exclusion and a complete 362-row
ledger. It is not redefined after seeing solver outcomes.

## Independent checks and trust boundaries

`encode.py` enumerates vertex subsets and simplifies their clauses.
`check.cpp` reverses each clause to the physical vertex set determined by
its variables, checks every free edge and every fixed value, rejects
duplicates, and compares the resulting set of physical subsets with a
separate recursive enumeration of all required subsets. It parses graph6
by direct bit extraction, independently of the producer's bit string.

SAT certificates are 64-digit lower-case hexadecimal integers. Bit i is
the red indicator for the i-th lexicographic pair among all 253 pairs.
The three high padding bits are zero. The Python verifier literally
enumerates all four- and five-subsets. The C++ verifier checks four-tuples
by six-edge sums and checks every possible blue extension of a blue
four-tuple. Both check the 45 fixed pairs. Neither trusts the SAT solver
for the validity of a witness.

For a solver UNSAT claim, `solve_one.py` preserves the exact binary DRAT
stream after flushing C stdio, then appends an explicit empty-clause
addition. The addition is a claim that the independent checker must
verify; it is never accepted just because the solver returned UNSAT.
`run.py` requires successful drat-trim verification before recording a
whole-task exclusion. Positive and deliberately false proof controls
check the proof-output path. The false proof is rejected.

The input SHA256 fixes all 362 named core records. Their isomorphism
completeness and the original complete good43 labeling cover are imported
from the pinned catalogue and h3887/h3873; this experiment does not
re-prove them. A verified individual residual witness needs only its
literal core record, not the completeness claim. The mathematical bridge
from the original maximal-packing task is an ordinary proof, not a proof
assistant formalization. No independent peer review is claimed.

Whole-task totals and child totals are separate. The prior 518 q7,r5
closures concern different task IDs. The 161 q10 children remain owned
by team-r55-1 and are not inputs to this experiment. A color-complement
redirect is not an UNSAT certificate.
