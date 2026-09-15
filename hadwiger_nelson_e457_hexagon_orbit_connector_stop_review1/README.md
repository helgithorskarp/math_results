# Independent review of the E457 paired-hexagon connector stop

**Verdict: accept as a scoped connector-relation stop, with a full-union
strengthening for the frozen support and an explicit scope correction.**

For two terminals at distance `8/3`, put one unit-radius regular six-point
orbit around each. In every placement there are at most two unit edges between
the two orbits. The two `C6` rims plus those contacts are three-colourable, so
the isolated 14-point support always has a proper four-colouring in which the
terminals agree. It therefore cannot supply the intrinsic different-terminal
relation required by the reviewed E457 composition argument.

The frozen maximal-contact realization independently reconstructs as 14
distinct points with all 26 unit edges, exactly two orbit-to-orbit contacts,
13 triangles, and chromatic number three. Its point and edge hashes match the
target exactly. The quarter-turned point
`(-sqrt(47)/24,23/24)` is genuinely outside the E457 rotated-field support.

## Full-union strengthening

The target deliberately stops before reconstructing incidental contacts with
E457. The review closes that gap for the frozen support. There are exactly two
plane isometries taking its ordered horizontal terminal pair to E457's ordered
vertical pair. For each one, an exact reconstruction in
`Q(sqrt(3),sqrt(11),sqrt(47))` finds:

- exactly 469 collision-merged points and 2,355 complete unit edges;
- exactly the two marked-terminal overlaps;
- no incidental unit edge between an E457-only and connector-only point; and
- a proper four-colouring extending the pinned E457 word, for every one of
  the six permutations of the connector's three nonterminal colours.

Thus both rigid embeddings of the frozen connector give actual four-colourable
plane unit-distance unions, not record candidates.

## Scope correction

An equal-terminal colouring of the isolated connector does not, by itself,
prove that every complete E457 union is four-colourable: incidental contacts
can invalidate it. The universal result therefore closes this orbit family as
an **intrinsic unequal-terminal connector**, which is the assigned preflight,
but it is not a global exclusion of every E457 union over all continuous orbit
phases. The review's 469-point/2,355-edge four-colour conclusion concerns only
the frozen support's two ordered-terminal embeddings.

This result is not five-chromatic, does not improve the supported 509-vertex
record, and says nothing about other at-most-53-point connectors, extra
orbits, radii, shells, or outside-field architectures.

## Independent method

`verify.py` imports no target code. It uses the nested representation
`Q(sqrt(3))[sqrt(47)]`, rather than the target's bitmask multiplication. For
the universal colouring relation it enumerates the complete 667-pattern
superset of zero, one, or two edges between two labelled six-cycles and checks
an explicit 52-word bank made from binary rim colourings with at most one
third-colour repair. Exactly 343 patterns are bipartite and 324 are strictly
three-chromatic; every pattern has a bank witness.

`union_check.py` is a separate exact model with the eight square-free basis
elements of `Q(sqrt(3),sqrt(11),sqrt(47))`. It imports neither target code nor
the isolated review model. It reads only the hash-pinned E457 coordinate and
colour certificate, collision-merges each alignment, rebuilds all pairwise
unit distances, and validates the positive union words.

## Reproduction

CPython 3.11 or later and only the standard library are required:

```bash
cd hadwiger_nelson_e457_hexagon_orbit_connector_stop_review1
sha256sum -c SHA256SUMS
python3 -B verify.py | diff -u EXPECTED.json -
python3 -O -B verify.py | diff -u EXPECTED.json -
python3 -B union_check.py | diff -u UNION_EXPECTED.json -
python3 -O -B union_check.py | diff -u UNION_EXPECTED.json -
python3 -B controls.py | diff -u VALIDATION.json -
```

Public source:
<https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_e457_hexagon_orbit_connector_stop_review1>.
Verified mathematical commit:
`48ac659cd8e9ed5323000cae785e3cdcad3b6718`.

The trust boundary is the two short universal arguments in `PROOF.md`, the
hash-pinned target and E457 input bytes, the two review programs, CPython exact
integer/`Fraction`/JSON/SHA-256 operations, and ordinary hardware. No solver,
floating-point predicate, omitted trace, or proof assistant is used.
