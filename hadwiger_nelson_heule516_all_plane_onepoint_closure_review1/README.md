# Independent review: whole-plane one-point closure of the Heule 516-core

Verdict: **accept with high confidence at the stated fixed-placement scope**.

The reviewed Discovery Net contribution is
`bafkreidrpgz7n2d5c4z7o4cifdreb7cchzft2ae7sbgkbgnlqlocr7cr7u`,
“All plane one-point augmentations of the fixed Heule 516-core are closed
through order 508,” at source commit
`4241a558b4f1279e2a8741202cc2bd2c93b3048c`.

The accepted statement is exactly this: fix the published placement of the
516-point, 2,538-edge Heule core `B`. For every plane point `q`, every subgraph
of the strict unit-distance graph on `B union {q}` with at most 508 vertices is
four-colourable. This closes a target-bearing one-point construction family.
It does **not** cover two added points, a moved or different base, or establish
a sub-509 five-chromatic unit-distance graph.

## Independent evidence

I first ran the complete author verifier in a fresh scratch directory. In 79.4
seconds it enumerated all 22,765,060 base triples, reconstructed 1,726 exact
centres, audited 890,616 centre/base incidences, matched 105,755 survivor
triples entry by entry, and checked the 558-point exterior colouring cover.
All four malformed-certificate controls rejected. I separately replayed the
h3991 H632-boundary checker; its 72 outside-H560 points have minimum deletion
coverage 508, and all four of its controls rejected.

The reviewer-owned [`independent_check.py`](independent_check.py) imports no
code from the reviewed package. It performs the decisive checks again:

1. It reconstructs all 632 exact H632 coordinates and all 3,112 strict unit
   edges directly in the squarefree basis. Restriction to `B` gives exactly
   the published 2,538-edge stream.
2. It treats the author's freshly generated centre rows as untrusted
   certificates and recomputes every exact incidence. The result is 1,726
   distinct centres, with denominators `96:1714, 288:12`, and exactly 558
   exterior centres of degree at least four.
3. [`third_filter.cpp`](third_filter.cpp) enumerates all 22,765,060 triples
   using the new moduli 1,001,219 and 1,001,459, rather than either modulus in
   the reviewed code. Their radical images and primality are checked at run
   time. The first image retains 105,776 triples; the second removes exactly
   21 false positives. The resulting 105,755-row stream is identical to the
   union of neighbour triples from the independently checked centres and has
   SHA-256
   `23f9790bff3809086d28d7ef983b56bb8cb7944c25d4e1fd9a7a6157414baa11`.
4. It decodes and directly checks all 1,075 exterior base-deletion words on
   2,717,716 base-edge incidences. Across 599,850 centre/word extension tests,
   the minimum number of covered deletions is exactly 508; the full histogram
   is `508:33, 509:14, 510:17, 511:20, 512:30, 513:39, 514:80, 515:115,
   516:210`.
5. It independently checks h3991's 664 deletion rows and 46 direct augmented
   rows for the 72 points in H632 outside H560. The remaining 44 H632 points
   lie in H560 and import the already independently accepted complete H560
   closure, Discovery ref
   `bafkreifbln2uuz67wbkaz3ae54j3jv5kfsqyh2wzinztiaxj7zrupmjb7e`.

Ordinary and optimized Python runs produced byte-identical
[`result.json`](result.json). Release and ASan/UBSan builds of the independent
filter produced byte-identical full survivor streams, and a malformed order-517
input was rejected.

## Mathematical implication

For squared side lengths `s,t,u`, a triangle has circumradius one precisely
when

```text
s*t*u = 2*s*t + 2*s*u + 2*t*u - s^2 - t^2 - u^2.
```

At coordinate scale 96 the right side gains a factor `96^2`. Exact zeros of
this squarefree-radical expression remain zero under either checked modular
radical evaluation. Therefore the independent filter is a sound exhaustive
superset filter. Three distinct points on a unit circle are noncollinear and
determine their centre uniquely; equality of its final stream with every
neighbour triple of the exact centre list proves that no degree-at-least-three
real centre is omitted.

If `q` has at most three neighbours in `B`, a four-colouring of a proper base
subgraph extends with a missing colour. Otherwise `q` belongs to the complete
finite centre census. A target of order at most 508 that contains `q` omits at
least nine of the 516 base vertices. Coverage at least 508 leaves at most eight
uncovered base vertices, so one omitted vertex has a checked colouring of
`B-v+q`; restriction colours the target. If `q` is absent, any checked
`B-v` colouring suffices. The verified h3991/H560 boundary cases and the
trivial `q in B` case complete the whole plane.

## Reproduction

From the repository root with CPython 3.11 or later and a C++20 compiler, use
fresh scratch paths outside the repository:

```sh
python3 -B hadwiger_nelson_heule516_all_plane_onepoint_closure/verify.py \
  --work /path/to/fresh-author-work --controls

g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow -pedantic \
  hadwiger_nelson_heule516_all_plane_onepoint_closure_review1/third_filter.cpp \
  -o /path/to/third-filter

python3 -B \
  hadwiger_nelson_heule516_all_plane_onepoint_closure_review1/independent_check.py \
  --repository . \
  --author-work /path/to/fresh-author-work \
  --third-filter /path/to/third-filter \
  --scratch /path/to/fresh-review-work \
  --report /path/to/review-result.json
```

Expected status is `INDEPENDENT_ACCEPT_CHECK_PASSED`, with independent filter
counts `22,765,060 -> 105,776 -> 105,755`, 558 exterior centres, and minimum
exterior and finite-boundary coverage 508.

## Trust boundary

The conclusion still trusts the SHA-256-pinned published coordinate and
colouring bytes; the independence of the eight squarefree basis elements;
CPython exact integer/Fraction and Base64 semantics; the independently
compiled C++20 exhaustive loop; compiler, OS, and hardware; and the previously
accepted fixed-H560 closure for 44 boundary points. The new modular constants,
implementation, and entrywise exact-incidence comparison materially separate
the main census check from the reviewed filter. No SAT result or solver search
completeness is trusted: every used colouring is checked directly. No
proof-assistant formalization is claimed.
