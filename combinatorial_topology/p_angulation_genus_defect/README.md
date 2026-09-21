# Fixed-excess embeddings above a clean p-angulation

Let a finite simple graph have a specified closed orientable `p`-angulation
of genus `h`.  Assume that every face boundary is a simple `p`-cycle, the
minimum degree is at least three, the graph has girth `p`, and every graph
`p`-cycle is one of the reference faces.  An embedding of genus `h+r` can
lose only a bounded number `t` of reference faces:

```text
2r + 1 <= t <= 2(p+1)r                 (r > 0).
```

The missing faces, one orientation bit for each retained-dual component,
and exactly `pt` local path blocks encode the embedding.  In particular,
for fixed `p,r`, all genus-`h+r` rotation systems can be listed in polynomial
time, with no maximum-degree assumption.  The precise coefficient bound is

```text
a_(h+r)(G) <= sum_t binom(f,t) 2^t ((t-1)!)^p,
```

where the sum runs from `2r+1` to `min(2(p+1)r,f)`.

- [PROOF.md](PROOF.md) gives the complete theorem, proof, decoder, scope,
  and literature boundary.
- [verify.py](verify.py) is a definition-level exact checker for the
  tetrahedral `p=3` and cubical `p=4` instances.
- [EXPECTED.json](EXPECTED.json) is its compact deterministic output.

Reproduce with CPython 3.11 or later; no third-party package is needed:

```bash
python3 verify.py > /tmp/p-angulation-genus-defect.json
diff -u EXPECTED.json /tmp/p-angulation-genus-defect.json
sha256sum -c SHA256SUMS
```

The computation checks every labelled orientable rotation system of both
fixture graphs and independently reconstructs the same systems from deleted
reference faces.  It corroborates the finite conventions; the universal
theorem is the mathematical argument in `PROOF.md`.

This extends the previously published triangular face-defect mechanism to
all clean `p`-angulations.  It does not prove log-concavity or unimodality of
genus distributions, and no optimality claim is made for `2(p+1)` when
`p>3`.
