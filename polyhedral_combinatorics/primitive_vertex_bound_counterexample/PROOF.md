# Primitive polytopes with more than \(2^d\) vertices

## Statement and target

Here a **primitive polytope** is a bounded, full-dimensional polytope
whose irredundant facet inequalities have this property: deleting any
one of them leaves an unbounded intersection. This is the definition in
Illya Ivanov, *Illuminating Primitive Polytopes*,
[arXiv:2607.08944v1](https://arxiv.org/html/2607.08944v1), Section 1.3.
It is unrelated to lattice-primitivity conventions.

Conjecture 6 of that paper states that a primitive \(d\)-polytope, \(d\ge4\),
has at most \(2^d\) vertices, with equality only for affine cubes.
The construction below refutes both the numerical bound and its equality
clause. It makes **no claim against the illumination conjecture or against
the paper's Theorem 2 about illumination**. A polytope's number of vertices
need not be its illumination number.

**Theorem.** For every integer \(k\ge2\), let
\[
 P_k=\left\{(y,z,x_0,\ldots,x_{k-1})\in\mathbb R^{k+2}:
 \begin{array}{l}
 y,z,x_0,\ldots,x_{k-1}\ge0,\\
 x_i+(2i+1)y+z\le k^2+i(i+1)\quad(0\le i<k).
 \end{array}\right\}.                                      \tag{1}
\]
Then \(P_k\) is a simple primitive polytope of dimension \(k+2\), with
exactly \(2k+2\) facets and
\[
                  f_0(P_k)=2^{k-2}(k+7).                    \tag{2}
\]
Consequently
\[
 \dim P_{10}=12,\qquad f_0(P_{10})=4352>4096=2^{12}.
\]
Also \(P_9\) has dimension 11 and 2048 vertices, but only 20 facets,
whereas an affine 11-cube has 22 facets. It refutes the equality
characterization independently of the strict numerical violation.
In this family
\[
               \frac{f_0(P_k)}{2^{\dim P_k}}=\frac{k+7}{16}
                   \longrightarrow\infty.                  \tag{3}
\]
No minimal-dimension assertion is made.

The proof uses only explicit inequalities, affine interval fibers and
elementary polytope facts. The interval-fiber operation is a classical
iterated facet wedge; novelty is claimed only relative to the searched
sources for its application to the stated primitive vertex conjecture.

## 1. Boundedness, dimension and all facets

Write \(b_i=k^2+i(i+1)\). All coefficients in the upper inequalities
of (1) are nonnegative. Thus
\[
 0\le x_i\le b_i,\qquad 0\le z\le k^2,\qquad 0\le y\le k,
\]
where the last inequality uses row \(i=k-1\), whose right side is
\(k(2k-1)\). Hence \(P_k\) is bounded.

The point with every coordinate equal to \(1/4\) satisfies all inequalities
strictly: row \(i\) has left side \((2i+3)/4\), at most
\((2k+1)/4<k^2\) for \(k\ge2\). This also proves full dimension.

Each coordinate lower inequality is a facet. Set its coordinate to zero
and leave all other coordinates equal to \(1/4\). Exactly that inequality
is tight. A sufficiently small open neighborhood in its hyperplane
therefore remains inside all the other halfspaces.

For upper row \(i\), set \(y=z=1/4\), set
\[
              x_i=b_i-(i+1)/2>0,
\]
and set every other private coordinate to \(1/4\). Again, exactly the
chosen inequality is tight. Thus each of the \(k\) upper inequalities
is a facet. These \(2k+2\) distinct inequalities are irredundant and
give every facet of \(P_k\).

## 2. Every single-facet deletion is unbounded

Let \(e_y,e_z,e_{x_i}\) be the coordinate unit vectors. Start from any
point of \(P_k\), for example the origin.

If the lower inequality for a coordinate \(u\) is removed, the whole ray
in direction \(-e_u\) satisfies every remaining inequality. Every other
lower coordinate is unchanged and all upper left sides weakly decrease.

If upper row \(i\) is removed, the whole ray in direction \(+e_{x_i}\)
satisfies every remaining inequality: only the removed upper row has a
positive coefficient on \(x_i\), and its lower bound improves.

These are nonzero recession rays, one for each facet deletion. Therefore
\(P_k\) is primitive in precisely the target definition. Translating
the interior point from Section 1 to the origin gives the normalization
used in the paper, without changing any claimed property.

## 3. The projected polygon

Put
\[
 c_i(y,z)=k^2+i(i+1)-(2i+1)y-z.
\]
Projection to the first two coordinates gives exactly
\[
 Q_k=\{(y,z): y,z\ge0,\quad c_i(y,z)\ge0\ (0\le i<k)\},       \tag{4}
\]
because the fiber over \((y,z)\) is
\[
                       \prod_{i=0}^{k-1}[0,c_i(y,z)].       \tag{5}
\]

The vertices of \(Q_k\) are
\[
              o=(0,0),\qquad q_j=(j,k^2-j^2),\quad 0\le j\le k.
                                                                  \tag{6}
\]
Here is a direct completeness proof. If \(j\le y\le j+1\),
\(0\le j<k\), row \(j\) supplies the least upper bound on \(z\), since
\[
 [b_i-(2i+1)y]-[b_j-(2j+1)y]
                 =(i-j)(i+j+1-2y)\ge0
\]
for every integer \(0\le i<k\). Therefore the upper boundary is exactly
the polygonal chain joining the successive \(q_j\). Together with the
two coordinate-axis segments it encloses (4); beyond \(y=k\), the last
row forces \(z<0\). This proves (6).

At these points the slacks have the useful exact values
\[
             c_i(q_j)=(i-j)(i-j+1),\qquad c_i(o)=b_i>0.     \tag{7}
\]
Thus no upper row is active at \(o\); one is active at each of \(q_0,q_k\);
and exactly two, \(j-1,j\), are active at every \(q_j\), \(0<j<k\).

## 4. Affine-box lifting lemma

**Lemma.** Let \(Q\) be a polytope and let \(c_1,\ldots,c_m\) be
nonnegative affine functions on \(Q\). In
\[
       B(Q,c)=\{(q,x):q\in Q,\ 0\le x_i\le c_i(q)\},
                                                                  \tag{8}
\]
the vertices are precisely the points over vertices \(q\) of \(Q\)
at which each \(x_i\) is an endpoint of its interval. Hence
\[
       f_0(B(Q,c))=\sum_{q\in\operatorname{vert}Q}
                    2^{\,|\{i:c_i(q)>0\}|}.                \tag{9}
\]
Zero-length intervals contribute one choice.

*Proof.* If some \(x_i\) is strictly between its endpoints, changing
only \(x_i\) in both directions proves nonextremality.
Otherwise write \(x_i=\epsilon_i c_i(q)\), with
\(\epsilon_i\in\{0,1\}\) (either choice is allowed if the slack is zero).
If \(q\) is not a vertex, express it as a proper convex combination
of distinct \(q',q''\in Q\). Affineness lifts this combination using
the same \(\epsilon_i\). The lifted points are distinct because their
projections differ, so \((q,x)\) is not a vertex.

Conversely, in a proper convex decomposition of a point above a vertex
of \(Q\), both projected points must equal that vertex. An interval-box
corner is extreme in that fiber, so the decomposition is trivial.
The choices in (9) are distinct and exhaustive. \(\square\)

This lemma is also a self-contained description of the familiar repeated
facet-wedge vertex count: wedging a facet keeps its vertices and doubles
the others. We do not claim the wedge construction itself as new.

## 5. Exact count and simplicity

Apply (9) to (4)--(5). The origin contributes \(2^k\) vertices, the
two axis endpoints contribute \(2^{k-1}\) each, and the \(k-1\) other
vertices contribute \(2^{k-2}\) each. Therefore
\[
 f_0(P_k)=2^k+2\cdot2^{k-1}+(k-1)2^{k-2}
                         =2^{k-2}(k+7),
\]
as claimed.

For completeness the examples are simple, even though simplicity is
not needed for the counterexample. At a vertex of \(Q_k\), let \(a\)
be the number of active upper rows and \(r\) the number of active
coordinate-axis rows. The polygon has \(a+r=2\). Above it, each of
the \(a\) zero private intervals activates both its lower and upper
facet; each of the \(k-a\) positive intervals activates exactly one.
Together with the \(r\) axis facets, the number of active facets is
\[
                       2a+(k-a)+r=k+2.
\]
Their normals are independent: eliminate the private coordinates
using one active endpoint row for each. The two remaining rows are
the independent active rows at the polygon vertex. Each vertex
therefore lies on exactly \(k+2\) facets of this full-dimensional body.

In particular, the lifted vertices in (6)--(7) have integer coordinates,
so the displayed examples also happen to be lattice polytopes.
Lattice properties play no role in the definition of primitive here.

## 6. An independent witness route and scope

To refute the numerical bound one does not need the completeness part of
Section 4. For \(k=10\), generate all distinct interval endpoint vectors
above the twelve points in (6). The accompanying checker evaluates all
22 inequalities on every one of the 4352 integer points and computes
the exact rank of its active normals. All ranks are 12. This proves
directly that the halfspace intersection has at least 4352 vertices.
It also checks strict interior and facet points, bounded-coordinate
certificates, and the 22 deletion rays. These direct checks do not
assume the wedge lemma or the numerical formula.

The universal exact formula and the unbounded ratio in (3) follow from
the written proof. Separate complete active-basis enumeration in small
cases checks the equality of the vertex sets, rather than only their
cardinalities. Exact checks use Python integers and rational arithmetic;
they are corroboration, not an independent peer review or formalization.

The checked primary source still lists only version 1 on 21 September
2026. Focused searches found no earlier refutation of its Conjecture 6.
The novelty statement is search-relative. This note does not classify
primitive polytopes, optimize the counterexample dimension, determine
illumination numbers, or challenge unrelated results in the source.
