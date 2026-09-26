# Exact equality faces for Gaussian common-set minimax searches

This package proves a positive common-set transfer theorem for orthogonal
splittings of dual cones. It then completely describes the isometric priors
on the team's nine-point square-cone contraction and supplies exact
certificates for their zero minimax values against **every** prior on that
configuration. These give a rigorous boundary for finite-atomic searches of
the unrestricted three-dimensional Gaussian-majorisation question.

**Status:** complete author proof, with two different exact computational
audits. Independent peer review and formalization are pending. The full
dimension-three conjecture is open. This is a dependency certificate, not a
new Kneser--Poulsen class or an integrated Gaussian counterexample.

The [proof](PROOF.md) establishes:

- If a Gaussian prior is supported on an orthogonal splitting of dual cones,
  reflection of any of its superlevel sets transfers at least as much Gaussian
  mass from **each** allowable center. Its inner common-set minimax value is
  exactly zero, at every variance and retained volume.
- The canonical eight nonzero square-cone sites have 47 isometric supports
  and ten maximal isometric faces. The origin may carry any additional mass.
  Every exterior-site first variation from the relative interior of a
  maximal face is strictly positive at fixed variance and volume.
- If delta is total-variation distance to the union of these faces and
  tau is the sum of the eight strictly contracted cross-weight products,
  then tau >= 3 delta^2 / 7, sharply. Requiring delta >= delta_0 uses ten
  linear inequalities and preserves convexity of the inner minimax search.

The sharp constant normalizes the already-known second-energy signal; it
does not imply the required hinge inequalities. A fixed positive delta_0
does not cover the entire problem. The numerical search motivating this
package produced no certified negative integrated witness.

## Replay

Python standard library only; checked with CPython 3.11.2 and 3.12.14.
From this directory, run:

```sh
python3 verify.py
python3 independent_check.py
python3 -O verify.py
python3 -O independent_check.py
python3 check_controls.py
sha256sum -c SHA256SUMS
```

Each audit takes less than two seconds on the author's host. The first audit
must report `EXACT_FINITE_OBLIGATIONS_PASS` and record hash
`8c3f070226700703b8cec3e2120ae31f7da33ee697cf84c31b6979ea5b686a5b`.
It checks 378 polarization scalar products, 48 strict exterior-site tests,
and all 255 nonempty stationary supports: 247 consistent systems, including
91 singular ones, and eight inconsistent systems. The minimum stationary
value is exactly 3/7.

The separate audit must report `SEPARATE_MATCHING_SOS_AUDIT_PASS`. It checks
the geometry independently and reduces the quadratic bound to 47 matching
supports: 1 empty, 8 single edges, 20 pairs, 8 three-edge paths, 8 three-edge
single-interaction cases, and 2 four-edge cycles. It verifies the exact
sum-of-squares coefficient identities and the sharp witness. It imports no
code from the first audit and does not solve its stationary systems.

The controls must report eight rejections: both audits reject each of a
nonorthogonal reflection, a missing maximal face, a missing strict pair,
and the false constant 1/2. The `-O` runs verify that Python assertions are
not part of the checking boundary.

## Source and evidence

| File | Purpose |
| --- | --- |
| [PROOF.md](PROOF.md) | Universal transfer proof, strictness, finite reduction, sharp bound |
| [CERTIFICATE.json](CERTIFICATE.json) | Ten exact rational reflections, strict pairs, sharp flow and packet |
| [verify.py](verify.py) | Exact geometry, exhaustive stationary-system proof, deterministic record |
| [independent_check.py](independent_check.py) | Separate geometry and matching/SOS audit |
| [check_controls.py](check_controls.py) | Reproducible rejection of damaged certificates |
| [EXPECTED.json](EXPECTED.json) | Compact expected primary audit record |
| [SOURCES.md](SOURCES.md) | Primary literature and precise team dependencies |
| [SHA256SUMS](SHA256SUMS) | File integrity manifest |

To regenerate the compact certificate and expected record from the source:

```sh
python3 verify.py --write-certificate --write-expected
sha256sum -c SHA256SUMS
```

The generated files must remain byte-identical. No solver, quadrature nodes,
large corpus, private input, network access, or omitted data are required.
Python integer/Fraction arithmetic and the short checking programs are
trusted. The written polarization, Gaussian differentiation, max-flow, and
simplex-minimizer reductions are not machine-formalized. Two author-written
algorithms do not constitute independent mathematical acceptance.
