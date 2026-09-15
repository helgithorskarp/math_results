# Exact gate for a two-anchor dominated-Moser E457 connector

## Result

This package rejects one requirement-first complement architecture for the
457-point E457 equal-pair source.  Take the displayed seven-point Moser
spindle and ask for two marked points `O,V` such that every spindle vertex is
at unit distance from at least one of `O,V`.  If `O,V` had the same colour in
a proper four-colouring, their common colour would be unavailable throughout
the four-chromatic spindle.  Such a support would therefore force `O,V`
different.

No such two points exist for this exact Moser realization.  More strongly:

> The only points having at least three unit-distance neighbours in the
> displayed spindle are the seven spindle vertices themselves, and the union
> of the open neighbourhoods of any two of those vertices has size at most
> six.

Consequently two unit circles cannot cover all seven spindle vertices.  The
failure is independent of the desired terminal distance, so in particular
there is no connector of this form with `|O-V|=8/3`.

This is an exact restricted construction gate, not a five-chromatic graph, a
global exclusion of at-most-53-point connectors, or progress below the
509-point record.  The architecture stops before an E457 union exists, so it
does not reach the required outside-E457-field stage.  Other four-chromatic
cores, other ways of coupling a Moser spindle to the terminals, and arbitrary
outside-field connectors remain unclassified.

## Exact support and proof

A coordinate row `(a,b,c,d)` denotes

```text
((a+b*sqrt(33))/12, (c*sqrt(3)+d*sqrt(11))/12).
```

The seven rows are

```text
( 0, 0, 0, 0)  (12, 0, 0, 0)  ( 6, 0, 6, 0)
(18, 0, 6, 0)  (10, 0, 0, 2)  ( 5,-1, 5, 1)
(15,-1, 5, 3)
```

For a row difference `(a,b,c,d)`, squared distance is exactly

```text
(a^2+33b^2+3c^2+11d^2 + 2(ab+cd)*sqrt(33))/144.
```

The checker reconstructs the 11 unit edges and verifies directly that the
graph is not three-colourable and has a proper four-colouring.

Now let a point have at least three spindle vertices at unit distance.  Pick
three such neighbours.  They lie on its unit circle.  For every one of the
35 vertex triples, the checker evaluates the circumradius without solving a
floating circle equation.  If `a,b,c` are the three squared side lengths,
then

```text
16*area^2 = 2(ab+bc+ca)-a^2-b^2-c^2,
R^2 = abc/(16*area^2).
```

All arithmetic lies in `Q(sqrt(33))`.  No triple is collinear; exactly ten
triples have `R=1`.  For each, its unique unit circumcentre is one of the
seven displayed spindle vertices.  Their complete open neighbourhood sizes
are six times three and once four.  All 21 centre pairs are then checked;
their maximum neighbourhood-union size is six.

This enumeration is complete: any point with at least three unit neighbours
is the unique circumcentre of one enumerated noncollinear triple.  If two
points covered all seven spindle vertices, neither could have at most two
neighbours because the other has at most four.  Both would therefore occur
in the enumerated list, contradicting the 21-pair check.

## Reproduction

CPython 3.11 or later and only the standard library are required.  From the
repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  hadwiger_nelson_e457_dominated_moser_gate/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -O -B \
  hadwiger_nelson_e457_dominated_moser_gate/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  hadwiger_nelson_e457_dominated_moser_gate/controls.py
(cd hadwiger_nelson_e457_dominated_moser_gate && sha256sum -c SHA256SUMS)
```

`verify.py` uses the squared-side/circumradius calculation above.  The
separate discovery program used full coordinate-field linear algebra to
solve the circumcentre equations; its seven centres and incidence sets agree,
but that exploratory implementation is deliberately not part of the theorem
package.  The published checker, explicit proof, exact rational arithmetic,
and ordinary Python runtime are the trust boundary.  Seven controls exercise
field arithmetic, the radius identity, unit/nonunit distances, duplicate
rejection, and three coordinate corruptions.

## Campaign boundary

E457 remains a reviewed exact forcing source, but it is not a record graph.
The exact whole-field colouring already excludes every complement contained
in

```text
Q*sqrt(3)+Q*sqrt(11)+i*(Q+Q*sqrt(33)).
```

This dominated-Moser architecture was allowed to start because its possible
unit-circle centres were not assumed to remain in that field.  Exact
enumeration instead shows that every centre with enough contacts is a spindle
vertex, so the construction both stays in-field and fails even to cover the
spindle.  Under the declared stop rule it is not widened to more Moser copies,
different seeds, shells, or terminal-contact variants.  E457 is banked until
an independently motivated exact outside-field unequal relation appears.
