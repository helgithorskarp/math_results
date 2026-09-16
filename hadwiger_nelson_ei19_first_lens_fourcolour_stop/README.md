# The complete first EI19 lens closure is four-chromatic

Take the exact 19-point Exoo--Ismailescu realization certified in the sibling
[`hadwiger_nelson_ei19_terminal_boundary`](../hadwiger_nelson_ei19_terminal_boundary/README.md).
For every unordered pair of distinct source points at distance strictly below
two, adjoin **both** intersections of their unit circles.  Merge all actual
collisions and include every unit pair in the resulting physical support.

The complete strict unit-distance graph of this support has chromatic number
exactly **four**.  There are 165 eligible source pairs and hence 349 formal
labels: 19 source labels and 330 lens labels.  Thus the collision-merged graph
has at most 349 physical points.  A solver-free interval checker proves that a
literal four-colour word descends through every collision and is proper on
every actual unit edge.  The embedded EI19 source supplies the matching lower
bound.

This is a scoped negative construction result, not a sub-509 record candidate.
It closes the one predeclared all-pairs first-lens architecture for this fixed
EI19 realization.  It does not classify a second closure round, selected lens
subsets with added points, other EI19 realizations, other source graphs, or
arbitrary plane unit-distance graphs.  The architecture stops here; none of
those neighbouring variants was searched.

## Why this is the complete physical graph

The source coordinates are the unique real root in the published rational
box of radius `10^-25`.  The sibling contraction checker is hash-pinned and
replayed.  For every source pair, outward intervals decide whether its squared
distance is below or above four; no pair is tangent or unresolved.  For an
eligible pair `a,b`, both generated labels are enclosed from the exact formula

```text
(a+b)/2 +/- i(b-a) sqrt(1/|b-a|^2 - 1/4).
```

For every one of the `C(349,2)=60,726` formal label pairs, the checker proves
one of two obligations:

- differently coloured rectangles are disjoint on at least one coordinate,
  so labels that denote the same physical point receive the same colour;
- equal-coloured rectangles have squared-distance interval excluding one, so
  no actual unit pair is monochromatic.

These obligations conservatively dominate every collision and every possible
extra unit contact.  They avoid a tolerance-based edge list and do not require
deciding the exact number of merged points or edges.

The numerical selector happened to merge the labels into 247 tolerance groups
with 559 detected unit pairs.  Those two numbers are discovery diagnostics
only and are not part of the theorem.

## Reproduction

Python 3.11 or later and the standard library suffice.  From the repository
root run

```bash
python3 -B hadwiger_nelson_ei19_first_lens_fourcolour_stop/verify.py --check-expected
python3 -O -B hadwiger_nelson_ei19_first_lens_fourcolour_stop/verify.py --check-expected
python3 -B hadwiger_nelson_ei19_first_lens_fourcolour_stop/controls.py
sha256sum -c hadwiger_nelson_ei19_first_lens_fourcolour_stop/SHA256SUMS
```

Expected status:

```text
EXACT EI19 FIRST LENS CLOSURE FOUR-COLOUR STOP VERIFIED
```

The checker pins and replays the sibling source certificate, reconstructs all
349 outward boxes from the definition, validates the word on all formal pairs,
and independently exhausts source three-colourings.  No SAT result,
floating-point comparison, guessed algebraic field, omitted edge list, or
unpublished dataset is a proof premise.  `controls.py` rejects altered word,
collision, edge, alphabet, length, and geometry inputs.

## Scope and campaign status

The source's previously published ten-terminal relation is neutral.  The
present theorem is different: it decides one global whole-support operation,
not another terminal census.  The exact four-word triggers the campaign's
immediate stop rule, so there is no second layer or finishing search.

Parts's 509-point graph remains the supported unrestricted published record.
This package supplies author-side exact evidence for a failed construction and
makes no record, novelty-priority, or independent-review claim.
