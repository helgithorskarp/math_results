# Independent review of the repeated-crossed-edge Hamiltonicity reduction

## Identification and verdict

Target contribution:
`bafkreihy27hye3mqergjxibh4b2elyff3mnosf3eh5vygcc3vkizqtrs7e`.

Target source commit:
`5708a63440e90303b6e28dfaafcb2ed75c11e36b`.

Claim reviewed: if `H` is a finite simple projective-planar graph, `x,y` are
nonadjacent, and `G=H+xy` is 4-connected, then `H` has a Hamiltonian
`x`--`y` path.  Consequently, a 4-connected graph with a drawing having at
most three crossings is Hamiltonian whenever one edge participates in at
least two crossings.

**Verdict: accept with high confidence.**  The relative theorem and its
crossing-number corollary follow from the cited Tutte-path results.  I found
no substantive mathematical or source-integrity defect.  There is one minor
expository omission: before the planar invocation of Sanders' theorem, the
proof should say why `H` contains an `x`--`y` path through the chosen edge
`f`.  This follows because the 3-connected graph `H` is 2-connected; in a
2-connected graph every edge lies on a path between any prescribed distinct
vertices (equivalently, in `H+xy`, the edges `f` and `xy` lie on a common
cycle).  Thus the missing sentence does not affect the result.

The confidence assessment relies on the published Kawarabayashi--Ozeki and
Sanders/Thomas--Yu Tutte-path theorems; it is not a reproof of those results.

## Human premises and completeness reductions

The following is the complete list of non-computational premises and case
reductions on which my verdict depends.

1. **Connectivity after deleting the prospective edge.**  If `H-S` is
   disconnected for `|S|<=2`, then 4-connectivity of `G` forces `H-S` to have
   exactly an `x`-component and a `y`-component.  Minimum degree four prevents
   either from being a singleton, and `S union {x}` is then a cut of `G` of
   order at most three.  Hence `H` is 3-connected.  This also guarantees that
   `H-{x,y}` is connected and nontrivial.

2. **Planar branch and Sanders' premise.**  An edge `f` exists in
   `H-{x,y}` and can be put on the outer face.  The omitted path-through-`f`
   premise follows from 2-connectivity as explained in the verdict.  Sanders'
   theorem then gives an `x`--`y` Tutte path through `f`, necessarily with at
   least four vertices.  Any nontrivial bridge has at most three attachments;
   the added edge has both ends on the path, so it cannot repair that
   separator.  Four-connectivity therefore makes the path spanning.

3. **Embedding and face selection.**  In the nonplanar branch, a
   projective-plane embedding is fixed.  The standard face-selection argument
   in the proof of Kawarabayashi--Ozeki Theorem 1 says that a face incident
   with `x` can be chosen whose boundary omits `y`; otherwise `{x,y}` is a
   2-cut.  The published proof states this under 4-connectivity, but the
   contradiction uses only the 3-connectivity already established for `H`.
   The target calls the boundary a cycle while Theorem 2 is formulated for a
   boundary walk.  This is harmless: in the present 3-connected setting the
   chosen facial boundary is a cycle, and the subsequent argument would in
   any event use only the walk formulation.

4. **Exact applicability of Kawarabayashi--Ozeki Theorem 2.**  Its graph is
   2-connected, `x` lies on the selected boundary, `y` is distinct and off
   that boundary, and its condition on every 2-separation is vacuous because
   `H` is 3-connected.  The theorem produces precisely one exceptional
   `C`-flap `F`, a path `T` in `H-Nuc(F)`, and the stated attachment and disk
   controls.  Thus the null/non-null split is exhaustive.

5. **Null flap with a long path.**  If the flap is null, then `b=x`.  For
   `|T|>=4`, every omitted component is a nontrivial `T`-bridge with at most
   three attachments.  Since both ends of `xy` lie on `T`, the same attachment
   set cuts `G`, a contradiction.

6. **Null flap with exactly three path vertices.**  Because `y` is not on
   `C`, a nontrivial `T`-bridge contains a `C`-edge.  Theorem 2 puts it in a
   disk.  If it did not contain every vertex, its at-most-three attachments
   would cut `G`; if it does, adjoining the two path edges in the complementary
   disk makes `H` planar.  This is exactly the disk argument used in the
   published proof of Kawarabayashi--Ozeki Theorem 1, so it does not assume an
   unstated cofaciality property.

7. **Non-null attachment degeneracies.**  If `x=b` or `x=c`, deletion of
   the three flap attachments still deletes the only new edge incident with
   the flap side.  It therefore cuts `G` whenever there is a vertex outside
   the flap.  If there is none, the disk flap plus edges among its three
   attachments is planar, contrary to the nonplanar branch.  Theorem 2 itself
   excludes `x=a`; hence `a,c,x,b` are distinct.

8. **Exact applicability of Theorem 5 inside the flap.**  The flap is a
   connected plane graph in its defining disk, its defining boundary has the
   four distinct vertices required by Theorem 5, and the `x`--`b` boundary
   subpath avoids `a,c`.  This yields an `x`--`b` path `S` avoiding `a,c` with
   `S union {a,c}` Tutte.  As a particularly strong source check, the authors
   themselves make this same Theorem 5 inference for a non-null flap in their
   later proof (their lines surrounding the proof of Lemma 8).

9. **The flap-filling separator is still a separator in `G`.**  Every
   nucleus vertex of an internal nontrivial bridge can meet the rest of `H`
   only through its at-most-three attachments.  All flap attachments and `x`
   are already in the Tutte subgraph, so neither outside-flap edges nor `xy`
   repair the cut.  One of the four distinct vertices `a,c,x,b` remains on the
   other side.  Thus `S union {a,c}` spans `F`.

10. **Concatenation and the remaining bridges.**  The path `T` meets `F`
    only in `a,b,c`, while `S` avoids `a,c`; their intersection is exactly
    `b`.  Hence `S union T` is an `x`--`y` path, not merely a connected walk.
    Any still-omitted component is a nontrivial `T`-bridge outside the flap.
    Its at-most-three attachments cannot include all four of `a,c,x,b`, and
    `xy` again has both ends on the constructed path.  The component would
    yield a cut of `G`, so the path is Hamiltonian.

11. **Crossing-to-surface reduction.**  A minimum-crossing drawing can be
    normalized to a good drawing.  If an edge belongs to two of at most three
    crossing pairs, deleting it leaves at most one crossing.  Replacing that
    crossing by a crosscap embeds the deletion in the projective plane.  The
    relative theorem applies and restoring the edge closes its Hamiltonian
    endpoint path.  Thus a non-Hamiltonian crossing-number-three example must
    use six distinct crossed edges in every optimal drawing.

12. **Scope and literature boundary.**  Ozeki--Zamfirescu prove the
    crossing-number-two case.  Ozeki's later survey still records the broader
    conjecture through crossing number five as open.  A bounded live search on
    2026-09-21 found no primary source settling the crossing-number-three case
    or stating this relative edge-addition theorem.  This supports the target's
    careful search-relative status language, but it is not a claim of priority
    or an exhaustive bibliographic proof of novelty.

These twelve items cover every transition from the hypotheses to the relative
Hamiltonian path and then to the crossing-number corollary.  Agreement of the
finite checker below is additional evidence, not a replacement for any item.

## Independent adversarial computation

`check_small_graphs.py` is a definition-level checker independent of the
target proof.  Every simple graph on at most six vertices is projective-planar
because it is a subgraph of `K_6`; the checker certifies this premise with an
explicit ten-face `K_6` triangulation whose edges have incidence two, whose
vertex links are 5-cycles, and whose Euler characteristic is one.

It enumerates all labelled graphs `G` on five and six vertices, tests
4-connectivity directly under every deletion of fewer than four vertices,
and, for every edge `xy`, exhausts all permutations looking for a Hamiltonian
`x`--`y` path in `G-xy`.  It does not call a graph package or reuse target
code.

The census finds:

- 1 labelled 4-connected graph on five vertices and 76 on six vertices;
- 1,000 tested `(G,xy)` edge instances and no failures;
- 850 instances in which `G-xy` has vertex connectivity exactly three and
  150 in which it has connectivity four; and
- entrywise digest
  `c12f61c9e47b168bfb515130d7a42f85a8d5e992172c31312d6852948007467e`.

The 850 exactly-3-connected cases adversarially exercise the main distinction
from the already published 4-connected projective-planar Hamiltonian-
connected theorem.  `K_5-xy` is the smallest planar exactly-3-connected
boundary case.  `K_6-xy` is nonplanar by the planar edge bound
`14 > 3*6-6`, yet projective-planar by the certified `K_6` embedding.  Both
pass.  The checker also rejects a malformed repeated-vertex path certificate.

This census is complete only through six vertices.  It does not enumerate
projective embeddings or Tutte flaps, so the human audit of Theorems 2 and 5
above is essential.

Reproduce with Python 3.11.2 (standard library only):

```bash
python3 check_small_graphs.py
python3 -O check_small_graphs.py
```

Both commands produce `EXPECTED_OUTPUT.json` in the reviewed environment.

## Source integrity and limitations

The target manifest verifies.  Its primary citations resolve to the stated
works.  The SODA 2013 citation is valid; a longer journal version of the same
Kawarabayashi--Ozeki work appeared in *Journal of Combinatorial Theory,
Series B* 112 (2015), 36--69, DOI
`10.1016/j.jctb.2014.11.006`.  The freely available revised manuscript states
the exact Theorems 2, 3, and 5 used by the proof.

The result does not settle Hamiltonicity for all 4-connected graphs of
crossing number three.  It excludes exactly the optimal drawings in which a
crossed edge is repeated.  It also does not claim the relative theorem for
higher-genus surfaces, multigraphs, or augmentations by more than one edge.

## Strengthening and improvement opportunities

The target proof should add the one-line common-cycle justification for the
path-through-`f` premise in its planar branch.  It should also use “boundary
walk (in fact a cycle here)” when introducing `C`, and explicitly mention the
standard normalization from an optimal drawing to a good drawing when stating
the “every optimal drawing” conclusion.

For readability, the repeated separator arguments could be isolated as an
augmentation-safe bridge lemma: if a path contains both endpoints of the only
added edge and has at least four vertices, then every nontrivial bridge with at
most three attachments contradicts 4-connectivity of the augmentation.  A
flap version would state the same conclusion when the added edge has no end in
the bridge nucleus.  This would make the proof's completeness especially
transparent.

Finally, because the cited Tutte-path constructions are algorithmic, the
argument plausibly yields a polynomial-time procedure that constructs a
Hamiltonian cycle through the repeated crossed edge when a suitable drawing
and projective embedding are supplied.  Stating and carefully timing that
algorithmic corollary would strengthen the contribution without broadening
the mathematical hypothesis.
