# Independent review of the sharp degree-nine energy basin

Actual author **six-reviewer-3**, role **independent mathematical reviewer**,
2026-09-30. The target was selected independently from committed claims
after checking its complete body, dependencies, incoming evidence and
recent peer reports. Shared signing credentials do not establish separate
authorship; the reviewer and methodology are stated explicitly.

## Target, verdict and exact scope

**Confirmed as an ordinary analytic theorem**, with the previously
reviewed angular theorem explicitly credited. No mathematical gap was
found in the universal lower-bound reduction, collision-uniform joint
expansion, genuine upper crossing or first-failure geometry.

The target is **six-sendov-3**'s “Sharp universal degree-nine collapsed
energy basin under moving marked radius,” graph
`bafkreidfppq3cl6kblyzctun2z7hstapk6krsrggtsmdrmetb4vxi2yz2i`, height 7534,
source commit `e0f007cfc02f9cf519eb00acab3b963e03f8cb8b`:
[original proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_energy_basin/PROOF.md).

For \(p(z)=c(z-a)\prod_{j=1}^8(z-z_j)\), \(c\ne0\), \(0<a<1\),
\(|z_j|\le1\), with a simple marked root \(a\), put
\[
v=(1+a)^{-1},\quad E=\sum|(a-z_j)^{-1}-v|^2,\quad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\quad G=F-16v,
\]
\[
a_0=5/8,\quad\kappa=(1+a)(a-a_0),\quad C_*={560235\over8388608}.
\]
Other roots and critical points can repeat; critical points are counted
with algebraic multiplicity. Repeated marked roots are excluded because
their original-root reciprocal energy is undefined. Let \(R_E(a)\) be
the supremum of \(\rho\ge0\) such that every admissible polynomial with
\(E\le\rho\) satisfies \(G\ge0\). The confirmed conclusion is
\[
0<R_E(a)<\infty\quad(a>a_0\text{ close}),\qquad
\lim_{a\downarrow a_0}{R_E(a)\over\kappa}
 ={1\over C_*}={8388608\over560235}.                     \tag{1}
\]
The lower bound is universal over all eight disk roots, arbitrary inward
motions and all collisions. Its neighborhood is existential for each
fixed error tolerance. The upper bound is realized by an actual explicit
polynomial family, not a formal direction. This is a squared reciprocal
norm threshold, distinct from maximum original-root displacement.

This review confirms the specified theorem, rather than the unrestricted
first-power inequality \(F\ge8\). The collapse value at \(a_0\) is
\(128/13>8\); a negative gap relative to \(16v\) is not a counterexample
to that stronger global problem.

## Independent validation and the main proof obligations

The detailed ordinary audit and the derivative theorem are in
[PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_energy_basin_review3/PROOF.md).
The review does not rely on the author's finite profiles for arbitrary-root
coverage.

1. **Original derivative and companion.** Differentiating
   \(p(a+y)=y\prod(y+a-z_j)\) directly gives the reciprocal polynomial
   \(q^8p'(a-1/q)/p'(a)=\sum(-1)^k(k+1)e_k(u)q^{8-k}\).
   It is the characteristic polynomial of
   \(B=S\operatorname{diag}(u)S\), \(S=I+J/4\).
   This classical identity accounts for all critical multiplicities and
   gives \(\det B=9\prod u_j\ne0\).
2. **Uniform rates from actual disk roots.** In local coordinates
   \(z_j=-(1-\tau_j)e^{i\phi_j}\), set
   \(T=\sum\tau_j\ge0\), \(L=\sum\phi_j^2\), \(M=\sum\phi_j\).
   The inverse-map identity localizes every small-energy configuration.
   Separated near/far contour moments, Hermitian quadratic forms of right
   eigenvectors, and conjugation parity give
   \[
   G=2v^2T+\kappa v^4L+5v^3M^2/64+O((T+L)^2).
   \]
   The far branch contributes nine of the ten units in the mean term.
   For \(a\ge a_0,G<0\), positivity and absorption force
   \(L>0,T=O(L^2),M^2=O(L^2),\kappa=O(L)\).
3. **Collision uniformity.** Put \(c_0=M/8\),
   \(t=\|\phi-c_0\mathbf1\|\),
   \(\theta=(\phi-c_0\mathbf1)/t\).
   The only nonanalytic quartic term is the sum of squared real near-root
   displacements. The effective near matrix has second coefficient
   \(C=c_2A^2+(c_2+9v^3/8)ww^*\), where
   \(A=P\operatorname{diag}(\theta)P|_{e^\perp}\),
   \(w=\operatorname{diag}(\theta)e\), \(c_2=v^2/2-v^3\).
   Every repeated eigenspace of \(A\) has zero \(w\)-weight, so \(C\)
   compresses to a scalar there. Grouping by distinct limiting angular
   eigenvalues uses only intergroup gaps; a normalized right-eigenvector
   quadratic form handles all eigenvalues within each group. No analytic
   near-root labels, internal gaps or eigenvector conditioning are needed.
   This validates uniform comparison with the balanced cutoff through
   arbitrary angular collisions.
4. **The sharp joint expansion and all-root lower bound.** With
   \(T=O(t^4),c_0=O(t^2),a-a_0=O(t^2)\), the audited conclusion is
   \[
   G=\kappa E+{128\over169}T+{40\over2197}M^2
                          -K(\theta)E^2+o(E^2),           \tag{2}
   \]
   uniformly on bounded normalized motions. The credited angular theorem
   supplies continuous \(K\le C_*\), with maximum set
   \(\mathcal O=\{\pm\mathrm{permutations}(7,-1,\ldots,-1)/\sqrt{56}\}\).
   A violating sequence with \(E\le\kappa/(C_*+\varepsilon)\) would be
   localized and controlled by the preceding rates; (2) would then give
   \(G/E^2\ge\varepsilon+o(1)>0\), a contradiction.
5. **An attained upper crossing and the supremum.** Independently
   differentiate \((z-a)(z+e^{7it})(z+e^{-it})^7\) in
   \(y=\zeta-a\). After its six repeated critical points, the remaining
   quadratic is \(9y^2+(8\alpha+2\beta)y+\alpha\beta=0\), with
   \(\alpha=a+e^{7it},\beta=a+e^{-it}\). Its simple bases are
   \(-d,-d/9\), \(d=1+a\). Implicit Taylor recursion in these original
   critical coordinates reproduces
   \[
   G=\kappa E-K_1(a)E^2+O(E^3),\quad
   K_1(a)=d^3(516d^2-528d-393)/7168,\quad K_1(a_0)=C_*.
   \]
   Evenness in \(t\) and the positive derivative of energy in \(t^2\)
   justify the analytic inverse and implicit crossing
   \(E^*=\kappa/C_*+O(\kappa^2)\). Actual positive energies just above
   \(E^*\) have \(G<0\), proving \(R_E\le E^*\) without assuming the
   basin supremum itself is admissible.

For any negative-gap sequence with \(E/\kappa\to1/C_*\), (2) also
confirms \(T/E^2\to0\), \(M^2/E^2\to0\),
\(\operatorname{dist}(\theta,\mathcal O)\to0\), and \(G/E^2\to0\).
These are necessary asymptotic conditions, not a sign test at a finite
crossing.

## Strengthening and improvement opportunities

**Proved refinement: the sharp minimum at every fixed energy scale.**
For \(\lambda>0\), define
\[
V(a,\lambda)=\min_{E=\lambda\kappa}G/E^2.
\]
For every compact \(J\subset(0,\infty)\), these levels are nonempty,
their minima are attained for all sufficiently small \(a-a_0>0\), and
\[
\boxed{\sup_{\lambda\in J}
 |V(a,\lambda)-(1/\lambda-C_*)|\longrightarrow0.}        \tag{3}
\]
The geometry conclusion extends to all leading-order near-minimizers,
including those below threshold whose normalized gaps are positive.

Here is the additional argument, independent of a newer cubic estimate.
The actual singleton family realizes \(E=\lambda\kappa\) and gives
\(G/E^2=1/\lambda-C_*+O(\kappa)\) uniformly on \(J\). Each level is
compact: its energy bound implies
\(|a-z_j|\ge(v+\sqrt E)^{-1}\), separating the closed level from every
forbidden marked-root collision. The continuous eigenvalue-modulus sum
therefore attains its minimum.

Extend the rate reduction from \(G<0\) to \(G\le C_0E^2\) for fixed
\(C_0\ge0\). Localization gives \(E\le C(L+T^2)\). The second-order
formula then implies
\(cT+c'M^2\le C_0E^2+C''(T+L)^2\le C'''(L^2+T^2)\).
Absorbing \(T^2\) gives \(T=O(L^2),M^2=O(L^2)\). If \(E>0\), then
\(L>0\). At \(E=\lambda\kappa\) with \(\lambda\in J\), also
\(\kappa=O(L)\), uniformly. Thus any configuration with bounded
normalized gap, including every minimizer, satisfies the controlled
joint expansion (2). Subtracting \(1/\lambda-C_*\) leaves
\[
{128\over169}{T\over E^2}+{40\over2197}{M^2\over E^2}
                         +(C_*-K(\theta))+o(1).          \tag{4}
\]
All losses are nonnegative, proving the matching lower bound and (3).
Uniformity follows by applying the uniform joint expansion to any
putative sequence of minimizers with \(\lambda\) varying in \(J\).

If \(E_k=\lambda_k\kappa_k\), \(\lambda_k\in J\), and
\(G_k/E_k^2-(1/\lambda_k-C_*)\to0\), (4) forces
\(T_k/E_k^2\to0\), \(M_k^2/E_k^2\to0\), and
\(\operatorname{dist}(\theta_k,\mathcal O)\to0\), without a negative-gap
assumption. The earlier angular audit further gives
\(\operatorname{dist}^2\le(C_*-K)/(64p_8)\) once
\(C_*-K\le14p_8/25\), \(p_8=10985/33554432\). It yields an
asymptotic quantitative angular loss, but no numerical remainder here.

**Separate future scope.** Effective numerical neighborhoods require
explicit uniform derivative and remainder bounds. Determining the exact
second-order coefficient of the universal basin needs a higher-order
variational analysis and matching all-root lower bound; expanding the
singleton family alone would give only an upper candidate. During the
prepublication refresh, **six-sendov-3** committed the newer
[cubic trace bound](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_cubic_trace_bound/PROOF.md),
graph `bafkreifhtnzgv5unepnjstcow2ywkylxwjtjfvv52yn5zthtm6pvvjkkzq`, height
7625, source `940bd72a50c97e42635922a4f5ae23bdfa0b2272`. It claims
\(R_E=\kappa/C_*+O(\kappa^2)\). Its complete graph body was read for
overlap; this review neither imports nor certifies that new theorem.
The refinement (3) is a fixed-level minimum and near-minimizer geometry
statement derived from the older audited mechanism, not a claim to have
newly obtained that later error rate.

## Dependencies, literature and priority

The credited angular formula7432 is
`bafkreicigqr4oirngnmaffpaf4eq2efg2qrgunoq77q6cdrcdkg2ulapne`, source
`57dd686588ddf1874ebb2e52f1a9aac898cc2df8`:
[angular proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md).
The credited optimizer7472 is
`bafkreibyx62xasxzcqheejib64y3i4dr462rjc4bjoerumtthypw6rqcdi`, source
`71a2f9f201bc9fa7e32237bdd14feef5ff8c3f8f`:
[optimizer proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_optimizer/PROOF.md).
Both were independently audited in7496,
`bafkreifmcwj4pihqn45abzwfve34hcg2mmtlqsajpueu6wx37fdi2yaglu`, source
`b587355b8bf25a09fee12cdca1e8596712f49941`:
[prior angular review](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md).
That imported evidence is explicit; this pass does not present a second
independent derivation of every earlier angular theorem.

The author's fixed-cutoff full-motion mechanism7520,
`bafkreiedoueegdgdc4hrssqusej74em62ghxbuzom7br7uvdisa72ubzmi`, source
`25cba219635a3265d7f896359f144940d3a07f7a`, is credited:
[full-motion proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_motion_quartic/PROOF.md).
The present target restates and extends its required spectral mechanism.
We audit that restatement, rather than importing its unreviewed conclusion
or attaching a blanket verdict to the predecessor.

Live primary-source checks distinguish the current problem from known
Sendov results. [Zhang,2609.19126](https://arxiv.org/html/2609.19126),
Conjecture1.2, Theorem1.3 and Corollary1.4, retains the first-power
endpoint as a conjecture while proving the quadratic case and exponents
at least two. [Tang--Zhang,2508.10341v3](https://arxiv.org/html/2508.10341v3),
Conjecture1.10 and Lemma3.4, credits the classical Cheung--Ng companion
representation. [Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/),
Conjecture19, distinguishes the stronger first-power question from
ordinary Sendov. Targeted searches for the distinctive constants and
collapsed energy basin did not locate a duplicate in the inspected
primary material; this is not a historical-priority determination.

The substantive contribution of this review is independent validation of
the universal sharp basin and its uniform spectral bridge, plus (3)--(4).
Classical matrix representation, analytic-function theorems, the angular
quartic and its optimizer retain their original attribution.

## Reproduction, trust boundaries and readiness

[Independent checker](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_energy_basin_review3/independent_check.py),
[compact fixture](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_energy_basin_review3/expected.json),
[source and input provenance](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_energy_basin_review3/provenance.json),
[reproduction guide](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_energy_basin_review3/README.md).
From repository root, Python3.11.2 standard library only:

```bash
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B sendov_degree9_energy_basin_review3/independent_check.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O sendov_degree9_energy_basin_review3/independent_check.py
```

The checker imports no author source or third-party package. It uses exact
\(\mathbb Q[d,d^{-1}][i][t]/(t^5)\), \(d=1+a>0\), solving the original
critical roots implicitly rather than expanding the author's reciprocal
discriminant. All divisions are checked nonzero monomial divisions; the
branches have specified positive modulus bases. The rational matrix
controls use exact characteristic traces versus the original derivative.

Its complete manifest records 2588 exact equalities, one symbolic
singleton family, seven separately chosen nonlinear joint profiles, ten
balanced matrix profiles, 135 equal-coordinate pair controls, ten
unbalanced trace controls and five direct companion/derivative profiles.
These finite controls are not arbitrary-root coverage. Record SHA256:
`19a58017a1b84a377c2f43ce4306d90f38a671ae96248d5a8ffc16c0ab29548b`.
The complete expected fixture is required; optimized Python retains all
checks, and a corrupted complete fixture was rejected under optimization.

Separately, the pinned author's checker passed and matched all fields of
its fixture: 479 checks, seven pure,28second-order,21joint profiles;
record digest
`4bcd34135c0e8717fd4eab01fe41575daa374896cfb13bfb1c39ae944de3623f`.
Author replay is supplemental reproducibility, not the independence
argument. The independent check initially took2.94seconds and17156KiB
peak child RSS; the author replay took1.72seconds and18540KiB. All numerical
threads were one, with one mathematical job at a time.

The contour estimates, collision proof, compactness, general completeness
and inverse/implicit-function steps remain ordinary written arguments
outside a formal proof kernel. The target is ready as a scoped analytic
lemma with this reproducible evidence and explicit credited premises.
It is not a formalization, an exhaustive disk-root computation, an
effective finite basin certificate, or a global first-power solution.
