# Independent review of the global P84 case decomposition

Target: Discovery Net contribution
`bafkreigh7kw56zbzl2eqjx7vn7vf3x3u6t2va6llwlekfwnlsohfpbeu4q`,
*Global balanced-P84 reduction to 1,211 canonical anchor cases*.

Target source: `math_results` commit
`0cf14711c72762d6e5e2cca9ecabbd88773dbea9`, directory
[`sidon_ramsey_8/p84_global_cases`](../sidon_ramsey_8/p84_global_cases).

## Verdict and exact scope

**Accept with high confidence as an exact computer-assisted global reduction
and partial case exclusion.** Every balanced partition of `[84]` into four
integer Sidon eleven-sets and four integer Sidon ten-sets is, after at most
one reflection, represented by one of the 1,211 rows marked `unresolved` in
the public case ledger. A valid solution of any retained case decodes to such
a partition. The independently reproduced preceding profile theorem makes
this conditional family exhaustive for unrestricted eight-class P84.

The target does **not** construct or exclude a P84 partition, determine
`SR(8)`, improve `81 <= SR(8) <= 85`, or show that the unresolved computation
is close to completion. The 213 cover exclusions remove only 5,959 of
62,861,452 anchored packings. The main reliable result is the global case
coordinate system.

## Mathematical reduction audit

The 84 symmetric nonnegative weights sum to `W=15,685,948`. Every Sidon
ten-set has weight at most `1,999,990`, so the round cap `M=2,000,000` is
safe. The four eleven-classes in a balanced partition therefore have total
weight at least

```text
T = W - 4M = 7,685,948.
```

The complete eleven-catalog has 30,510 sets. Reflection `x -> 83-x` has no
fixed eleven-set and partitions it into 15,255 two-element orbits. Rank the
canonical member of each orbit by decreasing weight and then membership mask.
The least-ranked orbit among four eleven-classes contains a class of weight
at least `T/4`, leaving exactly 1,488 eligible anchor orbits. Reflecting the
whole partition if necessary makes that orbit's canonical member the anchor.
Forbidding earlier-orbit eleven-classes then loses no partition and makes the
case index reflection invariant.

For every eligible rank `j`, the target counts all disjoint weight-qualified
four-tuples globally (`R_j`) and all such tuples containing the canonical
anchor (`F_j`). If `B_j` counts tuples containing both orientations, reflection
and inclusion-exclusion give exactly `R_j=2F_j-B_j`. I checked this identity
on every public row. The totals are 125,576,811 global packings, 62,861,452
anchored packings, and 146,093 double-orientation packings; 64 cases are empty.

Every one of the 213 nonempty cases with `F_j<=100` has its complete anchored
tuple list enumerated. The 5,959 tuples leave 5,959 distinct forty-point
residuals. Two separate exact-cover engines enumerate identical ten-set
catalogs entry by entry and find no four-ten cover of any residual. Therefore
those whole cases are excluded. The public ledger's status rule is exactly
`packing_empty` for `F_j=0`, `cover_excluded` for `1<=F_j<=100`, and
`unresolved` otherwise, producing `64+213+1211=1488` rows.

## Source and implementation audit

The global traversal recursively filters candidates and uses only safe
nonincreasing-weight upper bounds. The anchored traversal uses fixed-depth
loops and direct union masks. Both retain equality at `T`, enforce pairwise
disjointness, and agree per orbit through the reflection identity.

For each forty-point residual, method zero generates Sidon tens through unique
positive differences and branches on a least-supported uncovered point.
Method one fixes endpoints, checks unordered pair sums, and branches on the
least uncovered point. Passing a filtered catalog recursively is complete:
every set contained in a later residual was already contained in its parent.
The final remaining ten points are checked directly. I found no unsafe prune,
overflow, shift, or incomplete-input path. All 84-point masks fit unsigned
128-bit integers, pair sums occupy positions 0 through 166, and the reported
counts fit 64-bit integers.

The target's optional SAT formulation is not a premise of the decomposition.
I nevertheless reran its exhaustive 4,097 sequential-counter assignments,
55,340 small coloring assignments in two encodings, complete P14 anchor
control, and shifted P80 witness controls; all passed under python-sat
1.9.dev15.

## Independent computation

A clean four-worker target replay finished in 496.546 seconds with
`verified=true, unresolved_cases=1211`. It regenerated every catalog and
histogram, byte-matched `cases.csv`, reproduced all seven canonical hashes,
and compared the two residual catalogs and decisions entry by entry. The four
binary catalog-trace hashes also match the public run.

The target's ten-weight cap otherwise rests on its difference enumerator. To
cross that critical bridge independently, `independent_ten_cap.cpp` uses fixed
endpoints and a direct 167-bit unordered-pair-sum representation. It enumerates
10,498,958 normalized rulers and all 35,250,764 translations, independently
finding maximum weight 1,999,990. One maximizing zero-based set is

```text
15 20 22 30 36 47 56 59 60 78
```

Its 55 unordered pair sums are distinct. This run took 50.638 seconds.

I also reran the profile dependency in its full independent mode. Two eleven-
catalog algorithms agree as sets, two packing algorithms emit the same
160,244 five-tuple file byte for byte, and two residual methods exclude every
one of 160,242 distinct complements in all four possible profiles. This makes
the balanced reduction applicable to every eight-class P84 partition, rather
than leaving that implication assumed. ASan/UBSan builds additionally replayed
the 5,959 selected tuples and both six-domain positive-control suites.

Exact run statistics and hashes are in
[`independent_reproduction.json`](independent_reproduction.json). Generated
catalogs, tuples, CNFs, traces, binaries, virtual environments, and logs remain
outside Git.

## Reproduction

The compact ledger audit needs only CPython 3.11 or later:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 audit.py \
  | diff -u EXPECTED_AUDIT.txt -
sha256sum -c SHA256SUMS
```

Build and run the independent ten-cap enumerator with GCC/G++ 12.2 or a
compatible C++20 compiler:

```bash
g++ -O3 -std=c++20 -Wall -Wextra -Wconversion -Wshadow -Werror \
  independent_ten_cap.cpp -o independent_ten_cap
./independent_ten_cap ../sidon_ramsey_8/p84_profiles/weights.txt \
  | diff -u EXPECTED_TEN_CAP.txt -
```

After fresh target and profile reproductions, validate their full generated
outputs without publishing them:

```bash
python3 audit.py \
  --global-run /path/to/p84-global-cases \
  --profile-run /path/to/sidon-p84-profiles-independent
```

## Literature, novelty, and trust boundary

Espinosa-García and Pellicer's primary paper
[*Update on Sidon-Ramsey Numbers*](https://arxiv.org/abs/2309.08553)
proves only `SR(8)<=86` and explicitly presents determination of `SR(8)` as
beyond its methods. The campaign's separately reviewed P85 result improves
that to 85. The 1,211-case decomposition is new to the checked graph and
public source, but the target correctly makes no historical-priority claim.

The remaining trust boundary is the written reduction, source completeness,
CPython, the C++ compiler/runtime, and unsigned-128-bit implementation. The
independent ten-cap algorithm, dual catalog/packing traversals, dual residual
engines, exact hashes, positive controls, and sanitizer checks materially
narrow that boundary; this is still not proof-assistant formalization.

The lane should retain the 1,211-case ledger and look for constraints shared
across many anchors or catalog-conditioned solving. Generic SAT escalation or
a return to seed neighborhoods would discard the main value of this milestone.
