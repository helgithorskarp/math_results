# Four common neighbors are attainable and maximal on the torus

A thrackle on a surface is a drawing of a finite simple graph with simple
edge arcs, no edge through another vertex, and no triple interior
intersections, such that adjacent edges meet only at their shared
endpoint and each pair of independent edges crosses properly exactly
once. All surfaces below are orientable.

**Theorem.** Two distinct vertices in a toroidal thrackle have at most
four common neighbors. This bound is attained by a thrackle of
$K_{2,4}$. Consequently $K_{2,n}$ admits a thrackle on the torus exactly
when $0\le n\le4$, and its minimum orientable thrackle genus is one for
$2\le n\le4$.

The upper bound is a direct consequence of a known homology lemma.
The contribution here is an explicit cyclic construction attaining it,
with a small rotation certificate. Historical priority is not asserted;
see [SOURCES.md](SOURCES.md).

## The known obstruction and its equality case

Cairns and Nikolayevsky, *Bounds for Generalized Thrackles* (2000),
[Lemma 5(a)](https://link.springer.com/content/pdf/10.1007/PL00009495.pdf),
show that a thrackled four-cycle is nonzero in mod-two homology.
Here is the short argument. Label it $1234$, with crossings
$a=12\cap34$ and $b=23\cap14$. Split at $b$ into the loops
$1\,2\,b\,1$ and $3\,4\,b\,3$. Their turns at $b$ can be separated
locally; the resulting loops cross only at $a$. Their intersection
pairing is therefore one. The pairing on an orientable surface is
alternating, so these loops cannot represent the same class. Their
sum, the original four-cycle, is nonzero.

Now suppose $u,v$ have common neighbors $w_0,\ldots,w_{n-1}$.
Let $P_i$ be the two-edge arc $u w_i v$ and put
$h_i=[P_i+P_0]\in H_1(S_g;\mathbb F_2)$. The sum is a cycle
because the endpoints cancel. For distinct $i,j$, the class
$h_i+h_j=[P_i+P_j]$ is a thrackled four-cycle, hence is nonzero.
Thus the $n$ classes $h_i$ are distinct. Since
$|H_1(S_g;\mathbb F_2)|=2^{2g}$, we have $n\le4^g$.
The case $g=1$ gives the bound four. The case $g=0$ rules out a
spherical or planar thrackle containing $K_{2,2}$.

For any equality drawing on the torus, the four $h_i$ exhaust
$H_1(T^2;\mathbb F_2)$. Among the six four-cycles $P_i+P_j$,
each nonzero homology class occurs twice. More precisely,
complementary pairs of neighbors give the same class, since the
sum of the four $h_i$ is zero. This is an equality consequence of
the known obstruction, not an additional novelty claim.

## A cyclic rotation scheme attaining the bound

All subscripts in this section are modulo four. The original vertices
are $u,v,w_0,w_1,w_2,w_3$, with edges $e_i=uw_i$ and $f_i=vw_i$.
For $i\ne j$, introduce the crossing vertex $x_{ij}$ between $e_i$
and $f_j$. Prescribe the following edge paths in the planarization:

$$
e_i:\quad u,\ x_{i,i+2},\ x_{i,i+3},\ x_{i,i+1},\ w_i;
$$

$$
f_i:\quad v,\ x_{i+1,i},\ x_{i+3,i},\ x_{i+2,i},\ w_i.
$$

At $u$ use cyclic order $(e_0,e_1,e_2,e_3)$, and at $v$ use
$(f_0,f_1,f_2,f_3)$. Each $w_i$ has degree two, so has a unique
cyclic order.

At $x_{ij}$, name the four outgoing half-edges as follows:
$a$ points along $e_i$ toward $u$; $b$ points along $e_i$ toward
$w_i$; $c$ points along $f_j$ toward $v$; $d$ points along $f_j$
toward $w_j$. Use rotation

$$
\rho(x_{ij})=
\begin{cases}
(a,d,b,c),&j-i=1,\\
(a,c,b,d),&j-i=2\ \text{or}\ 3.
\end{cases}
$$

In both cases the two half-edges belonging to $e_i$ alternate with
the two belonging to $f_j$. This makes $x_{ij}$ a proper crossing
when the original edges are restored.

## The surface is a torus: four face orbits

A rotation scheme defines an oriented ribbon surface: take oriented
vertex discs and attach one untwisted band for every segment of the
planarization, respecting the specified cyclic orders. Cap every
boundary component with a disc. The result is a closed orientable
surface carrying a cellular embedding of the planarization. It is
connected because the graph is connected.

For explicit verification, the directed face walk traverses a segment
$p\to q$, then follows the outgoing segment immediately after $q\to p$
in the rotation at $q$. Thus its permutation is $\rho\alpha$, where
$\alpha$ reverses each directed segment.

The index shift $i\mapsto i+1$ preserves the paths and rotations.
All face walks are given by the following four orbits. Each displayed
word is cyclic, so its last vertex is followed by its first.

| Representative face | Orbit size | Length |
|---|---:|---:|
| $u,\ x_{02},\ x_{12},\ w_1,\ x_{31}$ | 4 | 5 |
| $x_{02},\ x_{03},\ v,\ x_{10},\ x_{12}$ | 4 | 5 |
| $x_{03},\ x_{02},\ w_2,\ x_{23}$ | 4 | 4 |
| $x_{01},\ x_{03},\ x_{23},\ x_{21}$ | 2 | 4 |

Substitution into the rotation rule checks each representative; shifting
indices checks its entire orbit. The resulting fourteen directed cycles
are disjoint on directed segments and contain
$4\cdot5+4\cdot5+4\cdot4+2\cdot4=64$ directed segments, exhausting
the two sides of all 32 bands. This also proves completeness of the
face list without a search.

There are six original vertices, twelve crossings, and four segments
per original edge. Consequently

$$
V=18,\qquad E=32,\qquad F=14,\qquad
\chi=V-E+F=0.
$$

The classification of connected closed orientable surfaces identifies
the capped surface as a torus.

## Restoring the thrackle

Inside each crossing disc, join the two $e_i$ half-edges and join the
two $f_j$ half-edges. Their alternation allows precisely one transverse
crossing. Outside these mutually disjoint discs the segment interiors
are disjoint, because they belong to an embedded graph.

Each original edge path visits five distinct planarization vertices,
and so is a simple arc after this replacement. Two $e$ edges meet only
at $u$, and two $f$ edges meet only at $v$. The pair $e_i,f_i$ meets
only at $w_i$. For $i\ne j$, the pair $e_i,f_j$ meets only at
$x_{ij}$, where it crosses properly. No crossing involves a third
edge, and no edge interior passes through an original vertex. These
are all pairs of original edges, establishing the thrackle definition.

Deleting some $w_i$ and their incident edges gives the cases
$0\le n<4$. For $2\le n\le4$, the four-cycle obstruction rules
out genus zero, completing the theorem.

## Verification boundary

The proof above specifies the full construction and its faces. The
code provides exact redundant checks, rather than a completeness
claim about a search. The input [certificate.json](certificate.json)
lists all paths, rotations as neighboring vertices, and the four
face representatives. The verifier reconstructs the ribbon faces
from that input without importing the constructor.

In addition to incidences, all 28 edge-pair intersections, alternating
crossing orders, connectedness, symmetry, and face exhaustion, the
verifier forms the cellular boundary matrices. It checks
$\partial_1\partial_2=0$ over the integers, cancellation of oriented
face boundaries, ranks $(17,13)$ over both $\mathbb F_2$ and
$\mathbb F_3$, and hence Betti numbers $(1,2,1)$. It also checks
the four distinct relative mod-two classes and their zero total.

The topological realization by discs and bands and the classification
of surfaces are ordinary mathematical arguments, not proof-assistant
formalizations. No solver, floating-point geometry, external dataset,
or unreported exhaustive enumeration is needed to establish the claim.
This result concerns the torus; it does not settle Conway's planar
edge-bound conjecture or the asymptotic thrackle genus of $K_{2,n}$.
