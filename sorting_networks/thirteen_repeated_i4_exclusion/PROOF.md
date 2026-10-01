# Complete repeated-effective-(i,4) B11 exclusion, i=1,2,3

Author and executing agent: **six-sorting-1, researcher**, 2026-10-01.
The shared signing identity does not identify the individual author.
This is a written, unformalized computer-assisted intermediate lemma.
Separate algorithms and certificate checks are not an external-person review.

**Result.** No ordinary sorter of the specified 158-row B11 image with
at most22 comparisons has an effective-event multiset containing any of
(1,4), (2,4), (3,4) twice. The complete nine classes below, all48465
effective orders, every permitted physical profile-loop interleaving and
arbitrary allowable depth are covered. This is a scoped conditional
exclusion, and supplies no size44 construction or full B11 exclusion.

Indices are zero based in the pinned original480-class quotient of
[graph7936](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_extreme_multiset_quotient/PROOF.md),
source `bc1675c66ddeb936edbf38d09395420be06f551a`. The producer and checker
select the entire union entrywise by the three effective-gate multiplicities.
Physical comparisons, including loops, may repeat freely.

| Index | Exact decimal class code | Repeated effective pair | Effective orders |
|---:|---|---|---:|
| 80 | 349871875451413182682808425906181 | (1, 4) | 5385 |
| 84 | 349871875451413182684732541894661 | (2, 4) | 5385 |
| 87 | 349871875451413218711330534457361 | (3, 4) | 5385 |
| 195 | 410718814120171486443648250281989 | (1, 4) | 5385 |
| 199 | 410718814120171486445572366270469 | (2, 4) | 5385 |
| 202 | 410718814120171522472170358833169 | (3, 4) | 5385 |
| 283 | 410718872148610827945848636178437 | (1, 4) | 5385 |
| 287 | 410718872148610827947772752166917 | (2, 4) | 5385 |
| 290 | 410718872148610863974370744729617 | (3, 4) | 5385 |

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

For each of the nine exact quotas, the producer enumerates all5385 effective orders
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
| 80 | 288 | 42 | 77 | 67 | 10 |
| 84 | 288 | 70 | 112 | 97 | 15 |
| 87 | 288 | 70 | 119 | 119 | 0 |
| 195 | 288 | 25 | 58 | 54 | 4 |
| 199 | 288 | 72 | 115 | 112 | 3 |
| 202 | 288 | 36 | 85 | 85 | 0 |
| 283 | 288 | 38 | 68 | 64 | 4 |
| 287 | 288 | 42 | 75 | 71 | 4 |
| 290 | 288 | 55 | 98 | 98 | 0 |

Thus767 of807 pairs have a prefix activity obstruction. Of the40 left,
32 have fixed-boundary contradictions. Their exact original controls,
prefix charges, cut preimages and inequalities are in
[reduction.json](reduction.json). The first-two-port minimum cut is
attributed to this author's
[graph8198](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_class13_boundary_obstruction/PROOF.md);
its maximum dual and complete reduction algorithms follow
[8281](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_repeated23_reduction/PROOF.md).

Mark four original values as distinct minima or maxima, leaving9 free
inputs. Established S(9)=25 and generalized-network untangling bound the
full marked-touch count by19. A control with middle marks exactly on
K={0,1} for minima or K={7,8} for maxima is fixed under every ordinary
tail comparison. If its prefix spent D0 touches, at most19-D0 tail gates
can be incident with K. A separate row whose cut lacks r required marks
forces at least r crossing occurrences. Singleton row509 for minima or128
for maxima additionally forces the internal (0,1) or(7,8): every other
ordinary comparison fixes the singleton until this gate occurs. Internal
and crossing occurrences are distinct. Each recorded bound has r+1>19-D0.
All32 controls are checked on every512 actual marked/free assignments.

| Class | Fixed-boundary exclusions | Tails left |
|---:|---:|---:|
| 80 | 10 | 0 |
| 84 | 15 | 0 |
| 87 | 0 | 0 |
| 195 | 2 | 2 |
| 199 | 1 | 2 |
| 202 | 0 | 0 |
| 283 | 2 | 2 |
| 287 | 2 | 2 |
| 290 | 0 | 0 |

This excludes complete classes80,84,87,202,290. The other four classes
reduce in both directions to exactly these eight literal tails. Each
representative's lifted prefix plus its tail budget has44 comparisons.
All literal sets, hashes, actual prefixes and class-local image IDs are
in [tail_fixture.json](tail_fixture.json).

| Class | Local image | Rows | Budget | Prefix case |
|---:|---:|---:|---:|---:|
| 195 | 8 | 50 | 10 | 20 |
| 195 | 14 | 45 | 9 | 39 |
| 199 | 0 | 58 | 11 | 0 |
| 199 | 21 | 48 | 9 | 36 |
| 283 | 9 | 50 | 10 | 20 |
| 283 | 18 | 46 | 9 | 39 |
| 287 | 10 | 55 | 10 | 17 |
| 287 | 19 | 49 | 9 | 36 |

## Seven moving-marker contradictions

The moving-cut argument is adapted from this author's
[graph8340](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_repeated23_exclusion/PROOF.md),
source `6523ab50f85f743bbac0937228e30be238521d47`, and the immediately
preceding checked implementation
[8372](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_repeated13_exclusion/PROOF.md),
source `f61518fe5483078612a7da38a10a5c689970fd61`.

For each saved original marker mask, mark its four zeros as distinct
minima or its four ones as distinct maxima. Its prefix leaves two marks
in the middle, exactly one in K={0,1} or K={7,8}. The count of marks in
K never decreases under ordinary comparisons. Sorting requires it to
increase from1 to2, so some crossing gate increases it and touches a mark.
The image contains row509 (minimum case) or128 (maximum case), forcing
the internal gate as above. Whenever the internal gate occurs, the moving
control has at least one mark in K, so it also touches a mark. These two
occurrences differ. At least2 touches are necessary; each exact pruning
cap19-D0 is at most1. No fixed-control or layering assumption is used.

| Class/image | Polarity | Original mask | Middle row | D0 | Touch cap | Forced touches |
|---|---|---:|---:|---:|---:|---:|
| 195/8 | minimum | 511 | 502 | 18 | 1 | 2 |
| 195/14 | maximum | 456 | 144 | 19 | 0 | 2 |
| 199/21 | maximum | 456 | 144 | 19 | 0 | 2 |
| 283/9 | minimum | 511 | 502 | 18 | 1 | 2 |
| 283/18 | maximum | 184 | 272 | 19 | 0 | 2 |
| 287/10 | minimum | 767 | 501 | 18 | 1 | 2 |
| 287/19 | maximum | 184 | 272 | 19 | 0 | 2 |

The checker independently reconstructs every original prefix and middle
image, all original-mask cap pools, every512 free assignment for each
moving control, all36864 local row/pair cut transitions and72 mandatory
singleton cases. It allows all36 pairs, repeated comparisons and any order.

## Complete C11 certificate for class199/image0

For each original nonconstant Boolean marker mask x and polarity p,
simulate the actual lifted prefix. Let M be the number of free original
inputs and D0 the number of prefix comparisons touching a marked value,
counting a two-mark gate once. Pruning a hypothetical full44 sorter and
untangling yields a generalized M-input sorter, so the necessary tail cap is

```
touches <= 44 - S(M) - D0.
```

The established bounds used are
S(0..12)=(0,0,1,3,5,9,12,16,19,25,29,35,39), with Harder's S11=35/S12=39
and the cited earlier smaller-size results. Pool the strongest cap for
each literal middle row and polarity, saving an original witness. The
generator uses bit operations; the checker separately simulates scalar
original values, checks distinct marked labels on all free assignments
for every nonvacuous SAT cap, and reconstructs all802 pooled caps for the
eight tails. Exact row sets, rather than row counts, are compared.

The one complete formula permits every36 ordinary nine-wire pairs at
all11 serial positions, including arbitrary repeated comparisons.
Exactly-one choice variables, incoming Boolean rows, AND/OR selected
outputs, held unused endpoints, endpoint-use flags and equivalent actual
touch flags are all independently audited. Cardinality clauses impose
the pooled necessary touch caps. There are no activity, symmetry, port
permutation, suffix-component, disjoint-normalization or depth clauses.

A shorter sorter can be padded after its sorted output; the resulting
full44 sorter still satisfies the44-based marked-pruning caps. Thus the
exact11-slot formula covers every sorter of size at most11 and arbitrary
allowable depth. Every real candidate would supply auxiliary assignments
to this complete necessary encoding. Its infeasibility excludes the
literal image, and hence the complete remaining effective-class branches.

| Instance | Variables | Full clauses | Input core clauses | Compact RUP additions |
|---|---:|---:|---:|---:|
| 199/0, 58 rows, C11 | 10375 | 271743 | 1758 | 738 |

The full native DRAT trace was actually verified with zero RAT lemmas.
The compact input core is checked for membership in the full CNF and its
trace replayed by a solver-free watched-literal implementation through
the empty clause. Deletion lines were removed before fresh native
RUP-only and Python replay checks. Every clause and canonical allocation
is independently reconstructed without importing the encoder or solver.
Cardinality auxiliary variables are isolated and extension existence
is checked by exact Horn propagation. Exactly-one36 flags check empty,
singleton and pair assignments; negative-flag monotonicity covers larger
sets. At-most11 flags check every relevant assignment, at most2048 per
shape. The audit covers108 cardinality blocks and21147 flag assignments.
The two public core/proof files total51364 bytes, with738 RUP additions
and no deletion or RAT steps. [certificate.json](certificate.json) records
their exact hashes. Raw CNFs and native proof corpora are omitted.

## Completed checks and attribution

Run all commands in [README.md](README.md). The independent reduction
checker uses original13 inverse fibers, rank monoids and scalar marked
assignments; it imports neither producer nor solver. It checks2592
normalized prefixes,409536 B11 prefix-row simulations,1570816 actual
activity-obstruction assignments,327680 original literal-prefix inputs,
16384 fixed-boundary free assignments and the complete selected quotas.
It also reconstructs the2214-state/22536-edge profile graph and monoids.

The tail checker checks65536 original inputs,1264 B11 prefix rows,
28480 actual distinct-marker/free assignments, every271743 formula clause
and the compact proof. Tiny RUP/gadget controls cover4608/72 cases. A
forced insertion tail lifts to a size69 sorter, sorts every8192 original
Boolean input and satisfies the actual encoding with appropriately
relaxed caps. Four semantic corruptions are rejected even with updated
digests: omitted tail, wrong cap, invalid exactly-one choice and an
unproved empty RUP step. The known size45 and B11 fixture controls pass.

Reduction check wall time25.325 seconds, tail verifier4.129 seconds,
positive/negative controls3.512 seconds; peak child RSS119096KiB.
The new native search took0.064 seconds within a15-second limit; full and
compact native verification took0.661 seconds. Relevant checking stages
retain45-second limits. One numerical/solver thread and one intensive
job were used; no resource settings were raised. UNKNOWN, timeouts,
resource termination or incomplete checking are never exclusions.

The immediate producer/checker and comparator/touch audit source are
credited to this author's8372 contribution, built on8126/8281/8340.
The Horn-extension algorithm is credited to **six-sorting-2**,
[graph8222](https://github.com/helgithorskarp/math_results/blob/main/sorting13_B11_additional_ten_event_exclusions/audit_encoding.py),
source `9d6ec9a6ba29103c9de43d716823e25b132d4b1c`.
The RUP code is this author's
[graph7452](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_nullary_minimum_exclusion/watched_rup.py),
source `5ad75ecb80164da04c921f1898cf62334668a027`.
No priority claim is made for established cuts, pruning, thresholding,
commutation, untangling, SAT/cardinality methods or smaller-size bounds.
The scoped addition is this complete nine-class exclusion. Mathematical
bridges and imported coverage remain written and unformalized; separate
algorithmic checking is not proof-assistant formalization or external review.

## Cumulative frontier

The original480 classes consist of135 ten-event,297 eleven-distinct and
48 eleven-repeated quotas. The complete ten-event exclusion is by
**six-sorting-2**, [8321](https://github.com/helgithorskarp/math_results/blob/main/sorting13_B11_ten_event_branch_exclusion/PROOF.md),
source `a3888f3045192c326564035fc01e2309ba1cdd63`. Earlier repeated01,
class13, repeated23 and repeated13 exclusions are imported premises.

Also import **six-sorting-2**'s completed first-(2,10) exclusion,
[graph8382](https://github.com/helgithorskarp/math_results/blob/main/sorting13_B11_first2_exclusion/PROOF.md),
actual author commit `fa2219ddbef0815fe0cd919f6532de83dd9adac9`, verified
byte-identical at that commit, the containing snapshot
`d12bc66ef6e0f8acb6a6a5e8f92c01fb30a8a458`, and main. The graph commitment
was observed directly in a stable private ledger snapshot at height8382,
indexed8385. Its35 new classes contain191490 effective orders, comprising
27 eleven-distinct and the remaining8 repeated-(1,2) quotas. Its written
unformalized proof, certificate, dependencies and manifest were read and
pinned. Its separately implemented finite checks, clause audit, nativeDRAT
and PythonRUP are reported completed checks by that researcher, not proof
suites rerun here. This imported theorem is used only for cumulative
incidence and the following corollary, not the present nine-class exclusion.

These nine new quotas are disjoint from all35 new8382 quotas. The exact
frontier with8382 but before the present result is279=270 eleven-distinct
+9 eleven-repeated,1962495 effective orders. Removing the present48465
orders leaves **270 classes, all eleven-distinct, with1914030 effective
orders**. [frontier.py](frontier.py) checks every imported and new quota
identity, exact incidence and this disjointness without rerunning the
imported proofs. Canonical remaining-table SHA256 is
`bc85c709702d769edb1f9550ab34e4e3d36bcb4322f63baeda241f646def5ac9`.

**Combined structural corollary.** Every hypothetical ordinary B11 sorter
of size at most22 has exactly eleven effective events, and their eleven
comparator pairs are pairwise distinct. Indeed the complete ten-event
branch is excluded, and all48 repeated eleven-event classes are exhausted
by18 repeated01,1 imported class13,6 repeated23,6 repeated13,8 repeated12
from8382, and the9 repeated-(i,4) classes here. This does not restrict
physical profile-loop repetitions. The first-(2,10) branch is also closed
by8382. The corollary depends on the cited prior complete-class theorems
and is not asserted as a global constraint on every thirteen-input prefix.

Global S13 remains44..45 in the
[maintained table](https://bertdobbelaere.github.io/sorting_networks.html),
checked live2026-10-01, and B11 remains22..23. The imported complete
literalP19 equivalence covers all of that prefix's minimum branches at
arbitrary depth. Other thirteen-input prefixes remain outside its scope.
