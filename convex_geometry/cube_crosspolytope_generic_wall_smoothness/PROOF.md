# Generic wall count and exact differentiability

## 1. Setup

Let

\[
g(x)=(|x|-1)_+,
\qquad
A_v(b,R)=\int_{\mathbb R^N}\delta(v\cdot x-b)
\mathbf1_{\{\sum_i g(x_i)\le R\}}\,dx.                 \tag{1}
\]

Fix a nonzero normal and \(|b|>\|v\|_1\).  Put

\[
M=\|v\|_\infty,\qquad
B=\frac{|b|-\|v\|_1}{M}>0,\qquad s=R-B.                \tag{2}
\]

Let \(q\) be the number of nonzero coordinates of \(v\), let \(z=N-q\),
and label the normalized active magnitudes

\[
w_i=|v_i|/M\in(0,1],\qquad 1\le i\le q.                \tag{3}
\]

For \(i\in[q]\) and \(J\subseteq[q]\setminus\{i\}\), define

\[
\omega_{i,J}
=B\left(\frac1{w_i}-1\right)
+\frac2{w_i}\sum_{j\in J}w_j.                         \tag{4}
\]

Call \((B,w_1,\ldots,w_q)\) **wall-nonresonant** when all the numbers in
(4) are pairwise distinct.  This condition implies that the active weights
are pairwise distinct.

## 2. The classification

For a label \((i,J)\), set

\[
\boxed{
\Delta_{i,J}=\frac{2^z}{M}\,
\frac{(-1)^{|J|}w_i^{2q-2}}
{\displaystyle
 (\prod_{k=1}^q w_k)
 (\prod_{\substack{k\notin J\\k\ne i}}(w_i-w_k))
 (\prod_{j\in J}(w_i+w_j))}.}                         \tag{5}
\]

Empty products are one.

**Theorem 1 (generic wall count and smoothness).**  Suppose the normalized
parameters are wall-nonresonant.  Then the ray-side section has exactly
\(q\,2^{q-1}\) chamber walls, namely \(s=\omega_{i,J}\).  If \(q\ge2\),
the section, extended by zero to \(s<0\), is \(C^{q-2}\) but not
\(C^{q-1}\) at every wall, and

\[
\boxed{
\partial_R^{q-1}A_v(b,B+\omega_{i,J}+)
-\partial_R^{q-1}A_v(b,B+\omega_{i,J}-)
=\Delta_{i,J}.}                                       \tag{6}
\]

If \(q=1\), the single wall is \(s=0\) and (6), with derivative order zero,
states that the section value jumps by \(2^z/M\).  Between consecutive walls
the section is a polynomial of degree at most \(N-1\).

Because every denominator in (5) is nonzero under wall nonresonance,
every displayed jump is nonzero.  Thus the count and differentiability claims
are exact, not merely an upper-bound arrangement.

## 3. Isolation of one wall term

We use the global subset formula from the source result.  For a nonempty
labeled weight set \(U\), its fictitious baseline is obtained from

\[
\mathcal R_U(t)=
\frac1{(1-t)^{|U|}\prod_{k\in U}w_k
\prod_{k\in U}(1-w_k+w_kt)}.                           \tag{7}
\]

Fix \((i,J)\) and write \(U=[q]\setminus J\), \(d=|U|=q-|J|\), and
\(\lambda_i=(1-w_i)/w_i\).  Distinctness of the weights makes
\(-\lambda_i\) a simple pole.  Its residue is

\[
\begin{aligned}
a_i^{(J)}
&=\lim_{t\to-\lambda_i}(t+\lambda_i)\mathcal R_U(t)\\
&=\frac{w_i^{2d-2}}
{(\prod_{k\in U}w_k)
 (\prod_{\substack{k\in U\\k\ne i}}(w_i-w_k))}.      \tag{8}
\end{aligned}
\]

Therefore the pole contributes the baseline term

\[
\frac{a_i^{(J)}}{(d-1)!}(s-\lambda_iB)_+^{d-1}.        \tag{9}
\]

The coordinate-specific tail operator acts on a term with no \(B\)-power by

\[
C(s-\lambda B-c)_+^r
\longmapsto
\frac{C\eta_0(w,\lambda)}{r+1}
(s-\lambda B-c-2w(1+\lambda))_+^{r+1},                \tag{10}
\]

where

\[
\eta_0(w_j,\lambda_i)
=\frac1{1+w_j+\lambda_iw_j}-\frac1{w_j(1+\lambda_i)}
=-\frac{w_i^2}{w_j(w_i+w_j)}.                          \tag{11}
\]

Applying the tails indexed by \(J\) to (9) gives exactly

\[
\frac{a_i^{(J)}}{(q-1)!}
\prod_{j\in J}\eta_0(w_j,\lambda_i)
(s-\omega_{i,J})_+^{q-1}.                              \tag{12}
\]

Every other pole/subset pair is labeled by some \((k,L)\ne(i,J)\), hence
has a different hinge under wall nonresonance.  It is consequently an
ordinary polynomial or identically zero in a neighborhood of
\(\omega_{i,J}\).

A zero-normal coordinate applies \(2(1+I)\), where
\((If)(s)=\int_0^sf(u)\,du\).  Thus \(z\) zero coordinates multiply the
lowest hinge term in (12) by \(2^z\) and add only higher powers of the same
hinge.  Finally delta scaling contributes \(M^{-1}\).  The jump in derivative
order \(q-1\) is therefore

\[
\frac{2^z}{M}a_i^{(J)}
\prod_{j\in J}\eta_0(w_j,\lambda_i).                  \tag{13}
\]

Substitution of (8) and (11) into (13) is exactly (5).  This proves the
theorem.

## 4. Why nonresonance is generic

Work in a normalized chart with one labeled weight fixed to one and every
other weight in \((0,1)\).  Equality of two walls is a polynomial equation
after multiplying by their positive denominators.

If their supplier index is the same, the equality is a nontrivial equality
of two distinct subset sums.  If the supplier indices differ, the coefficient
of \(B\) is \(1/w_i-1/w_k\), which is not identically zero.  Hence every
pairwise wall equality defines a proper algebraic hypersurface.  There are
only finitely many pairs, so their complement is open, dense, and of full
Lebesgue measure in the chart.

Equivalently, for weights having distinct relevant subset sums and distinct
coordinates, only finitely many positive values of \(B\) can be resonant.
Thus almost every ray-side offset for almost every normal satisfies Theorem 1.

## 5. Verification boundary

The exact checker evaluates (8) and (11) independently of their simplified
product (5) for all 1,793 labeled walls in eight rational nonresonant families.
It also reconstructs the original three-dimensional body from its 27
halfspaces, interpolates the chamber polynomials on both sides of 33 walls,
checks equality of all lower derivatives, and checks (6).  Dense, signed,
scaled, and sparse normals are included.  These computations corroborate the
algebra; equations (7)--(13) prove the theorem for all real nonresonant data.
