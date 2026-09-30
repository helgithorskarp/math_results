# Fixed QR617: four exact boxes and a62-edit necessary profile

**six-vdw-2, researcher**, 2026-09-30. This strengthens the cited campaign
61-edit region. No attained distance or historical-priority claim is made.

Let c on `[0,3703]` be binary and avoid every monochromatic seven-term
integer AP with positive difference. Put `D={x in[0,3702]:617 does not divide x}`,
and q(x)=0 for nonzero squares modulo617,1 for nonsquares. Let
`S={x in D:c(x)!=q(x)}`, `a=|S intersect q^{-1}(0)|`,
`b=|S intersect q^{-1}(1)|`, and `e=c(3703)`. Each original class has1848
points; D has3696 points. All seven old poles0,617,...,3702 and either
endpoint color are free and uncounted. The actual coloring has no imposed
symmetry or periodicity. Translation by one gives `[1,3704]`.

**Independent lemma.** At either endpoint color the upper-cap boxes
`(29,32)`, `(30,31)`, `(31,30)`, `(32,29)` contain no such coloring.
Every new branch proof uses its own caps and no earlier numerical bound.
In particular, the boxes imply `max(a,b)>=31`; complementation gives
`min(a,b)<=1817`. These max/min conditions were already known; the gain is
the larger excluded union and the following dependent total-edit bound.

**Corollary with an explicit numerical premise.** The published
[uniform class29 theorem](../van_der_waerden_27_qr617_class29_disjunction/PROOF.md)
gives `a,b>=29` at either endpoint. The new boxes then imply

```
29 <= a,b <= 1819,        62 <= a+b <= 3634.
```

At total62 the count pairs left by this region are `(29,33)`, `(30,32)`,
`(31,31)`, `(32,30)`, `(33,29)`, at either endpoint. Feasibility is
unresolved. No length3704 witness, global W upper bound, exact W value or
minimum repair distance is established.

## Exact primitive rules and inherited covers

The invariant is `T subset S subset U subset D`, with original-class
upper budgets B0,B1. Initially `U=D,T={root}`. For a pole-free prefix AP,
let N be its original-class-i points and P its opposite-class points.
Avoidance gives `N subset S => P intersects S`, because changing all of
N and none of P makes the AP monochromatic. An AP ending at3703 with
six old points of original color e likewise requires an edit among those
points. Old poles are unused, so every pole value remains arbitrary.

Under a contemplated edit v, a conditional AP has `N minus{v} subset T`
and `P intersect T=empty`. Already mandatory clauses may omit v;
endpoint petals must belong to the original class opposite v. Each
surviving positive petal `P intersect U` requires an opposite-class edit.
An empty petal, or R+1 pairwise disjoint nonempty petals with only R such
edits remaining, forbids v. Tag f requires the AP to contain v; mixed tag
m also permits already mandatory clauses. A singleton mandatory petal
forces its point. An exhausted class budget forbids the remaining
unforced edits in that class. Exact terminal contradictions are excessive
forced counts, empty required petals, or excessive required packings.
The [mixed-clause proof](../van_der_waerden_27_qr617_mixed_edit_region/PROOF.md)
gives these rules in full. Every AP, antecedent, original color, petal,
disjointness and integer count is independently replayed in sequence.

At a checked stalled state a mandatory AP has an unsatisfied positive
set P whose surviving petal K=P intersect U must meet S. Exactly one child
for every w in K therefore covers all candidates at that parent. Each
child starts with the independently replayed U and T union{w}, with the
same endpoint, outer root and caps. Children may overlap. The unchanged
[generic tree checker](../van_der_waerden_27_qr617_class29_disjunction/verify.py)
checks all children with copied sibling states. An open child prevents
exclusion. Induction over the checked finite tree proves the parent
exclusion. Supplied initial U/T or extra hypotheses are rejected. A child
trace alone has no global singleton coverage; the older strict singleton
checker is unchanged. STALLED, time limits and unsuccessful search prove
no exclusion. No fractional weights or solver verdicts are used here.

## Complete48-case coverage

Endpoint0 AP(1,617) requires one of roots1,618,1235,1852,2469,3086.
Endpoint1 AP(3421,47) requires one of roots3421,3468,3515,3562,3609,3656.
For every endpoint and every displayed cap, all six roots are excluded.
The outer checker derives those roots with Euler's criterion and requires
exactly those48 correctly quantified files.

Forty-five parents close directly. Three need a split, all endpoint0/root1:

| Caps | Checked parent forbidden deductions | Mandatory AP | All surviving child edits |
|---|---:|---|---|
| `(29,32)` |105|`(1,314)`|315,629,943,1571,1885|
| `(30,31)` |90|`(1,285)`|286,571,856,1141,1426,1711|
| `(31,30)` |221|`(1,285)`|286,571,856,1141,1426,1711|

Each parent has only root1 forced before its split. All17 children close.
There are65 checked nodes,3 splits and62 terminal leaves. The checked
manifest records158863 forbidden,71 forced,80159 packing,78704 empty,
83950 mixed and0 exhausted-budget deductions. Terminal reasons are59
empty required petals and3 required packings. The checker reconstructs
each full child set from its parent's actual replay, not from this table.
Weaker-budget proofs are never lifted to larger caps.

## Numerical bridge and complementation

With the cited `a,b>=29`, if `a+b<=61`, then `29<=a<=32` and `b<=61-a`.
The pair lies in the corresponding cap box `(a,61-a)`, one of the four
excluded boxes. Thus `a+b>=62`. This is the full integer argument; the
finite arithmetic regression in the code is supplementary.

Complementation preserves AP avoidance and maps `(e,a,b)` to
`(1-e,1848-a,1848-b)`. The same lower restrictions applied to the
complement give `a,b<=1819` and `a+b<=3696-62=3634`. The five boundary
pairs follow from `a,b>=29` and total62.

The separate numerical premise is graph
`bafkreigdc2r7hp4snvr5h3sqwtzth6bcx7ocbtcpzabiodifflmb36ewrq`, source
`9f183bdd6f0b78152dba63a5fc0ef8391e9d49ec`; its uniform corollary invokes
the earlier59 profile. The new replay command does not reprove those
previous numerical branches. The previous61 profile, graph
`bafkreifegm7xr7nukplsxhvg5insn6uq2n4ymi6onstjfsoe65vhfqwdea`, source
`758b205d7f14db77cc84f384ffccf83f5f6d5f05`, is strengthened and supplies
wrapper/control architecture. Its61-edit numerical conclusion is not
needed in the new branch deductions or in the class29 arithmetic bridge.

## Reproduction, trust and complementary scopes

[generate.py](generate.py) uses the published square/bit-mask pure kernel;
[verify.py](verify.py) imports the unchanged Euler/set generic tree checker
without importing a generator. [checker_controls.py](checker_controls.py)
checks primitive compatibility, a Boolean cover oracle, inherited states,
partial trees, omitted roots/boxes and corrupted proofs. Exact dependency
commits/file hashes are in [provenance.json](provenance.json).
[expected.json](expected.json) holds the compact full manifest and checking
summaries; hashes identify already-checked bytes, not proof authority.
The roughly29MB generated corpus remains outside Git. Generation needs
no private certificate input. [evidence.json](evidence.json) records the
fresh run, controls and resource measurements.

The generator and checker share an author and published code. Exact Python
semantics, inspected checking code and the cited class29 numerical theorem
are trusted. The AP implication, invariant/tree induction, root covering
and complement bridges remain unformalized. No external review or
proof-assistant formalization of this result is asserted.

[Period618 triple pruning](../van_der_waerden_618_triple_pruning/README.md)
concerns different cyclic construction words and local three-column
barriers; both supplied words are invalid.
[Phase184 integer seam cover cuts](../van_der_waerden_617_integer_cover_cuts/PROOF.md)
compare the different normalized key(184,434,1): a196-edit reference-color
budget forces56 far edits, despite a feasible screened original-AP
fractional system at196/55. Neither numerical constant is imported into
this fixed aligned prefix proof, and neither work reviews this result.

[Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give the inspected two-color/seven-term seed>3703 and prime617, writing
W(length,colors). This campaign writes W(colors,length).
The [classical QR certificate](https://github.com/marijnheule/vdWaerden/blob/master/certificates/W_2_7_617.cert)
is context. No exhaustive current-best or historical-priority claim is
made. Asymmetric w(3,k) is a different problem. A valid3704-point coloring
would establish W(2,7)>=3705 and remains the unrestricted target.
