# Sources, attribution, and scope

Primary literature checked live on 2026-09-21.

1. P. Erdős, Chao Ko, and R. Rado, *Intersection theorems for systems of
   finite sets*, Quarterly Journal of Mathematics 12 (1961), 313–320.
   [Original paper at the Rényi Institute](https://www.renyi.hu/~p_erdos/1961-07.pdf).
   Its classical uniform intersecting-family bound is the only external
   theorem used in our proof: for `n>=2k`, at most `binom(n−1,k−1)`
   pairwise-intersecting `k`-subsets. We make no claim to a new proof of it.

2. Márton Naszódi, *Fractional illumination of convex bodies*,
   Contributions to Discrete Mathematics 4(2) (2009), 83–88.
   [Original paper](https://cdm.ucalgary.ca/article/view/62022).
   Definition 1 is the finite-support fractional-illumination convention
   used here. The fractional-transversal viewpoint and its weak duality
   are established background. Proposition 6 already gives fractional
   illumination two for smooth bodies, whose ordinary illumination is
   dimension plus one. Thus unbounded gaps in the class of all convex
   bodies are old; our gap statement concerns the specified discrete
   family and follows from its exact covering-array reduction.

3. Wen Rui Sun and Beatrice-Helen Vritsiou, *On the illumination of
   1-symmetric convex bodies*, arXiv:2407.10314v1 (2024).
   [Author manuscript](https://arxiv.org/html/2407.10314v1).
   Theorem E settles the Hadwiger–Boltyanski conjecture for 1-symmetric
   convex bodies in all dimensions. Every `P(n,k)` here is 1-symmetric;
   proving just that it satisfies the Hadwiger bound would therefore not
   be new. Criterion A gives the standard active-normal illumination
   test. We derive the concrete test for our bodies directly. The paper's
   perturbed coordinate directions are also pertinent background.

4. Daniel J. Kleitman and Joel Spencer, *Families of k-independent sets*,
   Discrete Mathematics 6 (1973), 255–262.
   DOI: `10.1016/0012-365X(73)90098-8`.
   Binary covering arrays are classical, equivalently independent set
   families. We do not claim new covering-array theory. All elementary
   covering-array facts used in the proof, including the parity
   obstruction and the logarithmic lower bound, are proved in PROOF.md.
   The familiar small value `CAN(3,5,2)=10` is used only as an illustrative
   certificate, with its upper and lower bounds checked from scratch.

Additional context inspected: Sun–Vritsiou's
[1-unconditional-body paper](https://arxiv.org/html/2407.11331v1), and
Lawrence, Kacker, Lei, Kuhn, and Forbes's
[survey of binary covering arrays](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v18i1p84/pdf/).
These are context, not extra unproved inputs to the theorem.

## What is and is not claimed

The contribution is the exact formula
`I_f(P(n,k))=(n/k)2^k` for `2k<=n`, and `2^k` for `2k>n` and the exact cardinality-preserving
illumination/covering-array reduction for `2k>n`, with its equality
obstruction. The strict entering condition is essential: at `2k=n`,
equal-magnitude sign directions illuminate no vertices.

Targeted searches used illumination, fractional illumination,
hypersimplex, signed hypersimplex, cube/cross-polytope intersection,
cuboctahedron, covering arrays, and Erdős–Ko–Rado. The above sources did
not supply these exact statements for `P(n,k)`. This is a bounded
literature check, not a priority guarantee. The result may be described
as new to the sources checked, or as a structural synthesis of classical
ingredients; a claim of first discovery is unwarranted.

We assert no exact ordinary value for the full range `2k<=n`, no new
covering-array parameter table, and no resolution or strengthening of
the general Hadwiger–Boltyanski conjecture. Nor does this derive anything
from primitive-polytope vertex bounds or from the earlier zonotope
calculations in this repository.
