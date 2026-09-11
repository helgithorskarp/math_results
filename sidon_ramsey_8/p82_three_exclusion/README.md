# The P82 three-eleven profile is excluded

**Every partition of `[82]` into eight integer Sidon sets must have profile
`11^2 10^6`.** This computation excludes the entire other profile
`11^3 10^4 9` left by the [global P82 profile theorem](../p82_profiles/README.md).
Both complete methods close all **2,604 nonempty anchor cases**, comprising
**6,773,441 anchored triples**. Including the 1,417 packing-empty cases,
the traversal covers all 4,021 eligible canonical cases.

P82 itself remains undecided. The [P83 exclusion](../p83_exclusion/README.md)
and the published P80 partition still give **81 <= SR(8) <= 83**. The
remaining P82 question has a proved global cover of **3,840 nonempty cases
and 1,142,922 anchored pairs**, in `../p82_profiles/cases_2.csv`.

The arithmetic is ordinary integer addition. Sidon means distinct unordered
pair sums **including diagonal sums**. Programs use `0,...,81`; translate
by one for `[82]`. This result does not require a fixed seed partition or
a bound on how many seed classes can change.

## Reproduction and evidence

Requirements are Python 3.11 or later, its standard library, GCC with C++20
and `__uint128_t`, and POSIX named pipes. The recorded environment uses
Python 3.11.2 and GCC 12.2.0. Solver software is not needed for verification.
Run Python without `-O` or `PYTHONOPTIMIZE`; assertions perform proof checks.

To regenerate the prerequisite catalogs and their profile proof, then run
this computation, use a fresh directory outside the repository:

```bash
python3 reproduce.py --work /tmp/p82-three --jobs 5 --sanitizers
```

Alternatively reuse the outputs of a completed P82 profile reproduction:

```bash
python3 ../p82_profiles/reproduce.py --work /tmp/p82-profiles --jobs 4 --workers 6 --sanitizers
python3 reproduce.py --inputs /tmp/p82-profiles --work /tmp/p82-three --jobs 5 --sanitizers
```

The input masks are checked against the published prerequisite hashes,
and both complete ten catalogs are also compared byte for byte. Each
catalog is validated directly on loading. Five jobs mean five paired
traversals: ten search processes and five lightweight audit processes.
The recorded full traversal took 4777.83 seconds at most per pair;
rebuilding the prerequisite profile proof is additional work. A preliminary root-cache-only wrapper replay on all cases numbered at
least 2,000 took 74.80 seconds and checked 15,030 triples, including its
requested sanitizer controls. The final source was subsequently replayed
on the complete frontier with all controls, including the parent cache.
The full run reused the independently regenerated prerequisite catalogs;
it was not a second fresh reproduction of the entire prerequisite proof.

The full result is `verified: true`, with:

| Quantity | Exact value |
|---|---:|
| Anchored triples | 6,773,441 |
| Recursion calls per method | 223,793,348 |
| Candidate options per method | 217,019,907 |
| Nonempty query records per method | 61,586,509 |
| Final nine-set checks per method | 92,498 |
| Partitions found | 0 |
| Exact compared bytes per method | 7,816,140,848 |

`cases_3_completed.csv` contains every case count. `expected.json` and
`validation.json` give the compact result, per-shard stream hashes, input
hashes, controls, and validation scope. `terminal_examples.json` illustrates
failed final nine-sets. The complete terminal list stays in the work
directory. Full candidate streams are compared directly and then discarded;
they are not stored or committed. Hashes record provenance: they do not
replace the exact byte comparison.

`--minimum K` reproduces only the complete canonical case range `K,...,4020`;
it is a diagnostic option and reports its restricted scope. The full theorem
uses the default `K=0`. Sharding changes the order of whole cases but neither
the case counts nor the total trace length.

## Exhaustive reduction

The imported P82 theorem establishes the following facts afresh for this
parameter: there are 8,214 eleven-sets, 17,249,580 ten-sets, and no twelve-set;
only the two stated size profiles remain. For the 82 nonnegative integer
weights in `../p82_profiles/weights.txt`,

```
W = 30,884,468,   M = 4,000,000,   C9 = 3,776,423.
```

Every ten- or eleven-class has weight at most M, and every nine-class has
weight at most C9. The nine-cap enumeration has 431,916,048 sets; no new
nine enumeration is needed here because that cap is a stated dependency.

Three eleven-classes of a hypothetical `11^3 10^4 9` partition are disjoint
and have total weight at least `W-5M = 10,884,468`. The complete imported
catalog and reflection convention give the 6,773,441 anchored triples.
Reflection is `x -> 81-x`. The least used reflection orbit is represented
in its canonical orientation; all other selected row IDs exceed its even
anchor row. Every partition can be reflected into this form. This is a
cover, and is not asserted to select exactly one representative of every
reflection orbit.

The two packing implementations use nested loops and a recursive candidate
intersection, respectively. They visit every qualifying triple. Processing
case indices in descending order only changes scheduling. For each triple,
its 49-point complement D must admit `10^4 9`.

At a recursive state with r ten-classes and the nine remaining, let U be
the preceding ten-class weight, initially M. Ordering the ten-classes by
nonincreasing weight loses no partition. Prune if

```
w(D) > r U + C9.
```

Otherwise enumerate **every** ten-set A contained in D with

```
max(0, ceil((w(D)-C9)/r)) <= w(A) <= U,
```

then recurse on `D\A`, replacing U by `w(A)`. After four ten-classes,
the residual nine is tested directly. The nine-class is never required
to weigh less than the preceding ten: its separate size cap is used.
All complete searches fail.

## Exact residual catalogs

Queries initially use the complete global ten catalog. For a 49-point root
D0 define

```
L = max(0, w(D0) - 3M - C9).
```

Every ten-class in a completion has weight at least L: the other three tens
and the nine have total weight at most `3M+C9`. The program therefore may
cache all ten-sets contained in D0 with weights between L and M.

In fact this cache preserves the entire candidate stream of the recurrence,
not only successful completions. At a state with r tens left, removed
classes weigh at most `(4-r)M`, so the query lower bound is at least

```
(w(D0) - (4-r)M - C9) / r.
```

For an unpruned root `w(D0) <= 4M+C9`, this is at least
`w(D0)-3M-C9`. Every recursive domain is a subset of D0. Thus every candidate
that the global catalog would return also occurs in the residual catalog.
The cache is constructed on the 33rd ten query in a root; this deterministic
performance choice has no mathematical effect. Every cached row is checked
again for cardinality, order, Sidon property and weight.

There is also exact reuse across triples sharing their first two eleven-sets
A and B. Let E be their 60-point complement, and put b = w(B). The third
selected eleven-set C has weight at most b, because row IDs are ordered by
nonincreasing weight. Define

```
Lp = max(0, w(E) - b - 3M - C9).
```

For every root D = E\C in this family, `L(D) >= Lp`. On the third root-cache
preparation in a family, the program stores the complete sorted vector of
ten-sets in E with weights in `[Lp,M]`. Later root catalogs are obtained by
filtering this vector for containment in D and the sharper lower bound
L(D). Filtering gives exactly the same root catalog as querying the global
catalog. The parent vector is reset whenever the pair `(E,Lp)` changes.
Its construction trigger is a performance choice and omits no case.

The two query implementations are a compressed binary radix tree and
weight-ordered incidence bitsets. They share the exact recurrence and cache
cutoff proof, but implement subset queries differently.

## Validation and trust boundary

Each build passes 5,048 definition-level controls, including 522 negative
cases and positive mixed-size profiles. The changed cache produced the
same 80 control output files as the published baseline, byte for byte.
A complete 12,072-triple benchmark case also produced identical case counts,
175,435,344-byte candidate streams, and all 7,775 final nine-set checks,
with no cache, with root caches, and with the final two-level cache, for both catalog methods.

Another 20 positive control decisions per build explicitly exercise the
parent-vector cache and its reuse, including forced early activation of its
performance counter. The two-level and global queries give identical
2,490,512-byte streams on the ten-domain fixture for each method. Address
and undefined-behavior sanitizers also pass these controls.

During the full traversal, each paired stream is compared byte for byte.
The common stream is sent to `audit_stream.cpp`, which independently parses
every record, checks the domain and profile, verifies candidate order and
containment, recomputes the weight interval, and checks all 55 pair sums
of every ten-set. Its controlled corruption tests reject truncated records,
duplicate candidates, wrong weight bounds and actual sum collisions.
`verify.py` checks the complete case cover, all terminal partitions and
failed nine-sets, and the identity `calls = triples + options` using Python
integers. Every emitted option occupies at least 16 bytes, so the exact
Python byte counter gives a separate upper bound on the number of calls.
This also checks that all relevant counts fit unsigned 64-bit storage.

These are exact computer-assisted results, not proof-assistant theorems.
Trust remains in the written reductions, imported enumeration completeness,
shared recurrence, compiler/runtime, and checker implementations. The methods
do not constitute completely independent implementations of the whole proof.
No independent external review of this new exclusion is claimed here.

## A global obstruction to class-size weight bounds

`fractional_profiles.json` contains exact positive fractional partitions
with both profiles `11^3 10^4 9` and `11^2 10^6`. The certificates use 43 and
42 reflection-averaged Sidon-set rows, respectively. A row of rational weight
q assigns q/2 to the displayed set and q/2 to its reflection. Every one of
the 82 point equations equals 1 exactly, and the total coefficients of each
class size equal the stated multiplicities. `fractional_check` verifies
these facts with Python rational arithmetic and direct pair sums.

Consequently, for **any real point weights** and valid uniform caps Ck on
all Sidon k-sets, the weighted total W satisfies

```
W <= 3 C11 + 4 C10 + C9,   and   W <= 2 C11 + 6 C10.
```

Thus global class-size weight caps alone cannot exclude either profile.
The three-eleven exclusion above uses disjointness and compatibility in
addition to weight bounds. These fractional certificates are not integer
partitions and do not decide the remaining balanced case. They were found
by floating-point linear programming, then reconstructed and checked
exactly; solver status is not a proof premise.
