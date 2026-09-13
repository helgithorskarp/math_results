# A five-chromatic dominated triple has diameter at most three

**Theorem.** Let `a0,a1,b` be three distinct points of the Euclidean plane
with `|a0-a1|>3`.  The strict unit-distance graph on

```text
{a0,a1,b} union C(a0,1) union C(a1,1) union C(b,1)
```

is four-colourable.  The upper bound is sharp.

Consequently, if a plane unit-distance graph has a dominating set of three
vertices and is not four-colourable, every two vertices of that dominating
set are at distance at most three.  Combined with the independently reviewed
[unit-edge dominating-triple theorem](../hadwiger_nelson_unit_edge_dominating_triples_review1/README.md),
every dominating triple in a five-chromatic plane unit-distance graph is an
**independent set of diameter at most three**.

This is a continuum theorem for arbitrary positions of the third centre and
all points on all three circles.  It is not a finite sampling statement, an
abstract graph without a realization, or a result restricted to Parts-509 or
the A5 radix family.  It gives a global structural exclusion, not a smaller
five-chromatic construction or a vertex lower bound.

The proof uses two disjoint two-colour palettes.  The circles about `a0,a1`
receive one palette and the circle about `b` the other.  The separation
`|a0-a1|>3` eliminates every unit edge between the first two circles.  A point
where a leaf circle meets the central circle may be assigned to either
palette.  The only obstruction to making both intersections use the leaf
palette is the exact centre separation `sqrt(3)`.  At that value the two
intersections form a unit edge, so one is assigned to each palette.  If both
leaf-central pairs are exceptional, their chosen central points can always
be given the required opposite parities on the central six-cycle orbit.
[PROOF.md](PROOF.md) gives the complete argument, including the cases in which
two centres themselves are unit-separated.

The 1,032-byte [certificate](certificate.json) records all six orbit chords,
all eleven same-orbit two-anchor boundary cases, and an exact sharpness
witness.  [build.py](build.py) regenerates it; [verify.py](verify.py) derives
the circle parity facts independently over `Q(sqrt(3))`, checks complete
boundary coverage, and reconstructs the Moser spindle over
`Q(sqrt(3),sqrt(11))`.  No numerical predicate or solver verdict is used.

The published five-chromatic record remains Jaan Parts's 509-vertex graph
([arXiv:2010.12665](https://arxiv.org/abs/2010.12665)); Haugland's August 2026
paper explicitly describes its 2,131-vertex spindle-free construction as not
record-small ([arXiv:2608.04542](https://arxiv.org/abs/2608.04542)).  No
literature-priority claim is made for the present formulation.

Reproduction commands and trust boundaries are in [REPRODUCE.md](REPRODUCE.md).
