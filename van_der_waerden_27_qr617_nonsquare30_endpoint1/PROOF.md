# Fixed aligned QR617: endpoint-one nonsquare-class exclusion

Actual author: **six-vdw-2, researcher**, 2026-09-30.

Let c:[0,3703]->{0,1} avoid every monochromatic seven-term arithmetic
progression with positive integer difference. Put
D={x in [0,3702]:617 does not divide x}. Define q(x)=0 for nonzero
squares modulo617 and q(x)=1 for nonsquares. For
S={x in D:c(x)!=q(x)}, let a and b count S in the ORIGINAL q0 and q1
classes, respectively, and let e=c(3703). Each original class has1848
points. The seven old poles and endpoint are free and uncounted.
No symmetry or periodicity is required of the candidate coloring.
Translation by1 identifies this domain with the [1,3704] target.

**Independent exact computer-assisted lemma:** e=1 implies b>=30,
with a unrestricted over its full1848-point class. Equivalently, there
is no such coloring at e=1,a<=1848,b<=29. Every new root is checked at
exactly ORIGINAL caps(1848,29); no earlier numerical bound is used.

Complementing c preserves progression avoidance and maps
(e,a,b) to (1-e,1848-a,1848-b). Thus the independent lemma also gives
e=0 implies b<=1818. An endpoint-zero lower30 is a separate premise.

## Necessary constraints and their verification

The unchanged [primitive proof](../van_der_waerden_27_qr617_mixed_edit_region/PROOF.md)
and [generic tree checker](../van_der_waerden_27_qr617_class29_disjunction/verify.py)
are the computational dependencies. Maintain T subset S subset U subset D,
initially T={root},U=D. For each pole-free prefix AP, partition its points
into original-class-i antecedent N and opposite-class petal P.
Progression avoidance implies N subset S => P intersects S: otherwise
the edits make the entire AP the original color of P.

Under the contemplated edit v, a clause is necessary when
N minus{v} subset T and P intersects T is empty. A clause already
activated by T can participate even if its AP omits v. Each surviving
petal P intersect U requires an opposite-class edit. An empty petal,
or R+1 pairwise disjoint nonempty petals with only R opposite-class edits
remaining, forbids v. Already mandatory endpoint clauses are allowed
only in the checked opposite ORIGINAL class. A singleton mandatory
petal forces its point. An exhausted class budget forbids its other
unforced edits. Excessive forced counts, empty required petals or
excessive mandatory disjoint packings give terminal contradictions.

These rules preserve T subset S subset U by induction. Shrinking U
preserves disjointness; a petal that becomes empty gives a contradiction
itself. The exact checker recomputes every actual AP, antecedent, color,
surviving petal, remaining integer budget and terminal condition. It
rejects extra initial hypotheses or supplied U/T states. The generator
uses bit masks and lists of squares; the checker uses sets and Euler's
criterion. No solver verdict, fractional guide or maximum-packing
assertion is trusted. STALLED, incomplete traces and timeouts establish
no exclusion.

## Complete endpoint-one root cover

AP(3421,47) is
3421,3468,3515,3562,3609,3656,3703. Euler's criterion verifies that its
six old points all belong to D and have original color1. At e=1,
progression avoidance therefore forces at least one of those six old
points into S. The outer checker derives these roots and requires
exactly all six files at endpoint1 and ORIGINAL caps(1848,29).
Overlap between roots is harmless; every hypothetical coloring supplies
at least one root. All six roots close directly, without further splits.

|Root|Forbidden|Forced|Packing|Empty-petal|Mixed|
|---:|---:|---:|---:|---:|---:|
|3421|2452|1|1158|1294|1335|
|3468|2156|4|577|1579|515|
|3515|2148|8|577|1571|515|
|3562|2142|6|582|1560|521|
|3609|2155|3|577|1578|515|
|3656|2946|0|578|2368|516|

Totals:13999 forbidden,22 forced,4049 packing,9950 empty-petal,3917
mixed and0 exhausted-budget deductions. Each terminal is an empty
required petal. Six checked nodes, zero splits and six closed leaves
cover the whole stated budget. The exclusion follows from necessary AP
constraints, rather than an enumeration of all candidate colorings.

## Uniform profile with separate numerical premises

The [endpoint-zero nonsquare lemma](../van_der_waerden_27_qr617_nonsquare30_endpoint0/PROOF.md)
gives e=0 => b>=30 and, by complement, e=1 => b<=1818.
Its graph is bafkreibuhhnqsgi7lzuird4j2vuzxivtvnfms76wdchyhyumqvdwweeiuq,
source119c250dcefc79e323825b5f7156e9e8646e9835.
Combined with the independent new lemma, this proves
30<=b<=1818 at BOTH endpoints.

The [square-class30 result](../van_der_waerden_27_qr617_class30_endpoint1/PROOF.md)
separately gives30<=a<=1818 at both endpoints, invoking its cited
endpoint-zero square premise. Its graph is
bafkreifgkgk7nhqgg37tn2uevjg7u7zkmqobvmn4nvqycqp6bsba4vzfdq,
source472605037f4fad6a4a67284eb0692e7ca7edf53e.
The [total62 profile](../van_der_waerden_27_qr617_62_edit_profile/PROOF.md)
separately gives62<=a+b<=3634. Its graph is
bafkreieu7guaiaarct57a7ohr2y32mcvgc5d4uwaj6kwodienf3o5u2i2e,
sourcebc987b1e75efcc6966135728c2f7bf2b61e32f93.

Consequently the combined necessary profile at EITHER endpoint is
30<=a,b<=1818 and62<=a+b<=3634. The only numerical possibilities at
total62 are (30,32),(31,31),(32,30). For example endpoint1,(a,b)=(1000,29)
satisfied the earlier numerical profile but is now excluded. These
three boundary pairs remain unresolved; no total63, attained repair
minimum, length3704 witness, global W upper bound or exact value is
asserted. The reproduction command for the new independent lemma does
not replay any of these separately cited numerical premises.

## Reproduction, attribution and trust

[generate.py](generate.py) performs six primitive searches using the
unchanged public kernel. [verify.py](verify.py) imports no generator,
pins the computational dependencies and independently replays exact root
coverage and every deduction. [checker_controls.py](checker_controls.py)
compares full strict/generic states and rejects missing roots, wrong
endpoint, swapped budgets, extra hypotheses, malformed APs, false
terminals and incomplete proofs, including under optimized Python.
[expected.json](expected.json) records every certificate hash and full
checking result. Hashes identify checked bytes, rather than prove truth.
The roughly1.56MB corpus remains outside Git and can be regenerated
without private transcripts. [evidence.json](evidence.json) records the
fresh reproduction and exact comparison with the recovered local audit.

The outer wrappers are adapted from the endpoint-zero nonsquare source;
exact hashes and source credits are in [provenance.json](provenance.json).
The AP implication, invariant induction, root cover and complement map
remain written unformalized mathematics. Exact Python semantics and
inspected checking code are trusted. The generator and checker share an
author; no external review or formalization is claimed. The combined
profile additionally trusts the three cited numerical contributions.

Complementary period618 construction barriers and variable affine-seam
bounds use different reference classes; no constants or endpoint
conditions are transferred from them. They are cited as context in
provenance, not as reviews of this result.

[Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
retain the inspected length-seven/two-color seed>3703 and prime617,
using W(length,colors); this campaign uses W(colors,length). The
[classical certificate](https://github.com/marijnheule/vdWaerden/blob/master/certificates/W_2_7_617.cert)
is primary context. No historical-priority or exhaustive current-best
claim is made. The unrestricted target coloring would imply W(2,7)>=3705.
