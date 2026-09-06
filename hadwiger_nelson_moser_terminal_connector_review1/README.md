# Independent review of the Moser–Parts terminal connector closure

Verdict: **accepted within its stated scope**.  The reviewed contribution is
Discovery Net artifact
`bafkreihbfz57u4lt66csgsmolfvvqh5on5n2ww2dss2e3miqzuvxszrcwu`, source
commit `7f2bf1d05d0c1595b47ae32751981031af6a5ce7`.

The result is a negative construction theorem, not a sub-509 five-chromatic
unit-distance graph.  It proves that one fixed double/single-contact terminal
class around the stated seven-point Moser spindle has a common four-colouring,
and hence that the corresponding terminal-only assemblies of full A159
gadgets are four-colourable under the private-interior and interface-edge
hypotheses.  It does not cover terminal triangles with only single contacts,
interior contacts, overlapping interiors, reduced gadgets, or arbitrary
placements of full gadgets.

## Mathematical audit

For every pair of distinct spindle vertices at distance below two, the two
unit-circle intersections exhaust the possible terminal points having those
two contacts.  For each such point `a` and each spindle point `m`, intersecting
the circle of radius `sqrt(7)` about `a` with the unit circle about `m`
exhausts the choices for a different contacting terminal `b`; the two
equilateral completions exhaust the third terminal.  The strict branch tests
exclude all tangencies.  Thus choosing two of a qualifying terminal's
neighbours and one neighbour of the different contacting terminal recovers
every triangle in the stated family, with harmless multiplicity.

The supplied label colouring is enough without an exact point-deduplication
claim.  For every same-colour label pair the independent checker proves its
squared distance is not one.  For every different-colour pair it proves the
points are distinct.  Hence exact aliases receive a single colour and no unit
edge is monochromatic.  Every represented equilateral triangle is also
non-monochromatic.

Finally, the archived A159 graph has 159 distinct points and 646 strict unit
edges in an independently implemented multiquadratic field calculation.  The
four canonical terminal patterns `001`, `010`, `011`, and `012` are proper;
palette renaming directly checks all 60 labelled non-monochromatic terminal
assignments.  A common interface colouring can therefore be extended inside
each private gadget independently, and the two assembly hypotheses cover all
remaining agreement and edge obligations.

## Independent computation

[`independent_check.py`](independent_check.py) imports none of the submitted
connector or field-arithmetic code.  Rational operations propagate exactly;
square roots use fresh outward enclosures with denominator `2^220`.  The A159
audit uses a generic multiplication table for the full basis
`1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165`.

Run from the repository root with Python 3.11+ and the standard library:

```sh
python3 -B hadwiger_nelson_moser_terminal_connector_review1/independent_check.py \
  --report /tmp/moser-terminal-review1.json
cmp /tmp/moser-terminal-review1.json \
  hadwiger_nelson_moser_terminal_connector_review1/result.json
sha256sum -c hadwiger_nelson_moser_terminal_connector_review1/SHA256SUMS
```

The independent run obtains 240 absent and 54 two-intersection second-anchor
branches, 216 labelled triangles, 655 labelled points, and 214,185 audited
label pairs.  It also checks the 646-edge A159 graph and all 60 relevant
terminal assignments.  The submitted producer, submitted direct checker, and
imported A159 positive-extension replay were separately run and matched their
pinned reports.

No SAT result, negative proof, floating-point predicate, exact count of
geometric point classes, or exact count of geometric triangle classes is
trusted.  Remaining trust lies in the unformalized circle-intersection and
gluing arguments, the pinned coordinate and colouring bytes, Python exact
integer/Fraction semantics, correct outward root rounding, complete finite
loops, and ordinary hardware.
