# The radius-two Golomb direction ball is four-chromatic and pair-neutral

Let `G` be the exact ten-point Golomb graph.  Take the nine unoriented unit
directions occurring on its eighteen edges, include both signs, and call the
resulting eighteen-element set `U`.  This package studies the exact physical
support

```text
S = {a+b : a,b in {0} union U}.
```

Equal coordinates are merged and every actual unit edge between distinct
physical points is reconstructed.  The result has **163 points and 648 unit
edges**.  It contains the original Golomb graph and is therefore not
three-colourable.  The supplied proper four-colourings prove that its ordinary
chromatic number is exactly four.

The stronger construction gate is negative:

1. Normalize the unit triangle formed by Golomb vertices `0,1,2` to colours
   `0,1,2`.  There are exactly 95 proper four-colour patterns on the full
   Golomb graph, and every one extends to the complete 163-point graph.
2. For every physical nonedge `{u,v}`, one saved proper four-colouring has
   `colour(u)=colour(v)` and another has `colour(u)!=colour(v)`.

Thus the whole radius-two ball does not restrict the unrestricted four-colour
relation of its embedded Golomb source, and it has no forced-equal or
nonedge-forced-different pair.  In particular it supplies no forced-equality
half for a capped two-copy spindle completion.  This is an exact scoped stop,
not a five-chromatic construction or a global Hadwiger--Nelson result.

## Exact coordinates and completeness

Arithmetic is performed in

```text
Q(sqrt(33), i*sqrt(3), i*sqrt(11)).
```

A coefficient tuple `(a,b,c,d)` denotes

```text
a + b*sqrt(33) + c*i*sqrt(3) + d*i*sqrt(11).
```

The verifier reconstructs the ten Golomb points from their displayed rational
rows, derives the unit directions from the complete eighteen-edge source
graph, constructs and collision-merges all two-letter sums, and tests all
`C(163,2)` pairs for exact squared distance one.  No inherited or tolerance
edge set is used.

The certificate contains only positive witnesses: 95 extensions of the
normalized Golomb patterns, 85 proper colourings covering equality on all
12,555 nonedges, and 23 proper colourings covering separation on all
nonedges.  The standard-library verifier checks every word directly against
all 648 edges.  Solver UNSAT answers are not theorem premises.

## Reproduce

Python 3.11 or later and its standard library suffice to check the theorem:

```bash
python3 -B hadwiger_nelson_golomb_direction_ball/verify.py --check-expected
python3 -O -B hadwiger_nelson_golomb_direction_ball/verify.py --check-expected
python3 -B hadwiger_nelson_golomb_direction_ball/controls.py
(cd hadwiger_nelson_golomb_direction_ball && sha256sum -c SHA256SUMS)
```

To regenerate the positive witnesses, provide a CaDiCaL executable and write
to a fresh path:

```bash
python3 -B hadwiger_nelson_golomb_direction_ball/build_certificate.py \
  --solver /path/to/cadical --output /tmp/golomb-direction-ball.json
cmp /tmp/golomb-direction-ball.json \
  hadwiger_nelson_golomb_direction_ball/certificate.json
```

## Scope and campaign consequence

This closes only the frozen radius-two word ball of the exact Golomb unit
directions.  It does not classify other direction sets, word lengths, weighted
sums, nonlinear deformations, or arbitrary plane unit-distance graphs.  No
adjacent radius or generator sweep is inferred from the negative result.

The construction was admitted because it is plane-native, collision-capped in
advance, globally couples all unit directions of a four-chromatic source, and
retains that source.  Its complete unrestricted relation is nevertheless
neutral at both the embedded-source and pair levels, so the current campaign
gate requires changing architecture rather than enlarging this ball.

Parts's 509-point construction remains the supported unrestricted published
record.  Restricted-family exclusions, abstract chromatic graphs, and this
four-chromatic support do not alter that comparison.
