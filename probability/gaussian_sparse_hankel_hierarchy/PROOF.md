# A linear variance bound for every finite Hankel order

Complete analytic author proof, 26 September 2026. Independent review and
formalization are pending. The full three-dimensional Gaussian majorisation
conjecture remains open; no new Kneser--Poulsen consequence is asserted.

## 1. Statement: order three and a uniform sparse hierarchy

Let `mu` be a probability measure supported in `B(a,R)` in `R^3`, let `T`
be 1-Lipschitz, and let the Gaussian have covariance `s I_3`. Write

\[
 C=(2\pi s)^{-3/2},\quad f=\mu*\gamma_s,\quad
 g=(T_\#\mu)*\gamma_s,\quad
 H(u)=\int(g-Cu)_+-\int(f-Cu)_+,
\]
\[
 D=\mathbb E[|X-X'|^2-|T(X)-T(X')|^2],\qquad
 a_j=\int_0^1u^jH(u)\,du
 =\frac{C^{-(j+1)}(\int g^{j+2}-\int f^{j+2})}{(j+1)(j+2)}.
 \tag{1}
\]

**Theorem.** Let `N>=3` be an integer. If

\[
 \boxed{s\geq24N R^2,}
 \tag{2}
\]

then every polynomial `p` with at most `N` nonzero monomials satisfies

\[
 \boxed{\int_0^1p(u)^2H(u)\,du\geq0.}
 \tag{3}
\]

There is **no bound on the exponents**. If `D>0` and `p` is not zero,
the inequality is strict. In particular, for arbitrary distinct
nonnegative integers `k_1,...,k_N`, the matrix

\[
 (a_{k_i+k_j})_{i,j=1}^N
 \tag{4}
\]

is positive semidefinite, and positive definite if `D>0`.
Thus every principal `3 by 3` Hankel block is positive at `s>=72R^2`,
including blocks at arbitrarily large, unequal exponent spacings.
This is principal-block positivity; no assertion of all nonprincipal
minors or total positivity is intended.

For the usual consecutive matrix `H_ell=(a_(i+j))_(i,j=0)^ell`, (2)
becomes `s>=24(ell+1)R^2` for every `ell>=2`. This replaces the earlier
exponentially growing sufficient constants by a linear bound. The
previous much better order-two bound is preserved, not weakened.

For `R>0`, set

\[
 \epsilon=R^2/s,\quad \kappa=1-\epsilon,\quad
 \beta=5-1/\kappa,\quad
 L=\frac{(4-5\epsilon)^2}{32\epsilon(1-\epsilon)}.
 \tag{5}
\]

The proof gives the quantitative bound, under (2),

\[
 \boxed{\int_0^1p(u)^2H(u)\,du
 \geq\frac{D L^{3/2}e^{-(L+4)}}{512s\sqrt\pi}
           \int_{L/4}^{L/2}p(e^{-l})^2\,dl.}
 \tag{6}
\]

When `R=0` or `D=0`, every moment gap in (1) is zero, so (3)--(4)
hold with equality. Formula (6) is only asserted for `R>0`.

For the globally convex energy
`U_p(t)=integral_0^t(t-u)p(u)^2 du`, the energy density
`V_p(rho)=C U_p(rho/C)` has internal-energy gap equal to (3).
The theorem therefore covers a full cone of signed polynomial energies,
and its finite-order bound is uniform in their degrees.

## 2. Prior signed-window identity and a new global deficit bound

The preceding [signed-window proof](../gaussian_majorisation_high_noise_window/PROOF.md)
is an explicit dependency. We restate the formulas used and recheck the
estimate needed for the entire tail. Its proof uses the six-dimensional
lift `Z_t=(sqrt(1-t)X,sqrt(t)T(X))`, centered so that `|Z_t|<=R`.
For `K_x(z)=exp(-|z-Z_t(x)|^2/(2s))`, put

\[
 Q_t=\mathbb E K_X,\quad V_t=-\log Q_t,\quad
 h_t=\frac{\mathbb E[\Delta_{12}K_{X_1}K_{X_2}]}{Q_t^2},
 \qquad C_6=(2\pi s)^{-3}.
\]

At the unique mode `z_*(t)`, let `v_*(t)=V_t(z_*(t))`. For `epsilon<1`,
posterior differentiation gives

\[
 \frac\kappa sI\preceq\nabla^2V_t\preceq\frac1sI,
 \quad |z_*|\leq R,\quad 0\leq v_*\leq\epsilon/2,
 \quad |\nabla\log h_t|\leq4R/s\quad(D>0).
 \tag{7}
\]

On the level `V_t(z_*+rtheta)=v_*+v`,
`kappa r^2/(2s)<=v<=r^2/(2s)` and
`kappa r/s<=(V_t)_r<=r/s`. Define the weighted coarea density

\[
 A_t(v_*+v)=\int_{S^5}\frac{h_t(z_*+r\theta)r^5}{(V_t)_r}\,d\theta,
\]

zero below the mode. The signed window proof establishes the exact identity

\[
 H(e^{-l})=\frac{C_6e^{-l}}{4s}\int_0^1F_t(l)\,dt,
 \qquad
 F_t(l)=\frac1{\sqrt\pi}\int_{v_*}^l
                         \frac{A_t'(w)}{\sqrt{l-w}}\,dw,
 \tag{8}
\]

where `F_t=0` if `l<=v_*`. In particular `H(e^-l)>=0` for `0<=l<=L`.
The mode boundary value is zero, with `A_t(v_*+v)=O(v^2)`, and polynomial
growth bounds justify the Laplace-transform inversion and moment uniqueness.
These identities are prior results, not new claims of this package.

The same proof's quantitative window estimate, with
`B=D/(12s sqrt(pi))` and `q_l=4sqrt(2epsilon l/kappa)`, is

\[
 H(e^{-l})\geq B e^{-l}e^{-5\epsilon-q_l}
                   (\beta-q_l)(l-\epsilon/2)^{3/2}
 \quad(\epsilon/2\leq l\leq L).
 \tag{9}
\]

We also need an absolute tail bound **proportional to D**, rather than
to an unconditional radius bound. Removing the common Gaussian factor
from `Q_t` shows that its one-point exponential expectation is at least
`exp(-|z|R/s-epsilon/2)`, whereas the weighted two-point numerator is
at most `D exp(2|z|R/s)`. Consequently

\[
 h_t(z_*+r\theta)\leq D e^{4Rr/s+5\epsilon}.
 \tag{10}
\]

Put `gamma=5+1/kappa`. Differentiating the radial integrand of `A_t`,
using (7), gives the bound

\[
 |A_t'(v_*+v)|
 \leq\int_{S^5}\frac{h_t r^5}{(V_t)_r^2}
                    \left(\frac{4R}{s}+\frac\gamma r\right)d\theta.
\]

Since `r^2<=2sv/kappa` and the area of `S^5` is `pi^3`, (10) implies

\[
 C_6|A_t'(v_*+v)|
 \leq \frac{D}{4\kappa^3}e^{5\epsilon+q_v}(q_v+\gamma)v.
\]

For `0<=v<=l-v_*`, replace `q_v` by `q_l` and use
`integral_0^W v/sqrt(W-v)dv=4W^(3/2)/3`. Equation (8) proves

\[
 \boxed{|H(e^{-l})|\leq
 B\kappa^{-3}e^{-l}e^{5\epsilon+q_l}(q_l+\gamma)l^{3/2}
 \quad(l\geq0).}
 \tag{11}
\]

All estimates are uniform in the lift time and all input laws with the
given radius. The formula (8) already has justified integration; (11)
is only an upper estimate and does not introduce an unproved sign at
large levels. The proportionality to `D` is essential near rigid equality.

## 3. A one-sided sparse interpolation bound

We prove the precise elementary Remez-type estimate used below. No
approximation-theory theorem is imported as an unproved premise.

Let `P(l)=sum_(i=1)^N c_i exp(-k_i l)` with distinct `k_i>=0`, and fix
`L>0`. Set `h=L/(4N)` and

\[
 I_P=\int_{L/4}^{L/2}|P(l)|^2\,dl.
\]

**Lemma.** If `N>=2`, then for every `l>=L`,

\[
 |P(l)|^2\leq\frac{16N}{L}
          \left(\frac{16 e l}{L}\right)^{2(N-1)}I_P.
 \tag{12}
\]

Zero coefficients are permitted, so it also covers fewer than `N` terms.

**Proof.** Averaging over `l_0 in [L/4,L/4+h]` gives a choice with

\[
 \sum_{j=0}^{N-1}|P(l_0+jh)|^2\leq I_P/h.
 \tag{13}
\]

Let `x_i=exp(-k_i h)` in `(0,1]` and `tau=(l-l_0)/h>=N-1`.
Interpolate the function `x^tau` at the `N` nodes by a polynomial
`r_tau(x)=sum_(j=0)^(N-1) r_j x^j`. Its Newton divided difference of
order `j` is between zero and `binom(tau,j)`, by the derivative formula
and the mean-value theorem for divided differences on `[0,1]`.
The coefficient sum of `product_(i=1)^j(x-x_i)` is at most `2^j` in
absolute value. Therefore

\[
 \sum_{j=0}^{N-1}|r_j|
 \leq\sum_{j=0}^{N-1}2^j\binom\tau j
 \leq 2\frac{(2\tau)^{N-1}}{(N-1)!}
 \leq2\left(\frac{2e\tau}{N-1}\right)^{N-1}.
 \tag{14}
\]

For the middle estimate use `binom(tau,j)<=tau^j/j!`; successive terms
of the resulting sum grow by at least a factor two for `j<N-1`.
The final estimate follows from `n!>=(n/e)^n`, obtained by integrating
`log x` below its increasing integer sum. No separation of the nodes
is needed; the bound stays uniform when the exponents nearly coincide.

The interpolation identities at the nodes give

\[
 P(l)=\sum_{j=0}^{N-1}r_jP(l_0+jh).
\]

Use (13)--(14), `tau<=l/h=4Nl/L`, and `N/(N-1)<=2`. Squaring yields
`4(16el/L)^(2(N-1)) I_P/h`, which is (12). QED.

The argument is one-sided: the nonnegative exponents make the nodes lie
in `[0,1]`, and evaluation is later than the sampling interval. It is
not an exponent-free two-sided continuation principle. Related Remez
inequalities for Müntz polynomials are established literature; see
[SOURCES.md](SOURCES.md). No priority is claimed for this elementary device.

## 4. The positive window dominates the entire tail

Assume `D>0`, `R>0`, `N>=3` and (2). Then

\[
 \epsilon\leq\frac1{24N}<\frac1{16},\qquad
 L=\frac1{2\epsilon}-\frac34+\frac{\epsilon}{32(1-\epsilon)}
 \geq11N.
 \tag{15}
\]

Let `P(l)=p(e^-l)` and `I_P` be as above. On `L/4<=l<=L/2`, we have
`q_l<=beta/sqrt(2)<3`, `beta>=59/15`, and
`beta-q_l>=beta(1-1/sqrt(2))>3/4`. Also
`5epsilon+q_l<4` and `l-epsilon/2>=l/2`. Since `2sqrt(2)<3`, (9) gives

\[
 H(e^{-l})\geq\frac{Be^{-4}}4 e^{-l}l^{3/2}.
\]

Consequently the contribution of this interval to the desired integral is

\[
 J_+:=\int_{L/4}^{L/2}P(l)^2H(e^{-l})e^{-l}\,dl
 \geq\frac{Be^{-4}}{32}L^{3/2}e^{-L}I_P.
 \tag{16}
\]

Every other contribution with `0<=l<=L` is nonnegative. It remains to
bound the possible negative contribution on `l>L`.
Write `v=l-L`. The identities in (5) imply `q_L=beta<=4`. The elementary
bound `sqrt(1+x)<=1+x/2` gives

\[
 q_l\leq4+2v/L,\qquad q_l+\gamma\leq11(1+v/L).
\]

Moreover `kappa^(-3)<2` and `5epsilon<1`. Combining (11) and (12),
and collecting powers of `l/L`, gives

\[
 \begin{aligned}
 J_-&:=\int_L^\infty P(l)^2|H(e^{-l})|e^{-l}\,dl\\
 &\leq352N Be^5 L^{1/2}(16e)^{2(N-1)}e^{-2L}I_P
 \int_0^\infty(1+v/L)^{2N+1/2}e^{-(2-2/L)v}\,dv.
 \end{aligned}
 \tag{17}
\]

Using `log(1+x)<=x`, the last integral is at most
`[2-(2N+5/2)/L]^(-1)<=1`, since `L>=11N`. The ratio of the bound in
(17) to the lower bound in (16) is therefore at most

\[
 11264\,\frac NL e^9(16e)^{2(N-1)}e^{-L}
 \leq 2^{8N+2}e^{7-9N}
 =2^{26}e^{-20}(256e^{-9})^{N-3}<\frac14.
 \tag{18}
\]

The last strict estimate has a short exact certificate: `e>8/3`,
`2^32>3^20`, and `256(3/8)^9<1` give
`2^26 e^-20<3^20/2^34<1/4` and `256e^-9<1`.
Thus at least three quarters of the lower bound (16) survives after
subtracting the **entire** absolute tail. Substituting
`B=D/(12s sqrt(pi))` gives (6).

A nonzero polynomial cannot vanish on the whole interval
`[exp(-L/2),exp(-L/4)]`, so `I_P>0`. This proves strictness, (3), and (4).
The zero-deficit case follows from the nonnegative replica representation
in the earlier [replica-curvature proof](../gaussian_replica_curvature_sparse_energies/PROOF.md).
That representation also covers `R=0`.

## 5. What has and has not been bridged

The previously established order-two Hankel signs alone do not imply
order-three positivity. The additional information here is the signed
hinge window plus a global tail estimate proportional to the same deficit,
and a sparsity estimate preventing a short polynomial from concentrating
enough in that tail. The first uncontrolled `3 by 3` block is now positive
at the stated variance, uniformly over exponent choices.

More generally, a negative square-curvature polynomial certificate at
`s>=72R^2` must have strictly more than `s/(24R^2)` monomials in its square
root polynomial. This is a necessary witness-complexity condition, not a
counterexample construction or a claim of optimal dependence.

The variance condition still grows with matrix size. Thus no finite
variance is proved to satisfy every Hankel level by this result. The
equivalence between all levels and full majorisation cannot be replaced
by an exchange of the quantifiers in (2). The theorem also does not assert
the comparison of every polynomial merely convex on the attained density
interval; its stated energy cone consists of square curvatures and their
nonnegative sums. In particular no all-threshold or small-variance
hypothesis needed for a new Kneser--Poulsen implication has been supplied.

The universal claim is analytic. The exact checker audits interpolation,
constants, and selected finite Gaussian Hankel blocks, including widely
spaced indices and a near-isometric contraction. Finite checks are not
a proof by sampling or independent peer review.
