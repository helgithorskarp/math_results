# Two preceding HIGH merges, with their root joined to original port 11

Actual author and executing agent: **six-sorting-1, researcher**, 2026-10-02.
Status: **completed scoped author proof with separate same-author finite
checks, normal and optimized Python**. Independent-person review and formalization
remain pending; none is claimed here.

Ports are 0..12. Standard `(a,b)`, a<b, writes the minimum at a.
Let P be the literal size26 prefix B23;L4 from the published
[one-prior fixture](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/one_prior_high_barrier/fixture.json):

```
B23=(0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
    (0,2),(3,6),(4,12),(5,7),(8,10),
    (0,8),(1,3),(2,5),(4,9),(6,11),(7,12),
    (0,1),(2,10),(4,8),(3,6),(9,11),(11,12).
L4=(3,4),(1,2),(1,3).
```

**Conditional lemma.** A standard sorting completion of P of total size at
most44 cannot have a singleton first strict ordinary HIGH pair-mass increase
preceded by exactly two equal HIGH binary merges, where the first merges
two of the initial cost6 ports and the second joins its cost7 root to the
original cost7 root at port11. Any number of preparations, arbitrary
interleaving, repeated gates and arbitrary suffix depth are allowed.

This removes the ten dependent two-merge routes. It does not remove the
fifteen disjoint-pair two-merge routes, the zero/three-prior-merge cases,
other LOW prefixes or unrestricted thirteen-input size44. The maintained
[table](https://bertdobbelaere.github.io/sorting_networks.html) still gives
44..45, checked2026-10-02.

## Original domains and normalization

Import S(11)>=35 from [Harder](https://arxiv.org/abs/2012.04400) and the
ordinary/semantic pruning interface of lemma8539. The published9590 base
establishes P's held ranks and complete original pair inventories. The
current independent scalar base additionally reconstructs all8192 full
Boolean inputs and all39 tight original LOW cubes,2048 assignments each.
They have sorted LOW marks at0/1, D9/R0. An extra marked touch or an extra
whole-cube free identity would force total size at least10+35=45.
Consequently every prospective suffix avoids0/1; every remaining gate
must be active on each of these entire original cubes.

HIGH has five cost6 secondary ports5/6/7/9/10 and a cost7 port11; its held
maximum is12. Its mass448 has the ceiling512 at size44. Touching12
already overshoots. A singleton doubles its class weight, and a binary
merge of costs d/e replaces the two weights by2^(1+max(d,e)). Only an
equal merge preserves mass. The ten routes in the lemma are

```
g1=(a,b), g2=(b,11),  a<b in {5,6,7,9,10}.
```

Before the first strict event the HIGH support only shrinks. Every earlier
preparation avoids both endpoints of a later binary event, since those
endpoints are still live. Commute g1/g2 to immediately after P, retaining
all preparations in their original mutual order. Disjoint gates preserve
the entire function on every ordered input. Their dependency order remains
g1 before g2. The resulting prefix is P;g1;g2;F;s, with F an arbitrary
standard word on the six dead ports:2/3/4/8/a/b. Its full six-output Boolean
function determines its min/max lattice function on any totally ordered
values by thresholding. F's free singleton operand is not moved past F.

## Complete preparation functions

A breadth-first closure stores all64 Boolean rows of each complete
six-output function. A next gate is admissible only if it is active on
every original tight LOW cube after P;g1;g2;F. This predicate depends on
the whole function and the fixed original images. A function with a tight
original minimum at physical2 but a wrong global third statistic is an
absorbing impossibility by the published minimum-lock lemma9525: an
arbitrary future first touch of2 is a conditional identity, while any
touch of0/1 adds a marked deletion. Thus a fixed sorting schedule cannot
repair that wrong statistic within44 comparators.

For the ten routes the complete closure counts are

```
418,880,108,376,1314,670,264,646,270,98; total5044.
```

There are2327 absorbing minimum locks and2717 retained functions. The
independent scalar checker enumerates the complete function sets without
a word-length cutoff and matches all transitions, shortest representatives,
every representative's original-cube activity and every lock's full-input
witness. The maximum shortest length in this subfamily is eight. All
queues empty before the unchanged operational guards. Replacing F by its
shortest full-function representative cannot increase total size and
preserves every suffix's behavior. Arbitrary preparation lengths are
therefore covered; operational time/state limits are not proof premises.

After g1/g2 the live costs are6/6/6/8. Only a cost6 singleton fits the
remaining slack64. It has one of three live operands and one of six dead
operands, hence18 heads per retained F. It produces6/6/7/8 at mass512.
All later HIGH events must be equal binary merges. Exactly three are
forced: the two6 roots merge to7, the two7 roots merge to8, then the two8
roots merge to9 at11. Preparations preceding a future event avoid its
live endpoints, so these three events commute forward after s, retaining
the preparations' mutual order. Independent bottom-up event enumeration
checks every legal order and its entire16-row four-output function.

## Original-domain cuts and complete fronts

All48906 heads are accounted for.21189 are identities on a specified
whole original tight LOW cube. The27717 remaining heads have their unique
three-event tail.1539 tail prefixes have an original tight free-pivot cut
and a wrong full-input rank witness. The general induction is credited to
six-sorting-2's actual lemma9616, source3467d5cb5699e0cf55a74c74dbabacc3dac9262f,
[proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/one-sided-forest-frontier/PROOF.md).
Only that general induction is used; none of its native37 exclusions is
transferred.

For completeness, suppose a free physical port p on one original D9/R0
cube is at least every free value at a smaller port and at most every free
value at a larger port. Comparisons avoiding p preserve these inequalities:
comparisons on either side combine two values on that side, while a gate
crossing p is already ordered. A first future touch of p is then a
whole-original-cube identity, forcing45. The fixed suffix schedule cannot
touch p, so it cannot repair a wrong global rank at p. Marked0/1 are
already forbidden. This proves the obstruction for arbitrary preparations.
The actual cube functions and literal full-input witness are replayed,
with physical12 retained when checking the free inequalities.

The26178 remaining full fronts have literal length32+length(F) and complete
nine-wire images on physical2..10. All original held ranks0/1/11/12 are
correct; LOW and HIGH pair masses are saturated, so the suffix avoids those
four ports. The complete157-state ten-core image of P faithfully factors
every original Boolean input. The independent front checker replays all
4109946 core inputs, all27717 tail orders/277170 event controls and every
original LOW witness, image, physical map and budget. Image sizes29..92
and remaining budgets4..12 are exact.

## Every remaining core has a certified obstruction

For3196 fronts, a published9590 nine-core image A is contained in the new
image B and the new budget b_B is at most the old impossible budget b_A.
A standard nine-wire word sorting B within b_B would sort A within b_A,
contradicting9590. Both physical maps are2..10, and all four held ranks
are checked. The old full vectors are bound to published certificate
SHA8e18f17dbd27d7b0943a4c98170c039ea8521ad176c40031e80e5f9db96fb366.
An independent set-based check additionally replays1888 selected old and
3196 new literal images on798188 scalar core inputs and checks the budget
direction. The published negative theorem is imported rather than
re-established or called new.

The other22982 fronts use selected immutable original3LOW/3HIGH domains,
with all seven free Boolean variables. For each domain f delete marked
touches D_f and full-cube free identities R_f, tracking free carriers and
keeping reversed oriented pairs. Let Q_f be its retained seven-wire word.
Use the generic nested theorem9007 with

```
lambda_f = D_f+R_f+B7(Q_f),
lambda_z = max(lambda_f over selected originals with current tag pair z),
M = sum_z 2^lambda_z <=2^m for every sorting extension of total size m.
```

The selected current classes are disjoint. For22975 fronts take the
constant B7=16.47748 selected domain occurrences are independently
replayed on6111744 outer assignments, with221166976 gate evaluations,
and the complete retained carrier function is checked on another6111744
assignments. Every selected mass is greater than2^44; the minimum is
17729624997888=(129/128)*2^44. All bounded disjoint slices cover their
entire residual case list exactly, with no incomplete slice.

For the final seven fronts,26 selected occurrences use nine constant16,
fourteen anchor17 and three anchor18 bounds. Both semantic anchors are
the published8604 invariant, monotone lower bounds, combined by1+max heap
merges. Their full original five inner families are independently
recomputed;57344 inner assignments/412160 gate evaluations, plus3328
outer assignments and all carrier functions. The minimum selected mass
is18691697672192=(17/16)*2^44. These seven also require at least45.

Every numerical premise above agrees in normal and optimized Python.
All26178 full fronts are therefore excluded, and the complete preparation,
singleton and tail reduction proves the stated conditional lemma.

## Reproduction and evidence boundary

The ordinary threshold, commutation, pruning, free-cut and nested arguments
are written but unformalized. Numeric primitives are pinned to the published
9590 package and credited9420/9285/9127 ancestors. Known S11>=35,S7>=16,
S6>=12,S5>=9 are imported; their large proof corpora are not replayed.
Algorithmic independence is from separate same-author representations and
reconstructions, not a reviewer verdict. No resource failure, UNKNOWN,
timeout or incomplete enumeration is treated as a negative result.

The compact [certificate](certificate.json) records exact finite hashes.
Run `python3 run.py` from this directory to regenerate all needed arrays
and run every scalar checker normally and with Python optimization. The
[README](README.md) explains the serial stages and trust boundary. All large
arrays stay in ignored `work/` and `prior/work/`; they are not published.
The byte-pinned `prior/` source reconstructs the old kernel vectors for
inclusion checking without rerunning or claiming to reprove the published
9590 negative theorem. Source provenance is in [SOURCE-CREDITS.md](SOURCE-CREDITS.md).

The fifteen disjoint-pair two-prior routes remain a separate necessary
frontier: their preparation functions have been checked, but singleton/
tail intake has not yet been completed. The unrestricted44..45 problem
and other earlier HIGH-event cases remain open.
