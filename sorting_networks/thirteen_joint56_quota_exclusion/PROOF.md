# The joint (5,10)/(6,10) effective quotas of B11 C22 are excluded

Author and executing agent: **six-sorting-1, researcher**, 2026-10-01.
All team signatures share one identity; this names the actual author.
Status: written, unformalized computer-assisted intermediate lemma, with
separately implemented finite checks by this researcher. No external
reviewer verdict or proof-assistant formalization is asserted.

**Theorem.** An ordinary sorter of the specified 158-row B11 image with
at most 22 comparators cannot have both (5,10) and (6,10) among its
effective extreme events. The new finite part excludes all 18 original
eleven-distinct quotas with these two pairs, covering 210,960 effective
orders. Every one of those orders first touches port10 with (6,10);
that is a consequence of complete traversal, not a search restriction.
This is a quota-cohort exclusion, not an exclusion of the entire
first-(6,10) branch. No selected parallel depth is imposed.

The quotient indices are

```
96,97,98,99,100,101,102,103,104,106,107,108,109,110,111,112,113,114.
```

Their exact decimal codes and order counts are in
[fixture.json](fixture.json). All physical repetitions and ordinary
loop interleavings are covered by the imported normalization. The
global thirteen-input size gap remains 44–45; B11 remains 22–23.

## Exact target and complete coverage

All ports are zero based. Comparator(a,b), a<b, sends the smaller entry
to a. Bit i of an integer row is the value at port i. The literal full
prefix is G22=P19;(10,12);(0,5);(0,1), explicitly listed in the fixture.
Its image on original ports1..11 is B11, comprising 158 Boolean rows
with canonical SHA256
`2b776a68a6bfc671df43af0f186dfe42acc0ae870738bdd88fa153948bedeaf4`.
B11 port i is original i+1. The known B11 C23 control lifts to a full
C45 sorter; current scalar checks test all 8,192 original inputs.

Import six-sorting-2's
[complete literal-P19 equivalence](https://github.com/helgithorskarp/math_results/blob/main/sorting13_P19_binary_minimum_reduction/PROOF.md),
graph7885, source `ca993bc042ba81442a4afccb0d374d142696d0e7`:
a full C44 sorter beginning with literal P19 exists if and only if
this exact B11 image has a C22 sorter. This covers all P19 minimum
branches at arbitrary depth. Other thirteen-input prefixes are unresolved.

The [coupled profiles](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_joint_extrema_normal_form/PROOF.md)
(graph7871) and [480-class quotient](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_extreme_multiset_quotient/PROOF.md)
(graph7936) give initial low=(4,2,2,2,2,0,2,0,0,0,1) and
high=(0,0,0,0,0,4,0,2,4,4,1). At(a,b), low becomes
(2max(low[a],low[b]),0) at those ports and high becomes
(0,2max(high[a],high[b])). Both sums must stay at most16.
The first port10 partner cannot be0,7,9. Terminal profiles are low16
at0 and high16 at10. Effective events change these profiles or the
first-touch flag; other physical comparisons are retained as loops.

Import the [eleven-distinct-event necessity](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_repeated_i4_exclusion/PROOF.md),
graph8395, source `64e32080f865757fe190ab6623d6b9d43b7be6d1`.
Every B11 C22 sorter has exactly eleven effective events on pairwise
distinct comparator pairs. From the complete original480 table, select
exactly event count11, all55 multiplicities at most1, and multiplicity1
for both (5,10),(6,10). This gives exactly the18 quotas above, independently
of any previous frontier blacklist. Both current traversals exhaust all
their orders, with weighted first-touch histogram `{6:210960}`. Presence
of a pair in a quota is never used to fix its first occurrence.

## Full-function preparation and prefix obstructions

Import the [one-preparation-block theorem](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_single_preparation_normal_form/PROOF.md),
graph8126, source `9e233924e79cc8a4b52001cda87cc8f56db3003c`.
Every eleven-event C22 word is equivalent on arbitrary ordered inputs
to Eminus;A;f;Eplus;T, where f is the first port10 event and A acts on
the empty ports J before f. Earlier loops commute only past disjoint
later events within their phase; no loop crosses f, and overlaps keep
their order. Later loops go into the nine-wire tail T.
There are at most four ports in J. Replacing A by a shortest full-function
representative of length h preserves the function and leaves tail
budget11-h. The monoids on1,2,3,4 ports contain1,2,11,261 maps,
with maximum shortest lengths0,1,3,5. Boolean-function production and
independent functions on distinct-rank permutations agree exactly.

The forward weighted-profile producer is adapted from this author's
[first4 source](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_first4_branch_exclusion/PROOF.md),
graph8450, source `53917ff15b36151e11b69fc8df323afc1292e3bd`.
The independent checker reconstructs original13 marked-pair inverse
fibers, the full2,214-state/22,536-edge graph, rank functions and scalar
comparators. Only disjoint events within each phase commute; no wire
permutation is used. The 210,960 orders give240 canonical phase triples,
10,524 normalized prefixes and3,952 literal image/budget pairs.
Equivalent pairs use one representative because any sorter of their
literal image also lifts through that representative. Original0/1/11/12
hold the first two/last two order statistics. Tail port i is B11 i+1
and original i+2.

The [saturated activity obstruction](https://github.com/helgithorskarp/math_results/blob/main/sorting13_B11_pruning_saturation_activity/PROOF.md),
graph7944, excludes3,452 pairs. Each designated two-marker family spends
nine prefix passages; pruning any fullC44 completion leaves an eleven-input
sorter with35 comparisons. A retained prefix comparator always ordered
on that free Boolean domain could be deleted, contradicting S11=35.
The checker uses distinct minima(-2,-1) or maxima(2,3), strictly outside
the free values0/1. It checks7,069,696 assignments, plus26,624 for the
initial clamped domains. For all500 pairs left after activity it replays
4,096,000 original inputs. Fixed one/two-port boundary cuts exclude477
pairs, with248,320 strict marker/free assignments. Complete regenerated
boundary witnesses stay in ignored out/ and are authenticated by counts
and canonical hashes. Exactly23 literal tails remain.

## Pruning caps, direct cuts and twelve complete certificates

Give marked original inputs distinct constants all below, or all above,
the M free inputs. Deleting comparisons touching a mark leaves a generalized
M-input sorter; untangling yields an ordinary sorter with no additional
comparisons. A fullC44 sorter therefore has at most44-S(M) marked passages.
If the prefix spends D0, the necessary tail cap is c=44-S(M)-D0.
Marker membership follows an exact Boolean trajectory; a comparison
touching either mark is charged once. The producer pools the tightest cap
from all8,190 nonconstant original masks, separately for both polarities.
The independent scalar audit reconstructs every literal image and cap
and checks all binding controls against actual distinct-marker/free inputs.

The established size bounds used are
S(0)..S(12)=0,0,1,3,5,9,12,16,19,25,29,35,39.
[Harder](https://arxiv.org/abs/2012.04400v3) proves S11=35/S12=39;
[Codish, Cruz-Filipe, Frank and Schneider-Kamp](https://imada.sdu.dk/u/lcf/pubs/paper26.pdf)
prove S9=25/S10=29 and recall generalized-network untangling.
These results, pruning and the zero-one principle are prior work.

For a marked-minimum first-k cut, or marked-maximum last-k cut, the number
of marks inside never decreases and grows at most once per crossing.
Every growth touches a mark. This gives one single-control movement
obstruction. For two ports, the sole-zero row509 forces comparator(0,1)
and the sole-one row128 forces(7,8). If a control initially has a mark
inside that cut, this additional comparison is charged, separately from
the crossing deficit; this excludes six tails.

Four further tails use the fixed internal-count mechanism credited to
[six-sorting-2's first2 proof](https://github.com/helgithorskarp/math_results/blob/main/sorting13_B11_first2_exclusion/PROOF.md),
graph8382. Put exactly four marks in the sorted boundary cut K. The
control is fixed, so all internal and crossing comparisons touch a mark.
A row with a crossing deficit d forces at least d crossings. Restrict
the literal rows to those with all outside bits unmarked; crossings and
outside comparisons act trivially on that projection. Its restricted
four-port image requires q internal comparisons. Thus d+q>c is impossible.
The producer finds q by finite BFS. The independent checker exhausts
every ordinary word shorter than q, including repetitions, and tests a
positive word of length q. No heuristic lower bound is accepted.

For the12 other tails, all budgets are11. Encoding.py allows every one
of36 ordinary pairs at each of11 serial slots, including repetitions,
and includes every literal row. There are no activity, symmetry,
selected-depth, wire-permutation or suffix constraints in these CNFs.
Exact-one pair choices, endpoint flags and AND/OR/hold clauses implement
each comparator. One-sided touch flags and sequential counters implement
every necessary pooled cap. Any candidate sets flags to its actual
touches and extends the counter auxiliaries, so all mathematical
candidates are retained. If a shorter completion exists, pad its sorted
output to the stated budget; its fullC44 lift must still satisfy the caps.

Audit_encoding.py imports no producer or solver and reconstructs every
clause and variable allocation. The Horn extension-existence audit is
credited to [six-sorting-2, graph8222](https://github.com/helgithorskarp/math_results/blob/main/sorting13_B11_additional_ten_event_exclusions/audit_encoding.py).
Full native DRAT checks and compact native RUP replay have zero RAT steps.
The supplied compact cores contain22,088 clauses and the proofs9,443
RUP additions. The independent Python checker authenticates every core
clause against the regenerated full CNF and checks every RUP addition
through the final empty clause. The RUP kernel comes from this author's
[graph7452 source](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_nullary_minimum_exclusion/watched_rup.py).
All formulas and raw traces are regenerable; only compact evidence is public.
Twelve actual69-comparator positive controls sort all8,192 inputs each
and satisfy relaxed encodings. Semantic malformed-evidence controls
exercise data, cuts, choices, RUP and complete-quota coverage.

The complete partition is

```
3952 = 3452 activity + 477 fixed boundary
     + 1 movement + 6 moving two-port + 4 fixed internal + 12 CNF/RUP.
```

Consequently none of the18 quotas has a B11 C22 completion, including
arbitrary allowable depth and every covered physical-loop arrangement.

## Scope, cumulative incidence and trust

The prior ten-event/repeated-event exclusions, first2/first3 branches and
45-class first4 branch are imported, not rerun here. Removing the current
18 new quotas from that pinned frontier leaves171 distinct classes and
983,070 effective orders:135 allowed-partner(5,8) quotas and36(6,8) quotas.
These are quota memberships; they do not fix first touch or forbid later
port10 comparisons with other partners. The concurrent
[six-sorting-2 first4 variant](https://github.com/helgithorskarp/math_results/blob/main/sorting13_B11_first4_exclusion/PROOF.md),
graph8452, covers the same45 classes as8450 and counts zero additional
classes. Its reported algorithmic checks were read, not replayed here.
Other subsequently published peer closures are outside this pinned
cumulative calculation and must be incorporated in a later checkpoint.

The original all-real profile necessity, one-block normalization,
zero-one and pruning/untangling bridges remain written and unformalized.
Current exact algorithmic independence is not an external-person review.
Timeout, UNKNOWN, resource kill or incomplete computation would establish
no exclusion. No44-comparator sorter or arbitrary-prefix global exclusion
is claimed. See [README.md](README.md) for commands and
[dependencies.json](dependencies.json) for exact source/graph provenance.
