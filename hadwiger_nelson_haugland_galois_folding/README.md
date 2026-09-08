# Pointwise Galois folding of Haugland2131 needs at least 1,251 images

**Exact computer-assisted obstruction.** Put
`K=Q(t,sqrt(5))`, where `t=exp(pi*i/21)` is a primitive 42nd root of unity.
Let `z_0,...,z_2130` be the fixed complex coordinates of Haugland's archived
2,131-point graph `G3`, in the labels of the pinned sibling `graph.json`.
For each vertex independently, choose any automorphism `sigma_v` of `K/Q`.
If

```
f(v) = sigma_v(z_v)
```

preserves all 12,530 archived unit edges, then **`|f(V)| >= 1251`**.
Consequently no such folding yields a graph on at most 508 points. A common
Euclidean isometry after folding does not affect this conclusion.

The bound is not claimed sharp. This is a complete obstruction for the
specified conjugate-assignment mechanism, not a vertex lower bound for
arbitrary subgraphs of Haugland2131 or arbitrary plane unit-distance graphs.
It allows different automorphisms at different vertices and new points in
the Galois closure of the support. It is distinct from the previously closed
metric-ball extraction family. It does not cover arbitrary new supports,
vertex-dependent translations, or changing the common coordinate origin
before applying the rule.

## Construction gate and chromatic scope

The source is the published five-chromatic construction in
[Haugland, arXiv:2608.04542](https://arxiv.org/html/2608.04542v4), Section 3.
The campaign previously checked its exact geometry and strict edge list;
its independent endpoint-forcing SAT refutation remains unfinished.
**This package neither assumes nor completes that chromatic refutation.**
Its order obstruction holds for the explicit edge-preserving map problem
regardless of the chromatic number. No new graph requiring five colours is
claimed here.

An initial orbit screen found 355 Galois orbits in the finite reduction;
that count alone does not exclude 508 images. The full edge constraints
then gave the 1,251-point obstruction below. No candidate growth, geometric shell,
vertex deletion, or colouring SAT search was run. The Galois-folding route
is now closed at the target scale. No EI branch was resumed.

## Certificate and verification

The reduction has 6,049 possible modular sites. Normalize the image of source
vertex 1069 to its original value, which covers every possible choice up to
a common field automorphism. Nine synchronous rounds of arc consistency
leave 1,075 singleton domains and 1,056 domains of size six.

`certificate.json` names **1,251 source vertices whose remaining nonempty
domains are pairwise disjoint**. Every valid assignment must therefore use
at least 1,251 distinct modular sites, hence at least that many actual plane
points. The certificate does not rely on a SAT verdict, a graph-colouring
oracle, or a numerical distance tolerance. [PROOF.md](PROOF.md) proves the
Galois coverage, normalization, reduction, pruning, and cardinality bridges.

From this directory, using Python 3.11+ and its standard library:

```bash
python3 verify.py --check-expected
python3 -O verify.py --check-expected --controls
sha256sum -c SHA256SUMS
```

For a separate characteristic-zero reconstruction, install
`python-flint==0.8.0` in an environment outside the repository and run:

```bash
python3 audit_exact.py
```

That audit reconstructs the 740-, 1,066-, and 2,131-point sets in the rational
polynomial quotient `Q[t]/Phi_42(t)` and its quadratic extension by `sqrt(5)`.
It checks all 84 generating unit vectors, every path endpoint, and all
12,530 unit edges exactly. Its reductions at all 24 actions match the
Cartesian modular reconstruction's complete point stream. Its expected
output is `expected_exact.json`. Nonedges and the chromatic lower bound are
not rechecked.

`verify.py` imports no historical geometry implementation or producer code.
It lifts each field action to `Q(zeta_84,sqrt(5))` fixing `i`, reconstructs
real Cartesian coordinates, and verifies their relation to the complex
Galois action. The exploratory producer instead used complex coordinates
directly and an asynchronous AC-3 queue. Both give identical point streams
and final domains. The certificate checker uses synchronous complete sweeps
and checks domain separation directly, without the producer's domain-cover
minimization.

The canonical final-domain SHA-256 is

```
2f4db6e0a7ba543f04ffd1df3ed2695c245703d35e86beff9763ac1da26fad10
```

All input identities, modular constants, versions, and the producer/checker
comparison are in `provenance.json`. The source path table and edge list are
reused from the existing reconstruction package and pinned by SHA-256; no
large new graph or certificate is committed. `certificate.json` contains
only arithmetic constants, one anchor, and the disjoint-domain witness.

## Dependencies and limitations

The input and previous exact edge audit are available in
[the reconstruction](../hadwiger_nelson_haugland2131_exact_reproduction/README.md)
and [strict-edge package](../hadwiger_nelson_haugland2131_strict_edges/README.md).
The new characteristic-zero audit independently checks the geometry needed
for this edge-preserving map problem. Identification with the paper inherits
the archived Appendix A transcription; no new transcription is asserted.

The mathematical trust boundary is the elementary cyclotomic/Galois proof,
exact modular arithmetic, safe constraint propagation, direct disjointness
checks, and ordinary Python execution. The separate geometry audit also
trusts FLINT rational polynomial arithmetic. This is author cross-validation,
not an external review or proof-assistant formalization. Modular collisions
or spurious modular unit edges can only weaken the lower bound; neither can
invalidate the exclusion. The displayed site and orbit counts refer to the
modular reduction, not an asserted census of all characteristic-zero images.

The campaign's unrestricted comparison is the 509-vertex Parts graph. This package supplies a
scoped obstruction and no record improvement. Yield at this completed
milestone; do not enlarge or repeat the same folding family.
