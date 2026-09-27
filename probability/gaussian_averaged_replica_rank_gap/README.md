# A uniform averaged improvement in the four-replica comparison

Complete author proof, 27 September 2026. Independent review and
formalization are pending. **Full R3 Gaussian majorisation remains open.**

For every bounded R3 probability law, every 1-Lipschitz image and every
Gaussian variance, the [proof](PROOF.md) establishes

```
B4 >= (8/9)^3 (1+eta) I_D,
B2 B4 >= (8/9)^3 (1+eta) B3^2,
```

with ONE universal constant eta>0. Here Bm are the marked Gaussian replica
averages and I_D is the diamond-graph average defined in the proof.
There is no radius, variance, atom-count, minimum-weight, covariance-floor
or small-loss hypothesis. The new point is a strict UNIFORM improvement
over the six-dimensional conditional kernel bound after the actual time
average. It does not assert a stronger pointwise kernel representation.

The value of eta is non-effective: it uses separation of Gaussian-smoothed
Lipschitz graphs from the full Gaussian law. Its specified definition gives
eta<=5/2808. Consequently this theorem does **not** reach the required
first-Hankel constant (8/9)^(5/2), sign a new general beta entry, prove
full majorisation, or give a new Kneser--Poulsen class. Its purpose is an
averaged analytic dependency toward that missing sign, not a headline solution.

The mechanism combines an exact Gaussian-kernel/chi-square identity, a
compactness argument for Lipschitz graphs, and a truncated-exponential
coupling for the remaining interpolation loss. [SOURCES.md](SOURCES.md)
records the prior results and current dependency boundaries.

Reproduce the compact exact controls with standard-library Python3.11+:

```
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both Python runs compare their result to EXPECTED.json and print
AVERAGED_REPLICA_RANK_GAP_CONTROLS_PASS. They check graph/clock identities,
Gaussian completion and moment constants, normalization and rejection of
corrupted output. They do not compute eta or independently prove the
compactness theorem. No numerical search, floating sign, solver, dataset,
private artifact or omitted large certificate is a premise.
