# Global chamber classification for arbitrary normals

## 1. Affine section and normalization

Let

\[
g(x)=(|x|-1)_+,
\qquad
A_v(b,R)=\int_{\mathbb R^N}\delta(v\cdot x-b)
 \mathbf1_{\{\sum_i g(x_i)\leq R\}}\,dx.                 \tag{1}
\]

Fix \(|b|>\|v\|_1\).  Put

\[
M=\|v\|_\infty,
\qquad B=\frac{|b|-\|v\|_1}{M},
\qquad s=R-B.                                             \tag{2}
\]

The section is empty for \(s<0\).  Coordinate and central reflections reduce
to positive offset and nonnegative normal.  Let \(q\) coordinates be nonzero,
put \(z=N-q\), and normalize the active weights as

\[
w_i=|v_i|/M\in(0,1],\qquad 1\leq i\leq q.               \tag{3}
\]

Scaling the delta distribution contributes the final factor \(M^{-1}\).
After this normalization, anchor every active coordinate at its positive cube
vertex and write

\[
\beta_i=w_i(x_i-1),\qquad h_i=g(x_i)-\beta_i.
\]

Then the section equation and radius inequality are respectively
\(\sum_i\beta_i=B\) and \(\sum_i h_i\leq s\).  This is the
coordinate-measure representation used below.

## 2. The fictitious global baseline

For a nonempty labeled weight set \(W=(w_1,\ldots,w_d)\), allow each
coordinate to be either

\[
x=1+p\quad(p\geq0),
\qquad\text{or}\qquad
x=1-y\quad(y\geq0),                                      \tag{4}
\]

where the second state is temporarily unbounded.  Let \(F_W(B,s)\) be the
corresponding delta-normalized section with slack at most \(s\).

For every distinct weight \(u\in W\), define

\[
\lambda_u=\frac{1-u}{u},
\qquad m_u=|\{i:w_i=u\}|.                                \tag{5}
\]

Introduce the rational function

\[
\mathcal R_W(t)=
\frac{1}{(1-t)^d\prod_{i=1}^d w_i
 \prod_{i=1}^d(1-w_i+w_it)}.                             \tag{6}
\]

Let \(A_{u,\ell}\) be the principal-part coefficients at
\(t=-\lambda_u\):

\[
\mathcal R_W(t)=
\sum_{\ell=1}^{m_u}\frac{A_{u,\ell}}
{(t+\lambda_u)^\ell}+O(1)
\quad(t\to-\lambda_u).                                  \tag{7}
\]

Equivalently,

\[
A_{u,\ell}=\frac{1}{(m_u-\ell)!}
\left[\frac{d^{m_u-\ell}}{dt^{m_u-\ell}}
 (t+\lambda_u)^{m_u}\mathcal R_W(t)\right]_{t=-\lambda_u}. \tag{8}
\]

**Lemma 1 (baseline spline).**  For \(B>0\),

\[
\boxed{
F_W(B,s)=\sum_{u\in W}^{\rm distinct}\sum_{\ell=1}^{m_u}
A_{u,\ell}
\frac{B^{\ell-1}}{(\ell-1)!}
\frac{(s-\lambda_uB)_+^{d-\ell}}{(d-\ell)!}.}           \tag{9}
\]

Here \(x_+^0\) is one for \(x\geq0\) and zero otherwise, so all closed
chamber endpoints are included.

To prove the lemma, take the bilateral Laplace transform in \(B\) and the
ordinary Laplace transform in the cumulative slack.  One coordinate in (4)
contributes

\[
\frac1{w_i(\alpha+\lambda_i\beta)}
+\frac1{w_i(\beta-\alpha)}
=\frac{\beta}{w_i^2(\beta-\alpha)
 (\alpha+\lambda_i\beta)}.                              \tag{10}
\]

The cumulative inequality contributes \(1/\beta\).  Thus

\[
\widehat F_W(\alpha,\beta)
=\beta^{-d-1}\mathcal R_W(\alpha/\beta).                \tag{11}
\]

The poles \(t=-\lambda_u\) invert on the half-plane \(B>0\) to the terms
in (9).  The pole at \(t=1\) is supported on \(B<0\) and does not contribute.

## 3. Coordinate-specific physical-tail replacement

The fictitious inactive ray agrees with the physical interval until \(y=2\).
For a coordinate of weight \(w\), align the physical negative tail and the
fictitious tail by their common excess slack \(r\geq0\).  Their signed
difference defines

\[
\boxed{
(\mathcal T_wf)(B,s)=\mathbf1_{\{s\geq2w\}}
\int_0^{s-2w}\left[
\frac1{1+w}f\!\left(B+2w+\frac{w}{1+w}r,s-2w-r\right)
-\frac1w f(B+2w+r,s-2w-r)
\right]dr.}                                             \tag{12}
\]

The first term is the physical state \(x=-1-e\), with
\(r=(1+w)e\); the second subtracts the fictitious state
\(y=2+r/w\).  This is an identity of coordinate measures.

For computation, (12) has a closed coefficient action.  Put

\[
\eta_i(w,\lambda)=
\frac{w^i}{(1+w+\lambda w)^{i+1}}
-\frac{1}{w(1+\lambda)^{i+1}}.                           \tag{13}
\]

Then

\[
\boxed{
\begin{aligned}
&(B+a)^p(s-\lambda B-c)_+^r\\
&\quad\stackrel{\mathcal T_w}{\longmapsto}
\sum_{i=0}^p {p\choose i}\eta_i(w,\lambda)
\frac{i!r!}{(i+r+1)!}(B+a+2w)^{p-i}\\
&\hspace{42mm}\cdot
(s-\lambda B-c-2w(1+\lambda))_+^{r+i+1}.
\end{aligned}}                                          \tag{14}
\]

This follows by expanding the first factor and applying the beta integral.
For \(w=1\) and \(\lambda=0\), (13) is
\(2^{-i-1}-1\), exactly the earlier diagonal recurrence.

## 4. Exact global theorem

For a subset \(J\subseteq[q]\), write \(W_{J^c}\) for the labeled weights
not in \(J\), and put
\(\mathcal T_J=\prod_{j\in J}\mathcal T_{w_j}\).  The operators commute,
as they are convolutions of coordinate measures.

Let \(I\) denote integration in slack,

\[
(If)(B,s)=\int_0^s f(B,u)\,du.                           \tag{15}
\]

**Theorem 2 (all weighted ray chambers).**  For every nonzero normal,
\(|b|>\|v\|_1\), and \(s\geq0\),

\[
\boxed{
A_v(b,B+s)=\frac{2^z}{M}(1+I)^z
\sum_{J\subsetneq[q]}\mathcal T_JF_{W_{J^c}}(B,s).}     \tag{16}
\]

Equations (7)--(9) and (13)--(14) make (16) a finite explicit rational
coefficient formula whenever the weights and offset are rational.  For real
weights they remain exact algebraic-analytic coefficient formulas.

Proof: for each active coordinate write its physical state measure as

\[
(\text{plus}+\text{unbounded inactive})
+(\text{physical negative tail}-\text{fictitious inactive tail}).      \tag{17}
\]

Expanding the product gives (16) before the zero-coordinate factor.  The term
\(J=[q]\) has every active coordinate on a negative/fictitious tail and is
supported on \(B<0\), so it vanishes here.  For a zero-normal coordinate,
pushforward of Lebesgue measure by \(g\) is \(2\delta_0+2du\); convolving all
\(z\) such coordinates applies \(2^z(1+I)^z\).  Finally restore \(M^{-1}\).

## 5. Finite chamber arrangement

Every truncated-power hinge generated by (16) has its wall among

\[
\boxed{
\Omega(v,B)=\left\{
B\left(\frac1{w_i}-1\right)
+\frac{2}{w_i}\sum_{j\in J}w_j:
i\in[q],\ J\subseteq[q]\setminus\{i\}
\right\}.}                                              \tag{18}
\]

Indeed, choose a surviving baseline pole supplied by weight \(w_i\); each
replaced coordinate \(j\) adds \(2w_j(1+\lambda_i)=2w_j/w_i\) to its hinge.
Some displayed walls can coincide or cancel, but there are no others.
Therefore sorting the finite set (18) gives an exact chamber refinement on
which (16) is an ordinary polynomial of degree at most \(N-1\).  Formula
(14) also gives every one-sided derivative and hence decides which candidate
walls are genuine.

## 6. Recovery of the diagonal theorem

If all \(q=N\) weights equal one, a complement of size \(d\) has

\[
\mathcal R_W(t)=\frac1{t^d(1-t)^d}.                      \tag{19}
\]

Its principal part at zero is precisely the Legendre kernel \(H_d(B,s)\).
All subsets of a fixed size have the same replacement operator, so (16)
collapses to

\[
A_N=\sum_{r=0}^{N-1}{N\choose r}\mathcal T^rH_{N-r}.    \tag{20}
\]

The walls (18) reduce to \(0,2,\ldots,2(N-1)\), recovering the complete
diagonal chamber and smoothness classification.

## 7. Verification boundary

The checker constructs every principal part over `Fraction`, applies (14),
and aggregates the subset expansion.  It compares the result with exact
rational polygons obtained directly from all 27 halfspaces of the original
three-dimensional body, across signed, repeated, distinct, scaled, and sparse
normals and radii far beyond the first chamber.  Independent routines verify
the rational partial-fraction identity, the earlier first chamber, and the
equal-weight global recurrence.  These computations corroborate (16); the
measure decomposition and Laplace inversion prove it in all dimensions.
