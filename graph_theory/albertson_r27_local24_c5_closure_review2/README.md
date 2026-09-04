# Independent review of the terminal-triangulation `C5` closure

**Verdict: accept, with high confidence and an explicit imported trust
boundary.**  I independently checked the new topological step in
[`albertson_r27_local24_c5_closure`](../albertson_r27_local24_c5_closure/README.md)
at immutable commit
[`8c04121343a9e7a33aa7feeeda851531dc7cf8ee`](https://github.com/helgithorskarp/math_results/tree/8c04121343a9e7a33aa7feeeda851531dc7cf8ee/graph_theory/albertson_r27_local24_c5_closure).
Within the previously reviewed equality-profile classification, the proof
does close both remaining profiles and establishes

```text
cr(24,132) >= 165.
```

Together with the separately reviewed exact propagation, this settles the
remaining `r=27` Albertson frontier.  This review is deliberately narrower
than a re-review of the long structural classification on which the two
profiles depend.

## Independent derivation of the new step

Let a crossing-graph component be labelled

```text
b -- a -- c -- d -- f -- b.
```

Delete `b,c`.  Then `a` becomes uncrossed and `d,f` retain one crossing.
Doing this in every crossing `C5` gives a good simple 1-planar drawing `T`.
For the two imported profiles, exact arithmetic gives

| profile | crossing `C5`s | already full | `e(T)` | `x(T)` |
|---|---:|---:|---:|---:|
| A | 10 | 9 | 83 | 17 |
| B | 12 | 11 | 82 | 16 |

In either row, the planarization has

```text
V = 24+x(T),    E = e(T)+2x(T) = 3V-6.
```

The planarization is a simple plane graph.  Equality in the planar bound
(and the positive edge count) makes it a connected plane triangulation.
At the crossing vertex of `d,f`, the four distinct original endpoints
alternate.  Each consecutive pair is joined by an edge, because each
incident face is triangular.  Thus `d,f` occupy an empty kite.

Now take the unique non-full component and write `a=zw`.  The middle piece
of `c`, after crossing `a` and before crossing `d`, lies in a triangular
face.  Hence `zw` is a side of the kite.  Label the kite boundary cyclically
`z,w,r,t`, with `d=zr` and `f=wt`.  The face on the other side of `zw` is
`u,z,w`.  Tracing the final pieces of the deleted arcs through their unique
triangular faces forces

```text
c=ut,    b=ur.
```

The five relevant faces are therefore

```text
uzw, zwx, wrx, rtx, tzx,
```

where `x` is the crossing of `d,f`.  Their mod-2 boundary is the simple
5-cycle

```text
u-z-t-r-w-u.
```

Its complementary five `K5` edges are exactly

```text
zw, ur, ut, zr, wt,
```

and their crossing graph is a `C5`.  The distinctness needed here follows
from goodness and simplicity: the kite has four distinct endpoints, while
`u=r` or `u=t` would make `b` or `c` a loop.

The delicate point is provenance of the five outer sides.  A survivor made
uncrossed by deleting two edges from some *other* component cannot supply
one of them.  Every other component is an imported full pentagon, and
`m0=0` says all of its crossing-free boundary edges are present.  Its
vertex-empty pentagonal disk is therefore sealed: the five diagonals and
boundary form the complete simple graph on those vertices, and an outside
edge cannot cross the full 2-planar configuration.  Its survivor remains in
that disk.  The exceptional component cannot lie in the disk—there is no
interior vertex and no missing vertex pair—so all outer sides above were
already uncrossed in the original 2-planar drawing.  The exceptional
component is consequently a full pentagon too, contradicting the imported
counts `10=9+1` and `12=11+1`.

This is a global triangulation argument.  It does not assume that a face
from an earlier block-local reduction survives after blocks are reassembled.

## Independent executable evidence

[`verify_local_map.py`](verify_local_map.py) is a fresh exact checker of the
finite incidence layer.  It reconstructs the five-face disk, derives its
boundary by edge-incidence parity, forces the endpoints of `b,c`, verifies
that the crossed edges are precisely the complementary pentagram, checks
the crossing graph, recomputes both terminal profiles, and reproduces the
order-54 sampling bound.  It shares no code with the reviewed verifier.

Run with CPython 3.9 or later; there are no third-party dependencies:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_local_map.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify_local_map.py
```

The exact expected transcript is in
[`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt).  The deterministic certificate
digest is

```text
6ec60e1d459e86417e5166600564e395e6a94a2d62801cfe1bb19ed1df96ca34.
```

## Trust boundary and uncertainty

The program checks incidence and integer arithmetic; it does **not** certify
Jordan separation, face tracing, or the provenance argument.  Those are the
independently re-derived mathematical steps above.  This verdict imports:

- good-drawing normalization;
- the previously reviewed PRTT equality/profile classification, including
  that only the two displayed rows remain and each has exactly one non-full
  crossing `C5`;
- the Büngener--Kaufmann full-configuration facts and the predecessor's
  `m0=0` conclusion; and
- the separately reviewed exact sampling/convexification propagation from
  the local bound to the Albertson `r=27` frontier.

I re-ran the predecessor profile verifier, the target verifier, and two
independent global-propagation verifiers.  I also checked the primary
Büngener--Kaufmann definitions: a full 2-planar pentagon lies in a planar
vertex-empty pentagonal boundary, outside edges cannot cross it in a
2-planar drawing, and `m0` counts absent crossing-free boundary edges.

Residual uncertainty is therefore concentrated in the imported structural
classification, not in the short terminal-triangulation closure.  Because
the combined conclusion is a notable frontier result, publication should
state every imported lemma and version explicitly and should seek another
specialist check of the complete chain.

## Strengthening and improvement opportunities

1. Promote the proof attempt to a theorem only after pinning all predecessor
   statements and source commits in a single dependency manifest.
2. Add a rotation-system diagram (or formal combinatorial-map proof) for the
   triangle--kite union and spell out connectedness in the Euler-equality
   step.
3. State explicitly in the main proof that `u,r,t` are distinct and quote
   the exact definition of `m0`; these facts are valid but currently terse.
4. Consolidate the equality classification, local closure, and global
   propagation into one paper-style proof so the unconditional conclusion
   is not assembled only through repository cross-references.
5. Obtain a genuinely independent full-chain review before claiming
   priority; this audit establishes correctness within its stated imported
   boundary, not a literature-wide novelty claim.

## Sources

- J. Pach, R. Radoicic, G. Tardos, and G. Toth,
  [*Improving the Crossing Lemma by Finding More Crossings in Sparse
  Graphs*](https://doi.org/10.1007/s00454-006-1264-9).
- A. Büngener and M. Kaufmann,
  [*Improving the Crossing Lemma by Characterizing Dense 2-Planar and
  3-Planar Graphs*](https://arxiv.org/abs/2409.01733v2).
- E. Ackerman,
  [*On Topological Graphs with at Most Four Crossings per Edge*](https://arxiv.org/abs/1509.01932).
- A. Sadhu,
  [*Albertson's Conjecture and the Crossing Number of Sparse
  Graphs*](https://arxiv.org/abs/2609.01682).
