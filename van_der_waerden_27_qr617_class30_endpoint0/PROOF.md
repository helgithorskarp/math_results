# Fixed aligned QR617: a full-width endpoint-zero class30 lemma

**six-vdw-2, researcher**, 2026-09-30. This advances the cited campaign
edit region. No historical-priority or attained-distance claim is made.

Let c on `[0,3703]` be binary and avoid every monochromatic seven-term
integer AP with positive difference. Put
`D={x in[0,3702]:617 does not divide x}`. Define q(x)=0 on nonzero
squares modulo617 and q(x)=1 on nonsquares. Let
`S={x in D:c(x)!=q(x)}`, `a=|S intersect q^{-1}(0)|`,
`b=|S intersect q^{-1}(1)|`, and `e=c(3703)`.
Each original class has1848 points; D has3696 points. All seven old
poles0,617,...,3702 and the endpoint are free and uncounted. The actual
candidate has no imposed symmetry or periodicity. Translation by one
gives the named `[1,3704]` target.

**Independent computer-assisted lemma.** `e=0 => a>=30`, with b
unrestricted over its full1848-point class. Equivalently, the cap box
`e=0,a<=29,b<=1848` contains no such coloring. Every new branch is
checked under these caps without any prior numerical cut.

**Complement consequence.** Complementing c preserves AP avoidance and
sends `(e,a,b)` to `(1-e,1848-a,1848-b)`. For e=1 the complement has
endpoint0, so `1848-a>=30`, or `a<=1818`. This proves no endpoint-one
lower30 or original-nonsquare lower30 statement.

## Exact AP rules and the inherited cover

Maintain `T subset S subset U subset D`, with original-class upper
budgets B0,B1. Initially `U=D,T={root}`. For a pole-free prefix AP,
partition its points into original-class-i points N and opposite-class
points P. AP avoidance implies `N subset S => P intersects S`: otherwise
changing every point of N and none of P makes the AP monochromatic.
An AP ending at3703 with six old points of original color e similarly
requires an edit among those points. No clause constrains an old pole.

Under a contemplated edit v, a conditional AP has
`N minus{v} subset T` and `P intersect T=empty`. Already mandatory
clauses may omit v; endpoint petals used conditionally belong to the
original class opposite v. Each surviving positive petal `P intersect U`
requires an opposite-class edit. An empty petal, or R+1 pairwise disjoint
nonempty petals when only R such edits remain, forbids v. Strict tag f
requires v to belong to its AP; mixed tag m permits already mandatory
clauses. A singleton mandatory petal forces its point. Exhausting a
class budget forbids all remaining unforced edits in that class. Exact
terminal contradictions are excessive forced counts, an empty required
petal, or an excessive required packing. The
[mixed-clause proof](../van_der_waerden_27_qr617_mixed_edit_region/PROOF.md)
gives the primitive rules in full. Every AP, antecedent, color, surviving
petal, disjointness and integer count is replayed in sequence.

At a checked stalled state a mandatory unsatisfied AP has positive set P
and full surviving petal `K=P intersect U`. Every actual S must hit K.
One child for every w in K covers all candidates at that parent. Each
child starts from the replayed U and `T union{w}`, with unchanged
endpoint, outer root and budgets. Children can overlap; no exclusivity
claim is required. Induction over the finite checked tree proves parent
exclusion once every child closes. The unchanged
[generic tree checker](../van_der_waerden_27_qr617_class29_disjunction/verify.py)
checks every child with separate inherited states and rejects supplied
initial U/T or extra hypotheses. Any open child blocks exclusion. A
child trace alone is not a valid complete singleton proof; the earlier
strict singleton checker remains unchanged. STALLED and time limits
prove no exclusion. No fractional weight, solver verdict or optimal
packing assumption is used.

## All six roots and all28 children

Endpoint0 AP(1,617) consists of six old original-square points and the
endpoint. Thus S must contain one of
`1,618,1235,1852,2469,3086`. The outer checker derives this root cover
using Euler's criterion and requires exactly those six files at
`e=0,B=(29,1848)`. The second cap equals the entire original class size;
it places no constraint on b.

All six primitive root closures stall and have only the root forced.
None is an exclusion on its own. Their checked deductions yield the
following mandatory APs and full surviving petals:

| Root | Parent forbidden deductions | Mandatory AP | Every child edit |
|---:|---:|---|---|
|1|49|`(1,314)`|315,629,943,1571,1885|
|618|46|`(618,285)`|903,1188,1473,2043,2328|
|1235|47|`(1213,11)`|1213,1224,1246,1268,1279|
|1852|43|`(1084,192)`|1084,1468,2044,2236|
|2469|41|`(24,489)`|24,513,1002,2958|
|3086|49|`(1838,208)`|2046,2254,2462,2670,2878|

Every child is replayed in its actual inherited state and closes with
the same caps. The collection has34 nodes,6 splits and28 terminal
leaves. Its checked totals are46041 forbidden,46041 packing,45561 mixed,
2 forcing,0 empty-petal and0 exhausted-budget deductions. The checker
reconstructs every full child set from the parent's replay, rather than
trusting this table. The full root cover proves the lemma.

## Separate numerical premise for the combined profile

The [published62 profile](../van_der_waerden_27_qr617_62_edit_profile/PROOF.md)
gives `29<=a,b<=1819` and `62<=a+b<=3634` at either endpoint. Combining
that theorem with the independent lemma and its complement yields

```
e=0: 30 <= a <= 1819,       e=1: 29 <= a <= 1818,
both endpoints: 29 <= b <= 1819,       62 <= a+b <= 3634.
```

At total62 the pairs still permitted at e=0 are
`(30,32),(31,31),(32,30),(33,29)`; at e=1 they are
`(29,33),(30,32),(31,31),(32,30),(33,29)`. Every feasibility question
remains unresolved. The earlier62 region did not remove a count pair
such as `(29,1000)`; the new e=0 full-width class cut does.

The separate numerical premise is graph
`bafkreieu7guaiaarct57a7ohr2y32mcvgc5d4uwaj6kwodienf3o5u2i2e`, source
`bc987b1e75efcc6966135728c2f7bf2b61e32f93`. Its uniform lower29 premise
and older dependencies are documented there. The present replay command
does not reprove that numerical theorem. The class29 source supplies only
the unchanged generic checking algorithm to the independent lemma.
No endpoint-one lower30, uniform class30 or total63 bound is asserted.

## Reproduction, trust and complementary work

[generate.py](generate.py) uses the published square/bit-mask kernel;
[verify.py](verify.py) imports the unchanged Euler/set generic checker
without importing a generator. [checker_controls.py](checker_controls.py)
checks primitive compatibility, a small Boolean cover oracle, inherited
states, partial trees, omitted roots and corrupted hypotheses. Both
normal and optimized-interpreter controls use explicit checks, not assert.
[provenance.json](provenance.json) pins exact computational sources and
labels the separate numerical dependency. The outer wrappers and controls
are adapted from the cited62 suite.

[expected.json](expected.json) holds the full entry-level manifest and
checking summaries. Hashes identify checked bytes; no hash substitutes
for proof replay. The roughly14MB generated corpus stays outside Git.
Generation needs no private transcript input.
[evidence.json](evidence.json) records fresh generation, comparison with
the earlier local six-tree audit, control results and bounded resources.

Exact Python semantics and the inspected checking code are trusted. The
AP implication, invariant/tree induction, root cover and complement map
remain written unformalized mathematics. The independent generator and
checker share an author; no external review or formalization is asserted.
Only the combined corollary additionally uses the published62 theorem.
No length3704 witness, global W upper bound, exact W value or attained
minimum repair distance is established.

[Period618 triple pruning](../van_der_waerden_618_triple_pruning/README.md)
concerns different cyclic construction words and local move barriers;
the supplied words are invalid. The newer
[class197 seam covers](../van_der_waerden_617_class197_cover/PROOF.md)
give197 edits per reference color across617 reflection-antisymmetric
keys `(s,1-s,1)`, using a separate older613-phase numerical dependency.
Those partial seam references and their class sizes differ from this
fixed aligned prefix. No constant is imported or added here. Neither
work reviews the present result; their certificates were not audited here.

[Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give the inspected length-seven/two-color seed>3703 and prime617, using
W(length,colors). The campaign uses W(colors,length). The
[classical QR certificate](https://github.com/marijnheule/vdWaerden/blob/master/certificates/W_2_7_617.cert)
is primary context. No exhaustive current-best or historical-priority
claim is made; asymmetric w(3,k) is a different problem. The unrestricted
length3704 construction remains the target and would imply W(2,7)>=3705.
