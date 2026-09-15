# Independent review of the flexible-fish difference-body stop

Verdict: **accept, with an exact-source and exact-operation limitation**.

An independent exact interval checker confirms that the complete ordered
difference body

```text
F-F = {p_i-p_j : 0 <= i,j < 23}
```

of the reviewed flexible-fish self-contact realization has between **433 and
507 physical points** and complete strict unit-distance chromatic number
exactly **four**.  The construction is therefore not five-chromatic and does
not improve Parts's 509-point record.

## Independent result

The target uses a single midpoint-expansion bound.  This review instead forms
exact rational coordinate intervals for every one of the 529 formal
addresses, uses endpoint interval subtraction and squaring, and checks all
139,656 unordered address pairs.  It independently reproduces:

```text
possible collision components       433
possible-unit supergraph edges      1,646
supergraph SHA-256                   4584d4b3a39e3c85d7712184f418af6386474b4fb702e368e5440560d6682649
proper target four-colouring         yes
```

The 433 component sizes are 372 singletons, 46 pairs, 14 triples, and one
23-address diagonal class.  Different classes have certified squared
separation greater than `399/1000000`; every excluded possible-unit pair has
squared-distance gap greater than `17/1000000`.  Thus every actual collision
is internal to a colour class and every actual unit edge is represented in
the checked supergraph.

For the lower chromatic bound, every fixed-second-coordinate fibre is a
translated copy of the independently reviewed 23-point, 43-edge,
four-chromatic source.  A separate fixed-order search again proves that graph
non-three-colourable.  The 23 fibres cover the support and share the exact zero
point, which also proves that the actual quotient graph is connected.  Because
the source has no bridge, the actual graph is bridgeless as well.

## Reproduction

CPython 3.11 or later and a complete repository checkout suffice.  Only the
standard library is used:

```sh
python3 -B hadwiger_nelson_fish_flex_contact_review1/verify.py --check-expected
python3 -B hadwiger_nelson_flex_fish_difference_fourcolour_review1/verify.py --check-expected
python3 -O -B hadwiger_nelson_flex_fish_difference_fourcolour_review1/verify.py --check-expected
python3 -B hadwiger_nelson_flex_fish_difference_fourcolour_review1/controls.py
(cd hadwiger_nelson_flex_fish_difference_fourcolour_review1 && sha256sum -c SHA256SUMS)
```

The controls perform 8,235 interval sample checks, compare the colouring
engine with brute force in 1,024 graph/palette cases, and reject four colouring
certificate corruptions.  [PROOF.md](PROOF.md) gives the complete reduction,
[REVIEW.md](REVIEW.md) states the verdict and limitations, and
[PROVENANCE.md](PROVENANCE.md) pins the source chain.

## Exact limitations

This accepts only the complete ordered difference body of the one exact
self-contact root fixed by the reviewed geometry hash.  It does not classify
another fish flex, nearby contact, partial difference set, sum, rotation,
shell, or additional copy.  The conservative 433-vertex graph need not be the
actual physical graph: unresolved addresses within a component may be equal
or distinct, and possible-unit supergraph edges may be false positives.

Accordingly, the exact physical order remains the interval `433..507`; no
five-chromatic or global Hadwiger--Nelson conclusion follows.  Parts's
published 509-point construction remains the supported unrestricted vertex
record in the bounded 2026-09-15 primary-source check.
