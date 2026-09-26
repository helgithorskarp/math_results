# Validation and trust boundaries

The universal result is the written proof in [PROOF.md](PROOF.md), using
the previously published paired-rank theorem and Aishwarya--Li's analytic
continuous-contraction result. It is not a theorem inferred from numerical
quadrature or a finite parameter grid. Independent review is pending.

`verify.py` uses only Python integers and `fractions.Fraction`. It checks:

- All 144 ordered pairs of rays for each of two maps, as **exact quadratic
  polynomials in arbitrary radii**. Their deficits have the form
  `(r-u)^2+c*r*u` with `c>=0`; no sampled-radii argument is needed.
- Paired affine ranks six and five by rational row reduction, independently
  of the character argument in the proof, and the explicit hyperplane
  relation for the alternative map.
- Rank three of the difference between the two pushforward incidence
  matrices, with exactly the stated three balance equations.
- Equal pushforwards of a 37-atom probability law with an atom at zero,
  three unequal rational radii, unequal plane masses, and biased positive
  sign branches; 1,332 exact pairwise distance comparisons on this example.
- Two controls with unequal pushforwards, including one whose two relevant
  rays have equal total masses but different radial distributions. These
  controls are not counterexamples to Gaussian majorisation.
- The uniform twelve-to-six-point example and all twelve classical
  depth-one flap labels generated independently from tetrahedron vertices.

Run from this directory:

```sh
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

CPython 3.11.2 was used. Normal and optimized executions produce identical
output matching [EXPECTED.json](EXPECTED.json), with status
`RAY_RELABELLING_CHECKS_PASS`. All source and compact expected output are
included. There is no solver, floating-point dependency, downloaded data,
large certificate, random seed, or generated binary in the proof packet.
The manifest records the exact local source bytes.

The continuum extension uses the arbitrary-radius identities and equality
of finite radial measures in the written proof. Checking the 37-atom
example alone would not establish it. The checker does not verify the
external Gaussian theorem or Kirszbraun's theorem, and this work is not
proof-assistant formalized.

Private searches of truncated support functions and very-low-threshold
Gaussian hinges motivated this pass, but produced no certified failure.
Their raw output and numerical integration tools are not proof premises
and are intentionally excluded from this publication.
