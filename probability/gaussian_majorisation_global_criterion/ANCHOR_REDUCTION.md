# A fixed-atom reduction of the full Gaussian majorisation question

Status: complete author proof; independent mathematical review is pending.
This is a reduction of the full question, not a proof of majorisation and
not a construction of a counterexample. The separation estimate is uniform
over every hinge threshold. Its purpose is to identify a sufficient local
endpoint problem with exactly the strength of the unrestricted conjecture.

Write `gamma_s` for the centred Gaussian density with covariance `s I_3`,
`H_f(a)=integral(f-a)_+`, and

\[
\Delta(f,g)=\sup_{a\ge0}(H_f(a)-H_g(a))_+.
\]

By [the global criterion](PROOF.md), this is also the minimum failure
probability of the corresponding five-dimensional endpoint density-value
coupling. No coupling of the underlying labelled centres is assumed.

## 1. The local-to-global statement

Fix any number `epsilon_0` strictly between zero and one, however small.
The following statements are equivalent:

1. Every bounded probability measure in `R^3` and every 1-Lipschitz image
   obey Gaussian majorisation at every positive variance.
2. At variance **one**, the comparison holds for every bounded law of the
   form `mu=(1-epsilon_0) delta_0+epsilon_0 rho` and every 1-Lipschitz map
   `T` on its support with `T(0)=0`.

The probability `rho` and its bounded support are arbitrary. In particular
the bound on its support is not required to be uniform over this class.
This displayed mixture condition is exactly `mu({0})>=1-epsilon_0`.
The equivalence still holds if one further requires `rho({0})=0`, so the
fixed atom has mass exactly `1-epsilon_0`: the construction below meets
this stronger restriction. One fixed contamination fraction and one fixed
variance suffice; the assertion is **not** that statement 2 is proved.

The nontrivial implication follows from the quantitative construction below.
Every possible violation can be transferred to this test class, preserving
its sign. Rescaling space fixes the original variance to one.

## 2. A contractive extension with a distant fixed atom

Let `K` be the compact support of a bounded law `mu`, let `T:K -> R^3`
be 1-Lipschitz, and put `f=mu*gamma_s`, `g=(T#mu)*gamma_s`. Choose a unit
vector `e`, a number `eta>0`, and a scalar `L` large enough that

\[
e\cdot(Tx+Le-x)\ge\eta\quad(x\in K).
\tag{A1}
\]

Boundedness makes this possible. Set `y(x)=Tx+Le`, and define the finite
constants

\[
D=\sup_{x\in K}(|y(x)|^2-|x|^2),\qquad
M=\max\{\sup_{x\in K}e\cdot x,\sup_{x\in K}e\cdot y(x)\}.
\]

For sufficiently large `R`, let `z_R=R e` and extend the labelled map by

\[
\widehat T_R(x)=y(x)\ (x\in K),\qquad
\widehat T_R(z_R)=z_R.
\tag{A2}
\]

Choose `R>max(M,0)` and `2R eta>D`. The new point is outside both old supports,
and every pair with that point strictly contracts, because

\[
|z_R-x|^2-|z_R-y(x)|^2
=2R e\cdot(y(x)-x)-(|y(x)|^2-|x|^2)
\ge2R\eta-D>0.
\tag{A3}
\]

All old pair distances still contract: the output translation changes none
of them. Thus (A2) is a genuine 1-Lipschitz map on the enlarged support,
and has a global extension by the usual Kirszbraun theorem. The output
translation is essential to this general construction; simply adjoining
the same distant fixed point need not be contractive.

For `0<epsilon<1`, put

\[
\mu_{R,\epsilon}=(1-\epsilon)\delta_{z_R}+\epsilon\mu,
\qquad
\nu_{R,\epsilon}=\widehat T_{R\#}\mu_{R,\epsilon}.
\]

Their smoothed densities are

\[
F_{R,\epsilon}=h_R+\epsilon f,\qquad
G_{R,\epsilon}=h_R+\epsilon g(\,\cdot-Le),\qquad
h_R=(1-\epsilon)\gamma_s(\,\cdot-z_R).
\tag{A4}
\]

Both input and output give the fixed atom exactly the displayed mass.
Common translation by `-z_R` puts that atom at zero and does not alter any
hinge or contraction inequality.

## 3. An error bound uniform over all thresholds

Let `Q(t)=Pr{N(0,1)>t}` and set

\[
\beta_R=Q\!\left(\frac{R-M}{2\sqrt{s}}\right)
\le \exp\!\left(-\frac{(R-M)^2}{8s}\right).
\tag{A5}
\]

**Theorem.** The construction above satisfies

\[
\sup_{a\ge0}\left|
H_{G_{R,\epsilon}}(a)-H_{F_{R,\epsilon}}(a)
-\epsilon\big[H_g(a/\epsilon)-H_f(a/\epsilon)\big]
\right|\le\beta_R.
\tag{A6}
\]

In particular

\[
\left|\Delta(F_{R,\epsilon},G_{R,\epsilon})
-\epsilon\Delta(f,g)\right|\le\beta_R,
\qquad
\lim_{R\to\infty}\Delta(F_{R,\epsilon},G_{R,\epsilon})
=\epsilon\Delta(f,g).
\tag{A7}
\]

This is an exact asymptotic transfer of the *whole* global criterion, not
an estimate restricted to a tail window.
For a base pair of zero defect, (A7) only gives an error tending to zero;
it does not prove zero defect after adjoining an atom at a finite distance.
In particular it does not settle arbitrary-weight Gaussian adjunction at
the origin of the team's original square-cone configuration.

**Proof.** For nonnegative numbers `u,v,a`, define the hinge interaction

\[
J_a(u,v)=(u+v-a)_+-(u-a)_+-(v-a)_+.
\]

The elementary cases `u>=a`, `v>=a`, and `u,v<a` give

\[
0\le J_a(u,v)\le\min(u,v).
\tag{A8}
\]

Consequently, for `k=epsilon f` or `epsilon g(. - Le)`,

\[
H_{h_R+k}(a)=H_{h_R}(a)+H_k(a)+I_k(a),
\qquad 0\le I_k(a)\le\int\min(h_R,k).
\tag{A9}
\]

Split space at the hyperplane `e.x=(R+M)/2`. On the lower side, integrate
`h_R`; its mass there is `(1-epsilon) beta_R`. On the upper side, integrate
`k`. Every Gaussian centre making up `k` has projection at most `M`, so
this mass is at most `epsilon beta_R`. Tonelli makes the same argument
valid for nonatomic bounded laws. Thus each overlap in (A9) is at most
`beta_R`. The difference of the two interaction errors has absolute value
at most `beta_R`, since both lie in `[0,beta_R]`; a factor of two is not
needed. The common hinge cancels and
`H_(epsilon f)(a)=epsilon H_f(a/epsilon)`, proving (A6).
Taking suprema and positive parts gives (A7). The bound in (A5) is the
elementary Gaussian Chernoff estimate, obtained by applying Markov's
inequality to `exp(t N)` and optimizing at `t=(R-M)/(2 sqrt(s))`. QED.

If `H_f(a_*)-H_g(a_*)=delta>0`, choose `R` also so large that

\[
R-M\ge\sqrt{8s\log\frac{2}{\epsilon\delta}}.
\tag{A10}
\]

Then the transferred pair has

\[
H_{F_{R,\epsilon}}(\epsilon a_*)
-H_{G_{R,\epsilon}}(\epsilon a_*)\ge\frac{\epsilon\delta}{2}>0.
\tag{A11}
\]

This proves the implication from statement 2 to statement 1 in Section 1.
For a general starting variance, scaling every centre by `1/sqrt(s)`
first reduces it to variance one; thresholds transform by the density
Jacobian. No hypothetical violation is supplied or presumed to exist.

## 4. How close to a Gaussian a possible violation can be

Suppose, conditionally, that one violating pair exists. Keep this pair,
`s`, `e`, `L`, and `delta` fixed while letting `epsilon` tend to zero.
Equations (A3) and (A10) permit

\[
R_\epsilon=O\!\left(1+\sqrt{\log(1/\epsilon)}\right).
\tag{A12}
\]

Translate both endpoints by `-R_epsilon e`, putting the common fixed atom
at zero. Denote the resulting laws by `bar mu_epsilon,bar nu_epsilon`,
and their densities by `bar F_epsilon,bar G_epsilon`.
Every pair still violates a hinge by (A11), while the following all hold:

* Both laws have mass `1-epsilon` at zero. Their Gaussian convolutions
  have total variation distance at most `epsilon` from `gamma_s`.
* For every fixed finite `p>=1`, both input laws tend to `delta_0` in
  `W_p`. The same coupling proves that both smoothed laws tend to
  `gamma_s` in `W_p`.
* For every fixed multi-index `alpha`, the Gaussian-smoothed densities
  converge to `gamma_s` in the uniform norm of the derivative `D^alpha`,
  and also in the `L1` norm of that derivative.
* Both relative entropies `D(bar F_epsilon || gamma_s)` and
  `D(bar G_epsilon || gamma_s)` tend to zero, and their differential
  entropy gap tends to zero.

Here are quantitative proofs and their limits. If the old input and
translated output centres lie in `B(0,K_0)`, then

\[
W_p(\bar\mu_\epsilon,\delta_0)^p,
W_p(\bar\nu_\epsilon,\delta_0)^p
\le\epsilon(R_\epsilon+K_0)^p\longrightarrow0.
\tag{A13}
\]

Couple the same Gaussian noise on both sides to get the smoothed bound.
The density differences from `gamma_s` are `epsilon` times a difference
of two Gaussian mixtures, so for either the `L1` or uniform norm,

\[
\|D^\alpha(\bar F_\epsilon-\gamma_s)\|
\le2\epsilon\|D^\alpha\gamma_s\|,
\tag{A14}
\]

and likewise for `bar G_epsilon`. This is convergence for every fixed
derivative order, not a bound uniform in that order.
Convexity of relative entropy in its first argument and the exact
Gaussian translation formula give

\[
D(\bar F_\epsilon\Vert\gamma_s),\quad
D(\bar G_\epsilon\Vert\gamma_s)
\le\frac{\epsilon(R_\epsilon+K_0)^2}{2s}
\longrightarrow0.
\tag{A15}
\]

For completeness, writing `h` for differential entropy and
`b(epsilon)=-epsilon log epsilon-(1-epsilon)log(1-epsilon)`, the usual
mixture identity gives

\[
|h(\bar F_\epsilon)-h(\bar G_\epsilon)|
\le\epsilon|h(f)-h(g)|+b(\epsilon)\longrightarrow0.
\tag{A16}
\]

Indeed attach the Bernoulli component label. Its mutual information with
the observation lies between zero and `b(epsilon)`, and the two endpoints
have the same component masses and the same Gaussian-component entropy.
Translations do not change the other component entropies. Bounded-centre
Gaussian mixtures have finite entropies, so every term is well defined.
These are standard mixture facts, proved here to make the reduction's
normalizations explicit, not claimed as new entropy inequalities.

Thus a theorem proving zero defect for **all** contraction pairs in one
fixed sufficiently small neighbourhood described by any finite collection
of these bounds would resolve the full conjecture. The construction does
not furnish counterexamples in such a neighbourhood unless there already
is a counterexample to the conjecture. It also gives no uniform support
radius at the fixed variance: the rare support moves to infinity in (A12).

## 5. A bounded-support normalization and the team obligation

There is an equivalent version with both supports in the unit ball.
Divide the centred supports in Section 4 by
`d_epsilon=R_epsilon+K_0`, with `K_0` enlarged if necessary to be positive.
Use Gaussian variance `s_epsilon=s/d_epsilon^2`. Then both supports are
in `B(0,1)`, and the map fixes zero and satisfies

\[
\sup_{x\in\operatorname{supp}\mu_\epsilon}
|T_\epsilon x-x|
\le\frac{\sup_{x\in K}|Tx+Le-x|}{d_\epsilon}
\longrightarrow0.
\tag{A17}
\]

The defect is unchanged by this common spatial scaling. The violating
threshold becomes `epsilon a_* d_epsilon^3`, and
`s_epsilon -> 0`. Equation (A17) concerns displacement on the support,
not a small Lipschitz constant for `T_epsilon-I`.

This specifies two equivalent positive obligations for the analytic lane:
prove the fixed-atom test class of Section 1 at one variance **uniformly
over its bounded supports**, or prove the corresponding statement with
uniformly bounded support across the small-variance regime. A fixed-law
continuity estimate is not the needed quantifier.

The [bounded-law stability theorem](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md)
now identifies the exact interior of the full-comparison set in the
product `W_infinity` topology: strict mean-support and peak gaps, and
strict hinges below the target peak. It extends the earlier
[spatial-cloud theorem](../gaussian_majorisation_open_stability/PROOF.md)
and gives finite sufficient moment certificates when signed threshold
endpoints and a strict localization margin are supplied. At fixed `s`,
(A12) is not a small `W_infinity` perturbation of the atom. Under the
unit-ball normalization, the variance tends to zero. The Dirac comparison
itself is equality and is not an interior point. Thus that positive
theorem and the present conditional negative transfer have different,
explicit quantifiers; neither supplies the missing sign for the other.

The [paired-layer completion](../gaussian_paired_layers_majorisation/ALL_VARIANCES.md)
and the [geometric motion classes](DEPENDENCIES.md) retain all their
proved comparisons. They are not claimed to contain the arbitrary rare
packet in (A2). The recent
[strong-composition obstruction](../gaussian_axial_cone_rotations/COMPOSITIONS.md)
also concerns labelled centre motions, not this endpoint reduction.
The newer [axial robustness theorem](../gaussian_axial_cone_rotations/ROBUSTNESS.md)
does allow arbitrary weights, variances and individual radii throughout
its uniformly distorted domains, with a reserved amount of target
scaling. Its geometric hypotheses provide a sufficient zero-defect
certificate even for rare atoms in those domains. They do not encompass
an arbitrary packet and contraction in (A2). No claim of an all-weight
limitation is made for that motion-based class.

The [covariance-free entropy result](../gaussian_contraction_covariance_free/PROOF.md)
and its [independent acceptance and unsigned bridge](../gaussian_majorisation_bridge_barrier/AUDIT.md)
are retained. That audit accepts the covariance-free theorem; it does
not review the present reduction. Equations (A11)--(A16) show conditionally why small entropy
and unsigned closeness cannot automatically supply the missing exact sign:
a uniform assertion of that kind on the contraction class would already
be a proof of the full problem. This is an exact reduction to the global
criterion, not another counterexample to a proposed tail estimate.
No new Kneser--Poulsen class follows from this reduction alone.

## Reproduction, attribution and limits

From this directory with CPython 3.11 or later, standard library only:

```sh
python3 anchor_audit.py --check
python3 -O anchor_audit.py --check
sha256sum -c SHA256SUMS
```

Expected in both normal and optimized CPython 3.11.2:

```text
FIXED_ATOM_REDUCTION_EXACT_AUDITS_PASS 218fbb2cbe4e4163e93bd58d5422e023f382e110c381470ab7079061d84c44dd
```

The [checker](anchor_audit.py) audits the scalar hinge interaction, exact
disjoint-mixture normalization and an explicit contractive anchor extension
using rational arithmetic. Its deliberately negative finite-cell control
is **not** Gaussian data or a contraction counterexample. Invalid
parameter and extension controls are rejected. [ANCHOR_EXPECTED.json](ANCHOR_EXPECTED.json)
is the deterministic compact report. These checks supplement the written
universal proof; they are not independent review or numerical evidence for
a negative Gaussian hinge.
The report covers 729 rational scalar triples, six disjoint-mixture
controls, 81 overlapping-mixture pairs at all 448 piecewise-linear knots,
three rational anchor distances, and four invalid controls. A privately
altered expected report is rejected under `python -O`.

The original problem and the interpretation of full majorisation come from
[Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
The prior [finite strict rational reduction](../gaussian_majorisation_rank_abel/PROOF.md)
can be combined with this construction when a finite witness is wanted:
one additional atom suffices, and rational choices of the translation,
anchor, contamination fraction and threshold preserve rational data.
Choosing a larger rational anchor enforces the strict inequalities and
the required overlap margin. The present proof does not require a finite
input, a finite certificate for the hypothetical initial violation, or any
unpublished numerical computation. The elementary separated-mixture,
Gaussian-tail, and entropy ingredients carry no historical-priority claim.
