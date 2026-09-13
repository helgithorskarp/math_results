# Graph-first claim alignment, 2026-09-13

The committed Discovery Net view inspected at the start has height 4363,
2207 contributions, and 10837 relations. The initial authorized repository
HEAD is recorded in PROVENANCE.json. No new full r=29 endpoint theorem was
found in the committed Albertson neighborhood. Its terminal source explicitly
says that r=29 is not proved by that program.

| Artifact | Exact reference | Scope/status |
|---|---|---|
| Albertson conjecture, h280 | `bafkreidok2jdm7kiwmp7fo6zo4dm62ez4gg6dhq5uqenlznfozl4dsvg5y` | General problem; all r remains open |
| Eight-row gate, h2761 | `bafkreibw6w2mbyw5bt62int7zw5r22xhbrvbeokqrjzqq7h5m5rdjlkxl4` | Conditional old minimum-degree-(r-1) frontier: n=57,m=824..828 and n=58,m=838..840 |
| Order-57 closure, h3681 | `bafkreiby3yyat6arjzslah4ctyfbl6iel2l4leqrwv5sz54qbfzzbq5fxy` | Source claims closure of all five old order-57 rows; not a full r=29 result |
| Latest old frontier, h4263 | `bafkreifekhs5awrpg3henhvb56jzs3mfxx4ey2p4ygzea7rwcccldzk4ya` | Explicitly leaves order 58 open; its exact counts inherit an objection |
| First count objection, h4229 | `bafkreid57ri5mwtyskzcrzfkcu7jq34txexuehuxv455mo5usiae4jxmtq` | Unsafe upper substitution for actual component count in inequality (7); seven claimed closures reopen under ablation |
| Later count objection, h4273 | `bafkreiafqxskbbn4dsiq3oxk4wu2yyruug4h5n2wt2klasqpitztzvuuhy` | Same load-bearing defect: 455/2294 closures reopen; repeated-block aliases are additional latent defects |

The full bodies and directed relation neighborhoods were retrieved, including
older scope/seed repairs and confirming reviews. The h4229 objection challenges
both h4221 and its confirming h4225 review. The h4273 objection challenges
h4231 and the h4263 residual counts. The source-level witness uses actual
component count 1 versus an upper surrogate 2; the valid inequality reads
3<=3, while the substituted test rejects 6>3. Those objections have not been
turned into acceptance by this audit. Repeating their long ablations would
duplicate already-closed review work, so they were read, not rerun.

The two authorized repository review packages identify the separate
[Cao–Mehat preprint](https://arxiv.org/abs/2609.04771v1) and explicitly leave
its correctness unaudited:

- [h4221 review](../albertson_r29_h4221_inequality7_review1/README.md)
- [h4231 dependency review](../albertson_r29_h4231_inequality7_dependency_review1/README.md)

This is the nonduplicate verification target of the present package. Its
minimum-degree-r argument leads to different numeric rows, and its proof does
not use the old scan. In particular its n=58 floor is 841, already above the
old frontier's ceiling 840. One cannot silently mix the two chains: we verified
the preprint's own structural route, with independently derived arithmetic,
instead of assuming the old recurrence and all its structural dependencies.

There is no claim that the prior graph reductions are false merely because a
new stronger theorem empties their possible counterexamples. Their quantifier
scope and their outstanding count defects are preserved.

The latest general-principal report available at intake was
`20260913T080811.721387Z.md`; it governed the earlier R(5,5) holds, not the new
human Albertson assignment. No R(5,5), HN, prior critical-graph, Property B, or
order-54 archive was altered. Earlier pending transactions were not resubmitted.
