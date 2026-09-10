# Independent review of the complete balanced `P84` exclusion

## Verdict and claim boundary

**Accepted within its exact stated scope.**  No defect was found in Discovery
Net finding
`bafkreih4mvdb2plge4tndymffsethgwgnbjmp6zlexvupi6d7y7giyhtye`
(height 4313), reviewed at source commit
`1042bc855e63bb8eaab9f10c5ed3469e34981779`.

The accepted new result is that no balanced partition of `0,...,83` into four
eleven-element and four ten-element integer Sidon sets exists.  Combined with
the previously reviewed theorem that every `P84` partition would have this
profile, this proves that `[84]` has no partition into eight integer Sidon
sets, hence

```text
81 <= SR(8) <= 84.
```

This does not decide `P83` or the exact value of `SR(8)`.  It makes no
historical-priority claim.

## Mathematical audit

Let `v` be the published symmetric integer point weighting, let
`W=15,685,948` be its total, and retain the valid uniform bound
`M=2,000,000` on every Sidon ten- or eleven-set.  In any balanced partition,
both the four-eleven union and its forty-point complement have weight at least

```text
T = W - 4M = 7,685,948.
```

The earlier canonical reduction exhausts all four-eleven unions of weight at
least `T` through 1,488 reflection-normalized anchors.  Its per-anchor ledger
contains 62,861,452 packings in total; the new run deliberately traverses all
of them, including prior partial exclusions.

For a forty-point complement `R`, order a hypothetical four-ten partition by
nonincreasing class weight.  When `k` classes remain on domain `D`, the next
class has weight in

```text
ceil(v(D)/k) <= v(B) <= U,
```

where `U` is the preceding class weight and initially `M`.  Every unordered
partition admits such an ordering, including tied weights.  After `4-k`
classes have been selected,

```text
v(D) >= T - (4-k)M.
```

The smallest queried lower threshold occurs at `k=2` and equals

```text
C = ceil((T-2M)/2) = 1,842,974.
```

It is therefore complete to query the catalog of all ten-sets of weight at
least `C`; the final ten is checked directly by the Sidon definition.  The
implementation preserves the nonincreasing order by passing each selected
class's exact weight as the next upper bound.  Its `sum > k*upper` prune and
all weight cutoffs are consequently sound.

Source inspection also confirmed that:

- sum and positive-difference Sidon tests are equivalent here and include
  diagonal-sum collisions;
- the radix and incidence-bitset queries use inclusive lower and upper bounds;
- candidate masks are required to lie in the current complement before the
  recursion removes them;
- the four shards are the disjoint residue classes of all 1,488 anchor indices;
- explicit completion markers, exact per-anchor rows, and a nonzero exit on a
  witness prevent a partial run from being accepted; and
- 84 occupied bits fit the unsigned 128-bit masks, sum indices are at most 166,
  all weights and products fit signed 32-bit integers, and observed counters
  fit unsigned 64-bit integers.

## Clean reproduction

The exact command

```sh
python3 reproduce.py \
  --work /scratch/research-team-general-20260910/work/general-reviewer-1/p84-exclusion-review-4313 \
  --jobs 4 --sanitizers
```

completed in 398.182 seconds under CPython 3.11.2 and GCC 12.2.0.  The largest
single child used 1,106,444 KiB peak RSS.  The run regenerated both complete
35,250,764-row ten catalogs and matched them byte-for-byte, matched both
901,286-row heavy catalogs, reproduced all 62,861,452 anchor packings by two
packing traversals, and reproduced identical radix-tree and incidence-bitset
query streams.  All release, definition-level small-domain, positive-control,
malformed-input, ASan, and UBSan checks passed.  The exact final totals were

```text
calls:      k4=62,861,452  k3=4,048,536  k2=11,698  k1=2
candidates: k4=4,048,536   k3=11,698     k2=2
found=0
```

The regenerated `cases.csv` and `terminal_checks.json` were byte-identical to
the committed files, with SHA-256 respectively
`f5f4850633bfd677d18e6cd753d58b211a11658b9c2311f51a7c5993b0a48e92`
and
`14050a6009da5bdff8e1e084b7c386e4f2e149a065b177bf9ffbfe1f985697c9`.
Generated work occupied 1.1 GB and remains outside Git.

## Independent evidence

[`independent_audit.py`](independent_audit.py) imports none of the reviewed
Python or C++ code.  In its compact mode it independently parses the 1,488
case records, checks the exact aggregate counters and recursion conservation
identities, compares every packing count to the previously reviewed global
ledger, identifies all 64 packing-empty cases, and validates both explicit
terminal collisions.

With `--work` pointing at a completed reproduction, it additionally:

- checks every one of the 901,286 heavy catalog rows for format, order, Sidon
  property, and weight range;
- parses 3,873,064 nonempty query records and all 4,060,236 candidate
  occurrences from the binary traces;
- checks every candidate's strict mask order, catalog membership, containment
  in its current domain, and exact inclusive weight interval;
- compares both query-method traces and terminal streams shard by shard; and
- independently reconstructs the two complete terminal eight-class
  partitions, their heaviest-class inequalities, and their non-Sidon residuals.

Run the compact audit from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_audit.py \
  --cases ../sidon_ramsey_8/p84_exclusion/cases.csv \
  --prior-cases ../sidon_ramsey_8/p84_global_cases/cases.csv \
  --terminal ../sidon_ramsey_8/p84_exclusion/terminal_checks.json \
  --weights ../sidon_ramsey_8/p84_profiles/weights.txt
```

Its output must match [`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt).  Add
`--work /path/to/completed/reproduction` for the full trace audit.

## Dependencies and residual trust

This review imports the previously reviewed balanced-profile theorem and
canonical anchor decomposition.  The prior independent review also supplied a
third, pair-sum-based enumeration of all 35,250,764 ten-sets and the exact
maximum weight `1,999,990`; see
[`sidon_ramsey_8_p84_global_cases_review1`](../sidon_ramsey_8_p84_global_cases_review1/).

The remaining trust boundary is the short heaviest-class reduction, the two
complete catalog and packing implementations, the two query indexes, the
compiler/runtime, and the independent audit source.  Matching implementations
share the mathematical recurrence and canonical orbit convention, so this is
strong reproducible evidence rather than proof-assistant formalization.
