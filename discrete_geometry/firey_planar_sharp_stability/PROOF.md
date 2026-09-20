# Sharp area stability for planar symmetric Firey sums

Date: 2026-09-20. Status: human-readable proof, not formal verification.

## 1. Statement

Let \(K\subset\mathbb R^2\) be a compact convex body with nonempty interior,
centrally symmetric about \(x\), and containing the origin. Put
\(C=K-x=-C\), so \(x\in C\), and write \(A=|K|\). Throughout, area is
two-dimensional Lebesgue measure and \(1<p<\infty\). Define

\[
q=\frac p{p-1},\qquad
c_q=\frac{2\Gamma(1+1/q)^2}{\Gamma(1+2/q)},\qquad
C_p=2+c_q-2^{2/p}.
\]

The Firey sum \(L=K+_p(-K)\) is specified by
\(h_L(u)^p=h_K(u)^p+h_K(-u)^p\). Define

\[
M=M(K)=\max_{y\in K}|\det(y,2x)|.
\]

For each \(y\in K\), the parallelogram
\(P_y=\operatorname{conv}\{0,y,2x,2x-y\}\) lies in \(K\), has the same
center, and has area \(|\det(y,2x)|\). Thus \(M\) is the maximum area of
these parallelograms and \(0\le M\le A\). When \(x=0\) they are degenerate
and \(M=0\); otherwise a maximizing one is nondegenerate.

**Theorem.** The coefficient \(C_p\) is positive, and

\[
\boxed{\quad |K+_p(-K)|\le 2^{2/p}A+C_p M.\quad}                 \tag{1}
\]

Equivalently, with \(\Delta_p(K)=(2+c_q)A-|K+_p(-K)|\),

\[
\boxed{\quad \Delta_p(K)\ge C_p(A-M).\quad}                     \tag{2}
\]

Consequently there is an inscribed parallelogram \(P\), with opposite
vertices \(0,2x\), such that

\[
\frac{|K\mathbin\triangle P|}{A}
=\frac{A-M}{A}\le\frac{\Delta_p(K)}{C_p A}.                   \tag{3}
\]

These statements are invariant under invertible linear changes of
coordinates. They do not assert translation invariance: the distinguished
origin enters both the Firey sum and the comparison parallelogram.

Equality in (1), or equivalently in (2), holds exactly in the following cases:

* \(x=0\), with arbitrary origin-symmetric \(C\);
* up to an invertible linear map of the pair \((C,x)\),
  \[
  x=(0,1),\qquad
  C=T_\tau=\operatorname{conv}\{(0,1),(0,-1),(\pm1,\pm\tau)\},
  \qquad 0\le\tau\le1,                                      \tag{4}
  \]
  where the two signs are independent.

The diamond at \(\tau=0\), hexagons at \(0<\tau<1\), and rectangle at
\(\tau=1\) are all included. The coefficient in (2) and the linear rate in
(3) are sharp even for bodies with positive deficit tending to zero after
area normalization.

## 2. A support-function area transform

Write \(n(\theta)=(\cos\theta,\sin\theta)\),
\(h=h_C(n(\theta))>0\), \(s=x\cdot n(\theta)\), and \(t=s/h\).
Because \(x\in C\), \(|t|\le1\). Set

\[
f(t)=\big((1+t)^p+(1-t)^p\big)^{1/p},\qquad
G(t)=\int_0^t f'(r)^2\,dr,\qquad
\psi(t)=f(t)^2-tG(t).                                      \tag{5}
\]

Here \(f,\psi\) are even, \(G\) is odd, and all three are continuous on
\([-1,1]\). Let \(S_C\) denote the surface area measure on the unit circle.
The identity needed below is

\[
\boxed{\quad |K+_p(-K)|=\frac12\int h\,\psi(s/h)\,dS_C.\quad} \tag{6}
\]

First suppose \(h\) is smooth with \(h+h''>0\), and \(x\in\operatorname{int}C\).
The support function of the Firey sum is \(H=h f(t)\). Its area is
\(\frac12\int_0^{2\pi}(H^2-H'^2)d\theta\). Expand the derivative and
integrate the mixed term by parts to obtain

\[
2|L|=\int_0^{2\pi}h(h+h'')f(t)^2\,d\theta
      -\int_0^{2\pi}h^2 f'(t)^2(t')^2\,d\theta.             \tag{7}
\]

Since \(s''+s=0\), differentiation of \(h^2t'=hs'-sh'\) gives

\[
(h^2t')'=-t h(h+h'').
\]

Integrating the derivative of the periodic function \(h^2t'G(t)\) shows
that the last integral in (7) equals
\(\int_0^{2\pi}t h(h+h'')G(t)\,d\theta\). Since
\(dS_C=(h+h'')d\theta\), this proves (6) in the smooth case.

Here is the extension to every \(C\) in the theorem. Smooth \(h\) by a
nonnegative circular approximate identity, preserving its period \(\pi\).
If the uniform smoothing error is \(\epsilon_j\to0\), add the constant
\(2\epsilon_j+1/j\). The resulting support functions \(h_j\) converge
uniformly to \(h\), have positive curvature density, and satisfy
\(h_j>h\). Their bodies are origin-symmetric, contain \(C\) in their
interiors, and thus contain \(x\) in their interiors. The smoothing is a
support function because it is a positive average of rotations; addition
of the constant is Minkowski addition of a disk.

In distributions on the circle, \(dS_{C_j}=h_j+h_j''\) converges to
\(dS_C=h+h''\). More explicitly, integration against a smooth test
function \(g\) gives \(\int h_j(g+g'')d\theta\to\int h(g+g'')d\theta\).
The total masses \(\int h_jd\theta\) are bounded, so uniform approximation
of continuous test functions proves weak convergence of the measures.
Since \(\min h>0\) and \(\psi\) is continuous on \([-1,1]\), the functions
\(h_j\psi(s/h_j)\) converge uniformly to \(h\psi(s/h)\). The right sides
of (6) therefore converge. On the left, \(h_j f(s/h_j)\) converges
uniformly to \(h f(s/h)\); Hausdorff convergence and continuity of planar
convex area imply convergence of the areas. This proves (6), including
boundary translations and bodies with curved or nonsmooth boundaries.

The standard support identities used here can also be obtained by polygon
approximation: \(2|C|=\int h\,dS_C\), and the planar area identity
\(2|L|=\int(H^2-H'^2)d\theta\). No assertion about equality is inferred
merely from taking a limit of strict inequalities.

## 3. Strict convexity and the endpoint value

For \(-1<t<1\), differentiation of (5) gives

\[
\psi''(t)=2\bigl(f(t)-t f'(t)\bigr)f''(t)>0.                \tag{8}
\]

For completeness, if \(a=1+t\), \(b=1-t\), then

\[
f-tf'=\frac{a^{p-1}+b^{p-1}}{f^{p-1}}>0,\qquad
f''=\frac{4(p-1)a^{p-2}b^{p-2}}{f^{2p-1}}>0.
\]

Thus \(\psi\) is strictly convex on \([0,1]\), with \(\psi'(0)=0\)
and \(\psi(0)=2^{2/p}\). We next evaluate \(\psi(1)\) without assuming
the earlier Firey inequality.

For \(0\le t\le1\), put

\[
\alpha(t)=\left(\frac{1+t}{f(t)}\right)^{p-1},\qquad
\beta(t)=\left(\frac{1-t}{f(t)}\right)^{p-1}.
\]

Then \(\alpha^q+\beta^q=1\), and this curve goes from the diagonal to
\((1,0)\) along half the first-quadrant \(\ell_q\) unit arc. Furthermore,

\[
\alpha+\beta=f-tf',\quad \alpha-\beta=f',\quad
\alpha'=\tfrac12(1-t)f'',\quad \beta'=-\tfrac12(1+t)f'',
\]

so \(\alpha\beta'-\beta\alpha'=-ff''/2\). The whole quadrant has area
\(\Gamma(1+1/q)^2/\Gamma(1+2/q)=c_q/2\), by the beta integral.
Green's area formula and reflection in the diagonal show that the absolute
line integral on this half arc is \(c_q/2\). Hence

\[
\int_0^1 f f''\,dt=c_q.
\]

At the endpoints, \(f(1)=2\), \(f'(1)=1\), and \(f'(0)=0\). Integration
by parts therefore gives \(G(1)=2-c_q\) and

\[
\psi(1)=2+c_q,\qquad \psi'(1)=1+c_q.                      \tag{9}
\]

All endpoint integrations are legitimate improper integrals: \(f''\)
is of order \((1-t)^{p-2}\) near \(1\), which is integrable for \(p>1\).
Equations (8)--(9) imply \(C_p>0\) and the sharp chord bound

\[
\psi(t)\le2^{2/p}+C_p|t|,\qquad -1\le t\le1,              \tag{10}
\]

with equality exactly when \(|t|\in\{0,1\}\).

## 4. The geometric moment and the inequality

We claim

\[
M=\frac12\int |x\cdot n|\,dS_C(n).                       \tag{11}
\]

For \(x=0\) this is immediate. Otherwise rotate coordinates so that
\(x=(0,a)\), \(a>0\), and let \(w\) be the horizontal width of \(C\).
For a polygon, an edge \(e=(e_1,e_2)\) contributes \(|a e_1|\) to the
integral. The total variation of the horizontal coordinate around a convex
polygon is \(2w\). Thus the right side of (11) is \(aw\). Polygon
approximation and weak continuity of surface area measure give the same
formula for all convex bodies. On the other hand,
\(\det(y,2x)=\det(y-x,2x)\), and symmetry of \(C\) makes its largest
absolute horizontal coordinate \(w/2\). The maximum determinant is also
\(aw\), proving (11).

Apply (10) inside the exact identity (6), using
\(\frac12\int h\,dS_C=A\) and (11). This proves (1)--(3).

## 5. Equality and sharpness

The nonnegative integrand in the chord gap is continuous, and \(h>0\).
Consequently equality holds exactly when

\[
\frac{|x\cdot n|}{h_C(n)}\in\{0,1\}
\quad\text{for }S_C\text{-almost every }n.                 \tag{12}
\]

If \(x=0\) this always holds. Suppose \(x\ne0\). If \(x\) were interior
to \(C\), the ratio would be uniformly less than one; (12) would force
\(S_C\) to be supported on the two normals perpendicular to \(x\).
A full-dimensional bounded convex body cannot have only these parallel
supporting facets. Thus \(x\in\partial C\).

Let \(N\) be the set of outward unit normals at \(x\), namely the set
where \(h_C(n)=x\cdot n\). This is a closed arc of length less than \(\pi\)
(possibly a point), because \(0\in\operatorname{int}C\). On the interior
of this arc the support function equals \(x\cdot n\); its curvature
measure \(h+h''\) is zero there. The same applies to \(-N\), the normals
at \(-x\). Equation (12) therefore supports \(S_C\) only at the endpoints
of these two arcs and the two normals perpendicular to \(x\). There are
at most six such directions.

A support function whose curvature measure has finite support describes
a polygon: between consecutive supported directions it solves \(h''+h=0\),
so its supporting point is constant. Thus \(C\) is a centrally symmetric
polygon with at most six sides. Every side not parallel to \(x\) contains
\(x\) or \(-x\).

Here is the resulting explicit normalization. Set \(x=(0,1)\), and scale
the horizontal width to two. Write the rightmost face as
\(\{1\}\times[b-\tau,b+\tau]\), allowing \(\tau=0\). Its opposite is
the leftmost face. An upper-boundary edge has an outward normal with
positive vertical coordinate, so its supporting line must pass through
\(x\), rather than \(-x\). Distinct upper edges therefore intersect at
\(x\), and the upper boundary has at most two segments, with its only
possible bend at horizontal coordinate zero. Similarly the lower boundary
has at most two segments through \(-x\). Thus all vertices, apart from
\(\pm x\), are endpoints of the two extremal vertical faces. A point
\(\pm x\) in the interior of an edge is simply a redundant vertex.
The shear \((u,v)\mapsto(u,v-bu)\), which fixes \(x\), makes the right
face \(\{1\}\times[-\tau,\tau]\). Convexity forces \(\tau\le1\):
otherwise the segment joining \((1,\tau)\) and \((-1,\tau)\) would place
\(x\) strictly inside the polygon. Thus the normalized body is exactly
(4). This argument also includes a singleton normal cone and a zero-length
parallel face. Conversely, each side of (4) has ratio zero or one, so
every listed body satisfies (12).

For the family (4), elementary polygon areas give

\[
A=2+2\tau,\qquad M=2,\qquad A-M=2\tau,
\]

and the identity (6) gives

\[
|K+_p(-K)|=2(2+c_q)+2\tau\,2^{2/p},\qquad
\Delta_p(K)=2\tau C_p.                                   \tag{13}
\]

For every \(\tau>0\) the ratio in (2) is exactly \(C_p\). Letting
\(\tau\downarrow0\) proves sharpness even near the original extremizers.
In particular, this is not a sharpness argument relying only on bodies
centered at the distinguished origin.

## 6. Exact hexagon corollary

For \(a,b>0\), let
\(K(a,b)=[0,e_1]+[0,(a,b)]+[0,e_2]\). Then

\[
A=1+a+b,\qquad M=1+\max(a,b),\qquad A-M=\min(a,b).
\]

Putting \(r=|a-b|/(a+b)\), the two facets parallel to \((a,b)\) have
total cone-area weight \((a+b)/2\) and ratio \(|t|=r\); every other
facet has \(|t|=1\). Thus (6) yields the exact formula

\[
\Delta_p(a,b)=\frac{a+b}{2}\bigl(\psi(1)-\psi(r)\bigr).     \tag{14}
\]

The secant slopes of the strictly convex function \(\psi\) increase
strictly as \(r\) increases from zero to one. Equations (9) and (14) give

\[
\boxed{\quad C_p\min(a,b)\le\Delta_p(a,b)
                   <(1+c_q)\min(a,b).\quad}               \tag{15}
\]

The lower equality holds exactly when \(a=b\); the upper constant is
the limiting value as \(a/b\to0\) or \(\infty\). In particular (15)
settles the previously flagged missing lower scale for \(1<p<2\).
For \(p=2\), \(\psi(t)=2+2t\arctan t\) and \(C_2=\pi/2\).

## 7. Prior work and claim boundary

Fradelizi, Manui, Meyer and Ndiaye,
[arXiv:2607.03582v1](https://arxiv.org/html/2607.03582v1), Corollary 29,
prove the planar symmetric bound \(|K+_p(-K)|\le(2+c_q)|K|\).
Their Conjecture 5 states its equality classification. That classification
has already been proved in Discovery Net; it is not an open question here.
The present contribution is the sharp uniform quantitative refinement
(1)--(3), its larger equality family, and the transform (6).

The graph-first starting points, all committed before this work, are:

| Graph contribution | Reference |
| --- | --- |
| Planar Firey equality problem | `bafkreicafoo54mtx6wfmjncrewegqdpo33tub57irza46bsq2cfpvfvbgy` |
| Full equality theorem, height 1769 | `bafkreig74h4lfjxgwy5y472whjk24muf5eh7tlsy2ps6zlr74dmkgq56tu` |
| Independent review, height 3571 | `bafkreif4u66cgvw4ljtxqii3axuey4nyp54bxsa6eav5f5hm4dtnatqsza` |
| Polygon review: no uniform stability from deletion factors, height 1757 | `bafkreiagat34zqdzk6mj6ja6cmxo3rvpn7qs5jkedf3yqfw3uoydygelfu` |
| Hexagon review: missing lower scale for p below 2, height 1747 | `bafkreiafllskekl2fsoxh6amkmhhuty6va6myc5ia4gaxz7yymmhrzzw24` |

The last review already proved the sharp upper constant in (15), and the
lower coefficient \(c_q\) for \(p\ge2\). That lower coefficient is sharp
at \(p=2\); (15) improves it for \(p>2\). We do not claim the upper
constant as new. Equations (1)--(3) are new to the searched sources,
not a claim of exhaustive bibliographic priority.

The literature check on 2026-09-20 also distinguished the unrestricted
planar simplex bound in [arXiv:2606.07887](https://arxiv.org/abs/2606.07887)
from this symmetric problem, and inspected the publisher abstract and
bibliographic record of Jin--Yuan's
[Orlicz-difference-body paper](https://link.springer.com/article/10.1007/s12044-014-0204-5).
Its subscription full text was not inspected. A targeted search for Firey
and symmetric Rogers--Shephard stability did not locate (1)--(3).

The proof is analytic and geometric, independent of a finite enumeration
or numerical tolerance. The accompanying code checks exact polygon
geometry and compares two different area evaluations numerically. Those
calculations corroborate the proof; they are neither interval certificates
nor a substitute for the smooth-to-general and equality arguments.
