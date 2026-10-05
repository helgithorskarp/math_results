# Exact interval boundary composition for boxed2143 completion

Author: Lyra (literature-researcher-2), 2026-10-05. Partial mechanism for the
externally sourced target agreed in chat410. **Full target remains unsolved.**
The propositions below prove soundness/completeness of a specified finite
search, not nonemptiness of its root for every input. Another researcher must
check the entire stated scope before this is an accepted team result.

## Definitions and primary context

A word has distinct integer labels in an ambient alphabet [1,N]. A boxed2143
occurrence has positions i1<i2<i3<i4, values b<a<d<c in that order, and no
unselected position j with i1<j<i4 and b<w_j<c. Avoidance uses this precise
strict-interior convention. Missing ambient labels are not points of the word.

Kitaev, Qiu and Xu, *Coincidences and Growth of Boxed Mesh Patterns*,
arXiv:2609.13764v1 (12 September 2026), Theorem3.2 gives the value-interval
characterization used here; Conjecture7.4 proposes an unrestricted strict
odd/even completion. Theorem4.4 and Conjecture7.5 identify the remaining growth
question. Source: https://arxiv.org/html/2609.13764v1 . We reprove the elementary
interval equivalence below to make the interface claim self-contained. The
132 maximum decomposition is standard classical-pattern combinatorics and is
also proved here. No novelty claim for those ingredients or for a general
prefix/suffix automaton is made.

For I=[lo,hi], let w|I be the word obtained by keeping only labels in I. Let
P_I(w) be its first at most three entries and S_I(w) its last at most three.
The boundary signature is Sigma_N(w)=((P_I(w),S_I(w))) over all integer
intervals 1<=lo<=hi<=N. Labels stay absolute; signatures do not standardize
input substrings or discard their comparisons with a scaffold band.

## Proposition1: interval equivalence and exact composition

A word contains boxed2143 iff some w|I contains four consecutive entries
(a,b,c,d) satisfying b<a<d<c. For the forward implication take I=[b,c]. The
empty strict interior guarantees these four are consecutive after restriction.
For the reverse implication, every value strictly between b and c belongs to
I, so a shaded unselected point would contradict consecutiveness.

Suppose U and V are internally avoiding words on disjoint labels, and x is a
label absent from them. Form W=U x V. For each interval I form

    B_I = S_I(U) + (x if x belongs to I, else empty) + P_I(V).

Then W avoids iff every B_I has no consecutive2143. Indeed, an occurrence in
W|I wholly inside U|I or V|I is excluded by their internal avoidance. Any
remaining consecutive quadruple crosses a concatenation boundary and uses at
most three entries from each of U|I and V|I; it therefore appears as a window
of B_I. Conversely every four-entry window of B_I is an actual consecutive
window of W|I. It cannot lie wholly in one retained side because each side
contributes at most three entries. This proves both directions, including when
x is absent from I or one side restricts to the empty word.

If the merge avoids, its exact signature is computed from child signatures by

    P_I(W) = first3(P_I(U) + (x if in I) + P_I(V)),
    S_I(W) = last3(S_I(U) + (x if in I) + S_I(V)).

If a side has at least three retained entries the truncation already settles
the relevant end; otherwise its stored prefix/suffix is the entire side.
Consequently two internally avoiding child words with the same signature are
interchangeable for both avoidance and resulting signature in every such
merge. Iterating this statement justifies interface-state deduplication in a
larger binary composition. This is an exact composition interface, with no
claimed constant bound on its realizable states.

## Proposition2: complete132-scaffold dynamic program

Fix pi in S_m. A full strict interleaving is

    J_rho(pi)=(2*pi_1-1,2*rho_1,...,2*rho_(m-1),2*pi_m-1).

Restrict rho to classical132-avoiders. More generally a subproblem (f,e,L)
has the consecutive old input positions f,...,e-1 (zero based), their original
odd labels 2*pi_j-1, and the consecutive even ranks L,...,H where H=L+e-f-2.
There are s=e-f old entries and s-1 even entries. For s=1 the unique word is
the old odd singleton, whose signature is stored.

For s>=2, try every cut f<c<e. Put even2H at the root gap. The right subtree
has R=e-c-1 even entries and gets ranks L,...,L+R-1; the left subtree gets
L+R,...,H-1. Recursively combine every signature from (f,c,L+R) with every
signature from (c,e,L), using Proposition1, and retain one lexicographically
least word for each resulting signature. The full root is (0,m,1).

Why this is precisely the132 grammar: in a132-avoider, split at its maximum.
Every entry on its left must exceed every entry on its right, since a smaller
left entry, the maximum and a larger right entry would be132. Both sides avoid
132. Thus, for a consecutive rank set, their ranks are exactly the higher
left band and lower right band above. Conversely any such two avoiding sides
with left ranks all larger than right ranks yield a132-avoider. A triple
crossing left/right has its first left entry larger than its later right
entry and cannot be132; a triple using the maximum in the middle would also
need a left entry smaller than a right entry. Triples within one side are
already excluded.

Inductively, the dynamic program stores exactly the signatures of all
internally boxed2143-avoiding words in this scaffold grammar. Soundness follows
from the grammar and Proposition1. For completeness, any avoiding grammar word
has the unique split at its largest even entry. Its two contiguous position
subwords avoid: a boxed occurrence inside such a subword persists in the full
word since all additional positions lie outside its horizontal span. Their
signatures occur in the smaller memo states; the merge therefore reconstructs
the signature of the full word. Replacing each child by its canonical witness
does not change admissibility or signature. For a fixed cut, taking its least
left and right witness minimizes the concatenation, and minimizing over cuts
gives the lexicographically least representative of each signature. Equal
segment lengths make these lexicographic substitutions legitimate.

The recursion strictly decreases segment length and all state sets are finite,
so it terminates. This is a full correctness proof for the mathematical
algorithm for arbitrary m. The exploratory Python implementation explicitly
caps inputs at m<=9 and is not a claimed practical algorithm for arbitrary m.
No polynomial-time, small-state or universal nonempty-root conclusion follows.

Full-root output recovers pi from odd positions and rho from even positions.
If one later proves that the root is nonempty for every pi and every m, choosing
a canonical output would inject S_m into avoiding permutations of length2m-1.
Then a_(2m-1)>=m! and limsup a_n^(1/n)=infinity; for example m! is at least
(m/2)^(floor(m/2)), whose (2m-1)-st root is unbounded. **The antecedent remains
unproved.** A finite search cannot supply it.

## Proposition3: two induction invariants fail

First, augment the132 recursion by requiring its root gap at EVERY node to
be immediately before or after the largest old odd entry in that segment.
This rule cannot complete pi=(1,2,4,5,3). Its maximum5 has two eligible root
gaps; each remaining segment has its old maximum at an endpoint, so recursive
choices are forced. The only full words are

    (1,2,3,4,7,6,9,8,5), rho=(1,2,3,4),
    (1,4,3,6,7,8,9,2,5), rho=(2,3,4,1).

The first has the consecutive occurrence (7,6,9,8). The second has selected
values (4,3,6,5), at zero-based positions(1,2,3,8); all unselected points in
that horizontal span are7,8,9 or2, outside the open value interval(3,6).
These two checks refute the rule without relying on the finite minimality
search. A valid unrestricted132 completion is

    (1,6,3,4,7,8,9,2,5), rho=(3,2,4,1).

Second, an internally avoiding old lower word (labels below the available
even band) and old upper word (labels above it) are necessary for completion,
but not sufficient, even allowing ALL permutations of the available evens.
Consider old word (3,1,7,5) and available evens(6,8,10). The lower word(3,1,5)
and upper empty word avoid. Nevertheless every strict completion contains a
box. Classify by the position of6 among the three gaps:

* In the first gap, the consecutive entries (6,1,x,7), x=8 or10, form2143.
* In the second gap, select (3,1,6,5). The other inserted values8,10 and old7
  inside its horizontal span are above6.
* In the third gap, select (3,1,7,6). The other inserted values8,10 are above7.

This is an actual reachable subproblem (0,4,3) of full input
pi=(2,1,4,3,5,6,7): at the full cut4, the right subtree has two even entries
and the left band is ranks3,4,5. That single root choice is impossible although
the full input has the132 completion

    (3,2,1,4,7,6,5,8,9,10,11,12,13).

Thus neither failed rule refutes universal132 completion, unrestricted source
Conjecture7.4, or the agreed full growth target. They identify extra boundary
compatibility that a successful induction must preserve.

## Code, finite controls and precise limits

`boundary_completion.py` implements Propositions1–2; `check_boundary_completion.py`
independently enumerates every132 scaffold by factorial permutations filtered
through the literal triple predicate, then uses a direct boxed quadruple scan.
For all153 inputs m<=5 it compares every exact signature/canonical-witness map
of all3385 reached subproblems, not just root existence. The saved map stream
SHA256 is b0d3c57d6ee50acde2059c812f1e6c3f88d71fbd514b86cb94ca71b1490c7150.
The author implementation and verification are not an independent team review.

`probe_boundary_invariants.py` exhausts the exact adjacency-restricted grammar
and saves all witnesses at its first failing input. Its lower-length search
checks37 inputs (all shorter lengths then a prefix at5). Minimality is finite
additional evidence; it is not needed for the mathematical refutation. All six
arbitrary permutations of(6,8,10) are also checked at the named local band state.

Reproduction, from this directory with Python3.11 standard library:

    python3 -B check_boundary_completion.py --max-m 5
    python3 -B probe_boundary_invariants.py

These partial findings provide an exact compatibility model and two preserved
negative tests. They give no uniform growth bound, no universal completion
construction and no campaign completion evidence.
