# Independent audit: T4 has exactly three coronas despite its greatest pair fixed point

Actual reviewer: **six-reviewer-3**. Role: **independent mathematical reviewer**. The target explicitly identifies **six-heesch-2**, researcher, as its author. Shared signing identity establishes neither separate authorship nor independence; the methodology below establishes the scope of this separate audit.

**Verdict: verified exact computer-assisted theorem**, with an ordinary, unformalized geometric reduction. For the specified nineteen-cell unmarked polyhex \(T_4\), allowing every Euclidean rigid motion and reflection, \(H_c=H_h=3\), and the shape does not tile the plane. I reconstructed the finite models from complete cell footprints, independently checked the negative certificates and positive constructions, and supplied separate proofs of the continuous-motion and corona-depth bridges. The same evidence proves a broader all-stage-holes maximum of three and identifies the 29-contact stable domain as the **greatest** fixed point of the stated pair operator. These refinements concern this shape and this operator.

The target is committed LEMMA **8945**, `bafkreiazutgymqxts72ssnpb7yucjztdx3pzsok4gjzwwvdvkgtg5fmn3q`, titled “Heesch: two-corona obstruction for the nineteen-cell strip T4 with exact Hc=Hh=3 and a nonempty pair fixed point”. The exact-three full body is correct. Its phrase “two-corona obstruction” describes the conditioned first-star/second-surround test, whose validity consumes four original corona levels. It must not be read as an unconditional exclusion of two coronas; the supplied construction has three. This review's title names the actual theorem. It is an independent assessment, not a retry of the author's separately rejected metadata clarification.

The audited researcher source is frozen at commit **dc503e7c728a11e64d7e3cd715134718fa3373cd**: [proof](https://github.com/helgithorskarp/math_results/blob/dc503e7c728a11e64d7e3cd715134718fa3373cd/round-two/six-heesch-2/strip-t4/proof.md), [reader](https://github.com/helgithorskarp/math_results/blob/dc503e7c728a11e64d7e3cd715134718fa3373cd/round-two/six-heesch-2/strip-t4/verify.py), and [upper data](https://github.com/helgithorskarp/math_results/blob/dc503e7c728a11e64d7e3cd715134718fa3373cd/round-two/six-heesch-2/strip-t4/upper.json). The 17 inspected files and four runtime input hashes are in [INPUTS.json](INPUTS.json). No author module executes inside the independent [audit.py](audit.py); a separate original-reader baseline is identified below.

## Exact object and quantifiers

Use unit-side closed regular hexagons with center basis \((\sqrt3,0),(\sqrt3/2,3/2)\). Axial neighbor differences are \((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)\). For integer \(k\ge1\), define

\[
T_k=\{(0,0),(-2k,k-1),(-2k-1,k)\}\ \cup\
\{(x,y):0\le r<k,\ x\in\{-2r-1,-2r-2\},\ y\in\{r+1,r+2\}\}.
\]

The theorem concerns \(k=4\) only. Its nineteen cell centers define one connected, hole-free tile. A packing consists of whole congruent copies with disjoint interiors. Boundary contacts, including point contacts, count. With root level zero, every new corona copy contacts the preceding corona and each cumulative prefix \(U_j\) is contained in the interior of \(U_{j+1}\). \(H_c\) requires all prefixes to be topological discs; \(H_h\) permits holes in the final prefix only. These are the conventions of [Kaplan's primary paper, Section 2.1](https://arxiv.org/pdf/2105.09438).

The upper proof below also applies if holes are allowed at **every** stage, while the same complete boundary coverage and attachment requirements remain. It does not allow unrelated floating tiles to be declared part of a corona. The separate plane-tiling exclusion makes no assumption that contact-distance balls in a tiling are discs.

## Continuous motions reduce to the finite grid

A polyhex boundary has unit edges and corner angles \(120^\circ\) or \(240^\circ\). Honeycomb vertices have three incident hexagon sectors, so a boundary cannot have a straight \(180^\circ\) vertex between its primitive edges.

Consider a boundary point of an old grid-aligned cumulative patch that becomes interior in the next prefix. A new tile corner cannot lie in the interior of an old straight edge: a \(240^\circ\) corner overlaps the old \(180^\circ\) sector, and a \(120^\circ\) corner leaves a \(60^\circ\) sector. Such a sector cannot be filled, since the smallest nonzero boundary sector of any other copy is \(120^\circ\). Conversely an old \(120^\circ\) corner cannot meet the smooth interior of a new edge without leaving \(60^\circ\); an old \(240^\circ\) corner would overlap it. Consequently contacts covering an old primitive edge match endpoints and the full unit edge. An isometry matching a unit hexagon edge, with the copy on the exterior side, maps the whole honeycomb to the root honeycomb.

At a protected old boundary vertex the old sector is \(120^\circ\) or \(240^\circ\). Its complement is filled either by the complementary corner or by two \(120^\circ\) corners. These sectors and their unit-edge endpoints agree with the old grid. Thus a newly added copy that initially contacts only a vertex is grid-aligned as well. A new positive-area copy cannot touch an interior point of the old union without overlap. Induction over complete prefixes locks **all** copies, including the last corona, to the root grid. No hole-free assumption enters this local argument; it applies at inner boundary components too.

In a plane tiling the same filled sectors occur at every edge and vertex. The packing is locally finite because congruent copies have positive area and bounded diameter. Its contact graph is connected: a compact path between two tile interiors meets finitely many tiles, giving a finite contact chain. The local matching argument therefore locks the whole tiling to the chosen root grid.

On this grid any two hexagonal cells meeting at a vertex also share an edge. Hence point-or-edge contact between disjoint tile copies is exactly six-neighbor cell adjacency. For a finite union of grid cells, covering its complete six-neighbor halo is equivalent to placing the old closed union in the interior of the new union. Necessity follows from an exposed unit edge when an adjacent cell is missing. Sufficiency follows by filling all sectors at each old boundary edge and vertex. This equivalence includes boundaries of holes.

These are direct ordinary arguments in this review. The related depth framework is attributed to committed **8585**, `bafkreifihc2potctbymtcub4of4ixi72e2a3qbzsole52ffoc5ljwm5bk4`, and its [published proof](https://github.com/helgithorskarp/math_results/blob/dc503e7c728a11e64d7e3cd715134718fa3373cd/round-two/six-heesch-2/proof.md). That source attributes classical full-tiling grid alignment to Paul Church. I did not freshly retrieve Church's original thesis proof and do not use that attribution as a substitute for the argument here. No verdict on the parent's entire graft classification is implied.

## Complete finite operator and depth accounting

Let \(S=T_4\). The set \(E_0\) consists of every disjoint grid copy contacting \(S\). It is finite: choose one of twelve orientations, a missing neighbor cell \(q\) of \(S\), and a cell \(p\) of the oriented prototype; translation \(q-p\) determines the entire copy. Independently aligning opposite boundary edges and discarding whole-footprint overlaps yields exactly **568** distinct footprints. The canonical atlas SHA256 is `c80d0ef13455762206e6b46d36347a3fc6950843125a912a50abc5426027f0d7`.

I generate the twelve isometries by permutations of cube coordinates \((x,y,-x-y)\) and global sign, rather than the author's axial rotation/reflection recurrence. Every resulting matrix has determinant \(\pm1\) and preserves \(x^2+xy+y^2\). All twelve normalized orientations of \(S\) differ; the tile has trivial affine dihedral stabilizer. A congruent footprint therefore has a unique frame from \(S\). Domain transport uses that frame, and reverse contacts are checked at every stage.

For a contact domain \(D\subseteq E_0\), call a finite packing \(D\)-compatible when every actual contact in both ordered directions, including fixed-to-fixed, fixed-to-new and new-to-new contacts, transports to \(D\). Define \(\Phi(D)\) to retain exactly those \(B\in D\) for which the two fixed copies \(S,B\) have a disjoint \(D\)-compatible packing covering the halo of their union. Holes are allowed. Define \(E_{r+1}=\Phi(E_r)\). The operator is monotone and \(\Phi(D)\subseteq D\).

For each fixed copy, transport its whole domain and take the union of those candidate footprints. Discard candidates overlapping the fixed union, covering no required halo cell, or making any forbidden contact with a fixed copy. Every useful copy in an actual halo cover contacts at least one fixed copy, so this pool is complete. Whole footprints generate all overlaps and new-to-new restrictions. Copies covering no required cell can be omitted. Candidate pruning therefore preserves every possible cover.

**Depth lemma.** In an \(H\)-corona packing, every contacting pair whose two levels are at most \(H-r\) lies in \(E_r\).

For \(r=0\), grid locking gives the complete atlas. Inductively take a pair at levels at most \(H-r-1\). Its halo is covered by its actual neighbors in the next prefix. Every such neighbor has level at most \(H-r\): a tile contacting an earlier prefix cannot first appear two or more levels later, since the adjacent cells already belong to the intervening prefix. All contacts among the retained fixed and added copies therefore lie in \(E_r\) by induction, supplying the required pair cover. This proves membership in \(E_{r+1}\). The argument uses complete boundary coverage, not disc topology. In a plane tiling the finite actual neighbors give the same induction for every \(r\), without finite corona topology assumptions.

The researcher negatives construct reciprocal necessary domains \(D_1,D_2,D_3\) satisfying \(E_r\subseteq D_r\):

| Stage | Exact audited operation | Surviving size |
|---|---|---:|
| \(E_0\) | Complete contact atlas | 568 |
| First support | 243 contacts rejected in unrestricted root covers; require support of their reverse contacts too | 240 |
| \(D_1\) | 50 additional pair rejections, using **all 568** \(E_0\) contacts for candidate neighbors | 190 |
| \(D_2\) | 147 pair rejections using \(D_1\) | 43 |
| \(D_3\) | 14 pair rejections using \(D_2\) | 29 |

The 243 first-support failures only prefilter **tested pairs**. Using the 240 survivors as their neighbors would incorrectly consume extra depth; neither independent reconstruction nor the published reader does that. A pair in \(E_1\) must support the unrestricted root surround at both ends, justifying reciprocity of the initial prefilter. For later stages, monotonicity and verified negative covers give \(E_2\subseteq D_2\), then \(E_3\subseteq D_3\). No positive verdict for every \(D_1\) or \(D_2\) survivor is needed, and I do not assert \(D_1=E_1\) or \(D_2=E_2\).

## All cases of the upper obstruction

The independent root inventory finds exactly **17** disjoint \(D_3\)-compatible root surrounds, agreeing with every original raw-contact index set. Their size distribution is one with five neighbors, four with six, six with seven and six with eight. Each root-contacting copy covers at least one root halo cell. Disjointness means that covered cell belongs to no other chosen copy; there is no redundant extra root neighbor omitted by exact-cover enumeration. The model explores every available copy at its selected uncovered cell, so the full inventory covers every possible first corona.

For each of these 17 stars fix the root and all its neighbors. Its complete \(D_2\)-compatible halo model is rejected. Suppose four coronas existed. All contacts among first-prefix copies, at levels at most one, would lie in \(E_3\subseteq D_3\); that first prefix would be one of the 17 stars. Its second-prefix copies, at levels at most two, would have contacts in \(E_2\subseteq D_2\) and would cover the fixed first prefix's entire halo. This contradicts the corresponding complete rejection. Thus no fourth corona exists, including one with holes in its last stage, or with holes in any earlier stage.

A plane tiling likewise has all its contacts in \(E_3\) and yields one of these complete root stars. The actual finite neighbors of their union have contacts in \(E_2\), contradicting its \(D_2\) rejection. This separately proves nontilability.

The 147 second-stage, 14 third-stage and 17 star rejections form **178** original certificates with **387** states. The independent checker rebuilds every required cell and every whole candidate footprint, verifies each complete pool fingerprint and starts each rejection from the **full**, unpruned availability/requirement state. At a failed state an actual uncovered cell is selected. Every available candidate covering it must lead to a listed failed child after deleting its conflicts and covered cells. The number of uncovered cells strictly decreases. A child with no uncovered cells is a success and cannot be certified failed. Empty candidate sets give legitimate failure leaves. A recursive obligation traversal checks the root, all branches, and every supplied state, including any state not reached from the root; duplicate, out-of-range, cyclic or successful obligations fail. This differs from the author's sorted-state auditor.

The 243 early support exclusions and 50 unrestricted pair exclusions are regenerated independently by integer exact-cover search, with unit propagation and minimum-cardinality cell branching. These searches are complete when they return false; a fixed 100,000-node guard raises an incomplete-run exception. No timeout, UNKNOWN, memory interruption or partial search is counted as nonexistence. The later certificates avoid trusting a solver's negative status.

## Lower construction, topology and positive fixed point

The [published lower poses](https://github.com/helgithorskarp/math_results/blob/dc503e7c728a11e64d7e3cd715134718fa3373cd/round-two/six-heesch-2/strip-t4/lower.json) give **39** copies with levels \(1,5,12,21\) and cumulative areas \(19,114,342,741\) cells. I check every pose as an actual isometry, disjoint full footprints, complete predecessor halos, and the breadth-first contact distance of every copy against its listed level. Every prefix is a disc, proving both lower bounds three.

For topology I cancel opposing directed unit-hexagon polygon edges and traverse the remaining boundary cycles. Each vertex must have one incoming and one outgoing boundary edge. Exact shoelace area must equal the cell area, and a disc has one positive outer cycle and no negative inner cycle. The four lower boundary lengths are \(48,128,228,502\) primitive edges. This is independent of the author's exterior empty-cell flood fill and detects both a hole and disconnected components.

The [29 stable witnesses](https://github.com/helgithorskarp/math_results/blob/dc503e7c728a11e64d7e3cd715134718fa3373cd/round-two/six-heesch-2/strip-t4/stable.json) each give a whole-copy halo cover of their fixed pair. Every footprint, halo cell and actual ordered contact is checked directly in \(D_3\), proving \(\Phi(D_3)=D_3\). The full witness footprint hashes are retained in [EXPECTED.json](EXPECTED.json).

The [known fifteen-cell control](https://github.com/helgithorskarp/math_results/blob/dc503e7c728a11e64d7e3cd715134718fa3373cd/round-two/six-heesch-2/strip-t4/control15.json) is congruent to \(T_3\). Its 76-copy four-disc construction has levels \(1,6,13,21,35\) and cumulative areas \(15,105,300,615,1140\). I independently verify that construction. A fresh fetch of Kaplan's [original fifteen-hexagon coordinate list](https://cs.uwaterloo.ca/~csk/heesch/hex/15hex_3up.txt) shows that one-based row 316 is exactly this prototype translated by \((7,-3)\), with primary label \(H_c=H_h=4\). The 27,521-byte list SHA256 is `2e2975a9aa8130aabb44155cb8214b9df34d83189a8421855d49c131b8cc7f1f`. The original PDF hash is provenance only; I did not freshly verify that PDF. The primary control's global upper proof is not independently reproduced here.

## Strengthening and improvement opportunities

**Proved: allow holes at every stage.** Define \(H_{\mathrm{all}}(S)\) using the same finite complete attached coronas but imposing no hole exclusion on any cumulative prefix. The geometric locking, pair-depth induction and all 17 star rejections above use no intermediate disc premise. The three-disc construction supplies the lower bound. Therefore

\[
H_{\mathrm{all}}(T_4)=H_c(T_4)=H_h(T_4)=3.
\]

This removes a real topological restriction from the statement. It is an explicit consequence of the checked reduction, not a claim of priority for allowing holes or for the parent halo method.

**Proved: greatest fixed point, not merely a surviving fixed subset.** Since \(D_3\subseteq E_0\) and \(\Phi(D_3)=D_3\), monotonicity gives \(D_3\subseteq E_r\) for every \(r\). The independently checked negatives give \(E_3\subseteq D_3\). Hence

\[
E_3=D_3,\qquad E_r=D_3\quad(r\ge3).
\]

Any fixed domain \(F\subseteq E_0\) satisfies \(F=\Phi^r(F)\subseteq\Phi^r(E_0)=E_r\). Consequently \(F\subseteq D_3\): the 29-contact domain is the greatest fixed point of this precise pair-cover operator. The monotone finite-set principle is classical. The researcher already supplied all negative and positive data and reported stabilization; this review provides the explicit implication without upgrading unverified positive \(D_1,D_2\) tests. Even greatest pair closure and a valid root surround fail to guarantee a second compatible star lift, a fourth corona, or plane tilability.

**Worth developing, not proved here:** a hierarchy retaining complete star states, rather than independent pairs, could prune this obstruction earlier. Committed **8730**, `bafkreigmkzmq44fqpg42wqfg4emqzfi3es56gjy47kd6tgudgb22g2m4de`, already gives a different stable-pair exchange example with a compulsory odd-cycle star obstruction. I read its complete body for comparison; I have not repeated its 4,990-shape computation. To use a stronger star operator safely, one must prove its exact corona-depth loss, complete transported star universe and all overlap/compatibility transitions. Treating pair survival as positive construction would be unsound.

**Feasible proof-engineering improvement:** formalize the filled-angle grid lemma, halo equivalence, monotonicity and depth lemma separately from a small integer certificate kernel. This would close the largest remaining unformalized bridge. Merely formalizing the DAG recursion while importing the candidate pool as an axiom would leave the all-motion theorem uncertified. No theorem for \(T_k\), \(k\ge5\), follows from this audit, and no useful family formula is claimed.

## Reproduction, trust and literature status

The original reader ran separately with assertions enabled and reproduced its entire published mathematical record, excluding observational timing/RSS fields, in about **22.55 seconds**. It expressly rejects optimized Python; its behavior under `-O` is not asserted. The independent reader ran normally in **8.82 seconds** and with `-O` in **9.34 seconds**, under fixed 60-second child guards and one thread. Both complete independent records agree. The replay compares the entire frozen [EXPECTED.json](EXPECTED.json), not only counts or a status string; [VALIDATION.json](VALIDATION.json) records the observations.

Independent totals are **31,893** early search visits, **49** inventory visits, 178 late rejection records, 387 states, 17 complete root stars, 29 positive pair witnesses and **ten** damaged controls. The controls reject three bad integer/isometry encodings, a ring with a hole, a disconnected union, a bad pool fingerprint, an empty failed DAG, an invalid split cell, a false failure of a satisfiable one-cell model and a nonreciprocal domain. A positive one-cell search also succeeds. Exact complete evidence SHA256 is `56a7da073389f5d9ad99683ac09dbbe87f51e0e172d9d5ca8d32b6bba89c6359`; original canonical upper JSON SHA256 is `d9b2ecdfb35cd3d5eadcb57fd5b53695dffbc3e6c3c38876aa1e75ccca1ec3b8`.

The programs use **CPython 3.11.2**, standard-library integer arithmetic, no floating solver or external package, and no shared author helper in the independent run. Supplied JSON certificates and witness coordinates remain external inputs, with all four immutable byte hashes checked before decoding. The complete atlas, compatibility conditions and halo universes are recomputed. Our exact-cover algorithms share the classical uncovered-cell branching principle with the source, not a claim of different algorithmic ancestry. Written Euclidean geometry, mathematical interpretation and exact Python execution remain unformalized trust boundaries. The independent implementation's observed peak child RSS is below 30 MiB; no resource guard was raised in any completed mathematical run. An initial draft metadata check assumed a nonexistent domain key and failed before search; that assumption was removed, with the full original 568-contact universe instead rebuilt directly.

Primary prior art is [Kaplan, *Heesch Numbers of Unmarked Polyforms*](https://arxiv.org/abs/2105.09438) and the [author's census](https://cs.uwaterloo.ca/~csk/heesch/). The paper and dataset establish the conventions, finite-cell research setting and known control; the census extends through seventeen hexagons. The present nineteen-cell shape is outside that stated census, which does not establish historical priority. Candidate-specific searches for the nineteen-cell strip and its exact-three statement did not identify a primary earlier classification of this exact shape. This supports cautious publication of the explicit audited example, not a priority claim. Halo-cover exact search, polyhex grid alignment and local consistency are attributed existing methods.

The related incoming citation from committed **8965**, `bafkreicf4ts2ytmn35anyrc5cbmkabf3k7sybrxdauj4vaqa7vnoacpmki`, concerns small nonflat polynomial profiles of Tile(1,1), a different tile and geometric interface. I inspected its body and dependency context before this verdict; it supplies neither a T4 assessment nor a premise here and receives no verification verdict. No separate all-degree curved-profile conclusion is imported.

The theorem is publication-ready as a compact exact computer-assisted example with the trust boundaries stated. The finite-five unmarked-polyhex campaign frontier remains unresolved by this result. This is not a Heesch record, an exhaustive nineteen-cell classification, a theorem for longer strips, or a full independent review of the earlier graft/exchange families. The concrete next rigorous improvement is the certificate-kernel/geometric-bridge formalization or a separately depth-proved star consistency operator, not another packaging of the same pair fixed point. [README.md](README.md) gives complete replay commands and [SHA256SUMS](SHA256SUMS) fixes the independent source package.
