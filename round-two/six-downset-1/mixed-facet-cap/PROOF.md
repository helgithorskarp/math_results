# A triangle facet and a pendant at distinct cube marks

Actual author **six-downset-1**, role **researcher**, 2026-10-02.
This is an exact computer-assisted uniform theorem. The finite polynomial
identities and coefficient signs are replayed by the portable code. The real
PSD, complete-space, actual-empty and rank arguments below are ordinary and
unformalized. Independent review of this result is not claimed.

## Statement and prior scope

Let X be a set of n elements, n>=3, let x,z be distinct members of X, and
let u,v,b be distinct new elements outside X. Put

\[
 \mathcal F=2^X\cup2^{\{x,u,v\}}\cup2^{\{z,b\}},\qquad
 q=2^{n-1},\quad N=2q+8,\quad s=q+3,\quad h=N-s=q+5.
\]

**Theorem.** There is a rational symmetric matrix M on every actual member
of F, including the empty set and its permitted loop, such that

\[
 M\mathbf1=\mathbf1,\quad M_{AB}=0\ (A\cap B\ne\varnothing),\quad
 L=hM+sI\succeq0,
 \qquad h(I-M)\succeq\tfrac12 P_{\mathbf1^\perp}.                 \tag{1}
\]

Both rank L and rank(I-M) are N-1. The lower rank is greatest among **all
real H matrices** on F, without imposing rationality, an upper cap,
invariance or a sign condition. Thus the nonunit eigenvalues of M lie in

\[
 [-s/h,\;1-1/(2h)].                                          \tag{2}
\]

The cap is an additional property of this H certificate. No general
Conjecture H or inertia Conjecture I is resolved.

The unique largest star is the x-star, of size s. The z-star has q+1
members, other old stars q, u and v have four, and b has two.

Ordinary H and greatest lower rank on this family already follow from
the [one-point attachment closure](../one-point-attachments/PROOF.md),
published before this result at source
`ca8d2e363536435ad034f08cf3845a6ffd276326`, graph9361. Its raw output here
is uncapped (at n=3 its actual empty loop is7/3). The new assertion is the
**uniform capped** construction and its preserved greatest rank.
The [arbitrary-pendant result](../arbitrary-pendant-loads/PROOF.md) concerns
only new edges and supplies no triangle facet. The earlier
[two-facet](../UNEQUAL_FACETS.md) and [common-core sunflower](../ALL_PETALS.md)
results concern different facet arrangements: the three maximal facets
here have no common core with disjoint petals. Ordinary H for each finite instance is prior; the finite cap controls
here validate the new uniform construction and are not a new cohort.
The [structural core lift](../../../spectral_downsets_structural_certificates/PROOF.md)
and earlier [six-element forced-star argument](../../../spectral_downset_six_exact/REGULAR_SIX_PROOF.md)
are credited below. No historical priority claim is made.

The primary target is the tight weighted-Hoffman conjecture in
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version history](https://arxiv.org/abs/2609.28404), checked live on
2026-10-02, lists v1, 2026-09-23; H and I remain the open spectral targets.

## Core lift, full frame and the actual empty set

Index a core C by the nonempty sets. A Gram core with

\[
 C\succeq0,\quad C_{AA}=s-1,\quad C_{AB}=-1
          \quad(A\ne B,\ A\cap B\ne\varnothing)                 \tag{3}
\]

gives the credited full lift

\[
 E=\begin{pmatrix}-\mathbf1^T\\I\end{pmatrix},\quad
 Q=ECE^T,\quad L=J_N+Q,\quad M=(L-sI)/h.                     \tag{4}
\]

It has the required support and row sums, and is PSD below because Q is
PSD and Q1=0. Rank L=1+rank C, since E has full column rank and image
1-perp. Its actual empty vector in the Gram space is the negative sum of
the nonempty vectors; no artificial zero vector or dummy vertex is used.

If the nonempty Gram vectors are a_A and the actual empty vector a_0,
their full frame is the operator

\[
 \mathsf S=\sum_{A\in\mathcal F}|a_A\rangle\langle a_A|.       \tag{5}
\]

The nonzero spectra of S and Q agree by the elementary AA* versus A*A
identity for the column map with columns a_A. Therefore S<=(N-1)I on
its full Gram span implies

\[
 Q\preceq(N-1)P_{\mathbf1^\perp},\qquad
 NI-L=NP_{\mathbf1^\perp}-Q\succeq P_{\mathbf1^\perp}.        \tag{6}
\]

The frame, including the empty contribution, is the object checked below.

## Old cube and four marked spokes

On the 2q-1 nonempty members of the old cube use

\[
 C_0=(q+3)I+(q-3)P-J,                                      \tag{7}
\]

where P pairs proper nonempty complements and has a zero full-set row.
The original complement decomposition below proves C0 positive definite.
The identities may first be read in the formal bilinear space of (7);
that positive decomposition establishes a Euclidean realization without
assuming PSD in advance.
Write its independent Gram vectors as g_A, put G=sum g_A, f=g_X, and
H_i=-sum_{A contains i}g_A. Direct counting in (7) gives

\[
 \begin{split}
 G^2=f^2&=q+2, & Gf&=4-q,\\
 H_i g_A&=3(1-2[i\in A]), & H_iH_j&=3q\delta_{ij},\\
 GH_i=fH_i&=-3. &&
 \end{split}                                               \tag{8}
\]

In particular both signs of the first cross formula are retained.
Introduce T1,T2,T3 in a new orthogonal space with Gram
(q+3)(I3-J3/3), so sum Tj=0 and their span has dimension two.
Introduce Z in another new orthogonal direction with norm squared
2(q+3)/3. Define

\[
 H=H_x/3,\qquad
 V_j=H+T_j\ (j=1,2,3),\qquad V_4=H_z/3+Z.                  \tag{9}
\]

These represent xu,xv,xuv,zb. Their norms are w=q+2, all distinct
heavy spoke pairings are-1, the cross-mark pairings are zero, and (8)+gives every required old-set intersection pairing. Their span together
with the old cube has dimension 2q+2. Put

\[
 K=G+V_1+V_2+V_3+V_4=G+H_x+V_4.
\]

Equation (8) and the orthogonal residual spaces give

\[
 K^2=5q-4,\quad KH=q-1,\quad KV_4=q+1,\quad KT_j=0.        \tag{10}
\]

## A balanced completion with K-orthogonal contrasts

For every real q>=4 all denominators in these rational functions are
positive. Define

\[
 \begin{gathered}
 d=\frac{3(q-6)}{5q},\qquad g=\frac{q-4}{5(q+2)},\\
 b_0=\frac12\left(\frac{d(q-1)}{q+1}-g\right),\qquad
 a=-\frac{b_0(q+1)}{q-1},\qquad e=-g-2b_0,\\
 f_0=-2a-d=-\frac{g(q+1)}{q-1},\qquad
 c=\frac{(a-d)q}{q+3}.
 \end{gathered}                                             \tag{11}
\]

Coefficients b0,f0 are not the new element b or old full vector f.
Set

\[
 \begin{split}
 p_u&=-K/5+aH+b_0V_4+cT_2,\\
 p_v&=-K/5+aH+b_0V_4+cT_1,\\
 p_{uv}&=-K/5+dH+eV_4,\\
 p_b&=-K/5+f_0H+gV_4+cT_3.
 \end{split}                                               \tag{12}
\]

Their sum is-4K/5. Each of their contrasts from-K/5 is K-orthogonal,
because the three exact rational identities are

\[
 a(q-1)+b_0(q+1)=d(q-1)+e(q+1)=f_0(q-1)+g(q+1)=0.          \tag{13}
\]

Let eta_i=w-p_i^2, with eta_u=eta_v. Define

\[
 r=-1-p_up_{uv},\quad t=(\eta_{uv}+2r-\eta_b)/2,
\]

and a symmetric four-vector residual Gram W by

\[
 \begin{gathered}
 W_{ii}=\eta_i,\quad W_{u,uv}=W_{v,uv}=r,\quad
 W_{u,b}=W_{v,b}=t,\\
 W_{uv,b}=-\eta_{uv}-2r,\qquad W_{u,v}=-\eta_u-r-t.
 \end{gathered}                                             \tag{14}
\]

Every row sum of W is zero. Section "Uniform signs" proves it PSD of
rank three for all q>=4. Realize its four vectors w_i in a further
orthogonal space and put U_i=p_i+w_i, representing u,v,uv,b. Then each
has norm squared w and sum w_i=0.

For the required U/spoke intersections, equations (9)-(12) give

\[
 \begin{split}
 p_uV_1=p_uV_3=p_vV_2=p_vV_3
   &=-(q-1)/5+(aq-c(q+3))/3=-1,\\
 p_{uv}V_j&=-(q-1)/5+dq/3=-1\quad(j=1,2,3),\\
 p_bV_4&=-(q+1)/5+g(q+2)=-1.
 \end{split}                                               \tag{15}
\]

Equation (14) gives Uu.Uuv=Uv.Uuv=-1. These are **all** new
intersections: Uu and Uv are disjoint, and every Ui is disjoint from the
old cube; b and zb are disjoint from the triangle facet. Together with
(8)-(9), (15) proves all mandatory core entries in the original family.

The actual sum of the nonempty vectors is

\[
 G+\sum_jV_j+\sum_iU_i=K/5.
\]

Thus the actual empty vector is **-K/5**, and its squared norm is
(5q-4)/25. The loop and every empty-row entry are determined by (4),
without a centering assumption on that loop.

## The complete changed space and its full frame

Define the following ten physical vectors, in the displayed order:

\[
 \begin{gathered}
 g_+=G+h_0,\quad h_0=-(G+f)/2,\quad
 A_x=H_x-h_0,\quad A_z=H_z-h_0,\quad Z,\\
 t_A=T_1-T_2,\quad t_S=T_1+T_2-2T_3,\quad
 w_A=w_u-w_v,\quad w_{uv},\quad w_b.
 \end{gathered}                                             \tag{16}
\]

Their Gram Gamma has nonzero entries

\[
 \begin{gathered}
 g_+^2=q-1,\quad h_0^2=3,\quad
 A_x^2=A_z^2=3(q-1),\quad A_xA_z=-3,\quad Z^2=2(q+3)/3,\\
 t_A^2=2(q+3),\quad t_S^2=6(q+3),\\
 w_A^2=2(\eta_u-W_{u,v}),\quad
 w_{uv}^2=\eta_{uv},\quad w_b^2=\eta_b,\quad
 w_{uv}w_b=W_{uv,b}.
 \end{gathered}                                             \tag{17}
\]

All other cross terms are zero. The first seven directions are independent:
the Ax,Az plane has eigenvalues3q and3(q-2) in these coordinates and all
other displayed norms are positive. The last three have positive
definite Gram by the uniform residual certificate. Thus Gamma is PD.

In this basis H=(h0+Ax)/3, V4=(h0+Az)/3+Z and
K=g_++h0/3+Ax+Az/3+Z. Also

\[
 T_1=t_A/2+t_S/6,\quad T_2=-t_A/2+t_S/6,\quad T_3=-t_S/3,
\]

and

\[
 w_u=(w_A-w_{uv}-w_b)/2,\quad
 w_v=(-w_A-w_{uv}-w_b)/2.                                  \tag{18}
\]

These give every update vector in rational coordinates.
For the old frame S0=sum_old |g_A><g_A|, its bilinear matrix F0 on the
ten coordinates has only

\[
 (F_0)_{00}=q^2-1,\quad (F_0)_{01}=3(q-1),\quad(F_0)_{11}=9,
 \qquad(F_0)_{ij}=6\Gamma_{ij}\quad i,j\in\{2,3\}.          \tag{19}
\]

Here indices start at zero. To see (19) directly, the old complement
decomposition has S0 g_+=(q+1)g_++(q-1)h0 and
S0 h0=3g_++3h0; Ax and Az lie in its eigenvalue6 space.
These formulas follow either by summing (7) or by the pair description
in the next section, so no finite interpolation in n is involved.

The **complete** frame bilinear matrix F is

\[
 F=F_0+\sum_{a\in\{V_1,V_2,V_3,V_4,U_u,U_v,U_{uv},U_b,-K/5\}}
           (\Gamma[a])(\Gamma[a])^T.                       \tag{20}
\]

This includes all four spokes, all four unmarked new sets, and the
actual empty contribution. There are N terms in the original full frame.
[model.py](model.py) is a direct exact translation of (11)-(20).
The u/v swap changes the signs of coordinates5,7 and fixes all the
other eight. Both Gamma and F have zero cross terms between these
sectors; the code verifies these as rational identities, not sampled zeros.
Hence

\[
 B=(2q+7)\Gamma-F                                         \tag{21}
\]

splits into a2x2 antisymmetric and an8x8 symmetric block.

One diagnostic identity illustrating why (13) matters is

\[
 K^T F_0K=q^2+22q-34,
 \quad\sum_{j=1}^4(KV_j)^2=4q^2-4q+4.
\]

The U and empty contributions on K are K^4/5 because their contrasts
are K-orthogonal. Consequently the full physical cap slack along K is

\[
 (2q+7)K^2-\langle K,\mathsf SK\rangle=17q-6/5>0.          \tag{22}
\]

Equation (22) alone would not prove the cap; (21)'s complete blocks are
checked next.

## Uniform signs and independently checked polynomial identities

Substitute q=4+y with y>=0. All arithmetic in
[symbolic.py](symbolic.py) and [univariate.py](univariate.py) is exact over
Q[y] or Q(y). For each of three symmetric matrices, clear each row by
the least common multiple of its represented polynomial denominator
factors. Every such factor has nonnegative coefficients and positive
constant; its full factor/exponent list is in [RESULTS.json](RESULTS.json).
Thus each row multiplier is strictly positive for the entire half-line.
The determinant of any leading submatrix has the same sign before and
after clearing its rows.

The three matrices are the residual Gram on coordinates7,8,9 and
the two cap blocks of (21). All their cleared leading determinant
polynomials have **strictly positive coefficients**, of degrees:

| Matrix | Leading minor degrees |
|---|---|
| residual Gram, dimension3 | 6,13,20 |
| cap antisymmetric, dimension2 | 9,21 |
| cap symmetric, dimension8 | 2,15,27,41,52,64,80,96 |

The thirteen polynomials contain459 nonzero coefficients in total.
Their constants, complete coefficient fingerprints and positive row
clearing domains are recorded in RESULTS. The replay regenerates every
coefficient; hashes are evidence identities, not the reason for positivity.
Sylvester's criterion therefore proves all three original symmetric
matrices positive definite for every real q>=4, including q=4.

The determinant identities have a separate check. Exact fraction-free
Bareiss produces a polynomial p for a leading minor A(y). Independently,
the determinant degree is at most the sum, over its rows, of the largest
entry degree in that row. The code checks deg p is at most this bound d,
then checks p(j)=det A(j) at **every** integer j=0,...,d, using a separate
scalar Fraction Gaussian determinant with row swaps. The difference is
a polynomial of degree<=d with d+1 distinct roots, so it is identically
zero. This proves the symbolic identity; it neither reconstructs an
unknown polynomial without a bound nor samples a sign on y>=0.
The constant-positive coefficient certificate supplies that sign.
All exact polynomial divisions also require zero remainder. The arithmetic instantiates the credited
[earlier polynomial engine](../three-distinct-loads/polynomial.py) in one
variable; that algorithmic reuse supplies no verdict on this result. Packed
integer multiplication is checked coefficient by coefficient against
separate direct convolution on deterministic controls.

The residual Gram PD proves that (14)'s row-zero four-vector Gram is
PSD of rank three: the coordinate expressions in (18) provide a surjective
three-dimensional realization, and recover exactly every entry of (14).
Equations (17) and the other positive directions prove Gamma PD.
The two cap PD blocks prove S<N-1 on the complete changed space.
The next section supplies the remaining, unbounded-dimensional directions.

## All untouched directions and completeness

The old proper nonempty complement pairs number q-1. Their pair-constant
contrasts, with the common pair sum removed and full coordinate zero,
have dimension q-2. Equation (7) acts on them by eigenvalue2q.
Their Gram vectors are orthogonal to G,f,Hx,Hz and every new residual,
hence to all ten vectors in (16) and every update in (20).
Their full frame eigenvalue remains2q.

The old pair-antisymmetric space has dimension q-1 and eigenvalue6 under
(7). Ax and Az lie in this space and are independent for q>=4, as their
Gram from (17) is PD. Its orthogonal complement to their plane has
dimension q-3. All these directions are orthogonal to the ten changed
directions, to all updates, and to the actual empty vector; their full
frame eigenvalue remains6. Orthogonality here is in the original Gram
space; (7) acts as a scalar on each of these old spaces, so it agrees
with the corresponding coefficient-space orthogonality.

For precision, in coefficient space the high contrasts have equal values
on each proper complement pair with sum zero across pairs. The low
directions have opposite values on each pair and are constrained by
the two independent old-star linear forms. Multiplying (7) proves the
claimed eigenactions and all new-coordinate cross zeros directly.
This description includes every pair and the old full-set coordinate;
the remaining old two-plane is exactly span(g_+,h0), already in (16).

The old Gram rank is therefore
(q-2)+(q-1)+2=2q-1, and its eigenvalues on the first two spaces are positive.
The old two-plane is PD by g_+^2=q-1,h0^2=3 and g_+.h0=0.
This also establishes the PD premise used in (7).
Adding the two heavy T directions, the light Z direction and the three
private W directions gives

\[
 \operatorname{rank}C_{\rm seed}=2q+5=N-3
   =10+(q-2)+(q-3).                                      \tag{23}
\]

No physical direction is omitted. The entire full frame is the orthogonal
sum of (20), the q-2 space with eigenvalue2q and the q-3 space with
eigenvalue6. Both untouched eigenvalues are smaller than2q+7 at q>=4.
The PD blocks (21) thus prove S<=(N-1)I on its entire span. Equation (6)
establishes the seed's whole cap gap1, not just a quotient or an entrywise
bound. Its whole lower rank is N-2 by (4) and (23).

## Explicit repair to greatest lower rank

Use the credited [one-point closure](../one-point-attachments/PROOF.md)
on two private downsets: the two-dimensional cube at x and the
one-dimensional cube at z. Their largest stars are2 and1, both strictly
less than q. The loads are3 and1, so D=3,k=1. This gives a rational
raw core C_raw whose whole lower rank is N-1, and whose sole core
kernel is the x-star indicator. The present seed contains the same
forced kernel, since sum_old_x g_A=-Hx and V1+V2+V3=Hx.

For completeness, the generic raw trace formula specializes here to

\[
 \mathbf1^TC_{\rm raw}\mathbf1=9q-18+36/q,\qquad
 T=\operatorname{tr}(EC_{\rm raw}E^T)=2q^2+20q-4+36/q.       \tag{24}
\]

Indeed the private cube cores have d=3,1, largest stars2,1, and
1^TC_j1=1,0. Substitution into the credited empty-energy formula with
m=4,D=3,sum loads squared=10 gives the first expression in (24).
Adding (N-1)(s-1) gives the second. The standalone copy
[closure.py](closure.py) retains that prior constructor and its distinct
entry-table/factor comparison; copying it is not a new proof or review
of the generic closure.

Set

\[
 \epsilon=\frac1{2(1+T)}
          =\frac{q}{4q^3+40q^2-6q+72},\qquad
 C=(1-\epsilon)C_{\rm seed}+\epsilon C_{\rm raw}.             \tag{25}
\]

It preserves (3), rationality and the actual-empty lift. Both weights
are positive. The kernel of a positive convex sum of PSD matrices is
the intersection of their kernels, so C has exactly the raw one-dimensional
core kernel and rank N-2. Its whole L has rank N-1.

Let Q_raw=EC_rawE^T. It is PSD, annihilates1 and has trace T, so
Q_raw<=T P_1perp. Together with the seed bound (6),

\[
 \begin{split}
 NP_{\mathbf1^\perp}-Q
 &\succeq[1+\epsilon(N-1-T)]P_{\mathbf1^\perp}\\
 &=\left[\frac12+\frac{N}{2(1+T)}\right]P_{\mathbf1^\perp}
 \succeq\tfrac12P_{\mathbf1^\perp}.                         \tag{26}
 \end{split}
\]

Thus (1) holds and I-M has rank N-1. Finally let sigma be the indicator
of the largest x-star in any real H matrix. Its nonempty diagonal entries
in L are s and all different within-star entries are zero, so
sigma^T L sigma=s^2. Since L1=N1,

\[
 (\sigma-(s/N)\mathbf1)^TL(\sigma-(s/N)\mathbf1)=0.
\]

PSD forces this nonzero centered-star vector into ker L. Hence every
real H has lower rank at most N-1. This proves the claimed greatest
rank without a cap or symmetry assumption on competing matrices.

## Reproduction and trust boundary

[verify.py](verify.py) replays the thirteen uniform sign certificates and
all degree-bounded independent determinant identities. It also compares
every Gram/frame position between symbolic arithmetic and direct Fraction
arithmetic at nine scalar parameters, up to q=2^100. The q=1000000
control is an auxiliary real parameter, not a Boolean-cube half-size.
No literal huge family is built.

At original cube orders n=3,4,5,6, the code constructs every actual family
member, every core entry and the full lift. It compares400 original
Gram and400 original full-frame positions in total with (17)-(20),
checks every untouched eigenaction and every changed/empty cross term,
checks the complete rank census, all original support and row sums, both
whole PSD inequalities, the seed's scaled gap1, and the repaired ranks
and scaled gap1/2. The exact epsilon values are1/236,1/579,2/3325,4/21489.
Finite validation supports these reductions; it does not replace the
unbounded-dimensional argument or positive polynomial certificates.

The replay rejects meaningful coefficient, denominator, determinant,
actual-empty, support, PSD, frame and census damages, also under-O.
Complete normal and optimized mathematical records must agree with
RESULTS.json. [README.md](README.md) gives exact commands and observed
resource use. Only compact source and evidence are included.

Trust rests on ordinary real linear algebra and the written original-space
reduction, CPython arbitrary-precision integers/Fraction, the inspected
portable polynomial algorithms and their exact identity checks. No proof
assistant, solver, floating proposal, incomplete enumeration, timeout,
memory kill or reviewer verdict is a premise of this new theorem.
