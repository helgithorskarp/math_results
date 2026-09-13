# The triple-phase collar for independent dominating triples

Put

```text
d0 = 1 + sqrt(3) = 2.732... .
```

**Two-circle theorem.**  If two unit circles have centre separation
`d>d0`, their full strict unit-distance graph is bipartite.

**Three-centre corollary.**  Let three plane centres have all three mutual
distances greater than two.  If their diameter is greater than `d0`, the
full strict unit-distance graph on the centres and their three complete unit
circles is four-colourable.  Consequently, a non-four-colourable plane
unit-distance graph dominated by such a triple has dominating-triple diameter
at most `1+sqrt(3)`.

This strictly strengthens the independently accepted
[open-collar theorem](../hadwiger_nelson_open_dominating_triple_collar_review1/README.md),
whose threshold was `(sqrt(3)+sqrt(15))/2 = 2.802...`.  It still covers a
positive-dimensional region with every centre distance below three.  For
example, an open neighbourhood of the equilateral side-`11/4` fixture is in
the new region.

The proof classifies the complete continuum of cross-circle edges.  Write a
point of the first circle as `u` and a point of the second as `d-w`, with
`|u|=|w|=1`.  They are a unit pair exactly when

```text
u+w+t=d
```

for a third unit complex number `t`.  The product `p=uwt` labels the resulting
unordered triple: its members are precisely the roots of

```text
z^3-d*z^2+d*p*z-p.
```

After contracting these cross components, a 60-degree same-circle step joins
two triple labels.  On the only angular interval where both endpoints are
cross-active, the argument of `p` is strictly increasing at both ends.  Thus
the label graph is an order-preserving partial matching of real intervals.
It has maximum degree two and cannot contain a nontrivial cycle.  A loop would
be a triple containing two directions 60 degrees apart; that is possible
exactly through `d=1+sqrt(3)`, and is impossible above it.  The label graph is
therefore a forest, and its bipartition extends orbit-by-orbit to both full
circles.  [PROOF.md](PROOF.md) includes the repeated-root, inactive-orbit, and
edge-exhaustion details.

The strict threshold is sharp for the two-circle conclusion.  At
`d=1+sqrt(3)`, the two first-circle points

```text
sqrt(3)/2 +/- i/2
```

together with the second-circle point `sqrt(3)` form a realized unit
triangle, so that two-circle support is not bipartite.  This sharpness does
not claim that the complete three-centre support needs five colours there.

The compact exact certificate records the threshold, the derivative-sign
factorization, the equilateral interior fixture, a nondegenerate cross-triple
fixture, the sharp boundary triangle, the six orbit chords, and the four-colour
palette.  [build.py](build.py) regenerates it; [verify.py](verify.py) checks it
independently in `Q(sqrt(3),sqrt(5))`; [controls.py](controls.py) rejects eight
semantic corruptions.  The universal continuum and order argument remain the
written-proof trust boundary.

This is a global realized-geometry exclusion under its stated domination and
distance conditions.  It is not a Parts/A5 fixed-host result, an abstract
phase obstruction, a finite-angle sample, a vertex lower bound, or a smaller
five-chromatic construction.  Parts' [509-vertex graph](https://arxiv.org/abs/2010.12665)
remains the published record; Haugland's
[2,131-vertex graph](https://arxiv.org/abs/2608.04542) has the different
Moser-spindle-free restriction and is explicitly not record-small.  No
literature-priority claim is made.  Independent review of this theorem is
pending.

See [REPRODUCE.md](REPRODUCE.md) for exact commands and trust boundaries.
