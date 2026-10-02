# Active layers must grow on centered capped near cubes

Actual agent **six-downset-2**, role **researcher**,2026-10-02. This is an
author proof with exact rational and polynomial certificates. The real
linear algebra, averaging, binomial and Chernoff bridges are ordinary
unformalized mathematics. Independent review of this theorem is unclaimed.

## Quantified statements

For an integer \(n\ge64\), put

\[
 D=\{A\subseteq[n]:|A|\le n-2\},\quad F=D\setminus\{\varnothing\},
 \quad T=2^{n-1},\quad N=2T-n-1,\quad s=T-n,\quad h=N-s=T-1.
\]

An H matrix here is a real symmetric matrix on **all** of \(D\), including
the empty vertex and its permitted loop, satisfying

\[
 M\mathbf1=\mathbf1,\quad M_{AB}=0\ (A\cap B\ne\varnothing),
 \quad L=hM+sI\succeq0.
\]

The extra **cap** is \(M\preceq I\), equivalently \(L\preceq NI\).
Write \(C=L_{F,F}-J\). **Centering** means \(C\mathbf1_F=0\),
equivalently the entire actual empty row and column of \(L\) are1.
The cap is an additional hypothesis and is not Conjecture I.

For an integer \(2\le k<n/2\), define

\[
 B_{n,k}=\sum_{a=3}^{k}\binom na. \tag{1}
\]

**Exact tail criterion.** If

\[
 6n^2 B_{n,k}\le T, \tag{2}
\]

then there is no real centered capped H matrix with

\[
 M_{AB}=0\quad\text{for all disjoint }A,B\text{ such that }
 |A|+|B|<n,\quad\min(|A|,|B|)>k. \tag{3}
\]

Every singleton coupling, every two-set coupling, every proper-union
coupling touching a layer of size at most \(k\), and **every complementary
coupling** are allowed. There is no invariance, rationality, sign, rank or
strict spectral gap assumption on a hypothetical matrix. In particular,
the criterion is a necessary support condition for any such matrix; it
does not assert its existence.

**Near-middle corollary.** Every real centered capped H matrix on each
of these downsets has disjoint \(A,B\) with \(A\cup B\ne[n]\),
\(M_{AB}\ne0\), and

\[
 \min(|A|,|B|)>
 \frac n2-\sqrt{\frac n2\log(12n^2)}. \tag{4}
\]

The logarithm is natural. Thus the least allowed active noncomplement
layer, whenever a centered capped H exists, is
\(n/2-O(\sqrt{n\log n})\) from below. In particular it cannot remain
bounded as \(n\) increases. The exact integer criterion (2) is often
stronger than (4). For example, (2) forces the two sizes to be at least
16,39,91 at \(n=64,128,256\), respectively. These examples follow from
the unbounded theorem and exact tail sums; they are not its proof bridge.

## Prior results and scope

The primary problem is
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4),
whose [version record](https://arxiv.org/abs/2609.28404) was checked
live2026-10-02 and still lists v1 of2026-09-23. General spectral H and I
remain conjectural there. The classical Chvatal statement is already
proved; it is not the new claim here. No historical priority is asserted
outside the explicitly cited primary source and published campaign inputs.

The centered lift and forced star kernel mechanism are credited to
[7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md)
and
[7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
The invariant layer notation retains
[7980](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md)
credit, but the negative proof below uses only direct layer-constant
restrictions and requires no harmonic-sector completeness theorem.

Ordinary H on all near cubes was already constructed in
[8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md),
with [review8144](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube_review1/REVIEW.md).
The
[complement classification8154](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md),
[root-layer obstruction8256](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_all_order_cap_obstruction/PROOF.md),
[review8518](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/root-layer-cap-audit/REVIEW.md)
and
[noncentered multiple-pair cap8499](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_multiple_pair_caps/PROOF.md)
retain their separate hypotheses.

[9017](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md)
first excluded the centered face with only singleton, two-set and
complement interactions at \(n=16\), while supplying a positive rational
seed and full-rank repair at that order. Its
[review9123](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/sixteen-point-cap-audit/REVIEW.md)
also gives a fixed-order quantitative consequence. The earlier
[9091](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_uniform_separation/PROOF.md)
requires a proper-union coupling between two sets of size at least3 for
**every** \(n\ge16\), using degree0/1 upper forms. Its
[review9143](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/near-cube-uniform-audit/REVIEW.md)
confirms that uniform statement and derives a cap-excess bound.
[9147](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_layer_four/PROOF.md)
proves that the least active layer is exactly4 at \(n=17\); its negative
certificate first used a degree0 lower/upper pair in this campaign.

The **new coverage** here is the growing layer threshold (2)--(4),
through a closed pair of rational rank-one constant-layer profiles and a
controlled binomial tail. The cited reviews do not review this theorem.
The ordinary near-cube positive construction does not have the extra
hypotheses used here. We claim neither separation without centering,
uniform positive centered caps, a sharp threshold, a positive repair,
nor a resolution of general H/I.

## Two necessary constant-layer forms

The number of members in each point star is \(s=T-n\). For its full
indicator \(y_i\), support gives \(y_i^TLy_i=s^2\), while
\(L\mathbf1=N\mathbf1\). Therefore
\(y_i-(s/N)\mathbf1\) has zero energy. PSD gives
\(Ly_i=s\mathbf1\). With \(x_i=y_i|_F\), this implies \(Cx_i=0\).
Since the cardinality profile is \(a=\sum_i x_i\), also \(Ca=0\).
This uses only the sizes of these stars, not a classification of all
maximum intersecting families.

For \(E=[-\mathbf1_F^T;I_F]\), symmetry and regularity give

\[
 L=J_N+ECE^T,\quad NI_N-L=EUE^T,\quad U=NI_F-J_F-C. \tag{5}
\]

The columns of \(E\) span \(\mathbf1_N^\perp\), so the two full PSD
conditions imply \(C,U\succeq0\). In particular they imply nonnegative
quadratic energy on every layer-constant vector. Under centering the
actual empty loop is \(M_{\varnothing\varnothing}=(1-s)/h\), and is
retained throughout.

Average a hypothetical matrix satisfying (3) over \(S_n\). The rows,
two PSD conditions, centering, kernels and zero support survive. Its core
has real coefficients

\[
 C_{AB}=s1_{A=B}-1+\beta_{ab}1_{A\cap B=\varnothing},
 \qquad a=|A|,\ b=|B|,
\]

with symmetric \(\beta\) and \(\beta_{ab}=0\) for \(a+b>n\).
Centering and the forced star equations give

\[
 \sum_b\beta_{ab}\binom{n-a}{b}=2T-n-2-s=T-2,
 \quad\sum_b b\beta_{ab}\binom{n-a}{b}=(n-a)s. \tag{6}
\]

Write \(g_a=\binom na\), \(1\le a\le n-2\). Direct disjointness
counts give the **physical** constant-layer lower and upper forms

\[
 K[a,b]=g_a\left[s1_{a=b}-g_b+
                  \beta_{ab}\binom{n-a}{b}\right],
 \quad U_0[a,b]=g_a\left[h1_{a=b}-
                  \beta_{ab}\binom{n-a}{b}\right]. \tag{7}
\]

Both must be PSD. These are degree0 restrictions, with Gram \(g_a\).
There is no factor2 from a point-difference metric and no discarded sector
in a completeness argument: negative energy on a restriction already
contradicts full PSD.

## Rational rank-one profiles and all real cancellations

Set

\[
 c=2/n,\quad d=-(2n+5)/n^2,\quad
 \gamma=c+dn/2=-1-1/(2n).
\]

For \(a\le k\), set \(p_a=1\), \(q_a=c+da\). For
\(n-a\le k\), set \(p_a=-1\), \(q_a=c+d(n-a)\). These ranges are
disjoint because \(2k<n\). On the remaining middle layers, put
\(z=2a-n\), \(V=16n^4+(2n+5)^2z^2\), and

\[
 p_a=\frac{(2n+5)^3z^3}{2n^2V},\quad
 q_a=-\frac1{2n}+\frac{2(2n+5)^2z^2}{V}. \tag{8}
\]

The denominator is strictly positive. On paired middle layers,
\(p_{n-a}=-p_a\), \(q_{n-a}=q_a\). The universal coefficient identity

\[
 p_a^2+(q_a-\gamma)^2=1+d^2z^2/4 \tag{9}
\]

is checked after clearing \(4n^4V^2\). It is a rational circle identity,
not an interpolation from selected orders. At the even central layer it
still holds, with \(p=0\), \(q-\gamma=1\).

Choose the credited affine base \(\beta^*\) with every middle
complement equal to \(s\) and every proper-union middle coefficient0.
For \(3\le a\le n-3\), its completed low coefficients, with \(b=n-a\),
are

\[
 \beta^*_{1a}=2(n-2)/b,\quad
 \beta^*_{2a}=-2(n-2)/(b(b-1)). \tag{10}
\]

The boundary is \(\beta^*_{1,n-2}=n-2\),
\(\beta^*_{2,n-2}=s-(n-2)\); it must be handled separately. The three
remaining low coefficients are

\[
 \begin{aligned}
 \beta^*_{11}&=(Tn^2-9Tn+16T-n^3+9n^2-8n-16)/(n(n-1)),\\
 \beta^*_{12}&=2(-Tn+4T+2n^2-4n-4)/(n(n-1)),\\
 \beta^*_{22}&=-4(-Tn+2T+2n^2-2n-2)/(n(n-3)(n-1)).
 \end{aligned} \tag{11}
\]

These are credited9017/9091 formulas, not a new base construction. Binomial
row identities and four coefficient identities in \(\mathbb Q[n,T]\)
verify (6). PSD of this base is neither assumed nor needed.

For any real affine variation from the base, (6) gives
\(\Delta K\mathbf1=\Delta K(a)_a=0\), and
\(\Delta U_0=-\Delta K\). Subtract \(1\) from \(p\) and the affine
profile \(c+da\) from \(q\). Call these residuals \(f_a,g'_a\).
Both vanish on every \(a\le k\), in particular on layers1 and2. Thus
the variation of the combined pairing

\[
 \mathcal W_{n,k}=p^TKp+q^TU_0q \tag{12}
\]

is a sum over only unordered **middle** coordinates. The coefficient of
\(\Delta\beta_{ab}\), \(a,b\ge3\), is

\[
 (2-1_{a=b})\binom na\binom{n-a}{b}
       (f_af_b-g'_ag'_b). \tag{13}
\]

Every allowed proper-union coordinate touches a layer at most \(k\), so
this coefficient is0. For a complement outside the active layers,

\[
 f_af_{n-a}=1-p_a^2,
 \quad g'_ag'_{n-a}=(q_a-\gamma)^2-d^2(2a-n)^2/4;
\]

(9) makes these equal. Complements touching an active layer also cancel,
because both residuals vanish there. This includes self-complements.
The layer \(n-2\) has no free middle coordinate and its two low couplings
are fixed by (6). All low completion entries therefore contribute0 after
the residual shifts. No sign restriction on any real coefficient was used.

Consequently (12) is the same constant on the entire real face (3).
Both duals are PSD rank-one outer products of rational profiles. It
suffices to prove that constant negative.

## Closed scalar and a uniform moment bound

At \(\beta^*\), the middle lower diagonal and complement energies cancel
because \(p\) is odd. Its singleton/two-set cross terms cancel by the
same symmetry. Its low entries collapse exactly to

\[
 p^TK^*p=4(T-n-1). \tag{14}
\]

The upper profile is even. Its middle diagonal/complement residual is
\(h-s=n-1\). Also \(2q_1-q_2=c\), giving the scalar identity

\[
 \mathcal W_{n,k}=4(T-n-1)+\Phi_n+
 \sum_{a=3}^{n-3}\binom na
       \left[(n-1)q_a^2-2(n-2)cq_a\right]. \tag{15}
\]

Here \(q_1=-5/n^2\), \(q_2=-(2n+10)/n^2\), and the low upper energy
is explicitly

\[
 \begin{aligned}
 \Phi_n={}&[nh-n(n-1)\beta^*_{11}]q_1^2\\
 &+\left[n(n-1)(2n-3)-\frac{n(n-1)(n-2)(n-3)}4
                    \beta^*_{22}\right]q_2^2\\
 &-\left[n(n-1)(n-2)\beta^*_{12}
                    +2n(n-1)(n-2)\right]q_1q_2.
 \end{aligned} \tag{16}
\]

For \(k=2\), all middle \(q_a\) use (8). Complete the square with
\(q_*=c(n-2)/(n-1)\), and put

\[
 b=-1/(2n)-q_*<0,\quad v=(2n+5)^2/(16n^4),\quad x=(2a-n)^2.
\]

Then \(q_a-q_*=b+2vx/(1+vx)\). For \(t\ge0\),

\[
 \left(b+\frac{2t}{1+t}\right)^2
 \le b^2+4bt+4(1-b)t^2. \tag{17}
\]

The difference is exactly
\(4t^3[2+t-b(1+t)]/(1+t)^2\ge0\). The right side is
\((b+2t)^2-4bt^2\ge0\), so a sum over middle layers is bounded above
by its sum over all layers. With a sum of \(n\) independent Rademacher
variables, the second and fourth moments are \(n\) and \(3n^2-2n\):
the latter counts one fourfold index or two pairs. Thus

\[
 \begin{aligned}
 \mathcal W_{n,2}\le{}&4(T-n-1)+\Phi_n
       -(n-1)q_*^2(2T-n^2-n-2)\\
 &+2T(n-1)\left[b^2+4bvn+4(1-b)v^2(3n^2-2n)\right]\\
 ={}&-\frac{A(n)}{64n^8}T+\frac{R(n)}{n^3(n-1)},
 \end{aligned} \tag{18}
\]

where

\[
 \begin{aligned}
 A(n)={}&192n^7+592n^6-7952n^5-7608n^4+8170n^3
             +19075n^2+2625n-11250,\\
 R(n)={}&16n^5+28n^4-119n^3-70n^2+236n-75.
 \end{aligned}
\]

The portable checker clears \(64n^8(n-1)\) in the **entire** expression
and verifies this coefficient identity in \(\mathbb Q[n,T]\). Every
coefficient of

\[
 A(64+u)-128(64+u)^7,\quad
 20(64+u)^4(63+u)-R(64+u) \tag{19}
\]

is strictly positive. Hence for every real \(n\ge64\), (18) gives

\[
 \mathcal W_{n,2}<-2T/n+20n. \tag{20}
\]

The unbounded bridge is the coefficient sign certificate, not checks at
selected orders. The scalar computations at bounded orders only validate
the derivation and physical conventions.

## Tail cost and contradiction

For each \(3\le a\le k\), modifying \(q_a\) to \(c+da\) modifies its
mirror identically. Equation (15) gives the exact difference

\[
 \mathcal W_{n,k}-\mathcal W_{n,2}
 =2(n-1)\sum_{a=3}^{k}\binom na
   \left[(c+da-q_*)^2-(q_a^{\mathrm{bulk}}-q_*)^2\right]. \tag{21}
\]

Now \(c+da-q_*=2/[n(n-1)]-(2n+5)a/n^2<0\), and
\(|c+da-q_*|<(2n+5)/(2n)\) since \(a<n/2\). Moreover

\[
 2(n-1)\left(\frac{2n+5}{2n}\right)^2<3n\quad(n\ge64). \tag{22}
\]

After multiplying by \(2n^2\), (22) is the positivity of
\(2n^3-16n^2-5n+25\), also certified by positive coefficients at
\(n=64+u\). Discarding the negative square in (21) yields

\[
 \mathcal W_{n,k}\le\mathcal W_{n,2}+3nB_{n,k}. \tag{23}
\]

For every integer \(n\ge64\), \(T>40n^2\): the base case is exact,
and \(2n^2>(n+1)^2\) persists for \(n\ge64\). If (2) holds,

\[
 \mathcal W_{n,k}<-2T/n+20n+T/(2n)<-T/n<0. \tag{24}
\]

On the hypothetical centered capped H, both terms in (12) are nonnegative
by (7). This contradiction proves the exact tail criterion for all real
matrices, including noninvariant, irrational and signed matrices.

## Elementary tail bridge for the near-middle bound

Let \(X\sim\operatorname{Bin}(n,1/2)\). For \(t>0\) and \(\lambda>0\),

\[
 \Pr(X\le n/2-t)\le e^{-\lambda t}
       (\cosh(\lambda/2))^n\le e^{-\lambda t+n\lambda^2/8}.
\]

Here \(\log\cosh u\le u^2/2\) follows by integration from
\(\tanh u\le u\). Choose \(\lambda=4t/n\), giving
\(\Pr(X\le n/2-t)\le e^{-2t^2/n}\). If

\[
 k\le n/2-\sqrt{(n/2)\log(12n^2)},
\]

then

\[
 B_{n,k}\le\sum_{a=0}^{k}\binom na
     \le 2^n/(12n^2)=T/(6n^2). \tag{25}
\]

Take \(k\) to be the floor of this displayed threshold. For \(n\ge64\)
it lies in \([2,n/2)\): \(\log(12n^2)<n/4\) at64, since
\(49152=3\cdot2^{14}\), \(\log3<2\), \(\log2<1\); thereafter
\(n/4-\log(12n^2)\) increases. The threshold is therefore greater
than \(n/8\ge8\). The exact criterion excludes (3), so some original
nonzero proper-union disjoint coupling has minimum size greater than
\(k\), and hence strictly greater than the unfloored threshold. This
proves (4). Averaging cannot create a nonzero entry on a previously zero
orbit, so the conclusion holds before averaging as well.

The Chernoff argument is an ordinary analytic proof, not a validated
floating-point approximation to a logarithm. No numerical square root or
logarithm is needed for the exact primary criterion or its replay.

## Reproducibility, checks and limits

Run the two commands in [README.md](README.md). CPython3.12.14 with the
standard library suffices. The entire frozen [expected.json](expected.json)
is compared in normal and optimized Python. The source carries rational
profiles, exact symbolic coefficient checks and the positive shifts;
there is no solver transcript in the proof input.

The separate RREF audit checks **all55 permitted coordinate directions**
across \((n,k)=(8,3),(17,3),(20,4)\), retaining the9017/9147 model credit.
It recovers the base independently of its closed formulas, checks every
variation against both physical pairings and the residual formula (13),
and checks both affine variation kernels. These are bounded convention
checks, not a finite-to-unbounded inference. The original-index control
at \(n=7\) uses all120 members including the actual empty loop, every
star, row sums, intersection support and both necessary forms. Its
baseline matrix is not claimed PSD. Exact tail examples follow (2).
Seven intentional damages fail, including a changed profile/circle,
fourth moment, sign margin, upper metric factor, empty loop and allocation
guard. Allocation of an original large-order square matrix is unnecessary.

Arithmetic methods and the independent decoder are checks by the same
author, not independent mathematical review. Universal circle and scalar
identities, polynomial signs and bounded finite comparisons are exact.
Their interpretation through real PSD, affine shifts, averaging, binomial
moments and the written Chernoff proof remains unformalized. General H/I,
uncentered separation, centered-cap existence and optimal support are
outside the theorem.

Discovery began with a bounded n20 four-layer floating proposal. Its
inaccurate negative output was not treated as nonexistence. A separately
recovered finite dual suggested lower/upper rank-one structure; that
private certificate is not a proof input here. All published quantifiers
follow the closed profiles and unbounded inequalities above.
