# A convex body from its local Firey translation areas

For a full-dimensional centrally symmetric planar convex body C centered at 0,
let F_C(x)=|(C+x)+_2(C-x)| for small x. This packet proves:

- The analytic germ of F_C determines C; directional coefficient growth
  recovers its gauge, and the Taylor radius equals its radial boundary distance.
- A positive moment matrix detects whether C has at most 2r facets.
- A 2r-facet polygon is determined among all such convex bodies by its
  Taylor jet of order 2r. This order is sharp for every r≥2.
- Two adjacent even homogeneous terms give an explicit reconstruction.
  Classical L_p Minkowski uniqueness additionally makes the highest term
  alone sufficient; that uniqueness theorem is credited as prior work.

[PROOF.md](PROOF.md) gives the all-body argument, including nonsmooth bodies.
[REFERENCES.md](REFERENCES.md) credits the reviewed Firey transform and the
classical projection-body and moment-reconstruction ingredients. Priority is
not established. No numerical-stability or higher-dimensional claim is made.

## Reproduce

CPython 3.11.2 was used; Python 3.11+ standard library only, no external inputs.
From the repository root:

```sh
python3 discrete_geometry/firey_area_reconstruction/verify.py
python3 -O discrete_geometry/firey_area_reconstruction/verify.py
```

Both outputs must equal [expected.json](expected.json). Runtime is a few seconds
on the author host. All arithmetic is exact `fractions.Fraction`; checks remain
enabled under `-O`. The deterministic fixture seed is 440921.

The decoder in [reconstruct.py](reconstruct.py) accepts just homogeneous Taylor
coefficients, detects the first singular matrix, handles a projective root at
infinity, factors the rational kernel and recovers polar endpoints by ratios.
The checker [verify.py](verify.py) generates polygon jets from oriented edges
and reconstructs the original vertices by independent halfplane intersections.
It also compares an ellipse determinant formula with exact disk beta moments.
Shared elementary polynomial/rational routines are explicit; these are author
checks, not an independent peer review or formal proof.

Expected: 90 rational polygons (700 total facets), 440 matrix-rank checks,
3280 affine coefficient checks, 31 infinity-chart cases, 80 disk moment
identities, 40 positive-definite ellipse matrices and 97 rejection controls.
The square and a rational rotation give the explicit lower-jet ambiguity.
A finite integer Fourier-mode check accompanies, but does not establish, the
written all-r sharpness argument.

Decoded-polar record SHA-256:
`b89e2593bd0f1731e79f8dad7d209d119514a0a94b12b06b3daee9cb7bb8cfba`.

This is a compact validation set, not a classification census. The theorem
rests on the written proof and its named prior results, not on fixture counts.
The prototype decoder assumes exact rational polygon data; arbitrary malformed
jets, irrational factorization and noisy reconstruction are outside its contract.
