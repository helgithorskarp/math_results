# Sources, theorem alignment, and scope of attribution

Primary-source audit: 22 September 2026. The proposed contribution consists
of the order-ideal antipodal construction, the common-neighbor illumination
cover, their exact formula for joins of comparability graphs, and the
resulting count-preserving encoding of bipartite independent-set counting
as ordinary and fractional illumination. No claim of historical priority
or independent acceptance is made.

1. Vladimir Grujić, *Counting faces of graphical zonotopes*,
   [author manuscript, arXiv:1604.06931v2](https://arxiv.org/html/1604.06931),
   Section 2. The graphical-arrangement normal fan and the vertex bijection
   with acyclic orientations are classical inputs. We recall their proofs
   to fix the weighted support and orientation conventions. This paper
   concerns face enumeration; it does not supply our illumination formula.

2. Liran Rotem, Alon Schejter and Boaz A. Slomka, *The complex
   Illumination problem*, Combinatorica **46** (2026), article 3,
   [primary article](https://link.springer.com/article/10.1007/s00493-025-00195-7).
   Theorem 3.1 recalls Martini's real-zonotope bound; Appendix B, Lemma B.1,
   records invariance of ordinary/fractional illuminating measures under
   positive generator rescaling. These facts and the illumination
   conjecture for zonotopes are prior work. Our proof checks weighted
   supports directly and does not claim affine equivalence after arbitrary
   changes of positive weights.

3. J. Scott Provan and Michael O. Ball, *The Complexity of Counting Cuts
   and of Computing the Probability that a Graph is Connected*, SIAM
   Journal on Computing **12**(4) (1983), 777--788,
   DOI `10.1137/0212053`,
   [primary-paper scan at UC Davis](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Provan.pdf).
   The unnumbered Theorem on p.779, items 1--3, states `#P`-completeness
   for counting bipartite vertex covers, bipartite independent sets and
   antichains. The reduction convention on p.779 allows polynomially many
   oracle evaluations. Section 2, reduction 1, pp.782--783, uses
   interpolation to reduce vertex-cover counting to its bipartite version;
   reductions 2--3 give complementation and the height-two poset encoding.
   These pages were visually checked in the scanned primary text.
   Accordingly our corollary uses polynomial-time **Turing** reductions,
   not an unverified parsimonious completeness claim. Our new geometric
   transformation itself preserves the count exactly. The existing
   hardness theorem and the bipartite-poset correspondence are credited
   inputs, not new counting-complexity results.

4. Károly Bezdek and Muhammad A. Khan, *The geometry of homothetic
   covering and illumination*,
   [author manuscript, arXiv:1602.06040](https://arxiv.org/html/1602.06040),
   definitions and Section 3.3.3. Fractional illumination and antipodal
   lower bounds are established methods. Our equality uses a displayed
   finite certificate, not a claim that integral and fractional illumination
   coincide for arbitrary zonotopes.

5. V. Boltyanski and H. Martini, *Covering Belt Bodies by Smaller
   Homothetical Copies*, Beiträge zur Algebra und Geometrie **42**(2)
   (2001), 313--324,
   [primary archive PDF](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.42/no.2/b42h2mar.pdf).
   The previously inspected Section 2, Remark 2 and Lemmas 1--3 include
   classical low-dimensional values and antipodal certificates. General
   zonotope upper bounds and those special cases are not offered as new.

The graph-first anchor is the previous campaign
[complete multipartite theorem](../multipartite_zonotope_illumination/),
graph `bafkreibhpfxhrqajj534etfrvj735puftdp75flt23uf3ntuiuc2makzpe`,
committed at height 5651. Its exact formula is recovered by taking all
poset factors to be antichains. Its separate full-source-sign-cone
characterization remains unchanged. The new concentrated-negative-coordinate
construction needs only a common neighbor; it does not extend the old
claim to entire sign cones. The new lower proof uses three-level
covectors and ideal cuts rather than independent multipartite blocks.

The earlier
[circuit/cactus theorem](../circuit_zonotope_illumination/) supplies the
scope control `I(Z_C6)=I_f(Z_C6)=20`, compared with the new lower bound 17.
Its graph reference is
`bafkreignws6arp7zox3iz5ps3h5fukyz5yvugkp2bwvwhis26cl3h5awf4`;
the accepted review and its normalization clarification were previously
inspected. It is not used in the proof of the join formula or complexity
corollary, and its review does not review this contribution.

Bounded searches compared graphical/graphic zonotopes, illumination,
homothetic covering, comparability graphs, order ideals, antipodal sets,
independent sets, and counting/computational complexity. No identical
join formula, ideal certificate, or restricted geometric counting
equivalence was found in the primary sources inspected. This is only a
search-relative novelty boundary. We do not claim that all prior work on
illumination complexity has been exhausted or that the corollary is the
first hardness result in that subject.

The ideal/antichain bijection, ordinal sums, normal-cone criteria and
antipodal-measure argument are standard tools. The full structural
certificates are the proposed advance. The completed illumination-product
and tensor-power branch is not used or reopened. No theorem from an
inaccessible priority source is inferred from its title or abstract.
