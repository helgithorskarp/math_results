# Independent review: separated dominating triples

## Verdict

**ACCEPT with high confidence, with one minor continuum-definition
clarification and the stated strict boundary.**

The theorem in
[`hadwiger_nelson_separated_dominating_triples`](../hadwiger_nelson_separated_dominating_triples/README.md)
at mathematical source commit `7feac98a1aac9b819b63835ad7b524a25f23be39`
is correct:

> If `a0,a1,b` are distinct plane points and `|a0-a1|>3`, then the strict
> unit-distance graph on the three centres and their three complete unit
> circles is four-colourable. The bound four is attained.

It follows that every pair in a dominating triple of a non-four-colourable
plane unit-distance graph is at distance at most three. Together with the
separately reviewed theorem that such a triple cannot contain a unit edge,
every dominating triple in a five-chromatic plane unit-distance graph is an
independent set of diameter at most three.

This is a global structural restriction on actual plane unit-distance graphs,
not a finite sample or an abstract chromatic graph. It is not a vertex lower
bound or a smaller five-chromatic construction. The theorem deliberately does
not include centre distance exactly three or triples of diameter below three.
Parts' realized 509-vertex, 2,442-edge graph remains the published unrestricted
record
([Parts](https://arxiv.org/abs/2010.12665),
[Haugland](https://arxiv.org/abs/2608.04542)).

## Continuum proof audit

Let `C(c)` denote the unit circle centred at `c`. If a point of `C(a0)` and a
point of `C(a1)` were unit-separated, the resulting three-edge chain would
give `|a0-a1|<=3`. Thus under the strict hypothesis there is no unit edge
between the two leaf circles. This is the only use of the constant three.

Every unit circle decomposes into six-cycles under rotation through 60
degrees. Give the leaf circles palette `{0,1}` and `C(b)` palette `{2,3}`.
Pin `b,a0,a1` to `0,2,3`. Multiple-owner points can occur only in

```text
Mi = C(ai) intersection C(b).
```

For two intersecting unit circles whose centres are distance `d` apart, their
intersection chord satisfies `|p-q|^2=4-d^2`. The exact six-cycle chord table
is `0,1,3,4,3,1`. Equal binary prescriptions at both intersections therefore
fail only for `d^2=3`; the other odd case gives coincident centres. Away from
`sqrt(3)`, both intersections may use leaf colour 1. When `d=sqrt(3)`, the
two intersections form an edge; assigning one to each palette leaves only
one leaf prescription.

The central circle receives at most two prescriptions. A separation-one
event fixes centre `ai` on `C(b)`; a `sqrt(3)` event lets either endpoint of
an edge be selected. Two fixed events are impossible because they would give
`|a0-a1|<=2`. If the prescriptions lie in different six-cycle orbits, their
phases are independent. If they share an orbit, at least one selectable edge
has one endpoint of each parity, so an endpoint can always be chosen to meet
the required same/different colour relation. With two selectable disjoint
edges, either parity relation is likewise available.

This makes every same-palette unit edge proper: leaf-palette points either
share one binary-coloured leaf circle or lie on different leaf circles, which
have no cross edge; central-palette points all lie on `C(b)`. Different
palettes are disjoint in colour. The prescribed colours separately cover
every edge incident with a centre. Hence the argument colours the entire
uncountable strict support, not merely its finitely many intersections.

To make the construction fully explicit, choose one representative of every
six-rotation orbit by requiring its argument relative to its owner to lie in
the half-open sector `[0,pi/3)`, then assign the selected orbit phase. The
target proof says the remaining orbit phases may be chosen independently but
does not spell out this representative convention. This is a minor
definition-level clarification, not a gap in existence or edge coverage.

Every graph dominated by the three centres embeds as a subgraph of this
strict support: each noncentre vertex is adjacent to some centre and hence
lies on its unit circle, while every graph edge is present in the strict unit
graph. This proves the stated domination corollary without an induced-graph
assumption.

## Independent exact evidence

`independent_audit.py` imports no target module and reads no target
certificate. It uses a different finite representation:

- it enumerates all 64 binary words on `C6`, rather than trusting parity
  formulas;
- it tests every same-orbit fixed-anchor/selectable-edge placement directly
  against the two proper words, obtaining 11 cases and 14 valid endpoint
  pairs;
- it reconstructs the sharpness graph from the formulas
  `u=1`, `v=(1+i*sqrt(3))/2`, and `rho=(5+i*sqrt(11))/6` in an independently
  implemented bit-mask basis for `Q(sqrt(3),sqrt(11))`;
- it derives all 21 strict distances, the 11 Moser-spindle edges, domination
  by vertices `0,u+v`, non-three-colourability by all 2,187 labelled
  assignments, and an independent proper four-colouring;
- it checks that adjoining the distinct centre `4` gives a centre-pair square
  distance 16 and places the whole spindle inside the three-circle support.

The exact distance-three probe retains the collinear chain `0--1--2--3`.
Thus at the excluded boundary there really is a cross-leaf unit edge. This
does not show the boundary support is non-four-colourable; it confirms only
that the submitted no-cross-edge proof cannot silently include equality.

Semantic controls reject equal colouring of the two `sqrt(3)` endpoints and
an incompatible adjacent central prescription. They also delete each of the
11 spindle edges in turn and recover a three-colouring every time, detecting
any omitted edge in the sharpness certificate.

The target manifest passes. Its certificate regenerates byte-for-byte;
ordinary and optimized target verifiers agree apart from reported runtime;
five malformed target certificates reject. The independent audit and controls
also agree in ordinary and optimized modes.

## Reproduction and trust boundary

Using CPython 3.11 or later and only the standard library, run from the
repository root:

```sh
python3 -B hadwiger_nelson_separated_dominating_triples_review1/independent_audit.py \
  --check-expected
python3 -O -B hadwiger_nelson_separated_dominating_triples_review1/independent_audit.py \
  --check-expected
python3 -B hadwiger_nelson_separated_dominating_triples_review1/controls.py
sha256sum -c hadwiger_nelson_separated_dominating_triples_review1/SHA256SUMS
```

The review trusts exact Python integer/`Fraction` arithmetic, inspection of
the exhaustive loops, the elementary circle-intersection formula, and the
written passage from orbit prescriptions to all support edges. It does not
use floating-point predicates, numerical sampling, SAT/CAS output, or a
finite graph as a substitute for the continuum quantifier.

At review selection, the target Discovery Net contribution
`bafkreicilsrv4kdxphxwlpmfdzqggcqtk64fhre34rtslr5eoe64xlq4hm` was accepted
for broadcast but absent from the stale height-4363 ledger. The committed
two-centre predecessor had no attached objection. A targeted literature
search found no matching exact theorem, but no novelty-priority claim is made.
