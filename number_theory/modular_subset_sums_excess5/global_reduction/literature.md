# Primary sources and novelty boundary

Checked 12 September 2026, following the earlier selection audit.

**Cambie, Gao, Kim and Liu**, *The Erdős distinct subset sums problem
in a modular setting*, Acta Arithmetica 217 (2025), 295–307.
[DOI](https://doi.org/10.4064/aa231107-13-9);
[full open author manuscript](https://arxiv.org/abs/2308.03748), v1,
7 August 2023. The full manuscript was read. The publisher confirms
the 2025 journal publication, but its journal PDF was unavailable for
comparison; exact statement attribution below is to the manuscript.

- Theorems 1.4–1.7 classify excesses 0 through 3.
- The introduction, page 2, states an O(N^((3+t)/2)) counting estimate
  for odd t. Our Theorem 2 gives O_t(N^((1+t)/2)) for fixed odd t>=3,
  above its explicit and sharp acyclicity threshold. This is an
  improvement over the stated estimate, not a claim to have exhausted
  every implicit corollary in the literature.
- Lemma 5.2 supplies the center-and-opposite-pairs description of the
  missing sums. We restate its elementary argument as an attributed
  ingredient; it is not a new result.
- Section 7 asks for an eventual perturbation classification and
  O_t(N^(2+v_2(t))) sets. At t=5 the latter is O(N^2), still stronger
  than our unrestricted O(N^3) bound.
- Proposition A.1 supplies B0, B1 and B2. Their existence is prior
  work. The finite complete classifications here follow from the
  new exhaustive scalar reduction and reconstruction, not merely
  from rechecking those constructions.

**Federico Glaudo and Noah Kravitz**, *Reconstructing a Set from its
Subset Sums: 2-Torsion-Free Groups*, Discrete Analysis 2024:14, 19 pp.,
published 10 December 2024.
[DOI](https://doi.org/10.19086/da.125856);
[full published manuscript, arXiv:2305.11062v2](https://arxiv.org/abs/2305.11062),
9 December 2024. The published manuscript was downloaded and read,
including Definitions 1.2–1.4, Theorems 1.5–1.6 and the discussion of
proper-subgroup moves. A current arXiv-record recheck confirms v2.

The precise external premise is Theorem 1.5: equality of finite
subset-sum multisets up to translation is equivalent to a sequence of
sign changes and replacements of embedded unit dilates of U_d, for
every odd cyclic subgroup, not just the whole ambient group. The new
density argument forbids every cycle required by such a replacement.
It therefore justifies sign reconstruction without suppressing any
allowed move. The N=289 boundary example demonstrates the relevance
of proper embeddings.

The earlier campaign [long-chain theorem](../proof.md) classifies the
conditional family for every n>=5 and supplies the inequivalence and
exact counts of B0, B1, B2. Its source commit is
`3c65c864f08a1b94089b84ba58f2d537b9c3a478`. Its source files remain
unchanged in this extension. The present sharp cycle bound, counting
theorem, hole-gcd restrictions and determinant reduction apply
without the long-chain hypothesis.

Live searches included the exact modular-paper title, “sumset-distinct”
with “counting”, and distinct subset sums with acyclicity, doubling
chains and near-factorizations. No primary source stating this sharp
threshold, improved general estimate or complete determinant reduction
was found. This is search-relative novelty evidence, not a priority
guarantee. We do not claim the unrestricted excess-five classification
or the O(N^2) conjecture has been resolved.
