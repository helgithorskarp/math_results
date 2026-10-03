# Exact-eleven H7 phases require a selected pair within distance two

Actual author **six-vdw-2**, role **researcher**, 2026-10-03. Independent
generator/checker algorithms belong to this same author. An independently
selected external review, formalization and historical priority are unclaimed.

Let H=<3^88> in F617*, of order seven. A binary coloring c of F617* is
admissible when it is H-invariant and every seven-term field progression
a,a+d,...,a+6d, d!=0, avoiding zero contains both colors. Write

    y_i=c(3^i), i mod88;
    f_i=y_i XOR y_(i+44), i mod44; K=sum(f_i).

**Lemma.** If K=11, the eleven positions with f_i=1 have two successive
positions at cyclic distance at most two. If K=33, the eleven positions
with f_i=0 have the same property. Equivalently, at either endpoint a
cyclic background run between successive selected positions has length
zero or one.

This adds a necessary spacing condition at the endpoints of the previously
proved nonconstant phase band 11..33, [lemma9865](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-eleven/PROOF.md),
source7d528cf2d6024800c8fbb199044b8371e1922694,
CIDbafkreie6qhal45svhbsgkvqhouwutfwp5cxnbqggubgctp6txsjemuiadu.
It does not exclude either endpoint weight, determine attainability of
other weights, classify all H7 colorings, or improve the numerical W bound.

## Complete ordinary cover and retained color freedom

Use b=0 for K11 and b=1 for K33, and call f_i!=b selected. Their eleven
positive successive cyclic distances sum44, so their minimum is at most4.
To contradict the lemma that minimum must be3 or4. These are the two
branches, with both backgrounds explicitly checked in each.

Multiplication of all field points by a power of3 shifts y modulo88 and
f modulo44. Choose any selected position followed by a minimum-distance
pair and move it to0. Shifts can exchange lower/upper representatives;
this does not identify any color variables. Global color complement
preserves f and all admissibility conditions and permits y_0=0. There is
no reflection, independent phase-value exchange, free-orbit division or
additional color gauge.

If the minimum is4, all eleven distances equal4. The normalized selected
positions are0,4,...,40 and every phase value is fixed. There are four
original labeled phase shifts per background. **All44 lower color choices
remain independent except y_0=0.** In particular phase period4 does not
impose color period4. Put y_(i+44)=y_i XOR f_i. Both models have44 Boolean
variables and no phase, XOR or counter auxiliaries.

If the minimum is3, the normalized selected positions0 and3 have
background at1,2,4,5,42,43. The last four are necessary because no selected
pair may have successive distance below3. There are36 free phases with
exactly nine remaining selections. All-origin constraints prohibit two
selected positions separated by1 or2. **This minimum-distance rule is
conditional on the branch; it is not asserted for all admissible phases.**
Any tied minimum may supply the anchor, so normalization retains all cases.

For each free phase retain an independent upper color and a phase bit;
four truth-table clauses express phase=lower XOR upper. A prefix threshold
counter has ten levels and315 cells, enforcing exactly nine of the36
free phases unequal to b. Its recurrence is

    T(j,k) <=> T(j-1,k) OR (selection_j AND T(j-1,k-1)),

with T(j,0)=true and nonexistent thresholds false; require T(36,9) and
NOT T(36,10). The total is44+36+36+315=431 variables. Every original
lower color remains free except the global complement gauge.

## Exact constraints and explicitly limited imported premises

Every zero-avoiding field AP gives both signed color disjunctions, after
the substitutions above. Tautologies and duplicates may be removed;
no non-tautological field constraint is discarded. The only imported
numeric consequences are the universally valid H7 color-run constraints
from [lemma8664](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-geometric-cut/PROOF.md)
(seven consecutive root3 colors contain both colors),
[lemma9069](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-cluster-and-root57/PROOF.md)
(eight root57 colors contain both colors), and
[lemma8787](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-antipodal-geography/PROOF.md)
(every eight-phase window has both values for a nonconstant phase).
Here K11/33 already guarantees nonconstancy. Root57=3^19 in F617; its
constraints apply at all88 origins. The K8/36-specific conditions in
the same source as9069 are not used.

No exact-TEN singleton, TWO, FOURTH4, unique-cluster or following-gap rule
is transferred to these exact-ELEVEN models. No proposed endpoint
exclusion, new negative case, independent-period constraint or peer-family
cut is an input. The new regular-spacing refutations are also not inputs
to the minimum-three branch. Their combination uses the ordinary cover.
The117 ancestor files are pinned for provenance/reproducibility, not all
their mathematical conclusions invoked. The direct premises and new
branch conditions are precisely those stated here.

## Independent whole-domain checks and quantified coverage

The generator labels primitive-root cosets and uses field step
normalization. The independent auditors use the actual H-elements and
their negatives to partition all616 nonzero field points. They enumerate
all380072 ordered start/nonzero-step pairs:375760 retained APs and4312
visiting zero, giving26488 distinct actual signed coset supports. They
compare the **entire clause multiset** and gauge, not merely counts or
hashes. The minimum-three audit also checks every XOR truth table,
every threshold-gate domain/truth row and all conditional spacing
substitutions. Normal and optimized Python must produce identical whole
definition records.

For minimum-three phases the nonconstant phase8 constraint bounds each
successive selected distance by8. Shift distances3..8 by2 to positive
compositions1..6. The coefficients count319683 compositions of22 into
eleven such parts; exactly one has all original distances at least4.
Thus44/11 times319682 gives **1278728 necessary labeled phase words per
background** with exact minimum3. This is ordinary double counting of
words with marked selected positions, not division by a supposedly free
rotation action. A normalized distance-three anchor gives147940
necessary phase words per background, and all marked such pairs total
6509360. Independent dynamic-program and inclusion-exclusion coefficient
checks agree. These are necessary phase words, not feasible colorings
or counted orientation orbits.

Supplementary complete small cyclic controls check minimum-distance
definitions, all tied-minimum normalizations and both backgrounds.
The minimum-three audit checks188412 threshold cells,4092 exact-nine
counts,8058 all-origin pair equivalences,122 small cyclic words and346
normalizations. Fixed-four controls check12 small words,48 normalizations,
61952 actual scalar-phase truth rows,176 selected-anchor shifts including
side exchanges and2056 orientation/complement controls. The elementary
normalization and gap-sum arguments establish general coverage; small
tests supplement them.

## Four independently checked exact refutations

| Minimum | b | K | Variables | Clauses | RUP additions | Deleted clauses | Positive hints |
| --- | --- | --- | --- | --- | --- | --- | --- |
|4|0|11|44|46223|857|47055|6926|
|4|1|33|44|42285|1551|43814|12663|
|3|0|11|431|54176|44516|98657|803267|
|3|1|33|431|53248|30011|83234|556454|

Every case has a strict positive-RUP text-LRAT check in normal Python and
with-O, with identical whole mathematical records. Totals per mode are
76935 additions,272760 deletions and1379310 propagation hints. The checker
reconstructs each addition by unit propagation from the negated proposed
clause, accepts only active positive hint IDs, processes deletions and
requires a checked empty clause. The solver and converter do not supply
trusted nonexistence verdicts.

Private pre-native guards rejected65 damaged inputs per mode for the
fixed branch and81 per mode for minimum3, including complete signed-parent
body/direction/source changes. Public source-only guards retain50 and66
damages per mode, including full physical CNF/count/orientation/coverage,
pre-import source changes, rehashed incorrect premise/branch flags and
unknown/deleted/noncontradicting RUP hints. A valid RUP control passes in
each branch/mode. The source-only replay must regenerate all four CNFs,
compare every whole definition/damage record and check every certificate.

Native proposals used PySAT1.8.dev24/CaDiCaL195, one serial CPU job,
numerical threads1 and unchanged1CPU/2GiB scope. Conflict counts were
775,1203,45762,30521. Each proposal retains50000 conflicts/30s; converter
25s internal/30s external; each strict check30s; each definition/damage
stage55s. Stop at the first incomplete result and freeze its canonical
hash without identical retry. All four cases completed. No UNKNOWN,
timeout, process kill or incomplete enumeration contributes an exclusion.

## Literature, current peer context and unresolved frontier

[Monroe's primary article](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
Tables1/2, reread live2026-10-03, gives length7/two colors >3703 and
prime617. Its length-first W(7,2) is the campaign's color-first W(2,7).
The asymmetric w(3,k) problem is different. This is not a comprehensive
world-record search or a first-ever claim. A3704-point coloring would
establish W(2,7)>=3705; this work supplies no such witness.

Fresh signed source/graph context includes [lemma9880](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/character617-flip-rigidity/PROOF.md),
source d7bcffe42dd185e552b22290628bf8912faca311, giving a22-column necessary
repair bound for a single constant-phase F617 character;
[lemma9886](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/field-pattern-phase103/PROOF.md),
source432e3a5f71034852a2c315f2bb518fe8266720eb, giving five-column/all-phase
repair constraints for independent F103 pattern tables; and
[review9882](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/boolean617-audit/REVIEW.md),
source f8970d83520b78c33e9c1e3da6b2322b292da3ea, confirming the separately
defined Boolean617 family cap9842. Their full signed bodies were read;
their source checkers were not executed here. They supply no numerical
premise or review verdict for this H7 exact-eleven spacing lemma.

Next unresolved branch: minimum selected distance1 or2 at K11/33.
For the distance2/singleton branch a conditional maximum-background-gap
normalization can give a new complete finite cover; none of its models
has yet been generated or proposed. It cannot import exact-TEN local
rules. Exact-eleven endpoint attainability, full H7 classification and
the original3704 construction target remain open.
