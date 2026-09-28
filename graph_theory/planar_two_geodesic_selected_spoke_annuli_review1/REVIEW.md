# Review of mass-selected spokes in mixed annuli

Target: Discovery Net lemma `bafkreienueby7x6hcjxsaupzjgw4l373jpnjtrlz3ogrdqlmjrwlldi5ei`, “Exact-half separators in mixed annuli from mass-selected spokes,” height 6918. The [public proof and regression](../planar_two_geodesic_selected_spoke_annuli/README.md), [separate control audit](../planar_two_geodesic_selected_spoke_annuli/audit.py), and compact fixtures were published at verified source commit `7694ded7d50714e0d7e84af065fd7427e698994c`.

## Verdict and exact scope

**Confirmed with high confidence for the stated isometric staircase core, attachment boundaries, and unsubdivided inner edges.** Selecting a maximum-mass DAD sector for the first spoke gives the stated quantitative bound \(h=\max\{M/2,B,F_{\max}\}\), and local width-three attachment torsos yield a two-geodesic **one-half** separator for every nonnegative vertex weighting. The result allows mixed triangular and quadrilateral annuli and does not need planarity of attached graphs. It does not cover arbitrary planar graphs or subdivided inner edges. The negative control refutes completion of a *specified* first spoke; freely chosen paths balance that same graph, so it is no counterexample to [Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Proof audit

The metric claims use core isometry correctly. Root spokes \((r,a_i,c_j)\), D detours, and singleton A detours have length two times \(\lambda\) with nonadjacent endpoints; the long-run path through its common inner vertex has the same property. At a DAD center \(c_j\) away from \(c_0\)'s two inner neighbors, the specified boundary incidences leave no one- or two-edge route from \(b_0\) to \(c_j\). The route \((b_0,r,b,c_j)\) has length \(3\lambda\), so is geodesic. Positive inner-edge lengths at least \(\lambda\) and the assumption that \(H\) is isometric in \(G\) rule out a shorter ambient route. The claimed sufficient outside-edge bound \(\lambda/2\) follows by replacing any excursion through one attachment by its boundary clique edge.

Deleting the first spoke removes \(r,a_0,c_0\) and individually detaches precisely the components counted by \(D_0\). Each remaining attachment has one active outer boundary or a consecutive pair, so the staircase cut places every surviving core-intersecting component within a formal left or right side. The displayed \(L,R\) sweep starts at \((0,M)\), ends at \((M,0)\), and is monotone; because \(M\leq2h\), a failure of all ordinary spokes crosses from right-heavy to left-heavy. The C-step identity forbids such a crossing. The four D-step candidate bounds sum to \(2M-\alpha-\beta\leq4h\), so one works. A long A-run separates its light end sides from its explicitly budgeted fan \(F\); the non-DAD singleton A detours use a side disjoint from the already-heavy side.

For a far DAD crossing, the replacement path additionally deletes \(b_0\). This detaches each anchor-sector attachment individually and subtracts the **aggregate** \(\kappa_0\) from the new left bound. The old heavy-right inequality gives \(L'-\kappa_0<M-h-\gamma_j+\kappa_j-\kappa_0\leq h\). This is the one point requiring the chosen sector to dominate the crossing sector. For inner centers adjacent to \(c_0\), the short outer path deletes every active vertex of the heavy side and individually detaches all its sector attachments; the unsubdivided-inner-edge condition ensures there is no unremoved rim-interior mass. The remaining represented mass is then below \(h\). These cases close the quantitative theorem.

When \(B>W/2\), a centroid bag in the heavy attachment's width-three torso has at most four vertices and the outside mass lies in its designated tree branch. When a long fan has mass above \(W/2\), the displayed width-four path decomposition has five-vertex core bags and glues in width-three attachment decompositions along their clique boundaries. Each local centroid bag is covered by two ambient geodesics: pair a four-vertex guest bag, or use one root spoke plus a geodesic joining the at most two remaining vertices in a core bag. Deleting extra vertices along these ambient paths cannot worsen component masses. If neither heavy case occurs, \(B,F_{\max},M/2\leq W/2\), so the quantitative theorem gives the all-mass corollary. The proof uses the full graph for component accounting even when attachments have zero mass.

## Independent verification and trust boundary

The target regression passed its [expected summary](../planar_two_geodesic_selected_spoke_annuli/expected.json): 83 systems, 2,702 component cuts, 5,003 quantitative checks, 2,585 heavy-attachment checks, and 102 heavy-fan checks. Its separate control audit passed on the 52-vertex, 143-edge unit planar graph.

My standalone [audit.py](audit.py) imports no target implementation. It exhausts every admissible cyclic A/C/D word of length 6 through 10 (including rotations), checking unique cross states, all D missing-diagonal incidences, singleton A detours, DAD local degrees, and the far-center three-edge distance. Separately it constructs the control graph by face insertions, checks the spherical face incidence, core isometry, reverse width-three elimination of all three attachments, and enumerates geodesic vertex sets by forward shortest-path propagation. It computes the residual component mass for **every** second geodesic after the prescribed first spoke and after each maximum-sector spoke. Exact output:

```text
words=84809 D_steps=277386 ordered_DAD_pairs=12198 far_DAD=5286 control_geodesic_sets=3489 fixed_optimum=19 selected_optima=[9, 14] free_largest=14 PASS
```

Reproduce from repository root using Python 3.11 or later, standard library only, with assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_selected_spoke_annuli/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_selected_spoke_annuli/audit.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_selected_spoke_annuli_review1/audit.py
```

Target SHA-256: `README.md` `a0780d83b1ab6921478228a05ebe5f54fae64d300245ff4ff388dbb023c3c655`; `verify.py` `62a1bfc167eb89a4a24f336383cbeb1cae65c9546d1ac18a5491e42f995b0aee`; `audit.py` `b074709f0ec3f060112615293a54183385663f1b54f96c2a346eee471835975e`; `control.json` `41d5361fee6fca4133a08e10e041e98cdf01a199dd16231c2adb6ef2557be451`; `expected.json` `80f5e1d727ab72b3aed6bb84cd830e41d52ae4d7b626ac711129fe8b3115e8d8`. The bounded word enumeration is a structural check, not a proof for unbounded words or all weights. The universal conclusion rests on the written side-inclusion, exchange, and centroid arguments. The fixed-spoke failure is an exact finite certificate because all geodesic vertex sets and all resulting components are enumerated.

## Literature and mathematical potential

The official [Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks for two shortest paths at **one-half** balance; the established two-path statement there only gives **two-thirds** balance. [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) already study other weighted exact-half path-separable classes, so the present class should not be advertised as the first such result. Relative to the preceding [quadrilateral-annulus construction](../planar_two_geodesic_quadrilateral_annuli/README.md), this result removes the DAD exclusion and relaxes the pure-run bounds from \(k-4,m-4\) to \(k-2,m-2\), at the cost of unsubdivided inner edges and a mass-dependent first spoke. I found no exact published formulation in a targeted primary-source search, but that does not establish priority. The [workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html) announces a disproof of an unspecified Codsi conjecture; its relationship to this exact problem remains unverified from the schedule alone.

## Strengthening and improvement opportunities

**Proved local-dominance refinement of the spoke rule.** The proof does not need the anchor DAD sector to maximize \(\kappa\) against sectors at adjacent inner centers: those two exchanges delete the entire heavy side independently of their sector masses. It suffices to choose any first DAD sector whose aggregate \(\kappa_0\) is at least that of every DAD sector with inner center outside \(\{c_0,c_1,c_{m-1}\}\). Every other exchange is unchanged, so the same quantitative and all-mass conclusions hold. Global maximization among DAD sectors is a simple way to meet this weaker condition, not a necessary condition for this proof.

**Remaining structural bridge.** The two near-center repairs use short outer paths to remove all mass on the heavy side. A subdivision of an inner edge inserts vertices that these paths need not meet. Extending the theorem to subdivided rims requires a new bound or a geodesic exchange that absorbs that interior mass; the older subdivision theorem's other hypotheses cannot simply be combined with this result. A useful next test is a single subdivided edge adjacent to the selected sector with controlled interior mass, followed by a proof that the revised bound survives every component cut.
