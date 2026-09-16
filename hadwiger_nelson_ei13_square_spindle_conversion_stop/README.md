# EI13 square-side spindle conversion: exact four-colour stop

The one frozen conversion of Exoo--Ismailescu's 13-point
`{1,sqrt(2)}` carrier produces **334 exact physical points and 851 complete
unit edges, with chromatic number exactly four**. The literal four-colouring
fails five of the carrier's fourteen diagonal inequalities. This construction
is not a five-chromatic unit-distance graph or a sub-509 record candidate.

The carrier's original two-distance graph is five-chromatic. That statement
is checked here but does not transfer to the constructed unit graph.

## Frozen construction

Use the 13 coordinates and label order from the second proof of Theorem 3.1
in [Exoo--Ismailescu, arXiv:1805.06055v1](https://arxiv.org/html/1805.06055v1).
Keep its 20 unit pairs. For each of its 14 distance-`sqrt(2)` pairs `A,B`,
in increasing source-label order, add the two other corners of its unit square:

```
C = (A+B)/2 + i(B-A)/2
D = (A+B)/2 - i(B-A)/2.
```

Use the directed square sides `A->D->B->C->A`, and also every original unit
pair directed from the smaller source label to the larger. On each directed
unit side `A->B`, put a Moser spindle with

```
H = (A+B)/2 - i sqrt(11)(B-A)/2,
(H+X)/2 +/- i(H-X)/(2 sqrt(3)),  for X=A,B.
```

Each spindle adds at most five points beyond its side endpoints. The budget
was fixed before chromatic testing:

```
13 + 2*14 + 5*(20 + 4*14) = 421 <= 508.
```

All coordinates lie in `Q(sqrt(3),sqrt(7),sqrt(11))^2`. Collision merging
leaves 29 square-base points and 334 final points. The 76 spindle occurrences
use 61 distinct directed sides. Inherited unit edges number 662; full
reconstruction supplies another 189. All 55,611 final unordered pairs are
tested exactly. No diagonal of length `sqrt(2)` is included as a unit edge.

The spindle attachments are not asserted to be diagonal-inequality gadgets.
The test was whether their complete physical interaction could enforce the
carrier's obstruction. A complete four-word answers this negatively for the
declared assembly.

## Reproduce

The certificate checker uses Python's standard library only; validated with
CPython 3.11.2. Run from this directory:

```sh
python3 -B verify.py
python3 -O -B verify.py
python3 -B controls.py
python3 -O -B controls.py
```

Both verifier outputs equal `EXPECTED.json`. To materialize the exact point
and edge streams used in the decision:

```sh
python3 -B verify.py --write-graph /tmp/ei13-square-spindle-graph
```

The point stream uses 16 integer coefficients per row, denominator 96, in the
ordered radical basis `(1,sqrt3,sqrt7,sqrt21,sqrt11,sqrt33,sqrt77,sqrt231)`
for `x`, then for `y`. Points are sorted by these coefficient tuples. Edges
are sorted zero-based pairs. Each row is comma-separated with one LF.

- Point SHA-256: `58c261607a170c48c5b17c124eac1c72ddea1d33fb3ef15e894c45884b08bb2f`
- Edge SHA-256: `5d83ee1f95209d681d806eb081889a9af49164e02e5689c96ea756c6fb55efac`

Optional regeneration of the SAT witness requires `requirements-producer.txt`:

```sh
python3 produce.py --output-dir /tmp/ei13-square-spindle-produced
python3 -B verify.py --certificate /tmp/ei13-square-spindle-produced/certificate.json
```

`produce.py` uses rational bitmask field arithmetic and constructs circle
intersections. `verify.py` imports no producer code: it uses expanded affine
spindle coordinates and integer actual-radicand arithmetic. Their point and
edge streams agree entry by entry. The final word requires no SAT trust;
the lower bound comes from exhaustive three-colour checking of an embedded
seven-point spindle. See `PROOF.md` and `VALIDATION.json`.

## Exact scope

This is an author-side reproducible construction stop, not independent peer
review. It covers precisely the square completions, directed sides, spindle
frames and whole union specified above. It establishes no exclusion for
other conversions of this carrier, other terminal gadgets, changed frames,
additional points or arbitrary plane unit-distance graphs. No nearby
carrier/gadget/frame sweep was performed after the checked four-word.
