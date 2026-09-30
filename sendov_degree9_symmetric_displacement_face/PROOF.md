# A symmetric displacement face has no improvement over the four-block optimizer

Actual author **six-sendov-2**, role **researcher**, 2026-09-30.
Status: ordinary written proof with an exact finite polynomial certificate
and definition-level author controls. Independent review pending;
not formalized. The general angular coefficient and its collision
continuity are credited dependencies, not new results here.

## 1. Precise claim

Put \(a_0=5/8\), \(d_0=13/8\), \(p_0=10985/33554432\).
For \(0\le X,u\le1\), take the balanced slope vector
\[
 \theta=(1,1,\sqrt X,\sqrt u,-1,-1,-\sqrt X,-\sqrt u).       \tag{1}
\]
The corresponding degree-nine disk-root polynomial is
\[
 p_{a,t,X,u}(z)=(z-a)q_1(z)^2q_{\sqrt X}(z)q_{\sqrt u}(z),
 \qquad q_c(z)=z^2+2\cos(ct)z+1.                            \tag{2}
\]
The eight other roots are \(-e^{it\theta_j}\), with multiplicity,
and \(\max_j|z_j+1|^2=2(1-\cos t)\) for sufficiently small real \(t\).
There are up to three distinct conjugate pairs, or six angular blocks.
Two pairs have the maximum slope one; the other two pairs can move.
This is a proper face of all centrally symmetric balanced directions.

For critical points counted with multiplicity let
\[
 F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\qquad
 E=\sum_{j=1}^8|(a+e^{it\theta_j})^{-1}-(1+a)^{-1}|^2.
\]
The existing reviewed angular theorem gives, at \(a=a_0\),
\[
 F-128/13=-K(\theta)E^2+o(E^2),
 \qquad E=\mu_2d_0^{-4}t^2+O(t^4),\quad\mu_2=4+2(X+u).
\]
Its coefficient and remainder are continuous and uniform on (1),
including repeated slopes and critical collisions. Define the
**displacement functional**
\[
                    J(X,u)=\mu_2K(\theta)/p_0.             \tag{3}
\]
The factor \(\mu_2\) matters: maximizing the energy coefficient
\(K\) is a different problem. In the previously established
moving-marked-radius crossing mechanism the leading squared
maximum-displacement constant is \(106496/[5J]\).
Only the functional optimization and stability below are claimed anew.

Let
\[
 j(u)=\frac{2058+21912u-15876u^2+19224u^3+3402u^4}
                {(3+u)(1+3u)^2},                          \tag{4}
\]
and let \(u_*\) be the unique root in \((2/25,9/100)\) of
\[
 T(u)=26634-231084u-907290u^2+376920u^3
                      +971190u^4+224532u^5+30618u^6.       \tag{5}
\]
The curve (4), its optimum and the corresponding actual crossing were
already published in the author's
[four-block theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_block_basin/PROOF.md).
Set \(J_*=j(u_*)\).

**Theorem.** Over the entire square \([0,1]^2\),
\[
       J(X,u)\le J_*,\qquad
       J(X,u)=J_*\ \Longleftrightarrow
       (X,u)\in\{(1,u_*),(u_*,1)\}.                         \tag{6}
\]
Thus allowing the extra movable conjugate pair in (2) cannot improve
the earlier coefficient. The sole maximizing slope multiset has
three copies each of \(1,-1\), and one each of
\(\sqrt{u_*},-\sqrt{u_*}\).
After interchanging parameters so \(0\le u\le X\le1\), there is the
explicit quantitative bound
\[
 \boxed{J_*-J(X,u)\ge
  \min\left\{\frac{12}{7},\frac{1-X}{2}+450(u-u_*)^2\right\}.} \tag{7}
\]
This is a global statement within face (1), rather than an infinitesimal
softening check. It does not optimize all balanced slopes, all symmetric
four-pair slopes, or the unrestricted maximum-original-root basin.
It neither resolves nor refutes the degree-nine first-power endpoint
\(F\ge8\): the collapsed baseline here is \(128/13>8\).

## 2. A rational formula for the compression weights

Write \(S=X+u\), \(P=Xu\), and define
\[
\begin{aligned}
 A&=2+3S,& B&=S+2P,& \Delta&=A^2-16B,\\
 C_0&=S^2+2S+2PS-12P,&
 C_1&=8P-3S^2+4S-4,& W&=2C_1B+C_0A.
\end{aligned}                                             \tag{8}
\]
The symbol \(P\) here is a scalar product of parameters.
In the physical square,
\[
 \Delta=9(X-u)^2+4(1-X)(1-u)\ge0.                           \tag{9}
\]
Here \(B=0\) only at \((0,0)\), and \(\Delta=0\) only at \((1,1)\).

Let \(e=\mathbf1/\sqrt8\), \(P_e=I-ee^T\),
\(\Theta=\operatorname{diag}(\theta)\),
\(\mathcal A=P_e\Theta P_e|_{e^\perp}\), and \(w=\Theta e\).
For each distinct eigenvalue let
\(r_\lambda=\|\Pi_\lambda w\|^2\), and set
\(\Psi=\sum_\lambda r_\lambda^2\).
Full eigenspaces are used at collisions. The reviewed angular formula is
\[
 K(\theta)=p_0\left[224\frac{\mu_4}{\mu_2^2}
                      +122-5760\frac{\Psi}{\mu_2^2}\right],
 \quad \mu_4=4+2(X^2+u^2).                                \tag{10}
\]

For completeness, the needed compression identities follow directly
from a classical Schur complement. The auxiliary slope polynomial is
\[
 f(z)=(z^2-1)^2(z^2-X)(z^2-u)=g(z^2),
 \quad g(y)=(y-1)^2(y^2-Sy+P).
\]
It is not the original-root polynomial (2).
Since \(e^T(zI-\Theta)^{-1}e=f'(z)/(8f(z))\), and the balanced
block matrix of \(\Theta\) is
\(\left(\begin{smallmatrix}\mathcal A&w\\w^T&0\end{smallmatrix}\right)\),
\[
 \det(zI-\mathcal A)=f'(z)/8,
 \qquad w^T(zI-\mathcal A)^{-1}w=z-8f(z)/f'(z).             \tag{11}
\]
These rational identities extend across cancellations; no novelty is
claimed for the derivative-compression representation.

First work on \(0<u<X<1\). Exact differentiation gives
\[
 g'(y)=(y-1)Q(y),\quad Q(y)=4y^2-Ay+B,
 \quad f'(z)=2z(z^2-1)Q(z^2).
\]
The eigenvalues \(1,-1\) have zero \(w\)-weight. The others are
zero and \(\pm\sqrt{y_+},\pm\sqrt{y_-}\), where
\(y_\pm=(A\pm\sqrt\Delta)/8\).
The two weights at each opposite pair agree, by the permutation swapping
opposite slopes. Taking residues in (11) gives
\[
 r_0=4P/B,\qquad
 r(y)=-\frac{2(y-1)(y^2-Sy+P)}{y(8y-A)}\quad(Q(y)=0).       \tag{12}
\]
Reducing the numerator modulo \(Q\),
\[
 (y-1)(y^2-Sy+P)\equiv(C_1y+C_0)/16,\qquad
 r(y)=-\frac{C_1B+C_0A-4C_0y}{8B(8y-A)}.
\]
Consequently
\[
 r_++r_-=C_0/(8B),\qquad
 r_+-r_-=-W/(8B\sqrt\Delta),\qquad
 r_0+2r_++2r_-=\mu_2/8.
\]
Squaring the weights proves the rational formula
\[
 \boxed{\Psi(X,u)=
 \frac{(1024P^2+C_0^2)\Delta+W^2}{64B^2\Delta}.}            \tag{13}
\]
It holds on every nonsingular edge by continuity. The credited collision
lemma supplies this continuity: repeated compression eigenspaces have
zero \(w\)-weight, so merging zero weights cannot change their squared sum.
At \((0,0)\) the nonzero resolvent is \(z/(2z^2-1)\), with weights
\(1/4,1/4\); hence \(\Psi=1/8\). At \((1,1)\) it is \(1/z\),
with weight one; hence \(\Psi=1\).
Inserting these in (10) gives \(J(0,0)=532\), \(J(1,1)=480\).

Combining (3), (10), (13), put
\[
\begin{aligned}
 Z&=(1024P^2+C_0^2)\Delta+W^2,\\
 N&=(468S^2+976S+1424-448P)B^2\Delta-45Z,\\
 D&=(S+2)B^2\Delta.
\end{aligned}
\]
Then
\[
                         J=N/D                            \tag{14}
\]
off the two exceptional corners, with the continuous values just given.
The denominator is positive everywhere else in the square.
These are generic rational identities, not fitted numerical coefficients.

## 3. Exact reduction to the boundary

Symmetry allows \(u\le X\). In this section write
\(\widehat N(X,u)=N(X+u,Xu)\),
\(\widehat D(X,u)=D(X+u,Xu)\),
\[
 G=780\widehat D-\widehat N,
 \qquad H=(\partial_X\widehat N)\widehat D
                         -\widehat N(\partial_X\widehat D).
\]
The following finite certificate establishes
\[
\begin{array}{ll}
 J\le780,&0\le u\le X\le3/4,\\
 J\le780,&3/4\le X\le1,\quad1/4\le u\le X,\\
 H>5000,&3/4\le X\le1,\quad0\le u\le1/4.
\end{array}                                                \tag{15}
\]

Here is the complete specification of the certificate.
Define \(L(x,v)=G(x,xv)/x^2\); the division is an exact polynomial
division, so \(L\) is defined also at zero.
Define \(U(x,v)=G(x,1/4+(x-1/4)v)\).
For a box \([x_0,x_1]\times[v_0,v_1]\), first make its affine
substitution into the unit square. If the resulting polynomial has
power coefficients \(c_{ij}\) and coordinate degrees \(m,n\), its
tensor Bernstein coefficients are exactly
\[
 b_{kl}=\sum_{i\le k,j\le l}c_{ij}
             \frac{\binom{k}{i}}{\binom m i}
             \frac{\binom l j}{\binom n j}.                \tag{16}
\]
The Bernstein basis is nonnegative and sums to one on the unit square.
The minimum entry therefore bounds the polynomial from below.
No numerical sampling or solver is used.

| Polynomial | x interval | second interval | Degrees | Entries | Minimum |
| --- | --- | --- | --- | --- | --- |
| L | [0,3/4] | [1/2,1] | (6,6) | 49 | 8871/4 |
| L | [3/8,3/4] | [1/4,1/2] | (6,6) | 49 | 202153954571/134217728 |
| L | [3/8,3/4] | [0,1/4] | (6,6) | 49 | 81007363/122880 |
| L | [0,3/8] | [0,1/2] | (6,6) | 49 | 36110717/49152 |
| U | [3/4,1] | [0,1] | (8,6) | 63 | 0 |
| H | [3/4,1] | [0,1/4] | (10,10) | 121 | 2814851493/524288 |

These are all **380** entries, reconstructed exactly by
[verify.py](verify.py), which also reverses every full Bernstein
expansion back to its power polynomial. The U certificate has three zero
entries; every other listed entry is strictly positive.
The four L boxes cover its whole required rectangle.
For \(X>0\), \(u=Xv\) covers the lower triangle. For the upper
region, \(u=1/4+(X-1/4)v\) covers its trapezoid.
At the exceptional corners the separately computed J values are below780.
Division by positive \(\widehat D\) proves the first two parts of (15).

On the last rectangle in (15),
\[
 S+2\le13/4,\quad B\le7/4,\quad\Delta\le10,
 \qquad0<\widehat D\le3185/32<100.
\]
Thus
\[
                   \partial_XJ=H/\widehat D^2>1/2.        \tag{17}
\]
The already published boundary curve is reproduced by exact
cross multiplication: \(J(1,u)=j(u)\).
Since \(j(1/9)=5472/7>780\), every global maximizer avoids
the first two regions of (15). It has \(X>3/4,u<1/4\).
Integrating (17) from X to one shows that every maximizer has X=1.
This is a global reduction on the entire two-parameter face.

## 4. Unique optimizer and quantitative rigidity

Let \(D_b(u)=(3+u)(1+3u)^2\). Exact differentiation of (4) gives
\(j'(u)=T(u)/D_b(u)^2\).
On \([0,1/4]\), discard the negative linear term in T' and bound
each remaining positive power by its endpoint value. This gives
\[
 T'(u)\le-231084+\sum_{k=3}^6kT_k(1/4)^{k-1}
            =-24357717/256<-90000.                         \tag{18}
\]
Here \(T_k\) are the displayed coefficients in (5).
The exact signs \(T(2/25)>0>T(9/100)\) give exactly one root
\(u_*\) in \([0,1/4]\). The derivative j' is positive before it
and negative after it, so this is the unique boundary maximum relevant
to (15), proving (6). In particular its scalar maximum is nondegenerate.
The argument reproduces the needed part of the credited older scalar
optimizer, rather than attributing that optimizer anew.

Moreover \(D_b(u)\le637/64<10\) on this interval.
The mean value theorem applied to T, with \(T(u_*)=0\), gives
\[
 j'(u)\ge900(u_*-u)\quad(u<u_*),\qquad
 j'(u)\le-900(u-u_*)\quad(u>u_*).
\]
Integrating proves
\[
                        j(u_*)-j(u)\ge450(u-u_*)^2.        \tag{19}
\]
If \(J(X,u)>780\), (15), (17), (19) yield
\[
 J_*-J(X,u)\ge(1-X)/2+450(u-u_*)^2.
\]
If \(J(X,u)\le780\), its gap is at least
\(J_*-780\ge5472/7-780=12/7\).
These two cases prove the global quantitative claim (7).

## 5. A closed monotonicity route and the remaining boundary

A tempting stronger reduction would assert that spreading X,u at
fixed sum always increases J. It is false.
At the strictly interior physical pair \((X,u)=(15/16,1/16)\),
\(S=1,P=15/256\), exact differentiation of (14) gives
\[
 \left.\partial_PJ(S,P)\right|_{(1,15/256)}
                =765897880984/3166916181>0.                \tag{20}
\]
Moving the two squared slopes toward their fixed-sum mean increases P
and hence increases J locally at this point. This rules out universal
spread monotonicity on the physical face; it is not a polynomial
counterexample to a first-power inequality. The conditional increasing-X
route (15) succeeds where a globally monotone spread route fails.

The new result fixes the exact spectral invariant and maximizer on an
expanded angular face, with explicit rigidity. The old
\(B_*=106496/[5j(u_*)]\) remains the obstruction constant;
its previously published enclosure is \((27.106707,27.106708)\).
No better universal basin constant is reported in this contribution.
To cover every centrally symmetric direction one must still release
the second saturated unit pair, allowing slopes
\(\pm1,\pm\sqrt Y,\pm\sqrt X,\pm\sqrt u\).
Noncentrally-symmetric balanced directions are a further boundary.
The new all-disk energy-basin theorem of six-sendov-3 supplies a separate
joint moving-radius reduction, with review pending; it does not optimize
the displacement functional over those larger slope sets.

## 6. Reproduction and trust boundary

Run the standalone checker from repository root as specified in
[README.md](README.md). It reconstructs the complete rational formula,
the derivative numerator, all six Bernstein expansions and their
inverses, the boundary derivative and monotonicity obstruction.
It also computes seven definition-level spectral controls without root
finding: project \(ww^T=\theta\theta^T/8\) onto the real symmetric
commutant of the rational full matrix \(P_e\Theta P_e\).
The squared Frobenius norm of that projection is precisely
\(\sum\|\Pi_\lambda w\|^4\), because orthogonal projection onto
the commutant is spectral pinching. The extra e direction has zero w
component. Every commutation constraint and the orthogonal target
decomposition are checked, including dependent constraints.
These finite controls include the singular corners and repeated slopes.

All arithmetic uses exact standard-library fractions; no floating point,
solver, numerical root finder, interpolation or external data is used.
The residue and commutant routes are different author algorithms,
not independent reviewer implementations. Six corrupt-manifest controls
test fail-closed manifest equality. The polynomial certificates prove
signs over full specified regions; the seven matrix profiles alone do not
prove a universal identity. The universal spectral bridge, collision
continuity, physical family, region coverage, and calculus interpretation
are the written proof and credited inputs. No formal verification or
independent acceptance of this extension is claimed.
