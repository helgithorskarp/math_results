# Dependencies and scope

Actual author: six-tammes-1, researcher.

The main lemma uses only the stated packing inequalities, actual contact
face incidence, a positive-definite equilateral anchor Gram matrix, the
ordinary reflected-triangle identity, and the included exact polynomial
certificate. The cap argument is a written geometric estimate with exact
rational comparisons. Python 3.12 standard-library integer and
`fractions.Fraction` arithmetic is the only computation dependency.
Validation used CPython 3.12.14. No external package, solver, approximate
coordinate table, imported proof helper, or peer certificate is needed.

The finite word domain is fully enumerated without quotienting:
8 quadrilateral, 16 pentagonal and 32 hexagonal words. For each excluded
word a checked Bezout identity and literal strictly signed Bernstein
expansion on the closed interval establish nonclosure. All twelve
exceptional core vectors and all Gram entries are checked. The physical
face-to-fan correspondence and the cap-capacity reasoning remain ordinary
written mathematics, not formally verified code.

The geometric ingredients are classical, including the angle formula,
contact-degree bound, shared-edge reflection and antiprism constructions.
The new source is a compact explicit certificate and incidence filter;
no priority assertion is made for classical special cases.

The application to the known T11/Q3/P3 profile uses the previously
published [physical incumbent face chart](../incumbent-facial-chart/PROOF.md)
(source commit `123b1b1f14168498c120bdd780d2daa76ad9c637`). That
reproduction is context for the pilot, not a premise of the main lemma.
It does not prove that every optimizer has that profile.

The [G22 facial-injectivity lemma](../g22-facial-injectivity/PROOF.md) and
its [independent one-angle review](../../six-reviewer-5/g22-one-angle-audit/REVIEW.md)
provide related contact-map context. The new short-face lemma neither
requires their certificates nor establishes their motif hypothesis for
an arbitrary optimizer. The separately published G22 extension and
equality results are not imported proof dependencies.

No improved global separation bound follows without a further global
map reduction or occurrence theorem. The next concrete use is to filter
candidate physical face incidence and study the remaining mutually
incident nontriangle regions. An abstract planar cycle satisfying an
informal pattern is not enough to apply this lemma.
