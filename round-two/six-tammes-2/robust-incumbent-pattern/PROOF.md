# A contact-based neighborhood of the asymmetric Tammes-15 incumbent

Actual author **six-tammes-2**, role **researcher**, 2026-10-01.
Status: proved conditional stability and exclusion lemma, author checked;
independent review and formalization pending.

Put

\[
 I=[14/25,593/1000],\quad e_*=10^{-13},\quad
 F(t)=13t^5-t^4+6t^3+2t^2-3t-1.
\]

Let tau be the unique root of F in I, with the published rational bracket
`0.59260590292507377809642492233275 < tau <
0.59260590292507377809642492233276`.
This is the known incumbent cosine; its construction is prior work.

The graph G has all edges of the two anchor triangles `(0,5,11)` and
`(1,2,4)`. Each following `(new,a,b,old)` tuple adds the two edges
`new-a,new-b`:

```text
A: (6,0,11,5) (7,0,5,11) (9,5,11,0) (14,0,6,11)
B: (3,1,4,2) (8,2,4,1) (10,1,2,4) (12,1,10,2) (13,2,8,4).
```

Add the four cross edges `6-8,7-12,9-10,9-13`. This gives 28 edges on
all fifteen labels: the asymmetric incumbent's contact graph with edges
`3-7` and `3-14` removed. Every old triangle needed by a tuple is present.

**Stability theorem.** Let fifteen distinct unit vectors q_i satisfy all
pairwise inner products at most t, where t is in I. If, for some
`0 <= e <= e_*`, every edge of G has inner product in `[t-e,t]`, then

\[
 |t-\tau|\le30000e.
\]

There is a labeled exact asymmetric incumbent p_i, obtained from the
published one by an orthogonal transformation, such that

\[
 \max_i\|q_i-p_i\|\le2000000e.
\]

After a further rotation imposing the published local certificate's gauge
`q_0=p_0, q_5 in span(p_0,p_5)`, this distance is at most `20000000e`.
Consequently **t >= tau**. If `t <= tau`, necessarily `t=tau` and the
configuration is exactly the asymmetric incumbent, up to O(3).

**Strict-improvement consequence.** Every fifteen-point packing strictly
better than the incumbent, and every labeling of its points by G, has a
prescribed edge with inner product **strictly below `t-10^-13`**, where t
is that packing's actual largest pairwise inner product. No graph
completeness, face, convexity, symmetry, irreducibility, or prior proximity
assumption is used. This does not assert occurrence of G and supplies no
new global numerical bound or global optimality proof.

## 1. Approximate triangles and block alignment

We use the following elementary estimates from
[the near-contact eight-core proof, Sections 1–2](../robust-eight-core/PROOF.md).
They hold for the larger range `0 <= e <= 1/10000` on I; the present
proof needs no cap-covering result from that contribution.

An approximate equilateral unit triangle can be compared with an exact one
of common inner product t. Keeping its first point fixed and its second
point's tangent direction fixed gives errors at most `(0,2e,17e)`.
For clarity, write the approximate triangle's inner products as
`s,alpha,z in [t-e,t]`. In orthonormal axes its third point has coordinates

\[
 (\alpha,\beta,\gamma),\quad
 \beta=(z-s\alpha)/\sqrt{1-s^2}.
\]

The exact third point has coordinates
`(t,beta_0,gamma_0)`, with
`beta_0=(t-t^2)/sqrt(1-t^2)` and positive `gamma_0`.
Choose the third axis so that gamma is positive. The elementary derivative
bounds `|d sqrt(1-s^2)/ds| <= 1` and
`|d (1-s^2)^(-1/2)/ds| <= 2`, together with both normal coordinates
above 1/2, give
`|alpha-t| <= e, |beta-beta_0| <= 7e, |gamma-gamma_0| <= 9e`.
This proves the stated alignment, including both possible orientations.

The needed approximate reflection estimate is as follows. For four distinct
original unit points a,b,c,n, if
`a.b,a.c,b.c,a.n,b.n in [t-e,t]` and `c.n <= t`, then

\[
 \|n-[r(a+b)-c]\|\le20e,\qquad r=2t/(1+t)<1. \tag{1}
\]

Here is the branch argument. In axes proportional to a+b,a-b and a normal,
write each of c,n as `(A,B,C)`. The hypotheses imply
`|A| <= 3/4, |B| <= 2e, |C| > 1/2`; the corresponding differences of
A, B and absolute normal amplitudes are bounded by `2e,4e,4e`.
Equal normal signs would give `|n-c| <= 10e`, contrary to packing, which
requires `|n-c| > 4/5`. Thus the signs are opposite, and n is within
10e of the reflection of c across span(a,b). The difference between that
reflection and `r(a+b)-c` has axial and transverse components each at most
4e. Their sum proves (1). The checker's rational scalar inequalities
verify these constants; the coordinate and branch implications are this
written proof, not a formalization.

Apply the triangle alignment separately to the A and B anchor triples,
then build **exact** comparison blocks A_i and B_j using their listed
reflections. Each comparison point is unit; actual and comparison points
are in the same ambient R3. If `|q_i-P_i| <= K_i e`, (1) gives the error
recurrence `K_new=20+K_a+K_b+K_old`. Its values are

| Label | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| K | 0 | 0 | 2 | 39 | 17 | 2 | 39 | 39 | 39 | 39 | 39 | 17 | 61 | 78 | 76 |

In particular every error is below 80e. Every prescribed cross dot product
therefore differs from t by at most `e+80e+80e=161e`. Set `delta=161e`.

## 2. Selecting the common-neighbor reflection without proximity

Put `U=A_6, W=A_7, V_A=A_9`. The exact block identities give

\[
 U\cdot W=U\cdot V_A=W\cdot V_A=\kappa,
 \qquad \kappa=\frac{t(9t^2-2t-3)}{(1+t)^2}.
\]

In the B block, both `B_10` and `B_13` have inner product t with `B_2`.
Write

\[
 w=B_{10}\cdot B_{13}
   =\frac{16t^4-7t^3-5t^2+3t+1}{(1+t)^3},\quad
 c=\frac{t}{1+w}(B_{10}+B_{13}),\quad V_*=2c-B_2.
\]

The exact interval certificate proves

\[
 1/3\le w\le2/5,\qquad
 h^2:=1-2t^2/(1+w)\ge49/100.
\]

Hence B_2 and V_* are exactly the two unit common neighbors, with normal
amplitudes at least 7/10. The cross contacts `9-10,9-13` imply that each
of V_A's two dot constraints differs from t by at most delta.
The Gram matrix of `B_10,B_13` has least eigenvalue at least 3/5.
Thus V_A's projection onto their span differs from c by at most `2 delta`.
Here `|c|^2 <= 51/100 < (3/4)^2` and
`3/4+2 delta < 4/5`, so V_A's normal amplitude is above 3/5.
Rationalizing the unit equations bounds the difference of the absolute
normal amplitudes by `4 delta`. Therefore V_A is within `6 delta` of
one of B_2,V_*.

The B_2 branch is impossible. Actual q_9,q_2 have distance above 9/10,
whereas their comparison errors are 39e and 2e. Hence
`|V_A-B_2| > 9/10-41e > 4/5`, while `6 delta < 4/5`.
It follows, with no prior orientation or proximity choice, that

\[
 \boxed{\|V_A-V_*\|\le1000e.} \tag{2}
\]

## 3. Two complete orientations and an approximate linear system

Define

\[
 \gamma=\kappa/(1+\kappa),\qquad
 q=\sqrt{1+2\kappa}/(1+\kappa).
\]

The certificate proves `-3/10 <= kappa <= -1/5`, `|gamma| <= 1/2`
and `0<q<1`. The exact equilateral triple U,W,V_A consequently gives

\[
 W=\gamma(U+V_A)+\lambda(V_A\times U),\qquad \lambda\in\{-q,q\}. \tag{3}
\]

Both signs are retained. Replacing V_A by V_* in (3) changes W by at most
`(|gamma|+q)|V_A-V_*| <= 2000e`. Define

\[
 C=\gamma B_{12}+\lambda(B_{12}\times V_*),\quad
 h=t-\gamma V_*\cdot B_{12}.
\]

The remaining cross constraints `6-8,7-12`, (2), and
`U.V_A=kappa` give

\[
 U\cdot(V_*,B_8,C)=(\kappa,t,h)+z,
 \qquad \|z\|_\infty\le2161e. \tag{4}
\]

In detail the errors of its three entries are at most `1000e,161e,2161e`.
The last equality follows by the scalar triple-product identity
`(V_* cross U).B_12=U.(B_12 cross V_*)`.

Let Q be the matrix of the exact B anchors, so `Q^T Q=H=(1-t)I+tJ`.
Use coefficient vectors relative to Q. The construction is fully explicit
in [models.py](models.py). In particular

\[
 \mu_0=\frac{(t-1)(t+1)(2t+1)(3t-1)}{9t^3-t^2-t+1},\qquad
 \mu_0^2=\det(H)q^2.
\]

Absorbing Q's orientation and the sign of lambda gives exactly the two
coefficient branches `mu=+mu_0` and `mu=-mu_0`; neither is lost.
The linear system's coefficient matrix X has rows consisting of H times
the coefficient vectors of V_*,B_8,C. On each branch the certificate
proves invertibility and `||X^-1||_infinity <= 5` throughout I.
Let U_t be the exact, possibly nonunit, solution with z=0 in (4).
Since every Q-column is unit, coefficient errors of at most `5*2161e`
give

\[
 \|U-U_t\|\le40000e. \tag{5}
\]

## 4. Quantitative algebraic obstruction and the separation parameter

Let G_sigma be the Gram matrix of V_*,B_8,C in the selected branch,
and let D_sigma be its augmented four-by-four Gram determinant with
last column and row `(kappa,t,h,1)`. Exact linear algebra gives

\[
 D_\sigma=\det(G_\sigma)(1-\|U_t\|^2). \tag{6}
\]

Both Gram determinants are positive and at most one throughout I.
The actual U is unit, and `40000e < 1`, so (5) implies

\[
 |D_\sigma|\le120000e. \tag{7}
\]

The original exact core classification
[CONTACT_CORE.md](../../../tammes15_contact_pattern_obstruction/CONTACT_CORE.md)
derives the two determinant factorizations. The current checker replays
that proof's exact identities and existence checks, reconstructs the
determinants, and proves the following **new quantitative enclosures**:

\[
 D_{-1}(t)\ge1/10,\qquad
 D_{+1}(t)=J(t)F(t),\quad J(t)\le-2/5,
 \qquad F'(t)\ge10. \tag{8}
\]

These enclosures hold on the complete closed interval I. In particular
`120000e < 1/10` excludes the minus orientation. For the plus branch,
(7)–(8) and the mean value theorem give

\[
 |F(t)|\le300000e,\qquad \boxed{|t-\tau|\le30000e.} \tag{9}
\]

This approximate argument removes a distant wrong orientation before
invoking the local theorem. It does not infer a branch from a rounded
root or assume a configuration near the incumbent.

## 5. Recovering all fifteen points

In the surviving branch, define W_t by (3) with U_t,V_*.
The actual U,V_A are unit, as is V_*. The bilinearity of the cross product
and (2),(5) give

\[
 \|W-W_t\|\le(|\gamma|+q)(40000+1000)e<64000e. \tag{10}
\]

The three original A anchors are recovered from columns U,W,V_A by the
inverse of

\[
 R=\begin{pmatrix}r&r&-1\\-1&r&r\\r&-1&r\end{pmatrix},\qquad
 r=2t/(1+t).
\]

The certificate proves each column sum of absolute values in R^-1 is
at most three, and every A coefficient vector has sum of absolute values
at most three. Therefore the rational comparison model S_i(t), recovered
from U_t,W_t,V_* and the B block, satisfies

\[
 \max_i\|q_i-Q(t)s_i(t)\|\le
 (80+3\cdot3\cdot64000)e<600000e. \tag{11}
\]

At tau this comparison model has the known incumbent's full labeled Gram
matrix. The checker verifies its unit norms, all thirty contacts, and the
circulant cross Gram matrix modulo F. The exact core uniqueness and the
pinned local existence certificate give the same identification independently.

Keep fixed the orthonormal frame used for the B anchor alignment, and let
Q(t) vary along the exact equilateral-anchor path in that frame. Its first
column is fixed; its other columns have derivative norms at most six on I.
For its third column, the nontrivial coordinates are

\[
 \beta(t)=(t-t^2)/\sqrt{1-t^2},\quad
 \gamma_B(t)=\sqrt{1-t^2-\beta(t)^2}.
\]

Here `beta <= 5/16`, `|beta'| < 1`, `gamma_B > 1/2`, and
`|gamma_B'| < 2`, proving even a derivative bound of four.
The rational certificate proves, uniformly for all fifteen labels,

\[
 \|s_i(t)\|_1\le3,\qquad \|s'_i(t)\|_1\le18.
\]

Consequently

\[
 \|Q(t)s_i(t)-Q(\tau)s_i(\tau)\|
 \le(18+6\cdot3)|t-\tau|=36|t-\tau|.
\]

Combining (9),(11), and writing `p_i=Q(tau)s_i(tau)`, gives

\[
 \max_i\|q_i-p_i\|\le(600000+36\cdot30000)e<2000000e. \tag{12}
\]

## 6. Rotation gauge and the strict-improvement exclusion

Set `D=max_i |q_i-p_i|`. A plane rotation aligning q_0 with p_0 has
operator norm distance from identity at most D. After that rotation all
point errors are at most 2D. The tangent projections of q_5 and p_5 onto
p_0's perpendicular plane then differ by at most 2D, while the latter
has norm `sqrt(1-tau^2)>4/5`. Their normalized directions differ by
at most `4D/(4/5)=5D`. A rotation about p_0 aligning those directions
moves every unit point by at most 5D. The combined error is at most
`7D <= 10D`; it imposes exactly `q_0=p_0` and
`q_5 in span(p_0,p_5)`.

By (12) and `e <= 10^-13`, the gauged distance is at most
`20000000e <= 1/400000`. The pinned
[local stress theorem](../../../tammes15_exact_local_certificate/README.md)
therefore yields, for `eta=max_{i<j} q_i.q_j-tau`,

\[
 \eta\ge D_{\rm gauged}/37332\ge0.
\]

Since eta is at most t-tau, this proves `t>=tau`. If `t<=tau`, the
same inequality forces the gauged distance to be zero, the entire packing
to equal the incumbent, and `t=tau`.

Any actual strict improvement lies in I: deleting one of its points and
using the published N14 optimum gives cosine at least sigma, the positive
root of `4x^4-2x^3+3x^2-1`. This root exceeds 14/25 because the quartic
is negative there and its derivative `x(16x^2-6x+6)` is positive for x>0.
The incumbent comparison gives `t<tau<593/1000`. Thus the consequence
stated at the beginning covers the whole strict-improvement range.

## 7. Exact verification, independence, and limitations

[check.py](check.py) pins eight public prerequisite files by SHA-256,
replays the complete 24-contact algebraic core and local stress checks,
derives the new rational functions from the graph, and compares them with
[model-functions.json](model-functions.json). It checks the inverse,
orientation, augmented determinant and root identification identities.
Exact Bernstein enclosures on four subintervals certify every bound above,
including each relevant denominator sign. Endpoints are retained.

[audit.py](audit.py) imports no production arithmetic or prerequisite code.
It uses ordinary rational polynomial operations and centered Taylor interval
enclosures, rather than Bernstein enclosures, to audit the new rational
inequalities, all 45 model derivatives and the error constants. The model
table's derivation is checked by the primary checker; the audit deliberately
does not claim a separate derivation of the earlier core or local stress.
The handwritten geometric bridges remain unformalized.

No floating-point number, optimizer, solver status, network access, external
coordinate table, or unpublished input enters verification. The bound is
conditional on this specific graph. Absence of it does not constrain all
possible better packings, so current global bounds remain unchanged.

Primary literature for the packing is
[Kottwitz (1991)](https://doi.org/10.1107/S0108767390011370), the
[Buddenhagen–Kottwitz exact construction, Section 4](https://web.archive.org/web/20210507001707/http://www.buddenbooks.com/jb/pack/sphere/toggles7.pdf),
and [Cohn's current table](https://spherical-codes.org/) with its
[coordinate file](https://spherical-codes.org/data/3/15). Their exact
incumbent and polynomial are prior results. The
[Musin–Tarasov paper](https://arxiv.org/abs/1410.2536) proves the N14 optimum.
The present contribution is the explicit contact-tolerance entry into the
existing local exclusion, without assuming coordinate proximity. The
separate exact 28-contact spanning corollary and local stress certificate
are published campaign prerequisites, not new claims here.
