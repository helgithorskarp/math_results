# Heat evolution of concentration profiles: an exact comparison obstruction

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

The useful remaining route is an **integrated** comparison of the signed
forcing and boundary data in the profile equation. The pointwise coefficient
ordering cannot supply that route, even for this strict linear contraction.
The stopped representation is asserted only inside regions of regular
levels; a passage across arbitrary critical levels is not supplied.

[SOURCES.md](SOURCES.md) records the primary literature and the latest team
dependencies, including the fixed-atom reduction and the previous failure
of instantaneous Hankel positivity along the spatial lift.
