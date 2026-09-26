# Sources and dependencies

1. Gautam Aishwarya and Dongbin Li, *Gaussian Convolution, Internal Energies,
   and the Kneser--Poulsen Conjecture*, arXiv:2609.07041v2, 13 September 2026.
   [Paper](https://arxiv.org/html/2609.07041v2).
   Sole campaign problem source. Supplies the conjecture, replica identity,
   and known continuous-contraction comparison machinery. The arXiv record
   was checked during this pass; v2 remained current.

2. Holun Cheng, Ser Peow Tan, and Yidan Zheng, *On continuous expansions of
   configurations of points in Euclidean space*, arXiv:1107.0140, Theorem 2.1.
   [Primary paper](https://arxiv.org/abs/1107.0140).
   Classical simplex-flap construction and dimension obstruction, with the
   expansion reversed to a contraction. No construction novelty is claimed.

3. Team B geometric lane, *Paired affine rank and the half-order gap in
   Gaussian majorisation*.
   [Proof](../gaussian_majorisation_rank_abel/PROOF.md),
   [exact flap fixture](../gaussian_majorisation_rank_abel/flap_fixture.json).
   Graph: `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu`.
   Supplies the canonical coordinates, paired-rank reduction, and geometric
   context. Its generic half-order cancellation obstruction is not treated
   as a counterexample to the Gaussian contraction conjecture.

4. Team B analytic lane, *Exact Hankel certificates for Gaussian majorisation
   and failure of every aligned common-noise transport*.
   [Proof and independent certificate checker](../gaussian_majorisation_hankel_transport).
   Graph: `bafkreids462diitdof5ijilzcq2xqwftk2bzjr5t2gihnxk327uezbndbm`.
   Supplies the complete general moment criterion. The present result
   proves its first nontrivial determinant on a specified infinite family;
   it does not republish the general reduction as new.

5. Team B adversarial lane, *Sharp relative Gaussian moment gaps and a
   complete two-power energy cone*.
   [Proof](../gaussian_contraction_moment_gaps/PROOF.md).
   Graph: `bafkreibvtztcjy7u65knymr77p6txb2g2cteukcfsb6c5o7yh5lhi4ymna`.
   An actual dependency for the additional inequality `d4<=9*sqrt(3)*d3/16`,
   which extends the determinant certificate to every quartic convex on
   the attained density range.

6. Team B functional bridge lane, *Convex quartic comparisons and finite
   Hankel positivity at large variance*.
   [Proof](../gaussian_contraction_high_noise_quartics/PROOF.md).
   Graph: `bafkreig737fhqpda2iz657ruh6clkymbesvt2a53sw4suywpqb7obwgkay`.
   Inspected at the final prepublication refresh. Covers arbitrary
   contractions for sufficiently large variance relative to support radius;
   the present result covers every variance for a fixed symmetric family.
   This is complementary context, not a dependency of the certificate.

The new theorem is the uniform quartic margin for the symmetric depth-one
flap family. The classical construction, Bernstein basis test, and Gaussian
product formula are credited. A targeted review of these sources and the
team graph found no overlapping all-parameter quartic certificate; it is
not a comprehensive priority determination. No Kneser--Poulsen volume
inequality or full Gaussian majorisation theorem is claimed.
