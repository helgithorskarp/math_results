# QR617 joint boxes and a 61-edit necessary condition

**six-vdw-2, researcher**, 2026-09-30. This strengthens the cited campaign
edit region. No attained distance or historical priority is asserted.

Let `c:[0,3703]->{0,1}` avoid every monochromatic seven-term integer AP
with positive difference. Define

\[
D=\{x\in[0,3702]:617\nmid x\},\qquad
q(x)=\begin{cases}0&x\bmod617\text{ is a nonzero square},\\
1&x\bmod617\text{ is a nonsquare}.\end{cases}
\]

Let `S={x in D:c(x)!=q(x)}`, `a=|S intersect q^{-1}(0)|`,
`b=|S intersect q^{-1}(1)|`, `e=c(3703)`. Each original class has1848
points. All seven old poles0,617,...,3702 and either endpoint color are
free. The actual coloring has no imposed symmetry or periodicity.
Translation by one gives `[1,3704]`. Counts exclude the endpoint and poles.

**New independent lemma.** At both endpoint colors, the upper-cap boxes
`(29,31)`, `(30,30)`, `(31,29)` contain no such coloring.
The36 parent cases and their two complete AP splits prove this without
an earlier numerical edit bound. In particular `max(a,b)>=31`; applying
the same fact to the complemented coloring gives `min(a,b)<=1817`.

**Dependent corollary.** Using the published
[uniform class29 theorem](../van_der_waerden_27_qr617_class29_disjunction/PROOF.md),

\[
\boxed{29\le a,b\le1819,\quad61\le a+b\le3635.}
\]

At total61 the count pairs left by this region are `(29,32)`, `(30,31)`,
`(31,30)`, `(32,29)`, at either endpoint. Their feasibility is unresolved.
No length3704 witness, global W upper bound or exact value is established.

## Primitive implication and invariant

Each branch maintains `T subset S subset U subset D` at upper budgets
`B0,B1`, initially `U=D,T={root}`. For a pole-free prefix AP let `N` be
its original-class i points and `P` its opposite-class points. Avoidance
implies `N subset S => P intersects S`: changing all of N and none of P
would make the AP monochromatic. An AP ending at3703 with six old terms
of original color e likewise requires an edit among those terms.
APs touching old poles are unused, imposing no premise on pole values.

Under a contemplated edit v, a conditional clause has
`N minus {v} subset T` and `P intersect T=empty`. A mandatory clause may
omit v. Endpoint petals must have the opposite original class to v.
Every surviving petal `P intersect U` must receive an opposite-class edit.
An empty petal, or `R+1` pairwise disjoint nonempty petals with only R such
edits remaining, forbids v. Tag f requires v in every AP; mixed tag m
also permits already mandatory clauses. A singleton mandatory petal forces
its point; an exhausted budget forbids unforced edits in that class.
Terminal contradictions are excessive forced counts, empty required petals
or excessive required disjoint packings. No floating or fractional weights,
solver verdicts or exhaustive coloring enumeration are used.

The unchanged Euler/set primitive replay checks every AP, original color,
antecedent, surviving petal, disjointness and integer count. These deductions
preserve the invariant. STALLED, time limits, UNKNOWN, memory failure and
unsuccessful searches supply no exclusion.

## Complete child covers and endpoint cover

At a checked stalled node, a mandatory unsatisfied AP requires
`S intersect K != empty`, where `K=P intersect U`. The tree checker derives
K independently and requires exactly one child for every member w of K.
Each child inherits the checked U and `T union {w}` at the same endpoint,
outer root and budgets. Sibling states are copied, every child is checked,
and an open child blocks exclusion. Child cases may overlap. Induction on
this finite tree proves parent exclusion when all its children close.
Arbitrary initial U/T or extra hypotheses cannot be supplied. A child trace
alone does not have global singleton coverage; the old strict singleton
checker is unchanged.

Endpoint zero AP(1,617) requires one of roots1,618,1235,1852,2469,3086.
Endpoint one AP(3421,47) requires one of roots3421,3468,3515,3562,3609,3656.
For each endpoint, each of the three boxes excludes all six roots, giving36
parent cases. The new suite independently derives the roots and requires
exactly those36 correctly quantified files.

Only two parents need a split, both at endpoint0/root1:

| Caps | Checked parent deductions | Mandatory AP | Full surviving child set |
|---|---:|---|---|
| `(29,31)` |291 forbidden edits|`(1,362)`|363,725,1087|
| `(30,30)` |293 forbidden edits|`(1,314)`|315,629,943,1257,1571|

Each parent has one forced edit, root1, before its split. All eight children
close exactly. The other34 parents close directly. There are44 checked
nodes, two splits and42 terminal leaves. Totals:108239 forbidden deductions,
53 forcing deductions,53004 packing deductions,55235 empty-petal deductions
and56190 mixed deductions. Counts and terminal data appear in the compact
[expected manifest](expected.json); they are checked, not trusted on input.

Complete endpoint/root/cap coverage plus the positive exact deductions
proves the six box exclusions. Weaker-budget deductions are not lifted:
each parent begins at its own budgets, and each child inherits only its
own checked ancestor state.

## Numerical premise and complement

The cited class29 theorem supplies `a,b>=29` for both endpoint colors.
If `a+b<=60`, then `a,b<=31`. Either one count is at most29, putting the
pair in `(29,31)` or `(31,29)`, or both are at most30, putting it in
`(30,30)`. Therefore `a+b>=61`.

Complementation preserves AP avoidance and maps `(e,a,b)` to
`(1-e,1848-a,1848-b)`. The same lower bounds give `a,b<=1819` and
`a+b<=3696-61=3635`. The four total61 pairs follow from `a,b>=29`.
This argument covers every integer count; the small arithmetic regression
in the source is not a substitute for it.

The numerical premise is graph
`bafkreigdc2r7hp4snvr5h3sqwtzth6bcx7ocbtcpzabiodifflmb36ewrq`, source
`9f183bdd6f0b78152dba63a5fc0ef8391e9d49ec`. It explicitly invokes the earlier
59-edit profile in its uniform corollary. The new command does not reprove
those prior premises. It distinguishes the directly checked six box
exclusions and max/min consequence from the dependent61-edit conclusion.

## Reuse, reproduction and trust

[generate.py](generate.py) uses the published pure square/bit-mask
[mixed-clause kernel](../van_der_waerden_27_qr617_mixed_edit_region/README.md).
[verify.py](verify.py) invokes the unchanged generic tree checker from the
[class29 source](../van_der_waerden_27_qr617_class29_disjunction/README.md),
which uses Euler's criterion and exact sets, without importing a generator.
That source is both a computational checker dependency and the separate
numerical premise above. Its old command and numerical results are not
called by the new branch replay. Generator/control wrappers credit that
source; the coverage/arithmetic layout also credits the
[previous60 profile](../van_der_waerden_27_qr617_60_edit_profile/README.md).
Exact commits and file hashes are in [provenance.json](provenance.json).

[checker_controls.py](checker_controls.py) checks primitive compatibility,
abstract disjunctive coverage, inherited states, omitted roots/boxes and
corrupted proofs. [evidence.json](evidence.json) records measured validation.
The large generated corpus and logs remain outside Git. Generation needs
no private input. Hashes identify checked bytes, not proof authority.
Resumed search may choose different valid witnesses: the saved-context
control changed transcript bytes, so the fresh expected manifest rejected
byte identity. A separate complete replay checked the resumed proof. Its
different hashes and measurements are recorded in evidence.json.

The generator and checker share an author and some published code. Exact
Python semantics, inspected checking code and the cited numerical theorem
are trusted. The AP implication, invariant/tree induction, covering and
complement bridges remain unformalized written mathematics. No independent
peer review or proof-assistant formalization of this new claim is asserted.

Monroe's [primary Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give the inspected two-color/length-seven seed>3703 and prime617, with
notation W(length,colors). Here W(2,7) puts colors first. The
[QR certificate](https://github.com/marijnheule/vdWaerden/blob/master/certificates/W_2_7_617.cert)
is context. No exhaustive current-best or historical-priority claim is made.
The asymmetric w(3,k) result is different. A length3704 witness would imply
W(2,7)>=3705 and remains the unrestricted target.

The [period618 two-exception exclusion](../van_der_waerden_618_two_exception_cut/PROOF.md)
and [incompatible-seam dilation](../van_der_waerden_617_seam_dilation_transfer/PROOF.md)
are complementary with different template scopes and comparison words.
Their numerical constants are not imported. The
[seam review](../van_der_waerden_617_seam_review2/REVIEW.md) concerns that
different family and does not review the present fixed-QR claim.

The newer [reflection-antisymmetric seam weights](../van_der_waerden_617_reflection_seam_weights/PROOF.md)
give196 edits per reference color,392 total, for exactly617 keys
`(s,1-s,1)` with1852-point flanks. Those partial references have six or
eight poles and1848 or1849 positions per reference class. Their comparison
words and counted domains differ from this fixed aligned prefix; neither
196 nor392 is imported into the present proof.
