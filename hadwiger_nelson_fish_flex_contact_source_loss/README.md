# An exact flexible-fish self-contact loses a complete source colouring

This package certifies one isolated self-contact in the flexible
Hochberg--O'Donnell fish.  The exact support has **23 distinct plane points**
and its complete strict unit-distance graph has **43 edges**: the 42 fish
edges and exactly the additional edge `(10,21)`.  The complete graph is
exactly four-chromatic.

The result is a strict **complete-input source loss**, not a terminal
projection statistic.  The word

```text
01110021022330110210021
```

is a proper four-colouring of the entire 23-vertex, 42-edge fish, but it gives
vertices 10 and 21 the same colour and therefore does not lift to the
self-contact graph.  The word

```text
01110021022330110210012
```

is a proper four-colouring of the complete 43-edge physical graph, so the
event is nonvacuous.  An exhaustive three-colour search on the fish subgraph
visits 541 nodes and returns UNSAT; together these checks prove chromatic
number exactly four for both graphs.

This passes a narrow construction-intake gate: a plane-native global flex can
make an actual new unit contact that eliminates a complete colouring of its
necessarily used four-chromatic source.  It is **not five-chromatic, not a
candidate below the 509-point record, and not a record advance**.  No host or
cap-feasible route from this single lost edge to five-chromaticity is claimed.
The selected event is frozen; neighbouring contact events and other flex
parameters are outside scope.

## Exact support

The vertex labels are

```text
(A,B,p0,...,p10,q0,...,q4,r0,...,r4) = (0,...,22).
```

Vertices 0 and 1 are fixed at `(0,0)` and `(1,0)`.  The remaining 42 real
coordinates are the unique solution in the certified rational box to the 41
non-fixed fish edge equations and the self-contact equation

```text
|v10-v21|^2 = 1.
```

The box midpoint has denominator `10^50` and infinity radius `10^-25`.
[geometry_certificate.json](geometry_certificate.json) contains the midpoint,
the rational approximate inverse, all equations and the two colour words.
[verify.py](verify.py) proves root existence and uniqueness by contraction,
then checks all 253 point pairs exactly.  It proves there are no collisions
and no other unit contacts.  The rational midpoint is only an approximation;
the exact support is the unique real root isolated by the certificate.

The discovery approximation is

```text
t = -0.155471806259872530069869445946884598169641880386070041364744417916797045476902794518284971
```

but floating-point proximity is not a proof premise.  See [PROOF.md](PROOF.md)
for the exact argument and [PROVENANCE.md](PROVENANCE.md) for the source graph
and parameterization.

## Reproduction

The proof checker uses Python 3.11 or later and the standard library only:

```bash
python3 -B verify.py
python3 -O -B verify.py
python3 -B controls.py
sha256sum -c SHA256SUMS
```

Both verifier modes must reproduce [EXPECTED.json](EXPECTED.json).  The
controls alter the inverse, midpoint, edge set, radius, target and colour
words; all eight mathematical corruptions must be rejected without using file
hashes.

Optional byte-identical regeneration of the positive rational certificate
uses the pinned discovery dependency:

```bash
python3 -m venv /tmp/fish-flex-venv
/tmp/fish-flex-venv/bin/pip install -r requirements-discovery.txt
fresh_output=/tmp/fish-flex-geometry-certificate.json
/tmp/fish-flex-venv/bin/python build_certificate.py "$fresh_output"
cmp geometry_certificate.json "$fresh_output"
```

Regeneration locates the numerical root and rounds a midpoint and inverse.
Its output becomes evidence only after the exact standard-library checker
accepts it.

## Scope and campaign relevance

The result concerns one 23-point root of one fish flex.  It does not classify
all self-contacts, all fish flexes, or higher-arity colour relations.  It does
not imply that adding one more plane-native condition will make the graph
five-chromatic.  A future continuation would require a separately declared
exact global mechanism whose first complete support stays within 508 points
and yields further complete-input loss or an ordinary non-four signal; the
present package deliberately does not launch such a sweep.

Parts's strict 509-point construction remains the supported unrestricted
vertex record: [Parts, *A small 5-chromatic unit-distance graph in the
plane*](https://arxiv.org/abs/2010.12665).
