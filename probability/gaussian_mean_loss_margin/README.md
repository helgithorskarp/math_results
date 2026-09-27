# A uniform sign margin from small mean contraction loss

The [author proof](PROOF.md) establishes the following uniform bridge at
unit Gaussian variance. Fix a centered source-radius bound `R`, covariance
floor `kappa>0`, and finite volume bound `V`. There are `c,D_*>0`, depending
only on these three parameters, such that every bounded probability law in
this family and every 1-Lipschitz image with mean squared-distance loss
`0<D<=D_*` satisfy

```
L_target(v) - L_source(v) >= c v D,     0 < v <= V.
```

The same margin holds when the aligned target is tested on the actual
source top set, so it also signs every hinge above any fixed positive
normalized threshold. There is no minimum atom mass or number of atoms,
and rare points may move a fixed distance as `D` tends to zero. The radius
need not be small relative to the Gaussian variance.

The proof combines the credited posterior first variation with a strict
one-point reflection comparison and a bulk/rare decomposition. Its
compactness constants are **not numerically evaluated**. The covariance
floor, finite volume bound, and small mean loss remain hypotheses. Full
three-dimensional majorisation and a new Kneser--Poulsen consequence remain
open. Independent mathematical review is pending.

[SOURCES.md](SOURCES.md) records attribution and the minimal R2/R3/R8 handoff.
The exact rational controls demonstrate why small mean loss does not imply
small maximum aligned displacement; they are not a computer proof of the
compactness theorem.

From the repository root, with Python 3.11 and only the standard library:

```sh
python3 probability/gaussian_mean_loss_margin/verify.py
python3 -O probability/gaussian_mean_loss_margin/verify.py
```

Both commands must print `MEAN_LOSS_MARGIN_CONTROLS_PASS` and the same
record hash. [EXPECTED.json](EXPECTED.json) is a compact checked output;
[SHA256SUMS](SHA256SUMS) lists the source hashes. No external dataset,
solver, floating-point Gaussian quadrature, or credentials are needed.
