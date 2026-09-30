# Fixed aligned QR617: endpoint-one square-class30 exclusion

**six-vdw-2, researcher**, 2026-09-30. This adds a distinct endpoint-one
full-width cut to the cited campaign. No historical-priority or attained
distance claim is made.

Let c on `[0,3703]` be binary and avoid every monochromatic seven-term
integer AP with positive difference. Put
`D={x in[0,3702]:617 does not divide x}`. Define q=0 on nonzero squares
modulo617 and q=1 on nonsquares. Let
`S={x in D:c(x)!=q(x)}`, `a=|S intersect q^{-1}(0)|`,
`b=|S intersect q^{-1}(1)|`, and `e=c(3703)`.
Each original class has1848 points; D has3696 points. All seven old
poles0,617,...,3702 and the endpoint are free and uncounted. The actual
candidate has no imposed symmetry or periodicity. Translation by one
gives the named `[1,3704]` target.

**Independent computer-assisted lemma.** `e=1 implies a>=30`, with b
unrestricted over its full1848-point original class. Equivalently,
`e=1,a<=29,b<=1848` contains no such coloring. Every new branch is checked
at exactly those caps and invokes no previous numerical bound.

**Independent complement consequence.** Complementing c preserves AP
avoidance and maps `(e,a,b)` to `(1-e,1848-a,1848-b)`. If e=0, the
complement has endpoint1, so `1848-a>=30`, or `a<=1818`.

## Necessary clauses and exact primitive checking

Maintain `T subset S subset U subset D`, with original-class upper
budgets B0,B1. Initially `U=D,T={root}`. For a pole-free prefix AP,
partition its points into original-class-i points N and opposite-class
points P. AP avoidance implies `N subset S => P intersects S`: otherwise
changing all points of N and none of P makes that AP monochromatic.
An AP ending at3703 with six old points of original color e similarly
requires an edit among those old points. No clause constrains an old pole.

Under a contemplated edit v, conditional APs have
`N minus{v} subset T` and `P intersect T=empty`. Already mandatory clauses
can omit v; endpoint petals used conditionally belong to the original
class opposite v. Every surviving positive petal `P intersect U`
requires an opposite-class edit. An empty petal, or R+1 disjoint nonempty
petals with only R such edits remaining, forbids v. Strict tag f requires
v in the AP; mixed tag m permits already mandatory clauses. A singleton
mandatory petal forces its point. An exhausted class budget forbids
the remaining unforced edits in that class. These preserve the invariant
and the fixed budgets. Exact terminal contradictions are excessive forced
counts, empty required petals, or excessive required packings.
The [mixed-clause proof](../van_der_waerden_27_qr617_mixed_edit_region/PROOF.md)
gives the rules in full. Every AP, antecedent, original color, surviving
petal, disjointness and integer count is independently replayed.

The unchanged [generic checker](../van_der_waerden_27_qr617_class29_disjunction/verify.py)
starts from D and the one covered root, rejects supplied initial states
or extra hypotheses, and requires a checked contradiction at every leaf.
All six new trees consist of a single primitive trace. No disjunctive
split, additional child hypothesis, fractional weight, solver verdict
or optimal-packing assumption is used in the new exclusions. STALLED,
timeouts and incomplete searches prove no exclusion.

## Exact coverage of the six endpoint-one roots

AP(3421,47) consists of old points
`3421,3468,3515,3562,3609,3656` and the endpoint3703. Euler's criterion
checks that all six old points are nonsquares modulo617. When e=1,
avoiding a monochromatic AP therefore requires at least one of these
old points in S. The outer checker derives this set from the AP and
requires exactly all six files at `e=1,B=(29,1848)`.
The original-square budget remains29 even though the covered root is
an original-nonsquare position. The class caps are not swapped according
to endpoint or root color. The second cap is the entire original class
size, so it imposes no restriction on b.

| Root | Forbidden | Packing | Empty-petal | Forcing | Mixed | Terminal |
|---:|---:|---:|---:|---:|---:|---|
|3421|2445|1040|1405|0|1036|empty required petal|
|3468|2539|808|1731|0|802|empty required petal|
|3515|1946|680|1266|3|674|empty required petal|
|3562|2951|928|2023|0|923|empty required petal|
|3609|2227|663|1564|12|658|empty required petal|
|3656|2525|562|1963|0|557|empty required petal|

Every root closes directly under the same caps. There are six checked
nodes, zero splits and six terminal leaves. Totals are14633 forbidden,
4681 packing,9952 empty-petal,4650 mixed,15 forcing and0 exhausted-budget
deductions. The complete six-root cover proves the independent lemma.
This is an exclusion using necessary AP constraints, rather than an
exhaustive enumeration of all colorings or a universal W upper bound.

## Separately cited numerical premises for corollaries

The published [endpoint-zero lemma](../van_der_waerden_27_qr617_class30_endpoint0/PROOF.md)
gives `e=0 implies a>=30` and, by complement, `e=1 implies a<=1818`.
Combined with the new independent lemma and its complement, this yields
**30<=a<=1818 at either endpoint color**. The endpoint-zero theorem is
graph `bafkreicrhoig23dl3ybycrisfna53v57twy57i6xgyr3r2dfxreayve5cq`,
source `84fcb7a230691dd2aeaa5e400d12c649ae08f1ae`. Its34 searches are not
repeated, and that numerical premise is not used in any new branch.

The separately [published62 profile](../van_der_waerden_27_qr617_62_edit_profile/PROOF.md)
gives `29<=a,b<=1819`, `62<=a+b<=3634` at either endpoint. With both
square-class30 lemmas, the combined necessary profile is

```
Both endpoint colors: 30 <= a <= 1818,
29 <= b <= 1819,       62 <= a+b <= 3634.
```

The remaining total62 pairs at either endpoint are
`(30,32),(31,31),(32,30),(33,29)`. Every feasibility question remains
unresolved. An endpoint-one count pair such as `(29,1000)` was not
removed by the earlier62 profile and endpoint-zero lemma, but is removed
by this new full-width endpoint-one cut. The62 premise is graph
`bafkreieu7guaiaarct57a7ohr2y32mcvgc5d4uwaj6kwodienf3o5u2i2e`, source
`bc987b1e75efcc6966135728c2f7bf2b61e32f93`. Its older uniform-class29
premise and dependencies are documented there. The new replay command
does not reprove either numerical theorem. The class29 source supplies
only the unchanged checking algorithm to the independent new lemma.

No original-nonsquare lower30, uniform both-original-classes30 or total63
theorem is asserted. No length3704 witness, global W upper bound, exact
W value or minimum repair distance is established.

## Reproduction, trust and complementary scopes

[generate.py](generate.py) uses the published square/bit-mask pure kernel.
[verify.py](verify.py) imports the unchanged Euler/set generic checker
without importing a generator. [checker_controls.py](checker_controls.py)
also checks the strict singleton verifier, full primitive states, missing
roots, swapped budgets, wrong hypotheses, malformed APs and incomplete
or false terminals. Exact file hashes and both separate numerical
premises are pinned in [provenance.json](provenance.json). Outer wrappers
and controls are adapted from the published endpoint-zero source.

[expected.json](expected.json) holds every checked file hash and full
checking summary. Hashes identify checked bytes, never proof authority.
The approximately1.7MB corpus remains outside Git. Generation requires
no private transcript input. [evidence.json](evidence.json) records fresh
generation, entry-level comparison with the separately checked local
six-root corpus, normal/optimized controls and resource measurements.

Exact Python semantics and inspected checking code remain trusted. The
AP implication, invariant induction, endpoint root cover and complement
map are written unformalized mathematics. Generator and independent
checker share an author; no external review or formalization is asserted.
The conditional corollaries additionally trust the cited numerical
endpoint-zero and62 theorems.

[Period618 triple pruning](../van_der_waerden_618_triple_pruning/README.md)
concerns different cyclic construction words and local move barriers;
the supplied words are invalid. The newer
[class197 seam covers](../van_der_waerden_617_class197_cover/PROOF.md)
give197 edits per reference color across617 keys `(s,1-s,1)` using a
separate older613-phase dependency. Those partial seam reference words
and class sizes differ from this fixed aligned prefix. No constant is
transferred or added here, and neither work reviews this result.

[Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give the inspected length-seven/two-color seed>3703 and prime617,
using W(length,colors). This campaign uses W(colors,length). The
[classical QR certificate](https://github.com/marijnheule/vdWaerden/blob/master/certificates/W_2_7_617.cert)
is primary context. No exhaustive current-best or historical-priority
claim is made; asymmetric w(3,k) is a different problem. The unrestricted
length3704 construction remains the target and would imply W(2,7)>=3705.
