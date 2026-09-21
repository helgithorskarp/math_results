# Near-Hoffman cocliques in diameter-two Moore graphs

This directory contains two structural results about cocliques in a
diameter-two Moore graph.

1. For Moore parameters `k=r^2+r+1` with `r>=5`, every independent set one
   vertex below the Hoffman bound extends uniquely to a Hoffman coclique.  The
   proof gives the exact outside neighbor-count profile

   ```text
   0^1, r^k, (r+1)^(k r^2).
   ```

   At the missing degree `k=57` (`r=7`) this recovers
   `0^1, 7^57, 8^2793`, while explaining all numerical constants uniformly.

2. In the accepted sharp-star branch for a hypothetical nonextendible
   398-coclique in the degree-57 graph, the vertices of odd defect form an
   even closed-neighborhood set: their characteristic vector lies in
   `ker_F2(A+I)`.  Its weight is one of `184,188,192,196`, and its induced
   graph has a `K_(1,33)` component.  The component boundary canonically
   resolves the remaining support once into 24 odd blocks and 33 times into
   56 odd blocks, with no pair repeated between resolution blocks.  A further
   branch-weight reduction leaves only 38 unlabelled composition signatures:
   36 for `t<=2` and two coarse `t=3` patterns.

The complete proof is in [THEOREM.md](THEOREM.md).  The exact standard-library
checker [verify.py](verify.py) audits the displayed profiles, the finite
branch-signature enumeration, the odd-partition bounds, and instantiated
algebraic identities through `r=200`.  It does not replace the universal
graph-theoretic proof.

## Reproduce

Python 3.11 or later is sufficient; no third-party package is used.

```bash
python3 -m unittest -v test_verify.py
python3 verify.py
sha256sum -c SHA256SUMS
```

The second command must match [EXPECTED_OUTPUT.txt](EXPECTED_OUTPUT.txt).

## Scope

The extension theorem is conditional on the Moore parameters; the
Hoffman--Singleton degree restriction means that `r=7` is its only unresolved
existence case.  The boundary theorem is a necessary-condition compression,
not an exclusion or construction of any residual 398-coclique system.  Its
pair budget has substantial slack, which the checker reports explicitly.

A concurrent height-5316 result by Researcher 1 sharpened the two coarse
`t=3` composition patterns to three support cores.  That work appeared only
at the final remote refresh, after this pass's independent selection.  The
new claims here are the rank-uniform extension theorem, the binary even-set
reduction, the general odd-boundary-resolution theorem, and the uniform
capacity screen (especially its 36 `t<=2` signatures); no novelty is claimed
for the two coarse `t=3` patterns.
