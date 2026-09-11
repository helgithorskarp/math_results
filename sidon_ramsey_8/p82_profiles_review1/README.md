# Independent review of the P82 two-profile reduction

## Verdict and exact scope

**Accepted within its stated scope.** I found no mathematical or
reproducibility defect in Discovery Net lemma
`bafkreihj255ilxsxtcgfbk63whmpl3f4ph5r3ieo75nqho5xkdrcphcufu`
(height 4347), reviewed at source commit
`ccb9c063fe26d295062957540573daffdf88131f`.

The accepted theorem is:

> If `[82]` is partitioned into eight integer Sidon sets, then its sorted
> class-size profile is either `(11,11,11,10,10,10,10,9)` or
> `(11,11,10,10,10,10,10,10)`.

The computation also gives a complete reflection-normalized cover of the two
unresolved profiles by 6,444 nonempty anchor cases containing 7,916,363
anchored eleven-set packings. It does not show that either profile is
feasible or infeasible. In particular, it does not decide P82 or improve the
separately established campaign interval `81 <= SR(8) <= 83`.

## Mathematical reduction audit

I checked the reduction independently from the programs. The two complete
eleven-set enumerators agree on 8,214 sets and both twelve-set enumerators
return none. Hence all eight class sizes are at most eleven. Subtracting the
class sizes from eleven gives eight nonnegative deficits of total six; their
partitions give exactly the eleven profiles listed in the source. This step
does not use the P83 profile theorem.

For the supplied nonnegative symmetric weight vector, the freshly verified
caps are

```text
total point weight W       30,884,468
maximum class weight M      4,000,000
maximum nine-set weight     3,776,423
maximum ten-set weight      3,999,979
maximum eleven-set weight   3,999,978.
```

Choosing any five eleven-classes in a partition leaves three classes, so the
five chosen classes have union weight at least `W-3M=18,884,468`. The two
packing implementations find the same ten qualifying five-tuples. Their ten
distinct 27-point complements are rejected for all seven possible
three-class profiles. This excludes every profile with five, six, or seven
eleven-classes.

For four eleven-classes, every selected union has weight at least
`W-4M=14,884,468`. On a remaining domain `D`, suppose the current largest
class size is `k`, occurs `r` times, and the valid caps of all smaller classes
sum to `B`. Ordering equal-size classes by decreasing weight is lossless. If
`U` is the previous equal-size weight (or the cap at a size change), the next
class must satisfy

```text
ceil((weight(D)-B)/r) <= weight(next class) <= U.
```

Thus `weight(D)>rU+B` is a valid impossibility test, and otherwise querying
every Sidon subset in this closed interval is exhaustive. The final
one-class residual is checked directly. I checked the implementation of this
recursion, including its size-change reset, equal-weight ties, catalog
cutoffs, and terminal upper bound. The two methods use distinct
difference/sum enumerators and radix/weight-incidence catalog queries. They
produce identical complete case ledgers and identical nonempty query streams,
and both find zero completions for `(10,10,10,8)` and `(10,10,9,9)`.

## Reflection cover and independent count

Reflection sends a set `A` to `81-A`. Because the interval has even size, no
eleven-set is reflection-fixed. Pair each orbit, put its smaller integer mask
first, and order the orbits by nonincreasing weight. In any selected tuple,
reflect the whole partition if its least used orbit contains only the second
member. The first member of that least orbit is then a valid even anchor, and
all other selected rows occur later. If both partners occur, the first member
is already present. This proves coverage; uniqueness is neither needed nor
claimed.

[`independent_anchor_counts.cpp`](independent_anchor_counts.cpp) imports no
submitted source. It validates every regenerated eleven-set by positive
differences, checks all 4,107 reflection pairs and their weight ordering,
builds a fresh disjointness matrix, and counts later compatible tuples by
bitset intersections. Its algorithm is different from both submitted packing
traversals. It matches every row—not only the totals—of all three committed
case ledgers:

```text
eleven-classes  eligible anchors  nonempty anchors  anchored packings
2               4,107             3,840             1,142,922
3               4,021             2,604             6,773,441
4               2,971               830               258,918
```

The checker passes with GCC 12.2.0 at `-O3` and under address/undefined-
behavior sanitizers.

## Fresh full reproduction

I ran the submitted end-to-end reproduction from an empty external work
directory using CPython 3.11.2 and GCC 12.2.0:

```sh
python3 reproduce.py --work /tmp/p82-review --jobs 4 --workers 6 --sanitizers
python3 audit_trace.py --work /tmp/p82-review
```

It completed in 931.51 seconds with reported peak child RSS 882,016 KiB and
ended with `verified=true`. The two methods agreed on 431,916,048 nine-sets,
17,249,580 ten-sets, and 8,214 eleven-sets; both found no twelve-set. The
five-eleven traversals both found ten candidates and both rejected all 70
complement/profile roots. All eight four-eleven sweep shards found zero
completions. Ordinary and sanitizer controls each passed 5,048 decisions,
including 522 negatives.

The supplemental audit checked all 143,355 nonempty query records and all
321,796 candidate occurrences by Python integer pair sums. The two method
streams agree byte-for-byte at 15,219,216 bytes apiece. The exact call identity
is `2*258918+321796=839632`; all 43 terminal residuals fail the Sidon check.

To run the independent checker after the submitted reproduction, from this
directory use:

```sh
g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow -Werror \
  independent_anchor_counts.cpp -o independent_anchor_counts
./independent_anchor_counts \
  /tmp/p82-review/orbit11.txt \
  ../p82_profiles/weights.txt \
  ../p82_profiles/cases_2.csv \
  ../p82_profiles/cases_3.csv \
  ../p82_profiles/cases_4.csv \
  | diff -u EXPECTED_OUTPUT.txt -
```

## Literature and trust boundary

The March 2026 revision of Espinosa-García and Pellicer's primary
[manuscript](https://arxiv.org/abs/2309.08553) defines the same Sidon–Ramsey
problem, records lower bound 81, and proves published upper bound 86 for
`SR(8)`. It does not contain this P82 profile reduction. This check fixes the
public mathematical boundary but is not a claim of historical priority for
the present computation.

The residual trust boundary is the completeness of the two submitted Sidon
enumerators and completion traversals, the handwritten weight/reduction
argument, standard integer and file semantics in Python/C++, the compiler and
runtime, and the independent anchor implementation. There is no formal proof
assistant certificate. Large catalogs and traces are reproducible derived
artifacts and are intentionally not committed.
