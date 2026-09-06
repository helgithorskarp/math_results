# Complete primary-variable decision for Core194 with an empty pair

Consider red/blue colorings of K43 invariant under
`(0 1 2)(3 4 5)...(30 31 32)`, fixing vertices33,...,42.
The first four moving triangles are red internally, the other seven
blue internally. The first twelve vertices induce Core194, cross word
`100110110110110100`, indexed by cycle pairs01,02,03,12,13,23 and
offset `(t-s) mod3` for vertices `3i+s,3j+t` with i<j.
Vertices33,34 are blue to all twelve core vertices. Their mutual
edge is the one case parameter, blue or red.

The direct formula for each case is satisfiable **if and only if** a
coloring with exactly these properties and no monochromatic K5 exists.
This is an exact formulation theorem, not a SAT or UNSAT verdict.
The two cases cover all possible full Core194 extensions up to labeling,
conditional on the independently accepted at-least-two-empty theorem.
The old full formulas are not inputs to this generator or checker.

## Variables and fixed edges

Every Boolean variable is one physical edge orbit, with true meaning red.
The33 edges internal to moving triangles have constant colors. Other
edges have320 orbits:165 between moving triangles,45 between fixed
vertices and110 between fixed vertices and moving triangles.

For moving vertices `3i+s < 3j+t`, i<j, put

```
rank(i,j) = i(21-i)/2 + j-i-1
X(3i+s,3j+t) = 1 + 3 rank(i,j) + (t-s mod3).
```

For fixed vertices33+i<33+j use
`166 + i(19-i)/2 + j-i-1`. For `a<33<=f` use
`211 + 11(f-33) + floor(a/3)`.
These are the old primary meanings, but no old clause, variable for a
counter, definition or lexicographic comparison is imported.

There are27 fixed primary values:18 core cross-orbit colors, eight
empty-vertex links and one pair color. They are retained as explicit
units even though they are substituted during generation of the Ramsey
clauses. Keeping320 declared variables leaves293 unfixed primary values;
this is not a claim of293 independent degrees of freedom after constraints.

## Literal Ramsey clauses and equivalence

For each of the962,598 five-sets Q, forbid both monochromatic colors.
For red, form the disjunction of the negations of its ten edge colors.
For blue, form the disjunction of the ten colors. Substitute only the
constant internal colors and the27 fixed primary values.
Discard a clause only if a substituted literal is true. Otherwise remove
constant-false literals and repeated occurrences of a variable, preserving
an empty clause if it arises. Deduplicate identical clauses. There are
no mixed-sign original Ramsey clauses, so opposite literals do not create
another tautology issue. Sort the final distinct clauses lexicographically.

A graph satisfying the stated properties gives a unique assignment to
all320 primary orbits and satisfies these clauses. Conversely, any model
defines every one of the903 physical pairs, has the stated action and
fixed colors, and satisfies each original five-set prohibition by
substitution equivalence and the retained units. Thus its graph is a
Ramsey(5,5;43) graph. No degree bound, external Ramsey value, neighborhood
selection or unproved normalization enters this equivalence.

In the blue case additionally impose the eight necessary binary clauses
`X(33,f) OR X(34,f)`, f=35,...,42. Here is the standalone justification,
rederived without an earlier solver verdict. If f were blue to both
empty vertices, f cannot miss two red triangles Ci,Cj: their union has
a blue edge ab, since otherwise it is a red K6. Then33,34,f,a,b form a
blue K5. Hence f must be red to at least three core triangles. Each
complementary nine-vertex Core194 subcore has a red K4; omitting0,1,2,3,
witnesses are {3,4,7,10}, {0,1,7,10}, {0,3,9,10}, {0,3,6,7}.
Being red to any three triangles therefore makes a red K5. Contradiction.
The checker reconstructs an obstruction for all16 fixed signatures.
Thus these eight binary clauses preserve the equivalence above.
The red case receives none of them. The two small copied edge-list
fixtures certify local blue-pair consistency and the necessity of its
color guard; neither is a43-vertex target.

The full literal clauses already forbid any internally blue moving
triangle from being blue to both ends of a blue pair. Together with the
fixed-neighbor lemma this gives exactly the twelve core vertices as
their common blue neighborhood. We do not fix any further outside edge.

## Relabeling and exact scope of each case

The preceding independently accepted multiplicity result says every
full Core194 extension has at least two empty fixed vertices. Choose any
such unordered pair. Permute only the ten fixed vertices so that this
pair becomes33,34. This permutation commutes with the moving C3 action,
fixes the twelve core vertices pointwise, and preserves every Ramsey
constraint and every internal color. It preserves emptiness of the pair.
The new direct formula has **no fixed-row ordering or other normalizer**
that this permutation could violate. Its binary consequences are valid
for any chosen blue empty pair. Therefore this labeling gives a model of
the direct case matching that pair's color.

The cases are disjoint for a labeled distinguished pair. Their graph
families up to isomorphism need not be disjoint: an extension with both
red and blue empty pairs would appear in both under different labelings.
If either direct case is refuted, that color is impossible for **any**
empty pair in a full Core194 extension. This is stronger in scope than
refuting only the first ordered pair in the old normalized formula.
Both refutations, together with the accepted z>=2 theorem, would exclude
the entire Core194 class and its81 labeled representatives. One or two
UNKNOWN outcomes provide no such exclusion or feasibility evidence.

The relabeling proof does not permit selecting the colors of the other
fixed edges, sorting additional signatures, or imposing old counter
constraints without justification. None of those operations occurs here.

## Independent reconstruction and certificates

The producer uses closed-form orbit indices and all five-sets. The
checker imports no producer. It traverses the action on every physical
pair to recover orbit variables and reads the core from twelve literal
adjacency masks. For each color it forms the graph of edges still able
to take that color after the27 fixed values. A bit-intersection clique
recursion enumerates its possible K5s. Their unfixed physical edges
recover exactly the forbidden clauses. The checker adds the independently
reconstructed units and proved blue-pair consequences, then compares
every actual clause, not just counts or hashes. The model decoder uses
the producer's edge map, while a separate graph check inspects every
physical five-set, known color and action pair. A prescribed Boolean
assignment tests all903 decoder colors against physical orbit traversal.

Corrupted formulas, models and graphs are rejection controls. Both
normal and optimized Python must produce identical reports. A completed
UNSAT result is accepted only after full DRAT replay, including RAT,
then replayed again against a freshly regenerated and independently
checked full formula. A SAT result requires all320 model values, direct
clause evaluation, a compact edge list and independent literal graph
verification. Partial UNKNOWN traces are neither refutations nor saved
solver states. Hashes identify files, not proofs.

This formulation equivalence has ordinary unformalized reasoning and
exact code/runtime/hardware as its trust boundaries. The graph-to-two-case
coverage additionally imports the accepted z>=2 theorem; its inherited
proof dependencies remain at their stated scopes. No older UNKNOWN is a
premise. Counts for all197 cores import the earlier core catalog and
whole-exclusion review boundaries. Internal checking of this new code
is not independent peer review or proof-assistant formalization.
