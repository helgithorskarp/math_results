# Uniform moment budgets for the unrestricted Gaussian defect

Author proof, 26 September 2026; independent review is pending. This connects
the existing finite-atomic localization to the existing moment criterion,
including their equality and zero-weight boundaries. It supplies a uniform
**absolute-error** budget, not the missing sign of any unrestricted Gaussian
comparison. It gives no new positive class or Kneser--Poulsen case.

The concurrent [analytic handoff, Section 4](../gaussian_majorisation_global_criterion/INTERFACES.md)
already gives this compact moment formulation and an explicit diagonal
with error below 5/k and degree of order k^16. That reduction and its
quantifiers are credited there. The new analytic input here is the global
support modulus (U1)--(U3), reducing the sufficient degree to order k^8
at the same accuracy scale. No priority is claimed for the compact moment
formulation or its equivalence to the full question.

The [strict certificate](CERTIFICATE_INTERFACE.md) remains the interface for
proving an individual comparison exactly. The interface here instead bounds
the worst possible defect over all bounded laws, maps, and variances, using
one explicit compact finite moment problem for each requested precision.

## 1. A global modulus with the support radius as its only law input

Let f=mu*gamma_s and g=nu*gamma_s for arbitrary bounded probability laws
on R3, with covariance s I3, s>0. A map between the laws is not required
in this section. Suppose their supports fit, after separate translations,
in radius-R balls. Write

\[
 C=(2\pi s)^{-3/2},\quad r=R/\sqrt{s},\quad
 H(u)=\int(g-Cu)_+-\int(f-Cu)_+\quad(0\le u\le1).
\]

For 0<t<=1 define

\[
 \omega_r(t)=\frac{\sqrt{2/\pi}}3
       \int_0^t[r+\sqrt{2\log(1/v)}]^3\,dv,
 \qquad \omega_r(0)=0.                                  \tag{U1}
\]

**Lemma 1.** The function omega_r is increasing and concave on [0,1],
is continuous at zero, and

\[
 |H(u)-H(v)|\le\omega_r(|u-v|),\qquad
 \omega_r(t)\le\frac t3
       [r+\sqrt{2\log(1/t)}+2]^3.                        \tag{U2}
\]

**Proof.** A translated support in B(0,R) gives
f(x)/C<=exp(-((|x|-R)_+)^2/(2s)). Hence its superlevel volume V_f(Cv)
is at most (4 pi/3)[R+sqrt(2s log(1/v))]^3. The same bound holds for g.
Both volumes lie between zero and this bound, so their difference is
bounded by **one** copy of it. Layer cake consequently gives

\[
 |H(u)-H(v)|\le\frac{\sqrt{2/\pi}}3
    \int_v^u[r+\sqrt{2\log(1/t)}]^3dt\quad(v<u).
\]

The integrand decreases in t. Its integral over [v,u] is at most its
integral over [0,u-v], proving the modulus. It is integrable at zero;
its monotonicity also proves concavity of omega_r. No differentiability
of level surfaces or regular-value assumption enters.

For the explicit bound put q=sqrt(2 log(1/t)) and let Z have the exponential
law of mean one. Substitution v=t exp(-z) gives

\[
 \omega_r(t)=\frac{\sqrt{2/\pi}}3\,t\,
          \mathbb E\bigl[(r+\sqrt{q^2+2Z})^3\bigr].
\]

Since sqrt(q^2+2Z)<=q+sqrt(2Z), expand the latter cube. The elementary
Gaussian integrals give

\[
 \mathbb E\sqrt{2Z}=\sqrt{\pi/2}<2,\quad
 \mathbb E(2Z)=2\le4,\quad
 \mathbb E(2Z)^{3/2}=3\sqrt{2\pi}/2<8.
\]

The inequalities use 2<pi<4. Coefficientwise comparison with (r+q+2)^3
and sqrt(2/pi)<1 proves (U2). The same argument covers t=1 and r=0.
The value at t=0 follows by the limit. QED.

## 2. Uniform truncation of the integrated moment criterion

Use the normalized moments and beta averages from the
[global criterion](../gaussian_majorisation_global_criterion/PROOF.md)
and [input contract](CERTIFICATE_INTERFACE.md):

\[
 A_m(f)=C^{1-m}\int f^m,\quad
 a_j=\frac{A_{j+2}(g)-A_{j+2}(f)}{(j+1)(j+2)},
\]
\[
 b_{N,j}=(N+1){N\choose j}\sum_{l=0}^{N-j}
           (-1)^l{N-j\choose l}a_{j+l}
        =\mathbb E H(\operatorname{Beta}(j+1,N-j+1)),
\]
\[
 D_N=\max(0,-\min_{0\le j\le N}b_{N,j}),\qquad
 \Delta=\max_{0\le u\le1}(-H(u))_+.
\]

**Theorem 2.** For every N>=0, putting rho_N=(N+2)^(-1/2),

\[
 0\le\Delta-D_N\le\omega_r(\rho_N)
 \le \frac{[r+\sqrt{\log(N+2)}+2]^3}{3\sqrt{N+2}}.    \tag{U3}
\]

The error is uniform over all such law pairs. In particular it is valid
at isometries, point laws, zero-weight limits and collisions of atoms.
There is no least-weight, signed-tail, peak-gap or interior hypothesis.

**Proof.** Reuse the classical Bernstein--Durrmeyer kernel: for each u
take J~Bin(N,u), then V conditional on J with law Beta(J+1,N-J+1).
Its expectation of H is a convex combination of the b_(N,j), hence at
least -D_N. The already derived exact second moment is

\[
 \mathbb E(V-u)^2=
 \frac{2[1+(N-3)u(1-u)]}{(N+2)(N+3)}\le\frac1{N+2}.   \tag{U4}
\]

For completeness, use E J=Nu and E J^2=Nu(1-u)+N^2u^2 with the beta
moments E(V|J)=(J+1)/(N+2) and
E(V^2|J)=(J+1)(J+2)/((N+2)(N+3)). For N<=3 the numerator is at most
2, and for N>=3 it is at most (N+1)/2; both imply (U4).

Concavity and monotonicity of omega_r, followed by Cauchy--Schwarz, give

\[
 |\mathbb EH(V)-H(u)|\le\mathbb E\omega_r(|V-u|)
 \le\omega_r(\mathbb E|V-u|)\le\omega_r(\rho_N).
\]

This proves the upper bound on Delta. Every beta average is at least
-Delta, proving the lower bound. Equation (U2) gives the final explicit
expression. QED.

For fixed r the bound is O(N^(-1/2)(log N)^(3/2)), with the displayed
constant valid at every degree. This is a uniform alternative to the
older global Holder bound; no priority is claimed for positive-operator
approximation or use of concave moduli. The previous local O(N^(-1/2))
certificate on a fixed positive threshold window keeps its separate
signed endpoint hypotheses and can be more useful for exact positivity.

## 3. One diagonal finite moment problem approximates the full question

Let D be the supremum of the hinge defect over all bounded input laws
and contractions in R3 and all positive variances. Common spatial scaling
fixes the variance to one. The full question is D=0.

Use **exactly** the measure lane's compact parameter set K_k from
[DEFECT_LOCALIZATION.md](../gaussian_prior_localization/DEFECT_LOCALIZATION.md):
for an integer k>=1 there are n_k=k^6 sites, weights w_i>=0 summing to one,

\[
 x_1=y_1=0,\quad |x_i|,|y_i|\le2k,\quad
 |y_i-y_j|\le|x_i-x_j|\quad\hbox{for every }i,j.         \tag{U5}
\]

Repeated sites and zero weights are allowed. Coincident source sites have
coincident images. K_k includes all the sites and weights, but the threshold
has been integrated out into the moments. Set

\[
 N_k=2^{16}k^8-2,\qquad
 B_k=\max_{Q\in K_k}\max_{0\le j\le N_k}(-b_{N_k,j}(Q))_+.
                                                               \tag{U6}
\]

**Corollary 3 (refined degree for the existing interface).** These maxima exist,
B_k is nondecreasing, and

\[
 0\le D-B_k<\frac{14}{3k}<\frac5k.                       \tag{U7}
\]

Only normalized Gaussian powers through **2^16 k^8** occur in B_k. Thus

\[
 D=0\quad\Longleftrightarrow\quad
 B_k=0\text{ for every integer }k\ge1.
                                                               \tag{U8}
\]

This is a diagonal hierarchy with an explicit error, not a finite cutoff
for the full question. Its terms are still maxima over continuous
geometric and weight parameters.

**Proof.** The credited localization theorem gives compact attained D_k
on (U5), with 0<=D-D_k<4/k. At variance one, r=2k. Choose the degree in
(U6). Then rho=1/(256 k^4), and

\[
 q^2=2\log(1/\rho)=16\log2+8\log k
 \le8k+8\le16k^2.                                      \tag{U9}
\]

Here log 2<1, log k<=k-1, and
16k^2-8k-8=8(k-1)(2k+1)>=0. Hence q<=4k and r+q+2<=8k.
Equations (U2)--(U3) imply, uniformly on K_k,

\[
 0\le\Delta(Q)-D_{N_k}(Q)\le\frac{2}{3k}.                \tag{U10}
\]

Taking maxima gives B_k<=D_k<=B_k+2/(3k); combine with the existing
localization error. Gaussian replica moments are finite continuous
exponential sums on K_k, including its boundary, so the maxima in (U6)
exist. K_k embeds into K_(k+1) by adding zero-weight sites at zero. The
old degree-elevation identity

\[
 b_{N,j}=\frac{N+1-j}{N+2}b_{N+1,j}
              +\frac{j+1}{N+2}b_{N+1,j+1}
\]

shows that D_N increases with N. Thus B_k also increases. Its limit is
D by (U7), proving (U8). QED.

Two precise uses for the finite-atomic lane follow.

* Given a particular violation of size delta>0, every integer k>=10/delta
  has a configuration in (U5) and a beta index with b_(N_k,j)<-delta/2.
  This is conditional detection; it asserts no counterexample exists.
  It bounds the atom count, support radius and largest required power,
  but supplies neither a coordinate denominator nor an efficient evaluator.
* For a desired absolute tolerance 0<epsilon<=1, take
  k=ceil(10/epsilon). A **uniform** certificate
  b_(N_k,j)(Q)>=-epsilon/2 for every Q in K_k and every j yields
  D<epsilon/2+14/(3k)<=29 epsilon/30<epsilon.
  The tolerances must tend to zero to prove the full conjecture.

For fixed Q, interval enclosures [ell_j,u_j] imply

\[
 \max(0,-\min_j u_j)\le\Delta(Q)
 \le\min\{1,\max(0,-\min_j\ell_j)+2/(3k)\}.           \tag{U11}
\]

Every beta index of this row must be enclosed for the upper bound.
For a global upper bound on D, the lower bound must additionally cover
**every configuration** in K_k. Sampling parameters cannot establish it.
A single certified negative beta at a certified contraction does supply
a counterexample, by the already proved convex-energy interpretation.

## 4. Ownership, stability and trust boundaries

The law-uniform estimate (U3) is the functional lane's new analytic input.
The compact configurations and their spatial error are the measure lane's
existing result; their localization is not repeated or claimed here. The
moment identity and increasing beta defects are the analytic/transport
lane's existing results, as is the concurrent compact two-index maximum
and its degree-O(k^16) diagonal in the updated analytic handoff. The proof
above applies the sharper modulus to that same maximum. Evaluating or
bounding the signed exponential
sums, certifying contraction constraints, and covering parameter regions
remain finite-atomic obligations. Large alternating coefficients may make
even accurate individual moment intervals ineffective.

This interface also retains the old bounded-law transport control: Gaussian
L1 errors e_f,e_g change H, each beta average and each D_N by at most
e_f+e_g. For approximate individual inputs that budget adds directly to
(U11); it is not amplified through the alternating moment coefficients.
It does not justify a contraction after arbitrary independent rounding.

An isometric pair has H=0 and all beta averages zero. The present absolute
approximation includes these boundary pairs without asking for impossible
strict margins. It does **not** turn finitely many zero or positive beta
values into exact majorisation. The original signed-tail/peak/middle
certificate, its exact interior statement, and their source proofs remain
unchanged. The [common-set equality-face certificates](../gaussian_majorisation_minimax_faces/PROOF.md)
are useful finite-atomic controls, not a sign proof on all of K_k.

The new [heat-contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md)
and its unresolved posterior-covariance sign remain with the evolution
lane. No heat derivative, common-set optimization or extremal-map theorem
is used in (U1)--(U10). A subsequent rigid-mesh extension may add vertices,
so its complexity is not bounded by n_k here. The broad axial and ordered
classes remain the previously established positive benchmarks in
[HANDOFF.md](HANDOFF.md); the concurrent
[three-cap reflection theorem](../gaussian_disjoint_cap_reflections/PROOF.md)
is another geometric positive class with its own hypotheses. None is used
as a proof premise here. No arbitrary-mixture closure or new class follows.

The error is absolute at normalized variance one. A Kneser--Poulsen transfer
needs the separate threshold-dependent small-variance scale; (U7) by itself
does not provide a new geometric consequence. The power bound is deliberately
coarse (already 65536 at k=1); it is not a feasible exhaustive-search claim.
No value B_k>0, or nontrivial uniform bound on B_k, has been computed here.

The [exact audit](frontier_budget.py) checks the kernel identity, independent
small beta/binomial controls, the polynomial constant certificates and the
rational budget schedule. It produces no Gaussian moment enclosure and
does not validate an external all-configuration sign claim. The universal
analytic reasoning and credited localization theorem remain unformalized
author proofs. [UNIFORM_SOURCES.json](UNIFORM_SOURCES.json) pins the source
dependencies; [SOURCES.md](SOURCES.md) credits the standard ingredients.
