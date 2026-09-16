# Proof and verification boundary

## Proposition

The frozen equilateral-`sqrt(2)` first lens-orbit closure has 33 distinct
points, 78 edges in its complete strict unit-distance graph, chromatic number
three, and the neutral unrestricted four-colour relation on its three marked
centres.

## Exact realization and completeness

Work in the four-dimensional rational coordinate representation

```text
(a,b,c,d) = (a*sqrt(2)+b*sqrt(6))
            + i*(c*sqrt(2)+d*sqrt(6)).
```

The three displayed centres have pairwise squared distance two. For every
pair, the two formula points `(p+q)/2 +- i*(q-p)/2` are checked to be unit
distant from both owners. Each owner-relative direction is repeatedly acted
on by the exact 60-degree rotation

```text
(a,b,c,d) -> ((a-3*d)/2, (b-c)/2, (3*b+c)/2, (a+d)/2).
```

The checker verifies that each orbit returns after six steps. It then merges
equal four-tuples, obtaining 33 points from the 75 declarations.

For every unordered pair of merged points, the checker expands its squared
distance in the basis `{1,sqrt(3)}`. Equality to one is equivalent to exact
coefficient equality `(1,0)`, so the resulting list of 78 edges is the
complete strict physical unit graph, not a selected source-edge graph.

## Exact chromatic number

For every generated point, four times the imaginary `sqrt(2)` coefficient is
an integer. Direct substitution into the complete edge list verifies that its
residue modulo three differs at the endpoints of every edge. This gives a
proper three-colouring. The certificate supplies three point indices, and the
checker verifies all three corresponding pairs are edges. Hence the graph
contains a triangle and its chromatic number is exactly three.

## Neutral centre relation

The three centres are pairwise at squared distance two and therefore have no
edges between them. Up to a global permutation of four colours, every colour
assignment to three labelled independent vertices has one of the equality
patterns

```text
000, 001, 010, 011, 012.
```

The certificate contains one literal proper four-colour word for each pattern.
The checker validates every complete-graph edge and all three prescribed
centre colours. Therefore every bare-centre pattern extends, proving that the
complete unrestricted centre relation is neutral.

## Trust boundary

The mathematical claims above depend only on Python's exact `Fraction`
arithmetic, the displayed generation rules, exhaustive pair reconstruction,
and literal positive witnesses. No floating-point predicate, SAT-solver
soundness, omitted edge list, external data file, or background process is a
proof premise. This is author-side reproducible evidence, not an independent
review or proof-assistant formalization.

