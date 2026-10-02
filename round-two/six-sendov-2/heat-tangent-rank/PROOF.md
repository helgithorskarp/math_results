# Heat-tangent independence in the small quartic-variance octic chamber

Actual author **six-sendov-2**, role **researcher**, 2026-10-02.
Complete ordinary author lemma with exact identity certificates, unformalized
and independently unreviewed. The polynomial here has degree eight and real
original roots; this is an auxiliary angular frontier for degree-nine
complex first-power Sendov research.

## 1. Statement and mathematical gain

Let u1<...<u8 be distinct real numbers, sum ui=0, and set

\[
 f(z)=\prod_{i=1}^8(z-u_i),\quad h=f'/8,\quad
 N=\sum u_i^2,\quad S_3=\sum u_i^3,\quad
 D=\sum u_i^4-N^2/8.
\]

Put d=D/N^2, v=S3/N^(3/2), s=v^2. Define fixed-N balanced tangents

\[
\begin{split}
 R&=zf'-8f,\\
 Q_0&=f''-(56/N)R,\\
 Q_1&=zf''-7f',\\
 Q_2&=z^2f''-13zf'+48f.                              \tag{1}
\end{split}
\]

They have degree at most five. Each gives a locally feasible two-sided
coefficient variation at the distinct original roots.

**Lemma.** If

\[
                    d\le\Delta=69/5000,                 \tag{2}
\]

then 1,Q0,Q1,Q2 are linearly independent over R. There is no exceptional
rank-drop locus in this chamber, including its closed upper boundary.
The lemma does not assume stationarity or a lower bound on an angular
functional.

**Explicit complement.** Write fk for the coefficient of z^k in f. Let
a1,...,a5=f1,...,f5 and define two four-component vectors

\[
\begin{split}
r={}&(35a_1+6a_5a_2/N,\quad
24a_2+15a_5a_3/(2N),\
15a_3+8a_5a_4/N,\
8a_4+15a_5^2/(2N)),\\
t={}&(6a_3-1568a_1/N,\
12a_4-1008a_2/N,\
20a_5-560a_3/N,\
-15N-224a_4/N).                                       \tag{3}
\end{split}
\]

At least one of the six minors rij=ri tj-rj ti, 1<=i<j<=4, is nonzero.
Choose the first such pair in lexicographic order, and let {k,l} be the
complement of {i,j} in {1,2,3,4}. Then

\[
                   1,Q_0,Q_1,Q_2,z^k,z^l                 \tag{4}
\]

is a basis of all real coefficient directions of degree at most five.
The choice is locally constant on its open minor chart; no one minor is
claimed nonzero everywhere.

The [constant-term reduction9271](../constant-term-angular-reduction/PROOF.md)
provides the complete six coefficient stationarity equations. The
[heat-stationary restriction9323](../heat-stationary-reduction/PROOF.md)
forces every all-distinct stationary angular profile with C>=24.531 to
satisfy d<20273/1471860<Delta. The present lemma therefore reduces its
remaining full stationarity check, after the constant and three heat
equations, to exactly the two explicit monomial directions in (4).
It neither constructs nor excludes a high stationary profile. Original
collisions and the global angular equality remain separate questions.

## 2. Preliminary inequalities and critical moments

N>0, and D>0 because D=sum(ui^2-N/8)^2; equality would leave at most two
distinct original roots. Moreover

\[
 S_3=\sum u_i(u_i^2-N/8),\qquad S_3^2\le ND.
\]

Equality in Cauchy would make every ui solve
ui^2-N/8=t ui for one real t, again leaving at most two distinct values.
Consequently

\[
                         0\le s<d.                      \tag{5}
\]

Scaling z by sqrt(N) changes each polynomial in (1) by a nonzero scalar
and an invertible change of variable. Linear independence is invariant.
We henceforth assume N=1. Write lambda1,...,lambda7 for the distinct
real critical points and Tj=sum lambda_i^j, so T0=7. Newton identities,
f6=-1/2, f5=-v/3 and f4=3/32-d/4 give

\[
 T_1=0,\quad T_2=3/4,\quad T_3=5v/8,\quad
 T_4=3/32+d/2.                                         \tag{6}
\]

For A_i=h''(lambda_i)/h'(lambda_i),

\[
 A_i=2\sum_{j\ne i}(\lambda_i-\lambda_j)^{-1}.
\]

For integer q>=1, pairing the ordered reciprocal terms proves

\[
 \sum_i\lambda_i^q A_i
   =\sum_{\ell=0}^{q-1}T_\ell T_{q-1-\ell}-qT_{q-1},
 \qquad \sum_iA_i=0.                                   \tag{7}
\]

This is the classical electrostatic relation for simple polynomial
zeros, rederived here. Its relation with quadratic differential equations
is credited to Stieltjes and subsequent literature, including
[Steinerberger, Theorem1, 2018](https://arxiv.org/abs/1804.09697).
No orthogonality classification or convergence theorem is a premise.

## 3. A hypothetical rank drop forces one quadratic ODE

Suppose e+aQ2+bQ1+cQ0=0 with a,b,c,e real and not all zero. Differentiation,
using f'=8h and R'=Q1, gives

\[
 (az^2+bz+c)h''
 -[(11a+56c)z+6b]h'+(35a+392c)h=0.                     \tag{8}
\]

At the simple critical roots this says

\[
 (a\lambda_i^2+b\lambda_i+c)A_i
             =(11a+56c)\lambda_i+6b.                   \tag{9}
\]

Multiplying by lambda_i^2 and lambda_i^3, summing, and using (7) and
T1=0 gives respectively

\[
\begin{split}
 (a+56c)T_3&=5bT_2,\\
 (2a+56c)T_4&=aT_2^2+4bT_3+11cT_2.
\end{split}                                            \tag{10}
\]

Substitution of (6) eliminates b:

\[
 a(d-3/8-5s/12)+c(28d-3-70s/3)=0.                     \tag{11}
\]

Since 28d-3-70s/3<=28Delta-3<0, a=0 would force c=0,
then b=0 by (10), then e=0. Thus a!=0. Dividing (8) by a and putting
kappa=c/a and rho=b/a gives

\[
\begin{split}
 \kappa&=\frac{3/8+5s/12-d}{28d-3-70s/3}
       =-\frac{9-24d+10s}{8(9-84d+70s)},\\
 \rho&=\frac{(1+56\kappa)v}{6}
       =\frac{v(14d-9)}{9-84d+70s}.                    \tag{12}
\end{split}
\]

In particular the purported critical polynomial satisfies

\[
 (z^2+\rho z+\kappa)h''
 -[(11+56\kappa)z+6\rho]h'+(35+392\kappa)h=0.           \tag{13}
\]

## 4. Exact moment obstruction to seven real critical nodes

Define the following bivariate polynomials:

\[
\begin{array}{ll}
 A_0=9-84d+70s,& B_0=-9-21d+35s,\\
 C_0=-9-56d+70s,& E_0=-9-126d+140s,\\
 J_0=-9-336d+350s,& K_0=9-504d+490s,
\end{array}
\]

\[
\begin{split}
 P_0={}&1176d^3+567d^2-3150ds-162d+875s^2+900s-81,\\
 Q_0^\flat={}&-381024d^3+82320d^2s^2+952560d^2s+88452d^2\\
 &-929040ds^2-166320ds+18468d+196000s^3
      +185220s^2-43740s+729,\\
 R_0^\flat={}&-37632d^2s+12096d^2+31584ds-4752d
                          +4900s^2-11052s+81.
\end{split}                                             \tag{14}
\]

The superscript flat distinguishes these scalar factors from the
tangent Q0 and radial polynomial R. From (9), after a=1, pairing as in
(7) gives for r=2,...,7

\[
\begin{split}
 [(r-1)+56\kappa]T_{r+1}
 ={}&\sum_{\ell=1}^{r}T_\ell T_{r+1-\ell}\\
 &+\rho\left[(7-r)T_r+
                \sum_{\ell=1}^{r-1}T_\ell T_{r-\ell}\right]\\
 &+\kappa\left[(14-r)T_{r-1}+
                \sum_{\ell=1}^{r-2}T_\ell T_{r-1-\ell}\right].
\end{split}                                             \tag{15}
\]

The r=2,3 equations agree with (10). The r=4,...,7 denominators are
4B0/A0, 3C0/A0, 2E0/A0, J0/A0. They do not vanish in the domain below.
Thus (6),(12),(15) determine T5,...,T8 uniquely.

Let G3=(T_(i+j))_(0<=i,j<=2) and H5=(T_(i+j))_(0<=i,j<=4).
An exact determinant expansion gives

\[
 \det G_3=-J_0/128,\qquad
 \boxed{\det H_5=
 \frac{(s-d)^2K_0J_0^2P_0^2Q_0^\flat}
 {2359296\,E_0^2C_0^3B_0^4}.}                           \tag{16}
\]

For an explicit short way to verify the second expansion, partition
H5 after its first three rows/columns, and let U be the two-by-two Schur
complement of G3. Recurrence (15) gives

\[
\begin{split}
 U_{33}&=\frac{(s-d)J_0P_0}{48C_0B_0^2},\\
 U_{34}&=\frac{3v(s-d)(14d-9)J_0P_0}{32E_0C_0B_0^2},\\
 U_{44}&=-\frac{(s-d)P_0R_0^\flat}{384C_0^2B_0^2}.
\end{split}                                             \tag{17}
\]

Indices 3,4 label the residual monomials z^3,z^4 after projection
onto 1,z,z^2. The polynomial identity

\[
 R_0^\flat E_0^2+
       162sC_0(14d-9)^2J_0=K_0Q_0^\flat                 \tag{18}
\]

then yields (16) via det H5=det G3 det U. The standalone checker proves
all three identities (17) by exact bivariate expansion from a directly
constructed adjugate of G3, and (18) by a separate expansion. Recurrences
are checked as polynomial identities after clearing their displayed
nonzero denominators. SymPy was used only for discovery, not as a
runtime or correctness premise of the published certificate.

Here are sufficient uniform rational sign bounds for 0<=s<d<=Delta:

\[
\begin{split}
 A_0&\ge9-84\Delta=9801/1250>0,\\
 B_0,C_0,E_0,J_0&\le-9+14\Delta=-22017/2500<0,\\
 K_0&\ge9-504\Delta=1278/625>0,\\
 P_0&\le1176\Delta^3+1442\Delta^2+900\Delta-81\\
    &=-1067223357927/15625000000<0,\\
 Q_0^\flat&\ge729-43740\Delta-166320\Delta^2-1310064\Delta^3\\
    &=705242786589/7812500000>0.
\end{split}                                             \tag{19}
\]

The P bound drops its nonpositive terms and bounds all positive
monomials separately. The Q bound drops its nonnegative terms and
bounds d^3, ds^2 by Delta^3, ds by Delta^2 and s by Delta.
Thus (16) is strictly negative.

But for seven distinct real nodes H5 is the Gram matrix of
1,z,z^2,z^3,z^4 with unit positive weights. A nonzero polynomial of
degree<=4 cannot vanish at all seven nodes, so H5 is positive definite.
Its determinant is positive, a contradiction. This excludes the
assumed relation and proves the rank-four lemma.

The earlier four-by-four moment determinant is positive in this domain;
positivity at that truncation alone would not have excluded the ODE.
The extra moments through degree eight supply the decisive obstruction.

## 5. Complement and the two remaining stationarity equations

Return to general N. The leading coefficient of Q1 is 6N at degree5.
Modulo constants, eliminate degree5 from Q2 and Q0:

\[
 r(z)=Q_2-\frac{a_5}{2N}Q_1,\qquad
 t(z)=Q_0-\frac{28a_5}{N^2}Q_1-\frac{56}{N}r(z).          \tag{20}
\]

Their degree1,...,4 coefficients are exactly (3). Constants in (20)
are immaterial because direction1 is already in the span. Since the
original four directions are independent, these two vectors are
independent. Some rij is nonzero. Appending the two remaining coordinate
vectors completes a basis in degree1,...,4; adjoining Q1 and1 gives (4).

For clarity, the complete first derivative from9271 can be written
without evaluating negative powers at a zero critical node. Let

\[
\begin{split}
 m_j&=-8f(\lambda_j)/h'(\lambda_j),\qquad \eta=\sum m_j^2,\\
 C&=(N^2-\eta)/D,\\
 {\cal L}(q)&=-16\sum_j\frac{m_jq(\lambda_j)}{h'(\lambda_j)}
 -\frac14\sum_j\frac{m_j^2q''(\lambda_j)}{h'(\lambda_j)}
 +\frac14\sum_j\frac{m_j^2h''(\lambda_j)q'(\lambda_j)}
                         {h'(\lambda_j)^2}.
\end{split}                                             \tag{21}
\]

Along f+epsilon q, degree q<=5, one has dot N=0, dot D=-4q4,
dot eta=L(q), and

\[
                  D\dot C=-{\cal L}(q)+4Cq_4.            \tag{22}
\]

Consequently, once the constant and three heat derivatives vanish in
(2), full stationarity is equivalent to the two additional equations

\[
 {\cal L}(z^k)-4C\,{\bf1}_{k=4}=0,\qquad
 {\cal L}(z^l)-4C\,{\bf1}_{l=4}=0.                        \tag{23}
\]

This is a complete local chart reduction. It supplies no sign for the
two remaining equations, and the rank proof does not assert that the
constant/heat equations have no feasible solution.

## 6. Domain controls, reproducibility and unresolved work

The small-variance restriction is substantive: the probabilists'
degree-eight Hermite polynomial

\[
 f_H=z^8-28z^6+210z^4-420z^2+105
\]

has eight simple real balanced roots, N=56, D=336 and d=3/28>Delta.
Its equation fH''-zfH'+8fH=0 gives Q0=0; the constant/heat span has
rank three. The classical Hermite equation is credited, and the
checker confirms simplicity/real-root count by exact Sturm arithmetic.

The [checker](verify.py) uses only CPython standard-library rational
arithmetic. Its [entire fixture](expected.json) records all fixed
polynomial coefficients, identities, sign bounds, four real-root
coefficient charts, five independent coefficient-ODE/Newton/direct
five-by-five determinant checks, the Hermite control, and six damage
rejections. The ODE sample polynomials are formal exact test cases and
are explicitly not claimed real-rooted. No sample grid or finite
enumeration establishes the universal rank result.

The ordinary bridges are strict interlacing, Cauchy equality, paired
root sums, positivity of a real-node Gram matrix, and the coefficient
root chart/first derivative. They are proved above or attributed
explicitly, but not formalized in a proof assistant. The finite checker
is by the same author and does not establish independent peer review.

All-distinct high stationary existence/nonexistence, feasible original
collision strata, C*=c3 globally, and the actual complex degree-nine
first-power inequality remain unresolved here. The next concrete step
is to use (23) inside the concentrated four-plus-four chamber of9323.
