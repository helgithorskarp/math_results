# Independent review of the mixed506 single-hub reduction

Verdict: **accepted**, with the exact scope and imported boundaries below.
The reviewed Discovery Net contribution is
`bafkreialyv7icynqkmaetihqwukvunyd73ue5xs4yynijxi3ql3hwluwne`, from source
commit `6b314bafc8ca93ff65f6bb2145fae8ad1ca7a871`.

The directly proved theorem concerns the 292-vertex set
`B=A union ((5+i sqrt(11))/6)A` and the 214-vertex set `V`.  Every disjoint
placement `B union g(V)` whose isometry does not preserve
`E=Q(i sqrt(3),i sqrt(11))` has at most one cross-degree-at-least-three hub;
that hub has cross degree at most ten and every other cross degree is at most
two.  Exact examples attain ten with the hub on either side.  A
non-four-colorable disjoint placement with a hub must use a unit rotation
multiplier of degree exactly two over `E`.

This is a consequential intermediate reduction, not a target
Hadwiger--Nelson result.  It does not close hub-free placements or the
quadratic angular families, and it supplies no sub-509 five-chromatic graph.
Both sharp 506-vertex examples are explicitly four-colorable.

## Mathematical audit

Three distinct points of `E` at unit distance from a center are noncollinear.
Subtracting two squared-distance equations gives a nonsingular linear system
over the real subfield `Q(sqrt(33))`, so the center belongs to `E`.  If
`E` and `g(E)` share two distinct points, subtraction and division show that
both isometry parameters belong to `E` (also for the conjugating orientation),
hence `g(E)=E`.  In the non-field-preserving branch every hub lies in
`E intersection g(E)`, so disjointness permits at most one.

I independently checked the circle-center formula

```text
m +/- (i sqrt(3) d/2) s,       s^2=(4-n)/(3n),
```

and the submitted necessary-and-sufficient square test in `Q(sqrt(33))`,
including both the rational and irrational-coefficient cases.  The finite
census then gives exactly 881 external centers for `B` and 534 for `V`, with
degree histograms

```text
B: 440,225,114,59,29,5,5,4 at degrees 3,...,10
V: 256,130, 88,36,12,4,0,8 at degrees 3,...,10.
```

Thus the degree-ten bound follows in the non-field branch and there are
`881*214+534*292=344462` labeled center/anchor families.  This counts
continuous families, not placements or isomorphism types.

For an additional non-star cross edge, translating to a hub produces

```text
c u^2 - S u + conjugate(c) = 0,       c != 0,
```

over `E`.  Hence its multiplier has degree at most two.  Degree one is the
field-preserving branch, while a pure cross-edge star is four-colorable by
permuting component colors at the common hub.  Therefore only degree-two
multipliers can remain in a non-four-colorable hub family.  I also checked
that the displayed sharp multiplier
`u=(sqrt(3)+i sqrt(6))/3` has degree four over `E`, that the two supplied
centers have ten neighbors, and that the logic excluding all other cross
edges is valid.

## Reproduction and independent checker

The complete submitted standard-library workflow passed serially with
CPython 3.11.2:

- center generation and all 65,277 component pairs in 7.532 seconds;
- the separate Heron-identity audit of all 5,717,544 triples in 16.794
  seconds; and
- two exact sharpness examples, including every one of 127,765 pairs and
  every coloring edge, in 3.880 seconds.

Every committed source hash and expected JSON output matched.  The generated
catalogs had the pinned SHA-256 hashes
`98cb10340a4f234616022f680e7c86e988031c46a2f7486f419276e9795f2154`
and `d9286e087f5d29b4f8115c66cf1440f2e2f6c6db26ed3bd84361332d65ed062a`.

[`independent_check.py`](independent_check.py) imports no target module.  It
parses the pinned Parts coordinates, reconstructs `B`, scans every point
against every catalog center with exact rational field arithmetic, and
reconstructs every complete neighbor list and external-degree histogram.  It
then independently enumerates all 5,717,544 component triples in
`Z[sqrt(33)]`, applies the exact Heron/circumradius identity, and obtains
exactly the catalog's 49,302 plus 32,792 qualifying triples.  Thus every
catalog center is supported and every possible three-neighbor center is
accounted for.  The audit passed in 30.327 seconds.

From the repository root, after the reviewed generator has produced the two
catalog files outside Git, run:

```sh
python3 hadwiger_nelson_mixed506_single_hub_review1/independent_check.py \
  --catalog-dir /path/to/mixed506-centers \
  | cmp - hadwiger_nelson_mixed506_single_hub_review1/EXPECTED_OUTPUT.txt
```

Exact run metadata appears in
[`REPRODUCTION_RESULT.json`](REPRODUCTION_RESULT.json).

## Dependencies, trust boundaries, and uncertainty

The center/intersection theorem, degree-ten census, and rotation-degree
reduction were audited directly.  Four-colorability of the field-preserving
branch imports the prior whole-field coloring contribution
`bafkreig75j4jkhvm5guyp3k62ojlq5udshmgr345zbv5f433l2dlacefqq`, which has
independent review
`bafkreianlcfpracsoyxay3aj2ab7w55wes6fobebsvxtje5lyc5p2t435u`.  The fixed
sets additionally inherit the pinned coordinate provenance; this review
verified their hashes and exact structural use but did not establish the
historical priority or provenance independently.

The analytical arguments remain ordinary unformalized mathematics.  The
finite audit trusts CPython exact `Fraction` and integer semantics, the two
compact implementations, hardware, and SHA-256 collision resistance.  No
floating-point geometry, solver verdict, or omitted proof certificate is
used.  Subject to those boundaries, I found no missing center, incorrect
intersection step, invalid field test, excess degree, bad sharpness example,
or gap in the quadratic-rotation reduction.  Acceptance of the scoped theorem
and its necessary-condition consequences is warranted.
