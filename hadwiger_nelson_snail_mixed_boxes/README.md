# Target-capped mixed Snail boxes are four-colourable

This package certifies a **4,400-member** family of finite blow-ups of the
29-point Dúcz--Varga Snail configuration.  Every member has at most 508
physical points, and every member is four-colourable.  The ranges are:

| quantity | range |
|---|---:|
| transformed Snail copies | 4--40 |
| distinct physical points | 80--508 |
| finite-field supergraph edges | 176--1,782 |

The family deliberately combines two parts of the positive geometric
fractional construction.  Its first generator is one of the 20 Euclidean
motions with greatest overlap between the Snail seed and its image.  Its
second generator is one of all 22 motions arising from the two nontrivial new
pair-congruence classes containing the added vertices `p` or `q`.  We test
both composition orders and two through six augmentation layers, extending
the high-overlap direction to the 508-point boundary.

The source paper proves that the seed has geometric fractional chromatic
number greater than 4.0007 and obtains finite non-four-colourable blow-ups
asymptotically.  This package tests a target-sized implementation of that
positive mechanism.  It does **not** classify arbitrary blow-ups, arbitrary
generator sets, or boxes with more augmentation layers.  No improvement to
the 509-vertex record is established.

The [proof](PROOF.md) specifies the finite family and explains the exact
certificate.  The source is Dúcz and Varga,
[A unit-distance graph in the plane with independence ratio below 1/4](https://arxiv.org/abs/2606.28157v1).
The exact 29-point table is copied in [seed.json](seed.json) from the previously
verified [Snail source package](../hadwiger_nelson_snail_dihedral/README.md).

## Check

CPython 3.11+ and the standard library suffice:

```sh
python3 hadwiger_nelson_snail_mixed_boxes/verify.py --progress
python3 hadwiger_nelson_snail_mixed_boxes/controls.py
```

The checker reconstructs the degree-16 coordinate field, all 34 repeated
pair-distance classes, all 925 pair isometries, the selected generators, and
all 4,400 boxes.  It checks the physical point count, target-boundary rule,
finite-field supergraph, and stored four-colouring in every case.  It does not
trust a SAT verdict or a producer edge list.

## Rebuild

The optional producer requires `python-sat==1.9.dev15` and CaDiCaL 1.9.5:

```sh
python3 hadwiger_nelson_snail_mixed_boxes/build.py --output /tmp/certificate.json
cmp /tmp/certificate.json hadwiger_nelson_snail_mixed_boxes/certificate.json
```

The committed certificate is 552,675 bytes with SHA256
`7792f073fec4c7f14721e42e598e49166bf8398ad06dedb564b187b34344f81e`.
