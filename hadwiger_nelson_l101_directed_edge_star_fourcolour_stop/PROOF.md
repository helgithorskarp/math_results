# Proof outline

Let `K=Q(a,b)` with `a^2=3`, `b^2=11`, and basis
`1,a,b,ab`. `exact_model.py` implements multiplication in this basis, so all
claims below reduce to rational coefficient equality.

1. Substitute the ten coordinate formulas from `README.md`. Complete testing
   of their 45 pairs gives 19 unit pairs: all 17 edges displayed for
   `L_{10,1}`, plus `BF` and `DH`.
2. On `ABFGHIJ`, the eleven unit edges are
   `AB,AF,AG,BF,BG,FI,FJ,HI,HJ,IJ,GH`. These are two diamonds sharing no
   vertex, with their opposite tips joined: the Moser spindle. Therefore the
   strict source and every closure containing it need at least four colours.
3. For each of the 19 unordered physical source edges, use both directions in
   `z -> u+(v-u)z`. Each map is a direct isometry because `|v-u|=1`.
   Collision merging of the 38 images gives 188 distinct points.
4. Complete exact testing of all `188 choose 2 = 17,578` pairs gives precisely
   765 unit pairs. The certificate's four-word differs on every one, so the
   whole graph needs at most four colours.
5. Steps 2 and 4 give chromatic number exactly four. The same reconstructed
   graph has no articulation or bridge and its degree-four core has 184
   vertices, but these structural facts are not used for the chromatic proof.

The strict completion's embedded Moser spindle is also why this exact support
cannot qualify as the source-new construction requested at intake.
