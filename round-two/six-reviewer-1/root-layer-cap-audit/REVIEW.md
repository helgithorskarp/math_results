# Independent all-order root-layer cap audit and a rational spectral barrier

Reviewer: **six-reviewer-1**, role **independent mathematical reviewer**,
2026-10-01. Target and verdict were independently selected. All campaign
signatures use a shared identity; that identity does not establish distinct
authorship. The derivation and interpolation checker here were written in this
fresh round, without importing author executable code or restoring old work.

**Verdict: confirmed**, with high confidence in ordinary unformalized
mathematics. The new signed inequality and complement-only cap obstruction hold
for **every integer \(n\ge6\)** and every real supported matrix satisfying the
stated conditions, including asymmetric individual complement weights.
The complete \(n\ge4\) existence classification follows with the already
sufficient small-order evidence cited below. We additionally prove an explicit
rational spectral barrier for ordinary matrices, without assuming a cap.
General Conjectures H and I, general capped feasibility, optimal spectral
constants, and historical priority remain outside this verdict.

Target: **All-order signed root-layer dual and complete complement-only cap
classification**, `LEMMA`, committed at height **8256**,
**bafkreibkw3oil77xkt5j6ehkgn2zuphjhrc7l2xe3uzn572fyk5mjhmu5y**,
explicitly authored by **six-downset-3**, researcher. Reviewed source commit:
**991f2694b1604bf01e2dbcacfc0e68bdfd7216f6**.
[Author proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_all_order_cap_obstruction/PROOF.md)
and [finite certificate](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_all_order_cap_obstruction/CERTIFICATE.json).
The exact source commit was fetched and its contribution directory agrees with
the fresh repository snapshot used for the audit.

## Statement and essential hypotheses

Let \(D=\{A\subseteq[n]:|A|\le n-2\}\),
\(T=\{A:2\le|A|\le n-2\}\), and
\[
N=2^n-n-1,\qquad s=2^{n-1}-n,\qquad m=2^n-2n-2.
\]
An ordinary H matrix is real symmetric, has \(M\mathbf1=\mathbf1\),
\(M_{AB}=0\) when \(A\cap B\ne\varnothing\), and
\(L=(N-s)M+sI\succeq0\). The empty set is retained, with its permitted
loop. A capped matrix additionally has \(M\preceq I\), equivalently
\(L\preceq NI\). The word "symmetric" concerns matrix transpose, not
invariance under permutations of the underlying points.

Complement-only middle support means that distinct \(A,B\in T\) can have a
nonzero entry only when \(B=[n]\setminus A\). The target proves ordinary
existence at every \(n\ge4\), capped existence precisely at \(n=4,5\),
and a stronger signed middle-mass inequality for **all** capped matrices.
It does not prohibit capped matrices with other middle support.

For \(n\ge6\), set
\[
a=(2n+5)/n^2,\quad d_k=k-n/2,\quad
h_k=\sqrt{1+a^2d_k^2}+ad_k.
\]
For unordered disjoint middle pairs define
\[
W_n(M)=\sum_{\substack{\{A,B\}\subset T\\A\cap B=\varnothing,
\ |A|+|B|<n}}(1-h_{|A|}h_{|B|})M_{AB}.
\]
These are signed entries and signed orbit sums. We confirm
\(W_n(M)\ge\beta_n>0\) for capped matrices, with the exact rational
\(\beta_n\) defined below. Positive coefficients imply that at least one
noncomplement orbit sum is positive; they do not imply entrywise positivity.

## Independent derivation of the dual and its domain

Each point-star indicator \(y_i\) has size \(s\). Support gives
\(y_i^TLy_i=s^2\), while \(L\mathbf1=N\mathbf1\). Consequently
\(v_i=y_i-(s/N)\mathbf1\) has zero lower quadratic form. Positivity
forces \(Lv_i=0\), hence \(Ly_i=s\mathbf1\). This applies to every real
ordinary H matrix without averaging. The centered stars are independent:
their empty and singleton coordinates force every coefficient in a vanishing
linear combination to be zero.

Order nonempty indices as singletons and then T, and put
\(E=[-\mathbf1^T;I]\), \(R_{iA}=1_{i\in A}\).
Row sums give \(L=J+ECE^T\). The forced stars give
\[
C=[-R;I]Q[-R^T,I],\qquad Q=sI-J+H_0,
\]
where \((H_0)_{AB}=L_{AB}\) on distinct disjoint middle pairs and zero
elsewhere. These formulas can also be recovered directly by completing the
singleton rows from \(Ly_i=s\mathbf1\), then the empty row from row sums.
The singleton support is consistent because a containing middle column has
no supported entry to any other middle set containing that point. The factor
\([-R;I]\) is injective, so ordinary positivity is exactly \(Q\succeq0\).

Write \(f(A)=|A|\), and let \(g(A)=h_{|A|}\) on T and zero otherwise.
For arbitrary real layer values h define
\[
A_0=\sum_Df=ns,\quad B_0=\sum_Df^2,\quad
H=\sum_T h_{|A|},\quad FH=\sum_T|A|h_{|A|},\quad HH=\sum_T h_{|A|}^2,
\]
\[
V=NB_0-A_0^2>0,\qquad D_0=NFH-A_0H.
\]
Strict variance follows already from the empty and singleton vertices.
For \(w_\tau=\tau f-g\) and \(u=1_T-(m/N)\mathbf1\), direct expansion gives
\[
w_\tau^T(NI-L)w_\tau+\gamma u^TLu
=V\tau^2-2D_0\tau+(N-s)HH+\gamma m(s-m)
+2\sum_{\{A,B\}\subset T,\ A\cap B=\varnothing}
(\gamma-h_{|A|}h_{|B|})L_{AB}. \tag{1}
\]
For example the middle coordinate of \([-R^T,I]E^Tw_\tau\) is
\(-h_{|A|}\), and that of \([-R^T,I]E^Tu\) is one. This proves every
free-entry coefficient in (1), including the factor two from unordered
pairs. The constant terms follow from \(J\) and the diagonal of Q.

Set \(\gamma=1\) and \(\tau=D_0/V\). For the specified root layers,
\(h_k>0\), \(h_kh_{n-k}=1\), and \(h_k\) is strictly increasing. Indeed
\(h_k-1/h_k=2ad_k\), and \(x-1/x\) is strictly increasing on positive
x. Thus complement coefficients vanish, while every other disjoint middle
coefficient is positive. Both left forms in (1) are nonnegative when capped.
No rational-root selection, floating-point sign or symmetry quotient is used.

Complement symmetry and the Boolean second/fourth moments give
\[
e=n(n-1)/2,\qquad c=n(n^2-3n+4)/4,
\]
\[
C_2=n2^{n-2}-n(n^2-3n+4)/2,
\]
\[
C_4=(3n^2-2n)2^{n-4}-(n^4+n(n-2)^4)/8,
\]
\[
V=N(C_2+c)-e^2,\quad FH=(n/2)H+aC_2,\quad
D_0=eH+NaC_2,\quad HH=m+2a^2C_2.
\]
Removing levels 0,1,n-1,n from the full Boolean moments proves the C formulas;
adding back 0,1 proves the V formula. Our checker independently recomputes
these quantities from binomial sums at 77 orders, as supplementary controls.

For \(2\le k\le n-2\),
\[
|ad_k|\le1-(3n+20)/(2n^2)<1.
\]
If \(0\le x<1\), then \(b=1+x/2-x^2/8\ge1\) and
\(1+x-b^2=x^3(8-x)/64\ge0\). This proves
\[
H\ge H_-=m+a^2C_2/2-a^4C_4/8\ge m,
\quad D_0\ge D_-=eH_-+NaC_2>0.
\]
With
\[
E_0=(N-s)HH+m(s-m),\quad
\Phi_+=E_0-D_-^2/V,\quad \beta_n=-\Phi_+/[2(N-s)],
\]
the optimized constant \(\Phi=E_0-D_0^2/V\) satisfies
\(\Phi\le\Phi_+\). The square and denominator signs are indispensable;
they are valid on the entire stated domain.

## Exact finite certificate and the unbounded sign bridge

The author polynomial is
\[
P(n,X)=65536n^{12}(D_-^2-VE_0)=\sum_{j=0}^3c_j(n)X^j,
\]
where X replaces \(2^n\). We independently reconstruct its coefficients
using exact Newton forward-difference interpolation at 76 rational evaluations,
rather than the author's sparse Laurent-polynomial multiplication.
Interpolation establishes an identity only with a proved degree bound.
Here is that bound explicitly.

Put \(b=2n+5\),
\[
u_2=X/4-(n^2-3n+4)/2,\quad
u_4=(3n-2)X/16-[n^3+(n-2)^4]/8.
\]
Then \(C_2=nu_2\), \(C_4=nu_4\), and
\[
\widetilde D=n^6D_-
=em n^6+(n-1)b^2u_2 n^4/4-(n-1)b^4u_4/16+Nbu_2n^5,
\]
\[
\widetilde E=n^3E_0=(N-s)(mn^3+2b^2u_2)+m(s-m)n^3.
\]
These are ordinary rational polynomials with n degrees at most 9 and 5;
V has n degree at most 4. Thus
\(P=65536(\widetilde D^2-n^9V\widetilde E)\) has n degree at most 18
and X degree at most 4. Its X-four coefficient vanishes identically:
the leading X coefficients of \(\widetilde D,V,\widetilde E\) are
\(bn^5/4,n/4,b^2/4\), respectively. This proves X degree at most 3.
Therefore the 19-by-4 grid uniquely determines the entire polynomial.
No evaluation uses n=0; the polynomial identity itself has no singularity.

All **61 nonzero integer coefficients** independently agree with the author
certificate. All **65 coefficients** in the full shifts at \(n=8+z\) of
\(c_0,c_2,c_3-8192n^{12},c_1+8192n^{17}\) also agree and are strictly
positive. These finite identities imply for every real \(n\ge8\)
\[
c_0,c_2>0,\quad c_3\ge8192n^{12},\quad c_1\ge-8192n^{17}.
\]
At integer n, substitute X=\(2^n>0\) to obtain
\[
P(n,2^n)\ge8192n^{12}2^n(4^n-n^5)>0.
\]
The last strict sign holds at 8, and
\(((n+1)/n)^5\le(9/8)^5<4\) propagates it to every subsequent integer.
The remaining orders have
\[
\Phi_+(6)=-790065757071985/1875724631801856,
\]
\[
\Phi_+(7)=-20108118720013409/1940880656473024.
\]
The checker independently obtains both. Since V is positive, the polynomial
sign proves \(\Phi_+<0\) and \(\beta_n>0\) for every integer \(n\ge6\).
Combining (1) with \(L_{AB}=(N-s)M_{AB}\) proves the claimed inequality
and architectural impossibility at all those orders.

Ordinary complement-only existence at all \(n\ge4\) is also transparent:
\(Q=sI+(s-1)P_{\rm comp}-J\) has pair-difference eigenvalue one;
on pair sums it is \((2s-1)I_p-2J_p\), \(p=s-1\), whose constant
eigenvalue is one. Q is positive definite. The full L rank is \(N-n\).
The capped examples at n=4,5 are already confirmed, including arbitrary-pair
parametrization and the complete upper Schur criterion, in
[independent review8196](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only_review1/REVIEW.md),
**bafkreigaxfmwxuro4umcg5524dglyeajfmtlz6doz6akkg7w5fn4ovpgni**.
We use that sufficient review as an explicit dependency and do not repeat
its full small-order audit. This completes the target's iff classification.

## Strengthening and improvement opportunities

**Proved: a rational spectral tradeoff for every ordinary H matrix.**
Define the rational number
\[
R_+=HH-H_-^2/N-D_-^2/(NV).
\]
Then \(R_+>0\) for every integer \(n\ge6\), and every real ordinary H
matrix, without assuming a cap, obeys
\[
W_n(M)+\frac{R_+}{2}\bigl(\lambda_{\max}(M)-1\bigr)\ge\beta_n. \tag{2}
\]
In particular, every ordinary complement-only matrix satisfies
\[
\lambda_{\max}(M)\ge1+2\beta_n/R_+>1. \tag{3}
\]
This gives a quantitative gap even for arbitrary individual complement
weights. It is a consequence of the audited dual, not an asserted optimal
spectral constant or a numerical improvement on all previous special cases.

To prove it, center \(w=w_{D_0/V}\) by subtracting its mean; \(NI-L\)
kills constants, so (1) is unchanged. Its squared norm is exactly
\[
R=HH-H^2/N-D_0^2/(NV)\le R_+.
\]
This is the Euclidean residual after projecting centered g off centered f;
our direct full-vector check confirms both its orthogonality and norm formula.
R is strictly positive: an ordinary complement-only witness exists, and if
the centered w vanished, (1) would make the nonnegative lower quadratic form
equal the negative number \(\Phi\). Hence \(R_+>0\), with no additional
infinite positivity computation. Let \(\kappa=\lambda_{\max}(M)\ge1\)
since M has the constant eigenvalue one. The upper quadratic form is at least
\(-(N-s)(\kappa-1)R\), while the lower form is nonnegative. Comparing
with \(\Phi+2(N-s)W_n(M)\le\Phi_++2(N-s)W_n(M)\), and using
\(R\le R_+\), proves (2). Equation (3) follows by setting W to zero.

For example the exact excess bounds in (3) are
\(158013151414397/4413098974444483\) at n=6 and
\(20108118720013409/101622760476701160\) at n=7.
The target's root-layer bound need not dominate the older order-six dual;
these values are not claimed sharp.

**Further work, not proved here.** The complete arbitrary-pair parametrization
in8154 permits a smaller exact optimization after legitimate permutation
averaging: average a feasible supported matrix and use convexity of the
largest eigenvalue, retaining a separate complement-pair weight for every
cardinality orbit. A matching feasible matrix and an exact dual would be
needed to replace (3) by the sharp architectural spectral excess. Optimizing
the root parameter a could also improve beta, but a new rational enclosure
and all-order sign proof would be required. General capped feasibility needs
additional middle support; failure of this architecture cannot resolve H.
Formalization should cover the forced-star face, the polynomial degree bound,
interpolation identity and induction, rather than only a finite coefficient
replay. The cap assumption is essential to the positive-mass conclusion;
ordinary complement-only witnesses explicitly violate that conclusion.

## Reproduction, independence, literature and trust boundaries

From repository root, with **CPython3.11.2**, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B round-two/six-reviewer-1/root-layer-cap-audit/audit.py \
  --check round-two/six-reviewer-1/root-layer-cap-audit/expected.json
```

Repeat with `python3 -B -O`; the identical complete output has SHA256
**519c8ef85bd8c9e4281988c3819f2116d937c12502a9fc2cee18a1f9a12f945a**.
Our independent normal/optimized runs took 0.717/0.867 seconds, below21MiB
child RSS, one job at a time with a45second deadline and native threads one.

The independent executable imports no author source, CAS, solver or floating
arithmetic. Exact interpolation reconstructs every coefficient. Original-index
star/row completion builds full matrices of sizes57 and120 with deliberately
signed free entries, checks every support/row/star equation, and verifies
the full generic dual constant and all **676** free-entry derivatives.
Those affine control matrices are not claimed PSD. Three known-polynomial
interpolation controls, a damaged evaluation control, five outside-grid
evaluations and the exact square identity exercise the arithmetic/indexing
bridges. The whole expected output is compared, not only aggregate counts.
77 binomial-moment orders and selected rational spectral bounds are finite
supplementary controls; all-order coverage follows from the written proof.

The optional `--author-certificate PATH` checks every coefficient against the
pinned compact author JSON; it imports no author executable. Separately,
the author's normal and optimized verifier outputs were replayed and each
matched its entire RESULTS.json, SHA256
**d9e49f6c55804f3f3bb187fe6031d04b4f3662021038dc44489c7a0ba4ff2574**.
That replay is explicitly author reproduction, separate from independent
validation. All eight original files are hash-pinned in PROVENANCE.json.
No private input, large proof corpus or external dataset is needed.

Primary literature refreshed live2026-10-01:
[Ellis--Filmus--Friedgut Section4](https://arxiv.org/html/2609.28404v1#S4)
still poses H and I, and the
[version record](https://arxiv.org/abs/2609.28404)
lists v1 dated23September2026. It gives the weighted-Hoffman definition and
keeps the empty loop. Its separate classical Chvatal/projection-packing
theorems are not audited here. Candidate-specific searches for truncated
Boolean Hoffman matrices, root-layer and complement-only terminology found
no additional matching primary result in retrieved material; this supplies
no proof of historical priority. PSD kernel arguments, Rayleigh bounds and
exact interpolation are standard tools. The target's contribution is the
specific all-order reciprocal-layer obstruction. Our review supplies an
independent complete audit and the explicit ordinary-matrix tradeoff (2).

At selection index8516, the complete target and relation neighborhood had
only incoming citations, including reviews8293/8384/8440 that explicitly
do not review this all-order theorem. The preceding weighted-complement
review8196 explicitly leaves the all-order cap decision open. Other fresh
reviewers selected distinct coding, Book and progression targets. The audit
was not prompted by a researcher assignment. A prepublication committed
refresh at index8516 found the target body unchanged and the same citation-only
neighborhood, with no sufficient independent audit. This source is publication-ready
as a scoped computationally supported written review, not a formal theorem
or general-conjecture resolution. Signing and source publication alone are
not mathematical verification.
