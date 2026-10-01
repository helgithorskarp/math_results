# Scope and proof

Author/executing agent: **six-sorting-2, researcher**.

## The precise result

Number thirteen channels 0..12 and nine channels 0..8. An ordinary comparator
`(a,b)`, with `a<b`, sends the smaller value to `a`. Encode a Boolean vector by
`sum(bit[i]*2**i)`; the sorted nine-bit vector of weight w is
`((2**w)-1) << (9-w)`.

Take the following fixed 22-gate thirteen-wire prefix G:

```text
(0,12) (1,10) (2,9) (3,7) (5,11) (6,8)
(1,6) (2,3) (4,11) (7,9) (8,10)
(0,4) (1,2) (3,6) (7,8) (9,10) (11,12) (4,6) (5,9)
(10,12) (0,5) (0,1)
```

On internal eleven-wire indices 0..10, take

```text
E = (2,10) (1,6) (3,4) (0,2) (1,3) (0,1)
    (7,10) (5,9) (8,10) (9,10).
```

Shift every endpoint of E upward by 1 and append it to G to obtain the fixed
32-gate thirteen-wire prefix A. Let Y be the projection of its full 8192-element
Boolean output image onto original channels 2..10, renumbered 0..8. The complete
set Y has 61 rows. It is exactly image 56 in
`sorting13_B11_ten_event_loop_postponement/certificate.json`; its class code is
`410718871845198803939197429219333`. All parent input files are hash-pinned.

**Claim. Every ordinary nine-wire network sorting Y uses at least 13
comparators.** No selected depth is assumed. Consequently this one ten-event
class admits no B11 C22 word, by the parent's proved loop-postponement theorem.
The parent 417 necessary classes become 416: 89 ten-distinct, 297 eleven-distinct,
30 eleven-repeated. The 89 ten classes have 88 distinct images and 87 literal-index
inclusion-minimal images. This result covers no other thirteen-wire prefix and
does not resolve the global 44-versus-45 gap. The eleven-event classes are not
front-loaded by analogy.

## From a hypothetical completion to necessary constraints

The scalar checker independently evaluates A on every thirteen-bit input,
checks its two smallest values are held at 0/1 and its two largest at 11/12,
and reconstructs Y exactly. Therefore any ordinary twelve-gate sorter T of Y
lifts to the full 44-gate sorter A followed by T on original 2..10. If a sorter of Y
has fewer than 12 gates, append ordinary comparators after its sorted outputs
to make 12; these fix every sorted row. Thus exclusion of exact size 12 also
excludes all smaller sizes. This bridge is essential: the following full-input
sorting-network conditions do not apply to an arbitrary partial-input image
without such a lift.

We use the established size lower bounds

```text
S(0)..S(12) = 0,0,1,3,5,9,12,16,19,25,29,35,39.
```

In particular S11=35 and S12=39 are established by
[Harder](https://arxiv.org/abs/2012.04400v3), while S9=25 and S10=29 are from
[Codish, Cruz-Filipe, Frank and Schneider-Kamp](https://imada.sdu.dk/u/lcf/pubs/paper26.pdf).
The small-input values and the standard marked-value deletion principle are
imports, not claimed new.

For an original thirteen-bit input x, mark either its k zeros as minima or its k
ones as maxima. Delete the marked wires through the full sorter, rerouting
unmarked values at marked/unmarked comparators. Every comparator touching a
marked value is deleted; the remaining network sorts the 13-k unmarked inputs.
If D is the deletion count then `44-D >= S(13-k)`. This holds for each of the 8190
nonconstant original assignments. Let D_A(x,m) be its count through A and let
r be its projected nine-bit output. Every completion must obey

```text
tail_touches(r,m) <= min_x [44 - S(13-k(x,m)) - D_A(x,m)],
```

where the minimum ranges over original assignments giving r, separately for
the two polarities m. The scalar checker computes all 122 row/polarity cap
records from the original inputs; 100 caps are below 12 and constrain the tail.
This pooling does not lose any necessary inequality, because the tail
trajectory and its deletion count depend only on the current nine-bit row.

There are twelve mandatory two-marked clamped domains in the parent activity
certificate, graph 7944. For each, exactly 9 comparators of A are deleted and
the two marked values end at 0/1 or 11/12. Every tail comparator on 2..10 is
retained. Pruning a hypothetical full 44 network therefore gives a 35-gate
eleven-wire sorter. Every retained comparator must be active on the clamped
domain: otherwise remove it and obtain an eleven-wire sorter of at most 34
gates, contradicting S11=35. This forces every one of the twelve tail gates
to swap some row of each mandatory domain. The scalar checker reconstructs all
24576 clamped Boolean assignments and verifies the marked route and deletion
count using distinct actual values. It does not infer activity from a
relaxation or from the size bound on nine channels.

We may normalize a twelve-gate word by swapping an adjacent inverted pair of
disjoint comparators until no such pair remains. Each swap strictly decreases
the word in a finite lexicographic order, so this process terminates.
Disjoint comparators commute on arbitrary values. Each sees the same two
values in either order; passage counts and existence of an active witness in
each clamped domain are consequently preserved. The CNF uses only these
adjacent disjoint-pair prohibitions, not a fixed event order beyond the proved
parent E;T normalization.

Finally import Theorem 11 of
[Codish, Cruz-Filipe and Schneider-Kamp, Sorting Networks: the End Game](https://arxiv.org/abs/1411.6408).
For a sorting network without redundant comparators, a comparator joining
distinct connected components of the remaining suffix joins adjacent blocks.
Backward induction shows that every suffix component is an interval of
channels: singleton components start the induction, an internal edge keeps a
block unchanged, and an edge joining distinct adjacent interval blocks merges
them into one interval. All tail comparators here are nonredundant by the
activity premise. Remove any redundant prefix comparators if necessary;
their removal preserves the computed function and every tail activity witness.
Apply the established theorem to the resulting sorter. The four held extreme
channels are isolated in each tail suffix, so the same interval condition
holds on the nine projected channels.

Use one layer per comparator solely to state this theorem. This serialization
is available for every comparator word and imposes no extra depth bound.
If boundary[t,i] states that the suffix starting at t connects channels i,i+1,
then its terminal value is false and

```text
boundary[t,i] = boundary[t+1,i] OR (gate[t] spans the cut i,i+1).
```

For a chosen gate (a,b), at most one of the boundaries a..b-1 in the following
suffix can be false. Otherwise the gate would skip a distinct intervening
component. These constraints allow gates inside one component. The interval
condition is an attributed literature consequence, not a new theorem of this
submission. The independent `controls.py` graph/bit recurrence comparison checked
every one of 47989 nine-wire words of length at most 3 and 708 nonredundant
four-wire full-input sorters of lengths 5/6. The partial-image counterexample
`100 -> 001` via (0,2) confirms why full-input provenance is required.

## Exact Boolean encoding and its independent audit

For each of 12 slots, choose exactly one of all 36 pairs. Endpoint-use variables
are equivalent to the corresponding disjunction of selected pairs. For each
of 51 unsorted rows in Y, allocate the nine bits at every stage and one shared
swap variable per slot. Conditional on the chosen pair (a,b), three clauses
give `swap <=> (bit[a] AND NOT bit[b])`. At every channel six clauses give

```text
new_bit = old_bit XOR (used_channel AND swap).
```

Initial and final units fix the row and its sorted target. The ten already
sorted rows are constants, since every ordinary comparator fixes them.

For every active passage cap allocate twelve hit flags. Whenever a used
endpoint has the marked Boolean value, a one-sided implication forces that
slot's flag true; impose their sum at most the cap. A genuine feasible word
sets each flag to its actual touch indicator, so these one-sided clauses
cannot exclude a mathematical candidate by requiring an overcount. Activity
clauses are the disjunction of the relevant row-swap variables at each slot.
Sorted constant rows contribute no swap witness. The remaining clauses encode
the disjoint normalization and the attributed suffix conditions just proved.

The independent `audit_encoding.py` imports neither the encoder nor PySAT.
It reconstructs every non-cardinality clause in order and verifies the whole
variable allocation and section counts. It isolates each cardinality block's
fresh auxiliaries. After fixing its flag inputs the block is Horn, so least
Horn closure decides whether auxiliary values extending those flags exist.
It exhaustively checks all 4096 twelve-flag assignments for each distinct
at-most shape against the exact integer count. For each exactly-one gate
shape it checks all 36 singletons, zero and all 630 pairs; every at-most clause
has only negative flag literals, so rejection of every pair also rejects all
larger flag sets. Across the distinct shapes 45723 assignments are checked.
All 112 blocks are audited, with caching only after identical normalized clause
shapes have been established. Fresh auxiliary sets never interact between
blocks. This gives existential auxiliary coverage for every mathematical word
satisfying the necessary conditions; there is no reliance on the SAT library's
encoding correctness for that bridge.

The local Boolean kernel was exhaustively truth-table checked, and the genuine
36-gate insertion positive control satisfies every one of 385050 clauses of its
control formula and sorts all 8192 original thirteen-bit inputs. These controls
do not replace the written universal argument above. The supplied scalar and
clause audits together align that argument with the exact generated formula.

## Finished proof replay

The full target formula has 11598 variables,125802 clauses andSHA256
`f114e2136e50c2d6a44b8091610940e7ec86839ff354ad03606e584828a510a7`.
Glucose 4 returnedUNSAT within the fixed 30000-conflict/40-second limits. This
decision alone is not used as a proof.

Native `drat-trim` independently verified the actual certificate, extracting
26257 original core clauses and 7390 RUP additions, with zero RAT lemmas.
The separate published Python watched-literal RUP implementation, credited to
six-sorting-1, independently replayed every addition and checked that every
core clause occurs in the exact full formula. It first rejected a premature
empty clause. Its exhaustive tiny truth controls cover 4608 tests. Deletions
are ignored, retaining a stronger database of clauses already entailed by the
original core; the final empty clause therefore proves that core and its full
formula unsatisfiable. The checker imports no SAT solver.

Combining replayed UNSAT with complete necessary-condition coverage excludes
every ordinary twelve-gate sorter of Y, at arbitrary allowable depth. The
padding argument excludes all smaller sizes. The parent loop-postponement
result then excludes this original ten-event class, including every effective
event order and loop interleaving in it. No 13-gate witness, all-class B11
exclusion, or arbitrary-prefix exclusion follows from this result.

The compact public record includes exact trace hashes. Bulky traces and cores
are generated locally from the pinned source and are intentionally outsideGit;
reproduction takes seconds and requires no private fixture. All mathematical
reductions and literature imports are explicit and unformalized. Distinct
algorithms of this researcher provide the reported checks; no independent
human/agent reviewer verdict is asserted or requested.


Complementary work refreshed before this claim: six-sorting-1's
[one-preparation-block result](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_single_preparation_normal_form/PROOF.md),
graph8126, source9e233924e79cc8a4b52001cda87cc8f56db3003c, reduces the entire
unary eleven-event branch to one preparation block and supplies five
nine-wire tails for repeated-(1,2) class13. It excludes no class and leaves
this ten-event exclusion disjoint. It is cited for the next research frontier,
not imported as a premise of the61-row proof.
