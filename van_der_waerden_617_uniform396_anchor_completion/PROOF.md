# Single-class anchor completion

Actual author: **six-vdw-3**, role **researcher**. Complete author
computer-assisted proof, with independent review of this extension
pending. Coordinates below are zero-based.

## References and claim

Put `N=3704`, `p=617`, `C=1852`. Let `q(r)=0` for a nonzero square modulo
617, `q(r)=1` for a nonsquare, and leave `q(0)` undefined. For
`s=0,...,616`, put `t=(1-s) mod617` and define

```text
T_s(x) = q(x-C+s)          for x<C,
         q(x-C+t) XOR 1    for x>=C.
```

All arguments of q are reduced modulo 617. Let `R_c={x:T_s(x)=c}`.
For any binary `f` on `{0,...,3703}` avoiding every actual integer AP
`{a+j*d:j=0,...,6}`, `d>0`, `0<=a<a+6*d<3704`, define
`E_c={x in R_c:f(x)!=c}` and `e_c=|E_c|`.
The candidate f has no symmetry, character, balance or periodicity
hypothesis. Undefined reference positions have arbitrary binary f-values
and contribute to neither edit count.

**New four-phase lemma.** At each `s in {184,201,205,269}`, every such f
satisfies `198<=e_c<=1651` for each c, hence
`396<=e_0+e_1<=3302`.

**Combined corollary.** Importing the exact earlier phase profile identified
in DEPENDENCIES.md, every phase `s=0,...,616` satisfies
`396<=e_0+e_1<=3302`. Individual floors of at least 198 cover 616 phases;
the remaining individual-197 phase is 611.

The result is a necessary-distance restriction on hypothetical AP-free
words. It asserts neither their existence nor their nonexistence.

## Why completing an anchor removes the other cap

Fix one of the four phases and suppose **only `e_1<=197`**. All the
rigidity conclusions used for class 1 have this single-class hypothesis.
Let K_1 be the checked unchanged set and `V=R_1\K_1`. No point of K_0 is
fixed here, and e_0 is unrestricted.

Each phase has the actual original-0 anchor AP A in the table below.
AP freedom requires some `r in A` to belong to E_0: otherwise all seven
final bits on A would be zero. Thus it suffices to contradict each of
the **seven** possibilities `r in E_0`, always using only `e_1<=197`.

| Phase | Actual anchor `(a,d)` | Replayed old roots | New roots | `|K_1|` | Full `|V|` |
|---:|---|---|---|---:|---:|
|184|(286,561)|847,1408,1969,2530,3091|286,3652|80|1769|
|201|(957,235)|1427,1662,1897,2132,2367|957,1192|78|1771|
|205|(19,438)|895,1333,1771,2209,2647|19,457|81|1768|
|269|(35,323)|1004,1327,1650,1973|35,358,681|107|1742|

The old joint-box proofs omitted the new roots because those positions
would have been unchanged under an additional `e_0<=197` hypothesis.
This proof supplies all of those omitted alternatives. The union of old
and new roots is checked to equal the entire actual anchor, with no
duplicate or missing position. A candidate may edit several anchor
positions; choosing any one of its edited positions is sufficient.

## Mandatory AP petals and exact weighted contradiction

In a root trial `r in E_0`, the final bit at r is one. Two types of AP
must meet E_1:

1. An AP entirely in R_1.
2. An AP consisting of r and six positions in R_1.

For the second type, leaving all six original-1 positions unchanged would
produce seven final ones. These are the only root activations used.
No pole, additional edited position or unknown antecedent is permitted.
Because K_1 is unchanged, the required petal is the actual intersection
of the AP with **all of V**, not a chosen partial mask.

For three distinct required APs with nonempty petals `P_1,P_2,P_3`, if
`P_1 intersect P_2 intersect P_3` is empty, their union needs at least
two edits. A single edit hitting all three would lie in the intersection.
Give single-AP demands 1 positive integer weights lambda, and triple-union
demands 2 positive integer weights omega. Write

```text
W = sum lambda + 2*sum omega,
L_x = sum of weights of all single petals or triple unions containing x.
```

If `L_x<=D` at **every** point x of V, then

```text
W <= sum_{x in E_1} L_x <= D*e_1 <= 197*D.
```

Consequently `W>197*D` is a strict contradiction. All nine new
certificates use `D=1000000`, with no surcharges. The exact checker
reconstructs q by Euler's criterion, checks actual integer AP geometry
and colours, reconstructs full petals, tests each triple intersection,
and accumulates all point loads with native integers.

| Phase | Root | W | `W-197D` | Single rows | Triple rows |
|---:|---:|---:|---:|---:|---:|
|184|286|200646970|3646970|938|0|
|184|3652|198486445|1486445|915|0|
|201|957|199416752|2416752|936|0|
|201|1192|198868959|1868959|931|0|
|205|19|197056434|56434|897|29|
|205|457|198985435|1985435|949|0|
|269|35|197307490|307490|923|0|
|269|358|200311447|3311447|947|0|
|269|681|199046003|2046003|941|0|

The frozen phase201 coefficients were obtained by reflecting original-1
root trials at 2746 and 2511. Their reflected actual APs are rechecked
directly; the source-only proposer generates the displayed roots directly.
The smallest new gap is `56434/1000000`. The smallest terminal gap
among all old and new roots is the old phase184/root1408 gap
`7490/1000000`. Neither is a floating solver tolerance.

## Inherited rigidity and domain chains

The selected old proof inputs and checkers are copied unchanged, with
per-file source commits and hashes in provenance.json. They are replayed
here, rather than treating their final masks as axioms.

An original-class AP packing of total S and denominator D_0 yields

```text
sum_{x in E_c} (D_0-L^0_x) <= D_0*e_c-S,
```

where all defects are nonnegative. This uses only that same class's cap.
For phases184,201,205, the old complete removed-zero trees exclude editing
any zero-load position under `e_c<=197`. Removing one such edited point
leaves at most196 other edits. Base defects confine those remaining edits
to the checked residual screen. Every binary tree has both children and
fresh split positions. Each leaf subtracts an explicit worst demand loss
over **all** removed zero positions before proving its strict weighted
contradiction. Therefore the displayed K_1 is unchanged without an e_0
bound. The class-0 replay is an arithmetic counterpart, not a hypothesis
imposed on the candidate in the class-1 root proof.

Phase269 uses the earlier complete low-load removal proof instead:
`K_c={x in R_c:L^0_x<=65000}`. Removing a putative low-load edit z
leaves196 edits, whose base defect sum is at most
`196D_0-S+65000`. The copied checker computes the demand loss for every
one of the107 possible z in each class. Its strict packing gap remains
positive after subtracting the largest loss and every surcharge. Hence
no such edit is possible under that class's197 cap. No opposite cap enters.

For old root chains, every stage is replayed on the full inherited domain.
Besides single rows and empty-intersection triples, some old stages use
five required petals with maximum point membership two. Hitting all five
then requires at least three edits, since two points cover at most four
petals. Where a stage has nonnegative surcharges `u_x`, it verifies
`L_x<=D+u_x` and subtracts `nu=sum u_x`. With
`L'_x=min(L_x,D)`, the demand lower bound becomes `W-nu`, and

```text
sum_{x in E_1}(D-L'_x) <= 197D-(W-nu).
```

A point with defect strictly greater than this nonnegative budget cannot
be edited. The next full domain is exactly the resulting screen, whose
hash must match the next stage. This justifies successive restrictions
without negative defects, unproved deletions or an opposite-class cap.
The phase201/root1427 historical prefix screen is also replayed first.
Old phase269 root rows are passed through the **new single-cap checker**;
their historical `caps=[197,197]` field is provenance metadata and supplies
no e_0 assumption. Their surcharge lists are checked empty.

The four complete anchors cover19 old roots and9 new roots. The old main
chains contain27 stages, plus the phase201/root1427 prefix stage.
Each terminal stage gives a strict contradiction. Thus no AP-free f with
`e_1<=197` exists at any of these phases, proving `e_1>=198`.

## Reflection, complement and the complete profile

For every phase the checker verifies
`T_s(3703-x)=1-T_s(x)` away from paired poles. Thus
`f'(x)=1-f(3703-x)` preserves AP freedom and exchanges e_0,e_1.
Applying the same single-class contradiction to f' gives `e_0>=198`.
This transforms a candidate; it does not assume candidate symmetry.

At the four new phases both original classes have1849 positions.
Whole-colour complement `1-f` preserves AP freedom and sends each
`e_c` to `1849-e_c`. Therefore `e_c<=1651` and the total is at most3302.

The earlier explicitly imported profile has612 phases with individual
198 or stronger floors, plus phase611 with a total396 floor. Its only
total395 phases are exactly184,201,205,269. The new four-phase result
therefore makes the total396 floor uniform over all617 references.
The updated total-floor histogram is

```text
396:50, 398:72, 400:116, 402:142, 404:128,
406:69, 408:26, 410:12, 412:1, 416:1.
```

The checker reconstructs all617 references and verifies class sizes:
1849 in616 phases,1848 in phase1. Complementation therefore gives an
upper bound `2*1849-396=3302` uniformly; phase1 has the stronger3300
consequence from its smaller class size. The other-phase proofs are
mathematical imports, not reexecuted by this package or proved by a hash.

Trust boundaries are this written argument, native Python integer/set
semantics, the attributed old exact checkers, and the explicitly imported
earlier mathematical profile. The proposer imports the checker for
post-proposal validation; the checker imports neither proposer nor solver.
No native optimality status, unsuccessful search or source publication
alone is used as a mathematical proof. This is not proof-assistant
formalization or an external independent review.
