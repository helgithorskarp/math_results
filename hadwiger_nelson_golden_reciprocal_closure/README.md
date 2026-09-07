# Golden reciprocal-overlay closure

This package gives an exact negative decision for a candidate-bearing
unit-distance construction family derived from Jaan Parts's 16-point
`{1,phi}` graph, where `phi=(1+sqrt(5))/2`.

Let `B` be the reconstructed 16-point set.  For each scale `s` in
`{phi,1/phi}`, take every congruent or reflected copy `s R(B)+t` having at
least two distinct points in common with `B`.  The strict unit-distance graph
on the union of `B` and **all** such copies is four-colourable.  Consequently,
every graph obtained by choosing an arbitrary subcollection of these copies is
four-colourable, including every subassembly with at most 508 vertices.

The exact census has 5,568 labelled two-coincidence specifications and 328
distinct copy point sets at each scale.  The two one-scale closures each have
780 vertices, with 2,566 and 2,158 unit edges.  Their combined closure has
1,386 vertices and 4,380 unit edges.  The compact certificate is one explicit
four-colour word for that combined closure.

The source is reconstructed inside Parts's pentagonal Minkowski-sum host.  Its
distance graph has 28 unit edges and 28 edges of length `phi`; vertices
`{1,2,3,5,6}` form a `K5`, and an explicit five-colouring is checked.  Thus
the source is genuinely five-chromatic as a two-distance graph even though the
reciprocal-overlay conversion family is unsuccessful.

See [PROOF.md](PROOF.md) for the exact reduction, arithmetic, completeness
argument, and scope.  The primary geometric source is Parts,
[A small 6-chromatic two-distance graph in the plane](https://arxiv.org/abs/2010.12656).

## Reproduce

Python 3.11 or later and the standard library are sufficient.

```bash
python3 -B verify.py
python3 -B -O verify.py
python3 -B controls.py
python3 -B produce.py --output certificate.generated.json
cmp certificate.generated.json certificate.json
sha256sum -c SHA256SUMS
```

`verify.py` uses a nested quadratic representation independent of the
producer's cyclotomic power basis.  It reconstructs all copies, all closure
points, and every strict unit edge, then checks the colour word directly.
`controls.py` compares all 656 copy point sets entry by entry across the two
representations and rejects three malformed colourings.  The deterministic
DSATUR search in `produce.py` is only a certificate generator; solver
correctness is not a premise of the result.

The reference run on CPython 3.11.2 uses one process and one thread.  It takes
about 43 seconds for production, 25 seconds for either verification, and 51
seconds for the controls on the research host.

Verified source commit: `VERIFIED_SOURCE_COMMIT`.

Public directory:
<https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_golden_reciprocal_closure>

This is a complete result only for copies that each meet the fixed source `B`
in at least two points.  Copies constrained solely by other moved copies,
other scales, and deformations of the source lie outside the theorem.  No
five-chromatic unit-distance graph or record improvement is claimed.
