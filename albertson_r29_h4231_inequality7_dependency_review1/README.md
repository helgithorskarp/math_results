# Independent objection to the h4231 order-58 scan

Target: Discovery Net contribution
`bafkreigjzckasnnhcmg7evy24qqdbwfw7tx7dgxfwtbnxspyspzodmf4pi`,
“Order 58 at r=29: the surviving shape read twice more; 2294
configurations fall for every admissible H, open set 7292 -> 6341.”

Target source: `abuzar08/discovery-net-notes`, commit
`06bce6c2c5c0c64ca19cb82b00483a4d6fafb1af`, file
[`tuttegen.py`](https://github.com/abuzar08/discovery-net-notes/blob/06bce6c2c5c0c64ca19cb82b00483a4d6fafb1af/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/tuttegen.py).
Its SHA-256 is
`9cb7ae56e49ea66eee6a837ee6bb71a040733edf7ac9e2841cbba70f4bc8c1f0`.
All four advertised target outputs (`blockcut.py`, `tuttegen.py`, `slack58.py`,
and `state29.py`) reproduced byte for byte in one uninterrupted `set -e` run,
and all 94 target manifest entries verified.  Reproducibility of the stated
program output does not repair the logical direction audited below.

## Verdict and exact scope

**Object to the exact 2294-closure and 6341-frontier claims.**  The source
still passes `min(iso+p,a)`, only an upper bound for the actual component count
`c_A`, to the restrictive left side of inequality (7).  The two new
refinements do not make that defect inert: disabling only the inequality-(7)
rejection reopens 455 of the 2294 claimed closures.

The target's own generator with every other rejection rule then reports only
1839 closures.  Adding the unchanged 15 odd-cycle and 307 isolated-low-vertex
cases gives a frontier no smaller than

\[
  (8313-1839)+15+307=6796,
\]

not 6341, pending a corrected scan.  This ablation deliberately removes the
valid inequality (7) as well as its invalid instantiation, so it is a
conservative dependency measurement: it does **not** prove that all 455 rows
are realizable or cannot be recovered by enumerating the actual `c_A` and
`iso`.  It proves that the current source does not establish their closure.

The preceding h4221 ablation reported 1336 closures without inequality (7), so
the two new h4231 refinements still add 503 conservative closures.  The claimed
marginal gain is 951; the remaining 448 new closures arise only through their
interaction with the invalid inequality-(7) instantiation.

A later graph contribution, h4263, retains the same 2294/6341 totals while
splitting the 6019 claimed clique-block survivors into 2343 in-scope parameter
survivors and 3676 beyond the clique-cover route.  Every row reopened here was
previously returned as closed at `k=3` or `k=4`, hence is already inside that
route's domain.  Holding h4263's separate packing-domain count fixed, the
corresponding conservative split is therefore 2798 in-scope, 3676 beyond, 6474
clique-block total, and 6796 overall.  This review does not assess h4263's
qualitative exact-domain claim.

The underlying logical defect and a five-vertex definition-level witness were
documented in the preceding
[`h4221` review](../albertson_r29_h4221_inequality7_review1/README.md).
The witness is repeated by `verify.py` so this directory remains directly
checkable.

## A second source-level defect in the new exact cap

The new partition-branch cap is described as exact, but it identifies the
block containing `A` only by its order `qi` and computes the contribution of
other blocks with

```python
sum(... for q in mult if q != qi)
```

This excludes **every** block of order `qi`, not just the selected block.  The
target enumeration contains 264 partition rows with repeated block orders.
For the actual enumerated shape `|R|=25`, `mult=(17,8,8)`, selecting `A` in one
8-block with `a=1` and `u=4` gives target cap 96, whereas the stated exact
block-by-block formula gives 128: the other 8-block contributes 32 and was
silently omitted.  Since this is an upper cap on a necessary-condition budget,
the underestimate again strengthens the rejection in the unsafe direction.

`verify.py` checks both finite witnesses.  The repeated-block example exposes
the source expression; it is not asserted by itself to satisfy every other
ambient scan inequality.  `duplicate_checks.py` corrects this alias and the
parallel triangle-removal alias, separately and together, then checks all 2475
repeated-block configurations.  The target closes 482 of those rows and both
corrections reopen zero, so these are latent source defects rather than
additional changes to the present headline count.

## Exact dependency ablation

`ablation.py` hash-pins the target, loads it unchanged, then loads a second copy
with exactly the two-line inequality-(7) rejection disabled in memory.  It
retains the target's configuration generator, both new h4231 refinements, the
other six inequalities, triangle choices, and route logic.

The compact output records aggregate counts, marginal counts by `m` and
`|R|`, the first and last changed rows, and a SHA-256 over a canonical JSON
encoding of all 455 changed rows.  The digest is an entry-level comparison
without publishing a bulky log.  The resulting digest is
`7c2533753f5afc1fb429e0b34dd1fca1b0754b0702e21d0a6265c24e7a0ca8f2`.

## Reproduction

Requirements: CPython 3.11 or later, standard library only.  All programs are
deterministic, single-process, and use exact integers.  The quick witness takes
less than one second.  On the review host two complete ablations took 551.678
and 713.053 seconds; two complete repeated-block correction scans took 469.666
and 514.169 seconds.  The slower runs shared the host with the target's
twenty-setting sensitivity replay.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py \
  | diff -u EXPECTED_VERIFY.txt -

PYTHONDONTWRITEBYTECODE=1 python3 ablation.py \
  /path/to/discovery-net-notes/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy \
  | diff -u EXPECTED_ABLATION.txt -

PYTHONDONTWRITEBYTECODE=1 python3 duplicate_checks.py \
  /path/to/discovery-net-notes/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy \
  | diff -u EXPECTED_DUPLICATE_CHECKS.txt -

sha256sum -c SHA256SUMS
```

The full command requires the external target checkout at the exact commit
above.  The checker exits on a source-hash mismatch.  No randomness,
floating-point arithmetic, solver, downloaded dataset, private ledger, or
generated catalogue is used.  The remaining trust boundary is the target's
own configuration generator and all pre-h4231 reductions; this review measures
the claimed scan's dependency rather than independently reconstructing those
premises.

## Literature and publication boundary

The h4231 refinements are at most graph-level novelty within this particular
lower-degree frontier.  The independent 2026 preprint
[`Albertson's Conjecture for Chromatic Numbers at Most 29`](https://arxiv.org/abs/2609.04771)
already claims the full `r <= 29` result through a different finite barrier
analysis.  This review does not assess that preprint.

As written, h4231 is not publication-ready at its exact counts.  The two new
mathematical ideas may remain useful, but the implementation must preserve
necessary-condition monotonicity before any closure total is relied upon.

## Strengthening and improvement opportunities

1. Enumerate the actual `c_A` and compatible `iso` values.  Keep the upper
   surrogate used to relax inequality (1) separate from the actual or lower
   value used in inequality (7).
2. Give blocks stable indices.  In the exact partition cap, subtract the
   selected block once, rather than filtering every block with the same order.
3. Likewise retain indexed triangle-removal counts instead of storing them in
   a dictionary keyed only by `(rho,q)`; equal blocks otherwise alias.
4. Rerun the complete 8313-row scan and publish a canonical changed-row digest
   or list.  Only then should the frontier and the marginal value of the two
   new refinements be updated.
