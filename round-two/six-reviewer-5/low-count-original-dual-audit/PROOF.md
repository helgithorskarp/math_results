# Original dual exclusion and quantitative spectral separation

Actual reviewer **six-reviewer-5**, role **independent mathematical reviewer**,
2026-10-04. Ordinary, unformalized proof. Written target and named parent proofs
were exposed; new native author programs, outputs and controls were never imported.
The original defining table is a credited mathematical input. The finite vectors
are untrusted author certificate data, checked completely by our new energy reader.

## Scope and physical coordinates

Use exactly the original four-repair face in LEMMA10222/0. Its nonempty members
are the sets of size one or two and the triples containing at least two of
\(a,b,c\), with \(bcx\) removed for \(x\in Z\), where \(Z\subseteq W\),
\(|W|=q\), \(|Z|=k\). The actual empty vertex is retained. Set
\[
 N=(q^2+13q+16)/2-k,\quad s=3q+4,\quad
 C=C_0+\kappa\Delta+t_bR_b+t_cR_c+\sigma B,\quad U=NI-J-C.
\]
The repairs and the whole affine disjoint table are exactly the target's
specified definitions; the parameters are independent arbitrary real numbers.
For \(E=[-\mathbf1';I]\), set \(L=J+ECE'\) and
\(M=(L-sI)/(N-s)\). We use no optimized residual or nonfixed-space positivity.

An orbit coordinate is its value at every original member, without normalization.
An orbit has key \((c,z,w)\), with \(c\) the core bitmask, and \(z,w\) the numbers
of outside points in \(Z,W\setminus Z\). Its mass is
\(m_i=\binom{k}{z}\binom{q-k}{w}\). The 23 possible types omit \((6,1,0)\).
Zero-mass types may remain as zero rows; there is no division by their mass.
For disjoint core masks, the ordered disjoint pair count from type \(i\) to
\(j=(d,z',w')\) is
\[
 m_i\binom{k-z}{z'}\binom{q-k-w}{w'};
\]
it is zero for intersecting core masks. This follows by choosing the first set,
then choosing the second set outside it in each of the two outside blocks.
Multiplying by the original table's base and slope gives every disjoint entry.
The \(C_0\) diagonal and intersecting entries give
\[
 G_{C_0,ij}=s m_i\delta_{ij}-m_im_j+
  (\text{ordered disjoint pair count})\,\operatorname{base}_{ij}.
\]
The Delta Gram is the same ordered count times the slope; the upper Gram is
\(Nm_i\delta_{ij}-m_im_j-G_{C_0,ij}\). The repair Grams are literal singleton
core edges, each counted in both orders. These are quadratic energies on actual
members, with no invariant-subspace or quotient-positivity assertion.
This counting proves the formulas for every deletion set: permuting the outside
points fixing \(a,b,c\) carries every \(Z\) to the first \(k\) points.

## The new low-count leaf

Define the target's physical vectors \(y,v,\zeta\): \(y=1/2\) on \(ax,abc\),
\(1\) on \(b,c\), \(3/4\) on \(bx,cx\), \(-1/4\) on \(abx,acx\), and zero
elsewhere; \(v=2\mathbf1-e_b-e_c\); \(\zeta=1\) on outside-only members,
\(-1\) on \(abc\), zero elsewhere. Our complete exact calculation in
\(\mathbb Q(q,k)\) gives the five affine coefficient vectors, ordered as
constant, kappa, independent b trade, independent c trade, BC trade:
\[
 \begin{aligned}
 y'Cy&=3q/2+9/4+2\sigma,\\
 v'Uv&=3q^2+33q+28-12kq+4k^2-14k-d\kappa-2\sigma,\\
 \zeta'C\zeta&=\alpha\kappa,\\
 d&=2q(q+1)+\frac{4(3q+1-2k)}{3q+5},\\
 \alpha&=q(q+1)/2+\frac{3(q+1)}{3q+5}.
 \end{aligned}
\]
All independent repair coefficients are checked individually. For integers
\(q\ge4,0\le k\le q\), \(N-s>0\), \(\alpha,d>0\).
Both original cones being PSD forces \(\kappa\ge0\). Hence their necessary
nonnegative energy sum cannot equal
\[
 A-d\kappa<0,\qquad
 A=3q^2-12kq+4k^2+69q/2-14k+121/4,
\]
whenever \(A<0\). This excludes the whole real prescribed face without any
rank, strictness, upper kappa or equal-trade hypothesis.

For \(k=17+x\), the endpoint polynomials are exactly
\[
 A(k,k)=-4265/4-299x/2-5x^2,\qquad
 A(3k-1,k)=-107/4-173x/2-5x^2.
\]
They are negative for every real \(x\ge0\). Convexity in \(q\) bounds \(A\)
above by its endpoint chord, so every integer \(k\ge17,k\le q<3k\) is excluded.
For \(8\le k\le16\), direct complete integer coverage of this bounded range
leaves precisely the 33 target points with \(A\ge0\). The input certificate
supplies all 23 physical coordinates of each lower and cap vector, with positive
weights 1,1. Our checker requires the exact point list, whole coordinate order,
dyadic coordinates and every supplied affine coefficient, then recomputes them
from the original counting formula. At each point the sum is \(a+b\kappa\),
with \(a<0,b<0\), and every repair coefficient zero. It independently checks the
original orientation at that point. Thus all 33 points are excluded as well.
The least constant and slope margins are exactly the target's
\(2306279189/16580608\) and \(74897067859/197197824\).

This proves the entire NEW negative leaf: every \(k\ge8,k\le q<3k\), every
\(Z\), all real prescribed parameters. LEMMA10032's complete k7 theorem and
LEMMA10206's \(q\ge3k\) classification remain explicit ordinary premises.
Since the stated threshold exceeds \(3k\) for every \(k\ge7\), those two
premises and this new leaf exhaust \(q\ge k\). No whole-parent audit is inferred.

## Strengthening: unrestricted-parameter original spectral margin

The following is a new quantitative consequence, proved here. For a physical
nonempty vector \(x\), extend it by zero at the actual empty vertex and center:
\[
 \widehat x=(0,x)-\frac{\sum_A x_A}{N}\mathbf1_N,\qquad
 \beta_x=\|\widehat x\|^2=\sum_Ax_A^2-\frac{(\sum_Ax_A)^2}{N}>0
 \quad(x\ne0).
\]
Then \(E'\widehat x=x\), and direct original multiplication gives
\[
 \widehat x'L\widehat x=x'Cx,\qquad
 \widehat x'(NI-L)\widehat x=x'Ux.
\]
Both centered vectors lie in \(mathbf1^\perp\). This is the actual empty
lift; an unweighted orbit norm would give the wrong margin.

Suppose both original endpoint forms are bounded below by
\(-\tau I\) on \(mathbf1^\perp\), for \(	au\ge0\). The orientation forces
\(kappa\ge-\tau\beta_\zeta/\alpha\). A lower/cap dual sum \(a-d\kappa\),
where \(a<0,d>0\), is at least \(-\tau(\beta_y+\beta_v)\), so
\[
 \tau\ge \varepsilon:=
 \frac{-a}{\beta_y+\beta_v+(d/\alpha)\beta_\zeta}>0.                 \tag{1}
\]
This works for EVERY real kappa and all other real parameters: it needs no
exact lower-PSD orientation assumption. Consequently at least one of the two
original endpoint minimum eigenvalues on \(mathbf1^\perp\) is at most
\(-\varepsilon\). Equivalently, either the desired lower bound for \(M\) fails
by at least (arepsilon/\(N-s\)), or its cap fails by that amount. These are
certified separation bounds, without a claim that they are optimal distances.

For the constant vectors, exact complete member sums give
\[
 \begin{aligned}
 \beta_y&=(6q+9)/4-(3q+5)^2/(4N),\\
 \beta_v&=4N-10-(2N-4)^2/N=6-16/N,\\
 \beta_\zeta&=r+1-(r-1)^2/N,\qquad r=q(q+1)/2.
 \end{aligned}
\]
Apply \(1\) with \(a=A,d\) above for every integer \(q\ge4,0\le k\le q,A<0\).
At each of the remaining 33 points apply it to that point's full physical
certificate vectors and \(d=-b\). The record contains each exact norm,
orientation and endpoint/M margin. The least endpoint margin over those 33
points is \(349456647834036/445397087370401\), attained at \(k8,q23\);
the least M margin is
\(7135621763051595824/4735724112764259815823\), attained at \(k16,q47\).
Thus every point of the entire new low-count domain has an explicit strictly
positive unrestricted-parameter spectral separation.

On \(q=2k,k\ge8\), \(A=-167/4-73(k-8)-8(k-8)^2<0\).
The symbolic record also supplies complete rational numerator/denominator
coefficients for \(1\) and its M margin on this line. Their leading degrees and
coefficients give
\[
 \varepsilon(2k,k)/k\longrightarrow8/47,\qquad
 k\,\varepsilon(2k,k)/(N-s)\longrightarrow4/47.
\]
For a separate hand check, \(N=2k^2+12k+8\), \(-A\sim8k^2\),
\(d/\alpha\to4\), \(eta_y\sim3k\), \(eta_v\to6\), and
\(eta_\zeta\sim11k\). These give denominator \(47k\) in \(1\) and
\(N-s\sim2k^2\). The limits quantify this dual's separation; they are not
sharp optimization claims and do not exclude an enlarged repair face.

## Exact evidence and remaining ordinary bridges

The symbolic route uses SymPy1.14.0's characteristic-zero rational function
field with variable order \(q,k\), exact normalized coefficient dictionaries,
and full polynomial coefficient comparisons. It proves identities rather than
extrapolating a sample grid. The separate finite reader uses only stdlib
Fraction. Full literal-member reconstruction at \(q8/k8,q10/k8,q12/k9\) compares
EVERY entry of all six 23-coordinate forms, including zero-mass boundary types.
The two counting routes share the credited defining table; that shared definition
is an explicit trust boundary, not an independent authentication of its origin.

The source includes six complete normal/optimized positive records and 24
mathematical damage rejections. A first shared-table damage escaped the literal
comparison because both routes used the damaged definition; the final symbolic
orientation/dual checks reject it. The corrected control is recorded honestly.
No failed or partial phase is mathematical evidence. The finite certificates
are author inputs, not independently discovered vectors; all their entries,
weights, coverage and energy values are independently checked.

The original set-count derivation, real PSD implication, actual empty lift,
coefficient interpretation, convexity and two explicit classification parents
remain ordinary unformalized mathematics. Nothing here proves general H or I,
arbitrary/uncapped H absence, the later fifth-direction obstruction or a full
feasible parameter classification. No numerical optimization, failed search,
resource limit or incomplete enumeration supplies a negative conclusion.
