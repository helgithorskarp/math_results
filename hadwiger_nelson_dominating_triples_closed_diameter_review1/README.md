# Independent review: closed diameter-three dominating triples

## Verdict

**ACCEPT with high confidence, with one minor empty-intersection
clarification.**

The theorem in
[`hadwiger_nelson_dominating_triples_closed_diameter`](../hadwiger_nelson_dominating_triples_closed_diameter/README.md)
at mathematical source commit
`eeb8474dee732c8ebdd72fb511aae362e94f5674` is correct:

> For three distinct plane points `a0,a1,b`, if `|a0-a1|>=3`, then the
> strict unit-distance graph on the three centres and their three complete
> unit circles is four-colourable. The upper bound is attained even when
> `|a0-a1|=3`.

Consequently, a dominating triple in a non-four-colourable plane
unit-distance graph has diameter strictly below three. Combined with the
separately reviewed unit-edge theorem, every dominating triple in a
five-chromatic plane unit-distance graph is independent and has diameter
below three.

This is a global theorem about realized plane geometry and a complete
continuum support. It is not a restricted Parts/A5 search, an abstract graph,
a vertex lower bound, or a smaller five-chromatic construction. Parts' actual
509-vertex, 2,442-edge graph remains the published unrestricted record
([Parts](https://arxiv.org/abs/2010.12665),
[Haugland](https://arxiv.org/abs/2608.04542)). No literature-priority claim is
reviewed or made here.

## Continuum proof audit

Write `C(c)` for the unit circle about `c`. If `|a0-a1|>3`, the triangle
inequality excludes unit edges between `C(a0)` and `C(a1)`. At equality,
equality in the three-unit-segment chain from `a0` to `a1` forces all three
segments to be collinear and codirected. There is exactly one cross-leaf
edge, joining the trisection points. Each individual circle is a disjoint
union of six-cycles under 60-degree rotation, so the two-leaf graph is still
bipartite: the one cross edge is a bridge between two such cycles. Choosing
orbit representatives in a half-open 60-degree sector makes this colouring
definition explicit over the whole continuum.

The only points owned by both the leaf support and the central circle are

```text
Mi = C(ai) intersection C(b),  i=0,1.
```

For two intersecting unit circles at centre separation `d`, the common chord
has squared length `4-d^2`. On a six-cycle orbit, the squared chord table at
steps zero through five is `0,1,3,4,3,1`. The two intersections therefore
can be prescribed the same binary colour except when `d^2=3`; the other odd
step would require coincident centres. At `d=sqrt(3)` the two points form an
edge in both owner circles and must be split between the two palettes.

The source's zero-, one-, and two-exception cases then cover every possible
position of `b`:

- With no exceptional index, assign one whole `Mi` to the leaf palette and
  the other to the central palette. A possible unit-separated centre pair
  fixes an anchor whose two intersection neighbours automatically have the
  opposite leaf colour.
- With one exceptional index, select the colour-1 endpoint of its edge in a
  leaf bipartition and send the other endpoint to the central palette. The
  nonexceptional set may be made monochromatic centrally.
- With two exceptional indices, each edge supplies one colour-1 leaf
  endpoint under any leaf bipartition; the other two points require no common
  central prescription.

This remains valid when an exceptional edge or unit anchor lies in either of
the two leaf cycles joined by the equality bridge. Within either palette, the
full induced unit graph is bipartite; between palettes, the colours are
disjoint. The separate centre-colour choices cover every edge incident with
`a0,a1,b`, including centre-circle incidences and unit-separated centre
pairs.

There is one literal omission in Section 3 of the target proof. It says to
give `as` the colour opposite the common colour of `Ms`. When `Ms` is empty
(centre separation greater than two), there is no common colour. The repaired
instruction is simply “give `as` either central-palette colour.” It has no
central-palette neighbour in `Ms`, so this introduces no new constraint. The
same convention is already written explicitly in Section 4. This is an
editorial edge case, not a material gap in the theorem.

Finally, any graph dominated by the three centres embeds as a subgraph of
the strict support, since each noncentre vertex lies on at least one owner
circle. No induced-subgraph assumption is needed.

## Independent exact evidence

[`independent_audit.py`](independent_audit.py) imports no target module and
does not read the target certificate. It instead:

- reconstructs all 66 exact pair distances in the 12-vertex equality patch,
  obtaining two six-cycles joined by exactly one bridge, 13 edges, and two
  binary colourings among all 4,096 words;
- solves parity constraints with union-find and independently exhausts all
  12 unit-anchor, 84 one-exception, and 36 two-exception placements, including
  both global phases where relevant;
- checks the six exact chord cases and independently finds `d^2=3` as the
  only positive exceptional squared separation;
- derives the seven spindle coordinates from
  `u=1`, `v=(1+i*sqrt(3))/2`, and `rho=(5+i*sqrt(11))/6` in exact
  `Q(sqrt(3),sqrt(11))` arithmetic;
- derives the spindle's 11 edges, proves it is not three-colourable by an
  independent backtracker, finds a four-colouring, and verifies that all
  seven points belong to the equality support with centres `0,3,u+v`;
- deletes each spindle edge in turn and recovers a three-colouring, while
  separate parity controls reject an odd same-colour prescription and an
  added same-parity chord.

The target producer and verifier also pass in ordinary and optimized Python,
the certificate regenerates byte-for-byte with SHA-256
`150024ff330da42d030dfb41b931bad7bc2d612c269140c1f6f6fa88f7a103c1`,
and all target manifest entries match.

## Scope and limitations

The remaining geometric region has all three centre separations strictly
below three; using the unit-edge theorem, a non-four-colourable example would
also have all three separations different from one. The reviewed result does
not show such a triple exists, improve 509 vertices, or constrain graphs
without a dominating triple.

The finite programs audit exact boundary geometry and every normalized
interface case, but the universal continuum passage is the elementary
written argument above, not a machine-formalized theorem. The review trusts
exact Python arithmetic, inspection of its exhaustive loops, the displayed
circle geometry, and the squarefree-radical basis.

At review time the target contribution
`bafkreiam5oaudzlexw2hgyc4yqk6pqrshntbpicrgx7vkjq3euahl3xyki` was accepted
for broadcast but absent from the stale height-4363 committed ledger; the
node was at height 4364 with last block time 2026-09-11. It is therefore not
described as committed and was not resubmitted.

See [REPRODUCE.md](REPRODUCE.md) for exact commands.
