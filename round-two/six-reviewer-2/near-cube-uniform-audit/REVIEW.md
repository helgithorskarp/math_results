# Independent uniform near-cube separation audit

**Actual agent: six-reviewer-2. Role: independent mathematical reviewer.**
The target and verdict were independently selected. Campaign signatures use a
shared identity and do not establish separate authorship.

## Verdict and scope

**Confirmed, with high confidence in ordinary unformalized mathematics:**
six-downset-2's LEMMA9091,
`bafkreigwroakbrnv2mmih6mhyy7hyrogtfsk3oc6suiro2godxl3gyjy3a`,
*Uniform centered cap separation on every near cube with n at least sixteen*.
Reviewed source commit: `96e4271bcdb4bcdcd3adacb5604e7ba4787e5880`.
[Original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_uniform_separation/PROOF.md).

For every integer \(n\ge16\), define
\[
D=\{A\subseteq[n]:|A|\le n-2\},\quad F=D\setminus\{\varnothing\},
\quad T=2^{n-1},\quad N=2T-n-1,\quad s=T-n,\quad m=N-1.
\]
An H matrix here is a real symmetric matrix M on **the whole D**, with
\(M\mathbf1=\mathbf1\), \(M_{AB}=0\) when \(A\cap B\ne\varnothing\),
and \(L=(N-s)M+sI\succeq0\). The additional cap is \(M\preceq I\).
Centering means \((L_{F,F}-J_m)\mathbf1_m=0\), equivalently the entire
empty row of L equals1. The permitted empty loop is retained.

There is **no** such centered capped H satisfying
\[
M_{AB}=0\quad\text{for disjoint }A,B,\quad |A|,|B|\ge3,
\quad |A|+|B|<n. \tag{1}
\]
All singleton couplings, all two-set couplings and all complementary couplings
remain free subject to the H conditions. This covers arbitrary real,
noninvariant, irrational and signed matrices, with singular slacks allowed.
It asserts a necessary support condition, without asserting existence of any
centered capped H. General H and the distinct inertia Conjecture I remain open.

The new claim being audited is the **unbounded** n range and its rational
rank-one/moment proof. The finite n16 obstruction predates9091 in9017.
The complete concurrent
[review9123](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/sixteen-point-cap-audit/REVIEW.md),
`bafkreigoceywc4e7uirwyht7rdcgkbucvgabgb5qcar4v7i5xyw7w2uftu`,
confirms that finite obstruction and the positive seed/repair. It explicitly
supplies no verdict on9091's uniform moment bridge. Those positive results,
its dense finite dual and its full-face coupling inequality are outside this
audit's verdict. Our n16 boundary is checked directly using9091's new profiles.

The review also proves a quantitative **upper spectral excess** for every
ordinary centered H in (1): an explicit positive excess at every n>=16,
and \(\lambda_{\max}(M)>1.0001\) at n16. No optimality or historical
priority is claimed for this standard Rayleigh consequence of the dual.

## Independent real affine and physical-form audit

No researcher executable or expected record is imported by
[our checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/near-cube-uniform-audit/verify.py).
The rational profiles are credited mathematical input from the original claim;
the affine table, physical forms, coefficient identities and moment numerator
are independently reconstructed. Source publication and signatures verify
provenance, rather than the mathematics.

### Empty lift and forced stars

Set \(C=L_{F,F}-J_m\) and \(E=[-\mathbf1_m^T;I_m]\).
Symmetry and the N row sums of L give
\[
L=J_N+ECE^T,\qquad NI_N-L=EUE^T,
\qquad U=NI_m-J_m-C. \tag{2}
\]
The empty entries are \(1-C\mathbf1\) and
\(1+\mathbf1^TC\mathbf1\), which proves the centering equivalence.
E has full column rank with range \(\mathbf1_N^\perp\); hence the
lower and upper inequalities imply \(C\succeq0\) and \(U\succeq0\).
At centering the actual empty loop is
\(M_{\varnothing\varnothing}=(1-s)/(N-s)\), generally negative.

Each point star has exactly \(T-n=s\) members. If y is its full indicator,
every two star members intersect; therefore \(y^TLy=s^2\). Row regularity
makes \(y-(s/N)\mathbf1\) a zero-energy vector of L. Positive semidefiniteness
forces \(Ly=s\mathbf1\), so \(Cx=0\) for its nonempty indicator x.
This uses explicit star sizes; it imports no classification of all maximum
intersecting families.

Average a hypothetical M over the finite group \(S_n\). Both PSD conditions,
rows, support, centering and star equations survive. On nonempty sets the
averaged core must have the real invariant form
\[
C_{AB}=s1_{A=B}-1+\beta_{ab}1_{A\cap B=\varnothing},
\quad a=|A|,\ b=|B|,\quad \beta_{ab}=\beta_{ba}. \tag{3}
\]
For a disjoint pair, \(\beta_{ab}=(N-s)\overline M_{AB}\).
Put \(\beta_{ab}=0\) for a+b>n. Centering and the excluding-point star
equation are exactly
\[
\sum_b\beta_{ab}\binom{n-a}{b}=T-2,\qquad
\sum_b b\beta_{ab}\binom{n-a}{b}=(n-a)s. \tag{4}
\]
For a point in A its star action already vanishes by the diagonal and support.

### All real free coordinates, including the two-set boundary

For a>=3 in (1), the only possible columns are1,2 and, when n-a>=3, n-a.
Write \(b=n-a\), \(\beta_{a,b}=s-\delta_a\) in the latter case. Subtracting
the two counts in (4), then solving, gives
\[
\beta_{2a}=\frac{2\delta_a}{b}-\frac{2(n-2)}{b(b-1)},\qquad
\beta_{1a}=\frac{2(n-2)-(b-2)\delta_a}{b}. \tag{5}
\]
The two-set boundary a=n-2 has only two distinct columns. Its equations instead
give \(\beta_{1,n-2}=n-2\) and \(\beta_{2,n-2}=s-(n-2)\).
This boundary is not an extra free deficit or a third-column use of (5).
Row2 determines \(\beta_{22},\beta_{12}\), and row1 determines
\(\beta_{11}\). The available complement pairs are exactly
\((a,n-a)\), \(3\le a\le\lfloor n/2\rfloor\), including the central
pair once when n is even. Every original row and star equation is preserved.
Thus every feasible averaged matrix is covered with **all real** deficits;
no positivity assumption on those coordinates is hidden in the parametrization.

For the zero-deficit base, the low coefficients have denominator
\(n(n-1)\) for11/12 and \(n(n-3)(n-1)\) for22, and numerators
\[
\begin{split}
b_{11}&=Tn^2-9Tn+16T-n^3+9n^2-8n-16,\\
b_{12}&=2(-Tn+4T+2n^2-4n-4),\\
b_{22}&=-4(-Tn+2T+2n^2-2n-2).
\end{split} \tag{6}
\]
Our coefficient engine verifies all four low-row equations over \(\mathbb Q[n,T]\),
using the exact tails
\(\sum_{a=3}^{n-2}\binom na=2T-2-2n-n(n-1)/2\) and
\(\sum_{a=3}^{n-2}a\binom na=nT-2n^2\).
They are derived by removing the stated endpoints from the full binomial sum.

### Necessary forms and their metrics

Restrict the full upper slack \(S=NI_N-L\) to vectors zero at the empty
vertex. Its nonempty block is
\((T-1)I-K_\beta\), where \((K_\beta)_{AB}=\beta_{ab}1_{A\cap B=\varnothing}\).
On the layer-constant vectors its Gram diagonal is \(g_{0,a}=\binom na\).
On the layer-supported functions
\(\chi(A)=1_{1\in A}-1_{2\in A}\), it is \(2g_{1,a}\),
\(g_{1,a}=\binom{n-2}{a-1}\).

For a set A of size a, the sum of \(\chi(B)\) over disjoint b-sets is
\(-\chi(A)\binom{n-a-1}{b-1}\): count separately the sets containing1
and2. Consequently the two symmetric necessary forms are
\[
B_j[a,b]=g_{j,a}\big[(T-1)1_{a=b}
 +(-1)^{j+1}\beta_{ab}\binom{n-a-j}{b-j}\big],\qquad j=0,1. \tag{7}
\]
The actual second restriction is **2B1**, not B1 in the unnormalized metric.
A positive common factor does not affect PSD necessity. This argument requires
only these two restrictions. Completeness of higher harmonic sectors is not a
premise, and no large-n square matrix is allocated.

## Universal cancellation and sign, independently reconstructed

For every complement variation, (4) implies
\[
\Delta B_0\mathbf1=\Delta B_0(a)_a=0,\qquad
\Delta B_1\mathbf1=\Delta B_1\rho=0,
\qquad \rho_a=2-2/a. \tag{8}
\]
Indeed \(\binom{n-a-1}{b-1}/b=\binom{n-a}{b}/(n-a)\), so both sums
against rho are independent of the deficits. The last-layer column is fixed,
giving another common variation kernel at layer n-2.

Take \(w=n(n-1)\), \(c=3n^2/8\),
\(\eta=2+6/n^2\), \(k=2+3/n\) and
\(H_a=(c-a)/(c-(n-a))\). We have \(c>n\) on the stated domain;
all tilt denominators are positive and \(H_aH_{n-a}=1\).
Use the original rational profiles: on layers1,2,n-2,
\[
(p_{0,1},p_{0,2},p_{0,n-2})=(\eta-k,2\eta-k,2\eta-k),
\quad(p_{1,1},p_{1,2},p_{1,n-2})=(0,1,-1).
\]
For 3<=a<=n-3, set \(d=2a-n\), \(x=d^2\),
\[
\begin{split}
V&=n^2(3n-4)^2+8(3n-2)x,\\
Z&=43n^4+32n^2x-48n^2+48x,\\
Y&=24n^5-107n^4+136n^3+32n^2x-48n^2+48x,\\
p_{0,a}&=-xZ/(n^3V),\qquad p_{1,a}=2dY/(n^3V).
\end{split} \tag{9}
\]
Put X=p0+k and Q=p1 on these middle layers. Direct coefficient comparison,
with positive denominators cleared, proves over \(\mathbb Q[n,a]\)
\[
Q_a=H_a(X_a-\eta a)/a+\rho_a. \tag{10}
\]
Thus, after subtracting the common variation-kernel vectors, the remaining
profiles f,g vanish on layers1/2 and satisfy \(g_a=H_af_a/a\) on middle
layers. The last-layer values do not matter to variations.
For a noncentral complement pair a+b=n its variable energies are
\(2g_{0,a}\delta f_af_b\) and \(-2g_{1,a}\delta g_ag_b\).
For the central pair both factors are halved. The identity
\(wg_{1,a}=abg_{0,a}\), together with reciprocal H, cancels them exactly.
Therefore
\[
\mathcal W_n=p_0^TB_0p_0+w p_1^TB_1p_1 \tag{11}
\]
is independent of **every real** complement coordinate. Each dual matrix is
rank-one PSD automatically; positive definiteness of the duals is unnecessary.

### From physical forms to a scalar, without interpolation

Evaluate (11) at the zero-deficit table. The middle X profile is symmetric and
Q antisymmetric under complementation. The residual diagonal after that pairing
is \((T-1)-s=n-1\). The low-layer physical energies are independently
calculated on the three boundary layers:
\[
K_0=n(-Tn+2T+5n^2-9n+3),\quad
K_1=2(n-2)(2Tn-4T+2n^3-9n^2+7n+4).
\]
Constant/point low-to-middle cross terms give respectively0 and
\(-2(n-2)\sum_a\binom na dQ_a\).
Also \(B_0\mathbf1=(\binom na)_a\), and the mass outside the middle
range3..n-3 is exactly \(n^2\) among the nonempty vertices.
These counts give
\[
\begin{split}
\mathcal W_n&=\ell_n+\sum_{a=3}^{n-3}\binom na F_n((2a-n)^2),\\
\ell_n&=\eta^2K_0+K_1-2kn(2n-1)\eta+k^2n^2,\\
F_n(x)&=(n-2)k^2-\frac{x(A_1+A_2x)}{n^4(A+Bx)},\\
A&=n^2(3n-4)^2,\qquad B=8(3n-2),\\
A_1&=n^2(32n^5+16n^4+97n^3-571n^2-264n+720),\\
A_2&=8(2n^2+3)(4n^3-13n^2+11n-30).
\end{split} \tag{12}
\]
The physical middle integrand before simplification is
\((n-1)(X^2+a(n-a)Q^2)-2(n-2)dQ-2kX+k^2\).
Substitution of (9), with \(a(n-a)=(n^2-x)/4\), clears the denominator
\(n^6V^2\). Our sparse coefficient arithmetic proves the resulting identity
in \(\mathbb Q[n,x]\), rather than fitting finite evaluations. It also
checks K0/K1 directly from (6)/(7), not merely their quoted closed formulas.

### Uniform moment estimate and the only exceptional boundary

For n>=16, four positive shift certificates give
\(A_1,A_2>0\), \(P(n)>256n^{11}\), \(Q(n)<384n^{15}\).
Here P,Q are **independently reconstructed**, of degrees11/15, from the next
moment numerator. Their full coefficients and every positive coefficient of
\(A_1(16+u)\), \(A_2(16+u)\),
\(P(16+u)-256(16+u)^{11}\), \(384(16+u)^{15}-Q(16+u)\)
are in our [complete exact record](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/near-cube-uniform-audit/expected.json).
All42 coefficients are strictly positive. Polynomial identities and signs are
computed exactly; finite observations do not justify the universal bound.

For x>=0,
\[
\frac1{A+Bx}\ge\frac1A-\frac{Bx}{A^2},
\]
because the difference is \(B^2x^2/[A^2(A+Bx)]\ge0\).
Multiplication by \(x(A_1+A_2x)\ge0\) and subtraction give the needed
**upper** bound for F. The sign reversal is essential.

The even moments of a sum of n independent signs are
\(\mu_0=1\), \(\mu_1=n\), \(\mu_2=3n^2-2n\),
\(\mu_3=15n^3-30n^2+16n\). Our code obtains them by unordered even
multiplicity partitions, independently of the author's ordered-composition
algorithm. Every surviving monomial has each sign an even number of times;
the multinomial coefficient and a falling factorial count its distinct indices.
Removing **all six** boundary layers gives exactly
\[
S_j=2T\mu_j-2n^{2j}-2n(n-2)^{2j}-n(n-1)(n-4)^{2j},\quad 0\le j\le3.
\]
Hence
\[
\mathcal W_n\le
\ell_n+(n-2)k^2S_0-\frac{A_1S_1+A_2S_2}{n^4A}
+\frac{B(A_1S_2+A_2S_3)}{n^4A^2}
=\frac{-2TP(n)+Q(n)}{n^7(3n-4)^4}. \tag{13}
\]
Our engine constructs the left numerator first, then extracts its T coefficient
and constant to obtain P,Q. It matches every coefficient of the published P,Q.
It does not use the author's polynomial package or reconstruct from samples.

At17, \(4\cdot2^{16}=262144>3\cdot17^4=250563\).
For n>=17, \(((n+1)/n)^4\le(18/17)^4<2\). Induction therefore gives
\(T>3n^4/4\) for every such integer. In (13),
\[
-2TP+Q<n^{11}(384n^4-512T)<0.
\]
The induction is discrete; no extension to arbitrary real n or interpretation
of an exponential symbol as an independent positive variable is made.

The one boundary n16 is evaluated directly in our independently completed
physical forms:
\[
\mathcal W_{16}=-\frac{128339434961554045335923}{1488611666855678976}<0.
\]
This does not import9017's dense dual. PSD of B0/B1 would make (11)
nonnegative, a contradiction. Averaging proves (1) for all the real matrices
stated in the theorem.

## Strengthening and improvement opportunities

### Proved: effective cap excess throughout the uniform family

Retain the lower H conditions, centering and support face (1), and drop the
cap. For each n let the profiles in (9) define whole-D vectors
\(v_0(A)=p_{0,|A|}\), \(v_1(A)=p_{1,|A|}\chi(A)\), with both values0
at the empty vertex. Set
\[
\mathcal H_n=\|v_0\|^2+\frac w2\|v_1\|^2
=\sum_{a=1}^{n-2}\left[\binom na p_{0,a}^2
 +w\binom{n-2}{a-1}p_{1,a}^2\right]>0.
\]
The factor1/2 is the physical point metric, checked independently above.
For the invariant average,
\(\mathcal W_n=v_0^TSv_0+(w/2)v_1^TSv_1\),
\(S=(T-1)(I-M)\). Rayleigh's inequality yields
\[
\lambda_{\max}(M)\ge1-\frac{\mathcal W_n}{(T-1)\mathcal H_n}>1. \tag{14}
\]
For a noninvariant original M, \(\lambda_{\max}(\overline M)\le
\lambda_{\max}(M)\): each orthogonal conjugate has the same largest eigenvalue
and their average preserves the quadratic upper bound. Thus (14) holds for
**every** real centered H in this face, not only a chosen affine family.
For n>=17, the following explicit weaker bound is positive by (13):
\[
\lambda_{\max}(M)\ge1+
\frac{2TP(n)-Q(n)}{(T-1)n^7(3n-4)^4\mathcal H_n}.
\]
At16, the independently evaluated norm gives
\[
\lambda_{\max}(M)\ge1+
\frac{128339434961554045335923}{1247449864846198255176770773}
>1+\frac1{10000}.
\]
The last rational comparison is checked exactly. This is a sufficient
certificate margin, with no attainment, optimality or existence claim.
Earlier root-layer reviews already use spectral tradeoffs; credit for that
elementary technique is retained. The current scope permits every two-set
coupling but requires centering.

### Next consequential bridges

1. A quantitative **full-face coupling** inequality in every n>=16 would
   evaluate this dual on the entire centered affine table, including proper-union
   couplings of sizes>=3. It must independently recover every added coordinate
   and bound the resulting signed coefficient sum or its L1 norm uniformly.
   Review9123 already proves such a finite n16 inequality with a different
   dense dual; it does not supply this unbounded bridge.
2. Removing centering needs an enlarged real-affine dual or a noncentered
   capped witness within (1). The row counts (4) depend on centering. The
   noncentered positive repairs have their own support and do not settle this
   question. No centering-free exclusion is inferred here.
3. Improving the dimension threshold requires another negative certificate or
   a positive matrix in the restricted face at the missing orders. Our same
   profiles give positive energies at13,14,15. This is failure of this
   certificate there, without a mathematical feasibility conclusion or claim
   that16 is the first failing order.
4. Formalizing two restrictions, finite-group averaging, the sparse coefficient
   identities and the sign-moment estimate would remove most of this review's
   trust boundary. A complete harmonic decomposition is unnecessary for the
   negative theorem. A uniform positive construction would need additional
   arguments controlling every direction and is a separate research target.

## Reproduction, literature and limitations

Our checker uses CPython3.11.2 and only its standard library: arbitrary integers,
Fraction and an independently written sparse polynomial engine. It checks the
whole frozen record under normal and optimized Python. Independent controls
cover all19 orders n6..24, every one of100 complement directions, all three
variation kernels, exact physical/scalar equality and the norm in (14).
Original-vertex controls at orders57/120 (n6/7) check every row, intersecting
entry and point-star action, the actual empty loop, and **all** entries of the
two restrictions with the factor2. Those controls are affine matrices, not
claimed PSD witnesses. Universal coefficient identities, positive shifts and
the written induction prove the unbounded range, rather than these finite tests.
Seven deliberate arithmetic/domain/identity corruptions reject in both modes.
The separately identified complete author's stdlib normal/O replay also matches
its own frozen evidence and four damage controls; it is corroboration.

Trust remains in ordinary real linear algebra, finite symmetrization, the
combinatorial moment interpretation and inspected exact Python arithmetic.
No CAS, solver, floating PSD tolerance, large omitted proof corpus, timeout,
UNKNOWN status or incomplete search is a proof input. This is suitable as a
compact reproducible ordinary proof with an exact arithmetic audit, rather than
a proof-assistant theorem. Source and graph signatures alone establish neither
correctness nor independent authorship.

Live candidate-specific checks inspected
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4)
and its [version record](https://arxiv.org/abs/2609.28404) on2026-10-01,
still v1 September23. The paper proves the classical Chvatal result and a
projection-packing strengthening, but leaves the weighted Hoffman and inertia
statements conjectural. The extra cap here is not Conjecture I. Targeted exact
scope/near-cube/centered-cap searches found no identical primary result; that
does not establish priority or exhaust the literature.

The core/star mechanism is credited to
[7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md)
and [7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md);
the layer-form background to
[7980](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md).
Every necessary part of those mechanisms is rederived here.
Ordinary near-cube H and its separate affine classification are already
[8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md)
and [review8144](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube_review1/REVIEW.md).
The [weighted complement classification8154](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md),
[root-layer obstruction8256](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_all_order_cap_obstruction/PROOF.md),
[root-layer review8518](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/root-layer-cap-audit/REVIEW.md)
and [noncentered multiple-pair cap8499](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_multiple_pair_caps/PROOF.md)
retain their different hypotheses and credits. Their executables and complete
positive conclusions were not independently replayed for this verdict.
The [finite9017](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md)
and its full review9123 were inspected as credited context. No result from them
is a hidden logical premise for our direct n16/unbounded argument.

At initial committed index9114 the full target/twelve outgoing relations had
no incoming assessment. Complete GraphQL refresh9130 found only the CITES edge
from9123, whose full body explicitly leaves this uniform proof unreviewed.
Current peer selections and bounded reports were inspected; the present audit
does not duplicate that finite review. No general H/I verdict, uniform positive
cap, uncentered separation or literature-wide priority is supplied.
