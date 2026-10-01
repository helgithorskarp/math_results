# Independent full asymmetric angular audit and stationary classification

Actual reviewer **six-reviewer-1**, role **independent mathematical reviewer**,
2026-10-01. Shared signing identity does not distinguish the researchers.

The target is committed lemma **8800**, “Sharp degree-nine angular ratio on the
full asymmetric3+3+1+1 family, with complete equality classification”, reference
`bafkreidhga56a4o7yueda4no6kmkkkyf3zqor3ohnkznb4arj25wxy3nfu`, actual author
six-sendov-2. I read its complete 21,519-byte body, relations, and all five
source files at commit `167af56c25651784f7c8106a3ec1d85e52b51c82`:
[proof](https://github.com/helgithorskarp/math_results/blob/167af56c25651784f7c8106a3ec1d85e52b51c82/round-two/six-sendov-2/asymmetric-family-global-bound/PROOF.md),
[checker](https://github.com/helgithorskarp/math_results/blob/167af56c25651784f7c8106a3ec1d85e52b51c82/round-two/six-sendov-2/asymmetric-family-global-bound/verify.py),
[fixture](https://github.com/helgithorskarp/math_results/blob/167af56c25651784f7c8106a3ec1d85e52b51c82/round-two/six-sendov-2/asymmetric-family-global-bound/expected.json),
[instructions](https://github.com/helgithorskarp/math_results/blob/167af56c25651784f7c8106a3ec1d85e52b51c82/round-two/six-sendov-2/asymmetric-family-global-bound/README.md), and
[literature](https://github.com/helgithorskarp/math_results/blob/167af56c25651784f7c8106a3ec1d85e52b51c82/round-two/six-sendov-2/asymmetric-family-global-bound/LITERATURE.md).

**Verdict: confirmed complete ordinary proof, with independently reproduced
exact algebra and independently checked case coverage.** Its continuous
uniform extension, three-level bound and equality prerequisite is lemma8753,
source `6efce877eb9dcde6e12b6a90930d65382b29dd89`, independently confirmed in
[review8806](https://github.com/helgithorskarp/math_results/blob/178ddb2ff86b4c3f2e4be62ac31532045941a863/round-two/six-reviewer-1/three-level-angular-audit/REVIEW.md).
The present review additionally proves the complete interior stationary
classification and a global, existential quadratic stability bound on this
family. These are ordinary proofs with finite exact checks, not formalizations.

## Exact theorem and inherited scope

For real balanced norm-one \(\theta\in\mathbb R^8\), let
\[
 e=\mathbf1/\sqrt8,\quad P=I-ee^T,\quad
 H=P\operatorname{diag}(\theta)P|_{e^\perp},\quad
 w=\operatorname{diag}(\theta)e,
\]
\[
 X=\sum\theta_j^4,\quad
 \eta=64\sum_{\lambda\ \mathrm{distinct}}\|\Pi_\lambda w\|^4,
 \qquad C=(1-\eta)/(X-1/8).
\]
All projections use full eigenspaces. At the uniform4+4 orbit use the
continuous extension \(C=16\) proved in8753 and audited in8806.
Let \(\mathcal F\) be the normalized profiles, permutations and sign changes of
\[
 u=(c+x,c+x,c+x,c-x,c-x,c-x,-3c+y,-3c-y),\quad \|u\|>0.
\]
The target proves \(C\le c_3\) everywhere in this closed family, with equality
exactly the orbit \(\mathcal O_3\) of the normalization of
\[
 (\alpha,\alpha,\alpha,\alpha,1,1,1,-4\alpha-3).
\]
Here \(\alpha\) is the unique root in
\((-853410556973738/10^{15},-853410556973736/10^{15})\) of
\[
 4575t^4+11695t^3+11175t^2+4737t+746,
\]
and
\[
 c_3=\frac{8(\alpha-1)^2(5\alpha+3)^2}
 {(15\alpha^2+24\alpha+10)(35\alpha^2+38\alpha+11)}
 \in(24.53389668,24.53389670),\qquad c_3>49/2.
\]
Every genuinely four-level member is strictly below this maximum, but such
members can approach the equality orbit. The family includes all its
coincidences. It is not a reduction of arbitrary eight-coordinate profiles
to four levels. Neither the full-sphere equality \(C_*=c_3\) nor the
degree-nine finite-energy first-power endpoint follows.

## Independent compressed-operator derivation

I used a different starting point from the author's cofactor/Newton moment
calculation. Let block multiplicities \(m=(3,3,1,1)\) and block values
\(\ell=(c+x,c-x,-3c+y,-3c-y)\). In the block-constant subspace of \(e^\perp\)
take three vectors with block values \(1/m_i\) on blocki and \(-1\) on
block4. Their Gram and compressed quadratic-form matrices are
\[
 G_0=\operatorname{diag}(1/3,1/3,1)+\mathbf1\mathbf1^T,
 \quad B_0=\operatorname{diag}(\ell_1/3,\ell_2/3,\ell_3)
                       +\ell_4\mathbf1\mathbf1^T.
\]
The actual restricted operator is \(A=G_0^{-1}B_0\), and the raw coupling
coordinates are \(v=(3\ell_1,3\ell_2,\ell_3)^T\). The four remaining
dimensions are the two within-triple sum-zero spaces; their coupling is zero.
The independent checker verifies \(A^TG_0=G_0A\), the complete characteristic
polynomial
\[
 h(z)=z^3+4cz^2+[c^2-(x^2+3y^2)/4]z-6c^3+3c(y^2-x^2)/4,
\]
and every coefficient of the three coupling moments
\[
 \nu_i=v^TG_0A^iv\quad(i=0,1,2)
       =(N,S_3,S_4-N^2/8)_i.
\]
Here \(N=24c^2+6x^2+2y^2\),
\(S_3=c[18(x^2-y^2)-48c^2]\), and
\(S_4=168c^4+36c^2x^2+108c^2y^2+6x^4+2y^4\).

Set \(K_{ij}=\operatorname{tr}(A^{i+j})\), \(0\le i,j\le2\).
The orthogonal projection, in the operator trace inner product, of the
rank-one operator \(vv^TG_0\) onto \(\operatorname{span}(I,A,A^2)\) has
squared norm \(\nu^TK^{-1}\nu\). With distinct eigenvalues this is exactly
the sum of squared raw spectral masses, \(\eta_u\). This identifies the
same ratio by an actual operator calculation rather than a supplied root list.
For \(\kappa=c^2,U=x^2,V=y^2\), every odd exponent cancels, and
\[
 M=64\kappa^2+64\kappa V+(U-V)^2,
\]
\[
 \Delta=2304\kappa^3-32\kappa^2U+6624\kappa^2V
 -23\kappa U^2+942\kappa UV-855\kappa V^2+(U+3V)^3.
\]
The checker establishes the full identities
\[
 \det K=\Delta/16,\quad S_4-N^2/8=3M/2,\quad
 C=\mathrm{Num}/(M\Delta),
\]
where \(\mathrm{Num}=(32/3)[N^2\det K-\nu^T\operatorname{adj}(K)\nu]\).
It reconstructs and records every numerator coefficient, including the
vanishing \(\kappa^5\) coefficient. There are **20 nonzero monomials**.
The target prose says21 explicitly listed coefficients, whereas its
`NUM_TERMS` stores20; the missing degree-five monomial has coefficient zero.
This is an editorial counting correction, not a mathematical gap.

## Coverage, boundary and stationary reduction

Independent block swaps and a reflection make \(c,x,y\ge0\). Setting
\(N=1\) gives the compact triangle
\(24\kappa+6U+2V=1\). Its square-root map and the inherited extended C are
continuous, so a maximum exists. No singular boundary determinant is divided
by in this compactness argument.

On \(U=0\) the partition is6+1+1, and on \(V=0\) it is3+3+2;
their coincidences and uniform extension have \(C\le16\) by the verified
partition-specific8753 bounds. On \(\kappa=0\), exact cancellation gives
\[
 C=\frac{4(3U^3+67U^2V+177UV^2+9V^3)}{(U+3V)^3}
  =\frac{208}{9}-\frac{4(5U-21V)^2}{9(U+3V)^2}\le208/9.
\]
This also covers \(U=V\), where the value is16, and the nonzero endpoints.
The zero profile is excluded. Both boundary bounds are strictly below c3.
The equality profile belongs to the positive interior with
\(c=(\alpha+1)/2,x=(1-\alpha)/2,y=-(5\alpha+3)/2\), all positive.

In the positive interior, two triple values and two singleton values have
either four original levels or one triple/singleton coincidence. The two
quadratics with centers c and-3c cannot have both roots in common when c>0.
Ordinary compression interlacing gives three distinct h roots: three simple
gap roots in the four-level case; two simple gap roots and one inactive
original-level root in the collision case. Full original-level eigenspaces
have zero coupling. Thus \(\det K>0\), \(M>0\), and the rational ratio is
analytic even on the interior collision locus. This verifies the
Fermat-stationarity hypothesis, including that locus.

In the chart \(V=1\), write \(n=\mathrm{Num}(\kappa,U,1)\),
\(d=M\Delta(\kappa,U,1)\), and take positive-content primitive versions of
\(p=n_\kappa d-nd_\kappa\), \(q=n_Ud-nd_U\).
Their respective \((U,\kappa)\) bidegrees are(9,8) and(8,9).
The independent subresultant remainder sequence has U degrees9,8,...,0.
Its constant term is exactly the degree59 polynomial
\[
 R=A_0\kappa^7(16\kappa-1)^{14}(125\kappa+81)^5F_4F_6F_7F_{16},
\]
with the complete integer factors and A0 given in [check.py](check.py).
F4/F6/F7 are the target's quartic, degree-six and degree-seven factors;
F16 is its complete degree-sixteen factor. No omitted factor is dropped.

Crucially, the constant polynomial identity also has a separate verification.
Each term of the literal17x17 Sylvester determinant selects eight p-row
entries and nine q-row entries. Hence its kappa degree is at most
\(8\cdot8+9\cdot9=145\). A new integer-only Bareiss implementation verifies
the determinant equals R at **all146 distinct integers0 through145**.
The polynomial identity follows from this degree bound. Positive-size point
evaluation is a finite certificate of this identity, not sampled evidence
for a continuum inequality. All integer divisions are checked exact.

The factors kappa and125kappa+81 contribute no positive interior candidate.
At kappa1/16 the actual specialized gcd in U isU squared, excluding U>0.
F6 has all coefficients positive. Independent Fraction Sturm sequences give
zero positive roots ofF7, and exactly two positive roots each ofF4 andF16.
The respective zero/infinity variation pairs are(2,2),(3,1),(7,5).

The linear PRS member is \(L=A(\kappa)U+B(\kappa)\), of coefficient
degrees48 and49. For every preceding PRS step, the checker verifies the full
pseudo-division polynomial identity and that its scalar remainder multiplier
is coprime to bothF4 andF16. The seven multiplier degrees are
0,2,6,14,26,42,58. Thus common roots of p,q force L=0 after specializing
at *every* root of either factor; no generic division or presumed unique
lift hides an exceptional parameter. Gcd(A,F4)=gcd(A,F16)=1 then forces
\(U=-B/A\). The author's alternative row-cofactor argument is also valid:
its two15x15 minors are a polynomial-ideal identity, not a numerical fit.

ForF4, the independently checked lifted collision identity is
\((U-1-16\kappa)^2=64\kappa\). It gives a triple/singleton coincidence;
8753 bounds this branch by c3 with the complete inherited equality orbit.
ForF16, new root intervals independently generated from the factor and
certified with Fraction Sturm counts exhaust its two positive roots.
Exact rational interval evaluation forces positive lifts and denominators,
and respectively values in(23,24) and(7,8). Both are below c3.
Compactness, the strict boundary bound and this exhaustive necessary
stationary analysis therefore establish the target upper bound and equality
classification. I found no missing boundary, factor, lift or collision case.

## Strengthening and improvement opportunities

**Proved: complete interior stationary shapes, including existence and type.**
The target only needed necessary candidate bounds. I also verify the
denominator-cleared substitutions
\[
 A^{\deg_U p}p(\kappa,-B/A)\equiv0\pmod{F_j},\quad
 A^{\deg_U q}q(\kappa,-B/A)\equiv0\pmod{F_j},\quad j=4,16.
\]
Since A is nonzero, these prove actual stationarity at every positive root,
not merely resultant membership. Coprimality of the lifted collision
polynomial withF16 proves that both F16 shapes genuinely have four levels.
The four independent rational root intervals each have count1, and global
root counts prove exhaustion. Thus, modulo the stated block exchanges,
permutations and reflection, there are exactly **four interior stationary
shapes** in the normalized family.

Let P,Q denote the unnormalized derivative numerators. At a stationary
point the Hessian of C has diagonal entries \(P_\kappa/d^2,Q_U/d^2\) and
off-diagonal \(P_U/d^2\). The checker verifies
\(d(P_U-Q_\kappa)=2(Pd_U-Qd_\kappa)\), ensuring symmetry there.
Independent rational interval bounds certify the signs of
\(P_\kappa\) and \(P_\kappa Q_U-P_U^2\). They prove:

| Factor and positive root | Kappa for orientation | Certified C interval | Type within the two-dimensional family |
|---|---|---|---|
|F4, smaller|0.01338492598|(24.533896688,24.533896689)|Strict global maximum, exactly c3|
|F4, larger|0.50517725552|(4.291469467,4.291469468)|Saddle|
|F16, smaller|0.00041058898|(23.110004701,23.110004702)|Saddle|
|F16, larger|16.91757846337|(7.032426691,7.032426692)|Strict local maximum|

The kappa decimals are descriptive only. Certified rational endpoints,
positive lifts/denominators and Hessian sign bounds are in
[expected.json](expected.json), regenerated from [check.py](check.py).
The low-value local maximum is a genuine additional four-level local maximum
*within this family*. No assertion about its transverse full-sphere Hessian
is made. This classification warns that finding a four-level stationary
point or local maximum alone does not identify the global optimizer.

**Proved: global quadratic coercivity on this closed family.** With Euclidean
chord distance to the finite normalized equality orbit, there exists
\(b_{\mathcal F}>0\) such that
\[
 c_3-C(\theta)\ge b_{\mathcal F}\operatorname{dist}(\theta,\mathcal O_3)^2
 \quad\text{for every }\theta\in\mathcal F.
\]
Proof: review8806 gives local full-sphere coercivity with any fixed
\(0<b<\Lambda_4\), where
\(340.462200<\Lambda_4<340.462201\). Fix b340 and its neighborhood.
The remaining part of the compact family is disjoint from the complete
equality set, so its continuous deficit has a positive minimum delta0.
Sphere chord distances are at most2, hence
\(b_{\mathcal F}=\min(340,\delta_0/4)>0\) works everywhere.
If that remaining set is empty, take b340 directly. This is an existential
global family bound, not an effective numerical constant or full-sphere
global inequality.

The sharp asymptotic local coefficient within this family is still
\(\Lambda_4\), by the scalar fourfold-splitting quadratic form in8806.
Indeed the family contains the normalized curve
\[
 u_\epsilon=(\alpha+\epsilon,\alpha+\epsilon,\alpha+\epsilon,
 1,1,1,\alpha-3\epsilon,-4\alpha-3).
\]
Its perturbation has sum and scalar product with the equality profile zero,
and squared norm12, so \(\|u_\epsilon\|^2=N_0+12\epsilon^2\).
It is a nonzero fourfold-splitting tangent. Consequently
\[
 \frac{c_3-C(u_\epsilon/\|u_\epsilon\|)}
 {\operatorname{dist}(u_\epsilon/\|u_\epsilon\|,\mathcal O_3)^2}
 \longrightarrow\Lambda_4.
\]
No larger asymptotic coefficient can work; the validity of the endpoint
coefficient on an entire neighborhood is not asserted. Evaluating the
best **global** bF or furnishing an explicit collar remains a separate
two-dimensional minimization/certificate obligation.

**Open directions, not results.** The other four-level multiplicity patterns
need separate complete boundary/interior analyses. A universal support
reduction or a positive full-sphere upper-bound certificate is required for
Cstar=c3. This review supplies neither. The same exact elimination method
may grow sharply in other patterns; resource failure would be an operational
limit, not mathematical nonexistence. Formalizing interlacing, full spectral
projections and specialization-safe polynomial identities would remove
remaining software and ordinary-proof trust boundaries.

## Evidence, trust boundary and prior art

The reviewer checker imports **no researcher code or fixture as a proof
premise**. It uses pinned SymPy1.14.0 for exact characteristic, trace, derivative,
subresultant and quotient-polynomial operations, and a fresh Fraction/integer
implementation for the146 degree-bounded determinant checks, Sturm counts and
interval signs. All rings have characteristic zero; square substitution is
checked on every exponent; the elimination variable is U with coefficient
ringQ[kappa]. Congruence existence tests clear powers of A before reduction,
without numerical algebraic roots or denominator guessing. No floating-point
value, solver, heuristic reconstruction or incomplete enumeration is used.
The code uses explicit `require` guards, not removable assertions.

There are43 recorded exact checks, four internal mathematical damage controls,
complete normal/optimized fixture comparisons, and separately labeled author
replays. The independent fixture hash, runtimes, source hashes and comparison
details are in [provenance.json](provenance.json). Written arguments supply
compactness, interlacing, full-eigenspace interpretation, the degree bound,
specialization propagation, stationarity/Hessian interpretation and global
coercivity; software output alone is not a proof of those bridges.
No claim of a proof-assistant kernel check is made.

Target-specific live searches for the asymmetric3+3+1+1 angular family and
the distinctive c3 constant found no matching primary prior theorem. This
bounded absence is not a historical-priority proof. The graph contribution
extends the previously confirmed three-level8753 scope; the basic spectral
compression, Gram projection, resultants, Sturm theory, compactness and
Hessian tests are established techniques. The author's adaptation and
earlier campaign mechanisms retain credit.

[Zhang's primary paper](https://arxiv.org/html/2609.19126), Conjecture1.2,
states the first-power endpoint, while Theorem1.3 establishes the quadratic
case. This family ratio audit does not settle that endpoint or rebrand
ordinary Sendov as new. The source also credits [7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md),
[review7496](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md),
[7940](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_level_displacement/PROOF.md)
(a different displacement objective),
[8672](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/triple-angular-persistence/PROOF.md)
(symmetric slice),
[8702](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/asymmetric-angular-obstruction/PROOF.md),
[review8749](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/angular-obstruction-audit/REVIEW.md),
[8160](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_moving_pair_comparison_boundary/PROOF.md)
and [review8230](https://github.com/helgithorskarp/math_results/blob/main/sendov_moving_pair_threshold_review3/REVIEW.md).
These contextual citations are not additional unexamined theorem premises.
[SymPy's primary documentation](https://docs.sympy.org/latest/modules/polys/reference.html)
specifies the subresultant PRS operation; actual version is pinned here.

The review confirms8800 with8753 explicitly inherited; its local/global
coercivity refinement additionally depends on8806. It supplies compact,
independent reproduction and consequential scoped refinements, while the
full all-sphere optimum and finite-energy first-power conjecture remain open.
