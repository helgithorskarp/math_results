# Prior work and scope of the claim

Primary-source audit: 21 September 2026. No historical priority claim is
made. The proposed contribution is the uniform formula `2^n+2`, with an
explicit parity cover and matching antipodal certificate, for positive
weighted graphical zonotopes of `K_(2,n)`.

1. Liran Rotem, Alon Schejter and Boaz A. Slomka, *The complex
   Illumination problem*, Combinatorica **46** (2026), article 3,
   [full primary article](https://link.springer.com/article/10.1007/s00493-025-00195-7).
   The real illumination conjecture remains open in general. Theorem 3.1
   recalls Martini's classical `3*2^(d-2)` bound for nonparallelotope
   real zonotopes. Appendix B, Lemma B.1, explicitly proves invariance
   of illuminating measures, and hence ordinary and fractional numbers,
   under arbitrary positive rescaling of generators. Those sections
   were read. The weighted extension in our theorem uses this known
   invariance, also explained directly through normal fans in our proof.

2. Vladimir Grujić, *Counting faces of graphical zonotopes*,
   [arXiv:1604.06931v2](https://arxiv.org/html/1604.06931).
   Section 2 explains the classical normal-fan/graphical-arrangement
   correspondence and the bijection between vertices and acyclic
   orientations. This supplies standard context for our separate
   graph-based checker; neither correspondence is claimed new.

3. V. Boltyanski and H. Martini, *Covering Belt Bodies by Smaller
   Homothetical Copies*, Beiträge zur Algebra und Geometrie **42**(2)
   (2001), 313--324,
   [primary archive PDF](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.42/no.2/b42h2mar.pdf).
   Sections 2--3, including Remark 2 and Lemmas 2--3, were checked in
   the preserved primary text. Remark 2 gives the known value six for
   parallelogramic dodecahedra, including our `n=2` case. The value four
   at `n=1` is the classical parallelogram value. Lemma 2 concerns a
   four-dimensional zonotope with five generators; it is not our
   six-generator `K_(2,3)` family. Lemma 3 gives a `5*2^(d-3)` upper
   bound for indecomposable zonotopes in dimension at least four.
   The present exact formula does not replace or claim authorship of
   these earlier general bounds.

4. Károly Bezdek and Muhammad A. Khan, *The geometry of homothetic
   covering and illumination*,
   [arXiv:1602.06040v2](https://arxiv.org/html/1602.06040).
   The survey's definitions, general context and fractional-illumination
   discussion were checked. Classical illumination, fractional
   illumination, and quantitative illumination parameters must not be
   conflated; this note concerns the first two only.

The existing campaign's
[circuit/cactus theorem](https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/circuit_zonotope_illumination)
and its
[normalization addendum](https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/circuit_zonotope_illumination_addendum)
were inspected as graph context. They concern individual circuits or
independent circuit spans. For `n>=3`, the present graph has overlapping
four-cycles; this is a different structural family. The proof here does
not invoke the circuit formula or its chain cover. Neither that theorem
nor its completed review repair is republished.

Bounded searches combined graphical zonotopes, complete bipartite and
two-hub graphs, illumination numbers, sphere/cube sign patterns, and the
candidate formula. No identical all-`n` formula or parity construction was
found in the inspected primary texts. This is search-relative novelty,
not an exhaustive literature exclusion. The known low-dimensional values,
normal-fan methods, rescaling invariance, and antipodal lower-bound method
are explicitly credited. The general illumination conjecture, arbitrary
graphical zonotopes, zero weights and graphs with more hubs are outside
the result.
