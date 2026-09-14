# Fixed a=8 physical transfer and two positive selector refinements

This package freezes a **508-point strict plane unit-distance support with
2,435 edges**. Its unrestricted relation on the 19 marked terminals of Parts'
L374 source contains exactly **8 of the source's 20 canonical patterns**.
The driver consists of 126 original S points and 8 points from the already
sealed Q5 completion pool. All coordinates and all unit contacts are exact.
The graph is **four-colourable**, and is **not a five-chromatic record candidate**.

The other result is two directly checked positive colouring cuts, of sizes
14 and 6. Each excludes a physical a=8 selection that satisfies all previously
imported cuts (and, for the second, the first new cut). They strictly refine
the existing Boolean relaxation. Neither their number nor the terminal-pattern
count proves progress on the global minimum. This does not close a=8, prove
optimality within the pool, or improve the published 509-point record. Parts reports 509 vertices and
2,442 edges in [his minimization paper](https://arxiv.org/abs/2010.12665);
[Haugland’s August 2026 paper](https://arxiv.org/html/2608.04542v4) still identifies
509 as the record. Both primary pages were retrieved on 14 September 2026.

## Exact construction

Use the point labels in the sibling Parts source packages, with
`L = {0,...,373}`, `S = {374,...,508}`, and the 168-member `Q5` in
`hadwiger_nelson_parts509_s_replacement_budget/pool_S.json`. Remove from S:

```
374 375 389 390 393 413 415 438 493
```

and add from Q5:

```
548 552 565 598 693 720 1639 1645
```

The collision-merged total is `374 + (135 - 9) + 8 = 508`. The accepted exact
geometry reader reconstructs the 677-point ambient support and all 3,400
unit edges in `Q(sqrt(3),sqrt(5),sqrt(11))`, with common denominator 288.
Restricting its complete edge set to this support gives all 2,435 unit edges.
No approximate contact or abstract graph embedding is used.

The allowed class indices, in the ordering of the pinned `interface_L.json`,
are `[4,7,12,13,14,15,17,19]`. `certificate.json` supplies one proper full
508-point four-colouring for each, and a proper five-colouring. The latter
is an upper-bound witness only. `pool_five_colouring.txt` also colours the
entire 677-point ambient graph properly with five colours.

## Why this is the complete unrestricted relation

Every edge from any point of the sealed pool into L ends at one of the same
19 terminals covered by the earlier complete 20-class L theorem. The verifier
checks this equality of interfaces after reconstructing **all** ambient edges.
Consequently, the possible extension to the driver depends only on one of those
20 terminal patterns; it does not depend on which internal L colouring realizes
it. The original convention fixes the origin's colour and quotients by the
remaining colour permutations. No new restrictions are put on source colours.

Eight full positive words establish extension. To exclude the other twelve
patterns together, the verifier generates a one-hot four-colour CNF on the
134 driver points. Driver edges impose inequality. Twelve selector variables
have an at-least-one clause. Selecting a pattern activates the forbidden
colours at all driver-to-L contacts for that pattern. A model exists exactly
when at least one excluded input pattern extends: activate its selector for
the forward implication; use any active selector for the reverse implication.
Kissat produces an UNSAT proof; drat-trim checks it. The local replay gave
548 variables and 3,479 clauses, with a 896,956-byte DRAT certificate.
The proof is regenerated rather than stored in Git.

This imports the previously published complete L relation theorem; it is not
an independent reproof or review of that input. The eight positive words are
checked directly on every physical edge. The twelve negative extensions use
the checked proof, not the SAT search's unverified statuses.

## Positive cuts and the open construction decision

For each row in `colouring_cuts.json`, `D` is omitted from the full 303-point
pool and `c` is a proper colouring of the remaining pool, attached to the
specified full L witness `p`. A prospective non-four selection X must meet D:
otherwise this explicit colouring restricts to L union X. Thus each D yields
a necessary positive clause. Every colouring is checked on all physical edges.
Each row also supplies an `excluded_X` of the exact a=8 shape that misses D
while meeting every older imported clause. This verifies strict refinement
without treating a selector model as a chromatic graph.

The five imported files contribute 17,266 distinct clauses; their hashes are
in `seed_hashes.json`. Their mathematical validity is inherited from their
published source packages. New-cut validity uses only literal proper words.
The two new rows do not constitute an exhaustive cover.

`search.py` implements the isolated a=8 search. It selects exactly 126 S points
and 8 Q5 points, tests the complete 20-pattern interface, and adds only cuts
with checked proper colouring witnesses. The selected Q5 points must have
degree at least four: a low-degree point could be removed and its colour
extended after applying the already proved a=7 closure (adding one omitted S
point if needed). No degree condition is imposed on original S vertices.
The initial incremental solver reached its conflict budget; saved-master
Kissat decisions supplied further models. The ongoing fixed-cohort decision
is computationally unresolved. `UNKNOWN` is not an exclusion.

The 20-to-8 change is relative to the input L relation. It is not a monotone
improvement over every previously known 508-point support. Even simple single
vertex deletions from Parts' graph can have small terminal relations. This
package asserts neither a best relation count nor a newly discovered general
construction principle. It records the exact new driver and usable cuts at
the first open replacement shape after the published a=0,...,7 closures.

## Reproduction

From this directory in a full checkout of `math_results`, with Python 3.11+:

```bash
python3 -B verify.py --work /tmp/hn-a8-proof
python3 -B controls.py
python3 -O -B verify.py --work /tmp/hn-a8-proof-optimized
sha256sum -c SHA256SUMS
```

The first command checks coordinates, complete edges, all positive words,
new cuts and the generated CNF. Its status explicitly says the negative proof
has **not** been run. For the full relation claim, provide local executables:

```bash
python3 -B verify.py --work /tmp/hn-a8-full-proof \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

Expected full status: `EXACT_COMPLETE_INTERFACE_VERIFIED`, with `points=508`,
`unit_edges=2435`, `allowed=8`, `forbidden=12`, and `record_candidate=false`.
See `EXPECTED.json` and `VALIDATION.json` for frozen hashes and controls.
Proof bytes may depend on the producer build; the regenerated CNF is fixed
and the proof must check against that exact CNF. Original executable hashes
are recorded. No solver binary, raw search log, large CNF, or DRAT file is
published here.

Optional search requires `python-sat==1.9.dev15` and its `cadical195` solver:

```bash
python3 search.py --repo .. --work /tmp/hn-a8-search --seconds 3600 --seed 20260914
```

This is a search, not a guaranteed finite-time resolution. Its positive
calibration and definition-level decoder checks are mandatory. Mutable search
outputs stay outside this package. Existing literal cuts can be resumed from
`cuts.jsonl` in the work directory. Do not interpret an unverified UNSAT search
status as a record certificate. A genuine non-four signal would still require
an ordinary full-graph proof and a checked proper five-colouring before any
record claim.

Trust boundaries: Python arbitrary-precision arithmetic; the hash-pinned
previously accepted geometry reader and exact point inputs; the published
complete 20-class L theorem; the stated finite CNF reduction and drat-trim's
proof checking. This is author verification, not independent review. Larger
replacement shapes, other completion pools, and global minimality are outside
scope.
