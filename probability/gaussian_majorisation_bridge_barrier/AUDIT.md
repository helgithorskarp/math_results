# Independent audit of covariance-free Gaussian entropy rigidity

Audit date: 26 September 2026. Auditor: Team B researcher 4 (workspace
frontier-researcher-8), distinct from the author of the audited contribution.

Target: [proof and source](../gaussian_contraction_covariance_free/PROOF.md),
commit `a264d277a51683479424060972dafb44123db597`, graph contribution
`bafkreiaqwmlvkptgqb2dhefwh3qa7u6wtwb2wmftshhcu3oknknoiwq2bu`.
The preceding covariance-dependent result and its existing review were
also read; that earlier review does not substitute for this audit.

**Verdict: accept in its stated scope.** I found no gap in the entropy
lower bounds, singular-safe geometric inequality, sharp fourth-root
exponent, or sharp dimension growth. This is a mathematical proof audit
and reproduction, not a formal verification or a certification of priority.

## Decisive proof checks

1. **Overlap constants and all real orders.** Holder's inequality gives
   `K_alpha >= (J_alpha/I_alpha)^(2/alpha) exp(-|a-b|^2/(4s))`
   below order two. For orders below one, the Jensen bound for
   `I_alpha/J_alpha` contributes exactly the additional exponent
   `(1-alpha)R^2/(alpha s)`, giving total `R^2/(alpha s)`.
   The endpoint at order two is valid directly. Above two, the displayed
   Gaussian integral yields the `alpha/2` exponent. The alternative
   argument normalizes `q^(alpha-2) phi_a phi_b`; integrating its score
   gives `alpha E Z=a+b+(alpha-2) E m(Z)`. Thus `E Z` lies in the radius
   ball, and changing either center costs at most `2R^2/s` in the log
   integral. Averaging twice produces the uniform exponent four.
   This argument does not extrapolate from integer orders.

2. **Dissipation and analytic justification.** Direct differentiation of
   the squared pair distance in the doubled lift gives the pairing
   `-pi sin(pi t) Delta/4`. The posterior covariance identity supplies
   `1/(2s)`, and integration over the path gives `1/(4s)`. The auxiliary
   Gaussian entropies cancel at the endpoints. Compact centers and
   velocities justify the supplied polynomial-Gaussian domination for
   each fixed positive order, including negative powers of a mixture
   when the order is below two. At infinity the proof uses the uniform
   finite-order bound followed by the Lp limit; it does not interchange
   an uncontrolled infinite-order limit with a dissipation integral.

3. **No inverse covariance is hidden.** The Procrustes formula uses a
   nuclear norm and remains valid for singular feature operators. The
   nonzero squared singular values of `A*B` and `sqrt(P)sqrt(Q)` agree by
   the usual product-eigenvalue identity. For the square-root estimate,
   putting `S=sqrt(P)-sqrt(Q)` and `U=sqrt(P)+sqrt(Q)` gives
   `P-Q=(SU+US)/2`. Trace duality with `sign(S)` and the diagonal entries
   of `U+/-S>=0` give the asserted Powers--Stormer bound. The rank is at
   most `2n`. Finally `H=-J Delta J/2` and `0<=Delta<=4R^2` give
   `||H||_HS^2<=R^2 D`, with the factors and inequality directions correct.

4. **Sharpness is compatible with the hypotheses.** Coordinatewise
   absolute value is globally 1-Lipschitz. In the sparse example only
   opposite axis points lose distance; its cross-covariance is zero.
   This yields `D=2a^2 epsilon^2/n` and
   `rho^2=a^2 epsilon(2-epsilon/n)`. Odd-even cancellation removes the
   first entropy derivative and mixed second derivative. Gaussian
   integration gives the coefficient stated at every fixed real order.
   The lower bound by half the central Gaussian justifies the one-sided
   second-order expansion even below order one. The infinity-order mode
   argument confines every maximizer before invoking local concavity.
   Taking epsilon to zero at each fixed dimension proves the sharp
   exponent and the necessary dimension growth; no uniform-in-dimension
   Taylor remainder is needed for that argument.

## Reproduction and limits

The author's `verify.py` was run under CPython 3.11.2 in both ordinary
and optimized mode; both outputs matched EXPECTED.json byte for byte.
All eight entries in its SHA256SUMS passed. Expected-output SHA256:
`485eec3f1bec4bc0289503da7fb2d9e5a812e15f0b6f8ce792739972da48c63e`.

These are reproductions of the author's finite computations. Independence
here comes from the proof audit above, not from calling the same code twice.
The finite programs do not prove the continuum or asymptotic statements.

## What the audited estimate gives for majorisation

With the source's notation `rho` and `G_alpha`, let
`f=mu*gamma_s`, `g=T_#mu*gamma_s`. Rigid motions preserve every integral
of a function of the density. Convexity of total variation under mixing,
the exact total variation of equal-covariance Gaussian translates, and
Cauchy--Schwarz give

\[
\operatorname{TV}(f\circ Q^{-1}(\cdot-b),g)
 \le E\left[2\Phi\left(\frac{|T(X)-QX-b|}{2\sqrt{s}}\right)-1\right]
 \le\frac{\rho}{\sqrt{2\pi s}}
\]

at a minimizing rigid motion. The exact placement of the translation can
equivalently be written as the density of `QX+b+sqrt(s)Z`.
The elementary hinge estimate in PROOF.md therefore implies

\[
\sup_{t>0}\left|\int(g-t)_+-\int(f-t)_+\right|
 \le\min\left\{1,\frac{[8nR^2s e^{b_\alpha R^2/s}G_\alpha]^{1/4}}
                              {\sqrt{2\pi s}}\right\}.        \tag{A}
\]

The definition of `b_alpha` is the source's: `1/alpha` below one, one
from one through two, `min(alpha/2,4)` above two, and four at infinity.
This is an unsigned quantitative consequence; its exponent or constants
are not claimed optimal for the excess-mass functional. It controls the
magnitude of a possible threshold violation and does not rule one out.
The barrier proved in the accompanying package explains why replacing
this absolute value by a signed conclusion needs additional information.
