# Exact Boolean encoding

Vertices 0,...,5 are A, 6,...,11 are their ordered ridge completions B,
and 12,...,17 are R. An edge variable E_uv means an edge of the
**complement** H. All 153 unordered pairs have variables, including
pairs subsequently fixed by unit clauses.

For v and j=4,5,6,7, B_vj means deg_H(v)>=j. Degree bounds 3<=q_v<=7
are imposed separately. The two implications

    B_vj => sum_u E_uv >= j,
    not B_vj => sum_u E_uv <= j-1

give the equivalence and q_v=3+sum_j B_vj. At most ten B_v4 may be true.
For consecutive vertices of A, B_ij=>B_(i+1)j imposes nondecreasing degrees.

A triangle variable is the conjunction of its three edge variables.
T is their sum; t_v is the sum over those containing v. Product variables
P_vuj are conjunctions E_uv AND B_uj. Common-neighbor variables for u,v,w
are E_uw AND E_vw. All conjunctions are encoded in **both** directions.

Using the threshold variables, b<0 is precisely

    sum_v (2 B_v4 + B_v5 - B_v7) + T >= 15.

The summed link inequality is

    sum_v (8 B_v4 + 5 B_v5 + 2 B_v6 - B_v7) + 3T <= 90.

For each v, twice the individual link invariant is

    2 L_v = 10 - sum_(u,j) B_uj
               - 6 B_v4 - 4 B_v5 - 2 B_v6
               + 2 sum_(u != v,j) P_vuj - 2 t_v.

It is required to be nonnegative. The triangle condition is t_v<=1
conditioned on not B_v4. The common-neighbor count is at most one
conditioned on not E_uv, not B_u4, and not B_v4.

For a five-set S, the literal list I_S consists of its ten internal edge
variables. S is independent exactly when every member of I_S is false.
For v outside S, Y_Sv is the conjunction of not E_uv over u in S. Two
conditional cardinality constraints require sum_v Y_Sv=2 whenever S is
independent. Every CNF clause in that cardinality encoding is disjoined
with I_S. If S is not independent these clauses impose no restriction;
the auxiliary variables can be chosen arbitrarily. A seven-set S contributes
the clause OR_(u,v in S) E_uv. Sets containing a fixed true edge are skipped.

Fixed constants are simplified by exact Boolean arithmetic. Signed weighted
inequalities are normalized by a*x=a-a*(1-x) when a<0, adjusting the bound
exactly. Equal variable terms are collected first. Cardinalities use the
sequential-counter encoding; weighted inequalities use PBLib through PySAT's
`PBEnc` with `EncType.best`. The encodings have existential auxiliary
variables. For each satisfying assignment of the mathematical graph
constraints, a compatible auxiliary assignment exists; conversely, a CNF
model projects to a graph satisfying those constraints.

No graph assignment is removed on the basis of sampled data, floating-point
arithmetic, a solver score, or a solver's incomplete search. Case enumeration
and the maximal-facet relabeling argument in `PROOF.md` cover all hypothetical
negative examples. The only solver mode used in the final certificate run
is Glucose 4.1 via `python-sat`'s `glucose4`, with proof logging enabled.

The independent optional OR-Tools model uses integer degrees, exact allowed
degree/quadratic-value triples, neighbor-degree products, and the original
formulas from `PROOF.md`, rather than threshold variables or PB-to-CNF
translation. Its infeasibility statuses are corroboration, not substitutes
for the checked proof traces. An UNKNOWN status means an incomplete run.
