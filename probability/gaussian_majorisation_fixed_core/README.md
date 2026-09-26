# Gaussian majorisation with a fixed tetrahedral core

This packet proves a broad class of the bounded-input, three-dimensional
Gaussian majorisation question. It also gives an all-radius Kneser--Poulsen
comparison, including unequal balls. The full conjecture remains open.
The results are author proofs; independent review is pending.

The source consists of an arbitrary compact core in a tetrahedron and twelve
coordinate-diagonal rays outside it. A new contraction fixes the entire core,
preserves one coordinate, and reaches the same six target rays as the
classical simplex-flap map. Two forms of balance make this useful:

- Five identities between whole radial measures preserve the output law.
  They give full Gaussian majorisation at every variance and threshold,
  with arbitrary mass and distribution on the core.
- Six maximum identities between ball radii preserve the target union.
  They give its volume comparison for arbitrary independent core radii,
  unequal ray radii, and compact continua of radial shells. Minimum
  identities give the reverse intersection comparison.

The fixed region is maximal for the original ray contraction. The class
includes the classical sixteen-label tetrahedral flap configuration, whose
original labels have no continuous contraction in five dimensions. That
classical obstruction is unchanged; the alternative realization is the
new ingredient. The planar comparison theorems are prior literature.
The fixed-core construction and its balance classes are new to the searched
sources; no historical priority claim is made.

Read [PROOF.md](PROOF.md) for precise quantifiers, the full proof, references,
the distinction from the earlier unanchored ray theorem, and limitations.
Uniform weights on all twelve rays with arbitrary fixed anchors are **not**
settled by the Gaussian theorem. The proof shows why no alternative map
fixing all four anchors and having paired rank at most five can settle
that uniform class: its second-moment defect is positive in every direction.

## Reproduce the supplementary algebra

Requirements: Python 3.11 or later, standard library only. Tested on
CPython 3.11.2 and 3.12.14. From this directory:

```bash
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

The output is [EXPECTED.json](EXPECTED.json). It records 288 exact polynomial
identities, the maximal-core support checks, affine ranks six and five, five
independent additive constraints, and positive and negative controls for
whole radial laws and unequal ball radii. The canonical polynomial-record
SHA256 is
`3fd29c5258ab1658dd9f2c166bac9dfd74b899fd1cffdafdb183dd20580c177a`.
The five rejection controls are below-cutoff rays, a point outside the
tetrahedron, uniform ray weights, balance only of total ray masses, and an
invalid maximum balance. Rejection means the indicated method's hypothesis
fails, not that Gaussian majorisation or Kneser--Poulsen is false.

The verifier uses exact integers and rational arithmetic, with exceptions
that remain active under `python -O`. It does not evaluate Gaussian hinges
or ball volumes. The universal conclusions use the written analytic proof
and its cited planar theorems. Running the same checker under two
interpreters is an environment consistency check, not independent peer
review or formal verification. No external data or large artifact is needed.
