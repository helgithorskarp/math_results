# Complete repeated-effective-(1,3) B11 branch excluded

Author and executing agent: **six-sorting-1, researcher**, 2026-10-01.
The shared signing identity does not identify the individual author.
This is a written, unformalized computer-assisted intermediate lemma.
Separate algorithms and certificate checks are not external-person review.

**Result.** No ordinary sorter of the specified B11 image with at most
22 comparators has an effective-event multiset containing (1,3) twice.
The complete six classes below, all 32,310 effective orders, every permitted
physical profile-loop interleaving and arbitrary allowable depth are covered.
Physical comparator repetitions in other effective classes remain allowed.
The result does not settle B11 C22 or the global thirteen-input problem.

Indices are zero based in the original 480-class certificate of
[graph7936](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_extreme_multiset_quotient/PROOF.md),
source `bc1675c66ddeb936edbf38d09395420be06f551a`.
The programs select the entire group entrywise from that pinned table.

| Index | Exact decimal class code | Effective orders |
|---:|---|---:|
| 36 | 349871875148074941166444351586309 | 5385 |
| 42 | 349871875148075211365929319399429 | 5385 |
| 151 | 410718813816833244927284175962117 | 5385 |
| 157 | 410718813816833515126769143775237 | 5385 |
| 239 | 410718871845272586429484561858565 | 5385 |
| 245 | 410718871845272856628969529671685 | 5385 |

## Literal target and complete normalization

All ports are zero based. Comparator (a,b), a<b, sends its minimum to a.
Serialize any allowable parallel network without changing its function or
size. There is no parallel-depth restriction in this result.

The literal prefix G22 is P19;(10,12);(0,5);(0,1), given completely in
[fixture.json](fixture.json). Its image on original ports1..11 is exactly
B11, with 158 Boolean rows and canonical SHA256
`2b776a68a6bfc671df43af0f186dfe42acc0ae870738bdd88fa153948bedeaf4`.
B11 port i means original i+1. The known 23-comparator B11 control lifts
to a sorter of size45, checked on all8192 original Boolean inputs.

Import **six-sorting-2**'s complete literal P19 reduction
[graph7885](https://github.com/helgithorskarp/math_results/blob/main/sorting13_P19_binary_minimum_reduction/PROOF.md),
source `ca993bc042ba81442a4afccb0d374d142696d0e7`: a full size44 sorter
beginning with literal P19 exists if and only if this exact B11 image has
a sorter with at most22 comparisons. All normalized minimum branches and
arbitrary depth are covered. Other thirteen-input prefixes remain outside
that reduction.

The necessary coupled marked-pair profiles are imported from
[graph7871](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_joint_extrema_normal_form/PROOF.md).
Their reduced initial vectors are

```
low  = (4,2,2,2,2,0,2,0,0,0,1)
high = (0,0,0,0,0,4,0,2,4,4,1).
```

At (a,b), low weights become (2max(low[a],low[b]),0), and high weights
become (0,2max(high[a],high[b])). Both sums stay at most16. The first
touch of B11 port10 cannot have partner0,7,9. Terminal low16 is on0 and
high16 on10. A physical comparator is an **effective event** when it
changes these necessary profiles or their first10 flag. Other comparators
remain permitted physical loops.

The universal one-preparation-block theorem
[graph8126](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_single_preparation_normal_form/PROOF.md),
source `9e233924e79cc8a4b52001cda87cc8f56db3003c`, puts every eleven-event
word, on arbitrary ordered inputs, in the form

```
E_minus ; A ; f ; E_plus ; T.
```

Here f is the unique unary refill at the first port10 event. The pre-f
empty set J has at most4 literal ports; pre-f loops commute past later
pre-f events into A on J, and post-f loops commute past later post-f events
into T on B11 ports1..9. No loop is commuted across f, and overlapping
loops keep their order. Full comparator functions on j=1,2,3,4 ports have
1,2,11,261 elements and maximum shortest lengths0,1,3,5. Replace A by a
shortest full-function representative of length h, preserving its function
on all ordered inputs and never increasing its length. There are11 effective
events, so T has budget11-h. These all-real commutation and function-equality
bridges are imported written theorems; the finite monoids are also checked
here by Boolean functions versus distinct-rank permutation functions.

For each exact quota, the producer enumerates all5385 effective orders
using reduced forward profiles. The checker independently enumerates the
same orders using original thirteen-wire marked-pair inverse fibers.
Only disjoint comparisons within each E phase are exchanged. Their overlap
partial orders give exactly6 canonical phase triples per class. Trying every
shortest local function on each literal J gives288 normalized prefixes per
class. No wire permutation is used. Every original effective order and
allowed loop placement is covered by the imported normalization.

After a normalized prefix, B11 ports0,10 hold its extremes; original
ports0,1,11,12 hold the first two and last two original order statistics.
Nine-wire tail port i means B11 i+1 and original i+2. Two representative
prefixes with the same literal nine-image and budget pose exactly the same
tail-existence question. Any such tail sorts either representative's image
and lifts to a full sorter of at most44. A representative's original marked
routes need not coincide with the routes of another equivalent prefix.

## Prefix activity and fixed-boundary exclusions

Import established S(11)=35 from
[Harder](https://arxiv.org/abs/2012.04400v3), and the marked-pruning/activity
mechanism of **six-sorting-2**,
[graph7944](https://github.com/helgithorskarp/math_results/blob/main/sorting13_B11_pruning_saturation_activity/PROOF.md).
The fixture's12 families and13 marked-pair domains are reconstructed from
all26624 actual distinct-minimum/maximum and free-Boolean assignments.
On every normalized prefix, each selected original pair touches exactly9
comparisons and ends on the held minimum or maximum ports. The tail cannot
touch either selected mark.

Suppose a tail sorted a representative image. Lift and pad the full sorter
to44. Prune comparisons touching the marked pair and untangle: exactly35
comparisons remain on11 free inputs. If a retained prefix comparison never
swapped any free Boolean assignment, deleting it would give a sorter of
size34, contradicting S(11)=35. The stored activity obstruction therefore
excludes its entire image/budget pair. The producer tests bit-plane domains;
the checker replays scalar domains and all2048 actual marked/free assignments
at each recorded obstruction, confirming both operands are free and ordered.

| Class | Prefixes | Literal images | Image/budget pairs | Activity exclusions | Pairs left |
|---:|---:|---:|---:|---:|---:|
| 36 | 288 | 89 | 120 | 120 | 0 |
| 42 | 288 | 30 | 71 | 60 | 11 |
| 151 | 288 | 36 | 81 | 81 | 0 |
| 157 | 288 | 20 | 59 | 56 | 3 |
| 239 | 288 | 69 | 109 | 109 | 0 |
| 245 | 288 | 18 | 47 | 42 | 5 |

Thus468 of487 pairs are excluded. Of the remaining19, sixteen have
fixed-boundary contradictions, whose exact controls and original preimages
are in [reduction.json](reduction.json). The first-two-port minimum cut is
attributed to [graph8198](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_class13_boundary_obstruction/PROOF.md);
the maximum dual and the source algorithms follow this researcher's prior
[graph8281](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_repeated23_reduction/PROOF.md).

For clarity, the fixed-cut argument is as follows. Mark four original values
as distinct minima or maxima, leaving9 free inputs. Established S(9)=25
from [Codish, Cruz-Filipe, Frank and Schneider-Kamp](https://imada.sdu.dk/u/lcf/pubs/paper26.pdf)
and generalized-network untangling bound the full marked-touch count by19.
Choose a control whose middle marks are exactly K={0,1} for minima or K={7,8}
for maxima. This sorted marker row is fixed under every ordinary tail
comparison. If D0 touches were spent, the tail has at most19-D0 comparisons
incident with K. Another row requiring r further marks in K forces at least
r crossing comparisons. Row509 for minima or128 for maxima additionally
forces the internal (0,1) or(7,8): every other ordinary comparator fixes that
singleton marker row before the indicated comparison appears. Internal and
crossing occurrences are distinct. In every recorded case r+1 exceeds19-D0.

| Class | Images and budgets excluded by fixed cuts | Number |
|---:|---|---:|
| 42 | 1/10,5/10,6/10,12/9,13/9,14/9,15/9,16/9,17/9,27/8 | 10 |
| 157 | 0/11,1/10,9/9 | 3 |
| 245 | 1/10,10/9,11/9 | 3 |

All sixteen controls have nine free inputs and are checked on every512
free Boolean assignments. Their exact D0, r, original control and cut
preimages are independently verified. This closes classes36,151,157,239.
The other two classes reduce, in both directions, to exactly these tails:

| Class | Local image | Rows | Budget | Prefix case |
|---:|---:|---:|---:|---:|
| 42 | 0 | 54 | 11 | 0 |
| 245 | 0 | 51 | 11 | 0 |
| 245 | 5 | 46 | 10 | 20 |

Their complete literal sets, row hashes and B11 prefixes are in
[tail_fixture.json](tail_fixture.json). Local image IDs are class-local.

## Moving-marker proof for class245/image5

The34-comparator lifted prefix sends maximum-marker mask184, marking
original3,4,5,7, to middle row272, whose ones are on4,8. It spends18
marked touches. Pruning against S(9)=25 leaves a tail touch cap of1.
There are two middle marks, one initially in K={7,8}. Their number in K
never decreases under ordinary comparisons; sorting requires it to grow
from1 to2, so some crossing comparison increases it and touches a mark.

The literal image contains singleton row128, forcing (7,8) as above.
Whenever this internal gate occurs, the chosen moving control still has
at least one mark in K, so it also touches a mark. The crossing and internal
occurrences are different. At least2 touches are required, contradicting
the cap1. The control need not be fixed or already sorted. This argument
allows every gate order and physical repetition. The moving-cut mechanism
is attributed to this researcher's [graph8340](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_repeated23_exclusion/PROOF.md).

## Complete capped serial certificates for the two other tails

For each original nonconstant Boolean marker mask x and polarity p, simulate
its actual lifted prefix and count every comparison touching at least one
marked value; count a comparison touching two marks once. There are M free
original inputs, and D0 prefix touches. Removing touched comparisons from a
hypothetical full44 sorter gives a generalized M-input sorter. Untangling
and the established smaller-size bound S(M) imply the necessary tail cap

```
D_tail <= 44 - S(M) - D0.
```

Polarity0 encodes fixed distinct minima; polarity1 fixed distinct maxima.
Marker membership and touch counts depend only on Boolean comparisons,
independently of the free values. The zero-one principle licenses this
all-ordered-input pruning once the complete image tail sorts. Bounds through
12 are the known values0,0,1,3,5,9,12,16,19,25,29,35,39. They are imported,
with no new theorem claimed about them. Pool the smallest cap per literal
middle marker row/polarity, preserving its actual original witness.
The scalar checker reconstructs every pool from all8192 original inputs
and checks relevant witness trajectories with distinct marks on every free
Boolean assignment. All302 pooled caps over the three tails are compared.

The two complete CNFs permit every one of36 ordinary nine-wire pairs at
all11 serial positions, including arbitrary repeated comparisons. Variables
choose exactly one pair per position, describe all Boolean row values and
indicate whether each endpoint is used. Selected outputs are AND/OR;
unused endpoints stay unchanged. Initial rows and their sorted final rows
are fixed. Each touch flag is equivalent to the selected pair having an
incoming bit of its marked polarity. Cardinality clauses bound each actual
pooled touch sum. There are **no activity, symmetry, permutation, suffix
component, disjoint normalization or parallel-depth clauses**.

These are necessary conditions for every candidate. A shorter tail can be
padded after its already sorted output; the resulting full44 sorter still
satisfies the44-based pruning bounds. Consequently exact11-slot formulas
cover all tail sizes at most11 and every allowable parallel depth. Boolean
sorters admit auxiliary assignments for all specified row recurrences,
choice gadgets and actual touch caps; no omitted symmetry assumption is
needed. Infeasibility of either complete necessary encoding excludes that
tail, rather than just one layering.

| Class/image | Variables | Clauses | Input core clauses | Compact RUP additions |
|---|---:|---:|---:|---:|
| 42/0 | 9671 | 249217 | 1349 | 475 |
| 245/0 | 9218 | 237682 | 1413 | 613 |

The native full DRAT proofs were actually checked, with zero RAT lemmas.
Compact input cores are checked for membership in the full CNFs, and their
RUP traces are replayed by a solver-free watched-literal checker. Deletion
lines were removed, followed by native RUP-only and Python replay checks.
Every actual non-cardinality clause and canonical variable allocation is
independently reconstructed. Cardinality auxiliaries are isolated and
extension existence is checked by exact Horn propagation for all relevant
flag assignments: exactly-one36 flags checks0/singletons/pairs and proves
larger-set rejection by negative-flag monotonicity; at-most11 flags checks
all2048 assignments per distinct shape. The audit covers486899 clauses,
193 cardinality blocks and21147 relevant flag assignments.

Four core/proof files total81222 bytes, with1088 RUP additions and no
published deletion/RAT steps. Large regenerated CNFs, metadata and raw
native traces stay outside the source repository. [certificate.json](certificate.json)
records exact hashes. Merely obtaining native UNSAT was not a premise.

## Reproduction, attribution and remaining frontier

Run the complete sequence in [README.md](README.md). The reduction checker
uses original13 inverse fibers, distinct-rank monoids and scalar marked
assignments; it imports neither producer nor solver. It checks1728 prefixes,
273024 B11 row simulations,958464 actual activity-obstruction assignments,
155648 original literal-prefix inputs and8192 fixed-boundary free assignments.
The tail checker additionally checks24576 original inputs,474 B11 rows,
48128 distinct-marker/free assignments,36864 moving-cut truth cases and72
mandatory-gate cases. Tiny RUP/gadget controls cover4608/72 cases.

Two forced insertion controls lift to size69, sort all8192 original inputs
and satisfy the actual encoding with the appropriately relaxed touch caps.
Four malformed certificates are rejected: omitted tail, wrong cap with an
updated digest, invalid exactly-one gadget with updated digests and an
unproved empty RUP step. Native checking and relevant stages retain45-second
bounds. One solver/numerical thread and one intensive local job were used;
no resource cap was increased. Timeouts, UNKNOWN, resource termination or
incomplete checking are not mathematical nonexistence.

The reduction cores adapt this author's published8126/8281 source. The
comparator/touch encoding, audits and moving cut adapt this author's8340
source, `6523ab50f85f743bbac0937228e30be238521d47`.
The Horn extension routine is credited to **six-sorting-2**,
[graph8222's audit](https://github.com/helgithorskarp/math_results/blob/main/sorting13_B11_additional_ten_event_exclusions/audit_encoding.py),
source `9d6ec9a6ba29103c9de43d716823e25b132d4b1c`.
The solver-free RUP code is this author's prior
[graph7452 implementation](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_nullary_minimum_exclusion/watched_rup.py),
source `5ad75ecb80164da04c921f1898cf62334668a027`.
No priority claim is made for these methods, pruning, cuts or the known bounds.
The scoped addition is this complete six-class exclusion. The written
normalization, pruning/untangling and zero-one bridges remain unformalized.

[frontier.py](frontier.py) checks exact cumulative incidence using the pinned
480-class table, importing **six-sorting-2**'s whole ten-event exclusion
[graph8321](https://github.com/helgithorskarp/math_results/blob/main/sorting13_B11_ten_event_branch_exclusion/PROOF.md),
source `a3888f3045192c326564035fc01e2309ba1cdd63`, this author's complete
repeated23 exclusion8340, repeated01 exclusion
[8070](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_repeated01_activity_exclusion/PROOF.md),
and class13 exclusion8198. Those previously checked proofs are imported,
rather than rerun by the frontier script. These six new disjoint classes
reduce the8340 frontier320 to **314=297 eleven-distinct+17 eleven-repeated**,
with2153985 effective orders and canonical remaining-table SHA256
`9c943710d68fd6100c90618ccac6928b15653395d17448476bc878946c0e402b`.

Global S(13) remains44..45 in the
[maintained table](https://bertdobbelaere.github.io/sorting_networks.html),
checked live2026-10-01; B11 remains22..23. Other full13 prefixes remain
uncovered. No44-comparator construction, full B11 exclusion, external
review verdict or proof-assistant formalization is asserted.
