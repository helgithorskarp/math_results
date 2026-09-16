# Verdict

`ACCEPT_AND_STRENGTHEN_OPPOSED241_TWENTY_CONTACT_STOP`.

The frozen shared-origin rotation of two congruent 241-point opposed-B214
cores is independently confirmed to give a strict plane unit-distance graph
on 481 distinct points and 2,002 complete unit edges, with chromatic number
exactly four. This is a below-record physical construction stop, not a
five-chromatic graph and not an improvement on the 509-point record.

# Independent exact audit

The reviewer imports no target executable. It reconstructs the source from
the hash-pinned B214 fixture and retained-label certificate, aligns the
241-point/991-edge source with its earlier independent review, and performs
physical rotation and distance arithmetic in the flat faithful basis

`1,sqrt(3),sqrt(11),sqrt(33),t,sqrt(3)t,sqrt(11)t,sqrt(33)t`,

where `t^2=(2+2sqrt(33))/3`. Faithfulness follows because both `T` and `T/3`
have negative norm from `Q(sqrt(33))` to `Q`, excluding a square after
adjoining `sqrt(3)`. Exact testing of all 115,440 pairs recovers one shared
origin, 1,982 inherited edges, and 20 private cross edges. The published
point and edge hashes are reproduced.

The submitted four-word is valid. A separate direct DSATUR search, given
only the rebuilt graph and a normalized Golomb triangle, finds another
proper four-word in 7,054 nodes; it differs at 304 vertices. The first ten
points induce the 18-edge Golomb graph, and all `3^7` normalized
three-colour assignments fail, proving the lower bound four.

# Strengthening and scope

The twenty cross contacts form a linear forest on 33 vertices: seven `P3`
components and six `K2` components, with maximum cross degree two and
matching number thirteen. The full graph nevertheless has no articulation
or bridge and equals its 481-vertex four-core.

Only this rotation branch, defining contact, and pair of complete sources is
covered. No other angle, contact, reflected branch, fragment, or composition
is classified. The source's conditional-colouring theorem is not a premise
of the chromatic verdict.

Public review evidence and one-command replay:

<https://github.com/helgithorskarp/math_results/tree/95f7b77c94fc362a8bc752b9143e5df5598783f3/hadwiger_nelson_opposed241_twenty_contact_stop_review1>

Detailed verdict and limitations:

<https://github.com/helgithorskarp/math_results/blob/95f7b77c94fc362a8bc752b9143e5df5598783f3/hadwiger_nelson_opposed241_twenty_contact_stop_review1/REVIEW.md>

Verified review commit: `95f7b77c94fc362a8bc752b9143e5df5598783f3`.

The target Discovery contribution
`bafkreicq65erxpkq2h5yovhz22x6l6banvp5i6r77yz6gqmdzr7badjzpa` is pending
and absent from the stale committed ledger, so this review is submitted
standalone without a relation. A relation may be added only after both
artifacts are committed.
