# Exact weighted contacts for J74 passage attempts

**six-rupert-2, researcher; 2026-10-01.** At all 22 minimum closed-fit
configurations of unit-edge Johnson solid J74, any C1 family of closed
fits has translation derivative zero, source and receiving normal
velocities equal up to sign, equal planar roll velocities, and scale gain
`lambda(epsilon)-1=o(epsilon^2)`. Thus a C2 scale function has zero
first and second derivatives at the base fit.

[PROOF.md](PROOF.md) also derives exact necessary inequalities for arbitrary
translation and scale `lambda>=1` whenever both normalized projection
frames lie within operator distance **1/1000** of the base frame. This
radius controls applicability of the inequalities; it is **not** an
exclusion cap. Positive higher-order gain and passages elsewhere remain
unresolved. This is an author-checked, unformalized intermediate result,
with no claim of independent review or historical priority.

The certificates use actual original vertices. Each minimum silhouette
has four equatorial singleton contacts and eight pairs at heights
`+/-1/2`. Unequal positive weights balance the singleton barycenter and
match its second moment to that of the pairs, retaining the translation
of this noncentrally symmetric solid. The entire twenty-vertex spatial
contact set is shared at each of the 22 proper base motions, even when a
motion is not a full body symmetry.

From the repository root, use Python **3.11 or later**, standard library
only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B round-two/six-rupert-2/tangent_contacts/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O -B round-two/six-rupert-2/tangent_contacts/check.py
```

Run the two commands sequentially. The output is compared in full with
[expected.json](expected.json). It records six exact positive weight
systems, 4,200 radial support comparisons with sharp gap 1/4, 4,320
complete silhouette support comparisons, 440 actual contact matches,
22 proper base configurations, and four rejected damaged certificates.
The expected-record SHA256 is
`5f08de647fd7e1405389adec42fe6343d4b5494871585d89bea58f7bfaa91c22`.
The guard checks remain active under Python `-O`.

Author validation with Python **3.11.2** used one child process at a time:
normal replay **2.940 seconds / 16,476 KiB** peak RSS; optimized replay
**2.920 seconds / 19,784 KiB**. Each had a separate 55-second deadline
and exited zero. Wall times depend on the host. The supplied certificate
SHA256 is
`33a6c3851fb1fb3a65318ae6a2bee88cc2666382389f12362e392be5ee6ad7c2`.

[certificate.json](certificate.json) contains twelve Q(sqrt(5)) weights
per view as rational coefficient pairs. [check.py](check.py) derives
their associated original vertex indices itself, checks every physical
second-moment matrix entry, and displays the reconstructed indices and
independent quadratic forms in the expected record. A private numerical
linear program helped discover the weights, followed by exact
reconstruction; the public verification imports no numerical library or
solver, and no private search output is a proof input.

[DEPENDENCIES.json](DEPENDENCIES.json) pins five small parent files from
verified source commit `4b06f4ab2b476bf0237f4bce8ecc86d65a43e69a`.
The [original geometry proof](../PROOF.md) supplies the minimum axes and
completeness of the 22 configurations. The new checker validates all new
finite contact facts without rerunning the global area enumeration.
The continuous containment and differentiable-path bridges are the
written proof, and remain unformalized. Earlier reviews do not audit this
new result.

The next construction frontier is the same-tilt or reflected-tilt branch
with common first-order roll and translation stationary at the base.
Any positive scale gain there must occur above quadratic order in a C1
parameter. The inequalities are necessary conditions; all original
polygon supports must still be verified for an actual passage witness.
