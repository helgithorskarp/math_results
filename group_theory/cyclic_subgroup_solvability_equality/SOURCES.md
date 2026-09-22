# Literature, graph context, and external premises

Checked on 22 September 2026.

## Primary sources

1. A. Das, H. K. Dey, C. Galindo, K. Sharma,
   *Group Structure from Subgroup and Cyclic Subgroup Counts*,
   [arXiv:2604.08040v2](https://arxiv.org/abs/2604.08040v2),
   posted 9 September 2026.
   The current arXiv record lists v2 as the latest version.
   We read Sections 7–9 and Appendices B–E in the full 57-page PDF,
   together with the introduction and relevant preliminaries.
   Theorems 7.1 and 7.3 supply the nonsolvability lower bound and
   the stronger simple-group input. Remark 7.2 gives the
   $A_5$ times coprime squarefree cyclic examples.
   The equality necessity theorem proved here is not stated there.

2. A. Das, K. Sharma,
   *Solvability of Groups via Cyclic Subgroup Count*,
   [arXiv:2604.23664](https://arxiv.org/abs/2604.23664).
   Lemma 2.3(2) already gives the strict quotient count
   $c(G)\ge c(G/N)+c(N)-1$. Theorem A classifies nonsolvable
   groups with fewer than 50 cyclic subgroups as $A_5$ and
   $\mathrm{SL}(2,5)$. That is a bound on the absolute count,
   whereas this package treats equality in the normalized bound
   for arbitrarily many prime divisors.

## What is and is not new here

The solvability criterion, its sharpness examples, the elementary
element-order formula, and the quotient inequality are prior work.
The general shape of the socle reduction follows the first source.
The contribution is the complete equality analysis, including arbitrary
solvable radicals, expressed through a general transfer theorem and
the exact elementary abelian extension formula in PROOF.md.
No separate historical priority claim is made for that elementary formula.

The simple-group strictness is extracted from existing proofs, not
presented as a new family-by-family classification. The identity subgroup
is omitted by the nontrivial conjugate-subgroup lower bounds in Appendix D,
which supplies the necessary strict margin. Appendix C's only equal
comparisons are the two presentations of $A_5$; Appendix E's finite
comparisons are already strict. PROOF.md gives the complete audit.

Live searches used combinations of the paper title, author names,
“cyclic subgroups”, “equality”, “solvability”, “A5”, and “squarefree”.
They found no primary source stating the unrestricted necessity result.
This supports novelty relative to the searched sources, not a guarantee
of historical priority. In particular, the original graph conjecture
has been resolved in the literature and is not described here as open.

## Graph provenance

The target was selected from Discovery Net before consulting new literature.

* Original conjecture:
  `bafkreihaxgig7vbsmocdq7wbyisbl3hij6aglafg3qhyfvoxqz6zezyzuy`.
* Committed source-status correction, pointing to the resolved theorem:
  `bafkreicgxul7lxdpgraeom3sprsowio7aucm2ue7qbto4ur73geq7jn654`.
* Prior equality result restricted to alternating almost-simple socles:
  `bafkreidxtkc3rpo5e2nz53hr6wjbxvlqnqs7mw4qnqdhku2q64on5lb2zm`.
  Its [published proof](https://github.com/helgithorskarp/math_results/tree/main/group_theory/alternating_socle_cyclic_subgroup_bound)
  is consistent with the restriction of the new theorem.

No current researcher owned the equality target at selection.
No review of this new theorem is implied by prior graph reviews.

## Trust boundary

The general transfer theorem and extension formula have self-contained
written counting proofs apart from elementary finite-group structure
(minimal normal subgroups, socles, solvable radicals, and automorphisms
of products of simple groups). The coprime elementary abelian splitting
step is proved by averaging, so no black-box splitting theorem is needed.

The concrete $A_5$ classification additionally imports the
classification-dependent simple-group estimates in the first source,
including its Lie-theoretic and character-table inputs. We audited
strictness in those proofs; we did not independently reproduce that
57-page theorem or its GAP computations. The companion Python checker
requires none of those data and does not certify them.

No formal proof-assistant verification or independent peer review has
yet been performed. No downloaded third-party paper, private graph data,
credential, or large generated artifact is included in this directory.
