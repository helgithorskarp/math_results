# An exact quantified selector for the sealed Parts pool

## Statement

Retain the fixed 374-point set L. Let U be the specified 303-point set
S union Q5: 135 original S points and 168 completion points. Use every
strict unit edge on L union U. Let Q_b be the formula emitted by
`encode.encode` for this graph and budget b.

**Reduction theorem.** Assuming the established twenty-class interface
classification for L, Q_b is true if and only if some X subset U with
|X| <= b makes L union X non-four-colourable. In particular Q_134 is an
exact encoding of the fixed-L, at-most-508-vertex target family.

This theorem states an equivalence. It does not assert the truth or
falsity of Q_134. Non-four-colourability alone would also not establish
chromatic number exactly five without an explicit five-colouring.

## Applicability of the interface classification

The exact point data is reconstructed at denominator 288 in
Q(sqrt(3),sqrt(5),sqrt(11)). There are 677 distinct points and 3400 unit
edges: 1860 inside L, 1504 inside U and 36 between them. Every endpoint
in L of those 36 cross edges belongs to the original 19-vertex interface
I. This condition is checked for the entire sealed pool, including Q5.

The [interface theorem](../hadwiger_nelson_parts509_interface_lemma/README.md)
states that, after a colour permutation fixing the normalized origin,
every proper L-colouring restricts on I to one of twenty patterns. Each
pattern has a supplied proper full L-colouring. We use the actual witness
patterns, not a different choice of canonical representatives.

Consequently L union X is four-colourable exactly when there exist a
pattern p among these twenty and a map c:X -> {0,1,2,3} with:

1. c(u) != c(v) for every unit edge inside X;
2. c(v) != lambda_p(a) for every cross edge av with v in X.

For the forward implication normalize a whole-graph colouring and then
permute its nonzero colours to the supplied witness representative. This
also permutes the colours on X and preserves every edge inequality. For
the converse use the witness L-colouring of p. No cross edge can see a
different L vertex outside I, so the two colourings combine properly.

An arbitrary map c on X extends to a map on U by assigning arbitrary
colours to unselected points. Thus quantifying over all two-bit colour
assignments on U loses no case and adds no relevant restriction.

## Quantifiers and variables

The prefix is

    exists (x, a)  forall (p, c)  exists (t, mu, v, w).

Here x_u selects u in U. The variables a are cardinality auxiliaries.
Their clauses involve only the outer existential variables and encode
sum x_u <= b. The supplied truncated totalizer is the same exact counter
used in the earlier certified encodings. Each threshold means that the
corresponding subtree contains at least that many selected leaves. Its
two implication directions enforce that meaning; actual subtree counts
extend every admissible selection to a satisfying auxiliary assignment.

The universal p comprises five bits, with least significant bit first.
The universal c comprises two bits for each of the 303 pool vertices.
All four bit patterns represent colours; there is no invalid colour code.

The placement of x before p and c is essential: a single selected graph
must block every pattern and every colouring. Moving x after p would
allow a different selected graph for each pattern and change the claim.
The `common_selection` controls specifically detect that error.

## Lookup gates and unused pattern codes

For each j in {0,...,19}, an inner variable t_j is constrained to be the
conjunction of the five literals expressing p=j. Both directions of this
gate are encoded. For each a in I and each colour bit r, mu_(a,r) is the
disjunction of the t_j whose witness lambda_j(a) has bit r equal to one.
Again both directions are encoded, including empty disjunctions as false.

An inner gate v is equivalent to OR_j t_j. Thus v is true precisely for
the twenty valid indices. For indices 20,...,31 all t_j and v are false.
These twelve unused universal codes must be harmless, rather than
accidentally requiring another impossible colouring condition.

All lookup values are uniquely forced by p. Existentially quantifying
them after the universal block therefore introduces no freedom to change
the boundary colours.

## Witnesses for failed colourings

For each pool edge uv introduce an inner witness w_uv and the clauses

    w_uv -> x_u,       w_uv -> x_v,
    w_uv -> (c_(u,r) = c_(v,r))       for r=0,1.

The equality of two bits z,y under w is expressed by

    (-w OR -z OR y) AND (-w OR z OR -y).

For a cross edge au use the same two bit-equality implications comparing
c_u with mu_a, and the single selection implication w_au -> x_u.
Every witness therefore denotes an actual monochromatic edge of the
selected graph, with the fixed side coloured by lambda_p.

Finally impose the single clause

    -v OR (OR over all edge witnesses w).

If p is invalid, this clause is automatically satisfied; all witnesses
may be false. If p is valid, the inner existential block can satisfy the
clause precisely when there is an active monochromatic pool or cross
edge. If there is one, set its witness true and all other witnesses false.
Conversely a true witness forces that very edge to be present and
monochromatic. Reverse implications for w are unnecessary.

Thus, for a fixed admissible X, the universally quantified block succeeds
if and only if every valid pattern and every colouring fails on some
selected edge. By the interface argument this is exactly the failure of
four-colourability of L union X. The outer existential choice and its
cardinality condition finish the proof in both directions.

No killing-set library, necessary degree condition, previous a-stratum
closure or optimization lower bound occurs in this formula. Those results
remain valid but are not hypotheses of its exact quantified semantics.

## Dimensions and serialization

For b=134 the first block has 2620 variables (303 selectors and 2317
counter variables), the universal block has 611 (5 index bits and 606
colour bits), and the last block has 1599: 20 index matches, 38 boundary
colour bits, one validity gate and 1540 edge witnesses.

There are 4830 variables and 77505 clauses. Of these, 67917 clauses belong
to the outer cardinality encoding. Generated QDIMACS SHA-256:

    caacfbf264249f6da99f4c23e91ce3c7a9a6448ef1f7f30bc0542bbd159b5c14

The variable order, clause order and input hashes are deterministic.
Quantifier blocks partition all variables. Tiny abstract controls can
have irrelevant selectors or colour bits; harmless tautological clauses
ensure every declared atom occurs in the matrix, as required by strict
[QDIMACS](https://www.qbflib.org/qdimacs.html). The full pool instance needs
no such padding.

## Evidence and trust

The checker parses the emitted CNF independently of its gate construction.
A small DPLL evaluator checks inner satisfiability on all 5202 assignments
of selectors and universals in fourteen abstract fixtures. It compares
each answer with direct inspection of the fixed boundary colours and
selected graph edges. Outer auxiliary variables are checked to occur only
in constraints involving outer variables, so their existential choices
factor independently of the universal assignment. These tests exhaust
the small fixtures only, not the full pool or all possible inputs.

The real S-minus-397 control has an existing explicit proper colouring
of 508 vertices and 2427 unit edges. The public checker verifies it and
checks that its pattern and colour bits refute the generated matrix for
that fixed selection. The known non-four-colourability of the original
509-point control is imported from the existing certified Parts result;
the native QBF run did not establish it anew.

The universal equivalence above is ordinary unformalized mathematics.
The exact graph data, prior completeness theorem, parsing, arithmetic,
generator, independent finite checker and ordinary execution remain
explicit trust boundaries. Different geometry and CNF implementations
are author cross-checks, not external peer review or formal verification.
The generic use of quantified selection and Tseitin gates is standard;
no priority claim is made. The contribution is its exact sealed-pool
instantiation and reproducible checks.
