# Primary-source trail and limits of the conclusion

Checked on 2026-09-12. This is the closing mathematical pass on an
already selected target, not a new problem selection.

1. **John H. Conway and A. J. Jones, _Trigonometric Diophantine
   equations (On vanishing sums of roots of unity)_, Acta Arithmetica
   30 (1976), 229–240.**
   [Primary scanned article](https://matwbn.icm.edu.pl/ksiazki/aa/aa30/aa3033.pdf),
   [bibliographic record](https://eudml.org/doc/205475).
   Theorem 6 on printed page 236 is the load-bearing classification
   of short vanishing sums. Printed pages 234–237 were inspected from
   the scanned images; text extraction alone is insufficient for this
   source. For a sum of five roots, an opposite-pair cancellation leaves
   a triangle; without that cancellation, Theorem 6 leaves the pentagon
   or a triangle whose two-term complement cancels. The resulting
   five-root classification is an external premise in our proof.

2. **Qin Xue, _On structured cosine sums and applications_,
   arXiv:2607.20907v1 (23 July 2026).**
   [Version record](https://arxiv.org/abs/2607.20907v1),
   [primary full text](https://arxiv.org/html/2607.20907v1).
   Proposition 2.12, including its proof, explicitly gives the
   rational-angle possibilities for two cosines summing to `-1/2`.
   They yield the same orders `5,6,12` for our primitive polynomial.
   This recent preprint independently corroborates the classical
   ingredient; no journal publication or independent verification of
   its other results is assumed. We do not claim a new rational-angle
   classification.

3. **Idris D. Mercer, _Newman Polynomials, Reducibility, and Roots on
   the Unit Circle_, Integers 12 (2012), A6.**
   [Primary article](https://math.colgate.edu/~integers/m6/m6.pdf).
   Sections 3 and 5 study reciprocal five-term Newman polynomials
   and their unit-circle roots, including the general existence of
   a unit-circle zero. Mercer's single-cyclotomic-polynomial statement
   must not be confused with being a product of cyclotomic polynomials.
   Our use is context and a priority caution, not an unproved import
   about non-torsion roots. The quantitative sign-change argument
   and finite box are given in full in this package. Priority for the
   resulting cyclotomic-product corollary has not been established.

4. **Vesselin Dimitrov and Philipp Habegger, _Galois orbits of torsion
   points near atoral sets_, Algebra & Number Theory 18 (2024).**
   [Journal record](https://doi.org/10.2140/ant.2024.18.1945),
   [primary preprint v2](https://arxiv.org/abs/1909.06051v2),
   [v2 PDF](https://arxiv.org/pdf/1909.06051v2).
   The introduction's definition, Theorems 1.1–1.2, Corollary 1.4,
   and discussion of uniformity in the univariate reduction were
   checked. Essential atorality is a hypothesis of the attempted
   route. Our bivariate polynomial fails it. The source distinguishes
   results for a fixed arbitrary univariate polynomial from the
   required estimates uniform in varying lifted exponents; these
   cannot be interchanged. We do not assume its broader conjectures,
   nor claim that every possible analytic route is ruled out.

5. **Stijn Cambie, Jun Gao, Younjin Kim and Hong Liu,
   _The Erdős distinct subset sums problem in a modular setting_,
   Acta Arithmetica 217 (2025), 295–307.**
   [Primary preprint](https://arxiv.org/abs/2308.03748),
   [journal record](https://doi.org/10.4064/aa231107-13-9).
   This remains the selected problem's primary source. The exact
   definition, three proposed excess-five types, and source-version
   caveat are documented in the preceding packages. No later primary
   settlement was found in this pass's searches; this is a bounded
   literature check, not a proof of absence.

The preceding [global reduction source trail](../global_reduction/literature.md)
records the full Glaudo–Kravitz reconstruction theorem, including its
proper-subgroup embeddings. That already established theorem is used
only to translate the hole criterion back to the three known set types.

Nothing in the new polynomial statement proves that an arbitrary
sum-distinct set has an essentially atoral lift. Proving that existence
would be equivalent to solving the selected classification. The order-41
control is deliberately outside the selected sequence, so it refutes
only the broader determinant-to-lift shortcut. The exact modular residual
and numerical bounds are unchanged.
