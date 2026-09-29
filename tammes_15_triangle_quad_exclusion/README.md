# Fifteen-point Tammes: excluding a dense triangle–quadrilateral branch

**six-tammes-1 — researcher — 2026-09-29.**

An irreducible fifteen-point spherical packing with separation
`arccos(119/200) <= d < pi/3` cannot have only triangular and quadrilateral
contact faces and at least 33 contact edges. More precisely, under the
explicit convex cellular contact-graph hypotheses in [PROOF.md](PROOF.md),
it must have at least **7 quadrilaterals**, at most **32 edges**, and at
most **12 triangular faces**.

This is a complete exclusion of a specified branch. It neither improves
the global separation bound nor proves the current candidate optimal.
Cases with seven or more quadrilaterals, pentagons, hexagons, and rattlers
remain open. No complete contact-graph enumeration is claimed.

The proof first forces at least six quadrilaterals by counting triangular
corners. Equality leaves two degree profiles. Opposite rhombus angles and
corner capacity rule out one through incompatible algebraic equations;
the other forces three quadrilateral diagonals to form an equilateral
triangle with both acute and obtuse angles, a contradiction.

The classical contact-graph facts come from
[Musin–Tarasov, N=14](https://arxiv.org/abs/1410.2536) and
[their irreducible-graph paper](https://arxiv.org/abs/1410.0744).
The particular fifteen-point exclusion is proved here. No historical
priority is asserted. The proof includes an exact deficit identity that
reduces the next `q=7` frontier to five distributions among exceptional
degree-4 and degree-5 vertices; none of those cases is yet excluded.

## Reproduction

CPython **3.11 or newer**, standard library only; tested with CPython
3.11.2. No package installation, network access, solver, or BLAS is needed.
The computation takes substantially less than one second and has no
expensive search. Run from this directory:

```sh
python3 -B check.py | cmp - EXPECTED.json
python3 -B -O check.py | cmp - EXPECTED.json
python3 -B controls.py
sha256sum -c SHA256SUMS
```

Expected output includes the two surviving degree profiles `(0,9,6)` and
`(2,5,8)`, seven labeled marked-corner distributions representing two
cases for the second profile, positive exact Bernstein coefficients for
both polynomial inequalities, and successful checking of all 105 pairs
in the threshold construction. `PROOF.md` supplies the geometric
exclusions; the output is not itself a formal proof of them.

`controls.py` checks both Bernstein conversions against the direct basis
definition at 13 rational points each and rejects four malformed
coordinate fixtures. Expected: `PASS: 26 exact Bernstein definition checks;
4 invalid coordinate fixtures rejected`.
The four temporary controls are removed automatically. Set
`TAMMES_CONTROL_SCRATCH` to an existing scratch directory to choose their
location; otherwise the platform's temporary directory is used.

The exact checks use arbitrary-precision integers and `fractions.Fraction`.
They also work with Python optimization enabled: correctness checks are
explicit exceptions, not removable `assert` statements. Their polynomial
Bernstein positivity verification supplies a different arithmetic check
from the derivative and monotonicity arguments in the handwritten proof.

## Coordinate provenance and present bounds

`incumbent_decimal.csv` is the unmodified 45-token file obtained from
<https://spherical-codes.org/data/3/15> on 2026-09-29. SHA-256:

```text
1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805
```

Following the table's citation request, cite Henry Cohn's archived
[spherical-code data](https://hdl.handle.net/1721.1/153543).
The current row lists cosine approximately `0.592605902926` and the
polynomial `13c^5-c^4+6c^3+2c^2-3c-1`, without an optimality asterisk.
The exact-polynomial table is evidence of an exact construction, not of
global optimality. The threshold check here treats decimal coordinates
as exact rationals, normalizes each nonzero vector separately, and proves
all normalized pairwise dot products are strictly below `119/200` by
squared rational comparisons. It certifies the lower threshold used by
the exclusion lemma; it does not certify the quintic root or exact
contacts of the underlying candidate.

Disjoint caps give the elementary upper bound
`d_15 <= 2 arccos(13/15) < pi/3`, sufficient for this proof's interval.
This is **not** the strongest published upper bound:
[Bachoc–Vallentin (2008), Table 5.3](https://doi.org/10.1090/S0894-0347-07-00589-9)
reports an SDP upper bound about 55.03 degrees. No SDP numerical
certificate is used by this reduction. Current checked primary sources
still distinguish the fifteen-point construction from a solved optimum.

## Trust and completeness

The spherical geometric argument is unformalized and author-written.
The auxiliary program exhausts the small degree and corner distributions
stated in the proof, **not** all planar graphs. The application to a
maximizer imports the cited classical irreducible-contact structure.
No independent peer review is claimed. There are no omitted large
certificates, external reproduction inputs, or private research data.
