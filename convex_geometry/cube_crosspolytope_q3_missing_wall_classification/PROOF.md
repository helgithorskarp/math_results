# Complete missing-wall classification for three distinct active weights

## 1. Setup and aggregate jumps

For

\[
A_v(b,R)=\int_{\mathbb R^N}\delta(v\cdot x-b)
\mathbf 1_{\{\sum_i(|x_i|-1)_+\le R\}}\,dx,
\]

put

\[
M=\|v\|_\infty,\qquad
B=\frac{|b|-\|v\|_1}{M}>0,\qquad s=R-B.
\]

Suppose there are three active coordinates with pairwise distinct normalized
magnitudes \(w_0,w_1,w_2\in(0,1]\).  A label \((i,J)\), where
\(J\subseteq\{0,1,2\}\setminus\{i\}\), has candidate wall

\[
\omega_{i,J}=B(1/w_i-1)+\frac2{w_i}\sum_{j\in J}w_j                 \tag{1}
\]

and, after removing the common positive factor from zero coordinates and
normal scaling, jump

\[
\Delta_{i,J}=
\frac{(-1)^{|J|}w_i^4}
{(w_0w_1w_2)
 \prod_{k\notin J,\ k\ne i}(w_i-w_k)
 \prod_{j\in J}(w_i+w_j)}.                              \tag{2}
\]

For a numerical candidate \(\omega\), define its aggregate jump

\[
C_\omega=\sum_{(i,J):\ \omega_{i,J}=\omega}\Delta_{i,J}.           \tag{3}
\]

**Aggregate-jump lemma.**  Near \(s=\omega\), the only nonpolynomial active
part of the section is

\[
\frac{C_\omega}{2}(s-\omega)_+^2.                                  \tag{4}
\]

Consequently \(\omega\) is a genuine wall if and only if
\(C_\omega\ne0\), and it disappears completely if and only if
\(C_\omega=0\).

Indeed, distinct weights make every supplier pole simple, and the global
subset formula gives exactly one quadratic hinge with derivative jump (2) for
each label.  Terms at other walls are polynomial or zero locally.  Adjoining a
zero-normal coordinate applies a linear integral operator, so an exact active
cancellation remains zero; when (3) is nonzero, its lowest lifted hinge still
has nonzero coefficient.

For a fixed supplier, the four tail sums are \(0,p,q,p+q\), where \(p,q\)
are distinct and positive.  They are pairwise distinct.  Thus a resonant wall
has either two or three labels, never two labels from the same supplier.

## 2. All two-label cancellations

Let the two suppliers have weights \(x>y\), let the third weight be \(z\), and
write

\[
r=y/x,\qquad u=z/x,\qquad \beta=B/x,
\qquad 0<r<1.                                             \tag{5}
\]

For the \(x\)-supplied label, let \(e,f\) indicate whether \(y,z\) belong to
its tail.  For the \(y\)-supplied label, let \(g,h\) indicate whether \(x,z\)
belong to its tail.  We encode the pair by the four bits \(efgh\).  Put

\[
D(r)=r^5+r^4-r+1>0,                                      \tag{6}
\]

and let \(\alpha=(\sqrt5-1)/2\).  Let \(\beta_0\) denote the unique root in
\((0,1)\) of \(r^4+r^3-1\); numerically
\(\beta_0=0.819172513396\ldots\).

**Theorem 1 (two-label normal forms).**  Subject to the exclusions below, a
two-label candidate disappears exactly in one of the following four rows.

| Bits | Colliding labels | \(u=z/x\) | \(\beta=B/x\) | Parameter range |
|---|---|---|---|---|
| 0100 | \((x,\{z\})\), \((y,\varnothing)\) | \(\dfrac{r(r^2-r+1)}{(1-r)(r^2+1)}\) | \(\dfrac{2r^2(r^2-r+1)}{(1-r)^2(r^2+1)}\) | \(0<r<1\) |
| 1000 | \((x,\{y\})\), \((y,\varnothing)\) | \(\dfrac{r(r^4+r^3-r+1)}{D(r)}\) | \(\dfrac{2r^2}{1-r}\) | \(0<r<1\) |
| 1001 | \((x,\{y\})\), \((y,\{z\})\) | \(\dfrac{r(r^2+1)(r^2+r-1)}{D(r)}\) | \(\dfrac{2r(r+1)(1-r^3-r^4)}{D(r)}\) | \(\alpha<r<\beta_0\) |
| 1100 | \((x,\{y,z\})\), \((y,\varnothing)\) | \(\dfrac{r(r^2+1)(1-r-r^2)}{D(r)}\) | \(\dfrac{2r^2(1-r)(r^3+2r^2+2r+2)}{D(r)}\) | \(0<r<\alpha\) |

In the first row require \(u\ne1\), as the weights are distinct, and exclude
the unique roots in \((0,1)\) of

\[
E_1(r)=r^7-2r^6+4r^5-6r^4+7r^3-5r^2+3r-1              \tag{7}
\]

and

\[
E_2(r)=r^3+r-1.                                         \tag{8}
\]

They are \(0.614437260273\ldots\) and
\(0.682327803828\ldots\).  At these parameters a third-supplier label joins
the wall; the displayed pair cancels but the third jump is nonzero.

In the 1001 row exclude the unique root in \((0,1)\) of

\[
E_3(r)=r^{10}+2r^9+r^8-3r^6-r^5+3r^4+r^3+3r^2-2r-1,   \tag{9}
\]

namely \(0.736190214769\ldots\), for the same reason.  There are no
third-supplier exceptions in the 1000 or 1100 rows.

To recover normalized weights from a row, take

\[
x=\frac1{\max(1,u)},\qquad y=rx,qquad z=ux,qquad B=\beta x.        \tag{10}
\]

Arbitrary coordinate permutations give all placements of these normal forms.

### Proof of Theorem 1

With \(x\) divided out, collision of the two labels determines

\[
\beta=
\frac{2\bigl(g+h u-r(e r+f u)\bigr)}{r-1}.             \tag{11}
\]

Substitution of (2) gives a cancellation numerator linear in \(u\).  Factoring
the sixteen bit patterns and imposing \(u>0,\beta>0\) leaves exactly:

| Bits | Disposition |
|---|---|
| 0000 | \(\beta=0\) |
| 0001, 0010, 0011 | \(\beta<0\) |
| 0100 | first normal form |
| 0101 | \(\beta<0\) |
| 0110 | cancellation forces \(\beta<0\) |
| 0111 | \(\beta<0\) |
| 1000 | second normal form |
| 1001 | third normal form and its stated range |
| 1010, 1011 | \(\beta<0\) |
| 1100 | fourth normal form and its stated range |
| 1101 | cancellation forces \(u<0\) |
| 1110 | cancellation forces \(\beta<0\) |
| 1111 | \(\beta<0\) |

Solving the four surviving linear equations gives the displayed rational
functions.  Their denominators are positive on the stated intervals.  Direct
substitution gives collision and \(\Delta_x+\Delta_y=0\).

Only the four labels supplied by \(z\) can now join the wall.  Substitution
factors their four wall differences.  The factors with roots in the admissible
intervals are precisely (7)--(9), together with
\(2r^3-2r^2+2r-1\), whose root is exactly \(u=1\).  Sturm sequences show that
each has the single root stated above.  All remaining factors have constant
sign.  This proves both sufficiency and exhaustiveness.

## 3. All three-label cancellations

Order and normalize the weights as

\[
1>a>b>0.                                                \tag{12}
\]

For suppliers \(1,a,b\), number their four tails in the orders

\[
(\varnothing,\{a\},\{b\},\{a,b\}),\quad
(\varnothing,\{1\},\{b\},\{1,b\}),\quad
(\varnothing,\{1\},\{a\},\{1,a\}),                   \tag{13}
\]

respectively.  Thus, for example, pattern 120 means tails
\(\{a\},\{b\},\varnothing\).

Define

\[
\begin{aligned}
P_1(X)={}&4X^{10}-15X^8-5X^7+15X^6+29X^5+29X^4\\
         &+X^3-11X^2-9X-2,                              \tag{14}\\
P_2(X)={}&3X^9+7X^8-3X^7-17X^6-11X^5+13X^4\\
         &+23X^3-X^2-8X-4.                              \tag{15}
\end{aligned}
\]

Each polynomial has exactly one root in \((0,1)\).

**Theorem 2 (three-label classification).**  There are exactly two
three-label missing-wall orbits.

1. **Pattern 120.**  Let \(a\) be the root of \(P_1\) in
   \((143177/200000,715887/10^6)\), and set
   \[
   b=\frac{a^2(2a^4-a^3-7a^2-5a-3)}
           {(a+1)(2a^4+a^3-6a^2-5a-2)}.                 \tag{16}
   \]
   Then
   \[
   (a,b,B)=(0.715885947903\ldots,0.385107425216\ldots,
   0.896719217149\ldots),
   \]
   where \(B=2(a^2-b)/(1-a)\).  At \(s=2a\), the labels are
   \((1,\{a\})\), \((a,\{b\})\), and \((b,\varnothing)\).

2. **Pattern 310.**  Let \(a\) be the root of \(P_2\) in
   \((867093/10^6,433547/500000)\), and set
   \[
   b=-\frac{a(a-1)(a+2)(a^3+2a^2+a-1)}
            {a^5+2a^4+3a^3+3a^2-3a-2}.                 \tag{17}
   \]
   Then
   \[
   (a,b,B)=(0.867093373463\ldots,0.543022300067\ldots,
   3.351254367605\ldots),
   \]
   where \(B=2(a^2+ab-1)/(1-a)\).  At \(s=2(a+b)\), the labels are
   \((1,\{a,b\})\), \((a,\{1\})\), and \((b,\varnothing)\).

In both cases the three individual jumps are nonzero and their sum is zero.
Thus the complete quadratic hinge disappears.

### Exact elimination proof

For each of the \(4^3=64\) tail patterns in (13), equate the weight-one wall
to the other two walls and clear denominators.  This gives one collision
polynomial \(F(a,b)\).  Clear the denominator of the aggregate jump to obtain
\(G(a,b)\).  Factors among

\[
a,\ b,\ 1-a,\ 1-b,\ a-b
\]

are nonzero in (12) and may be removed.  The exact subresultant chain of
\(F,G\) with respect to \(b\), followed by Sturm isolation in \(a\), leaves
only the following common-zero orbits in the open ordered triangle:

| Pattern | \(a\) | \(b\) | Sign of required \(B\) |
|---|---:|---:|---:|
| 120 | \(0.715885947903\ldots\) | \(0.385107425216\ldots\) | positive |
| 310 | \(0.867093373463\ldots\) | \(0.543022300067\ldots\) | positive |
| 312 | \(0.792818832435\ldots\) | \(0.293072881345\ldots\) | negative |

The last orbit is inadmissible because \(B>0\).  The first two subresultant
linear equations give (16)--(17), and their primitive univariate factors are
(14)--(15).  For every pattern, the simultaneous vanishing of the linear
subresultant's coefficient and constant term has no root in \(0<a<1\), after
the displayed nondegeneracy factors are removed; thus division by that
coefficient loses no open-chamber solution.  Exact substitution verifies the
wall collisions and zero aggregate jumps.  This proves Theorem 2.

## 4. Complete classification

Every positive candidate wall for three distinct active weights has one, two,
or three labels.  A one-label wall has nonzero jump.  Theorems 1 and 2 exhaust
the other two cases.  Hence the four rational curves, with their explicit
third-label exclusions, and the two isolated algebraic orbits are the complete
list of disappearing walls, up to coordinate permutation.

The symbolic derivation uses exact arithmetic in \(\mathbb Q[a,b]\); numerical
approximations only describe isolated roots.  The independent checker uses
integer Sturm sequences and rational interval arithmetic for all nine stated
root certificates, tests 269 rational instances of the four curves, and
reconstructs the original 27-halfspace polygon on both sides of one example
from each curve.  It also verifies three exact univariate divisibility
certificates showing that each displayed triple-orbit formula satisfies the
remaining collision equation at its isolating polynomial, after the displayed
formula for (B) enforces the first one.
