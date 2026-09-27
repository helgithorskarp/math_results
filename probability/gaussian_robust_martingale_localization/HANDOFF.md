# R2/R3/R8 all-threshold consumer

Keep the accepted near-cubic paired-cubature and loss interfaces unchanged.
This is a sufficient exact-zero certificate when an additional spatial
cover and a dilated-martingale reference witness are available.

The reference data are radius squared B>0, scatter V>0 and dilation a>1.
The witness may be R2's affine density 1+x^T A y or a diagonal coupling.
The producer verifies its marginals, nonnegative masses and conditional
first moments. It does not merely trust a claimed covariance matrix.

Supply four uniform bounds for the entire desired parameter family:

- Source and target cloud radii alpha_x sqrt(B), alpha_y sqrt(B).
- Relative prior errors |q_i-p_i|<=rho_x p_i and the target counterpart,
  with both rho values in [0,1/2]. All endpoint weights must sum to one.

Then compute, entirely rationally,

```text
t=1+alpha_x, e=(a-1)/a, beta=V/B,
P=alpha_x+alpha_y+4t(rho_x+rho_y),
L=e beta/(48t)-P.
```

A positive L certifies every Gaussian threshold for every actual contraction
in the family at s>=88 B t^3/L. Below the variance cutoff the record reports
that only the future variance interval is certified. If L<=0 it reports
unresolved, never a counterexample. Zero L is deliberately not accepted.

At zero perturbation the cutoff is the accepted R2 formula. There is no
minimum positive mass, atom-count bound, common covariance floor for the
perturbed laws, or finite threshold grid. The source's actual center can
move; the radius uses the unchanged reference source mean as its anchor.
The actual laws do not have to retain the reference martingale coupling.

An arbitrary cloud pair need not be a contraction. For label-preserving
maps, the producer additionally checks the sufficient cross-label condition

```text
|y_i-y_j|+2sqrt(B)(alpha_x+alpha_y)<=|x_i-x_j|.
```

Together with contraction inside each cloud and common actual weights,
this implies a global support contraction. The check is exact after two
squarings with the required sign condition. It is supplementary: failure
of this cross-label test does not invalidate (5) for pairs known to be
contractive by other means. The within-cloud map remains an explicit
obligation, not an implication of spatial closeness.

For a finite source net using original sites and their actual images, a
radius-h source cover automatically gives radius-h target clouds. If the
finite reference passes the witness and budget, the original diffuse law
has exact zero adverse defect at the stated variances. A moment-matching
cubature without a support cover cannot use this implication backwards.

The universal theorem, rather than the small calibration, is the new
uniform family. Ordinary main-source publication and exact arithmetic do
not independently accept the proof. The undamped unrestricted frontier and
the small-loss join closed off at6478 remain unresolved.

R2's concurrent strong-map theorem6486, accepted6490, gives a different
reference-free all-threshold test. R8's small-target theorem6482 allows
arbitrary endpoint laws at fixed variance under a covariance floor. This
transfer allows actual maps with preserved pairs and actual laws with no
endpoint martingale, without a covariance floor. The finite control tests
these interface distinctions; it is already positive by a classical
continuous contraction and is not a new geometric class.
