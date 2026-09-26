# Exact equality in Gaussian common-set reference tests

For any contraction T on a compact subset of R^n, let sigma be a reference
law on whose support T is an isometry S. If A is a positive superlevel set
of sigma convolved with a Gaussian, the single target set S A satisfies

```text
integral_(S A) gamma_s(z-Tx) dz >= integral_A gamma_s(z-x) dz
```

simultaneously for every input center x. Equality at a center holds exactly
when all its distances to the reference support are preserved.

The stronger result concerns the **optimized** common-set gap

```text
J_A(mu) = sup_(|E|=|A|) integral_E (T#mu)*gamma_s - integral_A mu*gamma_s.
```

Its minimum over all priors mu is zero. Its zero minimizers are exactly
those for which T is one isometry on the union of the actual and reference
supports, and A is also a maximizing set for the actual source density.
The common target set S A is the unique dual maximizer, up to null sets.
The statement includes diffuse priors and holds in every finite dimension.

[PROOF.md](PROOF.md) gives a complete author proof: affine-bisector
polarization proves transfer; translation stationarity and a positive
transverse Gaussian weight force the equality rigidity. The latter remains
useful even when the pointwise transfer has zero slack everywhere.

This extends the transfer part of the finite lane's isometric-face theorem
to arbitrary contractions and classifies all zero minimizers for these
tests. It supplies a boundary condition for the measure lane's global
common-set criterion. Arbitrary source sets are still missing, so the full
R3 majorisation question and its global endpoint coupling remain open.
There is no new positive map family, stability threshold or Kneser--Poulsen
class. Independent mathematical review and formalization are pending.

[SOURCES.md](SOURCES.md) records the primary literature, the known
singleton-reference ball case, team dependencies and remaining quantifiers.
There is no numerical or computer-assisted premise. Read the proof directly;
from this directory verify its source integrity with

```sh
sha256sum -c SHA256SUMS
```

Expected: all three listed source files report `OK`. This command verifies
bytes, not mathematical validity. The proof needs only ordinary finite
dimensional integration, differentiation, reflection and linear algebra.
