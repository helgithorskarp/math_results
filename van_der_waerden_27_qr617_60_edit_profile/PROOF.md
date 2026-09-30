# QR617 joint edit boxes and the 60-change distance cut

**six-vdw-2, researcher**, 2026-09-30. This is a complete exact
computer-assisted necessary condition, strengthening the cited campaign
profile. It asserts no optimal distance or historical priority.

Let `c:[0,3703]->{0,1}` avoid every monochromatic seven-term integer
arithmetic progression with positive difference. Set

\[
D=\{x\in[0,3702]:617\nmid x\},\qquad
q(x)=\begin{cases}0&x\bmod617\text{ is a nonzero square},\\
1&x\bmod617\text{ is a nonsquare}.\end{cases}
\]

Write `S={x in D:c(x)!=q(x)}`, `a=|S intersect q^{-1}(0)|`,
`b=|S intersect q^{-1}(1)|`, `e=c(3703)`. Each original class has
1848 positions. All seven old poles `0,617,...,3702` and the new
endpoint color are free. The reference is fixed and aligned; the actual
coloring has no assumed periodicity, affine symmetry or template structure.
Translation by one gives the named interval `[1,3704]`.

**New lemma.** At either endpoint color, neither upper-cap box
`(a<=29,b<=30)` nor `(a<=30,b<=29)` contains a valid coloring.
The 24 new transcripts prove these four exclusions without an earlier
numerical edit bound.

**Dependent corollary.** Using the published
[uniform original-class29 theorem](../van_der_waerden_27_qr617_class29_disjunction/PROOF.md),
every such coloring satisfies

\[
\boxed{29\le a,b\le1819,\qquad60\le a+b\le3636.}
\]

Thus at total 60 the only count pairs left by this necessary region are
`(29,31)`, `(30,30)` and `(31,29)`, at either endpoint. Their feasibility
remains unresolved. This supplies no length-3704 witness, global van der
Waerden upper bound, exact value or attained-distance classification.
The total counts concern the 3696 nonpole **prefix** positions, excluding
the new endpoint as well as the seven old poles.

## Exact AP implication and checked invariant

Each branch maintains `T subset S subset U subset D` under upper budgets
`B0,B1`. Initially `U=D,T={root}`. The old strict singleton checker is
unchanged and rejects additional covering hypotheses.

For a pole-free prefix AP, let `N` be its points of original class `i`
and `P` its points of original class `1-i`. Avoidance gives

\[
N\subseteq S\quad\Longrightarrow\quad P\cap S\ne\varnothing.
\]

Changing all of `N` and none of `P` would make the AP monochromatic in
color `1-i`. An AP ending at 3703 whose six old terms all have original
color `e` similarly requires an edit among those six terms. APs touching
old poles are unused; their arbitrary values impose no hidden premise.

To forbid a contemplated edit `v` of original class `i`, each cited prefix
clause has `N minus {v} subset T` and `P intersect T=empty`. An already
mandatory clause may omit `v`. Endpoint clauses must require edits in
original class `1-i`. Under `v in S`, every surviving petal `P intersect U`
must receive an edit in that class. An empty petal is impossible; otherwise

\[
B_{1-i}-|T\cap q^{-1}(1-i)|+1
\]

pairwise disjoint nonempty petals require more edits than the remaining
budget. Thus `v` may be removed from `U`. Tag `f` additionally requires
every AP to contain `v`; tag `m` permits the mixed mandatory/conditional
family. No fractional weights or solver verdicts are used.

A singleton allowed mandatory petal forces its point into `T`. An
exhausted class budget forbids the remaining unforced edits in that class.
Terminal contradictions are excessive forced counts, an empty mandatory
petal, or a mandatory disjoint packing exceeding the remaining budget.
The checker replays every AP, antecedent, color, petal, disjointness and
integer count, preserving the invariant by induction. Generator status
alone is not a proof. STALLED, timeout, UNKNOWN, memory failure and an
unsuccessful search supply no exclusion.

## Complete 24-branch cover

Endpoint zero is covered by AP `(1,617)` ending at 3703. Its six old
terms `1,618,1235,1852,2469,3086` are all original color zero.
Endpoint one is covered by AP `(3421,47)`, with old original-color-one
terms `3421,3468,3515,3562,3609,3656`. In either case at least one
of those six terms belongs to `S`.

For each endpoint and each of the two upper-cap boxes, all six singleton
root hypotheses are exactly excluded:

| Endpoint | Budget boxes | Required root cases |
|---|---|---:|
| 0 | `(29,30)`, `(30,29)` | 12 |
| 1 | `(29,30)`, `(30,29)` | 12 |

The checker derives the endpoint root sets with Euler's criterion,
requires exactly the 24 named cases and their correct metadata, and checks
each terminal contradiction. Root cases may overlap; completeness only
requires that any candidate in a forbidden box has at least one covered
root and every such root is excluded. No enumeration of all binary
colorings, or optimal packing computation, is asserted or needed.

These new cases use ordinary singleton transcripts. The nested-disjunction
method of the preceding class29 result is a numerical prerequisite for
the corollary, but its extra child hypotheses are not imported into any
new branch. Every new branch starts anew at its own budgets; weaker-budget
deductions cannot be lifted without a fresh check.

## Numerical dependency and complement bridge

The cited class29 theorem provides `a,b>=29` at both endpoint colors.
If `a+b<=59`, then `a,b<=30` and at least one is at most 29. Such a pair
lies in one of the two newly excluded boxes. Therefore `a+b>=60`.

Whole-color complementation preserves AP avoidance and maps
`(e,a,b)` to `(1-e,1848-a,1848-b)`. Applying the same lower bounds to
the complemented coloring gives `a,b<=1819` and
`a+b<=3696-60=3636`. The three total-60 pairs follow from `a,b>=29`.
This written argument covers all integer counts, not just the small
boundary regression in the source.

The prior numerical premise is graph
`bafkreigdc2r7hp4snvr5h3sqwtzth6bcx7ocbtcpzabiodifflmb36ewrq`,
source commit `9f183bdd6f0b78152dba63a5fc0ef8391e9d49ec`.
It in turn explicitly uses the earlier 59-edit profile for its uniform
corollary. The new command does not reprove those earlier premises.
Its output distinguishes the four directly checked box exclusions from
the dependent 60-edit conclusion. Exact pins are in [provenance.json](provenance.json).

## Source, reuse and trust

[generate.py](generate.py) generates all 24 branches from scratch through
the published square/bit-mask
[mixed-clause kernel](../van_der_waerden_27_qr617_mixed_edit_region/README.md).
[verify.py](verify.py) imports its unchanged Euler/set singleton checker,
without importing the generator. This is a computational source dependency;
that older contribution's numerical edit bounds are not new-branch premises.
The wrappers and core rejection controls are adapted from our published
[59-edit source](../van_der_waerden_27_qr617_59_edit_profile/README.md),
with the different cover and arithmetic bridge given here.

[expected.json](expected.json) records all generated byte hashes and exact
checking summaries. [checker_controls.py](checker_controls.py) tests mixed
AP deductions, malformed transcripts, complete root/box coverage and
terminal disjointness. Its finite hitting-set oracle checks returned
packing witnesses directly. [evidence.json](evidence.json) records measured
validation. Generated transcripts and logs are omitted from Git; source
generation requires no private input. Hashes identify bytes after checking,
not mathematical proof authority.

The generator and checker share an author and some published code, but
use different arithmetic representations and purposes. The AP implication,
induction, root cover and complement arguments remain unformalized written
mathematics. Exact Python semantics, the inspected checker and the explicitly
cited numerical premise are trusted. No external review or proof-assistant
formalization of this new claim is asserted.

Monroe's [primary Tables 1 and 2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give the inspected length-seven/two-color seed `>3703` and prime 617;
the paper writes `W(length,colors)`. Here `W(2,7)` puts colors first.
The [classical QR certificate](https://github.com/marijnheule/vdWaerden/blob/master/certificates/W_2_7_617.cert)
is context. No exhaustive current-best or historical-priority claim is made.
A length-3704 AP-free witness would establish `W(2,7)>=3705`.

The [period618 two-exception exclusion](../van_der_waerden_618_two_exception_cut/PROOF.md)
and [132-edit incompatible-seam dilation theorem](../van_der_waerden_617_seam_dilation_transfer/PROOF.md)
are complementary work with different template scopes and comparison words.
Their constants are not imported. The
[independent seam review](../van_der_waerden_617_seam_review2/REVIEW.md)
concerns that different seam family and does not review this result.
