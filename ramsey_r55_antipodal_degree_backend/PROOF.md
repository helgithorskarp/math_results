# Bounded projected-backend decision: exact encoding contract

This source implements the mixed model of public source
40a6cd7ffbe45892bd52e3dfcdbb086f1b5afbfd, not a stronger Ramsey model.
The input neighborhood stream and complete projection descriptor are
pinned to their independently checked public hashes. No automorphism,
chosen Q completion, new degree profile or additional global K5 is imposed.

## Mathematical equivalence

Graph variables 1..523 are the public lexicographically ordered retained
pairs. For each of the 38 vertices in a projected block with maximum
residual U_v, introduce U_v Boolean variables y(v,1),...,y(v,U_v).
The total is 208, numbered 524..731 in increasing vertex order.
Impose y(v,t+1) => y(v,t), giving 170 clauses. The only admitted patterns
are prefixes of ones, uniquely representing r(v)=sum_t y(v,t) in [0,U_v].
Then min(r(v),k)=sum_{t<=k} y(v,t) for each required k=1,...,4.

For every vertex, impose

    sum of incident retained red-edge bits + sum_t y(v,t)
      = desired red degree - fixed red degree.

For a vertex outside the blocks the second sum is empty. This exactly
enforces the public residual equation, including its upper/lower bounds;
all 43 equations are included, even the three trivial root equations.
The two Q red-density equations are unchanged. For each block the equality
of the two sums of margin bits is the balance equation. Each of the 15
nonempty labeled row subsets S imposes

    sum_{v in S,t} y(v,t) <= sum_{v in R,t<=|S|} y(v,t).

Thus all 45 subset cuts, including redundant full subsets, are present.
There are 93 high-level constraints: 45 constant equalities (43 degrees
and two densities), three balances and 45 inequalities. Completeness does
not rely on a fixed graph's margins: the 208 margin bits remain variable.

## Exact binary circuits

The population count of each canonical multiset of input literals is
computed by a balanced binary tree of unsigned word additions. Singleton
leaves are their one-bit input words, empty input is the zero-width zero
word, and each addition retains its final carry. Identical population-count
inputs share the same circuit, but no graph labels are quotiented.

For a full-adder stage with Boolean inputs a,b,c, the two fresh outputs s,t
satisfy s+2t=a+b+c. The CNF encodes parity s=a xor b xor c with eight
truth-table implications and majority carry with six clauses. Constants,
tautologies and repeated literals are simplified, but repeated clauses
are allowed. Both directions hold, so every input assignment has exactly
one valid output assignment. Outputs are allocated in a strictly acyclic
order. Summing the stage identities with powers of two proves exact
unsigned addition; induction on each count tree proves its population sum.

Constant equality fixes each output bit. Balance compares corresponding
bits by equivalences after zero padding. For w-bit words A,B,

    A <= B iff B + (2^w-1-A) + 1 >= 2^w.

The right side is exactly the final carry of B + complement(A) + 1.
This has no overflow ambiguity: output carries are always retained.
The degenerate zero-width comparison is also valid, with carry-in one as
its output, although the actual cuts have nonempty input words.

Combining these identities with prefix-margin semantics proves that the
full CNF is satisfiable exactly when the public projected subsystem is.
By the prior projection theorem, this is exactly when the fixed H92
six-neighborhood degree system has a completion. It is not equivalent to
the unrestricted 43-vertex Ramsey problem, or to the entire hard profile.

## Audit and trust boundary

The separate audit.py imports no compiler, model, flow,
or solver implementation. It checks the full physical prefix and complete
descriptor identities, independently allocates the margin bits and
reconstructs the 93 mathematical input lists. Every actual full-adder
clause block is compared with s+2t=a+b+c on every assignment to all its
input and output variables (116432 assignments over 5037 stages). It then
checks every count-tree/ripple/comparison wire, exact terminal clauses,
and disjoint complete ownership of all variables and clauses. Therefore
there is no unchecked auxiliary or extra clause hiding a stronger model.
The unsigned comparison arithmetic identity is also tested on all 87380
word pairs for widths 1..8.

Seven altered encodings are rejected: reversed margin monotonicity,
omitted cut, changed degree, reused auxiliary, corrupted adder clause,
reversed final comparison, and an appended unexamined clause. Seven bad
solver-status transcripts are rejected. Normal and optimized fresh build
and audit agree byte-for-byte. This is internal algorithmic checking, not
peer review or proof-assistant formalization. The mathematical projection
and physical clause stream remain explicit imported trust boundaries.

The observed CNF has 10805 total variables, 125119 clauses, 5037 full-adder
stages and 100 population counts. Its 523 graph decisions plus 208 margin
bits are distinct from the 10074 deterministic arithmetic auxiliaries.
It is smaller than the old 33515-variable/200127-clause encoding, but this
alone does not imply faster solving, a stronger result, or a solution.

## Bounded execution and reproducibility

Python 3.11.2 standard library; exact integers, deterministic ordering,
no random seed or extra library. One 90-second Kissat 4.0.4 call is allowed
on this encoding, with outer cap 120 seconds. Its full trace stays local.
Exact status lines must match process exit 0/10/20.

A SAT requires every CNF variable, literal evaluation of every clause,
evaluation of the original mixed conditions, and flow lifting. A separate
physical graph check must then validate the claimed subsystem and full
K5 census before any existence publication. A full target, if encountered,
requires an independent target certificate, not merely a solver model.
An UNSAT trace is first preserved in pending.json, then checked by full
DRAT-trim (including RAT), with a 600-second bound. A checked result would
also require a fresh reconstruction/replay before publication. UNKNOWN
is neither infeasibility nor a restart certificate and must not trigger
an equivalent longer retry. None of these status labels claims a verdict
before the corresponding record and checks exist.

Commands from the repository root (fresh output paths):

```bash
python3 -B ramsey_r55_antipodal_degree_backend/generate.py --work /scratch/FRESH-backend --emit-only
python3 -B ramsey_r55_antipodal_degree_backend/audit.py --work /scratch/FRESH-backend --report /scratch/FRESH-backend/audit.json --controls
python3 -B ramsey_r55_antipodal_degree_backend/controls.py
```

README.md and run.json record the single UNKNOWN outcome and optional
solver invocation. This encoding proof itself makes no solver verdict.
