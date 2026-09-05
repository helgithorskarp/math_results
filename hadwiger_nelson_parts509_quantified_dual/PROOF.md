# A two-block quantified colouring dual

## Exact claim

Fix the 374-point set L and the specified 303-point pool U=S union Q5.
Use all strict unit edges of the 677 distinct points in L union U. Assume
the independently reviewed twenty-class interface theorem for L. The
formula D_b generated here satisfies

    D_b is true
    iff every X subset U with |X| <= b makes L union X four-colourable.

Consequently D_134 is the logical complement of the target formula Q_134
in the [prior reduction](../hadwiger_nelson_parts509_quantified_selector/PROOF.md).
We prove this semantic equivalence; we have not determined the truth of
the full-pool formula. A false value would identify a non-four-colourable
member of the at-most-508-point sealed family. It would still need an
independent non-four-colourability certificate and an explicit
five-colouring before a five-chromatic record claim.

This standard quantified dualization is not a new general logical method.
The contribution is its exact family instantiation and calibration with
a fresh checked certificate for the known 509-point graph.

## Boundary reduction

The pinned exact geometry contains 1860 L edges, 1504 U edges and 36
cross edges. Every L endpoint of a cross edge belongs to the reviewed
19-vertex interface. The prior package checks this for the entire pool
using two exact coordinate representations, including all 228826 point
pairs. Its input hashes are checked transitively before this generator
uses the geometry. This pass reuses that geometry; it does not claim a
fresh independent geometry implementation.

Write lambda_j for the interface colouring of actual full-L witness j,
where 0 <= j < 20. Every proper L-colouring can be normalized and permuted
to one of these witness restrictions. Hence, for fixed X, L union X is
four-colourable if and only if some j and map c:X -> {0,1,2,3} satisfy all
pool-edge inequalities and all cross inequalities c(v) != lambda_j(a).
The forward implication permutes the colours on X at the same time; the
reverse implication joins c to the supplied full-L witness. There are
no cross edges outside the interface. Pattern completeness, as distinct
from the checked positive L witnesses, remains an imported theorem.

## Prefix and overflow guard

The prefix is

    forall x  exists (t, c, p).

There is one universal selector x_v per pool point. The existential t
are a bidirectional truncated totalizer with outputs equivalent to
thresholds of the number of true selectors. Both implications are
required. In particular, g=t_(b+1) is forced to be true exactly when
the selection exceeds budget b. The counter clauses are unguarded.

Every selector assignment extends to the threshold assignment determined
by actual subtree counts. Conversely the totalizer's merge implications
force those counts up to the truncation threshold. This is the same
pinned exact totalizer used by the prior certified encodings. Because
t follows x, the count can depend on the selection, but the exact
constraints prevent it from inventing an overflow for a small selection.

If b equals |U|, g is the constant false and no counter is needed. The
empty-pool case is handled in this branch. For a fixed selection, g is
the corresponding Boolean constant and all selectors are substituted
before serialization. The fixed-instance formula therefore has only
existential variables and is ordinary SAT. Invalid fixed selections
are accepted, consistently with the guarded universal family statement.

## Colour and pattern clauses

For each v and colour k introduce c_(v,k). For each interface pattern j
introduce p_j. The following clauses all have the additional literal g:

    OR_j p_j
    -x_v OR c_(v,0) OR c_(v,1) OR c_(v,2) OR c_(v,3)
    -x_u OR -x_v OR -c_(u,k) OR -c_(v,k)    [pool edge uv, each k]
    -p_j OR -x_v OR -c_(v,lambda_j(a))      [cross edge av, each j]

If g is true, all these clauses are satisfied. The totalizer still has
a valid extension. Thus over-budget universal choices never refute D_b.

If g is false, at least one pattern j must be active. Every selected
vertex has a nonempty colour set. Adjacent selected vertices have
disjoint colour sets, and cross clauses exclude the boundary colour
of each active pattern. Choose any active pattern and one colour from
each selected vertex's set. All strict edges are properly coloured.

No at-most-one clauses are necessary for either pattern or colour
variables. A satisfying assignment with several patterns imposes more
cross exclusions, so choosing any one active pattern remains sound.
Likewise choosing one colour from a nonempty set preserves the edge
inequalities. Conversely any proper colouring and compatible pattern
give a satisfying assignment by setting just those colours and that
pattern true. Unselected vertices may have arbitrary colour variables.

For each fixed admissible X the matrix is therefore satisfiable exactly
when L union X is four-colourable. The universal selector block proves
the stated equivalence. Negating it yields the previous existential
non-four-colourable-selection claim. No finite colouring library,
degree filter, previous stratum closure or numerical bound is assumed.

## Quantifier dependence and serialization

Both the compatible pattern and the pool colouring may depend on X.
A different colouring for each selected graph is permitted; there is
no claim that one colouring simultaneously works for every graph.
The small common-selection fixtures check the complement of the earlier
quantifier-order controls. The previous matrix used universal pattern
and colour bits followed by existential conflict witnesses. This dual
uses one universal selector block and one existential response block.

The full instance has 303 universal and 3549 existential variables:
2317 counter variables, 1212 colour variables and 20 pattern variables.
Its 74956 clauses comprise 67916 counter clauses, 303 vertex clauses,
6016 pool-edge clauses, 720 cross-edge clauses and one pattern clause.
All 3852 variables occur in the matrix, and the two blocks partition them.
Tiny fixed controls can have unused colour variables; tautologies supply
their required occurrences without changing truth.

Full QDIMACS SHA-256:

    20f03643727208fafbe960bea868e443ea6fb8e0788c5846c8fb93c8ef660e20

The fixed original S control has 560 existential variables and 2944
clauses: 135 vertex clauses, 2208 internal-edge clauses, 600 cross-edge
clauses and one pattern clause. Removing its existential prefix gives
the exact SAT instance checked by DRAT. The SAT export function rejects
any instance with universal variables; stripping the full family prefix
would change its meaning and is not a permitted export.

## Validation and trust

The independent matrix parser checks syntax, variable partition and
occurrence. A reused small DPLL evaluator then compares matrix
satisfiability with a direct exhaustive search over boundary patterns
and four-colour assignments, for each of 491 selector assignments in
52 fixtures. The fixtures include all eight labelled graphs on three
vertices, each budget from zero through three, odd-length five-vertex
counter tests and the prior fourteen logical controls. All 491 constant
specializations are checked against the same direct definition. This
is exhaustive for those fixtures, not for the sealed family.

DepQBF 5.01 agreed on all 52 fixture truths and both fixed real controls.
Its false answer on fixed S is corroborated by a fresh Kissat proof of
the exact 560-variable CNF, accepted by the independent drat-trim checker.
That is a reproduction of the known 509-point non-four-colourability,
not a new graph theorem. The 1098848-byte binary DRAT trace is retained
locally and regenerated by the public command; its hash is compact
provenance, not a replacement for replaying the proof.

For S minus 397, the verifier checks both an existing proper colouring
and the newly decoded native colouring in native_witness.json against
all pool and cross edges and against their fixed-instance clauses. The
full L witness for each pattern is checked by the pinned input reader.

Trust boundaries include the imported interface completeness theorem,
exact input geometry, unformalized reduction above, totalizer and
generator, ordinary Python execution, and the DRAT checker for the
fixed 509-vertex certificate. The independent parser, definition-level finite
checks and proof checker reduce different risks; these are author
cross-checks, not external review or a formal proof of the generator.
No full-family truth value or QBF strategy certificate has been established.
