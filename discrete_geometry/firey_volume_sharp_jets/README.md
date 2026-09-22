# Sharp reconstruction from local Firey volumes in every dimension

Let C be a full-dimensional origin-symmetric convex body in R^d, d>=2.
The local function

    F_C(x) = volume_d((C+x) +_2 (C-x))

determines C. If C has 2r facets, its Taylor jet of order

    2(r-d+2)

determines C among **all** origin-symmetric convex bodies. This order is
optimal for every d and r>=d. In fact, just the two homogeneous terms of
degrees 2(r-d+2) and 2(r-d+1) suffice. Polygon-times-box examples prove the
uniform lower bound. The theorem includes nonsmooth bodies and arbitrary
facet configurations.

The [proof](PROOF.md) derives an all-dimensional integral transform, extracts
positive polar moments, and recovers normal lines and radii. A corollary
using classical L_p Minkowski uniqueness needs only the highest term,
except when its degree equals d: then that term determines exactly the
dilation class. The two-term theorem still recovers scale in that case.

This extends the previously reviewed planar inverse theorem. Classical
moment and convex-geometric ingredients are credited in [SOURCES.md](SOURCES.md).
Novelty is search-relative; independent mathematical review and formal
verification of the new theorem are pending at initial publication.

## Reproduce the compact checks

CPython 3.11.2; Python 3.11+ standard library only. From the repository root:

```sh
python3 discrete_geometry/firey_volume_sharp_jets/verify.py
python3 -O discrete_geometry/firey_volume_sharp_jets/verify.py
```

Both commands must print [expected.json](expected.json) exactly. From this
directory, `sha256sum -c SHA256SUMS` checks the source manifest.
No network, external data, solver, or floating-point library is used.
The generator seed is 6092206. The checks use exact integers and Fractions
and remain enabled under optimized Python.

The final replay took 5.4-5.7 seconds and at most 22 MiB on the author host.
Expected evidence includes 380 coefficient identities, 380 ball identities,
28 direct prism volumes, 28 curvature checks, 28 realizable polytopes with
132 reconstructed polar pairs, six smooth-ball and two cylinder controls,
and six rejected corruptions. Record digest:

`9effa3a6dd8d70eb058d9c95a7bb66aafee91640595dc34153ec395228140f31`.

[VALIDATION.md](VALIDATION.md) explains the independent slice-volume,
ellipsoid-moment and finite-reconstruction checks and their limits.
The executable checks a supplied rational normal-line certificate; it does
not implement a general real-algebraic solver to discover those lines.
The proof supplies the finite algebraic reconstruction for arbitrary real
coordinates. Computation corroborates the proof; fixture counts do not
establish its universal claims.

## Scope

This concerns exact, noiseless local volume data at Firey exponent two.
It does not prove numerical stability, minimal directional sampling,
nonsymmetric reconstruction, or a higher-dimensional Rogers-Shephard
inequality. A singular moment matrix by itself is not a polytope detector
in higher dimensions; the proof and checker include the circular-cylinder
boundary. No large or omitted certificate is required.
