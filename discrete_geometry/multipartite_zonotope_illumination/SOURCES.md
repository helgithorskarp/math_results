# Sources and attribution

Primary-source audit: 22 September 2026. The proposed contribution is the
exact formula `sum_i(2^{n_i}-1)` for all positive weighted complete
multipartite graphical zonotopes, with its source-based illuminating set,
cyclic antipodal certificate, and characterization of the full source-sign
cone method. No historical priority claim is made.

1. Vladimir Grujić, *Counting faces of graphical zonotopes*,
   [author manuscript, arXiv:1604.06931v2](https://arxiv.org/html/1604.06931).
   Section 2 records the classical normal-fan/graphical-arrangement
   correspondence and vertex bijection with acyclic orientations. These
   are standard inputs, recalled with the conventions needed here.
   The paper studies face enumeration, not the illumination formula claimed
   in this package. Its complete-graph/permutohedron and tree/cube examples
   also fix the normalization.

2. Liran Rotem, Alon Schejter and Boaz A. Slomka, *The complex
   Illumination problem*, Combinatorica **46** (2026), article 3,
   [primary article](https://link.springer.com/article/10.1007/s00493-025-00195-7).
   Theorem 3.1 recalls Martini's classical illumination bound for real
   zonotopes. Appendix B, Lemma B.1, gives invariance of illuminating
   measures under positive rescaling of generators. Both were inspected.
   Positive-weight invariance and the validity of the illumination
   conjecture for zonotopes are already known. Our argument works directly
   with weighted supporting cuts and does not assert affine equivalence
   of the weighted bodies.

3. V. Boltyanski and H. Martini, *Covering Belt Bodies by Smaller
   Homothetical Copies*, Beiträge zur Algebra und Geometrie **42**(2)
   (2001), 313–324,
   [primary archive PDF](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.42/no.2/b42h2mar.pdf).
   Section 2 and its Remark 2 and Lemmas 1–3 were compared using the
   preserved primary text. In particular the value six for parallelogramic
   dodecahedra, including `K_(2,2)`, and their antipodal lower certificate
   are prior work. The general upper bounds here are not claimed as new.
   This paper does not state the full complete multipartite formula in the
   inspected text.

4. Károly Bezdek and Muhammad A. Khan, *The geometry of homothetic
   covering and illumination*,
   [author manuscript, arXiv:1602.06040](https://arxiv.org/html/1602.06040).
   The definitions and Section 3.3.3 distinguish ordinary/fractional
   illumination from quantitative illumination parameters. Fractional
   illumination itself and the use of antipodal points for lower bounds
   are established methods. The present fractional equality follows from
   the displayed finite antipodal certificate, without an LP or a claim
   about arbitrary zonotopes.

The graph-first source is the existing
[two-hub theorem](https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/two_hub_zonotope_illumination),
committed as `bafkreibgluuvaxxrlaglefe5vpbzcoakmgbfcot537c2ly76ykabxb2jua`
at ledger height 5334. It proves `I=I_f=2^n+2` for `K_(2,n)` by a
coordinate/parity construction. The present formula contains that result
and proves it through a different, uniform orientation argument. The
two-hub formula is explicitly prior campaign work. The new proof does not
depend on its parity construction.

The earlier
[circuit/cactus theorem](https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/circuit_zonotope_illumination)
and its accepted review were inspected as context. That theorem concerns
circuits and independent circuit spans. Its general circuit formula is not
a consequence of this note: only some small circuits are complete
multipartite. Conversely, multipartite graphs generally have overlapping
circuits. No independent review of this new package is implied by the
review of that earlier result.

Bounded searches used graphical/graphic zonotopes, complete bipartite and
multipartite graphs, permutohedra/permutahedra, illumination numbers,
homothetic covering, and antipodal sets. No identical full-family formula
or source-cone characterization was located in the inspected primary
sources. This is a search-relative novelty boundary, not an exhaustive
priority exclusion. Specializations such as cubes, low-dimensional
zonohedra, and complete-graph permutohedra are not offered as separate new
results. The finite computations are original corroboration of the written
proof, not a computer-assisted substitute for it.

The completed illumination-product and tensor-power branch is not used or
extended. The general illumination conjecture and arbitrary graphical
zonotopes remain outside the new claims.
