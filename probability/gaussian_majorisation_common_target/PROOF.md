# Full Gaussian majorisation by a common-target convex decomposition

Author proof, 26 September 2026. Independent review and formalization are
pending. The result compares every hinge at every Gaussian variance for
the class below. The general dimension-three conjecture remains open.

## 1. The class and conclusion

Write

\[
 u_0=(1,1,1),\quad u_1=(1,-1,-1),\quad
 u_2=(-1,1,-1),\quad u_3=(-1,-1,1),\qquad
 P_h=h\operatorname{conv}\{u_0,u_1,u_2,u_3\},\quad h>0.
 \tag{1}
\]

Let \(\mathcal V\) be the twelve vectors with two coordinates in
\(\{-1,1\}\) and the remaining coordinate zero. Put
\(\mathcal Y=\{\pm e_1,\pm e_2,\pm e_3\}\). If \(v_k=0\) and
\(\{i,j,k\}=\{1,2,3\}\), define

\[
 S(v)=v_i v_j e_k.
 \tag{2}
\]

On the domain consisting of \(P_h\) and the rays \(rv\),
\(v\in\mathcal V\), \(2h\le r\le L<\infty\), let \(S\) fix the
core and send \(rv\) to \(rS(v)\). This is a contraction, as verified
in Section 3, and it has a global 1-Lipschitz extension.

Choose any probability law \(\rho\) on the solid core \(P_h\), any
probability law \(\eta\) on \([2h,L]\), any \(0\le\alpha\le1\), and
measurable ray weights \(p_v(r)\ge0\) with \(\sum_v p_v(r)=1\).
Set

\[
 \mu=(1-\alpha)\rho+
       \alpha\int\sum_{v\in\mathcal V}p_v(r)\delta_{rv}\,d\eta(r),
 \qquad \nu=S_\#\mu.
 \tag{3}
\]

Let \(\gamma_s\) have covariance \(sI_3\), and let
\(H_f(a)=\int_{\mathbb R^3}(f-a)_+\,dx\).

**Theorem A.** Suppose, for \(\eta\)-almost every \(r\),

\[
 \boxed{\quad\sum_{v\in\mathcal V}\left|p_v(r)-\frac1{12}\right|
                  \le\frac1{72}.\quad}
 \tag{4}
\]

Then

\[
 \boxed{\quad H_{\mu*\gamma_s}(a)\le H_{\nu*\gamma_s}(a)
          \quad\hbox{for every }s>0\hbox{ and every }a>0.\quad}
 \tag{5}
\]

This is full majorisation, hence comparison of all convex internal
energies for which the integrals are defined. The background law and its
mass are arbitrary. The radial law may be discrete or continuous, and
the twelve weights may vary measurably with radius. Condition (4) has
nonempty interior in the full eleven-dimensional probability simplex;
it imposes no equality between opposite-ray weights. The constant is a
convenient sufficient bound, not an optimal one.

In particular (5) holds for uniform weights \(p_v=1/12\). At a single
radius \(r=2h\), this contains the entire uniform-flap family with an
arbitrary solid tetrahedron background in the team's
[eventual-variance theorem](../gaussian_majorisation_eventual_endpoint/PROOF.md),
now **without its lower bound on the variance**. The support-level
Kneser--Poulsen comparison was already proved by the team's
[fixed-core theorem](../gaussian_majorisation_fixed_core/PROOF.md).
No new ball-volume consequence is claimed here.

We prove the uniform case first; it requires only three explicit
probability laws. Section 5 proves the open neighborhood (4) by a small
nonnegative-flow construction.

## 2. The functional bridge

**Common-target lemma.** Let \(\mu=\sum_i c_i\mu_i\), where the
\(\mu_i\) are probability measures, \(c_i\ge0\), and \(\sum_i c_i=1\).
If, for one fixed \(s>0\), every \(\mu_i*\gamma_s\) is majorised by
the **same** density \(\nu*\gamma_s\), then so is \(\mu*\gamma_s\).

Indeed convolution is linear, and pointwise convexity gives

\[
 \left(\sum_i c_i(\mu_i*\gamma_s)-a\right)_+
       \le\sum_i c_i(\mu_i*\gamma_s-a)_+.
 \tag{6}
\]

Integrate, then compare each term to \(H_{\nu*\gamma_s}(a)\).
All hinge integrals are finite, at most one. This elementary convexity
fact is not a new general theorem about majorisation. The new work is
constructing source laws with a common output in the present geometry.
Different output laws would not justify the last step in this argument.

We also recall and prove the planar-fibre principle used in the
fixed-core theorem. If a contraction \(R\) on a bounded subset of
\(\mathbb R^3\) preserves coordinate \(i\), then

\[
 \xi*\gamma_s\preceq(R_\#\xi)*\gamma_s
 \quad\hbox{for every probability law }\xi\hbox{ on that subset}.
 \tag{7}
\]

Subtracting the equal squared coordinate differences shows that
\((Rx)_\perp=F(x_\perp)\) for a well-defined planar contraction \(F\)
on the projected set. It extends to the plane by Kirszbraun's theorem.
For fixed coordinate \(z\), weight \(\xi\) by the one-dimensional
Gaussian \(\gamma_s^{(1)}(z-x_i)\), project onto the perpendicular plane,
and normalize by its positive mass \(m_z\). Denote the resulting
probability law by \(\xi_z\). The input and output density slices are

\[
 m_z(\xi_z*\gamma_s^{(2)}),\qquad
 m_z((F_\#\xi_z)*\gamma_s^{(2)}).
\]

Apply [Aishwarya--Li, Theorem 1.2](https://arxiv.org/html/2609.07041v2)
to \(\xi_z,F\) at hinge threshold \(a/m_z\), multiply by \(m_z\),
and integrate in \(z\). Tonelli applies to the nonnegative hinges.
This proves (7), without any coordinate independence assumption.

## 3. Three coordinate-preserving maps with the same fixed core

For each cyclic triple
\((i,j,k)=(1,2,3),(2,3,1),(3,1,2)\), define on \(\mathcal V\)

\[
 R_i(v)=
 \begin{cases}
 v_i e_i,&v_i\ne0,\\
 \tfrac12(v_j+v_k)e_j+\tfrac12(v_k-v_j)e_k,&v_i=0.
 \end{cases}
 \tag{8}
\]

Extend by \(R_i(rv)=rR_i(v)\) and by the identity on \(P_h\).
These are cyclic versions of the map constructed in the fixed-core
paper; that geometric construction is explicitly credited as a dependency.
Each map preserves coordinate \(i\) on its entire domain.

Here is a self-contained contraction check, including unequal radii.
For \(A=S,R_1,R_2,R_3\), every \(A(v)\) is a unit axis vector, and

\[
 d_A(v,w):=v\cdot w-A(v)\cdot A(w)\le1.
 \tag{9}
\]

For \(S\), two vectors in the same coordinate plane have \(d=1\),
except opposite vectors have \(d=-3\). In different planes the two
output vectors are orthogonal, so \(d=\pm1\).
For \(R_i\), if both vectors have nonzero coordinate \(i\), the
residual inner product is that of their one remaining signed coordinate,
and is at most one. If both have coordinate \(i\) zero, (8) scales
inner products by \(1/2\), so again \(d\le1\). If exactly one has
coordinate \(i\) zero, the residual is a signed half-sum or half-difference
of two signs, in \(\{-1,0,1\}\). Consequently

\[
 |rv-tw|^2-|rA(v)-tA(w)|^2
  =(r-t)^2+2rt(1-d_A(v,w))\ge0.                 \tag{10}
\]

For a core point \(z\in P_h\), one has \(|z_\ell|\le h\) and
\(u_\ell\cdot z\ge-h\). The vectors \(v-S(v)\) are among
\(\{-u_0,-u_1,-u_2,-u_3\}\). Each \(v-R_i(v)\) is a signed
coordinate vector perpendicular to \(e_i\). Thus, for every map above,

\[
 |rv-z|^2-|rA(v)-z|^2
 =r^2-2r z\cdot(v-A(v))\ge r(r-2h)\ge0.        \tag{11}
\]

Core-to-core distances are unchanged. The core and rays are disjoint
when \(h>0,r\ge2h\), so the definitions do not conflict. Kirszbraun
extends each map to a global contraction. Only its values on this
bounded domain enter the proof.

## 4. The uniform family: an explicit three-term decomposition

At radius \(r\), let \(P_r\) be the uniform law on \(r\mathcal V\),
and let \(Q_r\) be the uniform law on \(r\mathcal Y\). For each \(i\),
define the probability law \(P_{i,r}\) by

\[
 P_{i,r}(\{rv\})=
 \begin{cases}
 1/6,&v_i=0,\\
 1/24,&v_i\ne0.
 \end{cases}                                                    \tag{12}
\]

There are four points of the first kind and eight of the second, so
the mass is \(4/6+8/24=1\). Under \(R_i\), the first four points
map bijectively to the four axis points perpendicular to \(e_i\),
each of mass \(1/6\). The other eight split into groups of four over
\(\pm re_i\), again giving mass \(4/24=1/6\). Therefore

\[
 (R_i)_\#P_{i,r}=Q_r\quad(i=1,2,3),\qquad
 \frac13\sum_{i=1}^3P_{i,r}=P_r.                                \tag{13}
\]

The second identity follows because every \(v\) has exactly one zero
coordinate: its averaged weight is \((1/6+1/24+1/24)/3=1/12\).
Also \(S_\#P_r=Q_r\).

Use the same core law in all three components:

\[
 \mu_i=(1-\alpha)\rho+\alpha\int P_{i,r}\,d\eta(r).
 \tag{14}
\]

Then \(\mu=\tfrac13\sum_i\mu_i\), and every \((R_i)_\#\mu_i\)
equals the identical target
\((1-\alpha)\rho+\alpha\int Q_r\,d\eta(r)=\nu\).
Apply (7) to each component and then (6). This proves Theorem A for
uniform weights at every variance, with no asymptotic limit.

Notice that \((R_i)_\#P_r\ne Q_r\): applying the three maps to the
original uniform law is not the certificate. The different source laws
in (12) are essential.

## 5. A full-dimensional neighborhood of unequal weights

Here all vectors have radius one; the construction is applied separately
at each actual radius. For a probability vector \(p=(p_v)\), put

\[
 q_y=\sum_{v:S(v)=y}p_v\quad(y\in\mathcal Y).
\]

It suffices to find nonnegative numbers \(z_{i,v}\) with

\[
 \sum_i z_{i,v}=p_v,\qquad
 \sum_{v:R_i(v)=y}z_{i,v}=q_y/3
       \quad(i=1,2,3;\ y\in\mathcal Y).                         \tag{15}
\]

Indeed \(3z_{i,v}\) are the weights of a probability law whose
\(R_i\)-image is \(q\), while the average of these three laws is \(p\).
For uniform \(p^0_v=1/12\), a strictly positive solution is

\[
 z^0_{i,v}=\begin{cases}1/18,&v_i=0,\\1/72,&v_i\ne0.\end{cases} \tag{16}
\]

Construct a bipartite graph with twelve source vertices \(v\) and
eighteen target vertices \((i,y)\). The edge labelled \((i,v)\)
joins \(v\) to \((i,R_i(v))\), and is oriented towards the target.
There are thirty vertices and thirty-six edges. The graph is connected.
For an explicit connectivity check, the following four target fibers
connect all twelve source vertices to one another:

| Target vertex | Incident source vectors |
| --- | --- |
| \((1,-e_1)\) | \((-1,-1,0),(-1,1,0),(-1,0,-1),(-1,0,1)\) |
| \((2,-e_2)\) | \((-1,-1,0),(1,-1,0),(0,-1,-1),(0,-1,1)\) |
| \((2,+e_2)\) | \((-1,1,0),(1,1,0),(0,1,-1),(0,1,1)\) |
| \((1,+e_1)\) | \((1,-1,0),(1,1,0),(1,0,-1),(1,0,1)\) |

Every other target vertex is incident to a source, since each \(R_i\)
maps onto all six axes. Fix any spanning tree of this graph once and
for all. The supplied checker selects one by deterministic breadth-first
traversal, but the proof works with every spanning tree.

Let \(\delta=p-p^0\) and let
\(\delta q_y=\sum_{v:S(v)=y}\delta_v\). Prescribe signed divergences

\[
 b_v=\delta_v,\qquad b_{(i,y)}=-\delta q_y/3.
 \tag{17}
\]

Their sum is zero, and

\[
 \frac12\sum_a|b_a|
 =\frac12(\|\delta\|_1+\|\delta q\|_1)
 \le\|\delta\|_1.                                             \tag{18}
\]

On a tree there is a unique signed flow with these divergences. One
constructs it by rooting the tree and assigning to each edge the sum
of \(b\) in the child's subtree, with sign adjusted to the fixed edge
orientation. Its magnitude is at most half the total absolute divergence:
any subset sum of a zero-sum vector lies between its total negative and
total positive mass. Extend this correction flow by zero on the unused
edges and denote it by \(f_{i,v}\). Then

\[
 z_{i,v}=z^0_{i,v}+f_{i,v},\qquad
 |f_{i,v}|\le\|p-p^0\|_1.                                    \tag{19}
\]

The divergence equations are exactly the corrections to (15).
Since \(\min z^0=1/72\), assumption (4) ensures \(z\ge0\).
This proves (15) uniformly over the entire closed neighborhood (4).
The construction is affine in \(p\), so it is measurable for
measurable \(p(r)\). Its bound is a written analytic estimate, not an
inference from testing finitely many weight vectors.

Finally replace (14) by

\[
 \mu_i=(1-\alpha)\rho+
          3\alpha\int\sum_v z_{i,v}(r)\delta_{rv}\,d\eta(r).
 \tag{20}
\]

Equations (15) show that these are probability measures, their average
is \(\mu\), and every \((R_i)_\#\mu_i\) equals \(\nu\).
Sections 2--3 prove (5).

More generally, (15) itself is a sufficient certificate, even outside
(4). For fixed weights it is a finite system of linear equalities and
nonnegativity constraints. The explicit tree correction is only one
method of obtaining such a certificate; its failure outside (4) does
not prove infeasibility, much less failure of majorisation.

## 6. Why a mixture is needed, and limits of the method

The fixed-core paper already excludes a single core-fixing, paired-rank
at most five realization for the uniform law. That obstruction remains
valid throughout the neighborhood proved here. We give its quantitative
extension to clarify the scope of the bridge.

For a probability vector \(p\) on \(\mathcal V\), define

\[
 M(p)=\sum_v p_v\big[vv^{\mathsf T}-S(v)S(v)^{\mathsf T}\big].
\]

Direct averaging gives \(M(p^0)=I_3/3\). Each bracketed matrix has
eigenvalues \(2,0,-1\), since \(v\perp S(v)\), and thus operator
norm two. Under (4),

\[
 M(p)\succeq\left(\frac13-2\|p-p^0\|_1\right)I_3
           \succeq\frac{11}{36}I_3.                            \tag{21}
\]

Suppose \(0<\alpha<1\) and the four core vertices belong to
\(\operatorname{supp}\rho\). If a contraction \(F\) fixes these
vertices, has \(F_\#\mu=\nu\), and its paired support
\(\{(x,Fx):x\in\operatorname{supp}\mu\}\subset\mathbb R^6\)
has affine dimension at most five, that support lies in a hyperplane
\(a\cdot x+b\cdot Fx=c\) with \((a,b)\ne0\). Evaluating at the
four affinely independent fixed vertices gives \(b=-a,c=0,a\ne0\).
Thus \(a\cdot Fx=a\cdot x\), forcing equal directional second moments.
But the core contributions to the second-moment difference cancel, and
(21) gives

\[
 \int xx^{\mathsf T}d\mu-\int yy^{\mathsf T}d\nu
   =\alpha\int r^2M(p(r))d\eta(r)
   \succeq\frac{11\alpha}{36}\left(\int r^2d\eta\right)I_3\succ0,
 \tag{22}
\]

a contradiction. Continuity handles core vertices which are support
points rather than atoms. This rules out such a single realization,
not the three different input laws in (20). It does not rule out a map
moving those vertices, or other continuous-lifting mechanisms.

### A rigidity obstruction for every such finite mixture

**Theorem B (injective finite targets give no enlargement).** Suppose
\(\mu=\sum_{j=1}^N p_j\delta_{x_j}\), with distinct \(x_j\) and all
\(p_j>0\), and the original contraction is injective on these points.
Thus \(\nu=\sum_j p_j\delta_{y_j}\) also has \(N\) distinct atoms.
If

\[
 \mu=\sum_{i=1}^m c_i\mu_i,\quad c_i>0,\quad\sum_i c_i=1,
 \qquad (F_i)_\#\mu_i=\nu,                                    \tag{23}
\]

where the \(F_i\) are deterministic maps, then every \(\mu_i=\mu\).
In particular this common-target method yields no new case from a class
of admissible deterministic maps unless a map in that class already
sends the original \(\mu\) to \(\nu\).

To prove it, positivity in (23) forces each component to be supported on
\(\{x_1,\ldots,x_N\}\). A deterministic image with \(N\) positive
atoms then requires that all source atoms are present and mapped
bijectively to the target. Consequently each component weight vector
\(p^{(i)}\) is a permutation of \(p\), and has the same squared
Euclidean norm. Since \(p=\sum_i c_i p^{(i)}\),

\[
 \sum_i c_i\|p^{(i)}-p\|_2^2
   =\sum_i c_i\|p^{(i)}\|_2^2-\|p\|_2^2=0.                  \tag{24}
\]

Every term is nonnegative, proving the assertion. No Lipschitz or
geometric hypothesis on the component maps was needed. The reduction
from twelve ray points to six image points in Theorem A is therefore
essential to this particular convex-decomposition mechanism.

**A concrete boundary from the latest team result.** Researcher 7's
[simplicial-cone reflection paper](../gaussian_simplicial_cone_reflections/PROOF.md),
Theorem D, supplies the nine-point contraction

\[
 (0,A,-B)\longmapsto(0,A,B),\qquad
 A=((1,0,1),(0,1,1),(-1,0,1),(0,-1,1)),
\]
\[
 B=((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1)),                      \tag{25}
\]

whose prescribed labels admit no continuous contraction in
\(\mathbb R^5\). Give the nine displayed labels weights \(2^j/511\),
\(0\le j\le8\). All input and target sites are distinct. Theorem B
forces every component source law to be the original law. Since all
weights are distinct, its deterministic bijection to the target must
be the prescribed matching. Therefore there is **no decomposition
(23) into deterministic contractions admitting five-dimensional
continuous lifts**, of any finite number of components. This also rules
out coordinate-preserving component maps: the prescribed map sends
\(-b\) to \(b\) for a spanning list \(B\), so no nonzero linear
coordinate can be preserved.
This corollary depends on the cited nine-point nonliftability proof;
it is not a new proof of that geometric fact. It does not exclude
general stochastic couplings or decompositions performed after smoothing,
and it is not a Gaussian counterexample.

### Other scope limits

The three-map certificate is itself only sufficient. For example, if
\(p\) is concentrated at one vector \(v\), nonnegativity in (15)
forces every used source to be \(v\). Yet every \(R_i(v)\) lies in
the coordinate plane of \(v\), whereas \(S(v)\) is perpendicular to
that plane. Thus (15) is impossible. With no core mass, both Gaussian
laws in this example are translates of one Gaussian, so majorisation
holds with equality. Certificate infeasibility cannot be used as a
counterexample to the conjecture.

The universal conjecture, arbitrary unbalanced ray weights, and new
support-level KP cases remain open to other methods. Our earlier
replica-curvature and sparse Hankel results remain useful for arbitrary
bounded laws but have noise/order restrictions; they are not premises
here. This bridge obtains all orders at once from a common-target
convex decomposition and the planar theorem, not from entropy stability
or finitely many moments. The independently accepted entropy audit and
replica-curvature checkpoint are preserved.

## 7. Validation and trust boundary

The standard-library rational checker derives all four maps from (2)
and (8), checks all ordered ray-pair deficits and all core vertices,
verifies (12)--(16), constructs a spanning tree, and checks the linear
flow conservation on an exact basis of perturbations. It additionally
checks all 132 extreme directions of the stated zero-sum L1 ball,
including nonnegativity, common outputs, normalization, and (21).
It tests distinct radial shells, detects a deliberately wrong target
certificate, and records the point-mass obstruction just explained.

These are supplementary exact audits. The universal proof relies on
the written convexity, planar disintegration, tree-flow estimate, and
the cited planar theorem, not on finite Gaussian quadrature or the
successful execution of the checker. No proof-assistant formalization
or independent review is claimed. Sources and earlier team results are
identified in [SOURCES.md](SOURCES.md).
