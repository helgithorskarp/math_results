# Sources and status check

Checked on 2026-09-21 and corrected on 2026-09-22.

1. Martin Juvan, Bojan Mohar, and Robin Thomas, *List Edge-Colorings of
   Series-Parallel Graphs*, Electronic Journal of Combinatorics 6 (1999),
   R42.  DOI: <https://doi.org/10.37236/1474>.  Primary PDF:
   <https://www.combinatorics.org/ojs/index.php/eljc/article/download/v6i1r42/pdf>

   Theorem 3.1 proves that, for every integer `k>=3`, every simple
   series-parallel graph of maximum degree at most `k` is
   `k`-edge-choosable.  Consequently the `Delta>=3` part of the present
   list-edge-colouring equality for simple cacti was already known; the
   `Delta<=2` cases are elementary paths and cycles.  The paper's multigraph
   remark does not give the extension proved here: under an additional
   restriction on parallel-neighbour incidences, it requires lists of size
   at least `k+1` on every edge parallel to another edge.

2. Tomoya Fujino, Xiao Zhou, and Takao Nishizeki, *List Edge-Colorings of
   Series-Parallel Graphs*, IEICE Transactions on Fundamentals of
   Electronics, Communications and Computer Sciences E86-A(5) (2003),
   1034--1045.  Primary PDF:
   <https://www.ecei.tohoku.ac.jp/alg/nishizeki/sub/j/DVD/PDF_J/J147.pdf>

   Theorem 1 proves the endpoint-sensitive sufficient condition
   `|L(vw)|>=max{3,d(v),d(w)}` for every edge of a simple series-parallel
   graph.  This strengthens the uniform-list theorem above, but is again a
   theorem for simple graphs.

3. Amir Jafari, *The List Edge-Coloring Conjecture for Two New Infinite
   Families of Complete Graphs*, arXiv:2608.22895 (2026).
   <https://arxiv.org/abs/2608.22895>

   The introduction states the List Edge-Coloring Conjecture for loopless
   multigraphs, records that the complete-graph case is unresolved in general
   for even order, and proves two new complete-graph families.  This confirms
   that the ambient conjecture remains open at the time of this note.

4. Fred Galvin, *The List Chromatic Index of a Bipartite Multigraph*, Journal
   of Combinatorial Theory, Series B 63 (1995), 153--158.
   <https://doi.org/10.1006/jctb.1995.1011>

   Galvin proves equality of list chromatic index and chromatic index for all
   bipartite multigraphs.  The present cactus theorem overlaps that result on
   bipartite cacti but also covers cacti with odd cycle blocks; its proof is
   instead an exact line-graph degeneracy argument.

## Search boundary

The primary sources above and bibliographic searches for `list chromatic
index cactus graph`, `list edge coloring cactus multigraph`, `edge
choosability cactus graph`, and `line graph degeneracy cactus` were checked.
The initial search missed the two series-parallel papers, so the simple-cactus
list-edge-colouring equality must not be presented as new.  No source stating
the exact degeneracy formula or the equal-size-list classification for
loopless cactus multigraphs with parallel 2-cycles was located.  Absence from
a bounded search is not a priority claim, and the proof is elementary enough
that rediscovery is plausible.
