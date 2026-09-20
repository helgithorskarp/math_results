# Primary sources and novelty boundary

Checked 2026-09-20.

1. **Michael A. Bekos, Michael Kaufmann, Maximilian Pfister**,
   *Approximating Barnette's Conjecture*, GD 2025, LIPIcs 357, Article 6.
   [Publisher full text](https://drops.dagstuhl.de/storage/00lipics/lipics-vol357-gd2025/html/LIPIcs.GD.2025.6/LIPIcs.GD.2025.6.html),
   [DOI](https://doi.org/10.4230/LIPIcs.GD.2025.6).
   Section 2 specifies the dual-tree traversal, including a blue leaf root.
   Properties 1--4 supply the algorithm facts used here. Observation 2
   supplies the leaf/full sufficient condition for Hamiltonicity.
   Section 5, Question 2 asks recovery of an arbitrary prescribed cycle.
   Our proof identifies the exact eligible cycles and constructs a rootable
   leaf/full tree for each. The graph-to-tree disk argument and tree
   completion are supplied here, rather than assuming that arbitrary
   spanning trees have blue leaves.

2. **Muhammad Jawaherul Alam, Michael A. Bekos, Vida Dujmović,
   Martin Gronemann, Michael Kaufmann, Sergey Pupyrev**,
   *On dispersable book embeddings*, Theoretical Computer Science 861
   (2021), 1--22,
   [DOI](https://doi.org/10.1016/j.tcs.2021.01.035).
   Origin of the algorithm; its exact properties are read in source 1.
   The journal text itself is not an additional independently audited
   premise here.

3. **Behrooz Bagheri Gh, Tomas Feder, Herbert Fleischner, Carlos Subi**,
   *On Finding Hamiltonian Cycles in Barnette Graphs*,
   [arXiv:2212.02668v2](https://arxiv.org/html/2212.02668v2).
   Theorem 3.3 relates separation of face colors by a Hamiltonian cycle,
   A-trails, and spanning trees of faces. Its proof uses the weak dual of
   an outerplane graph. The underlying topological mechanism is prior work;
   our recovery theorem is an explicit algorithm-specific consequence
   combined with source 1. The product count concerns ordinary dual-tree
   completions with a designated blue leaf, not a new tree-of-faces theory.

4. **Lennart Rudolph**, *A Counterexample to Prescribed-Cycle Recovery
   in Barnette Graphs*, preprint dated August 11, 2026.
   [Zenodo record](https://zenodo.org/records/21890733),
   [DOI](https://doi.org/10.5281/zenodo.21890733),
   [author-uploaded full text](https://www.researchgate.net/publication/413747008_A_Counterexample_to_Prescribed-Cycle_Recovery_in_Barnette_Graphs).
   The full text and Zenodo API metadata were inspected. The displayed
   16-vertex graph gives a cycle omitting all three color classes, already
   disproving universal recovery. Its facial cycles and face colors are
   included as a credited fixture, independently checked by our verifier.
   We do not claim priority for the negative answer. Our two-cube fixture
   is illustrative, not a minimality result.

5. **Tobias Schnieders**, *Barnette Graphs with Faces up to Size 8
   are Hamiltonian*, [arXiv:2508.03531](https://arxiv.org/html/2508.03531).
   Current neighboring Hamiltonicity scope; not a proof dependency.
   Its introductory statement leaves the unrestricted conjecture open.

Bounded searches for prescribed-cycle recovery, the paper title, and
matching/color-class converses found sources 1, 3, and 4 but no explicit
blue-leaf-rooted recovery characterization or the stated rooted completion
count. This is a search-relative status statement, not a priority claim.
In particular, the original negative-answer target was abandoned as new
work when source 4 was found.
