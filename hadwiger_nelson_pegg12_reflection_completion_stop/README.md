# Pegg UD12-2 reflection forcing and its finite completion stop

This package gives one exact positive local forcing event and closes its
predeclared finite completion.  It does **not** produce a five-chromatic graph
or improve the 509-vertex record.

Let `P` be the exact symmetric realization of the 12-vertex, 21-edge
four-chromatic unit-distance graph catalogued as `{UnitDistance,{12,2}}` by
Ed Pegg and implemented in Shibuya.  Reflect `P` in the line through vertices
`0` and `6`, collision-merge the two fixed vertices, and reconstruct every
unit pair.  The result has **22 points and 50 edges**.  Eight edges are genuine
new contacts rather than edges inherited from either source copy, and the
complete graph has vertex connectivity three.

The interaction has strict complete-input force.  Up to colour permutation,
`P` has 756 proper four-colourings.  Exactly **136 fail to extend** to the
22-point graph and 620 extend.  In particular, the checked complete source
word

```text
011022011203
```

has no extension, while `012021021301` extends.  The verifier proves the
non-extension by exhaustive deterministic backtracking on the complete exact
graph; it is not inferred from a projected terminal relation.  If all eight
private contacts are deleted, the blocked input extends literally as
`0110220112032101212302`.  Three private edges are individually critical for
this fixed input in the complete graph.  Thus the loss is genuinely caused by
new physical contacts rather than by source overlap alone.

## Declared completion and stop

The bounded continuation was fixed as the union of the 18 source-pair-axis
reflections listed in `certificate.json` that arose in the finite selector
with genuine private contacts and the same strict input loss.  Collision
merging and all-pairs reconstruction give **165 distinct points and 597 unit
edges**, far inside the 508-point cap.  The committed 165-character word is a
literal proper four-colouring of this complete graph.  Since the base copy of
`P` is not three-colourable, the full graph is exactly four-chromatic.

Thus source-colouring loss in the first subassembly does not amplify to an
ordinary non-four obstruction in this complete route.  The exact source and
this reflection completion are banked.  No neighbouring axes, further copy
counts, lens layers, or receiver trial are implied.

## Exact coordinates

All coordinates lie in `K = Q(sqrt(3),sqrt(11))`.  In the basis
`1,sqrt(3),sqrt(11),sqrt(33)`, put

```text
a = (sqrt(33)-3)/12,
y = (sqrt(3)+3 sqrt(11))/12,
s = sqrt(3)/6.
```

The twelve points, in label order, are

```text
(0,0), (1,0), (-a,y), (1+a,y),
(1/2-a,y-s), (1/2+a,y-s), (1/2,-s),
(-a,y-2s), (1+a,y-2s),
(1/2-a,y+s), (1/2+a,y+s), (1/2,s).
```

These formulas are an exact simplification of the symmetric Shibuya
realization.  `model.py` implements the biquadratic field with rational
coefficient tuples.  Reflections use the exact rational-in-the-field matrix
for a line through two points.  Equality, collision merging, and all unit
tests are coefficient equality, never a tolerance.

## Reproduction

CPython 3.11 or later and only the standard library are required:

```sh
python3 -B verify.py
python3 -B controls.py
```

The verifier independently reconstructs both complete graphs, enumerates all
canonical source colourings, decides each extension problem, checks the
blocked and surviving fixtures, checks the private-contact and connectivity
claims, and validates the final four-colour word.  `SHA256SUMS` pins the compact
package.  This is author-side exact computation, not independent review or a
formal proof-assistant result.

## Provenance and claim boundary

Pegg's graph list appears in the primary
[Math StackExchange question](https://math.stackexchange.com/questions/3958839/are-4-chromatic-3-connected-unit-distance-graphs-always-rigid).
The coordinate construction was independently transcribed from
[`shibuya/graphs/pegg.py`](https://github.com/Parcly-Taxel/Shibuya/blob/218097c9971db2b60ab94a0b8dae20d76741cc43/shibuya/graphs/pegg.py),
MIT-licensed at pinned commit
`218097c9971db2b60ab94a0b8dae20d76741cc43`.  No external coordinate file is
needed for verification.

The theorem concerns only the displayed exact source, the single `(0,6)`
reflection, and the fixed 18-reflection union.  It is not a theorem about all
realizations of the abstract graph or arbitrary reflection compositions.  It
does not classify every possible continuation of the 22-point forcing event.
