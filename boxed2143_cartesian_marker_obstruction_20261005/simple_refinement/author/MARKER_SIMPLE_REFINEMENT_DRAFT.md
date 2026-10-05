# Simple permutations inside the common marker fiber

Author: Sage, literature-researcher-1, 2026-10-05. Separate uniform partial
author argument, awaiting Theo's different-researcher check. The exact full
growth target remains unchanged and unsolved. The earlier accepted marker
packet and its public/graph scope do not already cover these new claims.

An interval of a permutation is a contiguous position segment whose values
are a consecutive integer set. A permutation of length at least four is simple
if its only intervals are singletons and the whole permutation.

Use the previously checked map Phi on an input sigma of length M>=2:
X_i=M-1+sigma_i, H_i=2M-1+i, L_i=i, and

    Phi(sigma)=X_1,H_1,L_1,...,X_(M-1),H_(M-1),L_(M-1),X_M.

Its exact boxed-2143 occurrence correspondence and common minimum/maximum
Cartesian tree pair were independently checked by Theo. Verified source:
https://github.com/helgithorskarp/math_results/tree/2d02dc425cf66e89a01676bae3f19b076caf28c8/boxed2143_cartesian_marker_obstruction_20261005 .
The original proof SHA256 is
bb901334aba7735664bfe9668a16617305e5b4834e2b0944a722eafaef2125d6.

## Claim S1: exact simplicity criterion

Phi(sigma) is simple if and only if sigma_1!=M and sigma_M!=1.

Every three consecutive positions in Phi contain a low marker, a free point
and a high marker. Consequently every contiguous segment of length at least
three contains both a low value below M and a high value above 2M-1. If its
values were consecutive, it would contain the entire middle band [M,2M-1].
In particular it would contain both X_1 and X_M, at the first and last
positions. The segment would therefore be the whole permutation. Thus no
proper interval of length at least three exists.

For a length-two segment, the adjacent types are X_i,H_i; H_i,L_i; and
L_i,X_(i+1). The middle type has value difference 2M-1>=3. The first type
has difference at least i, and can be one only when i=1 and X_1=2M-1,
equivalently sigma_1=M. The third type has difference at least M-i, and can
be one only when i=M-1 and X_M=M, equivalently sigma_M=1. These are exactly
the two possible nontrivial proper intervals. This proves both directions.

## Claim S2: preserving every occurrence in a simple extension

For any permutation pi of length m>=1 set

    tau=(1,pi_1+1,...,pi_m+1,m+2),
    E(pi)=Phi(tau).

The length of E(pi) is 3m+4. It is simple by S1: tau starts with its minimum
and ends with its maximum, so the two prohibited endpoint values do not occur.
Neither appended extremum can be selected in a boxed2143: the new minimum
is leftmost and cannot play the second selected role; the new maximum is
rightmost and cannot play the third role. They also lie outside every old
occurrence's horizontal span. Thus padding gives an exact occurrence bijection,
and composing with the checked Phi correspondence gives an exact bijection
between occurrences in pi and E(pi). In zero-based indexing, an old index i
maps to 3(i+1).

Decode by reading every third point, subtracting (m+2)-1 to obtain tau,
deleting its first and last entries, and subtracting one. All images at a
fixed m have the same Cartesian tree pair from the checked construction.
Therefore every permutation has a recoverable simple extension of this
specified length preserving every boxed2143 occurrence, and in particular
every boxed avoider has such a simple avoiding extension.

If s_n counts simple boxed2143 avoiders, this proves s_(3m+4)>=a_m. More
precisely, one common tree-pair fiber of simple permutations at that length
contains a band-restricted slice with exactly a_m avoiding assignments. This
is an explicit entropy transfer; it does not establish the growth of a_m.

## Claim S3: unbounded viable branching survives simplicity

For every M>=2 use the checked common tree pair and prefix assigning
ranks 1,...,M-1 to L_1,...,L_(M-1). Exactly the M free positions are heap
available. Among complete **simple** boxed-2143-avoiding extensions, exactly
M-1 positions are viable for the next rank M.

For each t in {1,...,M-1}, take sigma with 1 at t and all other entries
increasing. Every inversion ends at that same 1, so sigma classically avoids
2143 and hence boxed-avoids. Also sigma_M=M and sigma_1 is 1 or 2. For M=2
the only allowed t is 1; for M>=3 either first value differs from M. Thus
S1 makes every Phi(sigma) simple. The checked correspondence makes it avoid,
and it assigns the next rank M at X_t with the common pair and prefix.

The last free position X_M cannot be viable for a simple extension, including
extensions outside the band-restricted slice: assigning rank M there puts
values M-1 and M at the final two adjacent positions L_(M-1),X_M. They form
a nontrivial proper interval. No other position is heap available. This proves
the exact count M-1, which is unbounded. Consequently restricting an attempted
constant local-branching proof to simple avoiders does not rescue that method.

## Scope, prior work and next obligation

Theo's separately checked arbitrary-inflation/substitution packet gives a
growth equivalence between all avoiders and simple avoiders. This construction
is a different explicit extension/fixed-fiber mechanism; it neither proves
his substitution result nor supplies its missing bound. Generic simple-
permutation theory and Cartesian-tree encodings are prior work. No priority
claim is made without a separate literature refresh.

A useful next full-target claim must control complete avoiding assignments,
even in these simple fibers, or construct an unbounded-rate avoiding family.
The simple extension takes avoiding inputs to avoiding outputs and cannot
repair arbitrary nonavoiding input. The statements here provide no uniform
exponential upper bound, superexponential family, universal132 completion, or
campaign completion evidence.
