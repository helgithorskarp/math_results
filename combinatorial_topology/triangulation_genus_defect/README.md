# A sharp face budget for embeddings above a triangulation's genus

Let a simple graph have a specified closed orientable triangulation of genus
`h`, and assume every graph triangle is a face of that triangulation. An embedding
of genus `h+r` can lose at most **8r reference triangles**. Those triangles,
orientations of the retained face components, and at most **24r local path blocks**
completely encode the embedding, without a maximum-degree assumption.

The [proof](PROOF.md) gives an exact decoder and, for `r>0`, the bound

\[
a_{h+r}(G)\le\sum_{t=2r+1}^{\min(8r,f)}
\binom ft\,2^t\big((t-1)!\big)^3,
\]

where `f` is the number of reference triangles and embeddings are counted as
labelled rotation systems, with global reversal counted separately. The minimum
coefficient is `a_h=2`. All fixed-excess-genus embeddings can consequently be
listed in `O_r((|V|+|E|) f^(8r))` time, given the promised triangulation.

The coefficient eight is sharp: an explicit octahedral torus embedding replaces
all eight spherical triangles by six quadrilaterals. A `K_7` control loses six
reference triangles at excess genus zero, showing why the triangle hypothesis
cannot simply be removed.

This is a structural contribution around [Mohar's triangulating-graph genus
conjecture](https://arxiv.org/abs/2405.10854), not a proof of log-concavity or
unimodality. The polynomial exponent and coefficient bound are not asserted
optimal. The proof is unformalized and historical novelty is search-relative.

## Reproduce

Tested with CPython 3.11.2; no external dependencies. From this directory:

```bash
python3 verify.py > /tmp/triangulation-genus-defect.json
diff -u EXPECTED.json /tmp/triangulation-genus-defect.json
sha256sum -c SHA256SUMS
```

A successful run prints the exact JSON in [EXPECTED.json](EXPECTED.json), exits
zero, and matches the manifest. The audited run took 3.60 seconds and about
41 MiB maximum resident memory on the campaign host.

[verify.py](verify.py) checks two different enumeration routes entry by entry:
all cyclic vertex orders directly, and reconstruction from deleted faces and
local path blocks. They agree on all 16 tetrahedral and 46,656 octahedral rotation
systems. The decoder examines respectively 54 and 86,714 candidates, rejecting
completions in which a nominally deleted triangle reappears. The full canonical
rotation-record SHA-256 for the octahedron is
`763c465b629dbaf2c007ef579e4a89305391bddfe928902b67e605825c4fabfa`.

The checker also verifies 25 certificate round trips on bipyramids and torus
grids, including degrees 12 and 64; the sharp octahedral quadrangulation; the
`K_7` hypothesis counterexample; and three invalid partial-permutation controls.
These finite checks corroborate the universal proof. Both enumeration routes
share the final face-orbit tracer; this is a disclosed common trust boundary,
not an independent peer review or formal verification.

Only compact source and deterministic output are included. No solver, floating
point calculation, external data set, or unpublished certificate is required.
