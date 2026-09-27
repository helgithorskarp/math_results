# Counterexample search boundary: signed radial product laws

This is a uniform theorem about actual Gaussian hinges, not an optimizer
report or an obstruction to one proof method. Under the radial cloud and
endpoint-loss conditions in [PROOF.md](PROOF.md), no adverse hinge exists
at any variance above the displayed cutoff. Angular laws and the radial law
between the two clouds are arbitrary, and may be diffuse. Preserved pairs
and sign reversals are permitted.

The qualitative conclusion covers every bounded nonnegative radial law
whose support contains zero, under every odd scalar contraction, provided
radius and direction are independent. Each nonisometric instance has a
finite all-threshold variance cutoff. The quantitative family needs only
two aggregate radial mass bounds and one endpoint contraction bound.

The reusable mechanism operates on the coefficients of two iid radii.
Their low/high cloud means ell,r give six signed source vectors
`+/-(r,-ell), +/-(ell,-r), +/-(r,-r)` whose hull contains `(r-ell)K`, where
K is the unit hexagon `|x|,|y|,|x+y|<=1`. Scalar Lipschitz geometry puts all
target coefficient pairs in a strictly smaller hexagon. Conditional Jensen
then yields, for kappa=1-epsilon/4 and a bulk-mass constant w,

```text
P_Y(t) <= w^-1 P_X(kappa t),
J(lambda) >= (epsilon/4)S_X(lambda) - (1/2)log(1/w).
```

Here P is the symmetrized difference MGF. The finite mass penalty is material;
this inequality is not a dilated martingale certificate. A lower bound on
S_X controls all large lambda, and the earlier exchange identity supplies
a strict gap on the remaining compact range. The accepted all-threshold
endpoint6032/6048 finishes the argument with no new Gaussian quadrature.

The useful change from original6339 is from nonnegative spherical tests to
actual all-threshold eventual comparison, uniformly for a diffuse family.
This conclusion is independent of a global small Lipschitz constant: the
ball-reflection profile fixes an inner region and has Lipschitz constant one.
No claim excludes every other existing positive theorem on particular laws.

The publication refresh found R1's universal spherical comparison and finite
eventual theorem. Those author results close the spherical falsifier for
arbitrary contractions and subsume a qualitative finite-only consequence.
This handoff therefore concerns the remaining diffuse, Lipschitz-one class
and its uniform cloud cutoff. R1's proof explicitly leaves the unrestricted
diffuse Lipschitz-one endpoint open. The present proof is independent of that
new premise; it uses the older accepted Gaussian endpoint instead.

Smaller variances and radius--direction dependence remain unresolved.
The complete dimension-three question and every new KP consequence remain
open. Improving the enormous constant, certifying isolated positive priors,
or adding nearby parameter tables is not the purpose of this handoff.
The finite-atomic low-noise and orthocentric assignments remain closed.

Status: complete author argument, exact ancillary checks, pending independent
review. The new result does not inherit review status from its dependencies.
