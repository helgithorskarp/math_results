# One period-two quotient of the nine-move seed is four-colourable

The specified lattice quotient of the certified nine-move Parts seed has
**432 distinct exact plane points and 1,055 complete unit edges**. A literal
proper four-colouring checks against all edges. This is a failed single
construction, not a five-chromatic graph or a theorem about arbitrary lattice
quotients. No period, frame, boundary convention, deletion or repair variant
was searched after this witness.

The positive input is the [509-point, 2,447-edge nine-move seed](../hadwiger_nelson_neutral_mutation_candidate/README.md).
Its source package provides an ordinary non-four certificate and proper
five-colouring. The present map changes edges, so that obstruction does not
automatically survive. The four-colour stopping result below does not depend
on trusting the parent's chromatic lower bound.

Write each source point uniquely as `p=s+t*omega`, where
`omega=(1+i*sqrt(3))/2`. Use the single fixed map

```text
m = floor((s+1)/2),       n = floor((t+1)/2),
f(p) = p - 2*m - 2*n*omega.
```

Its image lies in the half-open parallelogram with lattice coordinates
`-1 <= s,t < 1`. The two periods are `2` and `1+i*sqrt(3)`.
The distinct source points `+1,-1` have the same image, proving a budget of
at most 508 before inspecting chromaticity. No adjacent source pair collides.
All coordinates remain at scale 96 in the basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

This operation acts on nine translation cells. Within each cell the original
contacts survive. Wrapping also preserves unit edges parallel to `1` or
`omega`: the affected lattice-coordinate difference remains `+1` or `-1`.
Other crossing constraints must be reconstructed physically; their retention
is not assumed. This was the concrete coupling test, not a use of density or
a colour-count heuristic as non-four evidence.

| Exact quantity | Value |
|---|---:|
| Source points / edges | 509 / 2,447 |
| Image points / complete edges | 432 / 1,055 |
| Point-count saving | 77 |
| Moved source points | 297 |
| Collision classes of sizes 2, 3, 4 | 52, 8, 3 |
| Source labels participating in collisions | 140 |
| Source edges whose images remain unit pairs | 1,131 |
| Source edges lost | 1,316 |
| Distinct inherited unit pairs | 1,005 |
| New unit pairs with no source-edge preimage | 50 |
| Image points outside the nine-move seed | 220 |

The distinction between 1,131 retained source edges and 1,005 distinct
inherited unit pairs matters: several old edges have the same physical image.
The 50 genuinely new unit pairs are included in the colouring check. The
prescribed quotient therefore supplies physical cross contacts, but they do
not restore the lost chromatic obstruction. No exact chromatic lower bound
for this image is needed or asserted.

From this directory, CPython 3.11 and its standard library suffice:

```sh
python3 verify.py
```

The verifier reads the pinned exact source coordinates and integer translation
certificate. It verifies that each translated point is in the unique prescribed
half-open cell using rigorous 128-bit rational square-root enclosures. Thus
it checks the floor operation by its defining inequalities, independently of
the producer's iterative cell-location procedure. It merges exact coordinate
tuples, reconstructs all 129,286 source pairs and all 93,096 image pairs using
squarefree-radical/gcd products, and checks the literal 432-symbol four-word.
No floating-point tolerance or solver verdict is a verification premise.

For regenerated exact image coordinates, complete edges and collision classes:

```sh
python3 verify.py --emit /tmp/nine-move-period2
```

The source-coordinate rows have the published canonical SHA-256
`db7abc5818aee6729675838cefd92e12589f695bea9970425b62b9ee27afbae8`.
The input TSV bytes and word are bound by `certificate.json`. The separate
producer used the original seed constructor and integer mask-square arithmetic;
public regeneration agrees entry-for-entry on coordinates, edges and every
source-to-image assignment. One CaDiCaL 1.9.5 query found the four-word, with
exit 10. Geometry, that query and initial word checking took about 4.2 seconds.
The proof of the upper bound is the literal word check, not the solver.

The result is author-side reproducible evidence, not independent review or
formalization. Trust remains in the exact coordinate input, independence of
the radical basis, the elementary quotient formula, Python integer arithmetic
and the complete certificate checker. Generated geometry, CNFs and solver logs
remain outside Git. No refutation certificate is claimed.

The earlier [one-axis edge-preserving reflection theorem](../hadwiger_nelson_bisector_fold_gate/README.md)
and [delete-and-hinge closure](../hadwiger_nelson_hinge_flip_gate/README.md)
concern different maps. This result closes only the frozen period-two quotient
and its subgraphs. It does not justify another period or quotient search.
Both reviewed Parts receivers remain banked library inputs.

[Parts's 509-point record](https://arxiv.org/abs/2010.12665), still identified
as current by [Haugland v4](https://arxiv.org/html/2608.04542v4), is unchanged
by this four-colourable image.
