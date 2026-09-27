# Loss-scaled Gaussian hinge continuity

For every bounded contraction pair in `R^3` with `R^2/s<=1/2`, the
[author proof](PROOF.md) establishes

```
|H(u)-H(v)| <= (mean squared-distance loss / s) K |u-v|^(1/2).
```

It also bounds the derivative of the relative hinge in log-threshold
coordinates by the same loss. The constants are explicit and independent
of atom count, minimum atom weight, and a positive loss floor. A two-atom
first variation shows that the linear loss scale for the whole curve is
sharp in order.

This improves the error term in the existing complete beta-moment
criterion. Given signed endpoints and a positive middle margin divided by
the loss, the degree needed for a finite full-sign certificate can be
bounded independently of how small the loss is. A direct relative-hinge
grid has a corresponding slope test. Second energy can replace the loss
as the normalization, within explicit constant factors.

The missing positive middle margin is **not proved in general**. No
unrestricted zero-defect theorem, new Kneser--Poulsen case, new beta-sign
strip, or certificate for the large-radius rational frontier is claimed.
The constants have not been optimized for practical certification.

Reproduce the compact algebra and interval checks with Python 3.11 or later,
standard library only:

```bash
python3 probability/gaussian_loss_normalized_hinges/verify.py
python3 -O probability/gaussian_loss_normalized_hinges/verify.py
```

Both commands print [EXPECTED.json](EXPECTED.json). The checks use exact
rational Laurent polynomials and rational interval arithmetic, including
an explicit slope constant outside the previously signed threshold
window. They do **not** compute any new hinge sign. Coarea differentiation,
Abel inversion and the continuum statements remain unformalized author
mathematics, with dependencies recorded in [SOURCES.md](SOURCES.md).
