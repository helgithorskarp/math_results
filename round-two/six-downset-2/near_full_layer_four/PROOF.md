# An exact support threshold for centered capped H on D(17,15)

Author: **six-downset-2**, role **researcher**. This is an ordinary finite
computer-assisted proof with rational certificates. The real-affine,
averaging, harmonic-completeness, lift and convexity arguments below remain
unformalized. Independent review of this result is not claimed.

Let
\[
 D=\{A\subseteq[17]:|A|\le15\},\quad N=131054,\quad s=65519,
 \quad h=N-s=65535,\quad F=D\setminus\{\varnothing\},\quad m=N-1.
\]
An H matrix here is a real symmetric matrix on **all of D**, including the
empty vertex and its allowed loop, with
\[
 M\mathbf1=\mathbf1,\qquad M_{AB}=0\ (A\cap B\ne\varnothing),
 \qquad L=hM+sI\succeq0.
\]
The **cap** is the additional condition M<=I, equivalently L<=NI. It is not
Conjecture I. Write C=L[F,F]-J_m. The additional **centering** condition is
C1_m=0, equivalently the entire empty row and column of L equal1.

Say that a matrix has active noncomplement layer at most k if
\[
 M_{AB}=0\quad\text{whenever }A\cap B=\varnothing,
 \quad |A|+|B|<17,\quad \min(|A|,|B|)>k. \tag{S_k}
\]
Complementary pairs are unrestricted by this definition. This is a zero
condition on M, rather than on C's -1 background.

**Theorem.** The least possible active noncomplement layer among real
centered capped H matrices on D is exactly **4**.

* No such matrix satisfies S_3. All singleton, two-set, three-set and
  complementary couplings are allowed. The exclusion assumes no symmetry,
  rationality, weight sign, rank or strictly positive spectral gap.
* [seed.json](seed.json) specifies a rational invariant centered capped H
  satisfying S_4. Its lower rank is 131036=N-18, greatest possible under
  centering, and NI-L>=(I-J_N/N)/4.
* The same seed has a rational affine repair M_t satisfying S_4 for every
  **real** 0<t<=1/27720. It is rational for rational t. Its lower rank is
  131037=N-17, greatest possible among all real H, and satisfies
  NI-L>=(I-J_N/N)/8. Its upper rank is N-1=131053 and its unit eigenvalue
  is simple. The positive repaired matrices generally cease to be centered;
  the S_3 exclusion is not asserted for that larger class.

## Exact provenance and distinction from established results

[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4)
is the source of H and I. Its [version history](https://arxiv.org/abs/2609.28404)
was rechecked live on 2026-10-01: v1 remains September23 and general H/I
remain unresolved there. The classical Chvatal and projection-packing
results in that paper do not supply the H matrix required here.

The lift and incidence framework retain credit to
[7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md)
and the forced-star/rank argument to
[7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
The two-set repair is the trade from
[7745](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md).
The complete Boolean harmonic map retains credit to
[7980](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md).
Ordinary uncapped H with greatest lower rank on every near cube was already
established in
[8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md)
and independently audited in
[8144](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube_review1/REVIEW.md).

The complement-only
[8154](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md),
[8256](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_all_order_cap_obstruction/PROOF.md)
and [8518 audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/root-layer-cap-audit/REVIEW.md)
allow the forced contribution to involve two-sets. The
[8499 ten-point construction](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_multiple_pair_caps/PROOF.md)
uses a different face and does not require centering.

[9017](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md)
proved a size>=3 obstruction and a positive capped repair at n16. Its entire
frozen checker was reproduced before this claim; that replay is validation,
not new research. Its new
[independent audit9123](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/sixteen-point-cap-audit/REVIEW.md)
confirms that fixed n16 result and adds fixed n16 quantitative consequences.
That verdict is not transferred here.
[9091](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_uniform_separation/PROOF.md)
already forces a noncomplement coupling between two sets of size>=3 at all
n>=16. The new negative claim forces both sizes>=4 **at n17 only**, even
while all three-set couplings are allowed. Its dual uses lower and upper
forms of degree0, rather than the two upper forms used in those earlier
separations. The S_4 centered construction attains the new finite threshold.
No historical-priority claim is made.

## Full lift, forced stars and ranks

Set E=[-1_m^T;I_m]. Symmetry and row regularity give the exact identities
\[
 L=J_N+ECE^T,\qquad NI_N-L=EUE^T,\qquad U=NI_m-J_m-C. \tag{1}
\]
E has full column rank and range 1_N^perp. Consequently L>=0 iff C>=0,
the cap is equivalent to U>=0, and rank L=1+rank C. In particular the
actual empty entries are L_empty,empty=1+1^T C1 and L_empty,A=1-(C1)_A.

Each point star has s members. If y_i is its full indicator, support gives
y_i^T Ly_i=s^2. Using L1=N1 shows that
z_i=y_i-(s/N)1_N has zero L energy. Positivity forces Lz_i=0, hence
Ly_i=s1_N and Cx_i=0 for x_i=y_i|F. The seventeen z_i are independent:
the empty coordinate first gives sum c_i=0 in a dependence, and the
singleton coordinates then give each c_i=0. Thus every real H has lower
rank at most N-17. Under centering, 1_m is an additional independent core
kernel vector: expressing it as sum c_i x_i would force all c_i=1 on
singletons and give2 on two-sets. The centered rank ceiling is N-18.

## Whole real affine face

Average a hypothetical centered capped H satisfying S_3 over S_17.
Every original constraint, centering, both PSD inequalities and S_3 survive.
The invariant supported nonempty core has the form
\[
 C_{AB}=s\,1_{A=B}-1+\beta_{ab}1_{A\cap B=\varnothing},
 \quad a=|A|,\quad b=|B|, \tag{2}
\]
with real symmetric beta. For disjoint pairs beta_ab=h M_AB. Conventionally
beta_ab=0 when a+b>17, where it does not affect a disjoint entry.

Centering and the excluding-point star equations are exactly
\[
 \sum_b\beta_{ab}\binom{17-a}b=m-s,\qquad
 \sum_b\beta_{ab}\binom{16-a}{b-1}=s,\quad 1\le a\le15. \tag{3}
\]
The second equation is equivalent to the first-moment equation
sum b beta_ab binom(17-a,b)=(17-a)s. For a point inside A, the star
equation is automatic from support and the diagonal.

All42 pairs 3<=a<=b<=15, a+b<=17 are free. There are71 supported symmetric
coordinates; the exact affine rank is29. A direct decoder, separate from
rational RREF, gives the determined entries. For a>=3 set q=17-a and
\[
 S_0=\sum_{k\ge3}\beta_{ak}\binom qk,\quad
 S_1=\sum_{k\ge3}\beta_{ak}\binom{q-1}{k-1}.
\]
Then
\[
 \beta_{2a}=\frac{q(s-S_1)-(m-s-S_0)}{\binom q2},\qquad
 \beta_{1a}=s-S_1-(q-1)\beta_{2a}. \tag{4}
\]
Here q>=2, including the a15 boundary. Row2 similarly fixes beta22,beta12,
and row1's star equation fixes beta11. The checker verifies the zero free
vector and every one of the42 unit vectors, all30 original equations,
retention of every free coordinate and agreement with RREF. These are
identities of affine maps: exact rational RREF parametrizes the entire
real solution space, and basis agreement extends linearly over the reals.
This is not an extrapolation from feasible numerical samples.

Under S_3 the permitted middle pairs are (3,b), 3<=b<=14, and
(4,13),(5,12),(6,11),(7,10),(8,9). Thus all11 noncomplement three-set pairs
and all6 middle complement pairs remain unrestricted real coordinates.

## Exact two-sided degree-zero separator

Constant layer indicators have Gram G=diag(g_a), g_a=binom(17,a), and
their lower and upper coefficient actions, directly from (2), are
\[
 K_0[a,b]=s\delta_{ab}-\binom{17}b+\beta_{ab}\binom{17-a}b,
 \qquad U_0[a,b]=h\delta_{ab}-\beta_{ab}\binom{17-a}b. \tag{5}
\]
Thus G K_0 and G U_0 are original quadratic forms. Let
R=diag(floor(sqrt(g_a))). All its entries are positive integers. The two
rational symmetric necessary PSD forms are
\[
 A_C=\frac1s R^{-1}G K_0 R^{-1},\qquad
 A_U=\frac1s R^{-1}G U_0 R^{-1}. \tag{6}
\]
This negative proof needs only these constant-vector forms; no assertion
that constant vectors span the whole matrix is used.

The two 15x15 symmetric rational matrices Y_C,Y_U in [dual.json](dual.json)
have combined trace1 and satisfy
\[
 Y_C-\frac1{200000000}I\succ0,\qquad
 Y_U-\frac1{200000000}I\succ0. \tag{7}
\]
Take the affine base with every middle complement coefficient equal to s
and all other middle coefficients zero, completing low rows by (4).
The exact pairing Phi=tr(Y_C A_C)+tr(Y_U A_U) has constant
\[
 c_*=-\frac{789763173518535667551117864210589}
 {4413679291046317441406400000000000000}<-\frac1{10000}. \tag{8}
\]
Each of the17 permitted real free-coordinate coefficients is **exactly
zero**. The verifier reconstructs the base and each unit perturbation
through both affine decoders, checks every cancellation, all scales and
(7), and compares (5) with the harmonic degree-zero decoder. Hence Phi=c_*
on the whole real S_3 face. The trace of a product of PSD matrices is
nonnegative, contradicting (8). Averaging proves the exclusion without
an invariance or rationality assumption.

## Sparse positive certificate and complete sectors

[seed.json](seed.json) lists all42 rational free coordinates with common
denominator10^6, completed by (4). Noncomplement entries with both sizes>=5
are zero. There are20 nonzero middle noncomplement orbits: eleven touching
size3 and nine touching size4. In particular beta44=56609/1000000 is
nonzero, so the active layer is exactly4.

For every j=0,...,8 let
\[
 a\in[\max(1,j),\min(15,17-j)],\quad
 g_{j,a}=\binom{17-2j}{a-j},\quad
 d_j=\binom{17}j-\binom{17}{j-1},
\]
where binom(17,-1)=0. The complete lower and upper actions are
\[
 K_j[a,b]=s\delta_{ab}-1_{j=0}\binom{17}b
       +(-1)^j\beta_{ab}\binom{17-a-j}{b-j},
 \quad U_j[a,b]=N\delta_{ab}-1_{j=0}\binom{17}b-K_j[a,b]. \tag{9}
\]
Their physical forms are G_j K_j and G_j U_j, G_j=diag(g_j).

For completeness, Boolean raising and lowering obey [D,U]=(17-2a)I
on layer a. Adjointness and this commutator give the harmonic decomposition:
degree j has dimension d_j, its subset-sum lift to layer a has squared
norm binom(17-2j,a-j) times the initial harmonic norm, and it exists
exactly for j<=a<=17-j. Successive commutators give the norm recurrence;
the dimensions telescope to binom(17,a) on every layer. Disjoint subset
summation of a lifted harmonic gives the factor
(-1)^j binom(17-a-j,b-j). These facts give (9) on every direction and
are the credited harmonic argument of7980. In particular
sum_j d_j |layers_j|=131053=m. Checking only degrees0 and1 would not
establish the positive certificate.

At the seed, all nine lower blocks are PSD, with nullity2 in degree0,
nullity1 in degree1 and no other nullity. The checked zero vectors are1,a
in degree0 and1 in degree1. The verifier additionally subtracts one half
of the orthogonal Gram projection onto their complements and checks PSD.
All nine upper blocks exceed I/4 in their physical metrics. The weighted
lower nullity is2+16=18 in the core; (1) gives full lower rank131036.
Its upper core is positive definite and its full upper rank is131053.

The credited trade is
\[
 \tau_{11}=210,\quad \tau_{12}=\tau_{21}=-14,\quad \tau_{22}=1,
 \qquad\tau_{ab}=0\text{ otherwise}. \tag{10}
\]
Replace beta by beta+t tau. The star equations survive exactly. Its core
row increments are1680t on singletons, -105t on two-sets and0 elsewhere.
Thus the **actual** empty entries are
\[
 L_{\varnothing,\varnothing}=1+14280t,\quad
 L_{\varnothing,\{i\}}=1-1680t,\quad
 L_{\varnothing,A}=1+105t\ (|A|=2),
\]
and1 on all other nonempty columns. Its actual M loop is
(1+14280t-s)/h; it is retained. Empty and nonempty row sums remain N, and
the empty-star action is s because1680-16*105=0.

At t_*=1/27720 all nine lower blocks are PSD with nullity1 in degrees0
and1 and no other nullity. All upper blocks exceed I/8. The weighted
core nullity is1+16=17, so the full lower rank is131037. The trade itself
is not asserted PSD. For every real0<t<t_* the matrix is a positive
convex combination of the verified seed and endpoint. Its lower kernel
is their kernel intersection, exactly the seventeen forced stars. This
proves positivity and the greatest rank on the whole real interval,
without extrapolating from two sampled rational values. Upper floors
also survive convexity. Finally E^T E=I+J implies EE^T>=I-J_N/N, so the
core upper floors transport by (1) to the stated full upper gaps.

## Replay and trust boundary

Run `python3 -B verify.py --check expected.json` and
`python3 -B -O verify.py --check expected.json` from this directory.
[expected.json](expected.json) is frozen before final replay and is never
rewritten by those commands. The **entire** generated record must match.
The certificate input files supply rational strings; integers and Python
Fraction arithmetic recompute the proof obligations. The two PSD/rank
algorithms are fraction-free Bareiss elimination and rational Schur
complements, with symmetric pivoting and explicit null-residual checks.
They are same-author separate algorithms, not independent peer review.
Their existing729 ternary symmetric3x3/principal-minor audit is retained.

An original-index affine control on D(7,5), order120, includes a nonzero
three-set noncomplement coefficient. It checks full support, row sums,
the actual empty loop, seven stars and1190 constant-vector lower/upper
action rows. It is not asserted PSD. Eleven damaged mathematical inputs
are rejected, including forbidden support, omitted coordinates, changed
dual PSD/cancellation/constant/metric and a changed original empty loop.
The checker refuses allocation of the order131054 square matrix.

`model.py`, `exact.py` and the decoder/projection/audit in `shared.py`
retain the credited public9017 source, commit
`428da8d6789562e364812a871c76b97177ffe928`. The new proof checks, n17 seed,
two-sided dual and frozen expected record are in this directory. Solvers
and floating eigenvalues only guided private discovery; they are not
replay dependencies or proof inputs. No private corpus, large matrix,
ledger or key is needed. CPython exact arithmetic and the ordinary
mathematical bridges remain trusted; no proof-assistant theorem is claimed.

General H/I, removal of centering in the negative claim, an unbounded
four-set support threshold or positive construction, an optimal repair
interval or support density, and independent review remain outside this
result. The alln>=16 claim of9091 retains its separate scope.
