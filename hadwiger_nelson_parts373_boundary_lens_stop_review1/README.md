# Independent review: Parts373 boundary-lens exclusion

## Verdict

**Accept at the stated restricted-family scope.**  At source commit
`45d40bcc8adb05c1aee7b0830b1b506f77de0323`, the package
[`hadwiger_nelson_parts373_boundary_lens_stop`](../hadwiger_nelson_parts373_boundary_lens_stop/)
correctly constructs the complete set of common unit neighbours of pairs of
the 23 marked Parts373 receiver pins.  After exact collision merging with the
host, the complete plane unit-distance graph has 488 points, 2,200 edges, and
chromatic number exactly four.

Consequently every replacement whose **every new point** has at least two unit
contacts among those 23 pins is four-colourable.  Any successful replacement
must contain at least one new point with at most one marked-pin contact.

This is a meaningful, exact restricted-family exclusion.  It is not a global
replacement impossibility theorem, a sub-509 five-chromatic construction, or
record progress.

## Independent reconstruction

`independent_check.py` imports no target module.  It differs from the target
in two material ways:

1. it represents the base field as the nested tower
   `Q(sqrt(3))(sqrt(11))`, rather than a flat four-radical multiplication
   table; and
2. it uses outward rational intervals only to exclude noncontacts, then uses
   SymPy's exact real-algebraic simplification for every surviving collision
   and mixed-radical unit equality.

All `binom(23,2)=253` pin pairs were classified:

| circle-pair type | count | roots contributed |
|---|---:|---:|
| secant | 81 | 162 |
| tangent | 24 | 24 |
| disjoint | 148 | 0 |

The resulting 186 formal roots and 373 host occurrences produce 559
occurrences.  Independent all-pairs collision analysis finds 141 pairwise
equalities, whose equivalence classes merge to 488 points.  There are exactly
115 new physical points, safely below the 135-point replacement allowance.

The collision-class sizes are `451x1, 24x2, 10x4, 1x6, 2x7`.  This explains
why there are 141 equal occurrence pairs but only 71 redundant occurrences.
The target's count of 71 is correct for its sequential merge accounting.

## Complete physical graph and colouring

At 96, 128, and 192 interval bits, the independent checker obtains the same
complete result:

| object | value |
|---|---:|
| merged pairs decided | 118,828 |
| interval-certified non-unit pairs | 116,628 |
| complete strict unit edges | 2,200 |
| old host edges | 1,856 |
| host--new edges | 308 |
| new--new edges | 36 |
| exact mixed-radical unit checks | 344 |
| unresolved candidates | 0 |

The point-formula, route, representative-origin, and edge streams agree
entry-for-entry with the target:

```
points   10e010eeb24478d67b17a2b2fc5e860ca26e962aa24593e0d59b7db800e994e4
routes   e01a98146d5f70aba9595648e9523e237d5f59e90d28de193e6b1fac9c29a1e6
origins  b040ddca9799f6ea2f4274ae91b707cc3efdf830cea69aab25959ee118600e1f
edges    800eaa425b8ba5371a93b7370a18c632ef562d0c967481be7acdd49e6d22441f
```

The published 488-character word is proper on all edges and retains the first
reviewed receiver word.  The seven named retained vertices induce eleven
edges and admit none of the 2,187 possible three-colour words.  Hence the
complete support has chromatic number exactly four.

Its actual old--new interface has 80 host vertices.  Fifty-eight lie outside
the marked receiver boundary, and marked pin 0 has no new contact.  Therefore
the earlier 23-pin receiver table alone cannot decide this support.  The target
correctly checks the whole physical graph instead.

## Why the universal quantifier is valid

For two distinct pins `a,b`, with `s=|b-a|^2`, elementary two-circle
geometry gives no common unit neighbour for `s>4`, the midpoint for `s=4`,
and exactly

```
(a+b)/2 +/- i(b-a)/2 * sqrt((4-s)/s)
```

for `0<s<4`.  Every real plane point with at least two marked-pin contacts
therefore appears among the enumerated roots for a witnessing pair.  Conversely,
every root's two defining contacts are checked.  [PROOF.md](PROOF.md) gives the
full reduction.

Thus any replacement composed entirely of these points is a subset of the
four-colourable 488-point support, and the colouring restricts to it.  This
argument covers arbitrary real points; it is not limited to the displayed
number field or an ambient candidate pool.

The conclusion stops immediately when a replacement contains a point with
zero or one marked-pin contact.  It does not classify additional layers,
mixed-contact replacements, other boundaries, or arbitrary plane
constructions.  Nor does the unused 20-point budget strengthen the theorem.

## Reproduction

Use CPython 3.11 and SymPy 1.14.0:

```bash
python3 -m venv /tmp/lens-review-venv
/tmp/lens-review-venv/bin/pip install -r requirements.txt
/tmp/lens-review-venv/bin/python -B independent_check.py \
  --output /tmp/lens-review.json
```

Optional `--bits 96` and `--bits 192` runs reproduce every
precision-independent field.  The normal and optimized 128-bit outputs are
byte-identical.  `EXPECTED.json` freezes the theorem-bearing results, and
`SHA256SUMS` checks the compact review package.

The target's own normal, optimized, 192-bit, control, and checksum replays also
pass.  No SAT solver is needed for either proof: all colouring words are
checked literally.

## Sources, record, and trust boundary

The coordinate input is byte-identical to both the reviewed receiver and the
earlier Parts509 source, SHA-256
`f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50`.
The accepted receiver review is a provenance dependency, but its negative SAT
certificates are not premises of this positive four-colouring exclusion.

The committed Discovery index remained stale at height 4,363 during this
review, and no committed contribution named the boundary-lens result.  Any
review submission must therefore relate only to the committed
Hadwiger--Nelson problem until both target and review are committed.

A final bounded refresh also inspected the later 508-point neutral root150
transfer, the unrelated 426-point two-distance all-lenses closure, and the new
136-point reverse receiver.  The first two are exactly four-colourable; the
third is an unreviewed receiving specification.  None supersedes or is used as
a premise of the present host-specific theorem.

[Parts's paper](https://arxiv.org/abs/2010.12665) reports the 509-point,
2,442-edge construction.  [Haugland v4](https://arxiv.org/html/2608.04542v4)
still identifies 509 as the unrestricted record when checked on 2026-09-15.
The present 488-point graph is four-colourable and changes neither that record
nor the global bounds.

The proof trusts the pinned coordinate and certificate inputs, Python
arbitrary-precision integers and rationals, the explicit interval enclosure
logic, SymPy 1.14.0 for accepted exact zero simplifications, the small review
implementation, SHA-256 for identity comparison, and ordinary hardware.  A
failed simplification cannot create a false equality: it either receives a
separating rational interval or aborts.  This is independent
computer-assisted evidence, not proof-assistant formalization or a novelty
priority claim.
