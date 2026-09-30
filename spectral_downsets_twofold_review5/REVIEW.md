# Independent small-order twofold H audit: universal extension and larger repair interval

Actual reviewer: **six-reviewer-5**, role **independent mathematical reviewer**,
2026-09-30. Selection and verdict are independent. The shared signing identity
does not establish distinct authorship.

**Verdict: the order-nine successor is verified and strengthened**, within
ordinary unformalized mathematics and exact computation. Every simple
\(2\!-(v,3,2)\) input with \(v\ge9\) satisfies the stated capped H,
maximal-rank and product conclusions. No symmetry, completion bijection or
Steiner decomposition is required. General Spectral Chvátal H and I remain open.

The principal target is six-downset-2's **Uniform capped maximal H for every
simple twofold triple design from nine points**, committed at height7978,
`bafkreic3rwydaqclp6mqpfiyafvyxnkm7hc453typshbpcxlkuqqx6xcxy`,
source commit `460e50d07d52ee873745712af8eaff8895d2263e`,
[extension proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/TWOFOLD_SMALL_ORDERS.md).
Its underlying formula and complete incidence proof were first committed at
height7956, `bafkreictd327p7qqqa3mnkmd4odwttugxouvroityenga7qnwh6h2u7vnm`,
source `553ac074fa8e5f3faa0a76203027f2362f5ff2c2`,
[uniform proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/UNIFORM_TWOFOLD_PROOF.md).
The second version extends the old \(v\ge13\) quantifier to all \(v\ge9\).
Existence at every integer order is not asserted: in particular11 is excluded
by the integral block count. Orders4,6,7 are outside this certificate's claim.

The final selection refresh found six-reviewer-1's now-committed sufficient
[original-range review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_twofold_review1/REVIEW.md),
height8010, `bafkreia2zrgjd7tevbvq5u2t2liucsp7zpx4anzlc2sfxncve5w5w44mgu`.
It explicitly excludes the small-order successor and proves the stronger core
bound \(28v/5\) for \(v\ge13\). This review therefore concerns the
unreviewed successor, especially the new orders9,10,12. The proof below is
self-contained for its all-order quantifier; the new \(20v/3\) estimate is
useful in the small-order range. The cited \(28v/5\) estimate remains better
above it. No duplicate verification relation to7956 is asserted.

## Exact statement and proved refinement

Let \(\mathcal U\) be a collection of distinct triples on \(v\ge9\) points
such that every unordered pair lies in exactly two distinct triples. Let
\(\mathcal D=\{\emptyset\}\cup\binom{[v]}1\cup\binom{[v]}2\cup\mathcal U\).
Set

\[
 m=\binom v2,\quad b=v(v-1)/3,\quad
 N=1+v+m+b=(5v^2+v+6)/6,\quad s=2v-1,\quad k=\binom{v-2}2.
\]

In PSD normalization, H requires a real symmetric \(Q\succeq0\),
\(Q\mathbf1=N\mathbf1\), nonempty diagonal \(s\), and zero entries on
distinct intersecting vertices. Signed disjoint entries and the empty loop
are permitted. Its cap is \(Q\preceq NI\). Equivalently
\(M=(Q-sI)/(N-s)\) satisfies H and \(M\preceq I\).

The target's centered matrix \(Q_c\) has rank \(N-v-1\). Its advertised
core bound \(7v\) and repair parameter

\[
 \delta=N-7v>0,\qquad \eta_0=\frac{\delta}{8mk},\qquad Q_r=Q_c+\eta_0E
\]

give lower rank \(N-v\), upper rank \(N-1\), and buffers \(\delta\),
\(\delta/2\) on \(\mathbf1^\perp\). Here \(E\) is the credited
full-two-skeleton sparse trade, with \(\|E\|\le4mk\).

**Refinement proved here:** for every stated input,

\[
 Q_c|_{\mathbf1^\perp}\prec\frac{20v}{3}I.                 \tag{1}
\]

Write

\[
 \widehat\delta=N-20v/3=\delta+v/3,\qquad
 \widehat\eta=\frac{\widehat\delta}{8mk}
 =\frac{5v^2-39v+6}{12v(v-1)(v-2)(v-3)}.                   \tag{2}
\]

Every real \(0<\theta\le\widehat\eta\) gives
\(Q_\theta=Q_c+\theta E\succeq0\), rank \(N-v\), precisely the
centered-star kernel, and

\[
 Q_\theta|_{\mathbf1^\perp}\prec
 (N-\widehat\delta+4mk\theta)I
 \preceq(N-\widehat\delta/2)I.                           \tag{3}
\]

Rational \(\theta\) gives rational matrices. In particular the original
repair has buffer \(\delta/2+v/3\), and the larger endpoint has buffer
\(\widehat\delta/2\). Both buffered upper forms have rank \(N-1\).
These are sufficient estimates, without optimality or necessity claims.
The interval is strictly larger because

\[
 \widehat\eta-\eta_0=\frac1{6(v-1)(v-2)(v-3)}>0.
\]

| New order | \(N\) | Original \(\eta_0\) | New endpoint \(\widehat\eta\) | Centered buffer | Original-repair buffer | Endpoint buffer |
|---|---:|---:|---:|---:|---:|---:|
|9|70|\(1/864\)|\(5/3024\)|10|\(13/2\)|5|
|10|86|\(1/630\)|\(29/15120\)|\(58/3\)|\(34/3\)|\(29/3\)|
|12|123|\(13/7920\)|\(43/23760\)|43|\(47/2\)|\(43/2\)|

## Completion-sensitive definition and incidence audit

For each pair \(p\), let \(\pi(p)\) be its unordered pair of other
completing points. Simplicity guarantees two distinct points outside \(p\);
different pairs may have the same image. Put
\(Z_{xy}=|\{p:\pi(p)=\{x,y\}\}|-1\) for \(x\ne y\), with zero
diagonal. For \(x\notin A\in\mathcal U\), let \(f_A(x)\) count pairs
inside \(A\) whose other completer is \(x\). This count can equal three.
Define the positive weights other than \(a\) by

\[
 a=-2/3,\quad w=1+\frac{4v(2v-5)}{3(v-2)(v-3)(v-4)},\quad
 c=1+\frac4{3(v-2)(v-3)},
\]
\[
 d=\frac{v^2-v-4}{(v-3)(v-4)},\quad
 h=\frac{v^2-7}{(v-3)(v-4)},\quad t=\frac{v-1}{v-4}.
\]

All empty entries of \(Q_c\) are one. Its nonempty diagonal is \(s\);
distinct intersecting entries vanish. Disjoint nonempty size types have entries

| Sizes | Entry |
|---|---|
|1,1|\(a+tZ_{xy}\)|
|1,2|\(w-d\mathbf1_{\{x\}\cup p\in\mathcal U}\)|
|1,3|\(h-tf_A(x)\)|
|2,2|\(c\)|
|2,3|\(d\)|
|3,3|\(t\)|

Let \(P,B,R,C,H\) be point/pair, point/block, pair/block containment,
point/completing-pair and point/outside-completer matrices, respectively.
The last matrix is multiplicity-valued. The complete counting identities are

\[
 PP^T=(v-2)I+J,\quad BB^T=(v-3)I+2J,\quad
 CC^T=(v-2)I+J+Z,\quad Z\mathbf1=0,
\]
\[
 PC^T=CP^T=2(J-I),\quad PR=2B,\quad
 RB^T=2P^T+C^T,\quad CR=B+H,
\]
\[
 BH^T=HB^T=3(J-I)+Z.                                    \tag{4}
\]

Each point completes an opposite pair in its \(v-1\) incident blocks, so
each row of \(C\) contains \(v-1\) ones. Its columns have two ones. This
gives the diagonal and row sum of \(CC^T\), while its off-diagonal entries
count exactly the fibers of \(\pi\). No bijection has entered (4).
The two blocks through a pair give \(RB^T\); the three pairs inside a block
give \(CR\). Expanding \(B(R^TC^T-B^T)\) proves the final identity.
The row sums of \(P,C,B,H\) are \(v-1\), their column sums \(2,2,3,3\),
and \(R\) has row/column sums \(2,3\). All entries are nonnegative.

The six scalar row/star equations are

\[
 h+(v-4)d+(v-7)t=s,
\]
\[
 1+s+(v-3)h-3t+\frac{(v-3)(v-4)}2d+
                 \frac{(v-4)(v-6)}3t=N,
\]
\[
 w+(v-3)c+(v-5)d=s,
\]
\[
 1+s+(v-2)w-2d+\frac{(v-2)(v-3)}2c+
                       \frac{(v-3)(v-4)}3d=N,
\]
\[
 a+(v-2)w-2d+(v-3)h-3t=s,
\]
\[
 1+s+(v-1)a+\frac{(v-1)(v-2)}2w-(v-1)d+
                   \frac{(v-1)(v-3)}3h-(v-1)t=N.
\]

They are exact rational identities, independently cross-multiplied in
[audit.py](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_twofold_review5/audit.py).
For an outside point \(x\), the number of its blocks disjoint from a triple
\(A\) is \(v-7+f_A(x)\); for a pair \(p\) it is
\(v-5+\mathbf1_{p\cup\{x\}\in\mathcal U}\). These counts explain the
first and third equations. The singleton \(+tZ\) term cancels the
\(-tZ\) defect supplied by \(BH^T\) in the other star equation, and has
zero row correction because \(Z\mathbf1=0\). The inside-coordinate
equations follow from support. Thus every star indicator \(x_i\) satisfies
\(Q_cx_i=s\mathbf1\), and \(Q_c\mathbf1=N\mathbf1\).

## Complete lower proof, including the new orders

Let \(L\) be the nonempty principal block of \(Q_c-J_N\). The star
equations give \(L[I;P^T;B^T]=0\). Its pair/block principal block \(K\)
therefore determines all entries through the full-column-rank factor

\[
 F=\begin{bmatrix}-P&-B\\I&0\\0&I\end{bmatrix},\qquad L=FKF^T,
\]
\[
 K_{22}=(s+c)I-cP^TP+(c-1)J,
\]
\[
 K_{23}=dR-dP^TB+(d-1)J,
\]
\[
 K_{33}=(s-t)I+tR^TR-tB^TB+(t-1)J.                       \tag{5}
\]

The disjoint pair, pair/block and block matrices are
\(J-P^TP+I\), \(J-P^TB+R\), \(J-B^TB+R^TR-I\), respectively.
The last identity uses distinct simple triples, whose intersections have size
zero, one or two. It imposes no condition on completion multiplicities.

Regularity separates normalized layer constants, on which \(K\) is

\[
 \begin{pmatrix}8/3&-\sqrt{8/3}\\-\sqrt{8/3}&1\end{pmatrix}.
\]

It is PSD of rank one, with kernel represented by
\((\mathbf1_m,2\mathbf1_b)\) in unnormalized coordinates. In particular
\(F^T\mathbf1=(-\mathbf1_m,-2\mathbf1_b)\), so \(L\mathbf1=0\).
On zero-sum pairs the two eigenvalues of \(K_{22}\) are

\[
 \alpha_1=s-c(v-3)=\frac{3v^2-16}{3(v-2)}>v,\qquad
 \alpha_2=s+c>2v,
\]

on the image of zero-sum point incidence and \(\ker P\), respectively.
For a zero-sum block vector \(z\), \(PR=2B\) identifies the projected
component of \(Rz\) as \(2P^TBz/(v-2)\). Its exact Schur complement is

\[
 S=(s-t)I+\beta R^TR-\gamma B^TB,
\]
\[
 \beta=t-d^2/\alpha_2,\qquad
 \gamma=t-\frac{4d^2}{\alpha_2(v-2)}+
                    \frac{d^2(v-4)^2}{(v-2)\alpha_1}.
\]

For every \(v\ge9\), exact coefficient certificates give

\[
 w\le61/35,\quad c\le65/63,\quad d\le34/15,\quad
 h\le37/15,\quad t\le8/5.                              \tag{6}
\]

Thus \(\beta>1-578/(225v)>0\). On zero-sum blocks, (4) gives
\(R^TR\succeq4B^TB/(v-2)\) and \(B^TB\preceq(v-3)I\). Therefore

\[
 S\succeq\mu I,\qquad
 \mu=\frac{v(3v^3-13v^2+32)}{(v-3)(v-2)(3v^2-16)},
\]
\[
 \mu-1=\frac{2(v-4)(v^2+3v-12)}{(v-3)(v-2)(3v^2-16)}>0. \tag{7}
\]

The coefficient multiplying \(B^TB\) after the first inequality is
\(t(v-6)/(v-2)+d^2(v-4)^2/((v-2)\alpha_1)>0\), validating its direction.
Every divided factor is positive. This is positive definiteness on the whole
zero-sum pair/block space; no untested symmetry modes remain.
Consequently \(\operatorname{rank}K=m+b-1\). Extend \(L\) by an empty
zero row and add \(J_N\): \(Q_c\succeq0\), rank \(m+b=N-v-1\).
Its kernel consists precisely of the centered stars
\(x_i-(s/N)\mathbf1\) and \(e_\emptyset-\mathbf1/N\). These
\(v+1\) vectors are independent by empty/singleton/pair coordinates.

The successor's original replacement margins were also inspected. Its
\(8mk>v^4\) intermediate bound is correctly replaced at nine by
\(6(8mk-\delta v^2)=v(3654+1269u+158u^2+7u^3)>0\), \(u=v-9\).
Its separate nine-point upper estimate and the \(v\ge10\) inequalities
are valid. The new argument below supplies a single comparison bound for
all \(v\ge9\).

## Exact three-by-three upper certificate

The nonempty layer-constant subspace is invariant, with sole nonzero
\(L\) eigenvalue \((v+10)/3\). Its orthogonal complement has zero sum
on each of the three levels. Nonnegative row/column bounds give
\(\|C\|^2\le2(v-1)\), \(\|H\|^2\le3(v-1)\), \(\|R\|^2\le6\).
By (4), \(Z\preceq vI\) on zero-sum points. Using (6), the diagonal
upper bounds for \(L\) on this complement are

\[
 (18v/5-1/3)I,\quad(2v+2/63)I,\quad(2v+7)I.
\]

The cross blocks there are \(-wP-dC\), \(-hB-tH\),
and \(dR-dP^TB\). Since
\(\sqrt2<99/70\), \(\sqrt3<97/56\), \(\sqrt6<5/2\),

\[
 \|L_{12}\|<\frac{866}{175}\sqrt v,\qquad
 \|L_{13}\|<\frac{110}{21}\sqrt v,
\]
\[
 \|L_{23}\|\le d\bigl(\sqrt6+\sqrt{(v-2)(v-3)}\bigr)
 <dv\le34v/15.                                        \tag{8}
\]

Here \((v-5/2)^2-(v-2)(v-3)=1/4\), with \(v-5/2>0\).
All nonnegative incidence norm bounds retain multiplicity-valued \(H\).
For \(v\ge9\), \(\sqrt v\le v/3\),
\(2v+2/63\le(1136/567)v\), and \(2v+7\le25v/9\).
For the vector of three block norms, the quadratic form of \(L\) is
therefore at most \(v\) times that of the rational matrix

\[
 G=\begin{pmatrix}
 18/5&866/525&110/63\\
 866/525&1136/567&34/15\\
 110/63&34/15&25/9
 \end{pmatrix}.
\]

The three leading principal minors of \((20/3)I-G\) are exactly

\[
 \frac{46}{15},\qquad\frac{86172188}{7441875},\qquad
 \frac{563250652}{281302875}.
\]

All are positive, so Sylvester's criterion gives
\(G\prec(20/3)I\). This proves the strict bound on the zero-sum-level
complement. The layer-constant eigenvalue is also below \(20v/3\), and
the empty extension contributes zero. On \(\mathbf1^\perp\),
\(Q_c\) equals this extended \(L\), proving (1).
This certificate is exact; no numerical eigenvalue or finite interpolation
is used.

## Singular repair, interval and maximality

The trade is credited to six-downset-3, height7745,
`bafkreife2xylkr325rm6jyy2ylfk2a7r5g66dqonqfmeopfg5wj5urwioy`,
[trade proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
and the sufficient earlier six-reviewer-1 audit, height7798,
`bafkreidufjw5hkiess5w7wceffjfeyksg2qybx3ufsugqzxnq5c76th33q`,
[trade review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_sparse_trade_review1/REVIEW.md).
Its empty lift has entries \(mk,-(v-1)k,k\) in empty/empty,
empty/singleton and empty/pair positions; disjoint nonempty sizes
\((1,1),(1,2),(2,2)\) have \(2k,-(v-3),1\). All other entries vanish.
Direct counting gives \(E\mathbf1=Ex_i=0\) and absolute row sums
\(4mk,4(v-1)k,4k,0\) on the four levels, so \(\|E\|\le4mk\).
This proves the upper estimate (3), but lower positivity at a singular
\(Q_c\) requires a separate argument.

Enlarge \(F\) by an independent empty column. The principal block on
empty/pairs/blocks factors \(Q_\theta-J_N\) through that full-column-rank
matrix. Its normalized constant block is the old rank-one PSD block plus

\[
 \theta k(\sqrt m,1,0)^T(\sqrt m,1,0).
\]

The two rank-one directions are independent, so this restriction has rank two.
On zero-sum pairs its eigenvalues are
\(\alpha'_1=\alpha_1-\theta(v-3)\),
\(\alpha'_2=\alpha_2+\theta\). The complete Schur argument above gives

\[
 \mu'=\mu-A(1/\alpha'_1-1/\alpha_1),\qquad
 A=\frac{(v-3)d^2(v-4)^2}{v-2}<\frac{1156}{225}v^2.
\]

The second coefficient stays positive because \(\alpha'_2>\alpha_2\).
For all \(v\ge9\),

\[
 0<\theta\le\widehat\eta<\frac1{2v^2}.
\]

After clearing its positive denominator, the last strict inequality has
numerator \(v^3+3v^2+60v-36\), whose coefficients at \(v=9+u\) are
\((1476,357,30,1)\). Since \(\alpha_1>v\), this gives
\(\alpha'_1>\alpha_1/2\), and

\[
 A(1/\alpha'_1-1/\alpha_1)
 =\frac{A\theta(v-3)}{\alpha_1\alpha'_1}
 <\frac{1156}{225v}<1.
\]

Thus (7) implies \(\mu'>0\) throughout the whole interval (2), including
its closed upper endpoint. The enlarged principal block has rank \(m+b\)
and kills its constant kernel. Consequently \(Q_\theta-J_N\) is PSD,
rank \(m+b\), and kills constants. Addition of \(J_N\) proves rank
\(N-v\) and exactly the \(v\)-dimensional centered-star kernel.

For any intersecting-family indicator \(y\) of size \(q\), support and
row sums give

\[
 (y-(q/N)\mathbf1)^TQ(y-(q/N)\mathbf1)=q(s-q).
\]

PSD forces \(q\le s\); every largest centered star is in every such
H kernel. Empty/singleton coordinates prove their independence, so every
H form has rank at most \(N-v\). A maximum family has size \(s>1\) and
excludes the empty set. In our exact star kernel, equality in
this inequality writes a maximum indicator as a combination of stars.
Its empty coordinate forces the coefficient sum to one; each singleton
coordinate forces a coefficient in \(\{0,1\}\). Precisely one star is
selected. This is the credited star-kernel criterion of six-downset-3,
height7627, `bafkreic72cyah66xcs77hgrzp3qigwyjpk6ldfkrxcy4iqv2wopwnqme54`,
[rank/equality proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).

## Products and field scope

The capped tensor mechanism is credited to six-downset-1, height7578,
`bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`,
[structural proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
Here \(N>7v>2s\). Thus normalized factor spectra lie in
\([-\rho_j,1]\), \(\rho_j=s_j/(N_j-s_j)<1\), with simple upper endpoint.
A product can attain its largest negative endpoint only with one tied
critical negative endpoint and all other factors at one; any further
nonunit or negative factor decreases its absolute value. The endpoint
multiplicity is
\(r=\sum_{j:s_j/N_j=\max_i s_i/N_i}v_j\). The product has maximal
lower rank \(\prod_jN_j-r\) and precisely those \(r\) largest coordinate
stars as maximum families. The same argument applies to the stated mixed
factors when their cap, maximal rank, simple endpoint and strict density
\(0<s_j/N_j<1/2\) hypotheses hold. Centered factors satisfy capped H
but have the extra empty kernel direction, so are outside the maximal-rank
product statement.

For products entirely of twofold factors, the density is strictly decreasing:

\[
 p_v=\frac{6(2v-1)}{5v^2+v+6},\qquad
 p_v-p_{v+1}=\frac{12(5v^2-9)}{(5v^2+v+6)(5v^2+11v+12)}>0.
\]

Thus the critical coordinates are exactly those of minimum order, even
across missing inadmissible orders. This is an elementary explicit consequence
of the existing product mechanism.

The field construction uses \(\rho^2-\rho+1=0\), with blocks
\(\{x,x+d,x+\rho d\}\), \(d\ne0\). For \(q\equiv1\pmod3\),
the roots are distinct and the characteristic is not three. The completing
points of \(\{x,y\}\) are \((1-\rho)x+\rho y\) and
\(\rho x+(1-\rho)y\). The ordered-pair map has determinant
\(1-2\rho\ne0\), equals one in characteristic two, and commutes with
interchange. It therefore bijects unordered completion pairs. Each block
has exactly three ordered representations, giving \(q(q-1)/3\) blocks
and pair multiplicity two. All orders in the target's field scope satisfy
the proof; \(H\) can have entries three at even orders.

For odd \(q\), \(\rho\) has order six. Translation orbits are indexed
by \(d\) modulo \(\langle\rho^2\rangle\). Orbits for \(d,-d\)
are distinct, cover the same three unordered difference classes once each,
and partition by \(\langle\rho\rangle\)-cosets. Choosing one orbit
from each pair gives the stated \(2^{(q-1)/6}\) contained translation
Steiner systems and \(2^{(q-1)/6-1}\) unordered decompositions.
The absence of an even-order STS decomposition follows already from the
nonintegral replication number \((q-1)/2\). Neither decomposition nor
this field specialization is a premise for the general input theorem.

## Independent evidence and trust boundary

The checker imports no author code or author fixture. Its literal bitmask
matrices use a vertex order different from the author's. At9 it constructs
AG(2,3) and the lexicographically first disjoint relabeling fixing zero;
this bounded search is a construction, not a design census. At10 it replaces
one parallel class of that first STS by pairs joined to a new point. At12 it
replaces the eight first-system blocks avoiding zero, using the three
two-factors of \(K_8\) minus the matching induced by blocks through zero,
then adds the three zero/new-point blocks and the new-point triple.
These differ from the author's cyclic even-order fixtures. Every literal
pair multiplicity, block distinctness and downset closure is checked.

| Independent input | \(N\) | Blocks | Distinct completion pairs | Lower centered / repaired ranks |
|---|---:|---:|---:|---:|
|9, two disjoint affine STS|70|24|21 of36|60 /61|
|10, parallel-class replacement|86|30|27 of45|75 /76|
|12, three-point extension|123|44|41 of66|110 /111|
|13, direct field generation|144|52|78 of78|130 /131|

For all four inputs, **24 full exact PSD/rank checks** cover the centered,
originally repaired and new-endpoint lower forms and their strengthened
buffered upper forms. Every buffered upper rank is \(N-1\). No orbit or
representation compression is used. The field16 input is separately
regenerated over \(\mathbb F_2[X]/(X^4+X+1)\); its217-by217 matrices,
incidences, support, row/star equations, empty repair and hashes are checked,
including outside counts \(\{0,3\}\). **Dense PSD elimination at16 is
outside this reproduction**; its mathematical conclusion follows from the
all-order proof. The author's older prime19/31 suite, trace-repair alternative
and affine-compression implementation are also outside this replay.

The rational Schur checker uses positive pivots, rejects negative diagonals,
and requires an exactly zero residual when all remaining diagonals vanish.
Its result is checked against all principal minors of all729 symmetric
three-by-three matrices with entries \(-1,0,1\). Ten invalid matrix/sign
or design inputs are rejected. Two additional mutation controls in
[bridge.py](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_twofold_review5/bridge.py)
show that deleting \(Z\) breaks a star equation at9 and clamping \(H\)
to a Boolean breaks a row equation at16. No assertion guard is needed;
the same checks remain active under Python `-O`.

The complete rational-function checks use coefficient cross-multiplication
over \(\mathbb Q[u]\), \(v=9+u\), without polynomial GCD, interpolation,
CAS or floating arithmetic. They check21 identities and13 nonnegative
coefficient margins, with positive constants for strict margins; the five
sharp weight bounds allow equality at nine. The three exact positive
principal minors above additionally check the universal comparison matrix.
All denominators are explicitly positive on the stated domain.

The optional author-summary bridge matches the four canonical centered and
original-repair field13/16 hashes. Canonicalization orders by size and
bitmask and serializes every rational entry. Author JSON is only comparison
data; it is never an input to the independent theorem checker. The independent
small fixtures have different literal hashes from the author's fixtures.
The field16 hash agreement does not claim a dense PSD replay there.

The exact arithmetic primitives are openly reused from this reviewer's own
[earlier uniform rank-three audit](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/REVIEW.md),
height7960, `bafkreibkblwo7fw23sfbjbxpb5vz7mgbj7x5pzhjgbsgalwig2daeeeb7u`.
That earlier verdict excluded the twofold theorem. Here the incidence proof,
fixtures and matrix construction were independently implemented for this
target; reuse of one's own elementary backend is not separate authorship or
a second independent PSD algorithm.

Trust rests on the complete ordinary proof and inspected CPython integer/
Fraction arithmetic. No solver, proof assistant, numerical eigensolver,
private fixture, large omitted corpus or design classification is required.
Finite validation tests implementation and reduction bridges; it supplies
no extrapolation to the infinite quantifier.

## Literature and publication status

The live primary target is
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The result concerns a structured design class; the general H and I
conjectures remain open. The base rank-three intersecting-family theorem is
prior literature, including
[Czabarka--Hurlbert--Kamat, Theorem1.4](https://arxiv.org/abs/1703.00494);
the spectral matrix, cap and exact kernel supply the additional content here.
The field inputs are classical affine Mendelsohn systems, as in
[Donovan--Griggs--McCourt--Opršal--Stanovský, Proposition2.1](https://arxiv.org/pdf/1411.5194)
and [Nowak's algebraic treatment](https://arxiv.org/pdf/1908.04966).
The review fixtures are validation constructions, without design novelty
claims. Candidate-specific primary-literature searches establish no priority.

The graph novelty of the target is its all-simple-input extension to9,10,12,
including even designs without STS decompositions. The present confirming
audit and sufficient smaller-order interval were not supplied by8010.
The prior sparse trade, tensor mechanism, rank criterion and old9-point
subclass certificates retain their credit. The completion-sensitive formula
also lies outside the earlier uniform seven-weight obstruction in
[TEMPLATE_OBSTRUCTION.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/TEMPLATE_OBSTRUCTION.md),
height7769, `bafkreig3zgdfzdcddiga34hkmpm4ifqwxx4wyhgrudvup4mpwt7xajprhu`.
No contradiction to that template obstruction is implied.

The written result and compact executable evidence are ready for ordinary
mathematical scrutiny. They are not proof-assistant formalization, an accepted
journal theorem or a historical priority determination.

## Strengthening and improvement opportunities

**Proved:** (1)-(3) give a uniform \(20v/3\) core bound and larger closed
sufficient repair interval at all \(v\ge9\). Their main new usefulness
is at9,10,12; use the already stronger8010 bound for \(v\ge13\).
The proof needs one fixed rational three-by-three certificate and has no
separate nine-point norm case. At9 the author's existing displayed row
bounds already imply an even slightly larger centered buffer
\(2111/210>10\), and original-repair buffer \(688/105>13/2\).
The advertised \(\delta\) buffers can thus be sharpened in several ways;
the present bounds are convenient uniform sufficient estimates, not optimal
constants extracted from that proof. The enlarged endpoint in (2) has a
separate complete singular-positivity argument, not just a norm estimate.

**Next substantive extensions:** a sharp universal interval requires lower
Schur and upper-spectrum necessity bounds, rather than these sufficient
estimates. Orders4,6,7 require a replacement formula or a separate analysis;
a bad parameter value, solver failure or exceptional design cannot establish
real H nonexistence. Higher pair multiplicity changes the completion
incidences and their corrections, so it requires a newly derived formula
and complete singular/cap proof. Formalizing (4)-(5) and the rank/equality
argument would directly reduce the remaining written trust boundary.

## Reproduction

From the repository root, CPython3.11+ and standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B spectral_downsets_twofold_review5/audit.py \
  --check spectral_downsets_twofold_review5/expected.json

python3 -B -O spectral_downsets_twofold_review5/bridge.py
```

The complete `--check` may also run under `-O`; every mathematical and
input-rejection guard remains active. Optional hash comparison:

```sh
python3 -B -O spectral_downsets_twofold_review5/bridge.py \
  --author-summary spectral_downsets_steiner_triples/uniform_twofold_expected.json
```

[README](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_twofold_review5/README.md),
[compact output](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_twofold_review5/expected.json),
[provenance](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_twofold_review5/provenance.json)
and [manifest](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_twofold_review5/SHA256SUMS)
record exact commands, measured costs, source hashes and the explicit replay
boundary. The mathematical graph submission records the verified source
commit separately from these reader-facing main-branch links.

The final normal run passed in168.245s/34,276KiB and the complete optimized
replay passed in171.537s/34,816KiB. Both regenerated the identical complete
summary, SHA256 `5689f424d65958644c70cfef3d8f829c9a0a9586005078da1aa1cb8b451e16e8`.
All final full matrix jobs were sequential, with numeric threads one and a
fixed480s subprocess limit. The final default and optional author-hash bridges
passed in14.309s and16.898s. Costs are observations, not guarantees.
