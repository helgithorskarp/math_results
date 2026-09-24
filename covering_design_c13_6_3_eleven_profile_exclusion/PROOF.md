# Exact exclusion of the (11,10,9^11) profile

Let a `(v,k,t)` covering be a family of distinct `k`-subsets of a `v`-set
containing every `t`-subset in at least one member. Write `d(x)` for the
number of blocks containing `x`, and `lambda(x,y)` for the number containing
both `x` and `y`.

**Theorem.** A twenty-block `(13,6,3)` covering cannot have point degrees
`(11,10,9^11)`.

The theorem is conditional only on the established mathematical input
described below and the correctness of the exhaustive implementations.
Its finite computation is complete, with no unknown or limited cases.

## 1. Imported local classification

Deleting a point `x` from every block through it gives its point link.
Every point link of a triple covering covers all pairs on the other twelve
points. In particular, a point of degree nine has a nine-block `(12,5,2)`
link. Such covers have been classified into 107 isomorphism classes in
the [preceding contribution](../covering_design_c12_5_2_classification/).
Every point of every such link has degree between three and five.

`LINKS.json` extracts all 107 representatives and the fields used here from
that contribution's `CATALOGUE.json`. The prior classification, including
its completeness proof and imported maximum-degree-five theorem, is part
of the trust boundary. The present program directly checks each imported
cover and the automorphisms used, but does not repeat the classification.

It follows that

`lambda(x,y) <= 5` whenever `d(x)=9`.

This is a bound on pair multiplicity. We use no bound of two on triple
multiplicities and impose no bound of five on a pair of high-degree points.

## 2. There is a marked link with a degree-five high point

Suppose that a cover with the forbidden profile exists. Denote the points
of degrees eleven and ten by `h` and `q`; the other eleven points are low
points, each of degree nine. Put `c=lambda(h,q)`. Since `c <= d(q)=10`,

`sum_{x low} lambda(h,x) = 5d(h)-c = 55-c >= 45`.

Every summand is at most five. If they were all at most four the sum would
be at most 44. Hence there is a low point `p` with `lambda(h,p)=5`.
Fix one such point and label it `12`. Its link is a catalogue member in
which `h` has degree five. Mark the distinct point `q` as well.

The primary enumeration takes one representative of each degree-five point
orbit (56 choices over the catalogue), and then one representative for `q`
under the automorphism stabilizer of `h`. This gives 442 roots. Choosing a
single `p` of the stated kind loses no possible global cover.

In the first link, choose a point `r` other than `h,q` of largest link
degree. Such a point has degree at least four: otherwise the sum of the
twelve link degrees would be at most `5+5+10*3=40`, whereas it is `9*5=45`.
Thus `k=lambda(p,r)` is four or five. The point `r` is globally low and
also has a complete nine-block link.

The primary tie breaker minimizes the product of factorials of the common
block-membership cell sizes, then minimizes the point label. This affects
runtime only. Once a root is fixed, the chosen `r` is a specific point of
every hypothetical global completion represented by that root.

## 3. Primary symmetry checks and complete joining

All primary symmetries are explicit permutations of the twelve link points.
To construct them, `catalogue.py` permutes the intrinsic degree-three point
signatures and then all compatible cells of the nine block columns. A
column action is retained only when it preserves the multiset of all point
signatures. It is lifted through every bijection between equal-signature
point classes. Each resulting point permutation is checked directly against
the nine block masks. Their orbits and orders agree with the imported
metadata; the orders sum to 768. The independent audit below does not use
these automorphism quotients.

The two global stars through `p` and `r` share exactly `k` blocks.
Removing `p,r` leaves `k` four-subsets on eleven points. In the second
link, the point corresponding to `p` must have degree `k`. There are 592
marked degree-four classes and 56 marked degree-five classes, so the second
link has 648 possible pointed templates in total.

For every first root and every compatible second template, `joins.py`
enumerates all `k!` identifications of the common rows. For a fixed row
identification, group the eleven points by their membership pattern in the
`k` rows. An isomorphism exists exactly when corresponding cells have the
same cardinality; enumerate every bijection between those cells. This gives
every identification of the shared block families. Preliminary canonical
keys only reject pairs whose membership patterns differ under every row
permutation.

Map the second link's marked point to `p`, add `r` to its blocks, and take
the union with the first global star. The union has `18-k` blocks. It is
stored as a sorted tuple of integer masks, so duplicate identifications
are removed exactly, with no probabilistic isomorphism test.

Reject a union if a point already exceeds its prescribed global degree,
if its degree deficit exceeds the number `20-(18-k)` of remaining blocks,
or if a pair involving a low point already has multiplicity greater than
five. The pair `{h,q}` is left unrestricted by this filter. The actual
implementation gives it the harmless upper bound twenty.

The complete primary enumeration yields:

| Quantity | Count |
|---|---:|
| First roots | 442 |
| Raw identifications | 877,024 |
| Distinct unions, summed over roots | 392,195 |
| Unions passing the point-degree filter | 392,195 |
| Unions also passing the pair filter | 226,534 |
| Roots with no surviving union | 108 |

Counts of unions are per root, not counts of global isomorphism classes.

## 4. Exact residual search

Both stars are complete. Every additional block must avoid `p,r`.
There are exactly `binomial(11,6)=462` possible such blocks, of which six
or seven must be selected. For each fixed union, `residual.py` tracks:

1. The exact remaining degree of every point other than `p,r`.
2. Remaining pair capacities, with bound five except for `{h,q}`.
3. The uncovered subset of all `binomial(13,3)=286` triples.
4. The set of distinct blocks still available and the exact number needed.

Each is an integer or an integer bitset. A deficit outside `[0,number
needed]` is impossible. A point with deficit zero is removed from all future
blocks; a point whose deficit equals the number needed occurs in all future
blocks. Exhausting a pair capacity removes all other blocks through that
pair. A point with too few candidate blocks or an uncovered triple with no
candidate block rejects the branch.

Two support filters improve the search without strengthening its model.
If a point needs exactly one future block, that block must contain every
uncovered triple through the point. Intersecting the corresponding block
incidence sets gives precisely its remaining possibilities. At the initial
node, if a point needs two future blocks, enumerate pairs that jointly
cover its uncovered triples. Discard pairs violating another point's
degree-one margin or a pair's capacity-one margin. Any genuine completion
supplies one of these supporting pairs, so deleting unsupported blocks is
safe. Other necessary constraints may be omitted from a support test;
omission only leaves extra candidates to the exhaustive search.

At a general node, choose an uncovered triple with the fewest available
covering blocks and branch on each of those blocks. Earlier alternatives
are progressively removed from the domain. This is complete: every solution
has a first selected member in the ordered alternative list and occurs in
that branch. It does not impose a global increasing-label constraint on
blocks chosen for different triples. If every triple has already been
covered, continue branching until the required block count and exact degrees
are satisfied.

Every recursive call selects another block, so the search is finite. All
226,534 instances return `UNSAT`, using 10,179,552 recursive nodes in total;
the largest instance uses 16,920 nodes. There is no time limit, node limit,
floating-point pruning, solver status, or omitted case. `ROOTS.json` records
each root's full configuration-set digest, count, and node statistics.

By Sections 1--3 any forbidden global cover supplies one of these instances;
by this section its remaining blocks would be found. Their nonexistence
proves the theorem.

## 5. Independent exhaustive audit

The audit shares the 107 catalogue representatives and the mathematical
point-link reduction. It replaces both principal enumerations.

`audit_joins.py` keeps every degree-five point label: 64 such labels, each
with eleven choices of `q`, give 704 roots. It chooses `r` by largest
degree and then smallest label, without the primary cell-size tie breaker.
All 899 point labels of degree four or five are retained as second-link
templates. No point or stabilizer orbit quotient is used.

Instead of permuting shared rows, the audit backtracks the actual bijection
of the eleven points. At each stage it compares the multisets of projections
of the common rows onto the points already mapped. A full row isomorphism
preserves each such projection; at full depth equality is exactly equality
of the shared block families. Preliminary degree and intersection invariants
are also necessary conditions only. Thus every point bijection is found.
Degree and pair filters are recomputed directly with counters. Caching an
uncoloured union by the first design and `r` is safe because `h,q` affect
only those final filters. For every root also using the same `r` in the
primary computation, the entire sorted set of surviving unions is compared
by its SHA-256 digest.

`audit_residual.py` chooses an unfinished low point and enumerates its
**entire remaining star at once**. If its deficit is `d`, choose every
feasible `d`-block bundle through it that covers its remaining triples and
respects degree and pair capacities. A block through a fixed point covers
ten triples through that point, so more than `10d` missing triples is
impossible. For `d=1,2` bundles are enumerated directly; for larger `d` they
are built by an exact covering recursion. At the last block, intersect the
incidence sets of all remaining required triples. After a bundle is chosen,
delete every other candidate through that point. Any global completion
contains exactly one of the enumerated bundles, proving this branching
complete. If no low point has a positive margin while blocks are still
needed, no completion is possible: a six-subset cannot consist only of
the two high points.

The audit checks all 647,196 compatible joins without limits, using 687,823
point-search states. Of its 704 roots, 151 have no compatible join. The 141
roots with the same selected `r` as the primary search have identical
configuration-set digests. Its full statistics and canonical record digest
are in `AUDIT_EXPECTED.json`. For `w` workers,
worker `i` receives root indices `[floor(704i/w),floor(704(i+1)/w))`.
These disjoint ranges cover all roots. Records are merged by root index;
missing indices, worker errors, unexpected completions, and mismatches fail
the run. Changing the worker count changes neither enumeration nor digest.

These are different exhaustive algorithms developed within the same research
pass. They provide implementation checks, not independent external peer
review or a replacement for reviewing the shared mathematical reduction.

## 6. Positive controls and final scope

`UPPER21.json` is a known 21-block cover. Remove one through seven of its
blocks avoiding two selected points, and ask both completion engines to
restore a cover using the fixture's actual degrees and pair capacities.
All fourteen tests succeed. Returned block families are checked directly for
distinctness, all 286 triple constraints, exact point degrees, and every
pair bound. Two inconsistent degree-sum mutations are rejected. These controls
exercise the same completion engines; they do not assert that the 21-block
fixture has the degree profile being excluded.

For any twenty-block `(13,6,3)` cover, `C(12,5,2)=9` implies `d(x)>=9`.
Since the degree sum is 120, the total excess above nine is three.
The partitions of three leave exactly

`(12,9^12), (11,10,9^11), (10^3,9^10)`.

The prior exceptional-profile exclusion rules out the first. The present
theorem rules out the second. Thus only the third can remain. The earlier
exceptional-profile result is a dependency of this corollary, not of the
new theorem. No claim is made here that the balanced profile is realizable
or impossible, or that the numerical bound on `C(13,6,3)` has changed.
