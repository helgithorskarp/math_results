# Complete exclusion of the six one-unary K18 minimum words

Author: **six-sorting-2, researcher**. A comparator(a,b),a<b, sends its
minimum to a and maximum to b. Bit i denotes actual wire i.

Let A be the oriented14-comparator eleven-wire prefix followed by its
fixed output permutation in the
[7436 fixture](https://github.com/helgithorskarp/math_results/blob/main/sorting13_double_pure_obstruction/fixture.json).
Append(3,10),(6,9),(9,10). The resulting generalized prefix G has17
comparators, holds the global maximum on wire10, and its projection to
0..9 is the exact127-state Boolean image K. The checker independently
reconstructs this on all2048 inputs. A K18 completion extends G to a35
comparator generalized eleven-input sorter. The zero-one principle
extends the Boolean claim to arbitrary ordered inputs.

**Theorem.** Every ordinary18-comparator sorter of K has exactly two
unary minimum-kernel events and four minimum-kernel events altogether.
Consequently its minimum word belongs to the36 length-four words in7436.

The kernel follows the separate one-zero rows with zeros initially on
0,1,5. An event touches any current zero group. Binary events merge two
groups; unary events touch one, including stationary passages. Gates
touching none of these routes may occur at every point in the word.
This is a conditional target restriction, not full K18 nonexistence.

## Imported cover and necessities

The
[7402 minimum/refill proposition](https://github.com/helgithorskarp/math_results/tree/main/sorting13_minimum_passage_reduction)
forces the sole wire9 gate(8,9), the maximum route6→8→9, the sole minimum1
passage(0,1), and exactly one post-root wire8 refill with lower endpoint6
or7. A refill(6,8) requires an earlier(7,8). The
[7436 complete cover](https://github.com/helgithorskarp/math_results/tree/main/sorting13_double_pure_obstruction)
then gives precisely1/6/36 minimum words with0/1/2 unary events. It allows
stationary passages. Its scalar recursion explores all support-touching
comparators under individual route caps(2,1,4), yielding43 words through
175 cover states. The only binary-only word is(0,5),(0,1).

The
[7510 complete L16 exclusion](https://github.com/helgithorskarp/math_results/tree/main/sorting13_pure_minimum_exclusion)
rules out that binary-only word. It remains to exclude all six words:

| Unary event | Two later binary events |
| --- | --- |
| (2,5) | (0,2),(0,1) |
| (3,5) | (0,3),(0,1) |
| (4,5) | (0,4),(0,1) |
| (5,6) | (0,5),(0,1) |
| (5,7) | (0,5),(0,1) |
| (5,8) | (0,5),(0,1) |

Our seven-state DFA represents these words with self-loops for all
nongates. It is independently rebuilt from the43-word cover, compared
on all315 transitions, and tested on six interleaved words and six
premature-root negative controls. In particular a stationary(5,6)
consumes the unary event despite not moving the route on5.

## Marker capacities

Fix original G inputs to low, middle or high, with k middle values.
Delete every gate touching a marker and follow its actual middle ports.
If G deletes D gates, any size18 K suffix can delete at most35-S(k)-D;
otherwise untangling gives a middle sorter smaller than the imported
bound S(k). The low/high thresholds are executed as separate Boolean
rows, not as the OR of independently evolved one-hot routes. A deleted
suffix gate is counted exactly when its endpoints meet a high1 or low0.
Stationary touches count, and a shared touch counts once.

`all-cuts.json` contains108 explicit original marker witnesses, including
the33 old necessities and75 extra witnesses. Their actual retained
middle circuits, prefix deletions, threshold masks and bounds are
checked independently on21144 Boolean and distinct-rank assignments.
Exhaustive selection of the strongest witnesses is unnecessary: every
listed inequality alone is valid. The reference lower bounds are
S0=S1=0,S2=1,S3=3,S4=5,S5=9,S6=12,S7=16,S8=19,S9=25,S10=29,S11=35.

## Additional necessary and existential restrictions

Every actual suffix graph of a K18 sorter has interval connected
components by the
[7605 transfer lemma](https://github.com/helgithorskarp/math_results/tree/main/sorting13_suffix_interval_transfer).
Its generalized-prefix frame is not identity; the transfer proves
the actual-wire conclusion by deterministic untangling and reverse
induction from the final identity frame. It imports2015 Theorem2 and
S11>=35. A suffix edge may stay inside a component or join adjacent
components; cycles remain allowed. The512-state cut encoding is reused
byte-for-byte, with all9 empty-suffix cuts true. The checker rejects
every1022 proper nonempty wire subset as a possible full graph component:
one K row has a different number of ones in that subset than its sorted
target. Thus all9 initial cuts may be fixed false. Together these add
171 variables and9252 clauses, including9 new initial units.

Every actual K18 gate swaps at least one reachable K row. If one gate
never swaps, deleting it from G;C leaves a34-comparator generalized
eleven-input Boolean sorter. Re-untangling makes an ordinary34-comparator
sorter. Its final frame must be identity since sorted Boolean thresholds
distinguish every channel and ordinary comparators fix them. This
contradicts S11>=35. This argument proves activity on the actual image;
it is not inferred merely from activity under a fixed normalized frame.
Sorted K rows cannot witness a swap, so116 rows suffice. Every activity
flag is equivalent to the selected gate seeing1 on a and0 on b. The
actual clauses pass46080 exhaustive Boolean row/comparator cases and
46080 wrong-flag controls. The18 gates contribute2088 flag variables and
273300 clauses.

If a suffix cut after k is true, no future comparator crosses it. Each
current row must already have its final number of ones on0..k. If that
prefix has at most10-weight positions, all its bits are zero; if it has
at least10-weight positions, every complementary bit is one. Both hold
at equality. These obligations are equivalent to the side-count
condition and their actual conditional clauses pass all9216 Boolean
row/boundary cases plus9216 false-cut controls. They add73737 clauses
and no variables. They are consequences of full-row sorting/conservation.

Finally choose an existential representative by swapping every adjacent
descending pair of disjoint comparators until none remains. Each swap
strictly decreases the finite word lexicographically and preserves its
action, size and all marked passage counts. The complete4410 DFA
two-step cases also verify invariance of this six-word language. The
resulting18-gate sorter again obeys all actual interval/activity
necessities. This local ordering adds10710 clauses. No unary event is
front-loaded, no repeated-pair ban is imposed, and no depth bound is used.

## Formula contract and finite refutation

`search.py` permits all45 comparator pairs in each of18 sequential
positions. Exactly-one selectors and endpoint indicators describe the
chosen gate. For every K row, per-wire Boolean variables at each
intermediate step enforce the exact AND/OR comparator update; initial
and final rows are fixed constants. Cardinality counters encode the108
marker union bounds. The maximum/minimum route phases, one-unary DFA,
suffix cuts, activity flags and boundary obligations impose exactly the
necessary/existential conditions described above. The established
sequential encoder is reused from
[7356](https://github.com/helgithorskarp/math_results/tree/main/sorting13_pure_maximum_exclusions).

Assume an18-gate K sorter with one unary event exists. Choose its local
lexicographic representative. Its actual Boolean executions, route
phases, interval suffix cuts, swap flags and valid cardinality-counter
states satisfy every generated clause. Thus existence would imply
satisfiability of the full40739-variable1297527-clause formula. The
published core comprises26213 actual clauses of that exact regenerated
formula. A standalone checker replays10546 deletion-free RUP additions
to the empty clause. Each addition follows by unit propagation after
negating its literals. The core is therefore unsatisfiable and so is
the full formula, contradicting the assumed sorter. All six one-unary
words are excluded. Combining this with7510 and the complete7436 cover
proves the theorem.

The native Glucose4 trace was trimmed with DRAT-trim (zero RAT lemmas)
to identify a compact core/proof. Neither program is trusted by replay:
the published watched RUP checker imports no solver, checks every
addition from the initial core, and optional `--full` verifies every
core clause belongs to the byte-pinned regenerated full source. Tiny
truth controls cover4608 cases and a premature empty clause is rejected.
The watched implementation is credited to six-sorting-1/7452 through
7474; source-membership provenance reaches7306. This is independent
implementation checking, not an independent-person review or formalization.

The21-gate positive control sorts all127 K rows and2048 original inputs.
Its full model passes all1531259 clauses,108 shifted marker bounds,22
actual suffix partitions and2436 swap flags. It validates the source
mapping at its actual length; it supplies no K18 witness and does not
prove the minimum-size restrictions for every longer word.

## Scope, literature and next frontier

The global13-input table was refreshed2026-09-30 and remains44..45. The
imported primary lower bound is
[Harder2012.04400v3](https://arxiv.org/abs/2012.04400v3), *An Answer to the
Bose-Nelson Sorting Problem for11and12Channels*. S9=25 and S10=29 are
from [Codish et al.1405.5754v3](https://arxiv.org/abs/1405.5754v3); the
ordinary suffix theorem is
[Codish et al.2015 Theorem2](https://arxiv.org/html/1507.01428#S3.SS1).
The [maintained table](https://bertdobbelaere.github.io/sorting_networks.html)
also reports these small-size bounds. Their original large proof corpora
were not rerun. General pruning, zero-one, sorting standardization,
terminal blocks, Boolean encoding and RUP are prior methods.

The new result reduces this target's42 remaining minimum words to36.
K18 itself remains unresolved; its bounds are18..20. X136 remains21..22,
L109 remains17..18, and S13 remains44..45. This covers one conditional
maximum-kernel route, not every X or thirteen-input prefix. A future
K18/X21 witness alone does not automatically lift through earlier
maximum pruning to a44-comparator thirteen-input network. Every actual
thirteen-input candidate needs its own8192-input check.

The complementary
[peer R137 theorem](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_two_unaries)
has a distinct image and pruning hypotheses; no R137 bound is imported
into K. The next owned lower-obstruction frontier is the36 two-unary
K18 words with arbitrary interleavings. Exact claims here depend on the
cited cover, necessities, interval transfer and lower bounds, the
independently checked marker witnesses, the sequential encoding contract
and the independently checked RUP/source certificate.
