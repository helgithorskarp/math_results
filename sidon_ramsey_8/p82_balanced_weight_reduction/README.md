# A global eleven-class weight restriction for balanced P82 partitions

**Proved by exact computer-assisted exclusion:** every balanced P82 partition
contains an eleven-class of weight at least **3,824,714** for the fixed weights
specified below. All **460,485** pairs with lighter canonical anchors are
excluded. The complete remaining cover consists of **1,000 nonempty canonical
anchors and 682,437 pairs**. No P82 witness or complete P82 exclusion is claimed.

Write P82 = {0,...,81}. A set is Sidon when its unordered pair sums, including
repeated summands, are all distinct. The preceding
[P82 profile reduction](../p82_profiles/README.md) and
[three-eleven exclusion](../p82_three_exclusion/README.md) leave only the size
profile 11^2 10^6 for an eight-class partition of P82. The current interval
81 <= SR(8) <= 83 remains unchanged by a partial balanced-profile exclusion.

This computation covers **every** balanced partition whose heavier eleven-class
has weight at most 3,824,705, for the fixed integer weights in
[weights.txt](../p82_profiles/weights.txt). It uses no distinguished seed or
bounded modification neighborhood. The exclusion leaves the globally
exhaustive first 1,000 canonical anchor cases, containing 682,437 pairs.

The prerequisite two-profile reduction and every anchor count were subsequently
[accepted and independently reproduced](../p82_profiles_review1/README.md). The
present balanced-profile completion sweep has not received external review.

## Complete reduction

Let w be the cited reflection-symmetric weights, W = w(P82) = 30,884,468 and
M = 4,000,000. The earlier complete catalog computation establishes that every
Sidon ten-set and eleven-set has weight at most M. It supplies all 8,214
Sidon eleven-sets, in 4,107 reflection orbits, and all 17,249,580 Sidon ten-sets.

For an eleven-set S, use min(mask(S),mask(81-S)) as its orbit representative.
Order these representatives by decreasing w and then increasing mask. Put the
representative in row 2q and its reflection in row 2q+1. The two eleven-classes
A,B in any balanced partition can be relabeled and simultaneously reflected so
that A occupies an even row i=2q and B occupies a row j>i. This follows by
choosing the earlier of their reflection orbits and orienting its member as the
representative. If both classes are in one orbit they occupy the two rows of that
orbit. Because the six remaining classes each have weight at most M,

    A intersect B = empty,       w(A)+w(B) >= W-6M = 6,884,468.

All 1,142,922 pairs satisfying these conditions were already counted in the
complete profile ledger. The present independent stream auditor enumerates every
such pair in its requested range without the search program's early weight
termination. Its ordered pair headers must agree exactly with the search trace.
The per-anchor counts must also match the earlier complete ledger.

The boundary q=1000 is a strict weight boundary: q=999 has weight 3,824,714 and
q=1000 has weight 3,824,705. Thus every partition with both eleven-weights at most
3,824,705 occurs in the range 1000 <= q < 4107. There are 460,485 eligible pairs
in this range, spread over 2,840 nonempty anchors. The complementary first 1,000
anchors are retained in full; this is an exhaustive remaining cover.

## Six-ten completion search and proof of completeness

For a fixed pair, let D0=P82 minus (A union B), so |D0|=60. In a remaining state
(D,r,U), search for r disjoint ten-sets partitioning D, with every weight at most
U and U <= M. If w(D)>rU there is no completion. If r=1, test D directly by the
Sidon definition. Otherwise a heaviest remaining class C must satisfy

    ceil(w(D)/r) <= w(C) <= U.

Query every Sidon ten-set C contained in D in this interval, and recurse on
(D minus C,r-1,w(C)). Numeric mask order makes candidate traversal deterministic.
Every completion has an ordering by nonincreasing weight, so induction on r
proves completeness. A finite call limit returns UNKNOWN and cannot certify
exclusion; the claimed range requires zero unknown cases.

The reusable catalog for a fixed A consists of every ten-set in E=P82 minus A
of weight at least

    Lparent = max(0, w(E)-w(A)-5M).

Indeed w(B)<=w(A), and any one ten-class in the root complement has weight at
least Lroot=max(0,w(D0)-5M)>=Lparent. More strongly, no query candidate is lost by
this cutoff. After selecting 6-r classes, w(D)>=w(D0)-(6-r)M, and

    [w(D0)-(6-r)M]/r - [w(D0)-5M]
      = (r-1)[6M-w(D0)]/r >= 0.

The root is unpruned only when w(D0)<=6M. Hence every queried weight is at least
Lroot, regardless of whether that branch has a full completion. Reuse therefore
preserves the complete candidate stream, not only potential witnesses.

## Two query implementations and independent audit

Method 0 builds a radix tree for the global catalog, obtains the parent catalog,
and answers each recursive query by a direct linear scan over the applicable
weight interval. Method 1 builds point-incidence bitsets and answers subset
queries by eliminating rows containing forbidden points. Both return masks in
increasing order. Their input rows are validated independently using distinct
positive differences (method 1) and unordered pair sums (method 0).

A stable two-pass radix sort constructs the weight order. Its keys are M-w(C),
which lie in [0,4,000,000] and fit in 22 bits. The implementation then verifies a
strict lexicographic ordering by (-weight,row index) of all N indices in [0,N).
This also verifies that they form a permutation. Derived in-memory catalogs use
only rows returned by a validated input catalog; their cardinality, mask order,
point range and weight cutoffs are checked again.

The two full streams are compared **byte for byte**, not merely by hashes. A
separate auditor, sharing neither catalog nor search source, checks every pair
header against its independently enumerated cover, every emitted candidate for
all 55 pair sums, its subset relation and weight interval, every terminal test,
and per-pair counters. It does not itself prove candidate-list completeness or
replay the recursion; those remain explicit algorithmic trust boundaries. The
two implementations share the recurrence and weight-order construction.

The deterministic controls compare both indexed queries and the linear scan
against an unindexed definition-level oracle. They also compare the recurrence
against unordered combination enumeration on small catalog families, verify
238 known positive domains obtained from the published P80 partition, exercise
negative domains, and ensure a budget limit returns UNKNOWN. Malformed trace
controls must fail. AddressSanitizer and UndefinedBehaviorSanitizer run on these
controls. This is a computer-assisted proof architecture, not formal proof or
independent external peer review.

## Reproduction

Requirements: Python 3.11, GCC 12 with C++17, a POSIX system for FIFOs. There are
no Python package dependencies for the proof replay. Compilation uses -O3 and
-Wall -Wextra -Wconversion -Werror. Four paired shards use up to eight search
processes and four stream auditors. Each shard contains exactly q congruent to
its index modulo four; anchors run in decreasing order.

From this directory, first regenerate the prerequisite catalogs if needed:

```sh
python3 ../p82_profiles/reproduce.py --work /tmp/p82-inputs --jobs 4 --workers 6
python3 reproduce.py --work /tmp/p82-weight-reduction --inputs /tmp/p82-inputs \
  --jobs 4 --minimum 1000 --maximum 4107 --budget 100000 --sanitizers
```

Use fresh empty work directories outside the repository. The input hashes are
verified against the earlier published catalog validation. A failed or
interrupted run has no final validation file and cannot support the result.
Bulky catalogs, transient candidate streams and operational checkpoints are not
published; the streams pass through FIFOs and are audited without being saved.
Compact source, per-anchor counters, hashes and validation reports support full
reproduction. Candidate counts and byte counters use checked or bounded 64-bit
arithmetic; masks use unsigned 128-bit integers and all mathematical weights are
integers. No floating-point calculation enters an exclusion decision.

## Exact obstruction to a global point-weight shortcut

A separate standard-library rational checker verifies an **83-row certificate**:
57 Sidon ten-sets and 26 canonical pairs of disjoint Sidon eleven-sets have
positive rational coefficients. These rows cover every point with total
coefficient exactly one. Ten-row coefficients sum to six and pair-row
coefficients sum to one. No reflection averaging is used.

Every supported pair has old union weight at least 7,841,648, heavier eleven
weight at least 3,943,985 and lighter eleven weight at least 3,860,682. Thus the
certificate lies entirely in the retained heavy-anchor region. It even remains
valid under the stronger hypothetical restriction that the heavier eleven-class
has weight at least 3,943,985. The checker verifies the canonical orientation
from the weights and numeric masks, without trusting the LP's row identifiers.

Consequently, for **any real, possibly asymmetric** new point weights v, if C10
bounds v(T) for every Sidon ten-set and Cpair bounds v(A union B) for every
canonical admissible eleven-pair in that restricted region, then

    sum(v(x), x in P82) <= 6*C10 + Cpair.

This follows by applying the two caps to the exact positive combination. It
rules out a strict separation certificate of this particular global form. It
does not assert an integer partition, conditional fractional feasibility for
every pair, or impossibility of richer inequalities. The floating-point LP
used to discover the rows is outside the proof boundary; the published
certificate is checked only by integer pair sums and exact rational arithmetic.

```sh
python3 check_fractional.py --certificate canonical_fractional_certificate.json \
  --weights ../p82_profiles/weights.txt
```

Optionally append `--orbit /tmp/p82-inputs/orbit11.txt` to verify the support's
canonical row indices against the regenerated eleven-set catalog.

The supplemental real-trace corruption controls can be rerun after compilation:

```sh
python3 audit_candidate_controls.py --program /tmp/p82-weight-reduction/audit_stream \
  --fixture audit_candidate_fixture.json --weights ../p82_profiles/weights.txt \
  --orbit /tmp/p82-inputs/orbit11.txt
```

The same command with `audit_stream_sanitized` checks the sanitizer build.
These fixtures test rejection of out-of-range masks, wrong cardinality,
duplicates, weight violations and pair-sum collisions.

## Completed production evidence

The final paired replay completed in 1167.92 seconds, reusing the
previously regenerated catalogs after verifying their identities. Each method
completed all 3,107 requested anchor rows, including 2,840 nonempty rows, with
zero UNKNOWN and zero SAT results. A resource sample during the run measured
about 7.00 GiB of aggregate resident memory across the eight search workers and
four auditors; this is a sample, not a measured peak.

| Per-method quantity | Exact value |
| --- | ---: |
| Excluded canonical eleven-pairs | 460,485 |
| Search calls | 494,796,944 |
| Candidate occurrences | 494,336,459 |
| Nonempty query records | 146,387,690 |
| Terminal ten-set failures | 4,786 |
| Exactly compared and audited bytes | 14,969,338,824 |
| Largest completed pair search | 16,863 |
| Pair call limit, never reached | 100,000 |

The exact identity calls = excluded pairs + candidate occurrences holds. The
compact completed ledger is `cases_completed.csv`; `remaining_cases.csv`
retains every first-1,000 anchor and its full imported pair count. These files
partition the earlier global case cover. `validation.json` records all four
stream comparisons, independent audits, controls and frozen search-source
hashes; `expected.json` gives the main totals. The completed ledger SHA-256 is
`7ba3a83ac3022481ccbe99b9ebd3c3d83da497a9a9c2d878a0744631f38bc01c`. Auxiliary fractional and trace-corruption checkers were
added after the frozen full replay; they do not change its search sources.
