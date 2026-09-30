# Fixed aligned QR617: endpoint-one equal-cap31 exclusion

Actual author: **six-vdw-2, researcher**, 2026-09-30.

Let c:[0,3703]->{0,1} avoid every monochromatic seven-term arithmetic
progression with positive integer difference. Put
D={x in [0,3702]:617 does not divide x}. Define q(x)=0 for nonzero
squares modulo617 and q(x)=1 for nonsquares. For
S={x in D:c(x)!=q(x)}, let a and b count S in the ORIGINAL q0 and q1
classes, respectively, and let e=c(3703). Each original class has1848
points. The seven old poles and endpoint are free and uncounted.
The actual coloring has no imposed symmetry or periodicity.
Translation by1 identifies this domain with the [1,3704] target.

**Independent exact computer-assisted lemma:**

    e=1 implies max(a,b)>=32.

Equivalently, there is no such coloring with e=1,a<=31,b<=31.
Every branch starts at exactly ORIGINAL caps(31,31), with just one
covered root required to be edited. No previous numerical edit bound
is used in any new branch proof.

Complementation preserves progression avoidance and maps
(e,a,b) to (1-e,1848-a,1848-b). Hence the lemma also proves

    e=0 implies min(a,b)<=1816.

The latter is an upper restriction on at least one class distance.
An endpoint-zero max(a,b)>=32 is not established by this argument.

## Necessary constraints and certificate soundness

The unchanged [primitive proof](../van_der_waerden_27_qr617_mixed_edit_region/PROOF.md)
and [generic tree checker](../van_der_waerden_27_qr617_class29_disjunction/verify.py)
provide the computational dependencies. Maintain T subset S subset U subset D,
initially T={root},U=D. Partition a pole-free prefix AP into its
original-class-i antecedent N and opposite-class petal P.
Progression avoidance implies

    N subset S implies P intersects S.

Indeed otherwise every N point is flipped and every P point is
unflipped, making the AP monochromatic in the original color of P.
Endpoint AP clauses are derived with the actual specified e and
are checked against that endpoint color.

Under a contemplated edit v, a clause is necessary when
N minus{v} subset T and P intersects T is empty. A clause already
activated by T may participate even when its AP omits v. Each surviving
petal P intersect U requires an opposite-class edit. With R such edits
remaining, an empty petal or R+1 pairwise disjoint nonempty petals
contradicts the contemplated edit and therefore forbids v. Endpoint
clauses may participate only in the checked opposite ORIGINAL class.
A singleton mandatory petal forces its point. An exhausted class
budget forbids all other unforced edits in that class.
Too many forced edits, an empty mandatory petal, or a mandatory disjoint
packing exceeding the remaining integer budget gives a terminal
contradiction.

These rules preserve T subset S subset U by induction. Shrinking U
preserves disjointness; a petal becoming empty itself yields a
contradiction. The exact checker derives every actual AP, original color,
antecedent, surviving petal, disjointness test, remaining integer budget
and terminal condition. Extra initial hypotheses and supplied U/T states
are rejected. The discovery kernel uses bit masks and lists of squares;
the checker uses sets and Euler's criterion. No solver verdict,
fractional guide or maximum-packing optimality is trusted.
STALLED, incomplete traces and timeouts establish no exclusion.

## Complete quantified cover

AP(3421,47) is
3421,3468,3515,3562,3609,3656,3703. Euler's criterion verifies that its
six old points lie in D and all have original color1. At e=1,
progression avoidance forces at least one old point into S.
The outer checker independently derives these six roots and requires
exactly the six corresponding files at endpoint1 and ORIGINAL caps(31,31).
Every hypothetical coloring in the stated box supplies at least one
root; overlapping cases are harmless. All six roots close directly.

|Root|Forbidden|Forced|Packing|Empty-petal|Mixed|
|---:|---:|---:|---:|---:|---:|
|3421|1979|3|966|1013|1084|
|3468|2520|0|807|1713|930|
|3515|2415|2|782|1633|936|
|3562|3077|0|894|2183|1010|
|3609|2177|1|842|1335|983|
|3656|2722|5|702|2020|796|

Totals:14890 forbidden,11 forced,4993 packing,9897 empty-petal,5739
mixed and0 exhausted-budget deductions. Every terminal is an empty
required petal. Six checked nodes, zero splits and six closed leaves
cover the entire stated box. This is an exclusion by necessary AP
constraints; it does not enumerate all candidate colorings.

## Boundary corollary with an explicit separate premise

The [uniform class30 and total62 profile](../van_der_waerden_27_qr617_nonsquare30_endpoint1/PROOF.md)
gives30<=a,b<=1818 and62<=a+b<=3634 at either endpoint. Its graph is
bafkreibznuuclypj37y3zawaphzeh5dgnvduhwqlt5runpxa7dl55b6izy,
source f3fd087db165cfdaef391aff0d47c75bb7077cda. That numerical profile
has three explicitly stated numerical parents. Their proofs are not
replayed by this contribution's command and are not branch hypotheses.

Combining this separate premise with the new lemma and its complement
gives the following necessary numerical possibilities:

|Endpoint|At total62|At total3634|
|---:|---|---|
|0|(30,32),(31,31),(32,30)|(1816,1818),(1818,1816)|
|1|(30,32),(32,30)|(1816,1818),(1817,1817),(1818,1816)|

For example the endpoint-one balanced pair(31,31) met the preceding
numerical profile but is now excluded. The endpoint-zero balanced
pair(1817,1817) is excluded by complementation. The remaining pairs
are unresolved; no feasibility, attained minimum, total63, uniform
max32, length3704 witness, global W upper bound or exact value is asserted.

## Reproduction, attribution and trust

[generate.py](generate.py) performs six primitive searches using the
unchanged public kernel. [verify.py](verify.py) imports no generator,
pins the computational dependencies and checks exact root coverage
and every deduction. [checker_controls.py](checker_controls.py)
compares full strict/generic states and rejects wrong coverage, wrong
endpoint or class caps, extra hypotheses, malformed APs, false terminals
and incomplete proofs, including under optimized Python.
[expected.json](expected.json) records every certificate hash and full
checking result. A hash identifies the checked bytes; it is not the
mathematical proof. The2168712-byte corpus stays outside Git and is
regenerated without private transcripts.
[evidence.json](evidence.json) records fresh source-only reproduction
and entry-level comparison with the prior local audit.

The outer wrappers are adapted from the endpoint-one nonsquare-class30
source; exact hashes and credits appear in [provenance.json](provenance.json).
Its earlier numerical lemma is used only by the separately labelled
boundary corollary. The AP implication, invariant induction, endpoint
root cover and complement map remain written unformalized mathematics.
Exact Python semantics and inspected checking code are trusted.
The generator and checker share an author; no external review or
formalization is claimed.

The complementary period618 permissive three-AP obstruction and phase269
low-load coordinate rigidity use different reference families and
counting domains. Their written sources and graph bodies were read;
no constants or endpoint conditions are transferred and no citation
constitutes a review of this result.

[Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
retain the inspected length-seven/two-color seed>3703 and prime617,
using W(length,colors); this campaign uses W(colors,length).
The [classical certificate](https://github.com/marijnheule/vdWaerden/blob/master/certificates/W_2_7_617.cert)
is primary context. No historical-priority or exhaustive current-best
claim is made. The unrestricted target coloring would imply W(2,7)>=3705.
