# Sources and literature boundary

## Primary sources

- Alejandro H. Morales, Igor Pak, and Greta Panova, *Asymptotics of
  principal evaluations of Schubert polynomials for layered permutations*,
  arXiv:1805.04341, especially equation (1.1), the direct-product identity
  in Section 2.2, and Conjecture 4.1:
  <https://arxiv.org/abs/1805.04341>.
- Eric Marberg and Brendan Pawlowski, *Principal specializations of Schubert
  polynomials in classical types*, Algebraic Combinatorics 4 (2021),
  273--287, for a modern treatment of Macdonald's reduced-word
  specialization formula: <https://arxiv.org/abs/2002.00303>.
- Dale R. Worley, *On the combinatorics of tableaux -- A notebook of open
  problems*, version 3, Problem 14, for the natural all-\(k\) formulation:
  <https://arxiv.org/abs/2509.25446>.

The Grassmannian Schubert-to-Schur identification and Weyl dimension
formula used in the proof are standard.  Their application to identity
inflation is included in full in `PROOF.md`.

## Status and novelty boundary

The product identity for Schubert polynomials under direct sums is classical;
Morales--Pak--Panova explicitly use it in their Section 2.2.  Macdonald's
weighted reduced-word identity is also classical.  This contribution does
not claim either ingredient as new.

The contribution is the explicit **inflation-locality theorem**: the
normalized Morales--Pak--Panova ratio factors over connected Coxeter support,
so the conjecture reduces to support-connected permutations and every proved
class is closed under parabolic products.  The componentwise Grassmannian
corollary then supplies an unbounded class with arbitrarily many descents.

Targeted searches through 2026-09-20 used combinations of “identity
inflation,” “direct sum,” “Coxeter support,” “parabolic,” “principal
specialization,” and the notation \(\Upsilon_w\).  They recovered the
classical ingredients and the original conjecture, but no explicit statement
of the ratio-locality theorem or its componentwise Grassmannian corollary.
Novelty is therefore search-relative; no historical-priority claim is made.

The result does not settle the conjecture for a new support-connected class.
In particular, connected Boolean/Coxeter permutations remain open after the
reduction.
