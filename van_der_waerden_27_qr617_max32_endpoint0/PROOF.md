# Endpoint-zero equal-cap31 exclusion for fixed aligned QR617

Actual author: **six-vdw-2, researcher**, 2026-09-30.

Let c:[0,3703]->{0,1} avoid every monochromatic seven-term AP with
positive integer difference. Define
D={x in[0,3702]:617 does not divide x}, with q(x)=0 on nonzero squares
modulo617 and q(x)=1 on nonsquares. For S={x in D:c(x)!=q(x)}, let
a,b count edits in the ORIGINAL q0,q1 classes and let e=c(3703).
Each original class has1848 points. The seven old poles and endpoint
are free and uncounted. Actual c has no imposed symmetry or periodicity.
Translation by1 gives the[1,3704] target domain.

**Independent exact computer-assisted lemma:**

    e=0 implies max(a,b)>=32.

Equivalently no such coloring has e=0,a<=31,b<=31. Every new primitive
uses exactly ORIGINAL caps(31,31); previous numerical edit bounds are
not used by any branch.

Complementation preserves AP avoidance and sends
(e,a,b) to(1-e,1848-a,1848-b). Thus the independent new lemma also gives

    e=1 implies min(a,b)<=1816.

## Necessary clauses and exact replay

The unchanged [primitive proof](../van_der_waerden_27_qr617_mixed_edit_region/PROOF.md)
and [generic tree checker](../van_der_waerden_27_qr617_class29_disjunction/verify.py)
are the computational dependencies. Maintain T subset S subset U subset D,
initially T={root},U=D. A pole-free prefix AP partitions into its
original-class-i antecedent N and opposite-class petal P. AP avoidance
implies N subset S => P intersects S: otherwise all N points are flipped
and all P points unflipped, making the AP monochromatic. Endpoint clauses
are derived using the specified actual endpoint color e.

Under a contemplated edit v, a clause is mandatory when N minus{v}
is contained in T and P intersects T is empty. Clauses already activated
by T may participate even when their AP omits v. Each surviving petal
P intersect U needs an opposite-class edit. With R such edits remaining,
an empty petal or R+1 disjoint nonempty petals forbids v. Mandatory
singleton petals force their points; an exhausted class budget forbids
other unforced edits. Excessive forced counts, empty mandatory petals
or mandatory disjoint packings exceeding the remaining budget give
terminal contradictions.

The rules preserve T subset S subset U by induction. The checker
derives every integer AP, original color, antecedent, surviving petal,
disjointness, remaining integer budget and terminal condition. Supplied
U/T states and extra initial hypotheses are rejected. No solver verdict,
fractional guide or maximum-packing optimality is trusted. Incomplete
search, STALLED and timeouts establish no exclusion.

## Complete root and child coverage

AP(1,617) has terms1,618,1235,1852,2469,3086,3703. Its six old points
all lie in D with original color0. At e=0, AP avoidance forces at least
one old point into S. The outer checker independently derives exactly
these six root cases at ORIGINAL caps(31,31). Overlapping cases are
harmless; every hypothetical coloring in the box supplies a root.

The root1 primitive STALLED after87 checked forbidding deductions,
leaving3609 allowed positions and only root1 forced. This partial trace
alone is not an exclusion. AP(1,285) is mandatory in that replayed state.
Its full surviving opposite-class petal is

    {286,571,856,1141,1426,1711}.

For each point w in this petal, the child inherits the parent's checked
U/T and adds only w to T. Every possible S must contain at least one
petal point, so these six children form a complete disjunction. The
checker derives the entire petal, checks each child exactly once and
rejects missing, repeated or extraneous assumptions. The generator's
split plan supplies just AP(1,285); no supplied petal or state is trusted.
All six children close. The other five root cases close directly.

|Root|Nodes|Splits|Leaves|Forbidden|Forced|Packing|Empty-petal|Mixed|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|1|7|1|6|11727|3|9834|1893|10320|
|618|1|0|1|3162|0|1375|1787|1374|
|1235|1|0|1|3693|0|1845|1848|1845|
|1852|1|0|1|3662|0|1814|1848|1814|
|2469|1|0|1|3541|0|1693|1848|1693|
|3086|1|0|1|3125|0|1351|1774|1350|

Totals:12nodes,1split,11closed leaves;28910 forbidden,3forced,17912
packing,10998 empty-petal,18396 mixed and0 exhausted-budget deductions.
Ten leaves end in an empty mandatory petal. The root1/child571 leaf
has T={1,363,382,571}: one original-q0 and three original-q1 edits.
Its31 disjoint mandatory q0 petals exceed the remaining q0 budget30.
All terminal APs and this packing are exactly replayed.

## Uniform profile using two separate numerical premises

The [published endpoint1 lemma](../van_der_waerden_27_qr617_max32_endpoint1/PROOF.md)
gives e=1=>max(a,b)>=32 and, by complement, e=0=>min(a,b)<=1816.
Its graph is bafkreihbjzh7sdompvkm7aff6tdo63uhpckzcrltfl5vzefoi7edgoiioe,
source03bd90b4b786564eaa164360f765e109c9823b86. Combining it with the
new independent endpoint0 lemma gives, at BOTH endpoint colors,

    max(a,b)>=32 and min(a,b)<=1816.

The separately cited [uniform class30/total62 profile](../van_der_waerden_27_qr617_nonsquare30_endpoint1/PROOF.md)
gives30<=a,b<=1818 and62<=a+b<=3634, with its three explicit numerical
parents. Its graph is bafkreibznuuclypj37y3zawaphzeh5dgnvduhwqlt5runpxa7dl55b6izy,
sourcef3fd087db165cfdaef391aff0d47c75bb7077cda. These numerical premises
are not replayed by this command and enter no new branch hypothesis.

Consequently at either endpoint the only necessary total62 pairs are
(30,32),(32,30); the only necessary total3634 pairs are
(1816,1818),(1818,1816). The balanced pairs(31,31) and(1817,1817) are
excluded at both endpoints. Remaining pair feasibility is unresolved.
No total63, attained minimum, length3704 witness, unrestricted
nonexistence, new W bound or exact value follows.

## Reproduction and trust

[generate.py](generate.py) generates all six cases, with the root1
disjunction, from public source and a compact explicit AP plan.
[verify.py](verify.py) imports no generator, pins the computational
dependencies and checks every deduction and both levels of coverage.
[checker_controls.py](checker_controls.py) compares six full parent
states and rejects26 corruptions in normal and optimized Python.
[expected.json](expected.json) includes each certificate's hash and full
checking result. Hashes identify checked bytes; the proof is the written
soundness argument and exact replay.
[evidence.json](evidence.json) records fresh source-only reproduction
and exact comparison with the prior local audit. The6,305,338-byte
generated corpus stays outside Git and needs no private input.

Public ancestor source credits and pinned hashes are in
[provenance.json](provenance.json). Discovery uses bit masks and square
lists, while checking uses sets and Euler's criterion. Both share an
author. Written induction, cover and complement arguments and Python
integer semantics remain trusted; no external review or formalization
is asserted. The combined profile additionally uses the two separate
numerical premises above.

Period618 permissive three-AP domains and phase269 low-load rigidity
have different reference/counting domains. Their written sources and
graph bodies were read as context; no constants or endpoint conditions
are transferred and no citation is a review.
[Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
show length7/two colors>3703 and prime617, in length-first notation.
The campaign uses W(colors,length). The
[primary classical certificate](https://github.com/marijnheule/vdWaerden/blob/master/certificates/W_2_7_617.cert)
is context; no exhaustive current-best or historical-priority claim is made.
