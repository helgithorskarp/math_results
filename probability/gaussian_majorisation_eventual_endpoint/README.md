# Full Gaussian majorisation at sufficiently large variance

This author proof completes **every hinge threshold** at large variance
under a uniform positive spherical log-MGF gap. It joins the team's
explicit spherical-tail estimate to researcher 8's high-noise hinge
window; the thresholds overlap uniformly.

For an input supported in a radius-$R$ ball, a contraction $T$, and

\[
 J(\lambda)=\int_{S^2}\log
 \frac{\mathbb E e^{\lambda\theta\cdot X}}
      {\mathbb E e^{\lambda\theta\cdot T(X)}}\,d\sigma(\theta),
\]

the sufficient condition and endpoint are

\[
 \inf_{\lambda\geq1/(2R)}J(\lambda)\geq\kappa>0
 \quad\Longrightarrow\quad
 \mu*\gamma_s\preceq T_\#\mu*\gamma_s
 \quad\text{for }s\geq\max\{8,44/\kappa\}R^2.
\]

For finite noncongruent contracting pairs, strict spherical positivity
at every positive parameter suffices qualitatively, by the classical
strict mean-width theorem. An explicit martingale coupling certifying
convex order is one sufficient condition for that positivity.

There is also a concrete class with a quantitative endpoint. Let $\rho$
be any probability measure in the solid regular tetrahedron with vertices
$r(1,1,1)$, $r(1,-1,-1)$, $r(-1,1,-1)$, $r(-1,-1,1)$. Mix it with mass
$\alpha$ uniformly on the twelve difference vertices. Fix $\rho$ and
contract the difference vertices to the six corresponding axis vertices.
The resulting laws satisfy full majorisation for

\[
 s\geq352(150-99\alpha)r^2/\alpha,\qquad 0<\alpha\leq1.
\]

The background can be continuous or asymmetric. No dominant atom is
required. The written proof gives the contraction on the entire solid
tetrahedron and an explicit pointwise MGF bound uniform over the background.

The all-variance R3 conjecture remains open. **No new Kneser--Poulsen
consequence is claimed.** This is an analytic author proof, with exact
structural audits; independent review and formalization are pending.
See [PROOF.md](PROOF.md) and [SOURCES.md](SOURCES.md) for the complete
statements, dependencies, and relation to existing team classes.

## Reproduce

From the repository root, using CPython 3.11.2 and its standard library:

    python3 probability/gaussian_majorisation_eventual_endpoint/verify.py --check
    python3 -O probability/gaussian_majorisation_eventual_endpoint/verify.py --check

Both commands print:

    PASS c0b3660090073abc18950d1a2c4389b66db53c98f04227ea13ad90d4584b1a45

Without the flag, the checker prints [EXPECTED.json](EXPECTED.json).
From this directory, check the local manifest with:

    sha256sum -c SHA256SUMS

Every decision uses integers or exact rational arithmetic. The audit
checks 66 flap-pair and 48 anchor-flap distance losses, four Jensen
barycentric certificates, six martingale conditional distributions and
their marginals, two Laurent-polynomial MGF identities, a nonnegative
polynomial remainder, and the joining/variance constants. It uses no
spherical quadrature, random search, or external numerical packages.
Runtime is below one second; no large generated artifacts are required.

These are finite geometric and algebraic checks supporting the written
proof. They do not machine-check the two analytic dependencies or certify
the universal theorem by computation. Dependency versions and hashes
are recorded in SOURCES.md.
