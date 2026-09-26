# A robust asymmetric obstruction to two Gaussian comparison bridges

This packet supplies an exact covariance certificate and a quantitative
approximate-output separation for a rational three-dimensional contraction
outside two current proof mechanisms for Aishwarya--Li's Gaussian majorisation
question:

* no continuous contracting motion in five dimensions, even after replacing
  a deterministic map by a common-output mixture of such maps;
* no martingale comparison of the center laws after any separate Euclidean
  isometries, including after adding any common isotropic Gaussian noise.

The Gaussian density majorisation inequality for this pair remains open.
This is an obstruction to sufficient proof mechanisms, not a counterexample
to Aishwarya--Li or to the Kneser--Poulsen conjecture. It does not exclude
general density comparison operators or decompositions with different outputs.

Write

```
A = ((1,0,1), (0,1,1), (-1,0,1), (0,-1,1))
B = ((1,1,1), (-1,1,1), (-1,-1,1), (1,-1,1))
X = (0, A, -B)
Y = (0, A,  B)
w = (8,12,7,15,44,21,11,23,43) / 184.
```

For these laws the middle covariance eigenvalues satisfy
`lambda_2(Cov X) < 16/25 < 13/20 < lambda_2(Cov Y)`.
Exact integer inertia certificates prove the strict inequalities.
Every probability weight vector within `1/4000` in L1 of `w` still has
both obstructions, with covariance eigenvalue gap exceeding `11/2000`.
Thus the construction covers an open set of asymmetric weights.

The prior [common-target theorem](../gaussian_majorisation_common_target/)
proves the common-output limitation for **every injective finite atomic map**:
positive mixtures with the same output mass profile force each component
input law to equal the original input law. Distinct masses then force the
original matching, up to the allowed output isometry. The new quantitative version
for the displayed fixture also excludes mixtures of liftable contractions
whose output weights all differ from `w` by less than `1/851` in L1, on the
same target support after alignment by an isometry.

The geometry of the nine-point obstruction was proved in
[the earlier cone-reflection packet](../gaussian_simplicial_cone_reflections/).
The exact common-output obstruction was subsequently proved in researcher 8's
packet linked above. Both are reproduced only to make this construction
self-contained. The new contribution is the asymmetric covariance separation,
the complete 64-map classification, and a quantitative exclusion of approximate
common-output proofs. No priority claim is made for strict-convexity or
covariance arguments, or for the already published exact-mixture obstruction.

Read [PROOF.md](PROOF.md) for theorems, limitations and the relevance to the
shared problem, and [SOURCES.md](SOURCES.md) for dependencies.

## Reproduce

Run in this directory with CPython 3.11 or later; no packages are required:

```bash
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

Expected status: `ATOMIC_BRIDGE_OBSTRUCTION_EXACT_AUDITS_PASS`.
The checker verifies all 36 distances, enumerates all 64 bijective
contractions, checks their rank distribution and the exact separating margin,
verifies the two covariance inertia certificates, and audits the prior
five-dimensional motion obstruction and the robustness constants.
[EXPECTED.json](EXPECTED.json) records the compact exact output.

Claim status: complete author proof, with exact finite audits; neither formalized
nor independently peer-reviewed. The universal statements rest on the written
proof. No numerical quadrature, optimization result, or solver is a premise.
