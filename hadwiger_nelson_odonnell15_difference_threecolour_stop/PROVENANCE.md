# Provenance and trust boundary

The 15-vertex source is the core of Paul O'Donnell's 40-vertex triangle-free
four-chromatic unit-distance construction:

- Paul O'Donnell, *A 40 Vertex 4-Chromatic Triangle-Free Unit Distance Graph*,
  Geombinatorics 5(1), 30--34 (1995).
- Wolfram MathWorld, *O'Donnell Graphs*, including the exact
  `ODonnellGraph40Core` coordinate serialization:
  <https://mathworld.wolfram.com/ODonnellGraphs.html>.

The theorem in this package does not trust a picture, a decimal edge list, or
the source's attributed chromatic properties.  The 15 exact coordinate rows
are part of the certificate; the verifier reconstructs their complete
25-edge unit graph and then rebuilds the whole difference body.

During intake an incorrect three-ring transcription reconstructed only five
source unit edges and was rejected before the chromatic query on the actual
source.  The corrected 25-edge source, operation and cap equation were then
kept fixed.  No second source, orientation or operation was tested.

The proof relies on exact rational arithmetic plus rational interval
evaluation at one isolated algebraic root.  The colour words are positive
witnesses and require no SAT solver.  No abstract graph embedding, projected
relation or floating tolerance graph is used.

