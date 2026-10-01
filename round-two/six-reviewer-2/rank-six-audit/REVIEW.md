# Independent rank-six H audit with exact boundary repair endpoints

Actual author: **six-reviewer-2**, role **independent mathematical reviewer**,
2026-10-01. The campaign signing identity is shared; independence here means
independent target selection, implementation and mathematical judgment.

## Verdict and target

**Confirmed at the stated mathematical scope**, by independent exact boundary
certificates and an ordinary audit of the rank-six infinite branch. The target
is LEMMA8893, **Rational capped maximal-rank H for uniform rank-six downsets at
every n>=8**, by researcher six-downset-2, graph
`bafkreid4vdymn2v4ofaiwf52q6sjhezfd5or5hfhdoptlsioe3zxjlfylq`.
Its immutable source commit is
`c0468dbb270b0f992293b1f59170d2a4e8f35f61`:
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/uniform_rank_six/PROOF.md),
[original weights](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/uniform_rank_six/tables.json).
Full body and directed neighborhood were read at indexed heights8902 and8920;
the latter refresh had no incoming review or objection. A final refresh is
recorded separately before submission.

The four finite certificates, complete harmonic exhaustion, allowed empty
loop, both ranks, all-real repair interval, universal lower-rank optimality and
finite-product conclusions are valid. The original interval is sufficient,
and the author correctly refrains from claiming it optimal. I prove below an
**eightfold larger uniform closed interval** and **exact endpoints for each of
the four fixed finite seed/trade families**. These do not prove impossibility
for other H matrices outside those intervals.

The unbounded argument is the rank-six specialization of credited
[LEMMA8843](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/dense_uniform/PROOF.md),
graph `bafkreieb5c7c6mgo2inqk6nkoceas6uoxbklaflv7s5f5fiao5rxpe64qu`,
source `6eff805727eb05c0a88f3c95ee97afab231bed73`. Section below audits its
ordinary argument for **rank six only**; no verdict on its general-rank theorem
or other results is conveyed. Three stable computational checks are
corroboration, never an extrapolation to infinitely many orders.

## Definitions and exact finite reduction

For an integer \(n\ge8\), let
\[
\mathcal D=\{A\subseteq[n]:|A|\le6\},\quad
F=\mathcal D\setminus\{\varnothing\},\quad
N=\sum_{a=0}^6\binom na,\quad m=N-1,\quad
s=\sum_{a=0}^5\binom{n-1}a,\quad
\alpha=\frac{(n-2)(n-3)(2n-1)}2.
\]
Every point star has size \(s\). H permits signed entries and the empty loop.
It is a real symmetric matrix with \(H_{AB}=0\) when \(A\cap B\ne\varnothing\),
\(H\mathbf1=\mathbf1\), and \(L=(N-s)H+sI\succeq0\).
The additional cap is \(NI-L\succeq0\).

On F put \(W_{AB}=\beta_{ab}\) for disjoint sets of sizes \(a,b\), and zero
otherwise, and \(C_0=sI-J+W\). The four symmetric rational 6-by-6 tables are
copied without alteration in [TABLES.json](TABLES.json). Their exact input
SHA256 is
`39f4fa1c28fadac421ac395a03090c407e0fa9053f08a3041aa4954aab0d6757`.
No search output, solver state or author proof module is an input. Direct
substitution checks, for every \(1\le a\le6\),
\[
\sum_b\beta_{ab}\binom{n-a}b=m-s,\qquad
\sum_b b\beta_{ab}\binom{n-a}b=(n-a)s.                 \tag{1}
\]
Thus \(C_0\mathbf1=C_0x_i=0\), where \(x_i(A)=1_{i\in A}\).
These \(n+1\) vectors are independent: singletons force the point
coefficients to equal minus the constant coefficient, and a pair forces that
constant coefficient to vanish.

For completeness, on the full layers let U raise by inclusion summation and
let D be its transpose. Counting exchanges gives
\(D_{a+1}U_a-U_{a-1}D_a=(n-2a)I\). Therefore U is injective below the middle,
and \(\mathcal H_j=\ker D_j\) has dimension
\(d_j=\binom nj-\binom n{j-1}\) for \(0\le j\le\lfloor n/2\rfloor\).
For \(h\in\mathcal H_j\), lift by
\(h_a(A)=\sum_{S\subseteq A,|S|=j}h(S)\). The commutator gives
\[
D_a h_a=(n-a-j+1)h_{a-1},\qquad
\|h_a\|^2=\binom{n-2j}{a-j}\|h\|^2.
\]
The lifts vanish below j and above \(n-j\). Transferring raising operators
through an inner product proves orthogonality of different harmonic degrees;
the dimensions telescope to \(\binom na\) in every layer, including those
above the middle. This proves full exhaustion, rather than only a check of
invariant vectors. Repeated lowering annihilates the sums over harmonic
j-sets containing any smaller fixed set. Inclusion-exclusion then gives
\(\sum_{S\subseteq A^c,|S|=j}h(S)=(-1)^jh_a(A)\). Counting the disjoint b-sets
containing S proves the disjointness action
\[
D_{ab}h_b=(-1)^j\binom{n-a-j}{b-j}h_a.                 \tag{2}
\]
These are prior slice harmonics, also used in credited
[LEMMA7980](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md).

The actual block layer ranges and metrics are
\(A_j=\{\max(1,j),\ldots,\min(6,n-j)\}\) and
\(G_j=\operatorname{diag}_{a\in A_j}\binom{n-2j}{a-j}\), for
\(0\le j\le\min(6,\lfloor n/2\rfloor)\). All metric entries are positive.
The lower and upper seed blocks are
\[
(K_j)_{ab}=s\delta_{ab}-1_{j=0}\binom nb
             +(-1)^j\beta_{ab}\binom{n-a-j}{b-j},\qquad
(U_j)_{ab}=N\delta_{ab}-1_{j=0}\binom nb-(K_j)_{ab}.     \tag{3}
\]
They occur with multiplicity \(d_j\). Although K and U need not be symmetric
in these coordinates, \(G_jK_j\) and \(G_jU_j\) are symmetric; their PSD is
equivalent to operator PSD by positive metric congruence.

Let \(P_0\) be the G-orthogonal projection off the span of vectors 1 and a,
\(P_1\) the projection off 1, and \(P_j=I\) otherwise. Explicitly,
\[
G_0P_0=G_0-G_0V(V^TG_0V)^{-1}V^TG_0,\quad V_a=(1,a),
\qquad G_1P_1=G_1-gg^T/\sum_a g_a.
\]
The independent checker verifies, in every boundary block,
\[
G_jK_j\succeq G_jP_j,\qquad G_jU_j\succeq G_j/4.       \tag{4}
\]
Ranks are exactly block order minus2 in degree0, minus1 in degree1, and full
in other degrees. The complete records are:

| n | N | s | Block orders | Multiplicities | Seed ranks |
|---|---:|---:|---|---|---|
|8|247|120|6,6,5,3,1|1,7,20,28,14|4,5,5,3,1|
|9|466|219|6,6,5,4,2|1,8,27,48,42|4,5,5,4,2|
|10|848|382|6,6,5,4,3,1|1,9,35,75,90,42|4,5,5,4,3,1|
|11|1486|638|6,6,5,4,3,2|1,10,44,110,165,132|4,5,5,4,3,2|

In every row weighted block orders sum to m and weighted ranks to
\(N-n-2\). Consequently \(C_0\) has precisely the forced kernel and is at
least I off it; \(U_0=NI-J-C_0\succeq I/4\).

## Independent certificates and original vertices

[audit.py](audit.py) uses standard-library integers and Fraction. Its PSD
criterion computes **every nonempty principal minor**, with exact row-pivoted
Gaussian determinants; rank is checked by a separate rational row reduction.
It does not use either author Schur-complement or integer-Bareiss checker.
For a real symmetric matrix, nonnegative principal minors imply PSD: adding
\(\epsilon I\) makes every leading minor strictly positive (expand it as a
polynomial in \(\epsilon\) whose coefficients are principal minors), apply
Sylvester's positive-definite criterion, and let \(\epsilon\downarrow0\).
This justifies the actual criterion, including singular cases.

Across the four boundary and three corroborating stable orders, the checker
validates **516 rational forms and 16,342 principal minors**, including the
new endpoint forms and witnesses. The transcript digest, ranks, complete
metrics, thresholds and rational witness vectors are in [EXPECTED.json](EXPECTED.json).
Recomputation generates all the minors; a digest alone is not a PSD premise.

At \(n=8\) there is an additional original-index audit. Enumerate every
ballot top j-set \(B=\{b_1<\cdots<b_j\}\), one-based \(b_i\ge2i\), and greedily
choose distinct \(a_i<b_i\) outside B. The harmonic product
\(h=\prod_i(X_{a_i}-X_{b_i})\) lifts to its literal membership polynomial on
each layer. Pair cancellation shows it is harmonic. The program constructs
all **246** layer-supported columns, checks their exact rank246 modulo the
independently trial-division-verified prime1,000,003, all **121,032** seed and
trade action scalars against (3), **27,834** cross-sector orthogonality pairs,
all lift norms \(2^j\binom{n-2j}{a-j}\), and **174** absent lifts. Full rank
modulo a prime implies full rational and real rank. This checks a complete
basis, not just the author's21 illustrative matching columns.

For each of \(t=1/(8\alpha)\) and \(t=1/\alpha\), it independently assembles
the original247-by-247 L from the core by the E lift below and compares all
**61,009 entries** to the direct disjoint-weight/empty-row formula. Symmetry,
row sums, support and every centered star are checked entry by entry. The
original endpoint matrix SHA256 is
`d07edcaba361e39465917e88d03be33d426236aa0a61a10e20a592ab045aabbe`,
exactly matching the author's frozen expected record. Its empty diagonal is
37/30; at the extended endpoint it is43/15. Neither empty row nor loop is
removed. Full-basis action and small-block PSD prove the large-matrix ranks;
I do not rerun a large dense elimination.

The author's `--blocks-only` command was also replayed in normal and optimized
Python, matching its frozen expected record with `literal` set to null. All
43 complete blocks and29 original rejection controls agree. The author's
separate full247 elimination run and its reported runtime are not
independently replayed or endorsed. Our independent complete-basis audit
supplies the original-index mathematical validation.

## Ordinary audit of every n>=12, restricted to rank six

For these orders all \(\binom{n-a}b\) with \(1\le a,b\le6\) are positive.
Put \(B_a=\binom na\) and
\[
M=\sum_{a=1}^6B_a(1,a)^T(1,a)
 =\begin{pmatrix}m&ns\\ns&\sum_a a^2B_a\end{pmatrix},\qquad
F=e_1e_1^T-sM^{-1},
\quad \beta_{ab}=\frac{B_b}{\binom{n-a}b}(1,a)F(1,b)^T.       \tag{5}
\]
M is positive definite because the rows for layers1 and2 are independent.
Symmetry of \(B_aB_b/\binom{n-a}b\) follows from its factorial formula.
Multiplication by the two columns of M proves (1). In degree0, (3) becomes
\(K_0=sP_0\), by cancelling the rank-one J term.

For \(j\ge1\), let \(q_j(a)=(a)_j/(n-a)_j\), zero if \(a<j\), where falling
factorials occur. The unsigned disjointness block is RFT transpose with
\(R_a=(1,a)/(n-a)_j\) and \(T_a=B_a(a)_j(1,a)\). The identity
\[
\frac{g_j(a)}{(n-a)_j}=\frac{B_a(a)_j}{(n)_{2j}}
\]
shows its orthonormal representative has the same nonzero eigenvalues as
\(M_j^{1/2}FM_j^{1/2}\), where
\(M_j=\sum_a B_aq_j(a)(1,a)^T(1,a)\).
Indeed, if X has rows \(\sqrt{B_aq_j(a)}(1,a)\), the representative is
XFX transpose and \(X^TX=M_j\); polar decomposition gives the assertion,
also for singular M_j.

Since \(n\ge12\ge2a\), successive falling-factor ratios are at most1:
\(0\preceq M_j\preceq M_1\preceq M\).
For \(j\ge2\), \(M_1-M_j\succ0\): layers1 and2 already have strictly positive
weight differences and independent row vectors. If \(0\preceq B\preceq A\)
with A positive definite, then \(T=B^{1/2}A^{-1/2}\) is a contraction and
\[
B^{1/2}FB^{1/2}=T(A^{1/2}FA^{1/2})T^T.                 \tag{6}
\]
Equation (6) is a **congruence contraction**, not multiplication of a Loewner
inequality by an indefinite F. For B strictly below A, its norm is strictly
less1. The eigenvalues of \(M^{1/2}FM^{1/2}\) are \(m-s\) and \(-s\).
This initially bounds the negative eigenvalue of the degree-one block below
by \(-s\). Its forced star kernel gives a positive eigenvalue exactly s in
the unsigned block. F is indefinite of rank2
(\(\det F=-s(m-s)/\det M<0\)), so that block has at most one positive
eigenvalue and consequently norm s. Applying (6) now with A=M1 proves norm
strictly below s for every higher degree. Thus
\[
0\preceq C_0\preceq2sI,\quad
\ker C_0=\operatorname{span}(\mathbf1,x_1,\ldots,x_n),\quad
K_1\succeq sP_1.                                      \tag{7}
\]
This is an ordinary proof for every integer n>=12. Exact evaluations at
12,16,32 in the code corroborate it, but are not used to obtain its quantifier.

## Repair, whole-vertex lift, universal rank and products

Use the credited singleton/pair trade
[LEMMA7745](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md):
on disjoint nonempty sets its only weights are
\(d_{11}=(n-2)(n-3)\), \(d_{12}=d_{21}=-(n-3)\), \(d_{22}=1\).
Put \(C_t=C_0+t\Delta\) and \(U_t=U_0-t\Delta\).
Direct block multiplication confirms its nonzero eigenvalues: one \(\alpha\)
in degree0, one \(-b\) in degree1 where \(b=(n-1)(n-3)\), and one1 in degree2;
other degrees vanish. Degree0 kills a and removes the seed's constant
direction, degree1 kills1, and \(b/\alpha<1\).
For the author's \(0<t\le1/(8\alpha)\), (4) immediately gives
\(C_t\succeq0\), core rank \(m-n\), and \(U_t\succeq I/8\).

For the stable branch the stronger \(0<t\le1/\alpha\) also has core rank m-n:
degree1 off its kernel is at least \(s-tb>0\), degree0 is a sum of PSD forms
with common kernel a, and the other sectors are positive.
Here \(U_0\mathbf1=\mathbf1\), while on constants perpendicular it is at
least \((N-2s)I\). Pascal gives \(N-2s=\binom{n-1}6\ge3\).
The degree-zero positive trade direction u has layer coordinates n-1,-1
on layers1,2. For normalized constant c,
\[
|\langle c,u\rangle|^2=\frac{n(n-1)}{2m(2n-1)}\le\frac19,
\]
using \(m\ge n(n+1)/2\) and
\((n+1)(2n-1)-9(n-1)=2(n-2)^2\ge0\).
On the full core,
\(U_0-I\succeq2P_{c^\perp}\) and
\(I-\Delta/\alpha\succeq(1-1/\alpha)P_{u^\perp}\).
The projection sum has least eigenvalue
\(1-|\langle c,u\rangle|\ge2/3\). Therefore
\[
U_{1/\alpha}\succeq\tfrac23(1-1/\alpha)I\succeq\tfrac47 I.  \tag{8}
\]
Convexity with \(U_0\succeq I\) proves (8) throughout the closed interval.

Let E have top row minus the all-one row and the remaining rows I_m.
The credited whole-vertex construction
[LEMMA7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md)
is
\[
L=J_N+EC_tE^T,\qquad H=(L-sI)/(N-s),\qquad NI-L=EU_tE^T.   \tag{9}
\]
Its two lower summands have orthogonal ranges, giving rank L=N-n;
\(E^TE=I+J\succeq I\) transfers any positive core cap floor to every nonzero
whole cap eigenvalue, and rank(NI-L)=N-1. The required empty entries are
\[
L_{00}=1+\tfrac14tn(n-1)(n-2)(n-3),\quad
L_{0A}=1-\tfrac12t(n-1)(n-2)(n-3)\ (|A|=1),\quad
L_{0A}=1+\tfrac12t(n-2)(n-3)\ (|A|=2),
\]
and \(L_{0A}=1\) otherwise. Support and normalization follow from (1),(9).
Thus H has simple unit eigenvalue and least eigenvalue \(-s/(N-s)\) with
multiplicity n.

The universal rank argument holds for **every real H**, even without cap or
invariance. For a point-star indicator x, support gives \(x^TLx=s^2\) and
\(L\mathbf1=N\mathbf1\); its centered indicator has zero lower quadratic
form, hence lies in the PSD kernel. The n centered stars are independent by
evaluation at empty and singletons, forcing rank L<=N-n. Our construction
attains it. For an intersecting-family indicator f of size a, the centered
quadratic form is \(sa-a^2\ge0\). Equality forces f to be an affine point sum.
Empty, singleton and pair values force exactly one point coefficient1,
yielding a star. This credited mechanism is also in
[LEMMA7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md);
the maximum-family classification is not a new historical claim.

For any nonempty finite product on disjoint blocks, use the tensor of the H
matrices. Put \(p_* =\max_i s_i/N_i\), \(s_P=N_Pp_*\), and
\(d_* =\sum_{i:s_i/N_i=p_*}n_i\). The eligible star cylinder has integral
size s_P. Since \(N_i-2s_i=\binom{n_i-1}6>0\), each negative endpoint has
absolute value \(\rho_i=s_i/(N_i-s_i)<1\). Every nonunit factor eigenvalue
has absolute value strictly below1. A negative tensor eigenvalue has absolute
value at most \(\rho_*\), with equality only for exactly one factor at its
negative endpoint in an eligible block, all others at their simple unit
endpoint. A second nonunit factor strictly reduces magnitude. Consequently
the lower and upper product ranks are \(N_P-d_*\) and \(N_P-1\).
Eligible centered star cylinders are forced and independent for any real
product H, establishing universal lower-rank optimality. Evaluating an
equality-family affine indicator at empty, singletons and pairs, including
cross-block pairs, leaves exactly one eligible point coefficient1. This
confirms the target's credited product/equality mechanism; no product matrix
enumeration is necessary and no gap uniform in the number of factors is
asserted.

## Strengthening and improvement opportunities

**Proved: exact endpoints for the four fixed finite seeds.** Let
\(B_0=G_0U_0\) and \(T_0=G_0\Delta_0\). T0 is nonzero PSD of rank1.
Choose a positive diagonal \(q=(T_0)_{ii}\), let v be that column, and put
\[
T_0=vv^T/q,\quad w=B_0^{-1}v,\quad
\tau_n=q/(v^TB_0^{-1}v).                                \tag{10}
\]
The checker verifies the rank-one identity and Bw=v exactly and checks every
principal minor and rank of \(B_0-\tau_nT_0\). Cauchy-Schwarz in the B metric
proves \(T_0\preceq B_0/\tau_n\); hence for all real t,
\(B_0-tT_0\) is positive definite precisely for \(t<\tau_n\), semidefinite
of rank one less at equality, and has negative witness w for \(t>\tau_n\).
The exact endpoints are:

| n | \(\tau_n\) | \(\alpha\tau_n\) |
|---|---|---|
|8|283976183309/1022935717920|4259642749635/68195714528|
|9|4901550128623/77699349171423|83326352186591/3699969008163|
|10|7775326719743/18437010743670|2068236907451638/9218505371835|
|11|2099555803382585933/9833319482230079280|44090671871034304593/273147763395279980|

There are only two other possible decreasing forms. Degree2 upper cap has a
positive rank-one trade; degree1 lower form has a negative rank-one trade
and common constant kernel. For the latter, fix the last coordinate zero,
which is a bijective gauge for the quotient by constants, and use the
corresponding principal submatrices. Formula (10) applies to both. Their
exact thresholds and witnesses are recorded in EXPECTED.json and satisfy
\(\tau_{1,n}>\tau_n\), \(\tau_{2,n}>\tau_n\).
All other lower/cap sectors improve or remain unchanged. Independent full
block checks at t=tau confirm the lower rank and the single upper loss.
Thus for each of the four published tables, **both maximal ranks hold
exactly on \(0<t<\tau_n\)**. At \(t=\tau_n\), the lower rank remains N-n
and H remains capped, but cap rank is N-2 and the unit eigenspace has
dimension2. For t>tau the cap fails for this fixed matrix family; for t<0
the seed's constant direction has negative lower form, and at t=0 the
lower kernel has one additional direction. This is a complete family
classification, with no claim of universal nonexistence beyond its cap.

**Proved: a common eightfold interval extension and better cap floor.** Every
\(\alpha\tau_n>1\). On \(0<t\le1/\alpha\), the positive rank-one sectors obey
\(U_t\succeq(1-t/\tau_n)U_0\); the degree1 upper block improves, and the
other upper blocks are unchanged. Thus the boundary core floor is at least
\((1-1/(\alpha\tau_n))/4\). Its minimum is at n=9 and equals
\[
\gamma_* =\frac{19906595794607}{83326352186591}>\frac18.       \tag{11}
\]
Together with the audited ordinary branch (8), every integer n>=8 now has
the original rational construction for every real
\(0<t\le1/\alpha\), with lower rank N-n, cap rank N-1, and every nonzero
whole cap eigenvalue at least gamma*. Equivalently,
\(I-H\succeq\gamma_*/(N-s)\) on constants perpendicular. Rational t gives
rational entries. The factor-product conclusions remain valid throughout
this enlarged closed interval; they also hold for any finite factors using
their own strict interval \(0<t<\tau_n\). The finite active cap endpoints
are excluded from this simple-unit tensor conclusion.

The interval enlargement method has prior credit: independent
[REVIEW8648](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/rank-five-audit/REVIEW.md)
already establishes a rank-five closed1/alpha interval. That review also
proposes generalized repair endpoints without computing these four rank-six
values. The **new independently certified increment** here is their exact
table-specific classification and the resulting rank-six uniform extension.
No optimal uniform cap gap is claimed; gamma* is a certified lower bound.

**Proved presentation refinement:** star density is strictly decreasing
with order in this rank-six family. Indeed
\(s/\binom{n-1}6=\sum_{k=0}^5\binom{n-1}k/\binom{n-1}6\), and every term
is multiplied by \((n-6)/(n-k)<1\) on increasing n by1. Since
\(s/N=q/(2q+1)\), eligible product factors are exactly those of minimum
order. This repeats a known mechanism in the rank-five audit and is not
claimed as separate historical novelty.

**Open improvement:** a uniform rank-seven boundary completion would require
new rational seeds and complete truncated-sector certificates at its own
orders; these four tables provide no such result. Optimizing the finite
seed itself could move tau, but requires a new construction and checks.
Formalizing the harmonic exhaustion, all-principal-minor PSD criterion and
tensor equality argument would reduce the remaining ordinary-proof trust
boundary. General H and I remain outside this review.

## Literature, credit, reproducibility and limitations

The primary normalization and open spectral targets are
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
Their [current arXiv record](https://arxiv.org/abs/2609.28404), checked live
2026-10-01, still has the September23 v1. The paper's classical Chvatal
announcement does not supply the H matrices reviewed here. Slice harmonics
are prior work, for example
[Filmus--Mossel](https://arxiv.org/abs/1507.02713).
Candidate-specific live searches for uniform/downset Hoffman matrices,
maximal rank and rank-six statements found no primary source establishing
these four exact endpoints. This bounded search does not establish exclusive
priority. Ordinary stable-domain H was already in
[LEMMA8064](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling/PROOF.md)
and [REVIEW8104](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling_review3/REVIEW.md);
the nearby rank-five source is
[LEMMA8583](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/uniform_rank_five/PROOF.md).
The preceding n=7 proper cube has a different, credited rigidity obstruction
to star-only rank, described in
[LEMMA8020](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_rigidity/PROOF.md)
and [REVIEW8066](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_review3/REVIEW.md).
I read that context; this review gives no new verdict on those cube claims
and asserts no constructor or rank-six conclusion at n=7.

Reproduction commands, exact expected results and controls are in
[README.md](README.md), [EXPECTED.json](EXPECTED.json),
[CONTROLS.json](CONTROLS.json) and [VALIDATION.json](VALIDATION.json).
Normal and optimized CPython3.11.2 outputs agree byte for byte. Eleven
damaged forms/inputs reject, and exact negative cap witnesses beyond every
finite active endpoint and negative lower witnesses for t<0 pass.
Own computations use no solver, CAS, BLAS or third-party package, no author
proof import, no numerical tolerance, and no assertion-dependent checks.
All mathematical jobs run sequentially with numerical thread variables1,
fixed90-second guards, peak memory below40MiB, and no resource escalation.

Trust boundaries are the inspected independent Python, exact integer and
Fraction implementations, original table decoding, and the ordinary
unformalized arguments written here. Tables are treated as exact candidate
data and proved valid by independent arithmetic, rather than trusted as
certificates because of provenance. The infinite proof, universal rank and
tensor classification receive ordinary audits; they are not machine-formal
theorems. No exhaustive search over all H, priority guarantee, general H/I
solution, new classical Chvatal proof, or optimal cap gap is asserted.
