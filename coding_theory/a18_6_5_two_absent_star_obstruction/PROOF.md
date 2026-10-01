# Two absent neighbors and one saturated absent point force replication at most fourteen

Author: **six-code-3, researcher**, 2026-10-01.

## Statements and exact scope

For a family `F` of distinct five-subsets of a fixed eighteen-point set `V`,
assume any two members intersect in at most two points. Write
`r_p = #{W in F:p in W}` and `lambda_pq = #{W in F:p,q in W}`.
A shortened star at `y` consists of the quadruples `W\{y}` for words
through `y`. It is a pair packing: no pair occurs twice.

**Canonical local lemma.** Label `V={0,...,17}`, `x=14`, `y=17`.
Let `Q` be the twenty literal quadruples in [input.json](input.json).
Suppose the words through `y` are exactly `{y} union q`, for `q in Q`.
For any distinct `a,b` with `lambda_xa=lambda_xb=0`, if `r_a=20`,
then `r_x<=14`. No total-size or other replication hypothesis is imposed.

**Generic local consequence.** The same conclusion holds when the
shortened star at `y` has replication multiset `(4^5,5^12)`, the leave
induced on its five replication-four points has four edges, and `x`
is a marked isolated vertex of that induced leave. This consequence uses
the complete marked classification8350, source
**43dc0a95a2232b6b9ff1e85d18a1a34fe5705bbc**, independently confirmed
by six-reviewer-5 in review8401, source
**b45ab435bac5ce32ee8ef711bdc879497f3044b6**.
Its hypotheses include the isolated mark; this is a classification of
that specified subclass, not every unit star.

In particular, if `r_x=15` and `x` has two absent neighbors, neither can
have replication20. With the classical point cap20, both have replication
at most19. The point cap is used for this last inequality only, not for
the canonical bound `r_x<=14`.

Applying the reviewed one-unsaturated71 reduction8350 excludes its
`(n1,n2,n5)=(15,0,2)` cohort. This application is already covered by
six-code-1's [entire one-unsaturated71 exclusion](../../constant_weight_18_6_5_equality_structure/NO_SINGLE_UNSATURATED_71.md),
source **053622a2c8a24c2e83a6702e0d0648ede8031270**. The additional
result here is the local obstruction with arbitrary total size and
unrestricted other replications. The new lemma awaits independent review;
all written bridges remain unformalized. The global interval is69--71.

## From the hypotheses to three ordered models

Shorten at `x`. The two absences confine its quadruples to the fifteen
points `V\{x,a,b}`. At any of these points, incident quadruples have
disjoint three-point tails, so their number is at most `floor(14/3)=4`.
Consequently `4*r_x<=15*4`, or `r_x<=15`. To prove the lemma, it suffices
to exclude equality. Assume `r_x=15`. Its shortened star then has exactly
four occurrences at **every** one of its fifteen supporting points.

The template has four quadruples through `x`. Their other points are

```
{0,4,12}, {1,7,13}, {3,8,11}, {5,6,10}.
```

They give four common `x,y` words. The uncovered neighbors of `x` in `Q`
are exactly `N={2,9,15,16}`. An absent point must belong to `N`: a covered
pair `xa` in `Q` would already give a word through `x,y,a`. Neither absent
point can be `y`, since there are four common words.

For completeness the programs construct the full **actual** automorphism
group of `Q`, fixing `x`. In the producer, choose a high-cycle map and
map each low leave-neighbor cohort to its image cohort. There are
`8*4!*(2!)^4=3072` leave maps; retaining maps preserving the literal
twenty quadruples gives eight point maps. The checker uses point-by-point
incidence backtracking, preserving replication, pair and triple incidence,
then checking full quadruple images. Every true automorphism preserves
those invariants, so this second carrier is complete. It gives the same
eight maps in121 states.

Because the first absent point is the one assumed saturated, the choices
are **ordered** pairs `(a,b)` in `N`, not unordered sets. The twelve choices
have three disjoint orbits of four under these actual maps, represented by

```
(2,9), (2,15), (2,16).
```

All twelve choices are retained through this verified quotient. In
particular, the two unordered-pair orbits do not justify swapping `a,b`.
The relabelings fix the specified `y` star and apply to the entire family;
no automorphism of `F` or unproved transitivity is assumed.

## Complete two-star census

After the four common words, eleven `x` words remain. They avoid
`y,a,b`. Each is `{x} union R`, for a quadruple on the fourteen-point set
`V\{x,y,a,b}`. Test every such quadruple against all twenty fixed `y`
words for intersection at most two. There are exactly148 candidates in
each of the three normalized models. Two candidates can both occur
exactly when their quadruples intersect in at most one point.

The producer enumerates every11-clique in this148-vertex compatibility
graph using exact integer bitsets. Its greedy coloring partitions the
available graph into independent sets. At a reverse-order branch, the
color number bounds any clique among the still available vertices.
Each branch selects its vertex and restricts availability to its neighbors;
then that vertex is removed before the next branch. Thus each11-clique
is reached once, and the integer color bound only removes branches that
cannot attain eleven. No heuristic cutoff is used for a complete result.

The producer-free checker independently generates its candidates from
all `binom(18,5)=8568` literal five-subsets, using the same mathematical
intersection conditions. Every actual candidate tuple agrees. Its census
uses whole-point-star decomposition rather than graph coloring. Twelve
of the fourteen residual points have demand3, and two have demand4;
the total44 requires eleven new quadruples. At any state choose a point
with positive demand and enumerate its **entire remaining star** as an
increasing-index subset. Since all selected blocks contain that point,
their three-point tails must be pairwise disjoint. Remove the selected
blocks' pair incidences, subtract all point demands, and recurse.

Every completion has a uniquely determined full remaining star at the
chosen point. Increasing indices enumerate it once; the tail condition
is exactly its internal compatibility condition. The only rejection rules
are necessary: too few legal columns overall, too few columns at a point,
or fewer than three times its demand available tail points. Columns
colliding with already used pairs or touching a depleted point cannot be
in a completion. Induction on positive demands proves complete coverage
and absence of duplicate completions. The zero-demand leaf has exactly
eleven blocks. This method uses exact point/pair sets and no coloring.

| Ordered absent pair | Candidate graph edges | Complete11-cliques | Producer states | Independent whole-star states |
|---|---:|---:|---:|---:|
| `(2,9)` |7203|39|24959|6053|
| `(2,15)` |7269|51|24816|8046|
| `(2,16)` |7203|39|24483|6134|

Every **actual** solution fiber is compared entry for entry, using its
candidate-pool hash, not only these counts. Each completion restores a
literal31-word union with `r_y=20,r_x=15`; all weights, distinctness,
pairwise intersections, both absences and all fifteen `x` pair degrees4
are checked. The two-star completions are positive local fixtures, not
71-word constructions.

## Saturating the marked absent point gives an exact90-pair cover

In each of the129 complete seeds, let `a` be the first absent point,
normalized to2. Assume `r_a=20`. Since no word through `a` contains `x`,
its shortened star is twenty quadruples on the sixteen points `V\{a,x}`.
They cover120 distinct pairs, which equals `binom(16,2)`. Hence **every**
pair of those sixteen points must be covered exactly once. This is an
ordinary counting consequence; no classification of affine planes is used.

Exactly five existing seed words contain `a`. Their shortened quadruples
contain `y`, and their three-point tails partition the other fifteen points.
They cover all fifteen pairs with `y`, so the fifteen additional `a`
words must avoid `y`. Among the105 pairs of
`V\{x,y,a}`, the five tail triangles already cover15 pairs. Therefore
the additional quadruples must cover exactly the remaining90 pairs, once
each. Every point has residual pair degree12; an exact cover consequently
has four new occurrences per point and fifteen quadruples. Point quotas
are consequences here and are not trusted pruning rules.

There are405 quadruples using at most one point from each tail triple.
Keep every one whose five-word `{a} union R` intersects every word of
the31-word seed in at most two points. The producer constructs these
from all fifteen-point quadruples and explicit prefix-pair exclusion.
The checker reconstructs them from all eighteen-point five-subsets and
literal word intersections. The actual seed and candidate-pool hashes
are compared. Across the129 cases there are80--114 candidates per case.
Thus every possible completion of the saturated `a` star belongs to the
literal exact-cover instance audited below.

## The refutation certificate and its independent verification

A node of [certificate.json](certificate.json) is
`[pair_index, [[column_index, child], ...]]`. Its state is the set of
uncovered residual pairs. The designated pair must be in that set.
The branches must name exactly once **every** candidate quadruple
containing that pair whose six pairs are still uncovered. A child removes
those six pairs. An empty branch list is valid only when this complete
domain is empty. A state with no uncovered pair represents a positive
cover and is rejected as a refutation leaf.

Every exact cover at a node uses exactly one legal column containing
the designated pair. Complete branching therefore preserves every cover.
Induction on the number of uncovered pairs proves that a fully verified
tree with only empty-domain leaves certifies nonexistence. The checker
reconstructs every legal domain using literal pair sets; it does not
trust the producer's chosen pair, bitsets, coloring, quota calculations,
negative verdict, certificate counts or solver behavior.

| Ordered absent pair | Refuted cases | Candidate-count range | Certificate nodes | Largest tree |
|---|---:|---:|---:|---:|
| `(2,9)` |39|94--114|185|9|
| `(2,15)` |51|80--109|217|9|
| `(2,16)` |39|87--112|137|8|

All129 instances are negative. Their certificates contain539 nodes in
total and fit in38,041 bytes with the complete solution keys, actual
point maps, orbit lists and hashes. The certificate's SHA256 is
`74cfad4e86c907d5560d1f6311c3ab663915b5560d5adb7f6ec93191eaefbb64`.
The template's canonical-list SHA256 is
`fd7129751da4c53d9fbf4387d255d1075e9c30f118188849ed97d3567c801fcc`.
Serialization is sorted-key compact JSON with a final newline.

This excludes `r_x=15`, completing the canonical bound `r_x<=14`.
The ordered carrier covers either choice of a saturated absent point.
The marked classification supplies the generic consequence.

## Application, context and literature

The independently confirmed reduction8350 forces, for a71-word code
with exactly one unsaturated point `x`, `r_x=15`, every other replication20,
and exactly three possible counts of pair deficits1,2,5 at `x`:
`(9,8,0),(12,4,1),(15,0,2)`. In the third cohort two points never occur
with `x`; every one of the fifteen unit centers has the specified
isolated marked template. Choose any such center for `y` and either
absent point for `a`. The local bound contradicts `r_x=15`.

Six-code-1's [COMMON_UNIT](../../constant_weight_18_6_5_equality_structure/COMMON_UNIT.md)
and [NO_SINGLE_UNSATURATED_71](../../constant_weight_18_6_5_equality_structure/NO_SINGLE_UNSATURATED_71.md),
source053622a2c8a24c2e83a6702e0d0648ede8031270, give a complete author
proof excluding all three cohorts. Its premise concerns two saturated
unit stars sharing an isolated hub. The present canonical lemma concerns
one marked unit star, a replication-fifteen star and an absent saturated
star; only the latter has a complete sixteen-point pair cover.
Both sets of new coupling arguments await independent review. The
71 application here is a separate corroboration of the third cohort;
the generic bound applies with arbitrary family size and other replications.

The imported [marked classification](../a18_6_5_one_unsaturated_at_71/PROOF.md),
graph8350 `bafkreigsaibox67ch5nagmc6cm225eg7sxfqfvmlcuot75cbi55vvtvwhi`,
and its [independent review8401](../../constant_weight_marked_star_review5/REVIEW.md),
`bafkreihsysixlgro6wcblkekna3dovslmuqooytzxga6wcfqqm7ogfjaoe`,
are precise dependencies of the generic interpretation. The canonical
finite computation is self-contained. The71 equality reduction uses
the universal saturated-star theorem from [review8323](../../constant_weight_upper71_review1/REVIEW.md),
independently re-audited in [review8358](../../constant_weight_upper71_review5/REVIEW.md).

[Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf) proves the classical
point cap via `A(17,6,4)=20`. [Stanton and Street1987](https://combinatorialpress.com/jcmcc-articles/volume-001/some-achievable-defect-graphs-for-pair-packings-on-seventeen-points/),
JCMCC1,207--215, CaseVII(f), gives the positive local template. Their
[1988 follow-up](https://combinatorialpress.com/ars/vol26a/) has not been
fully assessed, so historical priority of the coupling obstruction remains
unassessed. The [maintained primary table](https://aeb.win.tue.nl/codes/Andw.html)
was checked live2026-10-01; it still lists69--72. The campaign upper71
has independent reviews8323/8334; it is not attributed to that table.
The established [69-word fixture](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
was exactly revalidated unchanged in this pass, SHA256
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
Reproducing that fixture is validation, not a new construction.

All cases finish within unchanged200000-state/ten-second guards. Sixteen
corruption/invalid-guard controls, five actual INCOMPLETE controls and
positive exact-cover/clique controls are described in [controls.py](controls.py).
The tests remain active under `-O`. Only source, the compact template,
the compact refutations and summary are published. Complete regenerated
search logs, private pilots and exploratory state are outside the source
package. Trust rests on the written reductions and recursion proofs,
CPython exact integer/set semantics and the explicitly credited imported
classification for the generic consequence. No proof assistant has checked
these bridges or this new coupling claim.

The35-word [positive coupling fixture](positive_seed.json) has this exact
`y` star, `r_a=20`, `r_x=4`, and all four leave neighbors of `x` absent
from its words. Its literal intersections and replications are checked
by the controls. Thus the local hypotheses have positive examples at
smaller hub replication; no sharpness or new global construction is asserted.
