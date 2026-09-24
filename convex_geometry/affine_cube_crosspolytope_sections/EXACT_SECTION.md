# Exact rational affine sections

For (M\geq2), rational (R\geq0), and rational (T), define

\[
A_M(T,R)=\int\delta(\textstyle\sum_i x_i-T)
 \mathbf1_{\{\sum_i(|x_i|-1)_+\leq R\}}\,dx.              \tag{1}
\]

Partition the coordinates into (a) plus tails (x=1+p), (b) minus
tails (x=-1-q), and (m=M-a-b) inactive coordinates (x=w-1\), with
(p,q\geq0) and (0\leq w\leq2).  If
(P=\sum p_i), (Q=\sum q_i), and (W=\sum w_i), the two constraints are

\[
P+Q\leq R,
\qquad P-Q+W=T+m-a+b.                                      \tag{2}
\]

The simplex fiber densities are (P^{a-1}/(a-1)!) and
(Q^{b-1}/(b-1)!).  Inclusion--exclusion for the upper bounds (w_i\leq2)
replaces the right side in (2) by

\[
s_j=T+m-a+b-2j
\]

and gives coefficient ((-1)^j\binom mj).  For (a,b,m\geq1), the
substitution (t=P+Q,v=P-Q), whose inverse Jacobian is (1/2), yields

\[
\frac1{2^{a+b-1}(a-1)!(b-1)!(m-1)!}
\int_{-R}^{\min(R,s_j)}\int_{|v|}^{R}
(t+v)^{a-1}(t-v)^{b-1}(s_j-v)^{m-1}\,dt\,dv.              \tag{3}
\]

The one-tail, no-tail, and no-inactive-coordinate cases follow by deleting
the corresponding simplex fibers.  In particular, the two affine pure-ray
terms, absent from a central section, are

\[
I_{M,0,0}(T,R)=
\mathbf1_{\{0<T-M\leq R\}}\frac{(T-M)^{M-1}}{(M-1)!},
\qquad I_{0,M,0}(T,R)=I_{M,0,0}(-T,R).                     \tag{4}
\]

Finally,

\[
A_M(T,R)=\sum_{a+b+m=M}\frac{M!}{a!b!m!}I_{a,b,m}(T,R).   \tag{5}
\]

Expanding (3) and splitting the (v)-integral at zero leaves only rational
polynomial antiderivatives.  [exact_section.py](exact_section.py) implements
(3)--(5) with arbitrary-size integers and `Fraction`; it performs no root
finding or quadrature.  With (M=n+1,T=\theta M,R=\rho M), its
`normalized_constant` is exactly the quantity in equation (2) of
[PROOF.md](PROOF.md).
