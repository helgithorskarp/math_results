# Proof of the spectral-to-gamma bridge

## 1. Transfer counts and the reduced numerator

For fixed dilation \(n\), a lattice point of \(nQ_m\) is a cyclic word
\((x_0,\ldots,x_{m-1})\) in \(\{0,\ldots,n\}\) satisfying
\(x_i+x_{i+1}\le n\). Therefore

\[
|nQ_m\cap\mathbb Z^m|=\operatorname{tr}(A_{n+1}^m)=p_m(n+1),             \tag{5}
\]

where \((A_N)_{rs}=1\) when \(r+s\le N-1\), and is zero otherwise.

The exact parity result in the adjacent source proves

\[
H_m(t)=(1+t)^mR_m(t),\qquad \deg R_m=m-1,
\]

with \(R_m\) palindromic. Direct cancellation in the definitions gives

\[
R_m(t)=(1-t)^{m+1}(1+t)F_m(t).                            \tag{6}
\]

Consequently there is a unique polynomial \(\Gamma_m\), of degree at most
\(q=(m-1)/2\), such that

\[
R_m(t)=(1+t)^{m-1}\Gamma_m\!\left(\frac{t}{(1+t)^2}\right).             \tag{7}
\]

## 2. Lagrange inversion

Put \(x=t/(1+t)^2\), and let \(t=t(x)\) be the formal solution with
\(t(0)=0\). From (6)--(7),

\[
G(t):=\Gamma_m\!\left(\frac{t}{(1+t)^2}\right)
     =(1-t)^{m+1}(1+t)^{2-m}F_m(t).                       \tag{8}
\]

Since \(t=x(1+t)^2\), Lagrange--Bürmann gives, for \(j\ge1\),

\[
\gamma_{m,j}=\frac1j[t^{j-1}]G'(t)(1+t)^{2j}.             \tag{9}
\]

Differentiate \(G(t)(1+t)^{2j}\) and compare the coefficient of
\(t^{j-1}\). Equation (9) becomes

\[
\begin{aligned}
\gamma_{m,j}
 &= [t^j]G(t)(1+t)^{2j}
    -2[t^{j-1}]G(t)(1+t)^{2j-1}\\
 &= [t^j](1-t)G(t)(1+t)^{2j-1}\\
 &= [t^j](1-t)^{m+2}(1+t)^{2j+1-m}F_m(t).                 \tag{10}
\end{aligned}
\]

The same expression is valid at \(j=0\), because both sides equal one.
Only coefficients of \(F_m\) through degree \(j\) can contribute, so (5)
turns (10) into the finite formula

\[
\gamma_{m,j}=[t^j](1-t)^{m+2}(1+t)^{2j+1-m}
              \sum_{n=0}^{j}p_m(n+1)t^n.                 \tag{11}
\]

Although the exponent of \(1+t\) is negative for \(j<q\), (11) is an
ordinary finite coefficient extraction in \(\mathbb Z[[t]]\). It is not an
analytic limiting statement.

## 3. The determinant and Newton recurrence

Let

\[
D_N(z)=\det(I-zA_N)=\sum_{k=0}^{N}d_{N,k}z^k.
\]

The cycle transfer determinant has the two-step form

\[
D_{N+2}(z)=(2-z^2)D_N(z)-D_{N-2}(z),                     \tag{12}
\]

starting with

\[
D_0=1,\quad D_1=1-z,\quad D_2=1-z-z^2,\quad
D_3=1-2z-z^2+z^3.                                       \tag{13}
\]

For completeness, put \(w=1-z^2/2\). With \(U_r\) denoting the Chebyshev
polynomial of the second kind, the two parity classes are

\[
\begin{aligned}
D_{2r}(z)&=U_r(w)-(1+z)U_{r-1}(w),\\
D_{2r+1}(z)&=(1-z)U_r(w)-U_{r-1}(w).
\end{aligned}                                             \tag{14}
\]

The usual convention \(U_{-1}=0\) covers \(r=0\). The formulas follow
either by the elementary sine eigenvectors of the Hankel matrix \(A_N\),
or from Ehrenborg's transfer determinant. The Chebyshev recurrence gives
(12) immediately, and (13) fixes the normalization. The checker also
compares (12) directly with the permutation expansion of the determinant
for \(N\le7\).

If \(\lambda_1,\ldots,\lambda_N\) are the eigenvalues of \(A_N\), then

\[
-\frac{zD_N'(z)}{D_N(z)}
  =\sum_{r\ge1}\left(\sum_i\lambda_i^r\right)z^r
  =\sum_{r\ge1}p_r(N)z^r.
\]

Equating coefficients gives

\[
p_r(N)=-r d_{N,r}-\sum_{k=1}^{r-1}d_{N,k}p_{r-k}(N),      \tag{15}
\]

where \(d_{N,r}=0\) for \(r>N\). Equations (11)--(15) prove the claimed
finite exact recurrence for the entire gamma vector.

## 4. The first three gamma coefficients

Formula (11) immediately gives \(\gamma_{m,0}=1\). For \(j=1\),

\[
\gamma_{m,1}=p_m(2)-2m+1.                                \tag{16}
\]

Now

\[
A_2=\begin{pmatrix}1&1\\1&0\end{pmatrix},
\]

so \(p_m(2)=L_m\), the \(m\)-th Lucas number. Thus

\[
\gamma_{m,1}=L_m-2m+1>0\qquad(m\ge5),                    \tag{17}
\]

for example by the Lucas recurrence and induction from \(L_5=11\) and
\(L_7=29\).

For \(j=2\), the first two nonconstant coefficients of
\((1-t)^{m+2}(1+t)^{5-m}\) are

\[
3-2m,\qquad 2m^2-6m+1.
\]

Hence

\[
\gamma_{m,2}=T_m+(3-2m)L_m+2m^2-6m+1,                   \tag{18}
\]

where \(T_m=p_m(3)\). Since

\[
\det(\lambda I-A_3)=\lambda^3-2\lambda^2-\lambda+1,
\]

Newton's identity is equivalently

\[
T_0=3,\quad T_1=2,\quad T_2=6,\qquad
T_r=2T_{r-1}+T_{r-2}-T_{r-3}.                            \tag{19}
\]

It remains to justify the strict sign in (18). The cubic in (19) has one
root \(a>11/5\), one root in \((0,1)\), and one root in \((-1,0)\): evaluate
it at \(-1,0,1,11/5,3\). Thus, for odd \(m\),

\[
T_m>a^m-1.
\]

Writing \(\varphi=(1+\sqrt5)/2<13/8\), one also has
\(L_m<\varphi^m\) for odd \(m\). The exact integer inequality

\[
\left(\frac{88}{65}\right)^9>15
\]

and induction in steps of two show
\((88/65)^m>2m-3\) for every odd \(m\ge9\). Therefore

\[
T_m>(2m-3)L_m-1\qquad(m\ge9),
\]

and (18) is greater than \(2m(m-3)>0\). The two remaining cases are
\(\gamma_{5,2}=1\) and \(\gamma_{7,2}=27\). This proves
\(\gamma_{m,2}>0\) for every odd \(m\ge5\) for which the coefficient exists.

Finally, the exact order \(m\) of the root of \(H_m\) at \(-1\), with
\((H_m/(1+t)^m)(-1)=1\), was proved in the adjacent parity source. Reading
the lowest-order term at \(-1\) in (7) gives

\[
\gamma_{m,q}=(-1)^q.                                    \tag{20}
\]

Equations (17), (18), and (20) prove the positive-prefix and terminal
statements without asserting signs for the intervening coefficients.

## 5. What remains open

Exact recurrence data suggest that \(\Gamma_m\) is real-rooted, with all
roots negative for \(m\equiv1\pmod4\), and with one positive root for
\(m\equiv3\pmod4\). Nothing in the argument above proves that assertion:
Newton recurrence is an exact evaluator, not a variation-diminishing or
interlacing theorem. A proof would need an additional structural input,
such as a Jacobi/matching determinant, a stable-polynomial interpretation,
or an interlacing operator for the diagonal family \(m=2q+1\).

