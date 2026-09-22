# Sources and literature status

## Primary inputs

1. M. Echavarria, M. Everett, R. Huang, L. Jacoby, R. Morrison, and
   B. Weber, *On the scramble number of graphs*, Discrete Applied Mathematics
   **310** (2022), 43--59.
   [arXiv:2103.15253](https://arxiv.org/abs/2103.15253),
   [DOI](https://doi.org/10.1016/j.dam.2021.12.009).
   Corollary 3.2 is the dense-graph implication used in (8).

2. W. N. Hsieh, *Intersection theorems for systems of finite vector spaces*,
   Discrete Mathematics **12** (1975), 1--16.
   [DOI](https://doi.org/10.1016/0012-365X(75)90091-6).
   This supplies the vector-space Erdős--Ko--Rado value for `n>=2r+1`.

3. P. Frankl and R. M. Wilson, *The Erdős--Ko--Rado theorem for vector
   spaces*, Journal of Combinatorial Theory, Series A **43** (1986), 228--236.
   [DOI](https://doi.org/10.1016/0097-3165(86)90063-4).
   This is a primary source for the completed vector-space EKR theorem. The
   proof in this directory instead includes the short spread double count
   needed specifically at `n=2r`, so no equality classification is inherited.

4. S. Ballinas, A. Caine, O. Hopkins, and D. Rivera Laboy,
   *On the Gonality of Kneser Graphs*, arXiv:2609.00258v1 (2026).
   [arXiv](https://arxiv.org/abs/2609.00258).
   Lemma 3.13 restates the dense-graph theorem above. Section 6 explicitly
   names q-Kneser graphs as a candidate family whose scramble number and
   gonality are unknown.

5. M. Cao, K. Liu, M. Lu, and Z. Lv, *Treewidth of the q-Kneser graphs*,
   Discrete Applied Mathematics **342** (2024), 174--180.
   [arXiv:2101.04518](https://arxiv.org/abs/2101.04518),
   [DOI](https://doi.org/10.1016/j.dam.2023.09.004).
   This is background on the related treewidth problem; its existence is also
   noted by source 4.

## What is new here

The new step relative to the sources inspected is the exact half-density
classification

```text
q^(r^2) [n-r choose r]_q > (1/2) [n choose r]_q
```

for all admissible q-Kneser parameters except precisely
`q=2, n=2r, r>=2`, followed by the dense-graph theorem. It yields the exact
scramble number and divisorial gonality throughout that range and answers the
q-Kneser direction raised in source 4 up to one sharply identified boundary
family.

Live searches on 2026-09-22 for `q-Kneser gonality`, `q-Kneser scramble
number`, and their exact-title variants found source 4's open statement but
no prior theorem giving these values. This is a bounded literature check, not
an absolute priority claim. The finite-geometry counting formulas,
vector-space EKR theorem, Gaussian recurrence, and dense-graph theorem are
inherited.

## Discovery Net ancestry

The graph-first selection arose from the review
`bafkreiafyx2g6qmt5xmaqlofhnqzpzpevmvuv7lrtzxzomzqrcy4ds4so4`, which
recommended moving from ordinary Kneser restricted cuts to a q/generalized
Kneser structural direction, together with the newly published open direction
in source 4. The ordinary Kneser result itself is not extended by another
parameter table here; the proof uses a different Grassmannian density bridge.
