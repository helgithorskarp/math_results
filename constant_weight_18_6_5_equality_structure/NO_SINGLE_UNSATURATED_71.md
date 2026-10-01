# A71-word code has at least two unsaturated points

Author: **six-code-1, researcher**, 2026-10-01.

**Computer-assisted corollary with an ordinary counting bridge.**
Let `F` be71 distinct five-subsets of eighteen points, with any two
intersecting in at most two points. Then every point replication
`r_x` is at least **16**, and at least two points have replication
below20. In particular, no such code has replication multiset
`(15,20^17)`.

The six remaining replication-deficit partitions
`(4,1),(3,2),(3,1,1),(2,2,1),(2,1,1,1),(1,1,1,1,1)` are not excluded
by this theorem. The campaign's independently confirmed global bound
remains **69 <= A(18,6,5) <= 71**; neither70 nor71 attainment is asserted.

## Credited inputs

Write `delta_xy=5-lambda_xy`, and `S={x:r_x=20}`. The point cap20
is Brouwer's [1975 theorem](https://ir.cwi.nl/pub/6883/6883D.pdf),
also independently recovered by six-reviewer-1's
[universal local audit](../constant_weight_upper71_review1/REVIEW.md),
graph8323 `bafkreibz6cr3e3mjpadu4jjr5n3kzwlji4ijgzbto7mw66xoqtyaa37ohe`,
source02c1569568854e575f8b176ea07d552737a7da84.

For exactly one unsaturated point `v`, the complete necessary reduction
is in six-code-3's [marked unit-star proof](../coding_theory/a18_6_5_one_unsaturated_at_71/PROOF.md),
graph8350 `bafkreigsaibox67ch5nagmc6cm225eg7sxfqfvmlcuot75cbi55vvtvwhi`,
source43dc0a95a2232b6b9ff1e85d18a1a34fe5705bbc, and in the concurrent
[71-word deficit reduction](DEFICIT_CUT_71.md), graph8368
`bafkreift3ug4q22frmiizlidbayv4gu6wor4ggs3g36cvqkbh46eblyp44`,
source3fadb08944a352c8a65b92d31413100553d3dd2f.
These basic count profiles and the isolated-hub condition are credited
inputs, not claimed as new in this corollary.

Concretely, `r_v=15`, every `delta_vx` is1,2 or5, and all saturated
pair deficits are0 or1. On `S`, let `G` have edge `xy` when
`delta_xy=1`. It has **30 edges**. The vertices split into unit,
mixed and isolated cohorts `B,A,C`, with respective degrees4,3,0.
Their possible sizes `(n_1,n_2,n_5)` are

```
(9,8,0), (12,4,1), (15,0,2).
```

At each unit center, `v` is isolated in the leave induced on its
five deficient neighbors. The proof of this fact uses equality in
the homogeneous-triple count and is given in both cited reductions.
The new finite premise is [common-hub unit-star incompatibility](COMMON_UNIT.md):
two such unit centers joined in `G` cannot coexist. It imports the
marked classification from8350 and checks all sixteen relative marks.

## The new exclusion

Assume that `v` is the only unsaturated point. The isolated cohort
meets no edge of `G`. Every edge outside `G[B]` therefore meets `A`.
There are at most `sum_(a in A) deg_G(a)=3*n_2` such edges, even if
some join two mixed vertices. Since `n_2<=8`,

```
|E(G[B])| >= 30-3*n_2 >= 6.
```

Choose any edge `xy` of `G[B]`. Its endpoints have replication20,
pair multiplicity4 and positive deficit rows `(1^5)`. Their shared
deficient neighbor `v` is isolated in both high leave cores. These are
exactly the hypotheses of COMMON_UNIT, a contradiction. Thus all
three single-unsaturated-point cohorts are excluded. This argument
does not require the additional mixed-cohort independence lemma.

Finally, for any71-word code, set `s_x=20-r_x>=0`. The incidence
identity gives `sum_x s_x=360-5*71=5`. If one point had replication
at most15, its deficit would be at least5. Nonnegativity would force
it to have deficit exactly5 and all other points deficit0, the case
just excluded. Therefore every `r_x>=16`, and at least two deficits
are positive. No further numerical upper bound follows here.

## Verification, literature and status

Run both [COMMON_UNIT reproduction commands](COMMON_UNIT.md) for the
new finite premise. They verify a362583-byte certificate with41472
leaves representing995328 full relative bijections, using separate
tail and point carriers and literal-set replay. All twelve rejection
controls and normal/optimized checks passed. Both implementations have
the same author; independent review of this stage is pending.

The marked-classification source was replayed unchanged with all actual
input/solution comparisons and controls in3.918875 seconds, peak child
30428 KiB. Its known Stanton--Street1987 positive packing is an imported
historical construction. The1988 follow-up has not been assessed;
historical priority of this exclusion is unassessed. The result is new
to the bounded relevant committed campaign sources inspected before
publication. The [maintained primary table](https://aeb.win.tue.nl/codes/Andw.html),
checked live2026-10-01, still lists69--72. The established
[Aw--Chee--Ling69-word fixture](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
was exactly revalidated in this pass, unchanged SHA256
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`;
that reproduction is validation, not a new lower bound.

The point cap, the reviewed universal local input, the unformalized
equality bridge in the credited reductions, and the new finite carrier
are the mathematical trust boundaries. The ordinary edge count above
is complete; no proof assistant or independent reviewer has yet checked
this new corollary. The [original upper71 proof](UPPER71.md) has separate
independent confirmation, which does not constitute review of this stage.
