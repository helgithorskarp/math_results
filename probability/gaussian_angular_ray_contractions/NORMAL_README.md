# Angular factors on convex normal rays

[NORMAL_BUNDLES.md](NORMAL_BUNDLES.md) gives an author proof of full Gaussian
majorisation and both arbitrary-radius Kneser--Poulsen inequalities for every
nonexpansive map fixing a closed convex core and multiplying each complete
outward normal ray by a nonnegative factor. The theorem characterizes the
allowed factors: they depend only on the normal direction and obey the
angular whole-cone condition. Bounded diffuse laws and all variances are
included; the core may be singular or unbounded.

A ball core gives factors depending jointly on radius and direction.
A cube example has different projection base points and is neither a
homogeneous ray map nor a common normal-profile map over any convex core,
in the precise scopes proved. General nonlinear dependence on normal
distance remains outside the theorem. The unrestricted R3 question is open.

Independent correctness and historical-priority review of this extension
are pending. [ACCEPTANCE.md](ACCEPTANCE.md) records the accepted predecessor;
[NORMAL_SOURCES.md](NORMAL_SOURCES.md) states the dependency and trust boundaries.
All seven original angular files and their original manifest are frozen.

From the repository root, using standard-library CPython3.11.2:

```sh
python3 probability/gaussian_angular_ray_contractions/check_normal_bundles.py --check
python3 -O probability/gaussian_angular_ray_contractions/check_normal_bundles.py --check
```

Both print `NORMAL_BUNDLE_AUTHOR_CHECKS_PASS`. Exact rational and quadratic
surd checks cover366 pair motions on seven core geometries, the projection
identity, whole-ray necessity controls and invalid input rejection.
The analytic universal theorem is written mathematics, not a consequence
of finite sampling. NORMAL_EXPECTED.json is canonical supplementary output;
NORMAL_INPUTS.json pins the original packet. Run `sha256sum -c NORMAL_SHA256SUMS`
from this directory to verify the new source files.
