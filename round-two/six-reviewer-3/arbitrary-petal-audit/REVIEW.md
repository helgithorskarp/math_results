# Independent arbitrary-petal H audit, pair-energy margins and closed repair

Actual author: **six-reviewer-3**, role **independent mathematical reviewer**,
2026-10-01. All campaign signatures share one key; independence comes from
target selection, the proof audit and the separate implementation below.

**Verdict: confirmed within the complete stated Boolean-sunflower and
strict-product scope.** The target is six-downset-1's committed lemma8700,
`bafkreidgml7pf6nx54p3kia4nl3fflkuvuwfejo67be3bya3iukdevbeji`,
“Capped universally maximal-rank H for every Boolean sunflower via
opposite-pair attachments,” source commit
**14187fad609a35139b7302d410accbb83c46ee9a**.
Its [proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/ALL_PETALS.md)
and [exact author checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/verify_all_petals.py)
supply a valid unbounded opposite-pair attachment bridge. The parity split
covers every number of petals; the dyadic split covers every petal order.
The kernel repair and repeated-maximum assembly attain universally greatest
lower rank. Common-core ranks and maximum-family cylinder statements have
the required endpoint and equality hypotheses.

This review proves stronger margins using the actual attachment energies,
proves the optimal pairing rule for the aligned bound, and transfers the
already published review8682 closed repair interval after checking its
hypotheses for the newly enlarged class. These are ordinary unformalized
proofs. Finite exact checks corroborate the reductions; sampled matrices
do not prove the infinite quantifiers.

## Scope and credited inputs

Let \(A_1,\ldots,A_r\) be disjoint nonempty finite sets, \(r\ge2\), and
\[
 D_0=\bigcup_j2^{A_j},\qquad u_j=2^{|A_j|-1},\qquad
 t=\max_j u_j,\quad k=|\{j:u_j=t\}|,\qquad
 N=1+\sum_j(2u_j-1).
\]
The largest star has size \(t\). An H matrix is real symmetric, satisfies
\(M\mathbf1=\mathbf1\), vanishes whenever its two set indices intersect,
and has \(L=(N-t)M+tI\succeq0\). The cap is \(I-M\succeq0\).
The empty vertex and its permitted loop remain present; signed entries
are allowed. The target gives a rational capped matrix with
\[
 \operatorname{rank}L=N-kt,\qquad \operatorname{rank}(I-M)=N-1.
\]
The lower rank is maximal among **all real H matrices**, even without a
cap or permutation-invariance restriction. No restriction on \(r,k\), or petal
orders remains.

For a disjoint common set \(C\) of order \(c\ge1\),
\(D=2^C\times D_0\) has order \(N'=2^cN\), star \(S=N'/2\), and both
slack ranks \(N'-2^{c-1}\). Maximum intersecting families are exactly
common-cube maximum cylinders. If \(c=1\), this is the unique common-point
star. One petal uses the full-cube baseline, whose unit endpoint can be
multiple. Redundant or empty petals can be removed before this nontrivial
sunflower description; they are not extra cases for the attachment lemma.

The new target extends lemma8642,
`bafkreiglidblsc6m6khrlu67rdcql6z4t3id4pwfr66tqvbj252uayq77i`,
whose [three-petal proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/MULTI_FACETS.md)
and [263-coefficient certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/MARGIN_COEFFICIENTS.json)
were independently audited in review8682,
`bafkreigttsx2qnsriu3ubzdrjag536y2wfbur77nkjdg22thyixhm5d33m`.
That [prior review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/three-petal-audit/REVIEW.md)
establishes the seed reduction, the full dyadic sign bridge, the seed-nullity
formula and the closed shifted repair estimate. This audit inherits that
already sufficient coefficient-identity audit rather than presenting its
repeated reconstruction as new evidence.

Parent lemma8579,
`bafkreifd6cnenokuntwqvjwv35ucss2k6i4lptc4esenyim62kzfcu7ak4`,
supplies the [two-petal seed](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/UNEQUAL_FACETS.md)
and [equal-star capped gluing](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/PROOF.md).
Independent review8640,
`bafkreibw7e376k3g4bhjl7ocv6d33ldj4ox3j6qql4giubit2adwjan43i`,
confirms those bridges and improves its parent mixing estimate:
[parent review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/two-facet-audit/REVIEW.md).
It does not audit the arbitrary-petal attachment step.

The [core and tensor mechanisms7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
`bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`,
and [full-cube forced-span source8020](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_rigidity/PROOF.md),
`bafkreigxn3orr2vhn77fnx2ky2ypv75uxoaeelrxyhahqennzowxykjihy`,
are credited inputs. The independently sufficient
[Boolean span/equality review8066](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_review3/REVIEW.md),
`bafkreigxr7bf7utsniiqpn3uj73dvxbduzzlmh7k6jrl6gro476tzi2y7m`,
is the trust boundary for their complete full-cube selector span.

The primary conventions and open H/I questions are
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [arXiv record](https://arxiv.org/abs/2609.28404), inspected live October1,
lists v1. Classical complementary selectors and switches are described in
[Loeb--Meyerowitz, Sections1–2](https://oeis.org/A007007/a007007.pdf).
The primary paper's separate classical Chvátal assertion is not independently
reviewed here. Candidate-specific literature searches did not identify an
earlier matching capped arbitrary-petal matrix theorem; this is not a proof
of historical priority. The defensible new increment in the campaign is
the unrestricted attachment bridge, followed here by quantified refinements.

## Complete frame and attachment audit

Assume \(t\ge2\), set \(A=t-1\), and index the nonempty vertices first.
Let \(E=[-\mathbf1^T;I_{N-1}]\). For a PSD core \(C_G\) with diagonal
\(t-1\) and intersecting off-diagonal \(-1\), put
\[
 Q_G=EC_GE^T,\qquad P=I-J/N,\qquad
 M_G=(J+Q_G-tI)/(N-t).
\]
Then support and row sums hold literally,
\(L_G=J+Q_G\succeq0\), and the cap is \(Q_G\preceq NP\).
No empty-row condition is silently omitted.

Full-set vectors \(h_j\) have rational Gram \(G\succeq0\) with diagonal
\(A\). Proper nonempty branch vectors are \(-h_j/A+w\), with residual
Gram \(tZ_{u_j}/A\). For \(u\ge2\), the complementary-pair projectors
give residual eigenvalues
\[
 0\ (1),\quad 2t(u-1)/A\ (u-2),\quad 2t(t-u)/A\ (u-1).
\]
For \(u=1\), the residual space is empty. Residuals sum to zero, are
orthogonal between branches, and are orthogonal to the full-vector span.
The full frame after the empty lift is
\[
 F=\sum_j d_jh_jh_j^T+bb^T,
 \quad d_j=1+(2u_j-2)/A^2,
 \quad b=-\sum_j\alpha_jh_j,
 \quad\alpha_j=(t-2u_j+1)/A.
\]
All residual eigenvalues are at most \(2t\). These sectors exhaust the
core; there is no neglected cross term. With
\(R=\operatorname{diag}(d)+\alpha\alpha^T\succ0\),
the full-frame bound is equivalently
\((N-\beta)R^{-1}-G\succeq0\), including singular \(G\).
This is a complete test within this residual construction, not a necessary
condition for every H matrix.

An attached pair has stars \(v\ge w\ge1\), \(v\le t/2\), and opposite
full vectors in its own orthogonal direction. Its Gram block is
\(A\begin{pmatrix}1&-1\\-1&1\end{pmatrix}\). Define
\[
 m_i=2(v_i+w_i-1),\quad
 \delta_i=2A+2(v_i+w_i-2)/A,\quad
 e_i=4(v_i-w_i)^2/A.
\]
Here \(\delta_i\) is its diagonal-frame eigenvalue and \(e_i\) its
contribution to \(\|b\|^2\). Since \(v_i+w_i\le t\),
\(\delta_i<2t\). Writing \(d=v_i-w_i\),
\(0\le2d\le t-2<A\) gives
\[
 0\le e_i\le2d\le2(v_i+w_i-2)=m_i-2.
\]
These are exact inequalities for the complete stated parameter range.

Let \(p\) be the pair count, \(T=\sum_i m_i\), and
\(E_b=\sum_i e_i\). For an aligned leading frame with diagonal-frame
norm \(\delta_0\ge2t\) and
\(\kappa_0=\delta_0+\|b_0\|^2\le N_0-\beta_0\), the full norm is at most
\(\kappa_0+E_b\). Residuals are at most \(2t\le\kappa_0\).
Thus the target's margin \(\beta_0+2p\) is valid.
For a centered leading frame \(b_0=0\), the leading and tail full frames
stay perpendicular. They have norms at most \(N_0-\beta_0\) and
\(2t+E_b\). This proves the target's
\(\min(T+\beta_0,N_0-2t+2p)>0\). In the applicable leading cases,
\(N_0>2t\); at \(p=0\) this may be a conservative residual estimate.
The enlarged Gram is rational and PSD because all added blocks are PSD.

## Quantifiers, kernel and transports

For a unique largest star, sort \(t=u_1>u_2\ge\cdots\ge u_r\).
Dyadic stars imply \(u_j\le t/2\) for \(j\ge2\).
If \(r\) is even, lead with two petals and pair all the remaining ones.
The aligned two-petal seed has
\[
 \delta_0=2t+2(u_2-1)/A,\qquad
 \beta_0=(2u_2-1)(t-2u_2+1)/A>0.
\]
If \(r\) is odd, lead with three petals. The inherited complete split is:

| Regime | Leading frame | Positive margin input |
| --- | --- | --- |
| \(u_2=u_3=1\) | centered | \(2\) |
| \(t=2u_2,\ u_3=1,\ u_2\ge2\) | centered | \(1/A\) |
| \(t=2u_2,\ u_3\ge2\) | aligned | \(2(u_3-1)(t-2u_3+2)/A\) |
| \(t\ge4u_2\), after the first row | centered | reviewed positive polynomial margin |

The aligned three-petal diagonal norm is
\(3t+(2u_3-3)/A\ge2t\). Centering means \(G\alpha=0\) exactly.
The wide-gap row uses the already independently verified 34,219,10
positive coefficients on \(u_3=1+x,u_2=u_3+y,t=4u_2+z\),
\(x,y,z\ge0\). Its positive constants and complete polynomial identities
give the infinite sign bridge. No attached-pair count enters that input.
The rows, with the indicated precedence, cover every dyadic unique-largest
triple, so every \(r\ge2\) is covered.

The shifted core is the direct sum of cube cores plus \((t-u_j)I\) in
branch \(j\). It is PSD, has norm at most \(2t\), and, when the largest
star is unique, has kernel dimension \(t\). Every H core kills maximum
family indicators: for a size-\(t\) intersecting indicator \(x\),
\(x^TCx=t(t-1)-t(t-1)=0\), hence \(Cx=0\).
The credited full-cube switches span the entire \(t\)-dimensional largest
branch kernel. Consequently every seed kills the shifted kernel. A positive
convex mixture has precisely that kernel, including a mixture coefficient
of one when the shifted matrix itself meets the cap. Injectivity of \(E\)
and the separate constant lower eigenvalue give lower rank \(N-t\).
This also proves the upper bound on lower rank for arbitrary real H matrices.

For \(k\ge2\), place all smaller petals with one largest petal; use full
cubes for the other \(k-1\) packets. Equal-star capped gluing is applicable
to these packets, adds nullities to \(kt\), and yields a simple unit
endpoint even when a full-cube input has repeated unit eigenvalues. If
\(t=1\), all petals are singletons and \((J_{r+1}-I_{r+1})/r\) has
lower rank1 and upper rank \(r\). Division by \(t-1\) is never used there.

Every petal factor has density \(t/N<1/2\), simple unit endpoint, and all
other eigenvalues of modulus less than one. Thus tensoring with the common
\(c\)-cube produces the endpoints \(\pm1\) only from the cube's respective
endpoints and the petal's sole unit vector. Both multiplicities are
\(2^{c-1}\). Its forced cylinder span gives universal maximal lower rank.
The lower kernel makes a maximum-family indicator independent of petals;
testing the empty petal coordinates shows its base is intersecting.

For finite products of strict petal factors, an endpoint-negative
eigenvector can use just one maximal-density factor; two nonunit factors
give smaller modulus. Eligible factor nullities \(\nu_j=k_jt_j\) therefore
add. Universal lower rank is
\[
 N_{\rm prod}-\sum_{j:t_j/N_j=\max_i(t_i/N_i)}\nu_j.
\]
The credited Boolean-additivity argument is applicable: a Boolean-valued
sum of independent factor functions can vary in only one factor. Hence
maximum families are eligible-factor cylinders. Balanced common-cube
factors are aggregated into one free core, rather than included in this
strict-factor additive formula.

## Strengthening and improvement opportunities

**Proved actual-energy margins.** Retain \(E_b\) instead of replacing it
by \(T-2p\). In the aligned case,
\[
 \boxed{\beta_* = \beta_0+T-E_b\ \ge\beta_0+2p.}
\]
For the centered case with \(p>0\), put
\(\delta_{\max}=\max_i\delta_i\). Each attached pair's residual norm is
at most its own \(\delta_i\): its symmetric residual eigenvalue is bounded
by \(t(t-2)/A<2A\), and, for a branch star \(q\ge2\), the other star is
at least one and
\[
 2A+2(q-1)/A-2t(t-q)/A
   =2(t+1)(q-1)/A-2\ \ge4/A>0.
\]
There is no residual for \(q=1\). Thus the entire tail, including its
empty contribution, has norm at most \(\delta_{\max}+E_b\). This proves
\[
 \boxed{\beta_*=
 \min(T+\beta_0,\ N-\delta_{\max}-E_b).}
\]
It is at least the target's old centered margin and remains strictly
positive. With no tail, take \(\beta_* =\beta_0\).
These refinements have no restriction on the number of attached pairs.

For balanced pairs \(v_i=w_i\), \(e_i=0\). An aligned leading frame and
all tails are then block diagonal; every tail norm is below \(2t\le\kappa_0\).
The complete seed norm stays exactly \(\kappa_0\), and
\(\beta_*=N-\kappa_0\) is the **optimal scaled margin for this fixed Gram**.
This does not establish a globally optimal H matrix or optimal leading seed.

**Proved pairing rule for the aligned bound.** For a fixed leading frame
and fixed even multiset of tail stars, adjacent pairing in sorted order
minimizes \(\sum(v_i-w_i)^2\), hence maximizes the displayed aligned
\(\beta_*\). If \(a\ge b\ge c\ge d\), the crossing pairing exceeds
\((a,b),(c,d)\) by \(2(a-d)(b-c)\), and the outer pairing exceeds it by
\(2(a-c)(b-d)\). Re-pair the two largest entries without increasing energy,
then induct. This exchange proof covers every finite multiset. It does not
optimize \(\delta_{\max}+E_b\) in the centered case or the choice of leading
petals. The target's sorted consecutive pairing already obeys this rule.

**Credited closed repair, now applicable to every unique-largest union.**
Review8682 already proved the following shifted estimate. Set
\[
 B=\sum_j[u_j-1+(t-u_j)(2u_j-1)],\quad h=t+1,\quad
 \Lambda=h+B,\quad K=2\sum_j u_j^2(t-u_j),\qquad
 \eta=\min(\Lambda-2t,K/\Lambda)>0.
\]
In the shifted core \(C\), \(z=C^{1/2}\mathbf1\) lies in the sector on
which \(C\preceq hI\); the remaining sector is bounded by \(2t\).
Direct block action gives \(\|z\|^2=B\) and
\(z^TCz=hB-K\). For a perturbed eigenvalue \(\lambda>h\), the resolvent
and the scalar chord bound on \([0,h]\) imply
\[
 1=z^T(\lambda I-C)^{-1}z
 \le B/\lambda+(hB-K)/[\lambda(\lambda-h)],
 \qquad \lambda^2-\Lambda\lambda+K\le0.
\]
The upper root is at most \(\Lambda-K/\Lambda\). Eigenvalues below
\(h\), and the untouched \(2t\) sector, are covered by \(\Lambda-\eta\).
Unique-largest unions have \(K>0\), and
\(B\ge2(t-1)\) gives \(\Lambda-2t>0\). Therefore
\[
 Q_{\rm shift}\preceq(\Lambda-\eta)P.
\]
The arbitrary-petal attachment proof now supplies every strict seed needed
to apply that already credited estimate. For every rational
\[
 \boxed{0<\epsilon\le\epsilon_*=
       \frac{\beta_*}{\beta_*+\max(\Lambda-N,0)},}
\]
the repaired matrix has precisely the forced lower kernel and a simple
unit endpoint. Its scaled upper separation is at least
\[
 \gamma=(1-\epsilon)\beta_*+
             \epsilon(N-\Lambda+\eta)>0.
\]
At \(\Lambda\ge N\), the closed endpoint cancels the two non-strict
terms and leaves \(\epsilon_*\eta>0\); at \(\Lambda<N\), even
\(\epsilon_*=1\) has positive separation. The smallest positive shifted
core eigenvalue is at least \(t-u_2\). Since \(E^TE=I+J\succeq I\) and
both PSD terms share the forced kernel, the positive lower slack is at
least \(\epsilon(t-u_2)\); its separate constant eigenvalue is \(N\).
For the eigenvalues of \(M\), divide these two bounds by \(N-t\).
The closed coefficient exceeds the target's conservative half-margin
coefficient, but their upper-gap guarantees need not be ordered.

**Concrete exact improvement.** Take petal orders \((3,2,2,2,2)\), so
stars are \((4,2,2,2,2)\), \(N=20\), and the aligned leading margin is
\(4/3\). Its balanced tail adds mass6 and energy0. The target gives
\(\beta=10/3\); the fixed-Gram optimal margin is \(\beta_*=22/3\).
Here
\[
 B=31,\quad\Lambda=36,\quad K=64,\quad\eta=16/9,\qquad
 \epsilon_*=11/35\quad\text{versus the author's }5/67.
\]
The new repaired matrix has scaled upper gap at least \(176/315\) and
positive lower gap at least \(22/35\), equivalently M endpoint gaps
\(11/315\) and \(11/280\). All fractions and full PSD/rank conditions are
independently checked in the receipt.

**Further work, not a verdict.** One can solve the exact small-Gram LMI
for better leading choices or centered pairing bounds. A useful next lemma
would give a rational strict seed for facets with different pairwise
intersections, replacing the disjoint residual splitting. The present
construction supplies no such overlap gluing, and proving ordinary maximum
family sizes alone would not supply its spectral cap. General H/I remain open.

## Independent reproduction and trust boundaries

[audit.py](audit.py) imports **no author Python code**. It reuses this
reviewer's already published independent
[8682 projector/Bareiss toolkit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/three-petal-audit/audit.py),
SHA256 `2382479d58813caf97b33f2b6cbc3fc318a4cd10e1c382aa9f6b4436108cd3c1`.
This dependency supplies complementary projectors, integer Bareiss PSD/rank
elimination, literal downset/support checks, prior seed parameters and the
credited gluing/tensor routines. It is an explicit prior independent
dependency, not a second independent audit of that toolkit or of its
263-coefficient interpolation proof.

The new checker independently assembles the parity leads and opposite-pair
blocks, verifies all budgets and stronger margins, and uses general rational
Gaussian inversion for \(R\), rather than the author's Sherman–Morrison
formula. It constructs the original-index cores and the sparse literal
\(ECE^T\) lift, comparing against dense multiplication for orders at most24.
It checks actual symmetry, support, row sums, both complete PSD slacks,
ranks, seed margins and repaired cap gaps. For stronger repairs it separately
checks the full \((\Lambda-\eta)P-Q_{\rm shift}\) PSD bound.
Its claimed positive lower conditioning bound has the written proof above;
the independent code does not repeat the author's additional polynomial
lower-gap checks as a separate test corpus.

All **50 author union matrices** and **seven product/common-core matrices**
match the published matrix hashes and ranks. Every directly recorded
unique-largest seed margin, Gram hash/rank, seed hash/rank and conservative
mixing coefficient also matches. The author receipt is a hash-pinned
comparison input, not a premise for the constructor. The new receipt also
verifies **29 stronger unique-largest repairs** and **five further examples**,
including both parity cases with **22 and23 petals**, and matrix order74.
There are **49 sorted tail multisets and471 perfect-pairing comparisons**,
corroborating the exchange argument. Ten corruptions/domain controls must
be rejected. A fixed literal order80 guard bounds this finite verifier,
without restricting the theorem.

The author checker was separately reproduced in normal and optimized Python,
including all263 prior sign coefficients and12 negative controls. The new
independent checker likewise matches its entire receipt in normal and
optimized Python; explicit exception checks survive `-O`.
[README.md](README.md) supplies exact commands, input hashes and expected
output. [expected.json](expected.json) is the compact independent receipt,
SHA256 `4cd4b65c3d897919b71ed9ddc18c714ea29e642e8a48b1b4c7954606837d1adb`.
[VALIDATION.md](VALIDATION.md) records actual runs and resource scope.

The trust boundary is ordinary unformalized real linear algebra, the
explicitly credited seed/span/gluing/equality proofs, and inspected CPython
integer/Fraction arithmetic. No solver, numerical approximation, private
input, omitted large corpus or proof assistant is used. This package is
reviewable and reproducible within that scope. It proves no general H/I
resolution, historical priority, global Gram optimum or distinct-overlap
facet theorem.
