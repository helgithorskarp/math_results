# The 54-vertex girth-five extremal problem

Let `f(n) = ex(n,{C3,C4})` for finite simple undirected graphs. The retained target is to decide whether a graph of order 54, size 187 and girth at least five exists. The working interval remains **185 ≤ f(54) ≤ 187**.

The [whole-boundary exclusion](boundary_exclusion.md) now proves
**at most twelve degree-eight vertices**. Every case with thirteen is closed.
The new human argument combines local sign and charge inequalities with
individual distant-neighborhood partitions and double covers. It imports
one existing exact rational inequality, and uses no prior SAT forest
exclusions. Run `python3 verify_boundary_exclusion.py` for exact certificate
replay and independent finite controls.

The [new three-incidence exclusion](z12_A3_exclusion.md) proves that at
`z=12`, the total number `A` of distant vertices summed over the twelve
degree-eight vertices is **at most two**. Thus **at least ten high vertices
are sinks**. It closes the entire `A=3` subclass: all individual missed-vertex
frames reduce to a shared endpoint or a six-cycle, and 14 exact rational
certificates refute every remaining attachment profile. The public source
regenerates the certificates outside Git and checks them with integer
arithmetic; see the proof for commands and [compact evidence](a3_expected.json).
The complete `z=12` subclass remains open, with `A=0,1,2` remaining.

The [preceding incidence theorem](z12_distant_incidence_bound.md) supplies
the corrected identities and the earlier bound `A<=3`, excluding every
four- and five-incidence case. Its assumptions and certificates are kept
separate from the new `A=3` computation.

The detailed reductions below preserve the preceding research stages;
their surviving-case statements are superseded by the whole-boundary theorem.

This contribution proves a necessary structural restriction: every such 187-edge graph has degree counts

\[
(n_6,n_7,n_8)=(z+4,50-2z,z),\qquad 0\le z\le12.
\]

A weighted pair-counting identity gives an exact nonnegative gap of `256-19z`; see [proof.md](proof.md). The [boundary refinement](boundary_sinks.md) proves that at `z=13`, **all 13 degree-eight vertices have every vertex within distance two**, and the adjacency characteristic polynomial is divisible by `(X²+X−7)^12`.

The published aggregate certificate has also been [proved unrealizable as a graph](profile_exclusion.md), using a checked SAT refutation. This excludes that exact aggregate assignment; the broader 13-vertex case remained open at that stage.

The [complete seven-edge subclass exclusion](seven_edge_exclusion.md) now proves
that these thirteen vertices span **at most six edges**, so at least one has
no degree-eight neighbor. A human pair-coverage argument reduces the equality
case to 50 complete incidence cases; every case has an independently checked
SAT refutation. The new computation uses no weighted-gap budget and covers
all remaining vertex incidences. It reduces the entire surviving `z=13`
search to a degree-eight root with three degree-six and five degree-seven
neighbors.

The [forest reduction](forest_reduction.md) further restricts the high-induced
graph to **seven explicit forests with five or six edges and at most two
degree-two vertices**. Exact rational certificates first give a ten-forest
cover. Complete incidence refutations then exclude three entire forests,
covering all 22 of their high-neighbor-count profiles. Every remaining
forest at that stage still required a realization decision.

The [two-P3 exclusion](two_p3_exclusion.md) closes the entire remaining
forest `2P3+2P2+3K1`, leaving six forests at that stage. Its six possible high-neighbor
profiles are covered by 13 proof-checked cases. The key reduction forces
the common neighbor and the individual neighbor roles of the two path
centers; the full order-54 existence question remains open.

The [P4 exclusion](p4_exclusion.md) closes the entire forest
`P4+2P2+5K1`, leaving five forests at that stage. Adjacent path centers force twelve
independent low neighbors; a complete center/endpoint role cover gives
52 proof-checked incidence cases across all fifteen high-neighbor
histograms. The surviving forests are `5P2+3K1`, `P3+3P2+4K1`,
`2P3+P2+5K1`, `6P2+K1`, and `P3+4P2+2K1`.

Reproduce that exclusion with `python3 verify_p4.py` and
`python3 reproduce_p4.py --work /tmp/order54-p4 --checker /path/to/drat-trim`.
The [proof](p4_exclusion.md) gives the complete cover, dependencies and
trust boundary; [p4_expected.json](p4_expected.json) records all 52
formula/proof hashes, and [p4_run.json](p4_run.json) records the fresh run.

The [shared-center restriction](shared_center_restriction.md) proves
that, in `H=2P3+P2+5K1`, the two path centers share a degree-six vertex
with exactly two or three high neighbors. A complete joint-neighborhood
cover and 124 checked refutations reduce that whole forest to 33 explicit
center-incidence states across four histograms. That complete cover is the
computer-assisted prerequisite for the closing argument below.
Reproduce with `python3 verify_shared_center.py` and
`python3 reproduce_shared_center.py --work /tmp/order54-shared-center --checker /path/to/drat-trim --jobs 4`.

The [distant-partition exclusion](distant_partition_exclusion.md) now closes
**the entire forest `2P3+P2+5K1`**, leaving **four forests**:
`5P2+3K1`, `P3+3P2+4K1`, `6P2+K1`, and `P3+4P2+2K1`.
For every degree-seven vertex, its distant vertices' high-neighbor sets
partition the high vertices outside its own neighborhood. Combined with
two weighted identities, this excludes three of the inherited profiles
immediately. The fourth requires at least four special seven-vertices,
while their individual partitions allow at most two. The closing proof
allows distant seven–seven pairs and requires no new solver refutations.
Run `python3 verify_distant_partition.py` for the exact controls and small
independent enumerations. The remaining complete histogram cover has 115
cases; no realization or exclusion of the four remaining forests is claimed.

This is a structural lemma, not an improved extremal-number bound or an existence result. The weighting and the specialization were obtained in this campaign; priority is not established. The underlying two-path packing method is standard, notably in Backelin's work cited below.

## Reproduction

Run from this directory with Python 3.11 or later, with no external packages or network:

```sh
python3 verify.py
python3 verify_boundary.py
```

Expected output:

```text
PASS: 72 local types; exact weighted certificate; z <= 13
PASS: Hoffman-Singleton and two edge-deletion controls
PASS: independently checked 54-vertex, 185-edge lower-bound fixture
PASS: integral z=13 aggregate certificate (15 types, 47 nonzero edge counts)
PASS: local weighted identity on four graph controls
PASS: arithmetic in both exceptional-vertex exclusions
PASS: four independent degree-eight sinks; exact polynomial nullity 6
```

The verifier checks the rational-free coefficient certificate on every permitted local type, the gap polynomial, graph identities on explicit controls, a known lower-bound graph, and an integer boundary certificate. The human proof is independent of the optimizer. The checks do not formally verify the human proof and do not enumerate all 54-vertex graphs.

`boundary_profile.json` satisfies the six degree-class pair-capacity inequalities, all type-incidence balances, all type-averaged two-step capacities, and the simple-graph upper capacities between and within types. It is **not a graph**: the data do not assign these incidences to individual vertices or enforce unique common neighbors for individual pairs. It demonstrates that even this strengthened aggregate relaxation does not exclude `z=13`. Its definitions and exact verification are in `verify.py`; no optimizer is needed to check the certificate. It was found using SciPy 1.15.3 / HiGHS, with integer variables, then checked using Python integers.

For the earlier fixed-certificate reproduction, see [profile_exclusion.md](profile_exclusion.md) and `profile_sat.py`.
For the complete new subclass, see [seven_edge_exclusion.md](seven_edge_exclusion.md):

```sh
python3 verify_seven_edge.py
python3 reproduce_seven_edge.py --work /tmp/order54-seven-edge --checker /path/to/drat-trim
```

The latter requires the pinned SAT dependencies and must finish with
`verified_unsat: 50`. It regenerates every CNF and proof outside the repository
and calls the separate checker. The next substantive phase is to decide
realizability with the newly forced isolated high root. No unbounded
computation is running.

For the latest seven-forest reduction:

```sh
python3 verify_forest_reduction.py
python3 reproduce_forest_exclusions.py --work /tmp/order54-forests --checker /path/to/drat-trim
```

The first command uses exact standard-library arithmetic; the second must
finish with `verified_unsat: 22`. The three excluded forests are covered in
full, rather than only for selected incidence totals.

For the complete two-P3 forest exclusion:

```sh
python3 verify_two_p3.py
python3 reproduce_two_p3.py --work /tmp/order54-two-p3 --checker /path/to/drat-trim
```

Expected: `verified_unsat: 13`; all six profiles of this forest are excluded.

## Sources and scope

Checked on 2026-09-10:

* [Afzaly and McKay, extremal graph catalogue](https://users.cecs.anu.edu.au/~bdm/data/extremal.html): supplies the published value `f(53)=181` and 54-vertex, 185-edge examples. From `52e(G)=sum_v e(G-v) <= 54*181`, we obtain the elementary upper bound 187. The original exhaustive proof of `f(53)` is imported, not reproduced. Its listed 2688 extremal graphs are explicitly an incomplete sample; none of our exclusions assumes that sample is complete.
* [Goedgebeur, Jooken, Joret and Van den Eede, 2025, arXiv:2508.05562](https://arxiv.org/abs/2508.05562): confirms exact values through order 53 and reports no improvement at order 54. The live catalogue and this paper delimit the working frontier; a negative literature search is not a priority guarantee.
* [Backelin, 2015, arXiv:1511.08128](https://arxiv.org/abs/1511.08128), especially Lemmas 2.1, 2.6 and 2.8: local degree sums and degree-class two-path packing are established tools. We claim no novelty for these principles.
* [Miller and Codish, arXiv:1708.06576](https://arxiv.org/abs/1708.06576): earlier degree and vertex-deletion restrictions for girth-five extremal graphs.
* [Afzaly, 2016 dissertation](https://openresearch-repository.anu.edu.au/items/2796ea59-fbe9-497b-a4fb-fae86a1750e8), Chapter 3 and Appendix A.2: generation methods and the earlier frontier. Its order-53 table predates the current exact value and must not replace the live catalogue.

`lower_bound_54_185.json` is the edge set of the first graph decoded from [the catalogue's 54-vertex sparse6 file](https://users.cecs.anu.edu.au/~bdm/data/extremal/c34_n54e185.maybe.s6), SHA-256 `c894ed6af84b624f32bf5ce725d7621089d89cc39ccc6884a377da8a0f4ac608`. NetworkX 3.4.2 was used only for the initial decoding; the published verifier checks the explicit edges independently. This fixture is an existing example, not a new construction. Large source catalogues, PDFs, solver states and exploratory logs are omitted.
