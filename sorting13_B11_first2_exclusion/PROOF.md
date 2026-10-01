# B11 first-(2,10) branch excluded at arbitrary depth

Author and executing agent: **six-sorting-2, researcher**, 2026-10-01.
This is a written, unformalized computer-assisted intermediate lemma.
The shared signing identity does not identify the individual researcher.
Separate exact algorithms are not an external-person review.

**Result.** The specified B11 image has no ordinary sorter of at most22
comparators whose first comparison touching B11 port10 is (2,10).
The new result excludes35 complete eleven-event classes and191490
effective orders, including every physical profile-loop interleaving
and every allowable depth. Physical comparator repetitions remain allowed.

All ports are zero based and comparator (a,b), a<b, sends its minimum to a.
G22=P19;(10,12);(0,5);(0,1) is the literal22-comparator prefix from
the [common fixture](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_single_preparation_normal_form/fixture.json).
Its exact image on original1..11 is the158-row B11 set. B11 port i means
original i+1. Import the complete literal-P19 equivalence
[7885](https://github.com/helgithorskarp/math_results/blob/main/sorting13_P19_binary_minimum_reduction/PROOF.md):
this B11 C22 existence question covers every normalized minimum branch
of literal P19, with arbitrary depth. Other thirteen-wire prefixes remain
outside that coverage. The maintained [table](https://bertdobbelaere.github.io/sorting_networks.html)
still gives S(13)=44..45, checked live2026-10-01.

**Complete quota coverage.** Import the necessary coupled-profile graph
[7871](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_joint_extrema_normal_form/PROOF.md)
and its complete480-class effective-multiset quotient
[7936](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_extreme_multiset_quotient/PROOF.md).
Initially the reduced low/high weights are

```
low  = (4,2,2,2,2,0,2,0,0,0,1)
high = (0,0,0,0,0,4,0,2,4,4,1).
```

At (a,b), low endpoint weights become (2max(low[a],low[b]),0), and
high weights become (0,2max(high[a],high[b])). Each sum is at most16.
An effective event changes this state or the first10 flag; other physical
comparisons are loops. Terminal low16 is on0 and high16 on10.
Every B11 C22 sorter has ten or eleven effective events. The entire
ten-event branch was excluded by this researcher's
[8321](https://github.com/helgithorskarp/math_results/blob/main/sorting13_B11_ten_event_branch_exclusion/PROOF.md),
sourcea3888f3045192c326564035fc01e2309ba1cdd63; that theorem is imported here.

In the eleven-event branch, the unique first10 comparison is a unary
refill f. Selecting all quotas containing (2,10) from the pinned480-class
table gives exactly36 classes and196875 effective orders. Independent
quota traversal verifies that f=(2,10) in every order of every selected
class, rather than just one representative. Class13, with exact code
349871875148001158693749134458897 and5385 orders, is already excluded by
six-sorting-1's [8198](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_class13_boundary_obstruction/PROOF.md).
The new35 classes and191490 orders are listed completely in
[certificate.json](certificate.json):27 have eleven distinct effective
gates and8 repeat effective(1,2). Effective repetition is separate from
permitted physical loop repetition. No known theorem is claimed as new.

**Physical-word normalization.** Import the general one-preparation-block
theorem [8126](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_single_preparation_normal_form/PROOF.md),
source9e233924e79cc8a4b52001cda87cc8f56db3003c. Every eleven-event physical
word is equivalent on arbitrary ordered inputs to

```
E_minus ; A ; f ; E_plus ; T.
```

Pre-f and post-f loops commute only past disjoint events in their own
phase. A acts on the literal jointly empty set J immediately before f,
with |J|<=4; T acts on B11 ports1..9. Full local comparator-function
monoids have1,2,11,261 functions for |J|=1,2,3,4 and maximum shortest
representative lengths0,1,3,5. Replacing A by a shortest full-function
representative of length h preserves its function on all ordered inputs
and does not increase length. Thus T has budget11-h. Shorter sorters
can be padded after their sorted output on the middle ports to the
stated budget, leaving the first10 event unchanged.

Canonicalize each E phase only through exchanges of disjoint comparisons;
its overlap partial order retains all possible physical functions.
The new generator uses reduced forward profiles and Boolean bit planes.
The checker independently uses original13 marked-pair inverse fibers,
distinct-rank permutation maps and scalar row lists. It reconstructs the
full2214-state/22536-edge parent graph and all local monoid entries.
Both recover318 canonical phase triples,20196 normalized prefixes and
6114 literal image/budget pairs. They compare each table entry, not only
aggregate counts. Neither wire permutations nor a parallel-depth bound
are used. Programs are credited to **six-sorting-1**, published8281/source
f88db8425d4534960ce783071ab274bbd45e025a; exact author bytes are pinned.

After each prefix original0,1 hold the two smallest and11,12 the two
largest values. Nine-wire port i means original i+2. Its lifted prefix
has33+h comparisons and its tail budget is11-h, totaling44. Prefixes
with the same literal image and budget have the same tail-existence
question. Any sorter of that image would also sort a representative
with the same image/budget, irrespective of differing marked routes.
For every surviving representative its original image is reconstructed
on all8192 inputs. Equality of row counts alone is never used.

**Prefix activity and ordinary boundaries.** Import established S(11)=35
from [Harder](https://arxiv.org/abs/2012.04400v3), and the selected original
marked-pair saturation domains of
[7944](https://github.com/helgithorskarp/math_results/blob/main/sorting13_B11_pruning_saturation_activity/PROOF.md).
Each selected pair touches exactly9 lifted-prefix comparisons and ends
on held ports, which the tail cannot touch. Pruning these two extreme
values from a hypothetical full44 sorter and untangling leaves35
comparisons on11 free inputs. Every retained prefix comparison must
swap some free Boolean assignment; otherwise deleting it yields a
sorter of size34, contrary to S(11)=35. A recorded non-swapping retained
comparison therefore excludes the whole representative image/budget.
The checker verifies the actual distinct-mark/free trajectories and
that both obstructed operands are free Boolean entries.

This excludes5693 pairs, using11659264 actual2048-assignment replays.
Of the421 remaining pairs,417 are excluded by the fixed first/last
two-middle-port cuts of8198 and their8281 maximum dual. Mark four original
minima or maxima, leaving9 free inputs. S(9)=25 bounds total marked
touches by19; subtract actual prefix touches. A sorted boundary-marker
control stays fixed under every ordinary tail gate. A separate row
forces crossing comparisons, and a singleton boundary row forces its
internal comparison. These are distinct occurrences, each touching
the control. All saved controls, cut preimages and inequalities are
independently checked on394752 actual free assignments. Established
pruning/cut methods are attributed prior work.

**Two stronger four-port internal counts.** The new cases use K={0,1,2,3}
in the middle nine wires. Mark the six original zeros of control127 as
distinct minima and leave7 free inputs. The actual prefix places two
marks on original0,1 and four marks on K. The control's middle row has
zeros exactly on K and ones elsewhere, hence every ordinary tail gate
fixes its Boolean marker membership. Established S(7)=16 bounds total
marked touches by44-16=28. The tail touches are precisely comparisons
incident with K; its cap is28-D0, where D0 is the prefix charge.

For any middle row r, the number of zeros in K never decreases. Sorting
needs min(4,9-popcount(r)) zeros there. Only crossing comparisons can
increase their number, by at most one. Thus

```
crossings >= min(4,9-popcount(r)) - (4-popcount(r & 15)).
```

Additionally consider every certified row whose five ports outside K
are all ones. All comparisons not internal to K fix such a row: an
outside gate compares ones, and a crossing gate has its minimum endpoint
in K and maximum endpoint outside. Consequently the subsequence of
internal comparisons alone must sort the four-port restricted image.
If that image needs q comparisons, at least q internal occurrences are
required. Internal and crossing occurrences are disjoint, so their
lower bounds add; both categories touch the fixed marked control.

| Parent class/local image | Budget | D0 | Touch cap | Crossings | Internal lower bound | Required |
|---|---:|---:|---:|---:|---:|---:|
| 129/8, prefix case20 | 10 | 23 | 5 | 2 | 4 | 6 |
| 129/23, prefix case46 | 9 | 24 | 4 | 2 | 3 | 5 |

Both use cut row414 with original preimage6331. Their internal images are
respectively [0,2,4,6,7,8,10,12,13,14,15] and
[0,2,8,10,11,12,13,14,15]. The producer finds shortest witnesses by exact
BFS. Independently the checker exhausts all six-pair words of lengths
below4 and below3,259+43=302 words, and checks explicit sorting words
of lengths4 and3. It replays all128 free assignments for each distinct
marked control. Truth controls separately check18432 row/gate crossing
cases and576 internal-projection cases. Hence6>5 and5>4 exclude these
two tails without a SAT premise. This is a new application of internal
sorting counts to these particular cuts; general pruning/cut principles
and the known S(7) bound are not claimed new.

**Two actual C11 certificates.** Exactly two pairs remain:

| Parent class/local image | Rows | Budget | Prefix case | Variables | Full clauses | Input core | RUP additions |
|---|---:|---:|---:|---:|---:|---:|---:|
| 14/0 | 59 | 11 | 0 | 9868 | 106568 | 609 | 88 |
| 129/0 | 55 | 11 | 0 | 9176 | 98498 | 615 | 116 |

Each lifted prefix has33 gates. For every nonconstant original input and
both polarities, mark all original zeros as minima or all original ones
as maxima. If M original free inputs remain and D0 marked touches were
spent, pruning/untangling a hypothetical full44 sorter gives the necessary
tail cap44-S(M)-D0. The original Boolean mask determines marker membership
and charges independently of the unmarked values. Pool the tightest
cap by literal middle row and polarity. Known size bounds through12 are
0,0,1,3,5,9,12,16,19,25,29,35,39. In the implementation the total size
is **len(prefix)+budget=33+11=44**. The old ten-event kernel's constant32
is not carried into this capacity calculation.

The CNFs permit all36 ordinary nine-wire pairs at all11 serial positions,
including repetitions. Boolean inputs and sorted outputs, min/max gate
recurrences, untouched wires, exactly-one choices and actual pooled
marked-touch capacities are encoded. Adjacent inverted disjoint gates
are put in lexicographic order; commuting them preserves the function
and all actual marker charges, and strictly decreases the serial word.
There are no activity or suffix-component constraints in these CNFs.
There is no wire-permutation or parallel-depth cutoff. Padding a shorter
sorter after its sorted output gives a valid full44 lift, whose pruning
caps still hold, so the11-slot exclusion also covers smaller tails.

The generic encoder and scalar/clause kernel come from this researcher's
[8222](https://github.com/helgithorskarp/math_results/blob/main/sorting13_B11_additional_ten_event_exclusions/PROOF.md),
source9d6ec9a6ba29103c9de43d716823e25b132d4b1c. The new provider computes
the actual33-gate prefix. The scalar audit changes only the two old
capacity constants to len(prefix), and supplies this cohort's strict
finite provenance. The clause/Horn auditor is reused verbatim. Neither
independent auditor imports the encoder or a SAT solver. It reconstructs
every original input, pooled cap, non-cardinality clause and canonical
variable allocation. Fresh cardinality auxiliaries are isolated; exact
Horn closure checks extension existence on every relevant flag assignment.
The actual two formulas have205066 clauses and206 cardinality blocks;
the shape checks exhaust23195 flag assignments. This proves every
mathematical candidate extends to the actual checked formula.

Both complete formulas were freshly solved with logged Glucose4 proofs.
Native DRAT checked both with zero RAT lemmas. The input cores are subsets
of the full audited CNFs, and the separately implemented watched-RUP
checker replays through the empty clause. It rejects an empty clause
before replay and checks4608 tiny truth controls. Deletion steps may be
ignored because retaining clauses only strengthens unit propagation.
The four supplied files total46499bytes,1224 input core clauses and204
RUP additions. Their hashes and exact provenance are in the certificate.
The checker is credited to **six-sorting-1**,7452/source
5ad75ecb80164da04c921f1898cf62334668a027. No native UNSAT answer or hash
alone is treated as proof.

A36-comparator insertion tail lifts to a genuine full69 sorter; all8192
original inputs and all356143 actual positive formula clauses are checked.
Five deliberate semantic corruptions are rejected by the actual public
checkers, bypassing hashes: omitted cohort class, omitted boundary leaf,
false internal lower bound, false distinct-mark prefix charge and false
pooled capacity. The finite checker itself covers3448832 original-prefix
inputs,26624 initial marked-domain assignments and the known full45
control. Full finite producer/checker wall times50.98/132.02seconds and
peak57728KiB stay within one CPU and the unchanged memory cap.

**Implication and remaining frontier.** All6114 pairs now have a checked
contradiction:5693 prefix activity,417 ordinary boundaries,2 four-port
internal counts and2 complete C11 proofs. The finite normal form exhausts
every physical sorting candidate in the35 new quotas. Importing8198
closes the36th quota, and8321 closes all possible ten-event words. The
first-(2,10) B11 branch is therefore excluded at arbitrary allowable depth.
Each of the two new C11-certified row sets needs at least12 comparisons;
no12-comparator construction or lower bound13 is asserted for them.

Relative to8321 and8281, the35 new disjoint exclusions reduce323 classes
and2202450 orders to288=270 eleven-distinct+18 eleven-repeated,2010960
orders. This pass also reads and imports six-sorting-1's concurrently
published [complete repeated23 exclusion](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_repeated23_exclusion/PROOF.md),
source6523ab50f85f743bbac0937228e30be238521d47, adding classes40/155/243,
and [complete repeated13 exclusion](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_repeated13_exclusion/PROOF.md),
sourcef61518fe5483078612a7da38a10a5c689970fd61, adding36/42/151/157/239/245.
Their checked proofs are imported, not rerun by this researcher. Exact
quota identities, byte pins and disjointness are checked entrywise:
these9 classes remove48465 further orders, leaving
**279=270 eleven-distinct+9 eleven-repeated**,1962495 effective orders.
The frontier arithmetic is separate from proof checking.

Established smaller sorting-network bounds and generalized untangling
are attributed to [Codish, Cruz-Filipe, Frank and Schneider-Kamp](https://imada.sdu.dk/u/lcf/pubs/paper26.pdf)
and earlier literature; Harder establishes S(11)=35/S(12)=39.
The maintained table attributes S(7)=16 to Knuth's earlier work.
Comparator commutation, thresholding, zero-one reasoning, pruning,
SAT/cardinality encoding and RUP are established methods. The scoped
addition is this complete35-class exclusion and the two specific
four-port-count applications. Written support/commutation/threshold/
pruning bridges and imported necessary coverage remain unformalized.
No exhaustive priority audit, external-review verdict, full B11 exclusion
or global thirteen-input resolution is asserted. Global S(13)=44..45
and B11=22..23 remain; non-P19 arbitrary-prefix coverage is still missing.
Reproduction commands and exact trust boundaries are in [README.md](README.md).
