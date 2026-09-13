# Independent review: three arbitrary rotations of Parts159

## Verdict

**ACCEPT with high confidence.**  At target source commit
`860f0b259e378142142482c2d02c75a281bebbff`, the theorem and its exact
physical interface are sound:

> Let `A` be the archived Parts `v159e646` point set, with its published
> vertex 0 at the origin.  For every three unit complex numbers `u,v,w`, the
> strict plane unit-distance graph on `uA union vA union wA` is
> four-colourable, after identifying coincident points and including every
> induced unit edge.  It has at most `1+3(159-1)=475` points.

This closes one shared-origin, rotation-only construction family.  It does
not cover reflections, different anchors, translations, different gadgets,
or four copies.  It is not a global plane result and does not improve the
published 509-vertex, 2,442-edge Parts record.

## Independent proof computation

`independent_audit.py` imports no target module.  It parses the hash-bound
coordinate file directly and uses the quotient basis

```text
1,t,r,tr,       t^2=-3, r^2=-11,
```

instead of the target's `1,sqrt(33),t,r` arithmetic.  A contact quadratic
extension is represented by a second quotient generator `q` with `q^2=d`.
Field inversion is the product of three Galois conjugates.  Every exact
decision uses Python integers and `Fraction`; no distance tolerance, SAT
answer, target event table, or target Python function is used.

The audit independently reconstructs the 159 distinct points and all 646
strict internal unit edges.  It exhausts the `158^2=24,964` nonzero labelled
point pairs and obtains:

| pair outcome | pairs |
|---|---:|
| negative discriminant | 2,937 |
| contact roots in `E` | 12,906 |
| contact roots outside `E` | 9,121 |

The outside row forms 1,490 irreducible contact quadratics and 2,980 physical
unit rotations.  Their 60 positive radicands split exactly into 52 quadratic
extensions.  All 1,490 quadratics have nonzero trace.  This last fact is
essential: if outside phases `a+b sqrt(d)` and `c+e sqrt(h)` belong to
different extensions, `conjugate(u)v` has nonzero coefficients on all four
biquadratic basis elements.  No nonidentity Galois involution fixes it, so it
has degree four over `E` and cannot be another degree-two contact phase.  This
excludes 4,319,976 different-extension phase pairs geometrically.

For the remaining 118,734 same-extension pairs, the checker reconstructs the
relative phase exactly, recovers its full contact and coincidence interface,
and checks a four-colouring of the actual identified point union.  It finds
80,858 pairs with no outer edge, 37,516 handled by the four-word component
library, and 360 handled by explicit positive certificate rows.  The same
calculation checks all 62 exceptional two-copy extension rows.  Every one of
the target certificate's 226 component words is used and checked on the 646
internal edges.  The independently reconstructed entry-level coverage hash is

```text
5abdc23954147463c5438704a65930fb0ddbfdc4ef9bc848758077f203571140
```

The checker separately enumerates every possible in-field nonzero
coincidence phase.  Thus equality constraints are checked in the physical
union, and the evidence is not merely a colouring of an abstract graph on
475 unmerged labels.

## Continuum completeness

The ordinary proof reducing all real angle triples to the finite audit is
also valid.  Join two copies when they have a non-origin cross edge.  A
nonzero coincidence forces such an edge because every gadget vertex has at
least two internal neighbours.  A disconnected copy-contact graph reduces
to one- and two-copy colourings agreeing at their common origin.  A connected
three-vertex contact graph has a copy adjacent to both others, which can be
normalized to `A`.

If both remaining phases lie in `E`, the separately reviewed four-colouring
of the entire field `E=Q(i sqrt(3),i sqrt(11))` applies.  If both are outside,
the different- or same-extension checks above apply.  In the mixed case, an
outer contact allows recentering at the outside copy, producing two outside
phases; without an outer contact, the in-field pair and the outside copy can
be coloured independently across that missing interface.  These cases are
exhaustive and retain all coincidences and strict unit edges.

The field-colouring premise and the one-contact quadratic reduction already
have independent reviews in
`hadwiger_nelson_nonmono_field_obstruction_review3` and
`hadwiger_nelson_nonmono159_origin_pencil_review3`.  This review rechecks the
specific field-colouring word and all contact events needed here.

## Additional checks and trust boundary

`symbolic_audit.py` uses SymPy over exact symbolic expressions to verify the
contact-line reduction, unit-root norm identity, quadratic minimal
polynomial, and all three nonidentity biquadratic automorphism differences.
`controls.py` exercises the three quotient relations and deliberately makes
each of the 226 supplied component words monochromatic on an internal edge;
every corruption is rejected.

The target solver-free verifier passed in normal and `-O` modes, and its own
second arithmetic representation checked 2,980 rotation norms, 18,242
outside cross edges, 10,138 deterministic nonedges across all 52 extensions,
and rejected all 422 certificate-row corruptions.  The SAT solver used to
discover the positive words is not a proof dependency.

The trust boundary is the unformalized algebraic continuum argument, the
separately reviewed whole-field colouring theorem, CPython's exact integer
and rational semantics, SymPy only for the secondary symbolic audit, the
hash-bound Parts coordinate file, and the compact positive target
certificate.  Source provenance identifies that coordinate file as the
intended archived Parts gadget; this review does not independently recover it
from the original publication.

See [REPRODUCE.md](REPRODUCE.md) for exact commands and [VALIDATION.json](VALIDATION.json)
for measured runs.
