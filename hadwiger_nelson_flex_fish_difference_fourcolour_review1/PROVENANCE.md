# Provenance and source integrity

## Reviewed target

- Mathematical target commit:
  `a0630a216e1b10f00ccb342fe1d76a1eb94fc173`.
- Target certificate SHA-256:
  `15c578fd0830897d39699972acf992648a18b6896957fd00490c3e9810e12ac1`.
- Source geometry certificate SHA-256:
  `e079c2d86f0b3574e6e24d9fc18a9abc2d8b7d7fe111ba011d5978875d5fc732`.

The review pins immutable bytes rather than accepting a moving branch tip.

## Imported source review

The exact 23-point source realization and complete 43-edge contact graph were
independently accepted in
[`hadwiger_nelson_fish_flex_contact_review1`](../hadwiger_nelson_fish_flex_contact_review1/README.md)
at mathematical review commit
`0eae3bf461ed663a48d898cf167aa48f4117847c`.  That review reconstructed the
fish edges from Parcly Taxel's pinned Shibuya implementation, checked the
retrieved source hash, used an independent interval-Jacobian contraction
argument, classified all 253 point pairs, and independently checked
chromaticity.  The present review reruns that checker and pins the same
geometry certificate.

The original 23-vertex fish graph is attributed to R. Hochberg and P.
O'Donnell, *Some 4-Chromatic Unit-Distance Graphs without Small Cycles*,
Geombinatorics 5 (1996), 137--141.  No novelty is claimed for that graph,
its flexibility, or difference sets in general.

## Record boundary

The bounded live literature check on 2026-09-15 still supports Jaan Parts's
509-point, 2,442-edge plane unit-distance construction as the smallest
published five-chromatic example.  Haugland's August 2026 paper independently
describes it as the smallest while studying the distinct Moser-spindle-free
frontier.  A recent 509-vertex, 2,259-edge certificate concerns the edge-count
record on the same order and does not lower the vertex record.

- Parts, [*Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*](https://arxiv.org/abs/2010.12665).
- Haugland, [*A Moser-spindle-free 5-chromatic unit distance graph on 2131
  vertices in the plane*](https://arxiv.org/abs/2608.04542).
- Amer, [509-vertex edge-reduction data](https://github.com/md-amer/hadwiger-nelson-e5).
