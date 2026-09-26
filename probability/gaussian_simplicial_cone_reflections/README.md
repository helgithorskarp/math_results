# Gaussian majorisation for simplicial-cone reflections

Let `K` be any full-dimensional simplicial cone in `R^3`, and write
`K*={a: a dot b >= 0 for every b in K}` for its positive dual. On
`K* union (-K)`, fix the first cone and centrally reflect the second:
`T(a)=a`, `T(-b)=b`.

An explicit motion in **five dimensions** proves full Gaussian
majorisation for every bounded probability measure on this domain,
with arbitrary weights and at every positive variance. The same motion
gives the three-dimensional Kneser--Poulsen inequalities for both unions
and intersections of finitely many balls with **arbitrary individual radii**.
The cone generators need not be orthogonal. There is no atom-count bound.

The contribution is the explicit motion for this geometric class;
the Gaussian and ball-volume consequences use established lifting results.
The class includes all seven-site dual-basis flips previously used in
the team's counterexample search, even though their paired affine rank
is six. It is not restricted to balanced masses or interchangeable labels.

The companion exact obstruction has **nine points**: the origin, four
fixed square-cone facet normals, and four reflected square-cone rays.
Its prescribed contraction cannot be realized continuously in `R^5`.
It supplies a small rational target outside the motion theorem, not a
counterexample to Gaussian majorisation or Kneser--Poulsen. No minimal
number of points or historical priority is claimed.

- [Proof, motion formula, and precise scope](PROOF.md)
- [Primary literature and team dependencies](SOURCES.md)
- [Exact checker](verify.py) and [expected output](EXPECTED.json)
- [Validation and trust boundary](VALIDATION.md)

Run from this directory with Python 3.11 or later, standard library only:

```sh
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

The checker uses integer polynomial arithmetic and rational linear algebra.
It audits universal motion identities, exact rational trajectories, rank
claims, the nine-point incidence obstruction, and invalid controls.
The written proof carries the all-parameter claims. Author proof;
independent mathematical review and formalization remain pending.
The full dimension-three Gaussian-majorisation problem remains open.
