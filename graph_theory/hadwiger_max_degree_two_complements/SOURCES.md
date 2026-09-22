# Sources and status boundary

## Primary prior art

1. Jaroslav Ivančo, *The Hadwiger number of complements of some graphs*,
   **Mathematica Slovaca** 47 (1997), no. 4, 393--403.
   [Primary PDF](https://dml.cz/bitstream/handle/10338.dmlcz/133144/MathSlov_47-1997-4_2.pdf),
   [persistent record](https://dml.cz/handle/10338.dmlcz/133144).

   Ivančo determines Hadwiger numbers of complements of graphs with no cycle
   shorter than seven (Theorems 4 and 5), using a matching obstruction.  In
   particular, this is directly relevant prior art for the present theorem's
   path and long-cycle components.  His Theorem 2 also treats Hadwiger numbers
   of graph joins.  The present package does **not** claim that the connected
   long-cycle values or the join mechanism are new.

2. Jacob Fox and Fan Wei, *On the number of cliques in graphs with a forbidden
   minor*, **Journal of Combinatorial Theory, Series B** 126 (2017), 175--197.
   [DOI](https://doi.org/10.1016/j.jctb.2017.04.004),
   [author manuscript](https://arxiv.org/abs/1603.07056).

   Lemma 2.1 proves the same general counting upper bound used here and shows
   it is attained whenever an `n`-vertex graph `G` with clique number `omega`
   and maximum missing degree `D` satisfies
   `n >= omega + 2D^2 + 2`.  Taking `G=complement(H)` and `D<=2` establishes
   the natural formula in the sufficiently dense range.  The present result
   resolves the remaining boundary exactly for `D=2`, rather than claiming
   the dense-range formula as new.

3. Deming Li and Mingju Liu, *Hadwiger's conjecture for powers of cycles and
   their complements*, **European Journal of Combinatorics** 28 (2007),
   1152--1155.  [DOI](https://doi.org/10.1016/j.ejc.2006.03.002).

   This establishes Hadwiger's conjecture for powers of cycles and their
   complements.  It is relevant to the connected cycle specialization but
   does not state the all-components exact classification used here.

4. G. A. Dirac, *Some theorems on abstract graphs*, **Proceedings of the
   London Mathematical Society** (3) 2 (1952), 69--81.
   [DOI](https://doi.org/10.1112/plms/s3-2.1.69).

   We use the theorem that an `N`-vertex graph of minimum degree at least
   `N/2` is Hamiltonian.

## Search and claim boundary

Before technical investment, searches were run for the exact Hadwiger number
of complements of maximum-degree-two graphs, complements of disjoint unions
of paths and cycles, and exact formulas for complements of paths and cycles.
The Ivančo, Fox--Wei, and Li--Liu papers above were the directly relevant
primary sources located.  Ivančo already covers the girth-at-least-seven
portion, while Fox--Wei gives the formula outside a bounded missing-degree
boundary.

The potentially new content is therefore scoped narrowly: a single exact
classification for **all** finite simple `H` with `Delta(H)<=2`, including
arbitrary mixtures of short and long components, with precisely eight
exceptional non-isolated cores.  The canonical forbidden-graph proof also
compresses the mixed-component problem to a maximum-degree-two matching
boundary.

This is a search-relative status report, not a claim of historical priority.
The source search cannot rule out an equivalent result under different
terminology or in an unindexed source.
