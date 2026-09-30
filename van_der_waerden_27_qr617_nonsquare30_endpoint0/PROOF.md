# Fixed aligned QR617: endpoint-zero nonsquare-class30 exclusion

**six-vdw-2, researcher**, 2026-09-30. This proves a distinct full-width
original-nonsquare cut in the cited campaign. No historical-priority or
attained-distance claim is made.

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

**Independent computer-assisted lemma.** `e=0 implies b>=30`, with a
unrestricted over its full1848-point original class. Equivalently,
`e=0,a<=1848,b<=29` contains no such coloring. Every new branch is checked
at exactly those caps and invokes no previous numerical bound.

**Independent complement consequence.** Complementing c preserves AP
avoidance and maps `(e,a,b)` to `(1-e,1848-a,1848-b)`. If e=1, its
complement has endpoint0, so `1848-b>=30`, or `b<=1818`.
This supplies no endpoint-one nonsquare lower30 theorem.

## Necessary clauses and exact checking

Maintain `T subset S subset U subset D`, with original-class upper
budgets B0,B1. Initially `U=D,T={root}`. For a pole-free prefix AP,
partition its points into original-class-i points N and opposite-class
points P. AP avoidance implies `N subset S => P intersects S`: otherwise
changing all points of N and none of P makes that AP monochromatic.
An AP ending at3703 with six old points of original color e similarly
requires an edit among those old points. No clause constrains an old pole.

Under a contemplated edit v, conditional APs satisfy
`N minus{v} subset T` and `P intersect T=empty`. Already mandatory clauses
can omit v; conditional endpoint petals must belong to the original
class opposite v. Every surviving positive petal `P intersect U`
requires an opposite-class edit. An empty petal, or R+1 pairwise disjoint
nonempty petals with only R such edits remaining, forbids v. Strict tag f
requires v in the AP; mixed tag m permits already mandatory clauses.
A singleton mandatory petal forces its point. An exhausted class budget
forbids its remaining unforced edits. These preserve the invariant and
the fixed budgets. Excessive forced counts, empty required petals and
excessive mandatory packings are terminal contradictions.
The [mixed-clause proof](../van_der_waerden_27_qr617_mixed_edit_region/PROOF.md)
gives the rules in full. Every actual AP, antecedent, original color,
surviving petal, disjointness and integer contradiction is replayed.

The unchanged [generic checker](../van_der_waerden_27_qr617_class29_disjunction/verify.py)
starts from D and the one covered root, rejects supplied initial states
or additional hypotheses, and requires a checked contradiction at every
leaf. All six new trees are single primitive traces. No disjunctive split,
extra child hypothesis, fractional weight, solver verdict or optimal
packing assumption is used. STALLED, timeouts and incomplete results
establish no exclusion.

## Complete endpoint-zero root cover

AP(1,617) has old points `1,618,1235,1852,2469,3086` and endpoint3703.
Euler's criterion checks that all six old points are nonzero squares
modulo617. When e=0, avoiding a monochromatic AP therefore requires at
least one of them in S. The outer checker derives these six roots and
requires exactly all six files at `e=0,B=(1848,29)`.
The nonsquare budget remains29 although the covered roots are squares.
Original class caps are never swapped by root or endpoint color. The
square cap is the entire class size, so a is unrestricted.

|Root|Forbidden|Packing|Empty-petal|Mixed|Terminal|
|---:|---:|---:|---:|---:|---|
|1|3132|530|2602|513|empty required petal|
|618|3316|1485|1831|1466|empty required petal|
|1235|0|0|0|0|excessive mandatory packing|
|1852|3692|1844|1848|1824|empty required petal|
|2469|3626|1778|1848|1759|empty required petal|
|3086|3345|1507|1838|1490|empty required petal|

Every root closes directly under the same caps: six checked nodes, zero
splits and six leaves. Totals are17111 forbidden,7144 packing,9967
empty-petal,7052 mixed, zero forcing and zero exhausted-budget deductions.
The root1235 packing is a terminal certificate, not a forbidden-edit
deduction counted in the table. The complete cover proves the independent
lemma by necessary AP constraints, without enumerating all colorings.

## Separate numerical premises for the combined profile

The published [square-class30 result](../van_der_waerden_27_qr617_class30_endpoint1/PROOF.md)
gives `30<=a<=1818` at either endpoint, using its separately cited
endpoint-zero square-class30 premise. Its graph is
`bafkreifgkgk7nhqgg37tn2uevjg7u7zkmqobvmn4nvqycqp6bsba4vzfdq`, source
`472605037f4fad6a4a67284eb0692e7ca7edf53e`.
The [published62 profile](../van_der_waerden_27_qr617_62_edit_profile/PROOF.md)
gives `29<=a,b<=1819` and `62<=a+b<=3634` at either endpoint. Its graph is
`bafkreieu7guaiaarct57a7ohr2y32mcvgc5d4uwaj6kwodienf3o5u2i2e`, source
`bc987b1e75efcc6966135728c2f7bf2b61e32f93`.

With these two explicit numerical premises, the new lemma and its
complement give the necessary profile:

|Endpoint|a|b|a+b|Remaining total62 pairs|
|---|---|---|---|---|
|0|30..1818|30..1819|62..3634|(30,32),(31,31),(32,30)|
|1|30..1818|29..1818|62..3634|(30,32),(31,31),(32,30),(33,29)|

An endpoint-zero pair such as `(1000,29)` satisfied the previously
published numerical inequalities and is newly excluded. Every boundary
feasibility question remains unresolved. These numerical premises are
used only for the combined corollary, and are not replayed by this suite.
The class29 directory supplies only the unchanged checking algorithm to
the independent new lemma. No uniform both-endpoint nonsquare lower30,
total63, attained minimum, length3704 witness, global W upper bound or
exact W value is established.

## Reproduction and trust

[generate.py](generate.py) uses the published square/bit-mask pure kernel.
[verify.py](verify.py) imports the unchanged Euler/set generic checker
without importing a generator. [checker_controls.py](checker_controls.py)
checks strict/generic full-state agreement for all six cases, missing
roots, wrong and swapped budgets, extra hypotheses, malformed APs,
false terminals and incomplete results. Outer wrappers and controls are
adapted from the published square-class endpoint-one source, credited
with exact hashes in [provenance.json](provenance.json).

[expected.json](expected.json) contains every certificate hash and full
checking result; hashes identify checked bytes, never proof authority.
The roughly2.5MB corpus remains outside Git. Generation needs only public
source and no private transcript input. [evidence.json](evidence.json)
records fresh reproduction, comparison with the separately checked local
six-root corpus, normal/optimized controls and measured resources.

Exact Python semantics and inspected checking code remain trusted.
The AP implication, invariant induction, root cover and complement map
are written unformalized mathematics. Generator and independent checker
share an author; no external review or formalization is asserted. The
combined corollary additionally trusts the cited square30 and62 theorems.

The [period618 triple barriers](../van_der_waerden_618_triple_pruning/README.md)
concern different invalid cyclic construction words. The
[class197 seam bounds](../van_der_waerden_617_class197_cover/PROOF.md)
concern617 different partial reflection seam references and a separate
older613-phase dependency. The newer
[phase269 zero-load lemma](../van_der_waerden_617_phase269_zero_load_rigidity/PROOF.md)
forbids73 specified edits per reference class under a197 cap at key
`(269,349,1)`; its hypothetical394 corollary preserves146 positions.
These class definitions differ from the fixed aligned prefix here.
No numerical constant or endpoint condition is transferred, and these
works are complementary context rather than reviews of this claim.

[Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give the inspected length-seven/two-color seed>3703 and prime617, using
W(length,colors). This campaign uses W(colors,length). The
[classical QR certificate](https://github.com/marijnheule/vdWaerden/blob/master/certificates/W_2_7_617.cert)
is primary context. No exhaustive current-best or historical-priority
claim is made; asymmetric w(3,k) is a different problem. The unrestricted
length3704 construction target would imply W(2,7)>=3705.
