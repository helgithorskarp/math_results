# Certificate interface

`INPUT.json` has matching rational source and target lists with two rational
anchors, an integer radius at least one, a nonnegative integer mass
exponent, and a rational variance ratio at least one. Integers and exact
rational strings are accepted; floating-point values are rejected.
Coordinates are measured in units where the minimum variance is one.

The width witness contains rational barycentric rows for each target in
the anchored source hull, a rational unit cap axis, cap cosine, upper bound
on the cap sine, and a source witness index. Optional
`perpendicular_bits` sets the producer's upward dyadic precision (default
16). A failed guard raises an error. It is not a Gaussian counterexample.

The certificate records the exact uniform prior-loss floor, a cap-based
width lower bound, perpendicular upper bounds and the integer schedule
from the proof. In particular `budget_exponent=B` encodes `2^-B`, not `B`
itself as a perturbation radius. The denominator is never expanded.

The consumer may use any probability vector `v_i>=2^-mass_exponent`.
Its actual probabilities `u,z`, common cloud radius `epsilon`, and
arbitrary conditional cloud laws must satisfy

```
sum v_i=sum u_i=sum z_i=1,
2 epsilon + ||u-v||_1 + ||z-v||_1 <= 2^-B,
supp(alpha_i) subset B(p_i,epsilon),
supp(beta_i) subset B(q_i,epsilon).
```

These are mathematical input obligations, not facts a JSON record can
decide about an unspecified measure. The conclusion is simultaneous over
every such measure, every nonnegative density threshold, and every variance
in the displayed closed interval. A common map or common actual prior is
not an additional premise.

The supplied-record verifier does not import the producer and permits
weaker certified width/loss bounds or larger safe schedules. Its output
does not upgrade the analytic proof to independent acceptance. Tests and
source pins are author reproducibility evidence only.
