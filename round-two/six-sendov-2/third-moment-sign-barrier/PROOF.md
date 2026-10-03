# A zero-third-moment sign barrier for the degree-nine angular problem

Actual author **six-sendov-2**, role **researcher**, 2026-10-03.
Complete ordinary author proof with exact finite algebra checks;
**unformalized and independently unreviewed**. The moment method is
classical. No historical priority is claimed; see [LITERATURE.md](LITERATURE.md).

Let \(u\in\mathbb R^8\) satisfy
\[
 \sum_i u_i=0,\qquad \sum_i u_i^2=1,\qquad \sum_i u_i^3=0.
\]
Write \(p=\#\{i:u_i>0\}\), \(q=\#\{i:u_i<0\}\),
\(X=\sum_i u_i^4\), and let \(r\) count the distinct coordinate values,
including zero when it occurs. Coordinates and multiplicities are real
original-root slopes, not an arbitrary list of critical points.

**Moment lemma.** If \(\min(p,q)\le3\), then
\[
                         X\ge\frac16.
\]
Equality holds exactly at permutations and reflections of
\[
 \frac1{\sqrt6}(1,1,1,-1,-1,-1,0,0).
\]
Only the third odd moment is assumed; the fifth odd moment is not needed.

For the angular functional of [7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md),
put
\[
 e=\mathbf1/\sqrt8,\quad P=I-ee^T,\quad
 H=(P\operatorname{diag}(u)P)|_{e^\perp},\quad
 w=\operatorname{diag}(u)e,
\]
and for every distinct eigenvalue use its **full** spectral projection:
\[
 \rho_\lambda=8\|\Pi_\lambda w\|^2,\quad
 \eta=\sum_\lambda\rho_\lambda^2,\quad
 C(u)=\frac{1-\eta}{X-1/8}.
\]
These definitions include every original-root collision and every repeated
critical eigenspace. On the sign sector considered here, the denominator
is at least \(1/24\), so no singular extension is required.

**Angular corollary.** On the entire sign sector of the moment lemma,
\[
 C(u)\le\frac{24(r-2)}{r-1}\quad\hbox{and}\quad C(u)<\frac{144}{7}.
\]
The latter constant is a sufficient bound, not a sharp angular maximum.
In particular, every zero-third-moment profile with \(X>1/8\) and \(C(u)\ge144/7\)
has exactly four positive and four negative coordinates and no zero.
This applies to the two-odd-moment-zero collision chart in
[10136](../collision-moment-reduction/PROOF.md), as well as its more singular
collision strata. It supplies a sign restriction, not their stationary
classification or the complex first-power Tang--Zhang endpoint.

## 1. Compactness and regular minimizing faces

The set \(\{u:\min(p,q)\le3\}\) is closed: its complement requires
at least four strictly positive and four strictly negative coordinates
and is open. Intersecting it with the balanced unit sphere and the
zero-third-moment equation gives a compact set. It is nonempty, because
the displayed equality profile belongs to it. Thus \(X\) has a minimum.

At a minimum let \(n\) be the number of nonzero coordinates. For \(n\le6\),
Cauchy--Schwarz gives
\[
       1=(\sum_{i:u_i\ne0}u_i^2)^2\le nX,\qquad X\ge1/n\ge1/6.
\]
Equality in \(X=1/6\) forces \(n=6\) and six equal squared magnitudes.
Balance then forces three of each sign. The resulting profile also has
zero third moment. It remains to exclude minima with \(n=7,8\).

Reflect the minimizing vector if necessary so that \(p\le3\), and fix its
nonzero support and signs. All its nonzero coordinates lie in an open
orthant of \(\mathbb R^n\); keeping its zero coordinates fixed and making
a sufficiently small perturbation on this face preserves the sign count.
The three constraints on this face are
\[
             \sum t_i=0,\quad \sum t_i^2=1,\quad \sum t_i^3=0.       \tag{1}
\]

A single nonzero level cannot balance. For two nonzero levels, let
\(k\) entries equal \(a>0\) and \(m\) entries equal \(-b<0\).
Balance and the third moment say \(ka=mb\) and \(ka^3=mb^3\).
Dividing gives \(a^2=b^2\), hence \(a=b\) and \(k=m\).
This is impossible for \(n=7\); for \(n=8\) it gives \(p=4\), also excluded.

With at least three distinct nonzero levels, the constraint gradients
in (1), whose rows are \(1,2t_i,3t_i^2\), have rank three. A three-column
minor at distinct levels is a nonzero scaled Vandermonde determinant.
The implicit function theorem therefore gives a smooth constraint
manifold in this open sign face, with tangent space equal to the common
kernel of those three rows. Lagrange multipliers give, at every level,
\[
            A(t)=4t^3-3\beta t^2-2\alpha t-\gamma=0.               \tag{2}
\]
Hence there are exactly three levels \(t_1<t_2<t_3\), and
\(A(t)=4(t-t_1)(t-t_2)(t-t_3)\).

The constrained Hessian is diagonal, with coefficient
\[
             A'(t_2)=4(t_2-t_1)(t_2-t_3)<0                         \tag{3}
\]
at the middle level. If that level had multiplicity at least two, the
vector which adds one to one such coordinate and subtracts one from
another would belong to the tangent space of all three constraints.
Its Hessian value is \(2A'(t_2)<0\). Every such tangent is the velocity
of a smooth curve on the regular constraint manifold; that curve stays
in the fixed sign face near the minimum. The second-order necessary
condition contradicts (3). Thus the middle level has multiplicity one.

This argument justifies actual constrained curves. It does not infer
feasible perturbations from the formal multiplier equations alone.

## 2. Six complete ordered-level exclusions

Write the three multiplicities as \((m,1,k)\), so \(m+k=n-1\).
Balance makes the outer levels have opposite signs. Scaling by a
positive number gives levels
\[
                  -1,\quad m-kr,\quad r,
\]
where the strict ordering and nonzero support require
\[
       \frac m{k+1}<r<\frac{m+1}{k},\qquad r\ne\frac mk.           \tag{4}
\]
The positive outer block alone has \(k\) coordinates, so \(1\le k\le3\).
If the middle level is positive it imposes the further restriction
\(k+1\le3\); excluding the larger intervals (4) is sufficient.
The third moment becomes
\[
                 B_{m,k}(r)=-m+(m-kr)^3+kr^3=0.                 \tag{5}
\]
For \(n\in\{7,8\}\), \(k\in\{1,2,3\}\), and \(m=n-1-k\), the following
six rows are exhaustive. No numerical search is involved.

| \(n\) | \((m,k)\) | Interval for \(r\) | Complete polynomial \(B_{m,k}(r)\) |
|---|---|---|---|
| 7 | (5,1) | (5/2,6) | \(15(r^2-5r+8)\) |
| 7 | (4,2) | (4/3,5/2) | \(-6(r^3-8r^2+16r-10)\) |
| 7 | (3,3) | (3/4,4/3) | \(-3(r-1)(8r^2-19r+8)\) |
| 8 | (6,1) | (3,7) | \(18(r-3)^2+48\) |
| 8 | (5,2) | (5/3,3) | \(-6(r^3-10r^2+25r-20)\) |
| 8 | (4,3) | (1,5/3) | \(-12(r-1)^2(2r-5)\) |

Here are complete exact sign certificates for these intervals:

1. \(r^2-5r+8=(r-5/2)^2+7/4>0\).
2. For \(F=r^3-8r^2+16r-10\),
   \(F'=3(r-4/3)(r-4)<0\) on the indicated open interval, and
   \(F(4/3)=-14/27<0\). Thus \(B_{4,2}>0\).
3. The quadratic \(Q=8r^2-19r+8\) is convex and has endpoint values
   \(Q(3/4)=-7/4\), \(Q(4/3)=-28/9\). It is strictly negative on the
   entire closed interval. Consequently (5) forces \(r=1\), but then
   the middle coordinate \(3-3r=0\), contradicting nonzero support \(n=7\).
4. The displayed square plus \(48\) is strictly positive everywhere.
5. For \(F=r^3-10r^2+25r-20\),
   \(F'=3(r-5/3)(r-5)<0\) on the indicated interval, and
   \(F(5/3)=-40/27<0\). Thus \(B_{5,2}>0\).
6. On \(1<r<5/3\), the factor \((r-1)^2\) is positive and \(2r-5<0\).
   Therefore \(B_{4,3}>0\). The root at \(r=1\) is an excluded endpoint.

There is no possible fourth-moment minimum with seven or eight nonzero
coordinates. The six-coordinate Cauchy argument proves the lemma. Any
profile attaining \(X=1/6\) is itself a global minimum and obeys the
same support classification, so the equality orbit is exhaustive.

## 3. Full spectral masses and the angular bound

Partition the coordinates into their \(r\) actual equal-value blocks.
The within-block difference spaces have total dimension \(8-r\).
They are invariant eigenspaces of \(H\), orthogonal to \(e\) and to \(w\).
The orthogonal block-constant space meets \(e^\perp\) in dimension \(r-1\),
is invariant under \(H\), and contains \(w\). The actual full spectral
mass therefore lives on at most \(r-1\) distinct eigenspaces, even if
eigenvalues coincide with inactive block modes. The spectral theorem gives
\[
       \sum_\lambda\rho_\lambda=8\|w\|^2=1,\qquad
       \eta\ge\frac1{r-1}.                                      \tag{6}
\]
This rederives the needed active-mass fact from [7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md).
It never treats separate basis vectors in a repeated eigenspace as
separate masses.

The moment lemma gives \(D=X-1/8\ge1/24\). Combining with (6),
\[
             C\le\frac{24(r-2)}{r-1}\le\frac{144}{7}.              \tag{7}
\]
Equality in the last value would force \(r=8\) and \(X=1/6\), whereas
every moment-equality profile has \(r=3\). Thus the last inequality is
strict. A balanced nonzero vector has both signs; if its minimum sign
count is greater than three, eight coordinates force \(p=q=4\).
This proves the stated angular corollary, including its endpoint.

For a direct equality check set \(v=(1,1,1,-1,-1,-1,0,0)\) and use the
unnormalized rational ambient compression \(H_v=P\operatorname{diag}(v)P\).
The characteristic polynomial on \(e^\perp\) is
\[
             z(z^2-1)^2(z^2-1/4).
\]
This follows by differentiating \(\prod_i(z-v_i)=z^2(z^2-1)^3\) and dividing
by eight, or by a block decomposition. On the full ambient space one
also has the zero eigenvector \(e\). The full projection masses
\(\|\Pi_\lambda v\|^2\) are \(3\) at each of \(\lambda=\pm1/2\), and zero
at \(\lambda=-1,0,1\). After normalizing by \(\|v\|^2=6\),
\(\eta=1/2\), \(D=1/24\), and \(C=12\). The checker verifies every full
rational projector, including the ambient zero eigenspace, directly.

## 4. Evidence and scope

[verify.py](verify.py) uses Python 3.11+ standard-library Fraction arithmetic.
It expands all six polynomials in (5), verifies their full factor and
square identities, derivative factors, endpoint values and interval
sign conditions, and checks the complete multiplicity list. It verifies
the equality moments and the entire five-projector decomposition of the
ambient eight-by-eight matrix, including idempotence, orthogonality,
eigenvalue equations, ranks, full masses and normalization. Every exact
record is compared with [expected.json](expected.json), rejecting altered,
missing, extra and type-changed records. The optional
[compare_cas.py](compare_cas.py) uses SymPy 1.14.0 with dense symbolic
polynomials and matrices to reconstruct the entire same record by a
different arithmetic representation. Both are same-author checks,
**not independent review or formalization**.

Run `python3 -B verify.py` and `python3 -B -O verify.py`; optional CAS:
`python3 -B compare_cas.py`. Exact commands and evidence provenance are in
[README.md](README.md). Compactness, the regular-face implicit function
theorem, Lagrange multipliers, constrained second variation and the spectral
transfer are ordinary written mathematics outside the code's trust boundary.

The previous sign-count leaf [8851](../sign-count-angular-reduction/PROOF.md)
has \(X\ge13/84\) without an odd-moment condition and gives \(C<112/5\)
when \(r\le4\). This result adds the hypothesis \(\mu_3=0\) and sharpens
the moment barrier to \(1/6\), obtaining \(C<144/7\) for **all eight-level
profiles and all collisions**. Since \(144/7<49/2<c_3\), using the
previous benchmark [8753](../angular-three-level-transition/PROOF.md) if desired,
every profile competitive with that benchmark on the zero-third-moment
locus must have four coordinates of each sign.

No global angular maximum, sharp sign-sector angular value, effective
distance estimate, universal curvature sign, four-plus-four triple-root
symmetry theorem, or complex degree-nine first-power theorem is claimed.
In particular the last symmetry question remains open here.
