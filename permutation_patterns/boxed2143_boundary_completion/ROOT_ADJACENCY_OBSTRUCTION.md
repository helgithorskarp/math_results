# A uniform obstruction to choosing the132 root beside the input maximum

Author: Lyra (literature-researcher-2), 2026-10-05. Separate addendum to the
frozen boundary-interface packetv1. Full target410 is unsolved. This theorem
refutes a candidate root-choice rule; it does not refute existence of another
132 scaffold, the unrestricted source completion conjecture, or growth.

For each m>=8 define the input permutation

    pi_m=(2,1,4,3,m-1,m,5,6,...,m-2).

Use strict odd/even interleaving J_rho(pi_m), and assume rho in S_(m-1) avoids
classical132. Then J_rho(pi_m) contains boxed2143 whenever the largest even
entry2m-2 is immediately before OR immediately after the old maximum2m-1.
The choices below that largest-even root are otherwise unrestricted within
the132 grammar. Hence allowing both adjacent root gaps at the full level does
not yield a universal completion rule.

## Largest even immediately before the old maximum

The root is the fifth scaffold gap (zero-based gap4). Its left segment has
five old entries, odd labels(3,1,7,5,2m-3), and four evens. Since rho avoids132,
every even rank on the left of its maximum exceeds every rank on the right.
The right has m-6 evens, so the four left even ranks are

    m-5,m-4,m-3,m-2.

For m>=9 their labels are all at least8. In particular all inserted entries
between the first four old points(3,1,7,5) are above7. Those four old entries
therefore form a boxed occurrence:1<3<5<7, and every unselected point in their
horizontal span is above the top7.

For m=8 the four left even labels are(6,8,10,12). If6 is in the fourth left
gap (after old5), the first three gap entries all exceed7 and the same old
box survives. If6 is in one of the first three gaps, use the respective cases:

* First gap: the consecutive entries(6,1,x,7) with x in{8,10,12} form2143.
* Second gap: select(3,1,6,5); all unselected interior entries are above6.
* Third gap: select(3,1,7,6); all unselected interior entries are above7.

These exhaust all placements of6. The other even ordering and both subtree
shapes are irrelevant to the resulting obstruction.

## Largest even immediately after the old maximum

The root is the sixth scaffold gap (zero-based gap5). The old entries m-1
and m are adjacent in pi_m, so the full output contains consecutive entries

    (2m-3, y, 2m-1, 2m-2),

where y is the different even entry just before the old maximum. Since the
largest even is already at the root, y<=2m-4. Thus

    y < 2m-3 < 2m-2 < 2m-1,

and these four consecutive entries are boxed2143. This direction does not
even require132 avoidance of rho.

## Scope and finite controls

For m8 the full exact boundary algorithm nevertheless finds the completion

    (3,2,1,4,7,6,5,8,13,10,15,12,9,14,11),
    rho=(1,2,3,4,5,6,7).

Its largest even14 is in the final gap, away from the input maximum15. Its
avoidance and recovery are checked by the direct boxed definition in the
addendum replay. No universal assertion about this increasing-scaffold
family is needed or claimed.

The separate replay enumerates the entire classical132 scaffold family by
the literal triple predicate at m8, checks every candidate with either root
gap, and also checks every arbitrary ordering in the left four-even band of
the before case at m8,...,20. It tests all possible labels y for the after
case at these sizes and reconstructs the displayed m8 full completion with
the exact boundary search. This author replay supports the written uniform
proof; it cannot replace a different researcher's all-size check.

Primary context: Kitaev–Qiu–Xu, *Coincidences and Growth of Boxed Mesh Patterns*,
https://arxiv.org/html/2609.13764v1, Conjecture7.4. The proposed adjacent-root
constraint is a research heuristic, not an externally stated open problem or
a replacement goal. The exact132 maximum grammar is standard and restated in
BOUNDARY_INTERFACE_LEMMA.md. Only this precisely delimited negative conclusion
is asserted.
