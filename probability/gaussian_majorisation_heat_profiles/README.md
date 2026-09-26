# Heat profiles: a comparison obstruction and a global contact reduction

[CONTACT_REDUCTION.md](CONTACT_REDUCTION.md) now reduces the full bounded-law
dimension-three question to a precise inequality at ordered heat-profile
contacts. Any hypothetical failure can be regularized and perturbed into
a finite positive-time contact with a **strictly adverse heat-flux sign**.
The proof supplies the initial order, a uniform bound at large volume,
and a treatment of critical density levels using a bulk flux integral.
It does not establish the missing contact inequality or settle the full
conjecture. Independent review of the reduction is pending.

The normalization smooths the input **before** applying a globally strict
contraction. Its auxiliary input has Gaussian tails; bounded failures
transfer to it and conversely. This removes the flat atomic initial-data
problem without assuming a Kneser--Poulsen comparison. A scalar target
dilation makes the first contact transverse, so a weak flux inequality
at all ordered contacts would suffice.

Its finite constant checks, with CPython 3.11 or later and no dependencies:

```sh
python3 contact_audit.py --check CONTACT_EXPECTED.json
```

The expected status is `CONTACT_CONSTANTS_AND_SCALAR_CONTROLS_PASS`.
The 54 exact tensor-grid checks certify a cleared polynomial identity
using its separate degree bounds. One rational tail fixture and a scalar
flat-crossing control check signs and normalization. They neither verify
the analytic reduction nor prove the missing flux inequality. See
[CONTACT_SOURCES.md](CONTACT_SOURCES.md) for dependencies and review scope.

The earlier result is a strict obstruction to ordering the heat coefficients
at arbitrary profile points:

For six equally weighted atoms at the vertices of the unit octahedron,
the injective contraction

\[
T=\operatorname{diag}(99/100,1/100,1/100)
\]

reverses the diffusion-coefficient ordering that a direct scalar heat
comparison proof of Gaussian majorisation would require. At variance one,
the ratio of target to source coefficients tends to a number **greater
than 1.007** as the retained volume tends to zero. Every pair of distinct
atoms strictly contracts. Both smoothed laws are strictly log-concave;
critical levels or coincident target atoms do not cause the obstruction.

This is an obstruction to a proposed proof mechanism. The example itself
obeys majorisation at every variance, by its elementary continuously
contracting diagonal motion. The unrestricted dimension-three conjecture
remains open, and no new Kneser--Poulsen class is claimed.

[PROOF.md](PROOF.md) derives the exact heat equation for the concentration
profile, the signed comparison equation, a stopped adjoint representation,
and the small-volume asymptotic used in the counterexample. Rearrangement
and parabolic concentration methods are classical; the specific strict
finite-atom obstruction is the contribution. Independent review is pending.

The same proof supplies global small-noise bounds for any finite atomic
law. If its support is K, its smallest weight is p_*, and rho_K(v) is the
radius for which |K+rho_K(v)B_3|=v, then

\[
 p_*Q_3(\rho_K(v)/\sqrt{s})\le1-L_\mu(s,v)
          \le N Q_3(\rho_K(v)/\sqrt{s}).
\]

Here Q_3 is the standard three-dimensional Gaussian radial tail. Although
every atomic profile tends to one as s tends to zero, the exponential rate
of its deficit retains the entire inverse tube-volume function. These
bounds quantify the known geometric bridge and expose the initial data
that a semigroup argument must retain.

The code is a compact exact audit of the geometric and numerical constants,
not a numerical PDE calculation or a proof assistant:

```sh
python3 audit.py --check EXPECTED.json
```

Python 3.11 or later, standard library only. It checks all 15 strict pair
inequalities, both curvature formulas through posterior covariance,
rational Taylor enclosures for two exponentials, and the cubed coefficient
ratio. It also checks the projection limit and the isometric and isotropic
controls. [EXPECTED.json](EXPECTED.json) contains small rational bounds.
No quadrature, random search, native solver, or large input is used.

The original note leaves an **integrated** comparison of the signed forcing
and boundary data. Its stopped representation is asserted only on regular
rectangles. The new contact reduction uses a continuous bulk flux and
different initial data; it does not extend that stochastic representation.
Pointwise coefficient ordering remains false, and the sign at ordered
contacts remains to be proved.

[SOURCES.md](SOURCES.md) records the primary literature and the latest team
dependencies, including the fixed-atom reduction and the previous failure
of instantaneous Hankel positivity along the spatial lift.
