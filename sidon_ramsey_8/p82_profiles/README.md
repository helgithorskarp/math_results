# A global two-profile reduction for P82

Every partition of `[82]` into eight integer Sidon sets has one of the two
class-size profiles

```
11,11,11,10,10,10,10,9
11,11,10,10,10,10,10,10.
```

Nine of the eleven initially possible profiles are excluded. The remaining
profiles have a complete cover by **6,444 nonempty canonical anchor cases**,
containing **7,916,363 anchored eleven-set packings**. Neither remaining
profile is asserted feasible or excluded. P82 and the exact value of SR(8)
remain open; the separately established campaign bound is `81 <= SR(8) <= 83`.

This is a fresh parameter-specific reduction. It does not import the P83
class profile or use the P83 exclusion as a premise. The P84 and P83 artifacts
are preserved. All points in the programs are zero-based, `0,...,81`; adding
one gives `[82]`. Sidon means that all unordered pair sums, including the
diagonal sums `2a`, are distinct. Equivalently, all positive differences are
distinct.

## Global size and weight bounds

Two complete enumerators, respectively using positive differences and fixed
endpoints with pair sums, find **8,214 eleven-sets and no twelve-set**.
Thus no larger class exists. The sorted eight-class profiles are precisely

| Number of eleven-classes | Remaining sizes | Status |
|---:|---|---|
| 7 | 5 | Excluded |
| 6 | 10,6; 9,7; 8,8 | Excluded |
| 5 | 10,10,7; 10,9,8; 9,9,9 | Excluded |
| 4 | 10,10,10,8; 10,10,9,9 | Excluded |
| 3 | 10,10,10,10,9 | Unresolved; complete case cover |
| 2 | 10,10,10,10,10,10 | Unresolved; complete case cover |

For another derivation of completeness, subtract each size from 11. The
eight nonnegative deficits sum to six. Enumerating the partitions of six
gives exactly these eleven possibilities. Empty classes are impossible,
since seven classes have total size at most 77.

Let `v` be the 84-entry vector in `../p84_profiles/weights.txt`, and set
`w_i = v_i + v_(i+2)` for `0 <= i < 82`. The supplied symmetric vector has

```
W = sum(w) = 30,884,468
max(w) = 444,444
M = 4,000,000.
```

The construction uses the earlier vector only as data. All necessary caps
are established afresh at 82:

| Class size | Complete count | Maximum weight |
|---:|---:|---:|
| 9 | 431,916,048 | 3,776,423 |
| 10 | 17,249,580 | 3,999,979 |
| 11 | 8,214 | 3,999,978 |
| 12 | 0 | — |

The two ten catalogs agree byte for byte; the two eleven enumerations agree
as sets, and every eleven-set is checked directly by pair sums. Two complete
nine-set enumerations agree on count and maximum; the nine catalogs are not
stored or compared entrywise. For sizes at most eight, `C_k = 444444*k`
is a direct bound. Use `C_9 = 3776423` and `C_10 = C_11 = M`.
Every class therefore has weight at most M.

## Excluding five or more eleven-classes

Choose any five eleven-classes in a hypothetical partition. Their union
has weight at least `W - 3M = 18,884,468`. Two complete weighted packing
traversals, using filtered lists and adjacency bitsets, find exactly **ten**
unordered choices meeting this condition. They agree on every tuple and
its catalog ordering. Their ten distinct complements each have 27 points.

All seven possible three-class profiles of 27 with maximum size 11 are
checked on every complement. These are exactly the remaining-size rows
obtained from the first seven profiles in the table. Both difference and
pair-sum subset enumeration, with the valid caps above, reject every
completion. There are 70 profile roots, 20 unpruned subset queries, and no
candidate in any such query. Consequently every profile with at least five
eleven-classes is excluded.

## Reflection cover, without a seed restriction

Pair every eleven-set A with its reflection `81-A`. There are no fixed
sets: a reflection-invariant subset of this even interval has even size.
The representative is the smaller integer membership mask. Order the
4,107 orbits by decreasing weight and then by representative mask, listing
each representative immediately before its reflection. Rows `2j` and
`2j+1` form orbit j.

Given any partition with a specified number t of eleven-classes, reflect
the entire partition, if necessary, so that its least used orbit contains
its representative. Use that even catalog row as the anchor, then list the
other selected eleven-rows in increasing order. All lie after the anchor;
the anchor's reflected partner is allowed. This argument covers every
partition. It need not count every reflection orbit exactly once when both
orientations of the least orbit are used.

Every selected t-tuple must be disjoint and have weight at least
`W-(8-t)M`. An anchor is eligible only if t times its weight reaches this
threshold. Two complete traversals, explicit nested packing loops and
recursive compatibility lists, give:

| t | Weight threshold | Eligible anchors | Nonempty anchors | Anchored packings |
|---:|---:|---:|---:|---:|
| 4 | 14,884,468 | 2,971 | 830 | 258,918 |
| 3 | 10,884,468 | 4,021 | 2,604 | 6,773,441 |
| 2 | 6,884,468 | 4,107 | 3,840 | 1,142,922 |

An additional Python audit checks *all* unordered eleven-set pairs before
reflection, with no packing DFS or pruning by a partial weight bound. It
finds 2,285,136 pairs, of which 708 are reflection-fixed. In every anchor
case, `(unreflected count + fixed count)/2` agrees with the two-class packing
ledger, giving 1,142,922 anchored pairs in total.

## Excluding both four-eleven profiles

For each of all 258,918 anchored four-tuples, the 38-point complement must
have profile `(10,10,10,8)` or `(10,10,9,9)`. The following complete recursion
checks both profiles, and also explains its pruning.

Let D be the remaining domain. Write the remaining profile in decreasing
size order, let k be its largest size, and suppose that size occurs r
times. Let B be the sum of the valid caps of all smaller classes. Order
classes of each *equal size* by decreasing weight. If U is the weight of
the previously selected class of size k, or C_k at the beginning of a size
group, then the heaviest remaining k-class has weight in

```
max(0, ceil((weight(D)-B)/r)) <= weight(A) <= U.
```

If `weight(D) > r*U+B`, no completion exists. Query every Sidon k-subset in
the interval, remove it, and recurse. At a size change reset U to the new
size's cap. Ties are all retained. A one-class residual is checked directly
for the Sidon property and the current weight bound. These rules remove no
possible completion.

For ten-set queries on domains with more than 30 points, method 0 uses a
compressed binary radix tree on the *complete* ten catalog; method 1 uses
weight-ordered incidence bitsets. There is no heavy-set truncation. Smaller
domains and other class sizes are enumerated directly, by positive
differences in method 0 and fixed-endpoint pair sums in method 1. Every
option list is sorted by its membership mask. A full witness would be
returned and checked; none occurs.

Both methods complete all cases and agree on the full case ledgers and
all nonempty query streams, byte for byte:

```
packing roots                258,918
profile roots                517,836
recursive calls              839,632
subset queries               809,167
candidate occurrences        321,796
terminal Sidon checks             43
completions                        0
query bytes per method    15,219,216.
```

All 43 terminal records are also checked using direct Python pair sums.
The supplemental trace audit decodes every emitted query using Python
integers, checks each candidate's cardinality, containment, Sidon property
and weight interval, and independently counts all candidate occurrences.
Each non-root recursive call corresponds to one emitted candidate. Thus
the exact call count is `517836 + 321796 = 839632`. In particular the
64-bit counters do not conceal overflow. Packing-counter bounds follow
already from choosing at most five rows out of 8,214; masks occupy 82 of
128 bits, and all weight arithmetic is below 2^31.

## Exact remaining frontier

`cases_2.csv` and `cases_3.csv` include *every* eligible anchor, including
packing-empty cases. Rows with positive `packings` are precisely the 6,444
nonempty cases in the stated cover. The case index is the eleven-orbit
index in the reproducibly regenerated catalog.

A t=2 case asks for its anchor, one later disjoint eleven-set, and six ten
classes covering the complement. A t=3 case asks for its anchor, two later
disjoint eleven-sets, four tens and a nine. Selected eleven-rows obey the
stated weight threshold. Any case witness is a P82 partition, and every
P82 partition has an image in this case cover. No case with a positive
packing count is asserted feasible merely from that count.

The t=3 completion search is deliberately not a proof premise of this
package. Preliminary global runs exposed a much greater query cost there.
They were stopped at this completed profile-reduction boundary. Improving
the compatibility queries for the full three-eleven profile is the next
concrete step. Fixed-seed and local-neighborhood searches play no role.

## Reproduce and trust boundary

Use CPython 3.11 or later and GCC with C++20 and `__uint128_t` support.
Tested with CPython 3.11.2 and GCC 12.2.0. All code uses the Python and C++
standard libraries. No optimizer, SAT solver, floating-point tolerance,
external catalog or network access is required for verification.

From this directory:

```bash
python3 reproduce.py --work /tmp/p82-profiles --jobs 4 --workers 6 --sanitizers
python3 audit_trace.py --work /tmp/p82-profiles
```

Keep the work directory outside the repository; use a fresh directory for
independent runs. The first command regenerates all catalogs, maxima,
packings and decisions, runs the controls, and requires equality with the
compact expected records. The second independently reads the complete
query streams. Assertions are required; both scripts reject Python `-O`.
Each ends with `"verified": true`.

Ordinary and address/undefined-behavior sanitizer builds each pass 5,048
control decisions, including 522 negative decisions. These include complete
small-domain checks against definition-based exact cover, positive examples
for all seven 27-point profiles, and two translations of known
38- and 49-point mixed-profile partitions with complete local ten catalogs.
The previously published 80-point partition is checked only as a control
and lower-bound witness.

The two traversals share the written reductions, weights, orbit convention
and compiler/runtime. Their agreement is not a proof-assistant formalization
or an external review. Completeness of the implemented enumerators and
query structures remains part of the computer-assisted trust boundary.
All large catalogs, binaries, full query streams and full terminal logs are
regenerated outside Git; source, compact case ledgers, four terminal
examples, validation metadata and hashes are retained here.

The fresh complete reproduction finished in 949.382 seconds,
using four shards per method and at most six worker processes. The largest
reported child-process resident set was 882,016 KiB.
The supplemental query-stream audit passed on the fresh output. These are
observed run measurements, not runtime guarantees.
