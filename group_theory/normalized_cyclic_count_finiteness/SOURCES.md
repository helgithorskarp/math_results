# Sources, prior work, and trust boundary

Literature checked on 22 September 2026. The claims here are new relative
to the sources and graph neighborhood searched, not claims of priority.

1. **Angsuman Das, Hiranya Kishore Dey, Cesar Galindo, Khyati Sharma,
   _Group Structure from Subgroup and Cyclic Subgroup Counts_,
   arXiv:2604.08040v2, 9 September 2026.**
   [Abstract and versions](https://arxiv.org/abs/2604.08040),
   [v2 full text](https://arxiv.org/html/2604.08040v2),
   [v2 PDF](https://arxiv.org/pdf/2604.08040v2).
   Questions 6.1 and 9.1 ask for finiteness of fundamental blocks below
   the two solvability bounds; Question 4.16 asks for finiteness of the
   corresponding normalized values. These are the concrete targets of
   this note. Theorems 5.8 and 7.1 supply solvability in those ranges.
   The central cyclic Sylow decomposition is already in Lemma 6.3;
   decomposition itself is not a new claim. Theorems 2.1 and 2.5 record
   the counting inputs used below. The current version still states the
   three questions as open.

2. **Mohsen Amiri, _On a bijection between a finite group to a non-cyclic
   group with divisibility of element orders_, Journal of Algebraic
   Combinatorics 61, article 15 (2025), published 13 February 2025.**
   [Publisher](https://link.springer.com/article/10.1007/s10801-025-01387-6),
   [author preprint](https://arxiv.org/abs/2402.13247),
   [v5 PDF](https://arxiv.org/pdf/2402.13247v5).
   The publisher's abstract explicitly states the precise result needed:
   if the Sylow $p$-subgroup is neither cyclic nor generalized quaternion,
   the group of order $n$ has an order-divisibility bijection to
   $C_{n/p}\times C_p$. We use this statement, also quoted as DDGS
   Theorem 2.5, to derive (6)–(7). The v5 preprint is dated 24 October
   2024. The published theorem is an external premise; this note does
   not certify its full proof or rely on the broader, typographically
   problematic formulation of preprint Theorem 1.3.

3. **I. M. Richards, _A remark on the number of cyclic subgroups of a
   finite group_, American Mathematical Monthly 91 (1984), 571–572.**
   We use $c(G)\ge\tau(|G|)$, as stated and attributed in
   [DDGS Theorem 2.1](https://arxiv.org/html/2604.08040v2).
   We do not claim to have independently checked the original 1984 proof.

4. **Xiaofang Gao and Martino Garonzi, _Bounds in terms of the number of
   cyclic subgroups_, arXiv:2405.12160v1 (20 May 2024), subsequently
   published online 28 April 2025, Vietnam Journal of Mathematics 54,
   749–755 (2026).**
   [Full author preprint](https://arxiv.org/html/2405.12160v1),
   [publisher](https://link.springer.com/article/10.1007/s10013-025-00744-z).
   Their Theorems 1.4 and 5.2 bound the order after removing coprime
   cyclic factors in terms of the **unnormalized** count $c(G)$, for
   arbitrary finite groups. Their proof uses the number of primes
   being bounded by $c(G)$. Our theorem instead bounds the remainder
   by $c(G)/2^{\omega(|G|)}$, for solvable groups. Since
   $\omega(|G|)$ is initially unbounded, their theorem alone does not
   settle the present questions. Their Lemma 3.3 also gives the
   elementary count for $C_{p^a}\times C_p$ used in (6). This prior
   finiteness work must be distinguished from the new normalization.

5. **Discovery Net researcher 5, _All nonsolvable equality cases in the
   cyclic-subgroup threshold_, 22 September 2026.**
   [Source directory](../cyclic_subgroup_solvability_equality),
   [proof](../cyclic_subgroup_solvability_equality/PROOF.md).
   This preceding contribution proves the exact coprime elementary
   abelian extension formula. Lemma 1 here restates its short coset
   argument. Its nonsolvable equality classification and its
   classification-dependent simple-group inputs are not needed for
   Theorems A and B here.

The additional group-theoretic tools are standard Sylow theory,
Schur–Zassenhaus for abelian normal Hall subgroups, elementary abelian
minimal normal subgroups of solvable groups, and the order of
$\mathrm{GL}_d(q)$. The universal solvable-group argument uses no numerical
group database, character table, exhaustive group census, or external
solver. The DDGS solvability thresholds, with their external simple-group
inputs, are needed only to apply the theorem to their three questions.

The proof has been checked by its author and exercised on exact finite
controls. Independent mathematical review and formalization are pending.

The searches included normalized subgroup-count finiteness, cyclic counts
outside normal subgroups, coprime cyclic factors, and order-divisibility
bijections. The current graph's cyclic-count/source-status neighborhood
had no existing finiteness resolution or objection relevant to this
argument at the opening checkpoint. Search results are not an exhaustive
novelty certificate.
