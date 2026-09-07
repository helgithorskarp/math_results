# All subgraphs through 573 in the native T721 spindle are four-colourable

**Exact computer-assisted theorem.** Let `G` be the strict unit-distance graph on the 1,441 points constructed below from Heule's native `T721.vtx`. Every vertex subset with at most **573** vertices, and every edge subgraph on that subset, is four-colourable. The host is also Moser-spindle-free.

This closes the entire at-most-508 extraction space in this fixed host. It is a negative support theorem, not a record improvement. The bound 574 is a lower bound for the order of a non-four-colourable subgraph, not an assertion that such a subgraph of order 574 exists. No imported non-four-colourability claim about the full host is needed in this proof.

## Fixed source and geometry

The primary input is `vtx/T721.vtx` in [Marijn Heule's CNP-SAT archive](https://github.com/marijnheule/CNP-SAT). [input.json](input.json) pins the upstream commit, download URL and exact 40,529-byte SHA-256 identity. Native half labels are zero-based input line numbers. In particular labels 0 and 1 are `a=(-1,0)` and `b=(1,0)`; label 2 is the origin. The journal's [author index](https://geombina.uccs.edu/author-index/marijn-heule) lists Heule's related *Odd-Distance Virtual Edges in Unit-Distance Graphs*, Geombinatorics 31(2), 2021, beginning on page 68. The present theorem is defined by the pinned native file and the following formula, without requiring an identification with another distributed drawing.

Write `T` for these 721 points and, in complex notation, set

\[
r=(7+i\sqrt{15})/8,\qquad
V(G)=T\cup\{-1+r(z+1):z\in T\}.
\]

Here `|r|=1`. The two copies intersect only at `a`, and the only edge between their disjoint interiors joins `b` to its image `b'`. Exact reconstruction gives 3,948 half edges and 7,897 full edges. All **1,037,520** unordered full point pairs are checked; extra contacts are included automatically.

Coordinates have denominator 96 in the ordered squarefree-radical basis

```
(1, 2, 3, 6, 5, 10, 15, 30).
```

An integer tuple gives eight x coefficients followed by eight y coefficients, divided by 96; each basis entry denotes its positive square root. Lexicographic tuple order labels the full host. The shared anchor is label 25 and the unique cross edge is `[1391,1428]`. Rotations of the half through multiples of 60 degrees preserve its exact point and edge sets.

[native.py](native.py) uses a restricted Python AST, dense coefficient vectors and conjugate products for division. The separate [exact.py](exact.py) uses a recursive-descent parser, sparse radicand dictionaries with gcd multiplication, and rational Gaussian elimination for division in the native field. Both reconstruct identical full points, edges and half maps. The independent census uses a checked ring projection modulo 1009 only to reject impossible edges; every survivor receives a complete exact norm check. Modular equality never accepts an edge.

## From positive colourings to mandatory vertices

A proper four-colouring of `T` is provided. For 236 nonterminal labels `v`, another word properly colours `T-v` with `a` and `b` different. These words are encoded by 12 explicit seeds, 196 exact rotation steps and 28 patches. A patch merely specifies changed entries relative to an earlier word; its search history has no proof status. Every decoded word is independently checked for its precise omitted vertex, legal colours, terminal separation and all induced edges.

Take these 236 labels together with `a,b`, and let `M` be the union of their two images in the full host. Thus

\[
|M|=2(236+2)-1=475.
\]

For a nonterminal deletion in either half, combine its separating colouring with the other half's baseline colouring. A permutation of four colours matches the shared anchor and separates the bridge endpoints. Deleting the anchor or a bridge endpoint is handled directly by permuting the two baseline palettes. [cover.py](cover.py) actually constructs **all 475 full-host deletion colourings** and checks every remaining edge, rather than relying solely on this palette argument.

Consequently every non-four-colourable subgraph of `G` contains `M`: a subgraph omitting `v in M` inherits a four-colouring from `G-v`. This alone gives a bound through 474. The next integer certificate supplies the additional 99 required vertices.

## The weighted minimum-degree certificate

Let `S` be the vertex set of a vertex-minimal non-four-colourable subgraph of `G`. It contains `M`, and every selected vertex has at least four neighbours within `S`; otherwise a four-colouring after deleting that vertex would extend greedily.

[weights.json](weights.json), only 856 bytes, assigns weight 1 to 61 vertices of `M` and weight 2 to another 28. All other weights are zero. Thus the total weight is 117. For each host vertex `u`, write

\[
t_u=\sum_{v\sim u}w_v.
\]

Direct integer checks establish

\[
\sum_{u\in M}t_u=269,
\qquad t_u\le2\quad(u\notin M,\ u\ne217),
\qquad t_{217}=3.
\]

Double-counting weighted incidences therefore gives

\[
468=4\cdot117
\le\sum_v w_v\,|N(v)\cap S|
=\sum_{u\in S}t_u
\le269+2(|S|-475)+1.
\]

It follows that `|S|>=574`. Any non-four-colourable graph on at most 573 vertices would contain a vertex-minimal one on at most that many vertices, a contradiction. This proves the stated complete subset theorem, including arbitrary edge deletions.

An LP suggested the weights. The proof checks only the displayed integer inequalities; neither floating-point optimization nor an optimality assertion is trusted. [discover_weights.py](discover_weights.py) optionally regenerates the weights and checks their integer consequence. No integrality assumption about an LP solution is part of the theorem.

## Moser-spindle absence

All real coordinate components belong to `K=Q(sqrt(2),sqrt(3),sqrt(5))`, which does not contain `sqrt(11)`: its seven quadratic subfields correspond to squareclasses 2, 3, 5, 6, 10, 15 and 30.

In an injective unit-edge drawing of a Moser spindle, each of its two diamonds has missing-edge tips at distance `sqrt(3)`. The two tip vectors from the common apex have squared lengths 3 and mutual distance 1, so their dot product is `5/2` and the square of their determinant is `11/4`. Coordinates in `K` would then force `sqrt(11)` into `K`, a contradiction. This is the usual elementary field obstruction, not a claimed new general theorem.

As a separate graph check, the verifier enumerates all 1,392 unit diamonds and finds no edge between two diamond tips sharing an apex. It therefore also excludes a Moser spindle directly from the reconstructed edge set.

## Reproduction and evidence

From the repository root, with Python 3.11 or newer:

```sh
python3 -B hadwiger_nelson_t721_weighted_cover/fetch_input.py /tmp/hn-t721/T721.vtx
python3 -B hadwiger_nelson_t721_weighted_cover/verify.py --input /tmp/hn-t721/T721.vtx --check-expected
python3 -B hadwiger_nelson_t721_weighted_cover/produce.py --input /tmp/hn-t721/T721.vtx
python3 -B hadwiger_nelson_t721_weighted_cover/controls.py --input /tmp/hn-t721/T721.vtx
```

The verification and certificate reproduction use only Python's standard library. The checker reports `verified: true`, `arbitrary_target_subsets_classified: true`, `minimum_critical_order: 574`, and `four_colourable_through: 573`. [expected.json](expected.json) contains the full exact report and mandatory labels. Verification took about 4.2 seconds on the research host.

The certificate regenerates byte for byte from [seeds.json](seeds.json), with the original deterministic batch order and one stored word per omitted vertex. Seed-free batches preserve that recorded order. SAT is unnecessary for reproduction. Optional LP regeneration uses `numpy==2.4.6` and `scipy==1.17.1`:

```sh
OPENBLAS_NUM_THREADS=1 python3 -B hadwiger_nelson_t721_weighted_cover/discover_weights.py --input /tmp/hn-t721/T721.vtx --output /tmp/hn-t721/weights.json
```

Normal and optimized Python verification and controls agree. Controls compare both exact geometries, 90 rational expressions, 7,646 feasible graph/subset/degree cases over all 1,099 simple graphs of orders 1 through 5, and reject 43 deliberate input, certificate, weight or geometry faults. The optional LP replay regenerated the identical 856-byte certificate. [validation.json](validation.json) records compact results.

| Evidence | Result |
|---|---:|
| Half-deletion words / full deletion words | 236 / 475 |
| Checked half-edge inequalities, including baseline | 933,264 |
| Checked full deletion-edge inequalities | 3,746,101 |
| Weighted mandatory vertices | 89 |
| Required additional vertices | 99 |
| Colouring certificate bytes | 33,819 |
| Integer weight certificate bytes | 856 |

The colouring certificate SHA-256 is `78465aea5e7c976bbd53ceb0a2a6be1c45ee42510841bd64cb836a3fc3a53883`.
The weight certificate SHA-256 is `ce0e2090b494ff7cc4756d116e4a4f0b9d1bb6c219ced0685fe36e313c017a7f`.
The canonical full deletion-word stream SHA-256 is `0ca2f9d13ede3573e1c1fbb944d13ee11af9b00f3d7f91ad07d34a7f4d2a063a`.

Discovery used PySAT 1.9.dev15, CaDiCaL 1.9.5 and Glucose 4. The finite primary universe had 360 inversion-orbit representatives, each eligible for at most one query with a requested 200,000-conflict limit. The completed queries gave 21 SAT words and 56 UNKNOWN answers; two interrupted labels were consumed without retry. All 21 positive words were independently checked. The largest reported count was 201,212 because a solver may check its requested budget between internal batches. UNKNOWN answers provide no evidence. Serial search was changed to disjoint four-process batches, then to fresh induced-graph encodings, with all finished results retained. The full search history and source snapshots are private operational evidence; the published positive certificates fully reproduce the mathematical result.

Queries stopped once the weighted bound closed the target. Thirty-four labels had already been skipped because their deletion was certified, and 247 remained unqueried. Their status has no bearing on the complete theorem. The frozen proof uses 12 seed words; remaining completed words are unnecessary to its check. No search job or unresolved proof remains running.

## Scope and campaign context

The terminal-colouring mechanism builds on the earlier [de Grey 1581 fixed-host exclusion](../hadwiger_nelson_degrey1581_terminal_cover/README.md). The new support is the exact native T721 spindle; the additional weighted degree argument is needed because its 475-vertex mandatory set alone does not reach the target. The earlier Heule catalogue block union, Parts compression, H632 pilot and Haugland locality families are not extended.

The teammate's separate [critical-shift transfer obstruction](../hadwiger_nelson_critical_shift_transfer/README.md), committed during this pass, was inspected before publication. It is context, not a premise of this theorem. The present artifact has not yet received an external review.

The trust boundary is the explicit input identification, exact radical arithmetic, the readable colouring and integer-incidence checkers, the elementary minimum-degree argument, and ordinary Python execution integrity. This is an exact computer-assisted theorem, not a proof-assistant formalization. The fixed T721 spindle extraction support is now retired through the record target; this result does not authorize a larger-threshold or deletion-query ladder. The general at-most-508 five-chromatic unit-distance target remains open.
