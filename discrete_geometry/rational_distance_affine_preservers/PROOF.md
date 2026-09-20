# Ambient affine preservers of rational-distance triangle density

For a noncollinear triangle \(T=(P_0,P_1,P_2)\) in the real plane, define
\[
 E(T)=\{Q:\ |Q-P_j|\in\mathbb Q\ (j=0,1,2)\},\qquad
 E_2(T)=\{Q:\ |Q-P_j|^2\in\mathbb Q\ (j=0,1,2)\}.
\]
Call \(T\) distance-admissible or square-admissible when \(E(T)\) or
\(E_2(T)\), respectively, is dense in \(\mathbb R^2\).
These loci are not asserted to have rational pairwise distances.

Let \(B=[P_1-P_0\ \ P_2-P_0]\) and \(G=B^TB\).
We use Corvaja--Turchet--Zannier [CTZ, Theorems 1 and 2]:

- square-admissibility is equivalent to \(G\in\operatorname{Sym}_2(\mathbb Q)\);
- distance-admissibility is equivalent to that condition together with
  \(z^TGz=1\) for some \(z\in\mathbb Q^2\).

Representing a nonzero rational square is equivalent to representing one
by homogeneity. The zero vector does not qualify.
These are imported density theorems; no correction to either is asserted.

## Exact preserver groups

**Theorem.** Let \(F(x)=Ax+b\), \(A\in\mathrm{GL}_2(\mathbb R)\).

1. \(F\) sends every square-admissible triangle to a square-admissible
   triangle if and only if
   \[
      A=\sqrt{\alpha}\,O,\qquad \alpha\in\mathbb Q_{>0},\quad O\in O(2).
   \]
2. \(F\) sends every distance-admissible triangle to a distance-admissible
   triangle if and only if
   \[
      A=rO,\qquad r\in\mathbb Q_{>0},\quad O\in O(2).
   \]

The translation \(b\) is arbitrary. One-sided preservation already implies
these characterizations; the resulting maps and their inverses preserve
the indicated class. Reflections are allowed.

**Proof of geometric rigidity.** Translation has no effect on the Gram
matrix. Put \(S=A^TA\).
Test the two fixed distance-admissible triangles
\[
 T_0=(0,e_1,e_2),\qquad T_*=(0,R e_1,R e_2),
 \quad R=R_{\pi/8}.
 \tag{1}
\]
They both have Gram matrix \(I\). If their images are square-admissible,
then \(S\) and \(R^TSR\) must both be rational matrices.
Write \(S=\left(\begin{smallmatrix}a&b\\b&c\end{smallmatrix}\right)\)
with rational \(a,b,c\). Direct computation gives
\[
 R^TSR=
 \begin{pmatrix}
 \frac{a+c}{2}+\frac{\sqrt2}{4}(a-c+2b)
   &\frac{\sqrt2}{4}(c-a+2b)\\
 \frac{\sqrt2}{4}(c-a+2b)
   &\frac{a+c}{2}-\frac{\sqrt2}{4}(a-c+2b)
 \end{pmatrix}. \tag{2}
\]
Rationality forces \(a-c+2b=c-a+2b=0\), hence \(a=c\) and \(b=0\).
Thus \(S=\alpha I\) with \(\alpha\in\mathbb Q_{>0}\), and
\(A=\sqrt\alpha\,O\).

This is necessary in both parts of the theorem, since distance-admissible
implies square-admissible. Conversely, such a similarity multiplies every
Gram matrix by \(\alpha\), preserving rationality in both directions.
Equivalently, \(E_2(F(T))=F(E_2(T))\).
This proves part 1. \(\square\)

The extra arithmetic restriction in part 2 follows from the next lemma.

**Norm obstruction lemma.** For each nonsquare
\(\alpha\in\mathbb Q_{>0}\), there is a positive integer \(d\) such that
\[
 \alpha(x^2+d y^2)=1 \tag{3}
\]
has no solution in \(\mathbb Q^2\).
An explicit choice is obtained from any prime \(p\) with \(v_p(\alpha)\)
odd. If \(p=2\), take \(d=3\). If \(p\) is odd, choose
\(1\le d<p\) such that \(-d\) is a quadratic nonresidue modulo \(p\).

**Proof.** Such a prime exists because a positive rational number is a
square exactly when all its prime valuations are even.
For odd \(p\), the equation \(X^2+dY^2=0\) modulo \(p\) has no nonzero
solution: if \(Y=0\), then \(X=0\), and otherwise it would make \(-d\)
a square. Thus, for rational \(x,y\) not both zero,
\[
 v_p(x^2+d y^2)=2\min\{v_p(x),v_p(y)\}
\]
after interpreting a zero coordinate as having infinite valuation.
In particular this valuation is even.

For \(p=2,d=3\), clear denominators and remove a common power of two.
For integer \(X,Y\) not both even, \(X^2+3Y^2\) is odd if exactly one
coordinate is odd, and is \(4\pmod8\) if both are odd. Its valuation is
therefore zero or two, respectively. Restoring the removed scale changes
the valuation by an even integer. So here also \(v_2(x^2+3y^2)\) is even.

In either case the valuation of the left side of (3) is odd, whereas
\(v_p(1)=0\). This contradiction proves the lemma. \(\square\)

**Completion of part 2.** By geometric rigidity, only \(A=\sqrt\alpha O\)
with positive rational \(\alpha\) remains. If \(\alpha\) is nonsquare,
choose \(d\) from the lemma and test
\[
 T_d=(0,(1,0),(0,\sqrt d)). \tag{4}
\]
Its Gram form \(x^2+d y^2\) is rational and represents one. It is therefore
distance-admissible by [CTZ]. The image form is
\(\alpha(x^2+d y^2)\), which does not represent one, so its image is not
distance-admissible.

Indeed \(E(F(T_d))\) is empty, a stronger conclusion. For any triangle
with rational nonsingular Gram matrix \(H\), rational squared distances
to its three vertices force the coordinates of the point in its edge
basis to be rational: subtract the distance equations and solve the
invertible rational linear system \(2Hz=\operatorname{diag}(H)+q_0-q_j\).
If all three distances were rational, at least one would be a nonzero
rational number. The form \(H\) would then represent a nonzero rational
square, hence one. This contradicts the norm obstruction.

It follows that \(\alpha=r^2\) for positive rational \(r\).
Conversely, an isometry followed by a rational nonzero scaling preserves
rationality of every distance in both directions, giving
\(E(F(T))=F(E(T))\). This proves part 2. \(\square\)

## A finite adaptive certificate

Every invertible affine map outside the distance-preserver group fails
on at least one of the two fixed triangles (1) or the single triangle
(4) chosen from an odd valuation of its scalar Gram factor.
If both fixed tests pass, its Gram factor is necessarily a positive
rational scalar; the third test is needed only if that scalar is nonsquare.
The third triangle is allowed to depend on the map.
For square-admissibility, the two fixed tests alone are necessary and
sufficient.

This is a uniform obstruction theorem, not an enumeration of affine maps.
For a matrix with arbitrary unspecified real entries, no algorithm for
deciding rationality of those entries is asserted.

## Explicit counterexamples to the introductory affine claim

The discussion immediately after the addendum to Theorem 1 of [CTZ]
(published pages 2–3; arXiv v2 after Theorem 1.1) describes a universal ambient
affine group containing rational invertible linear maps and scalings whose
squares are sums of two rational squares. Under the ordinary ambient action,
both of those preservation assertions fail:

1. Take \(A=\operatorname{diag}(2,1)\in\mathrm{GL}_2(\mathbb Q)\) and
   \(T_*\) from (1). The input Gram is \(I\), but its image Gram is
   \[
   \begin{pmatrix}
    5/2+3\sqrt2/4&-3\sqrt2/4\\
    -3\sqrt2/4&5/2-3\sqrt2/4
   \end{pmatrix}.
   \]
   It is not rational, so the image is not even square-admissible.
2. Take \(A=\sqrt2 I\) and \(T_3\) from (4). The factor squared is
   \(2=1^2+1^2\), but the image form \(2x^2+6y^2\) does not represent one.
   Consequently the image has no rational-distance extension point.

The second example also shows why testing only the two unit right triangles
cannot determine distance-admissibility preservation: their image form
\(2(x^2+y^2)\) does represent one, at \((1/2,1/2)\).
Furthermore every real orthogonal map preserves both classes, whether or
not it is a scalar multiple of a rational matrix.

The appropriate rational change-of-basis statement is different.
If the triangle edge matrix is \(B\) and \(M\in\mathrm{GL}_2(\mathbb Q)\),
replacing \(B\) by \(BM\) changes \(G\) to \(M^TGM\). Rationality and
representation of one are preserved. However, the corresponding ambient
map is \(BMB^{-1}\), which depends on the triangle. A single fixed rational
ambient matrix acts on the left, sending \(G\) to \(B^TA^TAB\), and
does not have that universal property.

These examples correct only the introductory affine-group assertion under
its ambient interpretation. They are consistent with, and the classification
uses, the paper's density criteria. This work is not a review of its
K3-surface arguments and does not resolve the Erdos--Ulam problem.

## Exact computation and its boundary

The checker evaluates the rotation using exact arithmetic in
\(\mathbb Q(c)\), \(c=\cos(\pi/8)\), with
\[
 c^4=c^2-\tfrac18,\qquad
 \sin(\pi/8)=4c^3-3c,\qquad \sqrt2=4c^2-2.
\]
This field has degree four: \(c^2=(2+\sqrt2)/4\) has degree two, and
cannot be a square in \(\mathbb Q(\sqrt2)\), since its norm \(1/8\) is
not a rational square. Thus nonzero higher basis coefficients really do
detect irrationality. Directly transformed vertex coordinates are compared
entry by entry with formula (2).

Norm certificates are checked by enumerating the finite residue obstruction
and by exact integer examples, including primes in denominators of the
rational scalar. For the explicit form \(2x^2+6y^2\), a separate homogeneous
test finds no primitive solution to \(2X^2+6Y^2=Z^2\) modulo 9 or modulo 16.
A rational solution would clear denominators to a primitive integral one,
so these are independently complete local obstruction certificates for
that example.

The code does not establish the imported density criteria, prove the
universal statement by enumeration, or provide independent peer review.
Those distinctions are part of the theorem's trust boundary.

[CTZ] P. Corvaja, A. Turchet, U. Zannier,
*Rational distances from given rational points in the plane*,
Geometriae Dedicata 219, article 59 (2025).
[Published article](https://link.springer.com/article/10.1007/s10711-025-01019-0);
[published PDF](https://d-nb.info/1372527907/34);
[arXiv v2](https://arxiv.org/html/2403.02030v2).
