# Three full triangular lattices sharing a point are four-colourable

For **every three unit triangular lattices with a common point**, the entire
strict plane unit-distance graph on their union is four-colourable. This
includes all rotations, overlaps and lattice points, with no patch bound.
The bound is sharp. For the full lattices, three colours suffice exactly
when no unit edge joins two points in their origin residue classes
`a-b=0 (mod 3)` in Eisenstein coordinates.

[PROOF.md](PROOF.md) gives the ordinary mathematical proof. An active
triangle of cross-lattice contacts forces the rotations into one quadratic
extension of the Eisenstein field. At a place above 3, either finite-field
reduction gives three colours, or conjugate valuations turn edges between
residue-zero points into touching intervals with at most three centres.
Their median supplies a bipartition; two further colours handle nonzero
residues. The proof checks coinciding representations and interval endpoints.

This generalizes the prior [two-full-lattice theorem](../hadwiger_nelson_triangular_overlays/README.md)
and removes the size and pairwise-irrationality restrictions from the
[three-P48 upper bound](../hadwiger_nelson_three_triangular_patches/README.md).
It establishes no smaller five-chromatic graph or global vertex lower bound.
The working record remains Parts' 509 vertices. Four or more arbitrary
lattices, different lattice scales and translates with no common point are
outside this theorem.

## Exact reproduction

From the repository root, with Python 3.11 or later and its standard library:

```sh
python3 -B hadwiger_nelson_three_full_triangular_lattices/verify.py --check-expected
```

[EXPECTED.json](EXPECTED.json) records the compact output. The checker:

- verifies the norm-one graph on F9 and its explicit three-colouring;
- checks 286 height triples, including 165 median-endpoint contacts;
- checks 9,801 valuation rows, including possible cancellation ties;
- checks quadratic conjugate orbits and the necessity of nonzero trace;
- reconstructs a 1603-point, 4602-edge **four-chromatic** active-triangle
  fixture over `Q(sqrt(-3),sqrt(33))`, checks every pair exactly, certifies
  the local leading residues by Hensel congruences with explicit error bounds,
  and checks the resulting four-colouring;
- propagates the three-colouring of each 535-point patch from one triangle,
  so the fixture's zero-to-zero edge proves its lower bound four; and
- checks the classical Moser spindle against all three- and four-colour words.

The fixture's lattice valuation heights are `0,-4,-5`, with median `-4`.
Its edge-stream SHA-256 is
`40b141ddb707932b3c7f4f778d6bdea1244d76bfc0ff00d3626d679fb974bcf3`.
It demonstrates that the old P48 active triangles' three-colourability and
radicand 21 do not extend unchanged to larger patches. It is not a new
five-chromatic candidate. The fixture is generated from short explicit
rational coordinates; no graph dump or large certificate is needed.

## Evidence boundary

The all-lattice theorem rests on the written proof, ordinary local-field
facts, and the earlier pair residue lemma (also reproved here). These
finite controls are not an exhaustive proof of infinitely many angles or
valuation levels. Code uses exact integer/rational arithmetic, no numerical
distance tolerance, SAT solver, external dataset or private input.
No independent-author review or proof-assistant formalization is claimed.
No historical priority claim is made for the theorem or classical ingredients.

The concurrently published [two-lattice theorem with arbitrary isometries](../graph_theory/hadwiger_nelson_two_lattices_arbitrary_isometries/README.md)
removes the common-point assumption for two lattices. It is complementary
and is not a premise here. Neither result settles three arbitrary translates.
