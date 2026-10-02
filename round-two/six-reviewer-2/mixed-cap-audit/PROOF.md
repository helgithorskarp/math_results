# Independent audit of the mixed-facet cap and a larger certified mixing interval

Actual reviewer **six-reviewer-2**, role **independent mathematical reviewer**,
2026-10-02. Target: LEMMA9408,
`bafkreibezbhkb2vjonipcluuqwedqxby6iodboi3jawloxl6xwonlcq7ji`,
actual researcher six-downset-1; defining source
`f8255e1d617237421c32b3d1e13dd865bffd50c4`.
This proof and the independent complete mathematical records were sealed
before inspecting any executable module or RESULTS.json from that source.
The target's displayed construction is credited, not rediscovered here.

## Exact statement and certified refinement

Let \(n\ge3\), let \(x,z\) be distinct members of an \(n\)-element set
\(X\), and let \(u,v,b\) be three distinct elements outside \(X\). Define
\[
\mathcal F=2^X\cup2^{\{x,u,v\}}\cup2^{\{z,b\}},\qquad
q=2^{n-1},\quad N=2q+8,\quad s=q+3,\quad h=q+5.
\]
The largest star is uniquely the \(x\)-star, of size \(s\): the other
sizes are \(q+1\) at \(z\), \(q\) at other old elements, \(4\) at
\(u,v\), and \(2\) at \(b\). All matrices below are indexed by every
actual family member, including the actual empty set.

The target's rational real symmetric matrix satisfies
\[
M\mathbf1=\mathbf1,\quad M_{AB}=0\ (A\cap B\ne\varnothing),\quad
L=hM+sI\succeq0,\qquad h(I-M)\succeq\tfrac12P,
\quad P=I-J_N/N.
\]
Both \(L\) and \(I-M\) have rank \(N-1\). The lower rank is greatest
among all real matrices satisfying the ordinary H conditions, without
a cap, symmetry under permutations, rationality, or entry sign restrictions
on competing H certificates (matrix symmetry itself remains an H condition).

There is also the following **proved refinement**, not an optimal interval:
keep precisely the target's seed and credited ordinary raw core, and set
\[
T=2q^2+20q-4+36/q,\qquad A=T-N+1=2q^2+18q-11+36/q.
\]
For **every real** \(0<\epsilon<1/A\), their convex mixture is an ordinary
real H certificate of greatest lower rank \(N-1\) and has
\[
h(I-M_\epsilon)\succeq(1-A\epsilon)P\succ0\quad\hbox{on }\mathbf1^\perp.
\]
It is rational when \(\epsilon\) is rational. For any \(0<\delta<1\),
\(\epsilon=(1-\delta)/A\) certifies a scaled upper gap at least \(\delta\).
In particular \(1/(2A)\) permits a strictly larger mixing weight for the
same half-gap than the target's \(1/[2(1+T)]\).
At the endpoint \(1/A\), this trace estimate gives only zero gap;
no upper-rank assertion or actual feasibility limit follows there.
Neither this review nor the target solves general Conjecture H or I.

## Complete core lift and actual empty vector

For a nonempty-indexed symmetric Gram core \(C\), require
\(C_{AA}=s-1\) and \(C_{AB}=-1\) whenever distinct nonempty sets intersect.
Use the prior structural lift
\[
E=\begin{pmatrix}-\mathbf1^T\\I\end{pmatrix},\quad
Q=ECE^T,\quad L=J_N+Q,\quad M=(L-sI)/h.
\]
Then \(Q\mathbf1=0\), \(L\mathbf1=N\mathbf1\), and every required
entry of \(M\) vanishes, including all nonempty diagonal entries.
The empty loop is permitted and determined by the lift.
Because \(E\) is injective onto \(\mathbf1^\perp\),
\(\operatorname{rank}L=1+\operatorname{rank}C\).

If \(a_A\) are the nonempty Gram vectors, the actual empty vector is
\(a_0=-\sum_{A\ne\varnothing}a_A\). The complete frame
\(S=\sum_{A\in\mathcal F}|a_A\rangle\langle a_A|\) and \(Q\) have
the same nonzero spectra, by the column-map identity for \(RR^*\) and
\(R^*R\). Thus \(S\preceq(N-1)I\) on its **whole** span implies
\(Q\preceq(N-1)P\), hence
\[
h(I-M)=NI-L=NP-Q\succeq P.
\]
The empty contribution may not be omitted from the frame or replaced
with a fictitious zero vector.

## Reconstructing the displayed seed

The old nonempty Gram is
\(C_0=(q+3)I+(q-3)P_c-J\), where \(P_c\) pairs proper nonempty
complements and has zero full-set row. Write its Gram vectors \(g_A\),
\(G=\sum g_A\), \(f=g_X\), and \(H_i=-\sum_{i\in A}g_A\).
Direct counting gives
\[
G^2=f^2=q+2,\quad Gf=4-q,\quad H_ig_A=3(1-2[i\in A]),
\quad H_iH_j=3q\delta_{ij},\quad GH_i=fH_i=-3.
\]
These are formal bilinear identities until positivity of the full old
decomposition is established below; no circular Euclidean premise is used.

Take orthogonal residuals \(T_1,T_2,T_3\) with Gram
\((q+3)(I_3-J_3/3)\), and a separate \(Z\) of squared norm
\(2(q+3)/3\). Set \(H=H_x/3\), \(V_i=H+T_i\) for \(i=1,2,3\)
and \(V_4=H_z/3+Z\). These represent \(xu,xv,xuv,zb\).
Their norms are \(q+2\). The required within-heavy and old/marked
intersections have pairing \(-1\); cross-mark entries are unconstrained.
Let \(K=G+H_x+V_4\). Then
\(K^2=5q-4\), \(KH=q-1\), \(KV_4=q+1\), \(KT_i=0\).

Use the target's rational functions, with \(b_0,f_0\) distinct from
the new element \(b\) and the old full vector \(f\):
\[
d=\frac{3(q-6)}{5q},\quad g=\frac{q-4}{5(q+2)},\quad
b_0=\tfrac12\left(\frac{d(q-1)}{q+1}-g\right),\quad
a=-\frac{b_0(q+1)}{q-1},\quad e=-g-2b_0,\quad
f_0=-\frac{g(q+1)}{q-1}=-2a-d,\quad c=\frac{(a-d)q}{q+3}.
\]
All denominators are positive for every real \(q\ge4\). Define
\[
p_u=-K/5+aH+b_0V_4+cT_2,\qquad
p_v=-K/5+aH+b_0V_4+cT_1,
\]
\[
p_{uv}=-K/5+dH+eV_4,\qquad
p_b=-K/5+f_0H+gV_4+cT_3.
\]
The \(cT_3\) term is part of the construction. The sum is \(-4K/5\),
and each contrast from \(-K/5\) is orthogonal to \(K\). The three
identities establishing this are
\(a(q-1)+b_0(q+1)=d(q-1)+e(q+1)=f_0(q-1)+g(q+1)=0\).

Put \(\eta_i=q+2-p_i^2\), \(r=-1-p_up_{uv}\), and
\(t=(\eta_{uv}+2r-\eta_b)/2\). The four residual vectors have Gram
\(W\) with diagonal \(\eta_i\) and entries
\[
W_{u,uv}=W_{v,uv}=r,\quad W_{u,b}=W_{v,b}=t,\quad
W_{uv,b}=-\eta_{uv}-2r,\quad W_{u,v}=-\eta_u-r-t.
\]
All rows sum to zero. Its residual three-space is proved positive
definite below. Thus it has a rank-three Euclidean realization with
\(\sum w_i=0\). Put \(U_i=p_i+w_i\), representing \(u,v,uv,b\).
Every norm is \(q+2\).

The rational identities in frame.py check all eight mandatory marked/private
intersection pairings and the two private/private intersection pairings.
Together with the old/marked counting, this is the full case partition:
private sets contain no old elements; marked sets contain exactly their
specified old mark; distinct marked sets at different marks are disjoint;
within the triangle, \(u\) meets \(xu,xuv,uv\), \(v\) meets
\(xv,xuv,uv\), and \(uv\) meets all three marked sets; \(b\) meets only
\(zb\). No sign or support condition is imposed on permitted disjoint
entries. Finally the sum of all nonempty vectors is \(K/5\), so
\(a_0=-K/5\), with squared norm \((5q-4)/25\).

## Changed coordinates and full frame

The physical ten-vector basis, in order, is
\[
g_+=(G-f)/2,\ h_0=-(G+f)/2,\ A_x=H_x-h_0,\ A_z=H_z-h_0,\ Z,
\ t_A=T_1-T_2,\ t_S=T_1+T_2-2T_3,\ w_A=w_u-w_v,\ w_{uv},\ w_b.
\]
Its Gram \(\Gamma\) has first-seven squared norms
\[
q-1,\ 3,\ 3(q-1),\ 3(q-1),\ 2(q+3)/3,\ 2(q+3),\ 6(q+3),
\]
the cross entry \(\Gamma_{23}=-3\), and no other first-seven crosses.
The last-three block has diagonal
\(2(\eta_u-W_{u,v}),\eta_{uv},\eta_b\), cross
\(\Gamma_{89}=W_{uv,b}\), and all other crosses zero. The first seven
are positive definite since the \(A_x,A_z\) plane has eigenvalues
\(3q,3(q-2)\); residual positivity supplies the last three.

The inverse expressions
\[
T_1=t_A/2+t_S/6,\quad T_2=-t_A/2+t_S/6,\quad T_3=-t_S/3,
\]
\[
w_u=(w_A-w_{uv}-w_b)/2,\quad
w_v=(-w_A-w_{uv}-w_b)/2
\]
recover the full residual Gram, not only a principal corner: symmetry
and zero row sums determine the fourth direction. Also
\(H=(h_0+A_x)/3\), \(V_4=(h_0+A_z)/3+Z\),
\(K=g_++h_0/3+A_x+A_z/3+Z\).

The old frame bilinear matrix \(F_0\) is zero outside
\[
(F_0)_{00}=q^2-1,\quad (F_0)_{01}=3(q-1),\quad(F_0)_{11}=9,
\qquad(F_0)_{ij}=6\Gamma_{ij}\quad(i,j\in\{2,3\}).
\]
Indeed the old frame sends \(g_+\) to
\((q+1)g_++(q-1)h_0\), and \(h_0\) to \(3g_++3h_0\), while
\(A_x,A_z\) have eigenvalue six. Counting in \(C_0\) gives these
identities for every cube order; finite tests are not their general proof.
The full changed-space frame is
\[
F=F_0+\sum_{v\in\{V_1,V_2,V_3,V_4,U_u,U_v,U_{uv},U_b,-K/5\}}
(\Gamma[v])(\Gamma[v])^T.
\]
The last term is the actual empty contribution. Coordinates 5,7 change
sign under \(u/v\) exchange; the other eight are fixed. The exact
rational computation verifies all cross-block entries of
\(B=(2q+7)\Gamma-F\) vanish. Both resulting cap blocks and the residual
three-block have strictly positive leading minors uniformly, as follows.

## Independent bounded polynomial reconstruction

rational.py is a new reviewer implementation. It uses ordinary direct
coefficient convolution, scalar Fraction Gaussian elimination with row
swaps, and Newton forward-difference interpolation as its **primary**
determinant method. It does not import the target's polynomial engine,
fraction-free Bareiss implementation, literal constructor, or fixtures.
Scalar Gaussian elimination is standard mathematics and also appears as
a secondary identity check in the target; independence is in the new
implementation, determinant reconstruction, controls, and complete record.

Set \(t=q-4\ge0\). Every rational denominator is a product of powers
of \(t+4,t+3,t+5,t+6,t+7\) and positive constants. Known linear factors
are cancelled only by exact synthetic division with zero remainder.
Each row is cleared by its factorwise least common multiple and a positive
integer clearing the remaining Fraction denominators. Every row multiplier
is positive throughout the half-line, including \(t=0\).
The cleared matrix need not remain symmetric; Sylvester's criterion is
applied to the original symmetric matrix, whose leading determinant signs
are unchanged by these positive row multipliers.

For any cleared leading submatrix \(D(t)\), a rigorous determinant degree
bound is
\(d=\sum_i\max_j\deg D_{ij}\), from the permutation expansion.
The scalar determinant is evaluated exactly at every integer
\(0,1,\ldots,d\). Newton interpolation produces the unique polynomial
of degree at most \(d\) with these values. Both this reconstructed
polynomial and the actual determinant have degree at most \(d\), and
their difference has \(d+1\) distinct roots. Hence they are identically
equal. Every interpolation residual and integer coefficient is checked.
This is an identity proof, not extrapolation from finitely many sign samples.

All thirteen reconstructed polynomials have **strictly positive**
coefficients, including their constant coefficients:

| Original symmetric block | Actual leading determinant degrees | Proven degree bounds |
|---|---|---|
| residual, dimension 3 | 6,13,20 | 6,13,20 |
| antisymmetric cap, dimension 2 | 9,21 | 9,21 |
| symmetric cap, dimension 8 | 2,15,27,41,52,64,80,96 | 2,15,27,41,53,65,81,97 |

There are 459 positive coefficients and 463 exact determinant evaluations.
The complete row multiplier exponents, integer multipliers, degrees,
constants, minimum coefficients, and coefficient/evaluation fingerprints
are in SYMBOLIC-EXPECTED.json. Regeneration verifies the whole record;
the hashes are identities of evidence, not the argument for positivity.
Strictly positive coefficients prove the half-line signs, so all three
original symmetric blocks are positive definite by Sylvester.

## Untouched spaces and completeness for every n

There are \(q-1\) proper nonempty complement pairs. Pair-constant
coefficients with zero sum across pairs and zero full-set coefficient
form a \(q-2\) space of eigenvalue \(2q\) for \(C_0\). They are orthogonal
to \(G,f,H_x,H_z\): each old mark occurs in exactly one member of each
pair. Pair-antisymmetric coefficients have eigenvalue six and dimension
\(q-1\); the two independent old-star forms remove the \(A_x,A_z\)
plane, leaving dimension \(q-3\). Gram and coefficient orthogonality
agree on each of these scalar eigenspaces. The remaining old two-plane
is \(g_+,h_0\) with positive diagonal Gram \(q-1,3\).
This proves \(C_0\) positive definite with rank \(2q-1\).

Both untouched spaces are orthogonal to every new residual, all ten
changed vectors, all frame updates, and the actual empty vector. Thus their
complete frame eigenvalues remain \(2q\) and six. The old span plus the
three marked residual directions and three private directions has dimension
\[
2q-1+3+3=2q+5=N-3=10+(q-2)+(q-3).
\]
The changed space and these untouched spaces are independent and exhaustive.
The cap blocks give \(S<(2q+7)I\) on the changed span. Both untouched
eigenvalues are below \(2q+7=N-1\) for \(q\ge4\). Hence the entire seed
has \(Q_{\rm seed}\preceq(N-1)P\) and scaled gap at least one.
Its core rank is \(N-3\), and whole lower rank is \(N-2\).

The rational half-line certificates use auxiliary real \(q\ge4\).
Actual family cardinalities and untouched dimensions use precisely
\(q=2^{n-1}\), \(n\ge3\). No family is claimed at nonintegral auxiliary
parameters. In particular the hypotheses cannot be dropped merely because
the rational expressions exist at another \(q\).

## Rank repair, maximum possible rank, and refinement proof

The ordinary one-point attachment closure LEMMA9361, independently
reviewed in REVIEW9412, applies to the private two-cube at \(x\) and
one-cube at \(z\). Their private largest stars are 2 and 1, strictly below
\(q\); loads are 3 and 1. This credited raw core is PSD with one-dimensional
kernel, the \(x\)-star indicator \(\sigma\), and rank \(N-2\).
The seed also annihilates \(\sigma\), since the old \(x\)-star vector sum
is \(-H_x\), while \(V_1+V_2+V_3=H_x\).

The raw empty energy is \(9q-18+36/q\), and the nonempty trace is
\((N-1)(s-1)\), yielding \(T=2q^2+20q-4+36/q\).
For a positive convex mixture, the kernel is the intersection of the two
PSD kernels. Consequently every \(0<\epsilon<1\) retains precisely
\(\mathbb R\sigma\) in the core kernel, and the whole lower rank is
\(N-1\). Since the raw whole \(Q\) is PSD, annihilates \(\mathbf1\), and
has trace \(T\), it satisfies \(Q_{\rm raw}\preceq TP\). Combining the
seed and raw estimates gives
\[
NP-Q_\epsilon\succeq
[N-(1-\epsilon)(N-1)-\epsilon T]P=(1-A\epsilon)P.
\]
For \(q\ge4\), \(A=2q^2+18q-11+36/q>1\) (already
\(2q^2+18q-11\ge93\)). Thus \(0<\epsilon<1/A\) implies positive
weights and positive cap gap. This proves the stated interval and every
\(\delta\) choice. Its half-gap mixing weight is strictly larger than
the original because \(A=T-N+1<T+1\). At \(q=4\), it is \(1/204\)
instead of \(1/236\). This is a refinement of the **same trace bound**,
credited explicitly; it is not a new construction or a sharp spectral norm.

For any competing real H matrix on the family, the largest-star indicator
in whole coordinates has \(\sigma^TL\sigma=s^2\) and
\(L\mathbf1=N\mathbf1\). Therefore
\[
(\sigma-(s/N)\mathbf1)^TL(\sigma-(s/N)\mathbf1)=0.
\]
PSD puts this nonzero centered-star vector in the kernel. The lower rank
of every such H is at most \(N-1\), so the constructed rank is greatest.
For any strictly positive scaled cap gap, \(I-M\) is positive definite
on \(\mathbf1^\perp\) and vanishes on \(\mathbf1\), proving its rank
\(N-1\). This uses no nonnegative-entry assumption.

## Original-set checks and explicit trust boundary

physical.py uses a separate primitive Gram representation on every old
nonempty vector, four marked residual coordinates, and four private residual
coordinates. This representation has the two null relations
\(\sum T_i=0\) and \(\sum w_i=0\). It builds the empty coefficient
vector by **negating the sum of all actual nonempty vectors**, and checks
its difference from \(-K/5\) lies in the primitive Gram kernel.
Literal equality of redundant coefficient arrays is not required.
A pre-seal checker failure exposed this representation issue and was
corrected; it was not a target failure or evidence used for a verdict.

At \(n=3,4,5,6\), all actual family members are generated. Exact whole
support, row sums, downset closure, unique largest star, lower PSD/ranks,
scaled cap and both repaired ranks are checked. All 400 physical ten-Gram
and all 400 complete-frame positions agree with the independent rational
model. There are 52 full high-space and 48 full low-space eigenactions,
including empty and new coordinates. Four mixing choices at each order
check the original weight and the new quarter, half and three-quarter
guaranteed gaps, for 16 complete repaired matrix checks.
PHYSICAL-EXPECTED.json contains the entire stable mathematical record.

The separate symbolic controls use nine scalar parameters from \(q=4\)
to \(2^{100}\), and 15 independent literal permutation determinant
polynomials. Meaningful coefficient, denominator, symmetry, PSD, actual-empty,
support, row-sum, excessive-gap and domain damages are rejected with explicit
checks surviving Python -O. These controls support the implementation;
the unbounded conclusion rests on the full-space proof and degree-bounded
positive polynomial certificates, not these finite controls.

Trust rests on ordinary unformalized real linear algebra, CPython exact
integers/Fraction, the inspected small reviewer arithmetic implementation,
and the credited ordinary closure/structural lift. No theorem prover,
solver, floating arithmetic, incomplete enumeration, timeout, or reviewer
signature is a premise. The target's executable and fixture records are
inspected only after this proof and independent records are sealed; any
later unchanged replay is corroboration rather than independent evidence.

## Strengthening and improvement opportunities

**Proved:** the larger certified interval above, including the arbitrary
positive target gap \(0<\delta<1\) and the larger half-gap weight.
It removes rationality only for the mixing parameter when rational entries
are not required, while preserving the original family and full ranks.

**Open and potentially useful:** replace the trace bound \(T\) for the raw
whole operator with a uniform bound on its actual largest eigenvalue, or
certify the full mixed cap block as a function of both \(q,\epsilon\).
Either requires a complete-space spectral reduction and a new uniform sign
argument. Finite feasible weights or entry bounds would not establish an
optimal mixing interval. This could give a larger permitted rank repair
or gap, but no such sharp claim is made here.

**Broader attachment classes remain open here:** an arbitrary triangle
plus multiple marked pendants, or higher-dimensional private attachments,
requires fresh marked/private residual feasibility and cap certificates.
The ordinary closure alone supplies no upper cap. Relabeling \(x,z,u,v,b\)
is already covered by the theorem and adds no mathematical novelty.
