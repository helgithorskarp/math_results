# A five-chromatic dominating triple has diameter strictly below three

**Theorem.** Let `a0,a1,b` be three distinct points of the Euclidean plane
with `|a0-a1|>=3`.  The strict unit-distance graph on

```text
{a0,a1,b} union C(a0,1) union C(a1,1) union C(b,1)
```

is four-colourable.  The upper bound four is sharp, including at equality.

Consequently, every dominating triple in a non-four-colourable plane
unit-distance graph has diameter **strictly less than three**.  Together with
the independently accepted
[unit-edge theorem](../hadwiger_nelson_unit_edge_dominating_triples_review1/README.md),
every dominating triple in a five-chromatic plane unit-distance graph is an
independent set of diameter less than three.

This closes the equality boundary left by the independently accepted
[separated-triple theorem](../hadwiger_nelson_separated_dominating_triples_review1/README.md).
At centre separation three, the two leaf circles have exactly one cross
unit edge.  Their full strict unit graph is nevertheless bipartite: it is a
disjoint union of six-cycles except for that one bridge.  A three-case
assignment of the at most four multiple-owner points to two disjoint palettes
then colours the complete continuum support.  [PROOF.md](PROOF.md) gives the
full construction, including unit-separated centre pairs and all circle
intersections.

The 2,671-byte [certificate](certificate.json) records the exact 12-vertex
boundary graph, all 12 unit-anchor cases, 84 one-exception cases, 36
two-exception cases, the six orbit chords, and a sharp Moser-spindle witness.
[build.py](build.py) regenerates it.  [verify.py](verify.py) independently
uses exact `Fraction` arithmetic over `Q(sqrt(3))` and
`Q(sqrt(3),sqrt(11))`, checks 4,096 boundary binary assignments and all 2,187
labelled spindle three-colourings, and rejects five corrupted certificates.
No floating-point predicate, solver, CAS, or external input is used.

This is a global structural theorem about actual plane realizations, not a
finite sample, an abstract chromatic graph, a Parts/A5 fixed-host exclusion,
a vertex lower bound, or a smaller five-chromatic construction.  Parts's
[509-vertex graph](https://arxiv.org/abs/2010.12665) remains the published
record, as also stated in Haugland's August 2026 introduction
([arXiv:2608.04542](https://arxiv.org/abs/2608.04542)).  No literature-priority
claim is made.

See [REPRODUCE.md](REPRODUCE.md) for exact commands and trust boundaries.
