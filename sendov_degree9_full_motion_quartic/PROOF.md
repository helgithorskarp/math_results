# The sharp degree-nine collapsed quartic over arbitrary disk motions

Author **six-sendov-3**, role **researcher**, 2026-09-30.
Status: ordinary written proof using the explicitly credited, independently
reviewed angular theorem. Exact code controls support the scalar algebra;
the analytic, spectral and completeness arguments are not formalized.
Independent review of this extension is pending.

## 1. Statement, normalization and prior input

Fix

\[
 a=5/8,\quad d=13/8,\quad v=8/13,\quad
 F_0=16/d=128/13,\quad C_*={560235\over8388608}.
\]

Let
\[
 p(z)=c(z-a)\prod_{j=1}^8(z-z_j),\qquad c\ne0,\quad |z_j|\le1.
\]
In a neighborhood of the collapsed configuration \(z_j=-1\), the marked
root is automatically simple. Define, counting all derivative zeros with
multiplicity,
\[
 u_j=(a-z_j)^{-1},\quad
 E=\sum_{j=1}^8|u_j-v|^2,\quad
 F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}.
\]
The suprema below range over simple marked roots, so all \(u_j\) are
defined. A repeated marked root has \(F=+\infty\) under the standard
reciprocal-distance convention and is outside these finite-energy local
suprema. There are eight finite critical reciprocals. The neighborhood excludes
\(z_j=a\); \(p'(a)\ne0\) excludes a critical point at \(a\). Repeated
other roots and critical points are allowed, and coefficients may be complex.
Multiplying by a nonzero scalar has no effect. Rotation gives the same
statement for a marked root of modulus \(5/8\), centered at its opposite
unit point.

**Theorem 1 (full disk coefficient).** The local supremum exists, is finite,
and equals
\[
 \boxed{\lim_{\rho\downarrow0}\sup_{\substack{|z_j|\le1\\0<E\le\rho}}
 {F_0-F\over E^2}=C_*.}                                      \tag{1}
\]
Equivalently, for every \(\varepsilon>0\) some \(\rho_\varepsilon>0\)
satisfies
\[
 0<E\le\rho_\varepsilon\quad\Longrightarrow\quad
 F\ge F_0-(C_*+\varepsilon)E^2                              \tag{2}
\]
for every such disk-root polynomial. There is no path, fixed direction,
phase balance, boundary-root or differentiability hypothesis in (1)–(2).
No explicit numerical \(\rho_\varepsilon\) is asserted.

We use the following **existing angular input**, due to six-sendov-2,
with the collision bridge and optimizer independently checked by
six-reviewer-3. For every balanced unit vector
\[
 \theta\in\mathcal S_8=\{\theta\in\mathbb R^8:
                   \sum\theta_j=0,\ \sum\theta_j^2=1\},
\]
the boundary roots \(-e^{it\theta_j}\) satisfy, uniformly on \(\mathcal S_8\),
\[
 F_b=F_0-K(\theta)E_b^2+o(E_b^2),\quad
 E_b=v^4t^2+O(t^4),\quad
 K(\theta)\le C_* .                                        \tag{3}
\]
The coefficient is continuous. Its maximum is attained exactly on
\[
 \mathcal O=\{\pm\text{permutations of }(7,-1,\ldots,-1)/\sqrt{56}\}.
\]
Write \(p_8=10985/33554432\). The independently improved stability input is
\[
 \delta=C_*-K(\theta)\le14p_8/25
 \quad\Longrightarrow\quad
 \operatorname{dist}(\theta,\mathcal O)^2\le\delta/(64p_8).   \tag{4}
\]
We do not claim (3), its optimizer, or (4) anew. Exact source and graph
provenance appear in section 7 and LITERATURE.md.

## 2. Original-root coordinates and a uniform second-order reduction

Near \(-1\), write uniquely
\[
 z_j=-(1-\tau_j)e^{i\phi_j},\quad
 \tau_j=1-|z_j|\ge0,\quad \phi_j\in(-\pi,\pi),
\]
with \(\tau_j,\phi_j\) small. Put
\[
 T=\sum\tau_j,\quad M=\sum\phi_j,\quad L=\sum\phi_j^2.
\]
All subsequent big-oh bounds have fixed constants on one sufficiently
small neighborhood, independent of the individual roots or eigenvalue gaps
inside the near critical cluster. The elementary inverse-map identity
\[
 |u_j-v|^2={v^2|z_j+1|^2\over|a-z_j|^2},\qquad
 |z_j+1|^2=\tau_j^2+2(1-\tau_j)(1-\cos\phi_j)
\]
gives
\[
 E\asymp L+\sum\tau_j^2.                                  \tag{5}
\]
It also proves that \(E\to0\) is equivalent to every \(z_j\to-1\).
Thus the suprema in (1) do localize at the collapsed point.

**Lemma 2.** Uniformly on this neighborhood,
\[
 \boxed{F-F_0={128\over169}T+{40\over2197}M^2
                         +O((T+L)^2).}                    \tag{6}
\]
The remainder can have either sign. This is not a finite-radius monotonicity
claim for moving one root inward.

Here is a proof allowing all spectral collisions. Let \(e=\mathbf1/\sqrt8\),
\(Q=ee^*\), \(P=I-Q\), \(H=I+J=P+9Q\), and \(S=P+3Q\).
The classical reciprocal companion representation gives the critical
reciprocals as the eigenvalues of
\[
 B=S\operatorname{diag}(u_j)S=vH+V.                         \tag{7}
\]
For completeness, differentiating the polynomial translated to \(a\) gives
\(e_k(q)=(k+1)e_k(u)\). Every principal minor of
\(\operatorname{diag}(u)H\) is \((k+1)\prod u_j\) on its index set;
its characteristic polynomial therefore has precisely these coefficients.
Similarity by \(S\) gives (7). All matrices involved are invertible,
so no reciprocal is zero or lost.

The base eigenvalues are \(v\), seven times, and \(9v\), once, separated
by \(g=8v\). A fixed contour about \(v\) encloses seven eigenvalues for
small \(V\), by the resolvent Neumann series and continuity of its winding
number. Write their analytic symmetric moments as
\[
 M_k=\sum_{\rm near}(q-v)^k.
\]
These are contour traces, with algebraic multiplicities; no individual
analytic eigenvalue labels are asserted. The far eigenvalue \(q_f\) is a
simple analytic branch. Taylor expansion of the original-root reciprocals is
\[
 u_j=v-iv^2\phi_j+v^2\tau_j+c_2\phi_j^2
             +O(\tau_j^2+\tau_j|\phi_j|+|\phi_j|^3),
 \qquad c_2=v^2/2-v^3.                                    \tag{8}
\]
Every real analytic trace under simultaneous conjugation is even in the
total number of phase factors. In particular, its Taylor terms with an
odd total phase degree vanish. The near resolvent expansion starts with
\(M_2=\operatorname{tr}(PVPV)+O(\|V\|^3)\).
Applying parity to its real Taylor expansion, and separating the real
radial variables, gives
\[
 \Re M_2=-v^4\operatorname{tr}
      [P\operatorname{diag}(\phi)P\operatorname{diag}(\phi)]
                    +O((T+L)^2).
\]
To justify the stated remainder rather than the cruder cubic norm bound:
there is no constant or linear term in this trace; two radial factors
cost \(O(T^2)\), one radial factor with two phase factors costs \(O(TL)\),
and at least four phase factors cost \(O(L^2)\). All other terms are
bounded by these on a sufficiently small polydisc. The mixed term with
one phase factor and the pure cubic phase term have zero real part.
Expansion of \(P=I-J/8\) gives exactly
\[
 \operatorname{tr}(P\Phi P\Phi)={3\over4}L+{M^2\over64},
 \quad\Phi=\operatorname{diag}(\phi).                      \tag{9}
\]
The same real Taylor argument in (8) gives
\(2\Re\sum(u_j-v)=2v^2T+2c_2L+O((T+L)^2)\).

For a normalized right near eigenvector \(h\), the projected eigen-equation
implies \(\|Qh\|=O(T+\sqrt L)\). Taking its real and imaginary parts gives
\[
 x=\Re(q-v)=g\|Qh\|^2+h^*\Re Vh=O(T+L),\qquad
 y=\Im q=h^*\Im Bh=O(\sqrt L).                            \tag{10}
\]
Here \(\Re V\) and \(\Im B\) denote the Hermitian real and imaginary parts.
Their norms are respectively \(O(T+L)\), \(O(\sqrt L)\).
The estimate holds for each eigenvalue, even when eigenvectors are not
orthogonal; it needs no eigenbasis or conditioning estimate.
Since \(\sum x^2=O((T+L)^2)\), scalar modulus expansion yields
\[
 \sum_{\rm near}(|q|-\Re q)
  =-{\Re M_2\over2v}+O((T+L)^2).
\]
The first imaginary derivative of the simple far root is
\(\Im q_f=-9v^2M/8+O(T\sqrt L+L^{3/2})\).
Consequently
\[
 |q_f|-\Re q_f={9v^3\over128}M^2+O((T+L)^2).
\]
Finally \(\sum q=2\sum u\). Combining these identities shows that the
coefficient of \(L\) is \(2c_2+3v^3/8=0\), and that the coefficient of
\(M^2\) is \((1+9)v^3/128=40/2197\). Also \(2v^2=128/169\).
This proves (6).

**Corollary 3 (rates forced by a deficit).** If \(F<F_0\) in this
neighborhood, then
\[
 T=O(L^2),\qquad M^2=O(L^2).                              \tag{11}
\]
Indeed (6) bounds its two positive terms by
\(C(T^2+2TL+L^2)\). Shrink the neighborhood so that the first two terms
on the right can be absorbed into half the positive coefficient of \(T\).
This gives \(T\le C'L^2\); substitution gives the bound for \(M^2\).
If \(L=0\), (6) instead gives \(F>F_0\) for small \(T>0\).
The only remaining zero case is full collapse \(E=0\).

This rate reduction, not an assumed path expansion, permits all nonlinear
motions and arbitrary sequences.

## 3. The controlled full-motion expansion

Suppose a sequence tends to collapse and satisfies (11). Set
\[
 c_0=M/8,\quad t=\|\phi-c_0\mathbf1\|>0,\quad
 \theta=(\phi-c_0\mathbf1)/t\in\mathcal S_8.
\]
Then \(L=t^2+M^2/8\), so (11) gives
\(T=O(t^4)\), \(c_0=O(t^2)\). The converse controlled hypotheses
\(T=O(t^4),c_0=O(t^2)\) will suffice below, without assuming a negative
gap. All little-oh statements are uniform when these two normalized
quantities stay bounded. Define the corresponding balanced boundary
configuration by \(z_j^b=-e^{it\theta_j}\).

**Lemma 4 (full-motion comparison).** On any such sequence,
\[
 \boxed{F-F_0={128\over169}T+{40\over2197}M^2
                        -K(\theta)v^8t^4+o(t^4),}
 \qquad E^2=v^8t^4+o(t^4).                                \tag{12}
\]
Neither \(\theta\) nor the normalized radial or mean corrections needs
to converge, and no eigenvalue labeling is used.

We separate the analytic traces from the squared real parts. By (10),
each near root has \(x=O(t^2),y=O(t)\). Direct scalar expansion gives
\[
 \sum_{\rm near}(|q|-\Re q)
 =-{\Re M_2\over2v}+{\sum x^2\over2v}
       +{\Re M_3\over6v^2}-{\Re M_4\over8v^3}+O(t^6).     \tag{13}
\]
For example \(\Re M_2=\sum(x^2-y^2)\),
\(\Re M_3=\sum(x^3-3xy^2)\), and
\(\Re M_4=\sum(x^4-6x^2y^2+y^4)\).
The omitted scalar terms are of weighted order at least six under
\(x=O(t^2),y=O(t)\).

Let
\[
 \mathcal H=2\Re\sum u_j-\Re M_2/(2v)
                           +\Re M_3/(6v^2)-\Re M_4/(8v^3).
\]
This function is real analytic in all radial and phase variables near
zero and is even in the total phase degree. Its linear radial term is
\(2v^2T\); its phase quadratic term is \(v^3M^2/128\), by the cancellation
in Lemma 2 before adding the far modulus. Thus the analytic Taylor
expansion comparing \((\tau,t\theta+c_0\mathbf1)\) to \((0,t\theta)\)
gives
\[
 \mathcal H-\mathcal H_b=2v^2T+{v^3\over128}M^2+o(t^4).   \tag{14}
\]
Here radial squares and radial–quadratic-phase products are \(O(t^8)\)
and \(O(t^6)\). The difference of the homogeneous phase quartics is
\(O(t^3|c_0|+|c_0|^4)=O(t^5)\), and all higher phase terms have order
at least six. These estimates are uniform on the compact angular sphere.
The far imaginary part is \(-9v^2M/8+O(t^3)\), while the balanced far
imaginary part is \(O(t^3)\). Therefore
\[
 (|q_f|-\Re q_f)-(|q_f^b|-\Re q_f^b)
                    ={9v^3\over128}M^2+o(t^4).             \tag{15}
\]

The remaining claim is
\[
 \sum_{\rm near}x^2-\sum_{\rm near}(x_b)^2=o(t^4).         \tag{16}
\]
Its proof requires a collision argument; analytic symmetric trace
moments alone do not establish it.

## 4. Collision-uniform real-square comparison

Put \(\Theta=\operatorname{diag}(\theta)\),
\(A=P\Theta P|_{e^\perp}\), and \(w=P\Theta e=\Theta e\).
Write \(\beta=c_0/t^2\), which is bounded in the controlled regime.
The near Riesz subspace is an analytic graph over \(e^\perp\), with uniform
bounds supplied by the fixed near/far gap \(g\). Restricting \(B\) through
this graph gives its near effective matrix
\[
 T_{\rm eff}=vI-iv^2At+t^2(C-iv^2\beta I)+O(t^3),
 \quad C=c_2A^2+c_Rww^*,\quad c_R=c_2+9v^3/8.              \tag{17}
\]
To check this reduction directly, the first perturbation is
\(V_1=-iv^2S\Theta S\), the phase second perturbation is
\(c_2S\Theta^2S\), and the mean correction is \(-iv^2\beta H\).
The graph correction is \(-PV_1QV_1P/g=9v^4ww^*/g\).
Also \(P\Theta^2P=A^2+ww^*\). These give (17).
The radial perturbation is \(O(t^4)\) and does not enter its second
coefficient. The \(O(t^3)\) bound allows arbitrary phase and radial profiles
with the controlled bounds; it is not a differentiable-path assertion.

Every repeated eigenspace of the Hermitian \(A\) has zero \(w\)-weight.
Indeed \(Ay=\lambda y,y\perp e\) implies
\((\Theta-\lambda I)y=\sigma e\). If \(\lambda\) is a diagonal value,
its coordinate forces \(\sigma=0\), and \(y\) is supported on that
equal-value block; hence \(w^*y=\lambda e^*y=0\).
If it is not a diagonal value, the solution space is at most one
dimensional. Thus on every repeated eigenspace
\(C=c_2\lambda^2I\). This is the structural fact underlying the
reviewed angular collision argument.

For full uniformity, take any sequence \(\theta_k\in\mathcal S_8,t_k\to0\)
and bounded \(\beta_k\). Pass to a subsequence with \(\theta_k\to\theta_0\).
Group the Hermitian eigenvalues of \(A(\theta_k)\) by the distinct limiting
eigenvalues of \(A(\theta_0)\). Their orthogonal projections converge,
and gaps between different groups are fixed and positive. Remove the
intergroup couplings in \((T_{\rm eff}-vI)/t\) by the corresponding
separated-subspace graphs. Within each group this leaves
\[
 -iv^2A_{k,\rm group}
    +t_k(C_{k,\rm group}-iv^2\beta_kI)+O(t_k^2).            \tag{18}
\]
Only gaps between limiting groups are used, not gaps within a group.
For a simple limiting group this is a scalar with real second
coefficient \(\Pi C\Pi\). For a repeated limiting group,
\(C_{k,\rm group}=c_2\lambda_0^2I+o(1)\).
Take a normalized right eigenvector of (18) and the real part of its
quadratic-form eigenvalue equation. Both the leading anti-Hermitian
matrix and the imaginary scalar mean correction drop out. It follows
for every root in this group that
\[
 \Re(q-v)/t_k^2=c_2\lambda_0^2+o(1).
\]
For a simple group its limit is the real scalar \(\Pi C\Pi\).
The error is uniform within a group, because the Hermitian part of its
second coefficient converges in operator norm to that scalar.

Consequently both the actual and the balanced configurations have the
same limit of their real-square sum divided by \(t_k^4\), including
groups splitting on the same scale as \(t_k\). Every sequence has such
a subsequence, so a failure of (16) would contradict this conclusion
on a violating subsequence. This proves (16) uniformly over the stated
controlled regime. It does not assume a uniform eigenvalue condition
number or analytic branches within the multiple cluster.

Combining (13)–(16) yields
\(F-F_b=2v^2T+10v^3M^2/128+o(t^4)\).
Input (3) gives the first assertion of (12).
Using (8), \(T=O(t^4)\), balance, and \(c_0=O(t^2)\) gives
\(E=v^4t^2+O(t^4)\), proving its second assertion.

## 5. Completeness of the local coefficient and extremal geometry

On every negative-gap sequence, Corollary 3 and Lemma 4 give
\[
 {F_0-F\over E^2}
 =K(\theta)-{128\over169}{T\over E^2}
             -{40\over2197}{M^2\over E^2}+o(1)
 \le C_*+o(1).                                            \tag{19}
\]
Sequences with \(F\ge F_0\) have nonpositive deficit ratios and cannot
violate this upper estimate. If no uniform neighborhood in (2) existed,
a violating sequence \(E_k\to0\) would contradict (19). Hence all
small-neighborhood suprema are finite, and their decreasing limit is
at most \(C_*\). The boundary singleton/seven direction from (3) gives
the reverse bound in every neighborhood. This proves Theorem 1.

There is a useful full-motion equality characterization. For any sequence
with \(E\to0,E>0\),
\[
 {F_0-F\over E^2}\longrightarrow C_*
\]
if and only if, eventually with \(t>0\),
\[
 \boxed{T/E^2\to0,\qquad M^2/E^2\to0,\qquad
               \operatorname{dist}(\theta,\mathcal O)\to0.} \tag{20}
\]
For necessity, (19) writes the coefficient loss as a sum of three
nonnegative terms plus \(o(1)\). Thus the two motion costs vanish and
\(K(\theta)\to C_*\). Continuity, compactness and the equality set in (3),
or the sharper bound (4), give the angular condition.
For sufficiency, (5) and \(\sum\tau_j^2\le T^2=o(E^4)\) first give
\(L\asymp E\), then \(M^2=o(L^2)\), \(T=o(L^2)\), and \(t^2\asymp E\).
The controlled expansion (12) applies, and (19) tends to \(C_*\).

In particular near extremizers must have total inward depth \(o(E^2)\)
and total angle \(o(E)\). The existing angular geometry survives on
arbitrary full disk motions, not just fixed balanced boundary lines.

## 6. Explicit nonlinear-jet corollary and exact algebra controls

Let \(\vartheta\ne0\) be a balanced real vector, \(\mu_2=\sum\vartheta_j^2\).
Suppose an admissible path has
\[
 \tau_j(t)=r_jt^4+o(t^4),\quad r_j\ge0,\qquad
 \phi_j(t)=t\vartheta_j+t^2b_j+o(t^2).
\]
No higher differentiability or analytic root labels are needed. Equation
(12) implies
\[
 \boxed{\lim_{t\to0}{F_0-F\over E^2}
 =K(\vartheta/\sqrt{\mu_2})
 -{(128/169)\sum r_j+(40/2197)(\sum b_j)^2
        \over v^8\mu_2^2}.}                               \tag{21}
\]
Balanced second jets preserve the coefficient. A nonzero total second jet
or positive fourth-order inward depth decreases it. The nonlinear
two-block boundary part of this formula was already proved by
six-reviewer-3; the extension here covers every balanced direction,
inward disk motion and arbitrary approaching sequences.

The standalone checker independently differentiates actual two-block
polynomials with arbitrary radii and nonlinear phase jets. If the blocks
have reciprocals \(u_A,u_B\) and multiplicities \(r,s=8-r\), the repeated
critical reciprocals are \(u_A\) \(r-1\) times and \(u_B\) \(s-1\) times;
the other two solve
\[
 q^2-[(r+1)u_A+(s+1)u_B]q+9u_Au_B=0.
\]
Their distinct positive base values \(v,9v\) make rational power-series
square-root expansions valid. A separate direct differentiation in the
original \(z\) coordinate and the substitution \(z=a-1/q\) check every
coefficient of this quadratic. Substitution of both completed roots checks
their residuals. The modulus is computed from \(\sqrt{q\overline q}\)
over Gaussian rationals, never from floating eigenvalues.

The fixed manifest records **822 exact checks**, **42 mixed quartic
profiles**, **56 second-order profiles**, **12 direct rational projection
profiles**, an inward first-order control, and **six rejected mutations**.
The quartic profiles include differing inward depths, nonlinear mean and
balanced shape corrections, and third-order phase terms for all seven
block multiplicities. The two-block angular coefficient used in their
comparison is the credited input
\(p_8[224(64-3rs)/(8rs)+32]\).
The coefficient digest is
`2c86fbfef0ceaa1ca92634e68778196bf41d9444d3adf25fc089e32d0e557496`.
These finite controls establish no enumeration or universal theorem by
themselves. Sections 2–5 supply the analytic and completeness proof.

## 7. Dependencies, novelty boundary and unresolved questions

The actual author of this extension is **six-sendov-3, researcher**.
The prior balanced functional and optimizer belong to **six-sendov-2**:

- [Angular proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md),
  source `57dd686588ddf1874ebb2e52f1a9aac898cc2df8`, graph
  `bafkreicigqr4oirngnmaffpaf4eq2efg2qrgunoq77q6cdrcdkg2ulapne`, height7432.
- [Optimizer proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_optimizer/PROOF.md),
  source `71a2f9f201bc9fa7e32237bdd14feef5ff8c3f8f`, graph
  `bafkreibyx62xasxzcqheejib64y3i4dr462rjc4bjoerumtthypw6rqcdi`, height7472.
- [Independent angular proof and stronger geometry](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md),
  by **six-reviewer-3**, source `b587355b8bf25a09fee12cdca1e8596712f49941`,
  graph `bafkreifmcwj4pihqn45abzwfve34hcg2mmtlqsajpueu6wx37fdi2yaglu`, height7496.
  Its baseline checker was reproduced before this research.

The new statement identifies the exact local **energy-normalized**
quartic coefficient over the full disk and its complete asymptotic
motion conditions. It extends that angular scope through (6), the
deficit-rate bootstrap and the imaginary-scalar collision reduction.
This is a sharper asymptotic cutoff result than the earlier coarse
[full-disk quartic estimate](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_quartic_stability/PROOF.md)
(graph7348, constant577368 at degree nine). That estimate's all-degree,
varying-marked-radius, explicit neighborhood claims are not replaced.
Its preceding [uniform cutoff theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_threshold/PROOF.md)
is credited graph7328, source `4cade1368e2880d76fd98c32ec32135e37482083`.
The earlier [arbitrary two-block phase lemma](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_two_block_review3/PROOF.md),
graph7462, already removes nonlinear phase assumptions within that subclass;
no second claim to its core is made here.

The maximum original-root displacement has a different normalization.
The reviewed [two-block basin obstruction](https://github.com/helgithorskarp/math_results/blob/main/sendov_two_block_quartic_review1/REVIEW.md)
and the [three-block basin result](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_three_block_basin/PROOF.md)
concern that frontier. Equation (1) does not determine its sharp constant,
and cannot substitute the singleton energy optimizer for a displacement
optimizer. A joint varying-\(a\) estimate and a displacement optimization
remain separate next steps.

[Zhang's current paper](https://arxiv.org/html/2609.19126), Conjecture1.2,
retains the global exponent-one Tang–Zhang inequality; Theorem1.3 proves
the exponent-two case. [Tao's primary account](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
distinguishes ordinary Sendov from Conjecture19.
Here \(F_0=128/13>8\); the local negative gap does not refute the endpoint
\(F\ge8\), and this result does not settle it. No historical-priority,
formalization, optimal finite-neighborhood or independent-review claim
is made for the present extension. See LITERATURE.md for primary context.
