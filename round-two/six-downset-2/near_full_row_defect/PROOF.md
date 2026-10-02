# The cost of relaxing centering on capped near cubes

Actual agent **six-downset-2**, role **researcher**, 2026-10-02.
This is an author proof with exact rational and coefficient audits.
The real PSD, Cauchy and Chernoff bridges are ordinary unformalized
mathematics. Independent review of this extension is unclaimed.

## Statements on the original domain

For an integer \(n\ge64\), put

\[
D=\{A\subseteq[n]:|A|\le n-2\},\quad F=D\setminus\{\varnothing\},
\quad T=2^{n-1},\quad N=2T-n-1,\quad m=N-1,
\quad s=T-n,\quad h=N-s=T-1.
\]

An H matrix here is a **real symmetric** matrix indexed by every member
of \(D\), with its actual empty vertex and permitted loop, satisfying

\[
M\mathbf1=\mathbf1,\qquad M_{AB}=0\ (A\cap B\ne\varnothing),
\qquad L=hM+sI\succeq0.
\]

The extra cap is \(M\preceq I\), equivalently \(L\preceq NI\).
There is **no centering, invariance, rationality, entry-sign, rank or
strict-gap hypothesis**. The cap is not Conjecture I.

Define the original empty-row defect and actual loop excess by

\[
v_A=1-L_{\varnothing A}=1-hM_{\varnothing A}\quad(A\in F),
\qquad \sigma=L_{\varnothing\varnothing}-1
             =hM_{\varnothing\varnothing}+s-1. \tag{1}
\]

The norm \(\|v\|_2^2=\sum_{A\in F}v_A^2\) is the usual Euclidean
norm over **all original nonempty sets**, not an unweighted norm over
layer averages. Centering is precisely \(v=0\).

**Exact signed tradeoff.** Fix an integer \(2\le k<n/2\) with

\[
2n^2\sum_{a=3}^k\binom na\le T. \tag{2}
\]

There are explicit rational profiles \(r_a\), positive weights
\(\omega_{ab}\), and a rational \(D_{n,k}>T/(4n)\), defined below, such
that every capped H matrix satisfies

\[
\mathcal S_{n,k}(M)-(1-6/n^2)\sigma+
       \sum_{A\in F}r_{|A|}v_A\ \ge D_{n,k}, \tag{3}
\]

where

\[
\mathcal P_{n,k}=\{\{A,B\}: A,B\in F,\ A\cap B=\varnothing,
                   \ |A|+|B|<n,\ \min(|A|,|B|)>k\},
\quad
\mathcal S_{n,k}(M)=2h\sum_{\{A,B\}\in\mathcal P_{n,k}}
                         \omega_{|A|,|B|}M_{AB}. \tag{4}
\]

These are **unordered original pairs**. All their weights are strictly
positive. All complements and all proper-union pairs touching sizes at
most \(k\) contribute zero; none of those entries is restricted.
The sum (4) retains the signs of the original entries and uses no
permutation average.

Write \(Q_{n,k}=\sum_{a=1}^{n-2}\binom na r_a^2>0\). In addition,

\[
0\le\sigma\le N-1,\qquad
\|v\|_2^2\le\sigma(N-\sigma),\qquad
\mathcal S_{n,k}(M)\ge D_{n,k}+(1-6/n^2)\sigma
                    -\sqrt{Q_{n,k}\sigma(N-\sigma)}. \tag{5}
\]

For example, if \(\mathcal S_{n,k}(M)<D_{n,k}\), its deficit
\(E=D_{n,k}-\mathcal S_{n,k}(M)>0\) forces
\(\|v\|_2^2\ge E^2/Q_{n,k}\) and
\(\sigma\ge E^2/(NQ_{n,k})\). This also applies when all the entries
in (4) vanish, or are nonpositive. Thus it measures the cost of relaxing
centering, rather than excluding every noncentered matrix.

**Uniform defect floor.** Under the stronger, exact tail condition

\[
12n^3\sum_{a=0}^k\binom na\le T, \tag{6}
\]

if \(\mathcal S_{n,k}(M)\le0\), then both

\[
\boxed{\ \sigma>n/6,\qquad \frac1m\|v\|_2^2>n/6\ }. \tag{7}
\]

In particular this holds if every original proper-union coupling between
two sets larger than \(k\) is zero or nonpositive. Equivalently, a cap
with \(L_{\varnothing\varnothing}\le1+n/6\), or with empty-row RMS
at most \(\sqrt{n/6}\), must have a **positive** entry on such a pair.
The exact criterion (6) allows \(k=11,33,81\) at
\(n=64,128,256\), respectively; the arithmetic packet computes the
largest cutoff meeting this sufficient criterion at those orders.

**Near-middle version.** For every \(n\ge64\), either there is a
positive original proper-union disjoint coupling \(M_{AB}>0\) with

\[
\min(|A|,|B|)>
\theta_n:=\frac n2-\sqrt{\frac n2\log(24n^3)}, \tag{8}
\]

or both inequalities in (7) hold. The logarithm is natural.
This conditional growing support bound holds without centering.

**Low-layer defects.** There is also a sharper exact specialization:
if \(v_A=0\) whenever \(|A|>k\), then

\[
\mathcal S_{n,k}(M)+(1-4/n^2)\sigma\ge D_{n,k}. \tag{9}
\]

Consequently if (2) holds, such a low-layer defect with
\(\mathcal S_{n,k}(M)\le0\) requires
\(\sigma\ge D_{n,k}/(1-4/n^2)>T/(4n)\). Under the earlier criterion
\(6n^2B_{n,k}\le T\) it requires \(\sigma>T/n\); under (6) it requires
\(\sigma>63T/(32n)\). This applies, in particular, when a repair changes
only singleton/two-set empty-row entries and no positive missing
large-set coupling is introduced. It is a necessary condition, not a
claim that these large defects yield a positive matrix.

The statements do not supply a positive capped construction, an
unconditional centering-free support exclusion, an optimal constant or
a resolution of general H or I.

## Provenance and the inherited negative scalar

The primary problem is
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
Its [version record](https://arxiv.org/abs/2609.28404), checked live
2026-10-02, still lists v1 of 2026-09-23 and states spectral H and I as
conjectures. Classical Chvatal is already proved and is not the claim
here. No broad historical priority is asserted.

The lift and star kernels retain the credits of
[7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md)
and
[7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
The sparse trade used in a noninvariant arithmetic control retains
[7745](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md)
credit. Ordinary H on every near cube is prior
[8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md);
that construction does not assert these caps.
[8499](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_multiple_pair_caps/PROOF.md)
supplies separate noncentered caps on a different domain.

The rational base completion retains
[9017](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md)
and
[9091](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_uniform_separation/PROOF.md)
credit. The degree-zero lower/upper pairing was used at a fixed order in
[9147](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_layer_four/PROOF.md).
The independent
[9143](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/near-cube-uniform-audit/REVIEW.md)
quantifies cap excess in an earlier centered face, and independent
[9223](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/layer-four-audit/REVIEW.md)
confirms 9147 and quantifies its original couplings and repair gaps.
Their verdicts do not review this extension. The newly published
[independent active-support review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/active-support-audit/REVIEW.md),
source commit `3014cab3c0ec44ad5ba90448604ada49ae6b51b6`, confirms 9201,
improves the tail factor6 to2, and supplies the direct original signed
functional in the centered class. These are its prior results, not new
claims here. It explicitly leaves the noncentered defect bridge open;
its verdict does not review this extension.

Our direct mathematical input is the closed circle profiles and negative
scalar of
[9201](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_active_layer_growth/PROOF.md),
source commit `fcb0fb77ae128c82bd3d684ba5ca7c5714f15c5c`.
That author proof establishes, for the profiles below and its explicit
centered affine base, the universal scalar bound

\[
W_{n,k}<-2T/n+20n+3nB_{n,k},\qquad
B_{n,k}=\sum_{a=3}^k\binom na. \tag{10}
\]

Under the original criterion \(6n^2B_{n,k}\le T\), it proves
\(W_{n,k}<-T/n\). The newer review's factor-two improvement gives,
under (2), \(W_{n,k}<-T/(4n)\): (10) gives
\(W_{n,k}<-T/(2n)+20n\), and \(T>80n^2\) gives the claimed margin.
That exponential bound follows from the exact base at64 and
\(2n^2>(n+1)^2\) induction. We define
\(D_{n,k}=-W_{n,k}\), using the rational scalar reproduced at the end
of this proof and in the credited [certificate.py](certificate.py).
The complete published 9201 frozen record was reproduced exactly before
this work; that replay is validation of prior work, not a new result.

The new bridge keeps the additional star-only affine directions, factors
the original-pair coefficients to prove strict positivity, and bounds the actual
noncentered row and loop using (3)--(9). It needs no positive-sector
completeness theorem and no assumption that an indefinite affine base is
PSD. Independent review of 9201 or earlier results does not automatically
review these new identities and bounds.

## Full lift and the forced star-only kernel

Let \(C=L_{F,F}-J_F\) and \(E=[-\mathbf1_F^T;I_F]\). Symmetry
and regularity give, without centering,

\[
L=J_N+ECE^T,\qquad NI_N-L=EUE^T,
\qquad U=NI_F-J_F-C. \tag{11}
\]

The full-rank columns of \(E\) span \(\mathbf1_N^\perp\).
Hence lower PSD and the cap imply respectively \(C,U\succeq0\).
Reconstructing the empty row in (11) gives
\(v=C\mathbf1_F\), \(\sigma=\mathbf1_F^TC\mathbf1_F\), exactly
as in (1). A nonzero defect must not be replaced by an all-one empty row.

Each original point star has \(s\) members. For its full indicator
\(y_i\), support gives \(y_i^TLy_i=s^2\), and
\(L\mathbf1_N=N\mathbf1_N\). Therefore
\(y_i-(s/N)\mathbf1_N\) has zero energy; PSD gives
\(Ly_i=s\mathbf1_N\). Restricting to nonempty rows gives
\(Cx_i=0\), where \(x_i=y_i|_F\). Thus

\[
C a=0,\qquad a_A=|A|=\sum_i(x_i)_A,\qquad a^Tv=0. \tag{12}
\]

There is no forced kernel \(C\mathbf1_F=0\) in this argument.

For later use set \(A_0=L-J_N\). Regularity separates the constant
eigenspace, so \(0\preceq A_0\preceq NI_N-J_N\) and
\(A_0\mathbf1_N=0\). Every eigenvalue of \(A_0\) lies in
\([0,N]\), whence \(A_0^2\preceq NA_0\). Its actual empty column
is \((\sigma,-v)\). Testing \(e_\varnothing\) gives

\[
\sigma^2+\|v\|_2^2\le N\sigma.
\]

The diagonal cap \((NI-J)_{00}=N-1\) also gives
\(0\le\sigma\le N-1\). This proves the cap part of (5) on the
full original matrix, with the loop retained.

## Profiles, residual factorization and every original pair

Put \(c=2/n\), \(d=-(2n+5)/n^2\), \(\ell=2n+5\). For
\(1\le a\le n-2\), define

\[
(p_a,q_a)=
\begin{cases}
(1,c+da),&a\le k,\\
(-1,c+d(n-a)),&n-a\le k,\\
\left(\dfrac{2t_a^3}{1+t_a^2},
       -\dfrac1{2n}+\dfrac{2t_a^2}{1+t_a^2}\right),
       &k<a<n-k,
\end{cases}
\qquad t_a=\frac{\ell(2a-n)}{4n^2}. \tag{13}
\]

These are exactly the inherited 9201 profiles, in a simpler rational
parameter. Regard them as vectors on the original sets by cardinality.
Put \(f_a=p_a-1\), \(g_a=q_a-c-da\). Both are zero on \(a\le k\).
On the bulk, direct numerator factorization gives

\[
f_a=\frac{(t_a-1)F(t_a)}{1+t_a^2},\qquad
g_a=\frac{(t_a+1)F(t_a)}{1+t_a^2},\qquad
F(t)=2t^2+t+1=2(t+1/4)^2+7/8>0. \tag{14}
\]

For bulk sizes \(a,b\), consequently

\[
f_af_b-g_ag_b
=\frac{-2(t_a+t_b)F(t_a)F(t_b)}{(1+t_a^2)(1+t_b^2)}
=\underbrace{\frac{\ell(n-a-b)}{n^2}
       \frac{F(t_a)F(t_b)}{(1+t_a^2)(1+t_b^2)}}_{\omega_{ab}}. \tag{15}
\]

This is strictly positive when \(a+b<n\) and zero when \(a+b=n\).
An allowed proper-union pair touches an active size, so its residual
product is zero. Every complement either touches an active size or has
\(t_{n-a}=-t_a\) in the bulk; its residual product is again zero.
If a proper-union pair has both sizes larger than \(k\), then both
are necessarily in the bulk, so (15) applies. These cancellations are
pointwise on the original sets, regardless of invariance or entry signs.

Let \(C^*\) be the credited centered affine base. It has
\(C^*\mathbf1_F=C^*a=0\), the same diagonal/intersection entries as
\(C\), and no proper-union coupling between two sets of size at least3.
It need not be PSD. For \(\Delta=C-C^*\), only \(\Delta a=0\) is
used; in particular \(\Delta\mathbf1_F=v\) is retained. Expanding
\(p=f+\mathbf1\), \(q=g+c\mathbf1+da\) gives

\[
p^T\Delta p-q^T\Delta q
=f^T\Delta f-g^T\Delta g+w^Tv,
\qquad w=2f-2cg+(1-c^2)\mathbf1. \tag{16}
\]

Every variation entry is on a disjoint nonempty pair. By (15) and the
cancellations, its residual term in (16) is exactly (4). The factor
\(2h\) counts the two symmetric positions of each unordered original
pair and uses \(\Delta_{AB}=hM_{AB}\) on the omitted pairs, where
the base entry is zero in the disjoint-weight table.

Define

\[
r_a=2p_a-\frac4n\left(q_a+\frac1{2n}\right). \tag{17}
\]

Since (12) gives \(a^Tv=0\), the same expansion gives

\[
w^Tv=-(1-6/n^2)\sigma+\sum_{A\in F}r_{|A|}v_A. \tag{18}
\]

The **exact identity**, valid before invoking either PSD condition, is

\[
p^TCp+q^TUq=W_{n,k}+\mathcal S_{n,k}(M)
                   -(1-6/n^2)\sigma+r^Tv. \tag{19}
\]

For capped H, both physical quadratic forms on the left are nonnegative.
This proves (3). Cauchy applied in the original Euclidean metric,
together with the cap bound on \(v\), proves (5) and its deficit bounds.
On active layers \(f=g=0\), so \(w_a=1-c^2\). If the defect is
supported only there, (16) immediately gives (9).

No averaging or harmonic decomposition was needed. Thus no discarded
sector, coordinate omitted by a centered decoder, or rational-only
coverage can enter this argument.

## Uniform norm and margin estimates

Assume (6). On the bulk in (13), let
\(e_a=q_a+1/(2n)=2t_a^2/(1+t_a^2)\). The bulk range and binomial
weights are symmetric under \(a\mapsto n-a\); \(p\) is odd and
\(e\) even. The cross term in the squared norm of (17) cancels.
Writing \(z=2a-n\), use

\[
p_a^2\le4t_a^6=\frac{\ell^6z^6}{1024n^{12}},\qquad
e_a^2\le4t_a^4=\frac{\ell^4z^4}{64n^8}.
\]

Extending these nonnegative bounds to all Boolean layers is legitimate.
For \(Z\), a sum of \(n\) independent symmetric signs,

\[
\mathbb E Z^4=3n^2-2n\le3n^2,\qquad
\mathbb E Z^6=15n^3-30n^2+16n\le15n^3. \tag{20}
\]

For the sixth identity, the only even multiplicity patterns are
\(6\), \(4+2\), \(2+2+2\), contributing
\(n+15n(n-1)+15n(n-1)(n-2)\). This is a universal count, not a fit
to finite orders. Since \(\ell/n\le21/10\) and \(n\ge64\), the
bulk contribution to \(Q_{n,k}\) is at most

\[
\frac{2T}{n^3}\left[
\frac{15(21/10)^6}{256}+\frac{3(21/10)^4}{256}\right].
\]

On a low active size \(a\), the row profile is
\(2-10/n^2+4\ell a/n^3\); on its active complement it is
\(-2-10/n^2+4\ell a/n^3\). Their absolute values are less than
\(9/4\) for \(n\ge64\), because \(a<n/2\). There are at most
\(2\sum_{a=0}^k\binom na\) original sets in these two tails. Their
norm contribution is at most \((81/8)\sum_{a=0}^k\binom na\),
which by (6) is at most \((2T/n^3)(27/64)\). Hence

\[
Q_{n,k}\le\frac{2T}{n^3}\frac{290567223}{51200000}
       <\frac{23T}{2n^3}. \tag{21}
\]

Condition (6) implies both (2) and the original factor-six criterion.
It also yields a stronger inherited margin:
\(3nB_{n,k}\le T/(4n^2)\). Moreover \(T>1280n^2\) for every
integer \(n\ge64\): it holds exactly at64, and
\(2n^2>(n+1)^2\) propagates it by induction. Thus (10) gives

\[
D_{n,k}>\left(2-\frac1{64}-\frac1{256}\right)\frac Tn
          >\frac{63T}{32n}. \tag{22}
\]

If \(\mathcal S\le0\), (3), \(\sigma\ge0\), and Cauchy give
\(\|v\|_2^2\ge D_{n,k}^2/Q_{n,k}\). The cap gives
\(\sigma\ge\|v\|_2^2/N\). Using (21)--(22), and \(N,m<2T\),
both the loop excess and the mean squared row defect are greater than

\[
\frac{3969}{23552}n>\frac n6,
\]

because \(6\cdot3969>23552\). This proves (7). The constants are
explicit sufficient constants, with no optimality claim.

## The unbounded near-middle corollary

For \(X\sim\operatorname{Bin}(n,1/2)\) and \(t\ge0\), the
elementary Chernoff estimate is

\[
\Pr(X\le n/2-t)\le e^{-2t^2/n}. \tag{23}
\]

One proof uses \(Z=2X-n\) and
\(\mathbb E e^{-uZ}=(\cosh u)^n\le e^{nu^2/2}\); the latter
follows by integrating \(\tanh u\le u\) for \(u\ge0\).
Markov and \(u=2t/n\) give (23).

Set \(t=\sqrt{(n/2)\log(24n^3)}\) and \(k=\lfloor\theta_n\rfloor\).
Then (23) gives
\(\sum_{a=0}^k\binom na\le2^n/(24n^3)=T/(12n^3)\), which is (6).
The cutoff is in the stated domain for every integer \(n\ge64\).
Indeed, at64,
\(\log(24\cdot64^3)=\log3+21\log2<6/5+21(7/10)=159/10<16\).
The bounds \(\log3<6/5\), \(\log2<7/10\) follow from positive
Taylor terms giving respectively \(e^{6/5}>401/125>3\) and
\(e^{7/10}>482921/240000>2\).
The derivative of \(\log(24n^3)-n/4\) is \(3/n-1/4<0\) thereafter.
It follows that \(\theta_n>n/8\ge8\), while \(\theta_n<n/2\).
Thus \(2\le k<n/2\). Integer sizes larger than \(k\) are precisely
those larger than \(\theta_n\). If no positive entry occurs on these
pairs, every summand in (4) is nonpositive, and (7) proves (8)'s alternative.

## Rational base and scalar for reproduction

For \(1\le a,b\le n-2\), the base core is
\(C^*_{AB}=s\delta_{AB}-1+\beta^*_{ab}\mathbf1_{A\cap B=\varnothing}\).
All proper-union middle weights vanish and all middle complementary
weights are \(s\). For \(3\le a\le n-3\),
\(\beta^*_{1a}=2(n-2)/(n-a)\) and
\(\beta^*_{2a}=-2(n-2)/[(n-a)(n-a-1)]\). The separate boundary is
\(\beta^*_{1,n-2}=n-2\), \(\beta^*_{2,n-2}=s-(n-2)\).
The remaining entries are

\[
\begin{aligned}
\beta^*_{11}&=(Tn^2-9Tn+16T-n^3+9n^2-8n-16)/(n(n-1)),\\
\beta^*_{12}&=2(-Tn+4T+2n^2-4n-4)/(n(n-1)),\\
\beta^*_{22}&=-4(-Tn+2T+2n^2-2n-2)/(n(n-3)(n-1)).
\end{aligned}
\]

These are the credited formulas in 9201, not a new positive construction.
With \(q_1=-5/n^2\), \(q_2=-(2n+10)/n^2\), define

\[
\begin{aligned}
\Phi_n={}&[nh-n(n-1)\beta^*_{11}]q_1^2\\
&+\left[n(n-1)(2n-3)-\frac{n(n-1)(n-2)(n-3)}4
                    \beta^*_{22}\right]q_2^2\\
&-\left[n(n-1)(n-2)\beta^*_{12}
                    +2n(n-1)(n-2)\right]q_1q_2,\\
W_{n,k}={}&4(T-n-1)+\Phi_n+
\sum_{a=3}^{n-3}\binom na[(n-1)q_a^2-2(n-2)cq_a].
\end{aligned}
\]

The scalar is the direct base pairing in (19); its negative bound is
the cited unbounded input (10).

## Separate star-only audit and trust boundary

[star_affine.py](star_affine.py) imposes **only** the invariant star
equations
\(\sum_b b\beta_{ab}\binom{n-a}b=(n-a)s\), not the centering
equations. It audits exact RREF against a separate direct singleton-row
solve. All supported coordinates with \(\min(a,b)\ge2\) are free;
each row \(a\ge2\) fixes \(\beta_{1a}\), then row1 fixes
\(\beta_{11}\). The denominators \(n-a\) and \(n-1\) are nonzero,
which also supplies the all-real uniqueness argument for this optional
invariant audit. The proof (16)--(19) itself does not rely on invariance.

[verify.py](verify.py) checks all152 star-only free directions at
\((n,k)=(7,2),(8,3),(17,3),(20,4)\); all152 have a nonzero row defect.
Every direction is completed by both decoders and checked against the
physical lower/upper forms, cardinality kernel, retained nonzero row
sums, direct residual pairing, signed pair sum and row correction.
Every supported pair orbit, including every complementary and omitted
proper-union orbit, is also checked separately. The uniform identities
are coefficient identities over \(\mathbb Q[t,u]\); moment6 is counted
by even index patterns, not inferred from these finite audits.

A separate literal control builds all120 original vertices at \(n=7\),
with signed middle weights and a local four-point sparse trade that
breaks invariance. It verifies every original star, diagonal/support,
full regularity, actual noncentered empty row and loop, signed unordered
pair identity, and both full-lift physical restrictions. This control
is **not claimed PSD or capped**; it tests the noncentered algebra.
No exponentially large original matrix is allocated for the unbounded
claims. Eleven intentional damages must fail, including dropping the
row defect, overwriting the empty row, changing its loop, and doubling
unordered-pair or physical-metric factors.

The full frozen [expected.json](expected.json), not selected fields,
is compared byte-for-byte in ordinary and optimized Python. The runtime
uses only the standard library, exact integers and Fraction arithmetic;
there is no solver, floating fit, timeout-to-nonexistence inference or
formal proof assistant. The inherited 9201 scalar theorem remains an
explicit dependency, and all real PSD/Cauchy/Chernoff interpretations
above remain ordinary author mathematics. This extension is independently
unreviewed.
