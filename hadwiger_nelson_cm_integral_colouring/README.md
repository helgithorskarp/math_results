# A three-colour obstruction for integral CM constructions

**Every unit-distance graph whose complex coordinates are algebraic integers
in one CM number field is three-colourable.** More precisely, the graph on
the entire ring of integers has chromatic number two when its roots of unity
have power-of-two order, and three otherwise. The statement includes every
finite support in that ring, with no vertex or coefficient bound.

The [proof](PROOF.md) gives an explicit additive map
`Z[zeta_n] -> F_3` that is nonzero on every root-of-unity direction, for every
conductor `n`. CM integrality forces all unit differences to be such roots.
Consequently a finite plane unit-distance graph with rational relative
unit-edge angles is also at most three-chromatic.

The condition is integrality at the physical unit scale. Arbitrary rational
denominators and rescaling are outside the theorem. The checker supplies an
exact boundary example: a seven-point, four-chromatic Moser spindle in the
CM field `Q(zeta_132)`, with a unit direction of quadratic trace `5/3` that
is not integral. This result excludes neither whole CM fields nor the known
five-chromatic constructions in them.

This was an analytic gate on a candidate-producing geometric source. The
fixed target-sized example has **256 vertices, 1,240 strict unit edges, and
chromatic number exactly three**. The uniform obstruction ends the source
before scaling. No five-chromatic graph or record improvement is claimed.

## Reproduce

Only Python 3's standard library is required; validation used CPython 3.11.2.
From the repository root:

```sh
python3 -B hadwiger_nelson_cm_integral_colouring/verify.py --check-expected
python3 -O -B hadwiger_nelson_cm_integral_colouring/verify.py --check-expected
```

`produce.py` deterministically regenerates `CERTIFICATES.json` and
`FIXTURE.json` without calling a solver. `colour.py` implements the explicit
colour formula for integral power-basis coefficient lists.

The independent checker imports neither producer module. Its certificates
cover 44 conductors and 7,321 root directions. It reconstructs cyclotomic
polynomials from Newton identities, checks the 256-point graph through every
one of its 32,640 pairs, and rejects five malformed certificates. The
producer uses polynomial division and norm comparisons instead. These finite
checks validate the implementation; the all-field and all-conductor claims
rest on the written uniform proof.

For example, from this directory:

```python
from colour import colour
colour(30, [1,0,0,0,0,0,0,0])  # colour of 1: 2
colour(30, [0,0,0,0,0,1,0,0])  # colour of zeta_30^5: 1
```

## Scope and campaign context

The earlier [inertial-conjugation obstruction](../hadwiger_nelson_inertial_field_barrier/README.md)
colours entire fields under a local ramification hypothesis. The present
theorem instead handles the integral points of every CM field, including
fields whose full unit graph has chromatic number at least four. Neither
result is a premise of the other.

The verified VND source and its
[fixed retained-proof-base obstruction](../hadwiger_nelson_vnd_case10_verified_gate/SUPPORT_GATE.md)
remain intact. Team-hn-3's new
[order-13 exclusion](../hadwiger_nelson_local_obstruction_order13/README.md)
was inspected for coordination and is independent of this arithmetic proof.
The square–Moser, EI/BPS, Parts, and other retired construction gates were not
reopened. The exact [1,003-vertex EI intermediate](../hadwiger_nelson_ei_terminal_core/README.md)
remains far above the target.

Source provenance, limits of the literature search, and validation details
are in `PROVENANCE.json` and `EXPECTED.json`. No external dataset, large proof
file, floating-point edge decision, or SAT-solver trust is required. No
priority, independent peer review, or proof-assistant verification is claimed.
