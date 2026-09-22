# Sources and status boundary

Checked on 2026-09-22.

1. A. G. Chetwynd and A. J. W. Hilton, *Some refinements of the total
   chromatic number conjecture*, Congressus Numerantium 66 (1988), 195--216.

   This is the original conformability source.  In particular, a Type-1
   total colouring induces a conformable vertex colouring.  The proof in
   this directory re-derives exactly the regular even-order parity statement
   it needs.

2. H. P. Yap and K. H. Chew, *Total chromatic number of graphs of high
   degree, II*, Journal of the Australian Mathematical Society 53 (1992),
   219--228.
   <https://doi.org/10.1017/S1446788700035801>

   The abstract explicitly records that the Total Colouring Conjecture holds
   for every graph of order `N` with maximum degree at least `N-5`.  This is
   the upper-bound input for complement degree `r<=4`.

3. K. H. Chew, *Total Chromatic Number of Graphs of High Maximum Degree*,
   Journal of Combinatorial Mathematics and Combinatorial Computing 18
   (1995), 245--254.
   <https://combinatorialpress.com/article/jcmcc/Volume%2018/vol-18-paper%2023.pdf>

   Chew proves `chi''(G)<=Delta(G)+2` when
   `Delta(G)>3|V(G)|/4-1/2`.  For `G=complement(H)` this becomes the threshold
   `N>4r+2` used here.

4. J. K. Dugdale and A. J. W. Hilton, *The total chromatic number of regular
   graphs of order 2n and degree 2n-3*, Journal of Combinatorics, Information
   & System Sciences 15 (1990), 103--110.

   This directly settles the complement-degree-two (`r=2`) classification.
   It was located during the primary-status gate, so neither the 2-factor
   special case nor the parity observation is claimed as new here.  The
   explicit family in this directory starts at complement degree three.

5. J. K. Dugdale and A. J. W. Hilton, *The Total Chromatic Number of Regular
   Graphs Whose Complement Is Bipartite*, Discrete Mathematics 126 (1994),
   87--98.  <https://doi.org/10.1016/0012-365X(94)90255-0>

   This is adjacent exact prior work for bipartite complements.  The cubic
   complements constructed here are nonbipartite in general and, more
   decisively, have no perfect matching.

6. Jozsef Pinter, *Conformability is NP-complete, even on connected regular
   graphs*, arXiv:2606.21534 (2026).
   <https://arxiv.org/abs/2606.21534>

   This current primary source restates the Type-1-implies-conformable
   necessity and uses clique packings in complements for an odd-order
   complexity theorem.  It provides current context but does not state the
   even-order perfect-matching criterion or the Type-2 family proved here.

## Search boundary

Primary and bibliographic searches used the combinations `total chromatic
number complement cubic graph perfect matching`, `total coloring cubic
complement`, `regular graph degree n-4 total chromatic`, `non-conformable
perfect matching complement`, and the exact degree-`2n-3` title.  The search
located the exact 1990 prior theorem at complement degree two and the current
2026 conformability paper, but no source stating the sparse-regular-complement
criterion or the explicit cubic family above.  Novelty is therefore
search-relative; no claim of historical priority is made.
