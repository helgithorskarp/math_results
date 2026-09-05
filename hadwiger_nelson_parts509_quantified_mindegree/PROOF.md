# Minimum-degree restriction of the quantified Parts family

## Scope and prior use

Let L be a fixed four-colourable graph on 374 labelled plane points. Let
U be the specified 303-point pool, and use every strict unit edge on
L union U. The target is some X subset U with |X| <= 134 for which
L union X is not four-colourable.

The minimum-degree argument is standard and was already used in the
[sealed-shape reduction](../hadwiger_nelson_parts509_pool_shape_closure_review1/README.md)
and [cover relaxation](../hadwiger_nelson_parts509_pool_cover_residual30/README.md).
We do not claim a new critical-graph lemma. This contribution applies
that necessary condition to the two-block quantified dual, proves its
family-level semantics, and validates the new guarded encoding and
colouring-extension procedure.

No full-family solve, new closed stratum, order lower bound or
five-chromatic graph is established. All existing graph and interface
inputs retain their preceding trust boundaries.

## Family equivalence

For X subset U write

    d_X(v) = |N(v) intersect L| + |N(v) intersect X|,  v in X.

Call X admissible when every selected v has d_X(v) >= 4. The empty
selection is admissible. L itself is four-colourable.

**Reduction.** Every X subset U of size at most b gives a four-colourable
L union X if and only if every admissible X of size at most b does so.

One direction is immediate by restriction of the quantifier domain.
For the other, suppose a non-four-colourable selection of size at most b
exists. Choose an inclusion-minimal such selection Y, minimizing only
the pool vertices while retaining every L vertex. If some v in Y had
d_Y(v) <= 3, minimality would supply a proper four-colouring of
L union (Y minus v). At most three colours occur at v's neighbours, so
one of the four colours extends it to v, a contradiction. Thus Y is
admissible and |Y| <= b. This proves the converse.

There is also a constructive extension argument. Starting from X,
repeatedly delete a selected vertex with current degree at most three,
always retaining L. The process terminates at an admissible set Y.
Given any proper four-colouring of L union Y, restore deleted vertices
in reverse deletion order, choosing an unused neighbour colour at each
step. The neighbours already coloured at that step are precisely among
those counted when the vertex was deleted. There are at most three,
so restoration always succeeds. Restriction supplies the converse:

    L union X is four-colourable iff L union Y is four-colourable.

This provides an explicit way to lift a verified colouring strategy on
the admissible domain to all budgeted selections. It does not require
the final Y to be inclusion-minimal, nor any canonical deletion order.
The finite checker uses the least-labelled available deletion.

**The restriction is not pointwise equivalence of the matrices.** For
example, K5 together with an isolated selected vertex is not
four-colourable, but the low-degree guard accepts that selection. Its
K5 subset remains admissible and refutes the universally quantified
family. These are abstract controls, not plane unit-distance graphs.
No individual ignored selection is declared four-colourable merely
because one of its vertices has small degree.

The argument uses a downward-closed size budget. This package keeps
|X| <= b and introduces no exact-size requirement. Combining degree
admissibility with an exact-size normalization would require a separate
proof; adding vertices to a minimal counterexample need not preserve
the degree condition on the new vertices.

## The guarded two-block formula

Reuse the exact base encoding from
[the colouring dual](../hadwiger_nelson_parts509_quantified_dual/PROOF.md).
It has a universal selector x_v for each pool vertex and existential
counter, colour and pattern variables. Its unguarded exact totalizer
forces g to mean |X| > b. Every ordinary colouring clause has guard g.
The complete twenty-class interface theorem converts satisfiability
of the colouring clauses to four-colourability beside L.

For each pool vertex v put f_v=|N(v) intersect L| and k_v=3-f_v.
If k_v < 0, v can never witness a degree violation. If its whole pool
neighbourhood has size at most k_v, x_v itself is a violation witness.
Otherwise introduce an existential w_v with

    w_v -> x_v,
    w_v -> (sum_(u in N(v) intersect U) x_u <= k_v).

The second implication uses the pinned Sinz sequential at-most counter,
with literal -w_v added to every one of its clauses. All its auxiliary
variables are existential after the universal selectors. For w_v true,
those clauses have an auxiliary extension exactly when the count is
at most k_v. For w_v false, they impose no restriction. A bidirectional
degree counter is unnecessary: only a claimed violation needs a proof.

Introduce one existential escape variable e, replace g by e in each
colouring clause, and add

    -e OR g OR (OR over the degree-violation witnesses).

The budget-counter clauses remain unchanged and unguarded. This single
implication is sufficient. It prevents escape when the budget is valid
and no selected vertex has small degree. Conversely, when overflow or
a genuine degree violation exists, the corresponding witness and e can
be set true, and all colouring clauses are then satisfied. Unused degree
witnesses can be false.

For every fixed selector assignment X, the new matrix is satisfiable
if and only if

    |X| > b
    OR some selected vertex has d_X(v) <= 3
    OR L union X is four-colourable.

The previous reduction therefore proves the whole quantified formula
equivalent to the original family dual. The prefix still has exactly
one universal block followed by one existential block. A false result
must select an admissible non-four-colourable graph within budget;
a true result still needs a checked quantified certificate before
family closure is claimed.

The selectedness implication is essential. An unselected low-degree
vertex cannot justify escape. The `unselected_degree_witness` fixture
contains a K5 and an unselected vertex whose full potential degree is
four but whose neighbours in that K5 number only one. Selecting just
the K5 must still refute the matrix.

## Constants, fixed selections and dimensions

With all selectors fixed, degree counts are computed directly. If a
selected vertex is deficient, the restricted matrix is true regardless
of colourability. Otherwise it is serialized byte-identically to the
base fixed-instance formula. In the true constant case, harmless
tautologies retain declared-variable occurrence required by QDIMACS.
The generic empty-pool and budget-equals-pool-size cases are included.

The complete pool gives 302 allocated degree-witness variables, one
selector alias, 7688 conditional sequential-counter variables and one
escape variable. It adds 17511 degree clauses and one escape clause.
The original 67916 budget-counter clauses are retained.

The resulting full instance has 11843 variables and 92468 clauses:
303 universal selectors followed by 11540 existential variables. It is
larger than the base 3852-variable, 74956-clause formula. The change
restricts the universally tested domain; no runtime improvement is
asserted. Deterministic QDIMACS SHA-256:

    08e5a931743148cb50534d0d5e4d8cd5687137d229844148215a0a080c77c9d6

The 303-selector universe is retained for stable labels and direct
comparison. Peeling the entire pool removes only global vertex 1302,
then stops at 302 vertices. Its exact remaining neighbours are recorded
in expected.json. This is a degree-based omission already implicit in
the necessary condition, not a new geometric-family closure.

## Evidence and trust

The independent parser and reused small DPLL evaluator check every
selector assignment in 58 abstract fixtures. Direct incident-edge counts
and a separate backtracking four-colourer determine the expected
matrix truth. All 1131 assignments, and all 1131 fixed specializations,
agree. Whole-family truth agrees before and after the restriction in
every fixture even where individual matrix answers differ.

A direct deletion-and-restoration implementation checks the peeling
equivalence on the same selections. It constructs and checks 910 lifted
proper colourings, including a five-vertex cascade. The K5-plus-isolate,
unselected-witness, fixed-boundary K4/K3 and repeated-boundary-colour
controls probe distinct failure modes. These finite cases validate those
fixtures only; the general equivalence is the unformalized proof above.

The original 509-vertex control has no degree violation and is byte-identical
to the previous 560-variable, 2944-clause SAT instance. Its existing fresh
Kissat DRAT certificate, independently accepted by drat-trim, therefore
applies without a new solver run. The deletion of vertex 397 control is also
unchanged. The previously published residual30 selection has 508 vertices,
2402 strict edges, selected degree at least four and a supplied proper
colouring; its fixed matrix is unchanged and its colouring is directly
replayed. This is a positive calibration of an admissible selection,
not a new search candidate or killing-set refinement.

The native calibration runs only changed small formulas. Unchanged
fixtures and fixed real inputs are identified by byte hashes and not
rerun. It supplies parser/solver calibration, not an independent proof
of the full family. The full revised instance is generated but unsolved.

Explicit trust boundaries are the pinned exact geometry and interface
classification, the prior base-encoding semantics, the at-most encoder,
the new guarded transformation, ordinary Python execution and the
unformalized reduction and restoration argument. The direct finite
checks use different graph and colouring logic from the encoders.
They are author checks, not external review or proof-assistant checking.
