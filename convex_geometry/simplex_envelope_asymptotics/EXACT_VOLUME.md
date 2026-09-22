# An exact finite formula for the section

For integer N≥2 and real R≥0, define

$$
A_N(R)=\frac1{\sqrt N}
\left|\left\{x:\sum x_i=0,\ \sum(|x_i|-1)_+\leq R\right\}\right|_{N-1}.
$$

The following formula uses only integrals of polynomials with explicit
limits; for rational R every term is rational. In particular it computes
every sharp constant \(C_{N-1}=(N-1)!A_N(N)/N^{N-1}\).
It is not an asymptotic approximation.

Partition coordinates into a positive active coordinates \(x=1+z\),
b negative active coordinates \(x=-1-z\), and m inactive coordinates
\(x\in[-1,1]\), where a+b+m=N. Boundary overlaps have zero section
volume. Let \(I_{a,b,m}(R)\) be the delta-normalized section volume for
one fixed such assignment. Then

$$
A_N(R)=\sum_{a+b+m=N}\frac{N!}{a!b!m!}I_{a,b,m}(R).          \tag{1}
$$

Here are all the cases.

1. When a=b=0,

$$
I_{0,0,N}(R)=\frac1{(N-1)!}
\sum_{j=0}^N(-1)^j\binom Nj(N-2j)_+^{N-1}.                  \tag{2}
$$

This is the ordinary inclusion-exclusion formula for a cube section.

2. When m=0, the answer is zero if either a or b is zero. Otherwise
put \(s=b-a\). If |s|≥R the answer is zero; if |s|<R it is

$$
I_{a,b,0}(R)=
\frac1{2^{a+b-1}(a-1)!(b-1)!}
\int_{|s|}^{R}(t+s)^{a-1}(t-s)^{b-1}\,dt.                  \tag{3}
$$

3. When m≥1 and a≥1,b=0, let \(s_j=m-a-2j\). Define

$$
J_{a,m}(s,R)=
\begin{cases}
\displaystyle\frac1{(a-1)!(m-1)!}
\int_0^{\min(R,s)}P^{a-1}(s-P)^{m-1}\,dP,&s>0,\\
0,&s\leq0.
\end{cases}
$$

Then

$$
I_{a,0,m}(R)=\sum_{j=0}^{m}(-1)^j\binom mj J_{a,m}(s_j,R).
                                                               \tag{4}
$$

Reflection gives \(I_{0,b,m}=I_{b,0,m}\).

4. When a,b,m≥1, set \(s_j=m-a+b-2j\). With an empty integral defined
as zero, put

$$
J_{a,b,m}(s,R)=
\frac1{2^{a+b-1}(a-1)!(b-1)!(m-1)!}
\int_{-R}^{\min(R,s)}\int_{|v|}^{R}
 (t+v)^{a-1}(t-v)^{b-1}(s-v)^{m-1}\,dt\,dv.                \tag{5}
$$

Then

$$
I_{a,b,m}(R)=
\sum_{j=0}^m(-1)^j\binom mj J_{a,b,m}(s_j,R).                \tag{6}
$$

To evaluate (5), expand all powers, integrate in t, and split the
v-integral at zero. No root-finding or numerical quadrature is needed.

For completeness, (3)–(6) follow directly by letting P be the sum
of the a positive excesses, M the sum of the b negative excesses,
and W the sum of the m shifted inactive coordinates \(x+1\in[0,2]\).
The constraints become

$$
P+M\leq R,\qquad P-M+W=m-a+b.
$$

The simplex fiber densities are \(P^{a-1}/(a-1)!\) and
\(M^{b-1}/(b-1)!\). Inclusion-exclusion for the m upper bounds
on the shifted inactive coordinates changes the right side to
\(s_j\) and contributes the factor \((-1)^j\binom mj\).
Their remaining density is
\((s_j-P+M)_+^{m-1}/(m-1)!\).
Finally \(t=P+M,v=P-M\) has inverse Jacobian 1/2.
These observations prove every case, including the factorial and
power-of-two normalizations.

[exact_section.py](exact_section.py) implements these formulas using
arbitrary-size integers and rational arithmetic. The verifier compares
them to direct halfspace intersection and facet volumes in small
dimensions, a different geometric decomposition. For example

$$
C_1=2,\quad C_2=16/3,\quad C_3=127/8,\quad
C_4=6208/125,\quad C_5=103561/648.
$$

The proof of the all-dimensional formula is the stratum calculation
above; finite comparisons corroborate its implementation.
