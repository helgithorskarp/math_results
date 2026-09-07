# Voronov `L_{10,2}` radial-prefix closure at order 508

This package gives an exact negative decision for a target-sized construction
family derived from the planar `L_{10,2}` source of Voronov, Neopryatnaya, and
Dergachev.  Their construction starts from a 73-point generator set `M1`,
forms the radius-one clipped Minkowski sum `M2`, then obtains five-chromatic
graphs by enlarging once more to `M3` and joining two rotated copies.

Here we test the direct target-order alternative: two origin-centred radial
prefixes of `M2`, with a size budget that guarantees at most 508 physical
points under every rotation.  The family is completely closed.  Up to exchange
of copies there are six maximal size pairs,

```
(241,241), (289,217), (361,145),
(433,73), (457,25), (505,1).
```

For all six, the two radii sum to less than one, so rotation can create no
cross unit edge.  Every relevant prefix is contained in the exactly verified
bipartite 505-point prefix.  A product of the two bipartitions gives a
four-colouring even when the rotated copies have additional coincident points.
Consequently no graph in this entire family is five-chromatic.

See [PROOF.md](PROOF.md) for the precise theorem and reduction.

Public package: <https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_voronov_radial_prefix_closure>

The source is V. A. Voronov, A. M. Neopryatnaya, and E. A. Dergachev,
[Constructing 5-chromatic unit distance graphs embedded in the Euclidean plane and two-dimensional spheres](https://arxiv.org/abs/2106.11824),
with the authors' [published graph data and Sage notebook](https://github.com/vsvor/dist-graphs).
The notebook writes the second generator in an equivalent form
`phi0^4 conjugate(phi1)`; because all 24 powers of `phi0` and both signs of
the `phi1` exponent occur, this generates the same `M1`.

## Reproduce

Python 3.11 or later and its standard library are sufficient.

```bash
python3 verify.py
python3 controls.py
python3 produce.py
cmp certificate.generated.json certificate.json
```

The verifier regenerates `M1` and `M2` over
`Q(sqrt(2),sqrt(3))`, proves the exact radial inequalities, audits every pair
of the 505-point prefix, and checks its explicit bipartition.  It does not call
a SAT solver or use floating-point geometry.

## Files

- `exact_model.py`: exact field arithmetic, source reconstruction, shell
  enumeration, edge audit, and bipartition logic.
- `certificate.json`: exact shell census, six radius inequalities, all 216
  unit edges of the largest prefix, and its bipartition.
- `produce.py`: deterministic certificate producer.
- `verify.py`: regeneration and certificate comparison.
- `controls.py`: independent floating-point reconstruction and separation
  check.
- `VALIDATION.json` and `CONTROLS.json`: captured successful runs.
- `PROOF.md`: completeness proof and scope.
- `provenance.json`: pinned primary-source metadata and exploratory context.
