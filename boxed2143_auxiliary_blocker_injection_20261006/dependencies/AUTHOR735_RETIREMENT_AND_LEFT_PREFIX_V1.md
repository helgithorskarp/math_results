# Charged point retirement and the positive birth account

Quinn / literature-researcher-3, 2026-10-06. New AUTHOR working proof and
falsifiable account. This is OUTSIDE pending718 and its Theo722 ownership.
The exact agreed target410 remains UNSOLVED. Neither the uniform statements
below nor the new finite control inherit a different researcher's acceptance.

Use persistent global birth values, actual original tags and the K convention
from the pending718 V3 proof. In an n-original completed parent, each boundary
before an original and END has weight1, each boundary before an auxiliary0.
For point j, K_j is the sum strictly after j through its nearest greater right
point, or END. Accepted648 supplies the ordered initial charge labels in an
episode. Accepted592 supplies the actual rightmost legal earlier repair cut.
We use the pending718 exact fixed-point transport, rather than assuming it
has passed Theo's fresh entire check.

## Alternating order and exact final fences

Suppose an episode charges old identities j_1,...,j_c and inserts auxiliaries
a_1,...,a_c, followed by the new original h. The charged nodes follow one
Cartesian path; each later charged node is in the previous node's right
subtree. Their positions strictly increase and their values strictly decrease.
The i-th rightmost legal earlier cut is in j_i.left, by accepted648. Later
offending labels stay in j_i.right. Therefore that later cut lies STRICTLY
after j_i. All these statements use current positions, not the shifting old
integer gap index. At the final stage the order is

    a_1 < j_1 < a_2 < j_2 < ... < a_c < j_c < h

where '<' in this display means position. Values of all new points increase
in that order of birth and exceed every old value.

There is no old point greater than j_i between a_i and j_i: the cut is in
j_i.left. There is none greater than j_i between j_i and a_(i+1), or h for
i=c: this segment stays in j_i.right. Thus the final nearest greater LEFT
identity of j_i is EXACTLY a_i, and its final nearest greater RIGHT identity
is EXACTLY a_(i+1), or h. Both are real and the left value is smaller, so
EVERY charged old point is finally eligible, including points with K0.
The intervals of all finally charged points are pairwise disjoint.

This proof needs the cut-in-left-subtree and preserved-right-subtree facts;
merely noting that auxiliary cuts increase does not prove these fences.

## Loss of selected mass and terminal exception

Let g be the initial selected unit gap. It is in every charged point's initial
interval. For i<c the next new auxiliary lies before that selected boundary
and has a zero new left boundary. Thus

    K_j_i(final) <= ordinal_j_i(g)-1 <= K_j_i(initial)-1.

The last charged point has right fence h. Its interval includes h's new unit
left boundary, and hence K_j_c(final)>=1; it has the cap
K_j_c(final)<=ordinal_j_c(g)<=K_j_c(initial).
Consequently every initially K1 charged point except the last ends with K0.
By the pending718 monotonicity/zero-absorption proof, it can never be charged
in any future episode. The last point can stay K1 and recur without bound,
as the already preserved auxiliary4 source family demonstrates.

All final charged intervals lie strictly after j_1 and through the new unit
boundary before h. They are disjoint, so

    sum_i K_j_i(final) <= ordinal_j_1(g).

Summing individual nonterminal losses proves the useful but insufficient
deterministic bound

    c-1 <= sum_i (K_j_i(initial)-K_j_i(final)).

It does not control future newborn mass or the desired source expectation.

## Exact left prefix, without suppressing births

The final interval of auxiliary a_i ends at a_(i+1), or h, by pending718's
ordered newborn fence proof. It contains j_i and the entire final interval
of j_i. Define the LEFT prefix mass

    L_i = sum of final unit gaps strictly after a_i through the gap before j_i.

These are actual original boundaries; the boundary before j_i has weight1
only if j_i is original. No new auxiliary boundary has weight1. The exact
partition is

    K_a_i(final) = L_i + K_j_i(final),
    sum_new_aux K - sum_charged_old K(final) = sum_i L_i.

Left prefixes may have positive mass. It is therefore invalid to identify
newborn auxiliary mass with the retained charged-old mass or to omit a birth
because its own final eligibility is false. Ineligibility at birth can change.

Let P be the number of ALL existing points with positive K, without imposing
eligibility. Let R be the number of old positive points ending with K0 in this
episode, and B the number of new auxiliaries with positive final K. Every old
K is nonincreasing and the new original has positive K (END has unit mass),
so the exact live-point identity is

    P(final) = P(initial) - R + B + 1.

This identity retains original and auxiliary retirements and births separately.

## One precise prospective amortization premise

Candidate C1, NOT claimed proved: for every actual completed source parent and
every next original choice, B<=R+1. If true, the live-point identity would give
P(final)<=P(initial)+2. That implication would still be a partial bound, not
the actual-source little-o(m log m) estimate or full410.

The new pinned audit will test C1 on the EXISTING1725 V2 episodes, in their
stored order, and preserve the FIRST failing episode and the number of failures.
A failure of C1 will NOT be relabeled a failure of the alternating/fence,
retirement or partition claims. It will not be used to refute the full source
average, other potentials, or the agreed growth question. No larger census,
global minimum-counterexample claim, new source-history law or fitted constant
is authorized by this audit. If C1 passes finitely it remains unproved.

The missing positive-birth influx is substantive: the retired K1 charge alone
does not pay L_i, and nonterminal positive-mass charges may shrink without
retiring. The next estimate must retain these transfers and actual history
probabilities. The planned computation is a same-author falsification/control
on fixed inputs, not an independent reproduction or all-size proof.
