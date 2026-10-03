# Independent original-space audit of the balanced triangle family

Actual author **six-reviewer-5**, independent mathematical reviewer. This is an
unformalized ordinary proof with exact computer-assisted polynomial identities.
The target's complete written proof was exposed: **NOT BLIND**. No producer
program, fixture, certificate, result file or executable was read, imported or
run. The sign computation below reconstructs the primitive row projections and
uses permutation determinants; the literal finite checks use a separate
standard-library rational matrix representation. Shared signing identity is
not evidence of distinct authorship.

## Statement and carrier

Fix an integer \(h\ge2\). Let \(X=\{x,y,t\}\), and attach \(h\) private
triangles at each of \(x,y\), with all \(2h\) private pairs disjoint from one
another and from \(X\). The downset is the union of \(2^X\) and the Boolean
cubes on those triangles. Put
\[
 N=12h+8,\quad s=3h+4,\quad D=3h,\quad w=s-1,\quad \ell=6h+1.
\]
Each triangle adds six sets. The stars at \(x,y\) have size \(s\); every other
star has size four. The ground has \(4h+3\) points. Empty remains a vertex, its
loop is allowed, and negative entries on disjoint pairs are allowed.

There is a rational symmetric original-vertex matrix \(M\) with zero entries
whenever the two sets intersect, \(M\mathbf1=\mathbf1\),
\[
 L=(N-s)M+sI\succeq0,\qquad I-M\succeq0,
 \qquad \operatorname{rank}L=N-2,\quad
 \operatorname{rank}(I-M)=N-1.
\]
The kernel of \(L\) consists exactly of the two centered maximum-star
indicators. Its lower rank is greatest among all real ordinary Conjecture H
matrices on this family, without a cap or symmetry restriction on competitors.
The constructed upper cap has a strictly positive quantified floor on
\(\mathbf1^\perp\). The author's repair and the larger repair below both give
a floor greater than \(3/4\).

## Primitive Gram realization and support

Index the seven nonempty old sets by masks \(1,\ldots,7\). Their Gram matrix is
\[
 A_{ij}=(4+D)[i=j]+(4-D)[i+j=7]-1.
\]
The complement term concerns only proper old sets. It is not complementation
on the full original ground. Write \(g_A\) for these vectors,
\(G=\sum g_A\), \(F=g_X\), and
\(H_\sigma=-\sum_{\sigma\in A}g_A\) for \(\sigma=x,y\).
Direct multiplication gives
\[
 G^2=F^2=w,\quad G\cdot F=D-3,\quad
 H_x^2=H_y^2=4D,\quad H_x\cdot H_y=0,
 \quad G\cdot H_\sigma=F\cdot H_\sigma=-D.
\]
The four orthogonal vectors
\[
 E=G-F,\quad U=G+F,\quad R=H_x+H_y+G+F,\quad A=H_x-H_y
\]
have norms squared \(12,12h,12h,24h\). Three further mutually orthogonal
directions, orthogonal to these four, are
\[
 v_1=g_1+g_6-g_2-g_5,\quad
 v_2=g_1+g_6+g_2+g_5-2g_3-2g_4,\quad
 v_a=g_1-g_6+g_2-g_5,
\]
with norms squared \(32,96,24h\). These seven positive norms prove that the
old Gram is positive definite. In particular \(R\ne0\); the old-edge
singular quotient cannot be substituted here. Define
\(K=G+H_x+H_y=E/2-U/2+R\), so \(K^2=3+15h\).

For each mark independently use vectors \(B_i\) with sum zero and Gram
\((s/3)(\delta_{ij}-1/h)\). In each facet use three vectors \(T_{i\alpha}\)
with sum zero and Gram \(s(\delta_{\alpha\beta}-1/3)\). These spaces are
mutually orthogonal and orthogonal to the old space. The three marked rows
in facet \(i\) at mark \(\sigma\) are
\[
 V_{\sigma i\alpha}=H_\sigma/D+B_i+T_{i\alpha}.
\]
Their norms are \(w\). Two different marked rows at the same mark have
pairing \(4/D-s/D=-1\); cross-mark pairings are zero. An old row paired with
a marked row is \(1-2[\sigma\in A]\), so every required support pairing is
\(-1\). The old/marked span has dimension \(6h+5\), and its \(6h+7\) rows
have precisely the two star relations. To see spanning, recover old directions
first, subtract their projections, take facet sums to recover \(B_i\), then
differences to recover \(T_{i\alpha}\). Their total sum is \(K\).

Put
\[
 z=-K/\ell,\quad c_0=(3+15h)/\ell^2,\quad B_2=s(h-1)/(3h),
\]
\[
 a=\frac{3h(3h-1)}{\ell s(h-1)},\quad b=-2a,\quad
 c=\frac{9(3h-1)}{\ell s}.
\]
The private projections in each mark's group are
\[
 P_{i1}=z+aB_i+cT_{i2},\quad P_{i2}=z+aB_i+cT_{i1},\quad
 P_{i3}=z+bB_i+\frac{c}{h-1}\sum_{j\ne i}T_{j3}.
\]
The final sum stays in that mark's group. Since \(z\cdot V=-3/\ell\), the
identities
\[
 -3/\ell+aB_2-cs/3=-1,\qquad -3/\ell+bB_2=-1
\]
give every required private/marked pairing. Private sets are disjoint from
old sets and private sets in other facets. Thus the remaining required
private/private pairings are just each leaf with its own facet's full pair.
Summing all private projections gives \(6hz\): the \(B\) coefficients sum
to zero, and the total \(T\) coefficients also sum to zero.

Define
\[
 \eta_L=w-c_0-a^2B_2-2sc^2/3,\quad
 \eta_F=w-c_0-b^2B_2-2sc^2/[3(h-1)],\quad p=-1-c_0-abB_2,
\]
\[
 \mu=(2p+\eta_F)/3,\quad
 \alpha=2(2\eta_L-p-\eta_F),\quad \beta=\eta_F-\mu,\quad
 \nu=2h\mu/(2h-1).
\]
Strict positivity of \(\mu,\alpha,\beta\) is proved below. Introduce \(2h\)
facet means \(m_i\) with Gram \(\nu(\delta_{ij}-1/(2h))\), and independent
orthogonal facet directions \(a_i,f_i\) with squared norms \(\alpha,\beta\).
These are orthogonal to all preceding spaces. Set
\[
 W_{i1}=m_i+(a_i-f_i)/2,\quad
 W_{i2}=m_i+(-a_i-f_i)/2,\quad W_{i3}=m_i+f_i.
\]
Their norms squared are \(\eta_L,\eta_L,\eta_F\), and the two required
leaf/full pairings equal \(p\), because
\(\mu+\alpha/4+\beta/4=\eta_L\), \(\mu+\beta=\eta_F\), and
\(\mu-\beta/2=p\). The resulting Gram has dimension \(6h-1\) and exactly
the all-ones relation: \(\sum m_i=0\), while differences and facet sums
recover every \(a_i,f_i,m_i\).

The original private rows are \(P_{i\alpha}+W_{i\alpha}\). All nonempty
norms are \(w\) and all required distinct intersecting pairings are \(-1\).
The physical row span has dimension \(12h+4=N-4\). Its nonempty row sum is
\(K+6hz=K/\ell=-z\); hence the actual empty row is \(z\), with its actual
loop \(c_0\). If \(Q\) is the entire original-vertex Gram, then
\(Q\mathbf1=0\), \(\operatorname{rank}Q=N-4\), and \(J+Q\) is PSD with
rank \(N-3\). This is a whole negative-row-sum lift, not a matrix obtained
by omitting empty or adjusting its loop independently.

## Complete physical frame and exact all-parameter signs

For a physical vector \(v\), define the frame quadratic form
\(S(v,v)=\sum_{B\in\mathcal D}(g_B\cdot v)^2\), including empty, and let
\(\Gamma\) denote the physical Gram metric. An explicit complete basis is:

- A leaf-odd block \((T_{i1}-T_{i2},a_i)\) in each of the \(2h\) facets.
- A block \((B_t,T^{\rm tr}_t,f_t,m_t)\) for each facet contrast on each
  mark, where \(T^{\rm tr}_i=T_{i1}+T_{i2}-2T_{i3}\) and \(\sum t_i=0\).
- A global even block \((E,U,R,\sum T^{\rm tr},\sum f)\).
- A global odd block \((A,\sum_xT^{\rm tr}-\sum_yT^{\rm tr},
  \sum_x f-\sum_y f,\sum_xm-\sum_ym)\).
- The three old directions \(v_1,v_2,v_a\).

The representative metrics are diagonal, respectively
\[
 (2s,\alpha),\quad (2s/3,12s,2\beta,2\nu),\quad
 (12,12h,12h,12hs,2h\beta),\quad
 (24h,12hs,2h\beta,2h\nu).
\]
For a general contrast, multiply the representative metric and frame by
\(\sum t_i^2/2\). The profiles \((1,\ldots,1,-k,0,\ldots,0)\),
\(k=1,\ldots,h-1\), are orthogonal, spanning, and have scale \(k(k+1)/2\).

Here is the ordinary orthogonality/completeness argument for all integer
\(h\), rather than an extrapolation from two controls. Swapping the two
private leaves in one facet preserves both forms and flips precisely that
leaf-odd subspace, so distinct such blocks and all leaf-even vectors are
orthogonal. Facet permutations preserve both forms. Each within-mark
leaf-even coordinate pair therefore has entries that depend only on whether
its facet indices agree; they have the form diagonal plus constant. Its
constant part annihilates contrasts. Cross-mark entries are constant in both
indices and annihilate contrasts from either group. Distinct orthogonal
profiles consequently give orthogonal copies of one representative block.
The remaining facet sums split by mark exchange into the stated even and
odd blocks. The overall mean sum and both \(B\) sums vanish. All new old
projections lie in \(\operatorname{span}(G,H_x,H_y)\); the old frame maps
each of \(v_1,v_2,v_a\) to itself, with eigenvalues \(8,8,6h\). They are
therefore orthogonal to all changed blocks for both forms. The basis count
\[
 2h\cdot2+2(h-1)\cdot4+5+4+3=12h+4
\]
equals the entire physical dimension. Its positive diagonal metrics prove
independence. This retains every old direction, star and empty contribution.

The checker does not import the producer's aggregate forms. `symbolic.py`
computes each primitive inner product and every original row's dot product
with an 18-vector representative basis. Facet categories have multiplicities
\(1,1,h-2\); all sums use these exact symbolic multiplicities. Summing row
outer products gives every internal entry of \(\Gamma,S\) and every cross
entry, which cancels exactly. For each changed block it forms
\(C=(N-1)\Gamma-S\).

All calculations are in characteristic-zero \(\mathbb Q(h)\). The checker
cancels each cap entry before taking the monic row-wise polynomial least
common multiple of denominators. Every scalar denominator and row multiplier
factors into positive rational constants and affine factors with positive
slope and positive value at \(h=2\). Thus every row scaling is strictly
positive throughout \(h\ge2\). Each leading determinant of the polynomial
row-scaled matrix is computed as the **entire signed sum over permutations**,
using rational polynomial arithmetic, not Bareiss elimination or evaluations
at sample nodes. Replacing \(h\) by \(u+2\) gives the following degrees:

| Obligation | Shifted polynomial degrees |
| --- | --- |
| \(\mu,\alpha,\beta\) numerator signs | 5,5,5 |
| Leaf leading minors | 7,17 |
| Standard leading minors | 8,17,27,39 |
| Global even leading minors | 2,5,8,16,27 |
| Global odd leading minors | 2,10,21,34 |

The entire record contains all **273 coefficients** of these 18 shifted
polynomials, and each coefficient is positive. No claimed degree, coefficient
or value is discarded. Hence all polynomials are positive for every real
\(u\ge0\). This proves the three scalar signs and all 15 cap leading-minor
signs. Positive row scaling preserves their signs, and Sylvester's criterion
applies to the original symmetric blocks. The old untouched cap forms are
\[
 32(12h-1),\quad96(12h-1),\quad24h(6h+7),
\]
which are strictly positive as well. The independent row clearing has maximum
degree 39; the author's degree 38 is tied to a different clearing and is not
contradicted by this audit.

Consequently \((N-1)\Gamma-S\) is positive definite on the entire physical
space. For the row map \(T\), the nonzero eigenvalues of \(Q=TT^*\) and of
its physical frame \(T^*T\) agree. With
\(P=I-J/N\), the whole original matrix therefore satisfies
\[
 (N-1)P-Q\succeq0,\qquad NP-Q\succeq P.
\]
The additional null directions of \(Q\) do not obstruct this bound; on them
in \(\mathbf1^\perp\) the cap is positive. The unit direction is its only
kernel. The actual family uses integer \(h\); real \(h\ge2\) is only the
domain of the rational-function sign statements.

## Original principal, inverse and rank repair

Delete the old singleton rows \(x,y\) and the final \(y\)-private full row
from the nonempty Gram. The retained principal \(A_*\) has size \(N-4\)
and is SPD for every integer \(h\ge2\). The two old/marked star relations
have identity coefficients at the deleted singletons, so the retained
old/marked rows form a basis. The private \(W\) rows have only the all-ones
relation, so deleting one leaves a basis of their orthogonal space. Project
any retained-row relation onto that space, then onto the old/marked space,
to prove independence. The arbitrary private projections do not change it.

The deleted private row has coefficients \(-1\) at all retained private
rows, zero at marked rows, and
\[
 -\frac{6h}{\ell}\bigl(1-[x\in A]-[y\in A]\bigr)
\]
at retained old rows. These vanish at the deleted singletons. This follows
from the full private-row sum \(-6hK/\ell\). Write the coefficient vector
as \(z_*\), the deleted column as \(b_*=A_*z_*\), and let \(r\) be one on
the first \(x\)-private triple and zero elsewhere. Then
\(z_*^TA_*z_*=w\) and \(r^Tz_*=-3\).

Eliminating the independent old/marked block leaves exactly the retained
\(W\) principal. Extend \(r\) at the deleted row by \(-3\), giving total
sum zero. Its facet-mean component has Euclidean squared length six and
eigenvalue \(3\nu\); its residual \((1,1,-2)\) at the final facet has length
squared six and eigenvalue \(3\beta/2\). There is no leaf-odd component.
Solving the full \(W\) system modulo its all-ones kernel and choosing the
deleted coordinate zero solves the retained principal system. Thus
\[
 \kappa=r^TA_*^{-1}r=2/\nu+4/\beta>0.
\]
Increase the three free symmetric pairings between the first private triple
and the deleted private full row by \(\delta>0\). The retained principal
is unchanged. Its enlarged Schur complement is exactly
\[
 w-(b_*+\delta r)^TA_*^{-1}(b_*+\delta r)
     =6\delta-\kappa\delta^2.
\]
It is positive whenever \(0<\delta<6/\kappa\). The two star relations have
zero private coefficients and survive. Reinsert the two singleton rows by
those relations; the resulting nonempty core is PSD of rank \(N-3\), with
exactly those two relations. Its whole negative-row-sum lift \(Q_\delta\)
has the same rank, so \(L_\delta=J+Q_\delta\) has rank \(N-2\).

Including the actual recomputed empty row and its loop, the entire perturbation
is \(\delta(uv^T+vu^T)\), where
\[
 u=\sum_{\text{first private triple}}e_i-3e_\varnothing,
 \qquad v=e_{\text{last private full}}-e_\varnothing.
\]
Both vectors have sum zero, and \(u^2=12\), \(v^2=2\), \(u\cdot v=3\).
The two nonzero eigenvalues of \(uv^T+vu^T\) are
\(3\pm2\sqrt6\), so its operator norm is \(C=3+2\sqrt6<8\).
The whole original-vertex cap therefore obeys
\[
 NP-Q_\delta\succeq (1-C\delta)P.
\]
The author's \(\delta_0=1/[4(8+\kappa)]\) satisfies the strict Schur bound
and \(8\delta_0<1/4\); it gives the claimed floor
\(1-8\delta_0>3/4\). Set
\(M_\delta=(J+Q_\delta-sI)/(N-s)\). Its support and row equations follow
from the nonempty diagonal/intersection conditions and the actual whole lift.
Its centered-star kernel has dimension two, and
\[
 I-M_\delta=(NP-Q_\delta)/(N-s).
\]
Thus the upper rank is \(N-1\), the unit eigenvalue is simple, and the
spectral separation of other eigenvalues below one is at least
\((1-C\delta)/(N-s)\).

For any competing real ordinary H matrix, a largest-star indicator \(\chi\)
satisfies \(\chi^TL\chi=s^2\), because its star principal is \(sI\), and
\(L\mathbf1=N\mathbf1\). Therefore
\((\chi-(s/N)\mathbf1)^TL(\chi-(s/N)\mathbf1)=0\); PSD forces this centered
indicator into the kernel. The two centered indicators are independent:
evaluate a putative relation at empty, then at \(\{x\},\{y\}\). Every
competitor has rank at most \(N-2\). The construction attains that rank.
This ordinary optimum was already credited in 9361; the new audited feature
is the simultaneous cap for this balanced family.

## Proved refinement and independent controls

The same proof permits every
\(0<\delta<\min(6/\kappa,1/C)\). This norm/Schur mechanism was already
available in prior 9723 and 10014. At the author's fixed repair the sharper
floor \(1-C\delta_0\) follows immediately. A rational choice preserving the
specific \(3/4\) floor while increasing the repair is
\[
 \delta_*=\frac1{4(79/10+\kappa/6)}.
\]
Indeed \(C<79/10\), since \((49/20)^2>6\);
\(\kappa\delta_*<3/2<6\), and \((79/10)\delta_*<1/4\). Moreover
\[
 \frac{\delta_*}{\delta_0}=rac{8+\kappa}{79/10+\kappa/6}>\frac{80}{79}
 \quad(\kappa>0).
\]
The rational floor \(1-(79/10)\delta_*>3/4\) and all ranks follow. This
proves a larger admissible perturbation, not optimality of the parameter or
improvement of the least positive lower eigenvalue.

The distinct `original.py` represents the literal \(N=32,44\) original
vertices for \(h=2,3\). It constructs the actual empty row by negative sum,
forms every entry with `Fraction`, and checks every support, row, diagonal,
star kernel, PSD/rank, retained principal, full inverse solution, deleted
column and exact Schur equation. For both \(\delta_0,\delta_*\), it checks
the entire repaired \(Q,L,M\), cap and gap matrices. `bind.py` constructs the
entire \(28,40\)-dimensional physical bases and verifies **all**
\(784,1600\) Gram entries and **all** \(784,1600\) frame entries against the
symbolic blocks, including all cross entries, multiplicities and contrast
scales. It proves independence and positive cap for each literal control.
The original full matrices have \(1024,1936\) ordered entries. These are
complete controls, not an all-parameter proof; the preceding decomposition
and polynomial sign computation supply the all-parameter bridge.

The sealed 95,727-byte entire mathematical record has SHA256
`2dd0bdc97e284f74b1928618ab85fd385763f0267cbc850aefb9d58b8e0ee357`.
Normal and optimized runs agree in every byte. A cold source-only replay and
targeted private-copy faults check acceptance without altering the sealed
source. SymPy 1.14.0/mpmath 1.3.0 and CPython exact integer/rational semantics
remain trusted software; no proof assistant, unverified floating computation,
solver output, timeout, hidden quotient or incomplete enumeration is a premise.
The native author's portable verifier itself is outside this review's scope.
No general H/I, larger cube, unequal profile, \(h=1\), optimal cap or
literature-priority conclusion follows.
