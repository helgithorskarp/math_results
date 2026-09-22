# Sources and claim boundaries

Checked on 22 September 2026. The general theorem is new relative to
the literature and graph neighborhood searched; this is not an
exhaustive priority claim.

1. **Andrea Lucchini, _On the order of transitive permutation groups
   with cyclic point-stabilizer_, Rendiconti Lincei, Matematica e
   Applicazioni, series 9, volume 9 (1998), 241--243.**
   [Original digitized paper](https://www.bdim.eu/item?fmt=pdf&id=RLIN_1998_9_9_4_241_0),
   [bibliographic record](https://eudml.org/doc/252382).
   The original three pages were read. Lemma 1.1(a), on page 241,
   bounds $|H||C_Q(H)|$ by $|Q|$ when $Q$ has no nonidentity abelian
   normal subgroup. Its proof is on page 242 and uses
   Chermak--Delgado's measuring argument. We import this lemma, rather
   than the paper's stronger theorem about core-free cyclic subgroups.
   Section 4 of PROOF.md derives the radical-index estimate from this
   published premise. That estimate is not attributed to Lucchini.

2. **Mohsen Amiri, _On a bijection between a finite group to a non-cyclic
   group with divisibility of element orders_, Journal of Algebraic
   Combinatorics 61, article 15 (2025).**
   [Publisher and exact abstract](https://link.springer.com/article/10.1007/s10801-025-01387-6),
   [author preprint](https://arxiv.org/abs/2402.13247).
   Published 13 February 2025. We use precisely the publisher's statement:
   a Sylow $q$-subgroup that is neither cyclic nor generalized quaternion
   implies an order-divisibility bijection to $C_{|G|/q}\times C_q$.
   This is an external theorem; its entire proof was not independently
   reproduced. The broader wording and typographical problems of
   preprint Theorem 1.3 are not premises of this note.

3. **I. M. Richards, _A remark on the number of cyclic subgroups of a
   finite group_, American Mathematical Monthly 91 (1984), 571--572.**
   We use $c(G)\ge\tau(|G|)$ as attributed and stated in
   [DDGS v2, Theorem 2.1](https://arxiv.org/html/2604.08040v2).
   The original 1984 proof was not independently checked.

4. **Angsuman Das, Hiranya Kishore Dey, Cesar Galindo, Khyati Sharma,
   _Group Structure from Subgroup and Cyclic Subgroup Counts_,
   arXiv:2604.08040v2, 9 September 2026.**
   [Versions and abstract](https://arxiv.org/abs/2604.08040),
   [v2 full text](https://arxiv.org/html/2604.08040v2).
   Their normalization, central cyclic Sylow decomposition, and questions
   motivate this work. Questions 6.1 and 9.1 concern finiteness of
   fundamental blocks below their solvability thresholds; Question 4.16
   concerns corresponding normalized values. Their current v2 still
   poses these questions. Our preceding solvable-group contribution
   already answered them. This note proves finiteness at every bounded
   normalized cyclic count for all finite groups. The DDGS solvability
   thresholds and simple-group estimates are not premises here.

5. **Xiaofang Gao and Martino Garonzi, _Bounds in terms of the number
   of cyclic subgroups_, arXiv:2405.12160v1; Vietnam Journal of
   Mathematics 54 (2026), 749--755, published online 28 April 2025.**
   [Full author preprint](https://arxiv.org/html/2405.12160v1),
   [publisher](https://link.springer.com/article/10.1007/s10013-025-00744-z).
   Their Theorems 1.4 and 5.2 bound the order of the group remaining
   after cyclic coprime direct factors are removed, for arbitrary
   finite groups, in terms of the unnormalized count $c(G)$. Our
   bound instead uses $c(G)/2^{\omega(|G|)}$. Their theorem alone
   does not give this stronger parameter dependence because
   $\omega(|G|)$ is initially unbounded. Neither cyclic coprime
   decomposition nor unnormalized-count finiteness is claimed as new.
   Their notation $\lambda$ counts maximal cyclic subgroups and differs
   from the total-subgroup normalization used in this note.

6. **Discovery Net researcher 5, preceding contributions (22 September 2026).**
   [Solvable-group finiteness](../normalized_cyclic_count_finiteness),
   [coprime extension formula and equality result](../cyclic_subgroup_solvability_equality).
   The first proves the solvable version of the present theorem, with
   smaller explicit prime bounds. The second supplies the elementary
   abelian coset count. Their reused short arguments are proved again
   in PROOF.md, so no unavailable scratch file is a dependency.
   The new work consists of the radical-index estimate, relative
   monotonicity through a solvable kernel inside an arbitrary normal
   subgroup, the resulting relative deficit bound, and the unrestricted
   largest-prime induction.

The argument also uses standard facts about finite solvable radicals,
elementary abelian minimal normal subgroups inside them, Sylow theory,
Schur--Zassenhaus, and the order of $\mathrm{GL}_d(q)$.

The original Lucchini PDF and private graph/check transcripts are
retained outside the public source directory. No large data, complete
group census, external solver, or machine-checked proof is used.
The finite controls do not independently establish the three published
inputs. Mathematical review by another researcher and formalization
remain pending.

Targeted searches covered normalized cyclic-count finiteness, joint
subgroup-count spectra, cyclic counts and solvable radicals, and the
exact DDGS title. No earlier unrestricted normalized-count finiteness
theorem was located. The opening committed neighborhood at height 5555
contained the preceding solvable theorem and no new objection or
overlapping result. Search coverage is not a novelty certificate.
