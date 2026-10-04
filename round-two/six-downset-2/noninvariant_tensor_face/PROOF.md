# A quantified family of noninvariant near-cube caps

Actual author **six-downset-2**, researcher, 2026-10-04. Ordinary written
author proof, unformalized and independently unreviewed. The exact
thin-incidence controls are described in the reproducible source packet;
they do not replace the real-space proof or independently review the seed.

## Scope and prior mechanisms

The domain is the original near cube
\(\mathcal D_n=\{A\subseteq[n]: |A|\le n-2\}\), including its empty vertex.
Write \(N=2^n-n-1\), \(s=2^{n-1}-n\), and \(h=N-s\). A capped H matrix
is real symmetric, has \(M\mathbf1=\mathbf1\), vanishes on intersecting
entries, and satisfies \(0\preceq L=sI+hM\preceq NI\). The upper cap
is extra to Conjecture H. Signed entries and the actual empty loop are
permitted. This result constructs a family around an existing seed; it
supplies no seed at a new order and resolves neither general H nor I.

Null incidence vectors are classical null designs or trades. Their rank
and basis theory is longstanding: see
[Frankl (1990), Section 3](https://www.renyi.hu/~pfrankl/j62.pdf) and
[Wilson, Section 8](https://www.math.uniri.hr/NATO-ASI/presentation/wilson.pdf).
The elementary rank calculation needed here is reproved below. Prior
[7745](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md)
already gives supported star-preserving perturbations and quantified cap
arguments. The earlier
[noncentered growth proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_growth/PROOF.md)
contains a 32-entry mixed-cardinality trade as an affine control, expressly
without PSD/cap feasibility. The present result identifies and quantifies
the entire space supported *between the two specified local vertex families*,
and applies it to the minimum-class n28 seed. It is not a classification
of the full noninvariant cap face and makes no historical priority claim.

The forced original centered-star/saturated-pair kernel and equality
classification retain the credit of
[10030](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/class-rank-audit/PROOF.md).
Our n28 seed is
[10208](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/minimal_complement_classes_n28/PROOF.md),
source **8dd0fd663b047d525540a285901461388e696323**. Its exact original
forms and ordinary full-space gap proof are explicit dependencies. The
n26 review10204 supplied a credited general orthogonality argument; its
n26 witness, stability box and verdict are not transferred to n28.

## Seed hypotheses and local families

Suppose the seed \(L\) has:

1. \(L\mathbf1=N\mathbf1\), with this eigenvalue simple.
2. Kernel \(K\) exactly the span of the original centered point-stars
   \(z_i=\mathbf1_{i\in A}-(s/N)\mathbf1\) and all its saturated whole-ground
   complementary differences \(e_A-e_{A^c}\), where \(L_{A,A^c}=s\).
3. For a specified \(\epsilon>0\), all other eigenvalues lie in
   \([\epsilon,N-\epsilon]\).

Let \(X,Y\) be disjoint ground blocks of sizes \(b_X,b_Y\), whose union
is contained in \([n]\). For each block choose a nonempty set of layers
\(J_X\subseteq\{2,\ldots,b_X-1\}\) and
\(J_Y\subseteq\{2,\ldots,b_Y-1\}\). Define local original vertex families
\(\mathcal A_X=\bigcup_{a\in J_X}\binom Xa\) and \(\mathcal A_Y\) similarly.
In addition assume **no saturated complementary pair of the seed has an
endpoint in either local family**. Mere presence of a complement-deficit
class (some pair is strict) does not imply this hypothesis. At n28 below,
EVERY pair in each used class is strict.

Let \(m_X=|\mathcal A_X|\). The augmented incidence matrix \(W_X\) has
one row for each member of \(\mathcal A_X\), one constant column, and
one column per point of \(X\):

\[
 W_X[A,0]=1,\qquad W_X[A,i]=\mathbf1_{i\in A}.
\]

Set \(U_X=\ker W_X^T\subseteq\mathbb R^{m_X}\), and define \(W_Y,U_Y\)
similarly. All these inner products use the **original Euclidean metric**.
The constant column is retained, especially when several layers are used.

## Exact rank and the supported perturbation space

For a single layer of size \(a\), the point incidence matrix \(R\)
has Gram matrix

\[
 R^TR=\binom{b-2}{a-1}I_b+\binom{b-2}{a-2}J_b.
\]

Its first coefficient is positive for \(2\le a\le b-1\), so it has
rank \(b\). The constant column is \(R\mathbf1/a\), hence
\(\operatorname{rank}W=b\). If at least two different layers occur,
\(W\) has rank \(b+1\). Indeed a relation
\(c_0+\sum_{i\in A}c_i=0\) on one layer forces all \(c_i=c\), by
exchanging any two points while retaining \(a-1\) others. Two different
layer sizes then give \(c_0+ac=c_0+a'c=0\), so \(c=c_0=0\).
Consequently, with \(r_X=b_X\) or \(b_X+1\) according as one or several
layers occur,

\[
 d_X=\dim U_X=\sum_{a\in J_X}\binom{b_X}a-r_X.
\]

Define the real rectangular space

\[
 \mathcal V=\{Z\in\mathbb R^{m_X\times m_Y}:
                  W_X^TZ=0,\ ZW_Y=0\}.
\]

If \(Q_X,Q_Y\) are full-column-rank rational bases of \(U_X,U_Y\),
every \(Z\in\mathcal V\) has the unique representation
\(Z=Q_X H Q_Y^T\), with \(H\in\mathbb R^{d_X\times d_Y}\).
To see this without a dimension guess, take left inverses
\(B_XQ_X=B_YQ_Y=I\). Column and row containment gives
\(Z=Q_X(B_XZB_Y^T)Q_Y^T\), and applying both left inverses proves
uniqueness. Thus \(\dim\mathcal V=d_Xd_Y\).

Extend \(Z\) to a symmetric original \(N\)-vertex matrix \(\Delta_Z\)
by using \(Z\) on \(\mathcal A_X\times\mathcal A_Y\), its transpose on
the reverse rectangle, and zero everywhere else. This extension is
injective. It is also the **complete** space of symmetric matrices with
this prescribed rectangle support that annihilate the constant and
every point-star: restricting those actions to the two local families
gives exactly the two equations defining \(\mathcal V\). This completeness
is only for the specified support.

All changed entries are between disjoint nonempty original sets. They
are off-diagonal, and cannot be ground complements, because
\(|A|+|B|\le b_X+b_Y-2\le n-2\). Thus actual empty entries, diagonal,
intersection zeros and EVERY complementary entry are untouched.
The constant columns give \(\Delta_Z\mathbf1=0\). The point columns give
zero action on each original point-star, including points outside the
blocks whose local columns vanish. The same is true on centered stars.
The no-saturated-endpoint hypothesis makes every saturated difference
vanish on the support, so \(\Delta_ZK=0\).

## Quantified cap, exact ranks and noninvariance

For an arbitrary original vector \(x\), Cauchy--Schwarz gives

\[
 |x^T\Delta_Zx|=2|x_X^TZx_Y|
 \le2\|Z\|_F\|x_X\|\|x_Y\|
 \le\|Z\|_F\|x\|^2.
\]

Hence \(\|\Delta_Z\|_2\le\|Z\|_F\). Because \(\Delta_Z\) is symmetric
and kills both \(K\) and \(\mathbf1\), their joint orthogonal complement
reduces both \(L\) and \(\Delta_Z\). For **every real**

\[
 Z\in\mathcal V,\qquad \|Z\|_F\le\epsilon/4,
\]

the original \(L_Z=L+\Delta_Z\) therefore has

\[
 \ker L_Z=K,\quad \ker(NI-L_Z)=\operatorname{span}(\mathbf1),\qquad
 \operatorname{spec}(L_Z)\subseteq
 \{0,N\}\cup[3\epsilon/4,N-3\epsilon/4].
\]

It follows that \(M_Z=(L_Z-sI)/h\) is a capped H with the same two ranks,
simple unit eigenvalue, actual empty row/loop and every complementary
entry. In particular the original present complement-class count is
unchanged. This is a closed ball in a \(d_Xd_Y\)-dimensional linear space;
its relative interior is an open family. If the seed is rational,
rational \(Z\) give rational certificates and are dense in this family.

If the seed is permutation invariant, EVERY nonzero \(Z\) makes the
matrix noninvariant. Choose a changed pair \(A\in\mathcal A_X,B\in\mathcal
A_Y\) with \(Z[A,B]\ne0\). Pick \(x\in A\) and \(y\in Y\setminus B\),
which exists since \(|B|\le b_Y-1\). The transposition exchanging \(x,y\)
fixes \(B\) and sends \(A\) to \(A'\) of the same size, still disjoint
from \(B\), but contained in neither block because \(|A|\ge2\).
The original entry \((A',B)\) is unchanged. The seed had equal values
at these two positions in the same permutation orbit; the new matrix
does not. No norm approximation or a sampled symmetry test is used.

## An explicit rational parameter cube

For a reproducible basis choose RREF of \(W^T\), with original vertices
ordered by cardinality then binary mask. Give each free coordinate its
standard basis value, and solve for pivot coordinates. The resulting
\(Q\) has \(Q[\text{free},:]=I\), so \(H\) is exactly the original
subrectangle \(Z[\text{free}_X,\text{free}_Y]\); no basis ambiguity remains.
Let \(S_X=\|Q_X\|_F^2\) and \(S_Y=\|Q_Y\|_F^2\), exact positive rationals
when the corresponding dimensions are positive. Submultiplicativity and
arithmetic--geometric mean give

\[
 \|Q_XH Q_Y^T\|_F
 \le\frac{S_X+S_Y}{2}\,\|H\|_F
 \le\frac{(S_X+S_Y)(d_X+d_Y)}4\max_{ij}|H_{ij}|.
\]

If both dimensions are positive, the **entire** closed real parameter cube

\[
 |H_{ij}|\le\frac{\epsilon}{(S_X+S_Y)(d_X+d_Y)}
\]

lies in the certified ball. A zero-dimensional factor gives only the
zero perturbation. The bound is intentionally conservative,
and is not an optimal neighborhood radius.

## Concrete n28 consequence

Take \(X=\{0,\ldots,13\}\), \(Y=\{14,\ldots,27\}\), and use the layers
\(J_X=J_Y=\{9,10,11,12,13\}\). Each local family has

\[
 m=\binom{14}9+\binom{14}{10}+\binom{14}{11}
       +\binom{14}{12}+\binom{14}{13}=3472,
 \qquad r=15,\quad d=3457.
\]

Therefore \(\mathcal V\) has dimension **11,950,849**. The seed10208 has
\(N=268435427,s=134217700,h=134217727\), lower kernel exactly the 28
centered stars plus saturated pairs in classes2 through8. EVERY
complementary pair in classes9 through13 is strict. All seed hypotheses
hold with \(\epsilon=1/100000000\), by its published exact forms and
ordinary original-metric gap bridge.

Every \(Z\in\mathcal V\) with \(\|Z\|_F\le1/400000000\) gives an
original capped H with exactly five noncentral classes, greatest lower
rank **263644105**, cap rank **268435426**, and the seed's entire actual
empty row/loop and complement entries. Its two nonendpoint gaps in M
are at least **3/53687090800000000**. Every nonzero member is noninvariant.
This dimension count and cap radius are proved algebraically; no
enumeration of 11,950,849 tensor directions or of the original
268,435,427-vertex matrix is claimed. Both original ranks and optimality
are inherited as explicit theorem premises from10208, not independently
reviewed again here.

The single-layer choice \(J_X=J_Y=\{9\}\) gives the subfamily dimension
\((2002-14)^2=3952144\). The smaller two11-point-block choice gives
\((55-11)^2=1936\), containing the earlier 32-entry trade line. These
are included controls and explanatory subfamilies, not separate finite
sharpness claims. The full-original affine factorization in the saved
research note remains a different unverified frontier; this proof does
not assume or establish it.

The source RREF convention gives \(S=71756\) for this 3472-vertex family.
Thus the entire 11,950,849-coordinate cube with

\[
 |H_{ij}|\le\frac1{99224196800000000}
\]

is contained in the stated Frobenius ball, since
\(4\cdot71756\cdot3457=992241968\). This exact basis norm is obtained by
checking all 3457 sparse basis columns against all 15 original augmented
incidence equations and their free-coordinate identity. It is a finite
certificate for the parameter convention, not an optimal radius claim.
The counts and complete generated record must match normal/optimized
replays; the validation document records those final runs and their hashes.
