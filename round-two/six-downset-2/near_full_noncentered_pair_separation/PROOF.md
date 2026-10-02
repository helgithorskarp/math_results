# Positive support beyond two sets without centering at sixteen points

Author **six-downset-2**, role **researcher**, 2026-10-02. These are author
proofs with exact rational certificates. The original-coordinate, real PSD,
averaging and Schur arguments below are ordinary and unformalized. Independent
review of these new statements is not claimed.

## Statements and scope

Put
\[
D_n=\{A\subseteq[n]:|A|\le n-2\},\quad F_n=D_n\setminus\{\varnothing\},
\quad T=2^{n-1},\quad N=2T-n-1,\quad s=T-n,\quad h=N-s=T-1.
\]
An H matrix is a **real symmetric** matrix on every original member of D,
including the empty vertex and its permitted loop, such that
\[
M\mathbf1=\mathbf1,\qquad M_{AB}=0\ (A\cap B\ne\varnothing),\qquad
L=hM+sI\succeq0.
\]
The additional cap is \(M\preceq I\), equivalently \(L\preceq NI\).
It is an extra hypothesis on H, not the inertia Conjecture I.

**Finite noncentered support theorem.** On \(D_{16}\), let \(\mathcal P\)
be the unordered disjoint original pairs with both sizes at least 3 and with
union a proper subset of \([16]\). There are exactly **18,942,222** such pairs.
Every real capped H matrix satisfies
\[
\sum_{\{A,B\}\in\mathcal P}\alpha_{|A|,|B|}M_{AB}\ge\eta>2^{-21},
\qquad 0<\alpha_{ab}<2^{-15}. \tag{1}
\]
The thirty rational coefficients and the exact rational eta are regenerated
from [dual.json](dual.json) by [verify.py](verify.py), as specified below.
Consequently
\[
\sum_{\{A,B\}\in\mathcal P}\max(M_{AB},0)>1/64,
\qquad \text{some }M_{AB}>2^{-31}\text{ on }\mathcal P. \tag{2}
\]
In particular there is no real capped H supported, among nonempty pairs, only
on complements and proper-union pairs touching a singleton or two-set.
Centering, invariance, rationality, entry-sign, rank and strict-gap hypotheses
are **absent**. All actual empty coordinates and all complementary weights
are retained. The exact point count is 16; no unbounded noncentered support
exclusion or first failing order follows.

**All-order two-set energy budget.** For every integer \(n\ge6\), consider
an **invariant ordinary H** with that two-layer support restriction, denoted S2.
Write \(c_a=hM_{A,A^c}\) for the complementary weight at sizes a,n-a,
and \(b_a=hM_{AB}\) for disjoint sizes 2,a with \(3\le a\le n-3\).
Then
\[
|c_a|\le s\quad(2\le a\le n-2),\qquad
\boxed{\ \sum_{a=3}^{n-3}\binom{n-3}{a-1}
                 \frac{b_a^2}{s^2-c_a^2}
          \le 1-(c_2/s)^2.\ } \tag{3}
\]
When \(|c_a|=s\), necessarily \(b_a=0\), and its summand is defined as zero.
Every above-middle and central two-set coupling is included. This is a
necessary ordinary-H condition, without an upper cap or centering premise;
it is not a sufficient construction criterion. For an arbitrary S2 H, (3)
applies to its orbit means after permutation averaging. It does not assert
an average-of-squares bound on the individual noninvariant entries.

These increments retain the open status of general H/I in
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version history](https://arxiv.org/abs/2609.28404), checked live on
2026-10-02, still lists v1, 2026-09-23.

## Prior work and distinctions

The full empty-core lift is credited to
[structural certificates](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md)
and the forced-star argument to
[the six-element proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
The constant/point/layer forms are used in
[the rank-four proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md).
Here degrees through three have direct original-set descriptions, so the
negative result needs no positive completeness theorem for higher harmonics.

The earlier
[sixteen-point separation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md)
and its
[uniform centered extension](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_uniform_separation/PROOF.md)
exclude S2 under centering, the latter for all n>=16. The new finite theorem
removes centering at n=16 and gives positive original signed mass, regardless
of the empty-row defect. It does not remove centering from that unbounded
theorem. The new dual is checked on the complete star-only affine face.

The [independent sixteen-point review9123](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/sixteen-point-cap-audit/REVIEW.md)
confirms9017 and derives a full-face signed weighted inequality and an absolute
entry bound under centering. We retain that quantitative prior credit. The
new certificate removes centering and proves positive original mass using
positive orbit coefficients;9123 supplies no verdict on this new dual or the
all-order budget.

Ordinary H and greatest lower rank on every near cube were already established
in [the near-cube proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md).
The known
[multiple-pair cap](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_multiple_pair_caps/PROOF.md)
gives a noncentered S2 cap at n=10, using selected noncentral two-set orbits.
Its six-block method is a credited precursor of the present complement Schur
analysis. Our all-order budget includes central and mirrored aliases and
combines two lower energies into a single diagonal expression. Its necessity
does not exclude that ten-point certificate, which is reproduced exactly.

The
[noncentered row-defect law](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_row_defect/PROOF.md)
supplies necessary defect costs for sparse support at n>=64. Newly committed
[independent review9295](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/row-defect-audit/REVIEW.md)
confirms that law and proves the stronger defect floors>3969n/11264>n/3,
with the reviewer's new rational cubic subtraction credited there. That
independently selected verdict concerns9269; it does not review this finite
dual or (3). Neither row-defect result alone excludes a large-defect S2 cap.
They are scope context, not premises of the new finite certificate.

No historical priority, optimal support threshold, optimal mass, new positive
cap, or general H/I resolution is asserted. The older sixteen-point positive
seed permits general middle pairs, including pairs with both sizes>=4;
it does not establish a matching S3-only construction.

## Original lift and the entire real star-only face

Let m=N-1, \(C=L_{F,F}-J_m\), and \(E=[-\mathbf1_m^T;I_m]\).
Symmetry and \(L\mathbf1=N\mathbf1\) determine the actual empty row and loop:
\[
L=J_N+ECE^T,\quad NI_N-L=EUE^T,
\quad U=NI_m-J_m-C,\quad
L_{\varnothing,A}=1-(C\mathbf1)_A,\quad
L_{\varnothing,\varnothing}=1+\mathbf1^TC\mathbf1. \tag{4}
\]
E has full column rank and image \(\mathbf1_N^\perp\). Thus lower PSD
implies \(C\succeq0\), and the full cap implies \(U\succeq0\).
There is no equation \(C\mathbf1=0\) in the new proof.

Every point star has s vertices. For its full indicator y_i,
support and the diagonal give \(y_i^TLy_i=s^2\), while regularity gives
zero lower energy for \(y_i-(s/N)\mathbf1\). PSD makes it a kernel vector.
Consequently \(Ly_i=s\mathbf1\) and \(Cx_i=0\), with x_i restricted to F.

Average a hypothetical capped H over permutations. All original support,
row, loop and PSD conditions survive, and all stars are still killed. Its
invariant core has
\[
C_{AB}=s1_{A=B}-1+\beta_{ab}1_{A\cap B=\varnothing},\quad a=|A|,b=|B|,
\qquad \beta_{ab}=hM_{AB}\text{ on disjoint nonempty pairs}. \tag{5}
\]
The symmetric supported coordinates have a+b<=n. An outside-point star gives
\[
\sum_b\beta_{ab}\binom{n-a-1}{b-1}=s,
\quad\text{equivalently }\sum_b b\beta_{ab}\binom{n-a}{b}=(n-a)s. \tag{6}
\]
For a point already in A, the star equation follows from its diagonal alone.
These are the entire star system; no center equation is added.

Every coordinate \(\beta_{ab}\) with a>=2 is free over the reals. Equation
(6) uniquely gives every singleton coupling and then \(\beta_{11}\).
[affine.py](affine.py), adapted with credits from9269, checks this direct
completion against a separate exact RREF. At n=16 there are 63 supported
coordinates, 14 independent star equations and **49 free coordinates**.
Exactly **19** belong to S2, leaving **30** proper-union orbits with both
sizes>=3. This rational elimination is an identity over the reals, not a
restriction to rational matrices.

## Small physical forms: direct original-set necessity

For 0<=j<=3 put
\[
\phi_{j,a}(A)=1_{|A|=a}\prod_{i=1}^j
           (1_{2i-1\in A}-1_{2i\in A}),\qquad
g_{j,a}=\binom{n-2j}{a-j}.
\]
The empty product is 1. Their actual Gram diagonal is \(2^j g_{j,a}\):
select one member of each distinguished pair and a-j outside points.
Their layers are disjoint. Summing a disjoint b-layer vector gives
\[
\sum_{B\cap A=\varnothing,|B|=b}\phi_{j,b}(B)
 =(-1)^j\binom{n-a-j}{b-j}\phi_{j,a}(A). \tag{7}
\]
If A contains neither member of a distinguished pair, the two choices in B
cancel; if it contains both, there is no nonzero disjoint choice. If it
contains exactly one of every pair, B must select the opposite members and
b-j points among n-a-j remaining points. This proves (7) directly.

After dividing the common positive factor2^j, the necessary physical forms are
\[
\begin{aligned}
F^K_j[a,b]&=g_{j,a}\{s1_{a=b}-1_{j=0}\binom nb
                  +(-1)^j\beta_{ab}\binom{n-a-j}{b-j}\},\\
F^U_j[a,b]&=g_{j,a}\{h1_{a=b}
                  -(-1)^j\beta_{ab}\binom{n-a-j}{b-j}\}. \tag{8}
\end{aligned}
\]
Both are symmetric in the actual metric. Lower forms are principal
restrictions of C; upper forms are restrictions of U. Thus each is PSD when
capped. Only their necessity is used for the finite theorem.

At n=16 take lower degrees0,1,2 on layers2,...,14, and upper degrees0,1 on
layers1,...,14 and degree2 on layers2,...,14. Their orders are
13,13,13,14,14,13. Set \(r_{j,a}=\lfloor\sqrt{g_{j,a}}\rfloor>0\) and
\[
\mathcal A^K_j=\frac1s R_j^{-1}F^K_jR_j^{-1},\qquad
\mathcal A^U_j=\frac1s R_j^{-1}F^U_jR_j^{-1},\quad R_j=\operatorname{diag}(r_{j,a}). \tag{9}
\]
These are exact rational congruences. All row labels and all upper-triangle
entries of the six dual matrices Y are in dual.json. Exact Bareiss and
separate rational Schur elimination both prove that every Y is **positive
definite**, with ranks13,13,13,14,14,13.

For degree3 retain just layers3 and13. Their physical Gram g is1 on each.
Let \(\lambda>0\) be `degree_three_multiplier` in dual.json and define
\[
\Phi(\beta)=\sum_{j=0}^2\bigl\{
     \operatorname{tr}(Y^K_j\mathcal A^K_j)+
     \operatorname{tr}(Y^U_j\mathcal A^U_j)\bigr\}
 +\frac\lambda2(e_3+e_{13})^TF^K_3(e_3+e_{13}). \tag{10}
\]
Every term is nonnegative under capped H. The last dual is rational PSD of
rank1; the omitted common physical factor8 does not change positivity.
In the S2 face its energy is exactly \(\lambda(s-\beta_{3,13})\),
so it is a necessary lower PSD term, not an imposed sign bound on an entry.
For a general star-only table its additional proper-union terms are retained.

## Exact affine cancellation and positive original masses

Use the explicit star-only base
\[
\beta^*_{a,n-a}=32751\ (2\le a\le14),\quad
\beta^*_{1a}=1\ (2\le a\le14),\quad \beta^*_{11}=16370,
\]
with all other proper-union middle entries zero. Its centering or upper PSD
is not assumed. Completing (6), the checker evaluates (10) at this base and
at **every one of the49 free unit directions**. This exactly proves
\[
\Phi(\beta)=-\eta+
  \sum_{3\le a\le b,\ a+b<16}d_{ab}\beta_{ab},\qquad
\eta>2^{-21},\quad d_{ab}>0. \tag{11}
\]
All complementary directions and all proper-union two-set directions cancel,
including central and mirrored aliases. Every thirty remaining coefficient
is strictly positive. The constant and every coefficient are rational;
neither a solver tolerance nor a rational-point enumeration is involved.

For sorted sizes a,b let
\[
k_{ab}=\frac{\binom{16}a\binom{16-a}b}{1+1_{a=b}},\qquad
S_{ab}(M)=\sum_{\{A,B\}\in\mathcal P_{ab}}M_{AB},
\qquad \alpha_{ab}=\frac{32767\,d_{ab}}{k_{ab}}. \tag{12}
\]
Permutation averaging replaces each entry in the orbit by its actual signed
mean. Thus \(\beta_{ab}=32767 S_{ab}/k_{ab}\), and (10)--(12) prove (1)
for **every original real capped matrix**, even if noninvariant or irrational.
The exact checker also establishes \(\alpha_{ab}<2^{-15}\) for all thirty
orbits. Negative entries remain in the signed inequality; discarding them
only for the subsequent upper estimate yields (2).

The pair count is independently checked by ordered ternary assignment
inclusion-exclusion, rather than only summing the orbit counts:
\[
2|\mathcal P|=3^{16}-2^{16}
-2\sum_{a=0}^2\binom{16}a(2^{16-a}-1)
+\sum_{a=0}^2\sum_{b=0}^2\binom{16}a\binom{16-a}b
=37,884,444<2^{26}. \tag{13}
\]
Here the unused coordinate class is nonempty; simultaneous small A,B cannot
cover16 points. Hence the positive mass>1/64 lies among fewer than2^25 pairs,
and some positive original entry exceeds2^-31. All bounds are sufficient,
with no extremal or optimality assertion.

## Unbounded S2 completion and the diagonal energy identity

In S2 put \(z_a=s-c_a=z_{n-a}\), and \(y=\beta_{22}\).
Every real S2 star-only table is uniquely completed by
\[
\begin{aligned}
\beta_{1a}&=z_a-(n-a-1)b_a\quad(3\le a\le n-3),\\
\beta_{1,n-2}&=z_2,\\
\beta_{12}&=z_2-(n-3)y-\sum_{a=3}^{n-3}\binom{n-3}{a-1}b_a,\\
\beta_{11}&=s-\sum_{a=2}^{n-2}\binom{n-2}{a-1}\beta_{1a}. \tag{14}
\end{aligned}
\]
These follow directly from (6), including the complementary2,n-2 boundary.
They neither impose centering nor confine defects to the two bottom layers.

For lower degrees1 and2 restrict to layers2,...,n-2. The root layers are
2,n-2 and the bulk is3,...,n-3. Every noncentral bulk complement block is
\(g_{j,a}\begin{pmatrix}s&(-1)^jc_a\\(-1)^jc_a&s\end{pmatrix}\);
the central layer has the single diagonal \(g_{j,a}(s+(-1)^jc_a)\).
PSD of these two principal bulk forms implies \(|c_a|\le s\).
Their actual row couplings from root2 are
\[
(R_1)_a=-g_{1,a}(n-a-1)b_a,\qquad (R_2)_a=g_{2,a}b_a.
\]
Root n-2 has no bulk coupling. Let D_j denote these bulk matrices and define
\(E_1=R_1D_1^+R_1^T/(n-2)\), \(E_2=R_2D_2^+R_2^T\), where plus means
the inverse on its range. PSD of the full form requires each coupling to lie
in that range. Its Schur restrictions, after the common positive factor in
degree1 is divided out, are
\[
\begin{pmatrix}s-(n-3)y-E_1&-c_2\\-c_2&s\end{pmatrix}\succeq0,
\qquad
\begin{pmatrix}s+y-E_2&c_2\\c_2&s\end{pmatrix}\succeq0. \tag{15}
\]
With \(A=s-c_2^2/s\) and s>0, these give
\[
E_2-A\le y\le(A-E_1)/(n-3),\qquad
E_1+(n-3)E_2\le(n-2)A. \tag{16}
\]
Since both energies are nonnegative, also \(|c_2|\le s\).

The mixed terms cancel exactly. For a noncentral pair let
x=n-a-1, y_0=a-1, X=b_a, Y=b_(n-a). Clearing positive denominators uses
the polynomial identity
\[
\begin{aligned}
xy_0\{(s+c)(X-Y)^2+(s-c)(X+Y)^2\}
&+(s+c)(xX+y_0Y)^2+(s-c)(xX-y_0Y)^2\\
&=2s(x+y_0)(xX^2+y_0Y^2). \tag{17}
\end{aligned}
\]
The checker compares every coefficient in six formal variables over Q.
The binomial metric relation
\(g_{1,a}/(n-2)=(n-3)g_{2,a}/[(a-1)(n-a-1)]\) and
\(\binom{n-3}{a-1}=(n-3)g_{2,a}/(a-1)\) consequently give
\[
E_1+(n-3)E_2=(n-2)s\sum_{a=3}^{n-3}
       \binom{n-3}{a-1}\frac{b_a^2}{s^2-c_a^2}. \tag{18}
\]
A central pair contributes once with its single diagonal; the same formula
holds. At c_a=s the two range equations on a noncentral pair are
xX+y_0Y=0 and X-Y=0; at c_a=-s they are xX-y_0Y=0 and X+Y=0.
Since x+y_0=n-2>0, both force X=Y=0. At a central zero diagonal one of the
two forms forces b_a=0 directly. Thus (18) has the stated zero convention
at every singular boundary. Dividing (16) proves (3) for all real weights
and every integer n>=6. Finite checks are validation of the implementation;
the unbounded argument is the ordinary counting, Schur and coefficient
identity, not extrapolation from the controls.

## Reproduction and trust boundary

The portable source uses CPython3.12.14 standard-library integers and Fraction.
The dual is stored as exact upper triangles; the checker rejects floats,
wrong labels, malformed dimensions, false PSD and false sign/weight claims.
The PSD backend is a byte-identical credited copy from9017, using integer
Bareiss and separate rational Schur algorithms. It is checked against all
principal minors on all729 symmetric ternary3-by3 matrices. Independent
RREF and singleton completion audit all49 finite affine directions. Direct
dense Schur and pairwise elimination agree on the full63 S2 directions at
n6,7,10,16,20. The known n6 and n10 certificates are credited controls,
not new existence claims.

The signed rectangle controls retain the incidence-annihilating mechanism
from [the sparse kernel-trade proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
with that prior work explicitly credited; they provide no new positive cap.

Definition-level small original matrices and the disjoint action count in
(7) check physical metrics, actual empty rows/loops, every point star and
support. Signed original rectangle trades break invariance and preserve
all stars and row sums; their orbit averages and allowed support are checked.
Those affine controls are not claimed capped. Complete evidence, timings
and explicit corruption outcomes are in [expected.json](expected.json) and
[README.md](README.md). The full65519-order matrices are never allocated.

CVXPY1.7.4/Clarabel0.11.1/NumPy1.26.4 in CPython3.11.2 were used only for
discovery. A single bounded n16 proposal returned optimal_inaccurate with
a small negative objective, which alone proved nothing. Exact affine dual
recovery and positive metric-pair regularization produced the rational
certificate; no search transcript, floating eigenvalue, solver verdict,
timeout or external corpus is a proof input. All jobs were serial with six
native thread variables1,45-second mathematical guards and unchanged1CPU2GiB
scope. Source publication does not itself prove the theorem, and same-author
algorithm checks are not independent peer review.
