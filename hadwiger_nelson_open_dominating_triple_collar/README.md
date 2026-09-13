# An open four-colourable collar for dominating triples

Define

```text
delta=(sqrt(3)+sqrt(15))/2 = 2.802... .
```

**Theorem.** Let three plane centres have all three mutual distances greater
than two.  If their diameter is greater than `delta`, the full strict
unit-distance graph on the centres and their three complete unit circles is
four-colourable.

Consequently, any non-four-colourable plane unit-distance graph dominated by
three vertices at pairwise distances greater than two has dominating-triple
diameter at most `delta`.

This enters the open region requested after the independently accepted
[closed diameter-three theorem](../hadwiger_nelson_dominating_triples_closed_diameter_review1/README.md).
It excludes, in particular, the nonempty open set in side-length space where
all three distances lie in `(2,3)` and the largest exceeds `delta`.  The exact
equilateral fixture of side `2*sqrt(2)` is an interior point.  Thus this is
not another isolated equality boundary.

The mechanism is geometric.  On either of two unit circles separated by
more than `delta`, every point having a unit neighbour on the other circle
lies in a cap of Euclidean diameter below one.  Each 60-degree six-cycle
orbit therefore contains at most one such cross-active point.  Orient the
binary phase of every active orbit so that active points on opposite circles
receive opposite colours.  This bipartitions the two complete leaf circles,
including every cross edge.  Since all three owner circles are disjoint, a
second binary palette colours the third circle and the centres use colours
outside their own circle palettes.  [PROOF.md](PROOF.md) gives the full
continuum argument and edge audit.

The 2,738-byte [certificate](certificate.json) records the exact threshold,
six orbit chords, the interior fixture, its strict inequalities, a cap
fixture, and the palette assignment.  [build.py](build.py) regenerates it;
[verify.py](verify.py) independently checks it using `Fraction` arithmetic in
`Q(sqrt(2),sqrt(3),sqrt(5))`; [controls.py](controls.py) rejects six semantic
corruptions.  The computation audits the exact algebra and explicit
realization.  The universal continuum theorem is the written proof trust
boundary.

This is a global realized-geometry exclusion under stated distance
conditions.  It is not a Parts/A5 fixed-host result, an abstract phase graph,
a finite-angle sample, a vertex lower bound, or a smaller five-chromatic
construction.  Parts' [509-vertex graph](https://arxiv.org/abs/2010.12665)
remains the published record; Haugland's
[2,131-vertex graph](https://arxiv.org/abs/2608.04542) has the different
Moser-spindle-free restriction and is explicitly not record-small.  No
literature-priority claim is made.  Independent review of this new collar
theorem is pending.

See [REPRODUCE.md](REPRODUCE.md) for exact commands and trust boundaries.
