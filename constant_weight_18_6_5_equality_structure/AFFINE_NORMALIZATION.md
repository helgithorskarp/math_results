# The order-four affine-plane normal form

Author: six-code-1, researcher. Date: 2026-09-30.

The uniqueness of the affine plane of order four is established mathematics,
not a new classification claim. We include the complete elementary argument
needed to justify the finite normal form in [SUPPORT16.md](SUPPORT16.md).
For primary exposition see Anurag Bishnoi, *Finite Geometries* (2012), Theorem 3.6:
<https://anuragbishnoi.wordpress.com/wp-content/uploads/2014/09/report21.pdf>.
The argument below is self-contained and does not import a classification
program or assume that an arbitrary plane is a field plane.

Choose two parallel classes in an affine plane of order four and label
their intersections by the sixteen cells of a four-by-four array. The
remaining twelve lines each intersect every row and every column once,
and so are graphs of twelve permutations of four symbols. Two such
permutations agree at at most one place, since two lines cannot share
two points.

Consider the graph on the 24 permutations in which two are adjacent
when they disagree at exactly two places. Adjacency is composition
with a transposition. The graph is connected, because transpositions
generate the symmetric group, and every vertex has degree six.
Permutation parity gives its bipartition. Our twelve line permutations
are an independent set. Their incident edges number twelve times six,
which equals the total number of edges in this graph. Thus the other
twelve vertices also form an independent set. A connected bipartite
graph has only its two bipartitions, up to exchange, so the line
permutations are precisely the even or the odd permutations. Relabel
columns to make one line the identity; the set is then exactly \(A_4\).

Over \(\mathbb F_4\), the twelve maps \(x\mapsto mx+c\), \(m\ne0\),
are exactly these even permutations. A nonzero translation is a product
of two disjoint transpositions; multiplication by a nonidentity nonzero
field element is a three-cycle on the nonzero elements. The twelve maps
are distinct and even. Their graphs, together with rows and columns,
are the twenty field-plane lines. This proves uniqueness and gives an
explicit normal form.

For the application, a distinguished point may be translated to the
origin. Two distinguished directions may be sent to the coordinate
axes by an invertible linear map. Once these axes are specified, a
line missing the origin whose direction is neither axis has equation
\(y=mx+c\), with \(m,c\ne0\). Independent nonzero scaling of the two
coordinates sends it to \(x+y=1\). Swapping the coordinates exchanges
its two axis intersections. The field automorphism
\(x\mapsto x^2\) exchanges the other two points of that line and fixes
the axis intersections. These transformations preserve the two-axis
part and the other-three-directions part of a split point.

Write \(\mathbb F_4=\{0,1,\omega,\omega^2\}\), with
\(\omega^2=\omega+1\), and label \((x,y)\) by \(4x+y\), using
integer field labels \(0,1,2,3\). The line \(x+y=1\) is
\(\{1,4,11,14\}\). Any configuration on that line with two points
from the axis part, two from the other-directions part, and a chosen
point in each part can therefore be normalized to
\[
v=4=(1,0),\qquad u=11=(\omega,\omega^2),
\]
with the other points \(d=1\) and \(c=14\). This covers all
configurations used in SUPPORT16; it is not a symmetry assumption
about the global code.

The source checks verify all 24 permutation vertices, all 72
transposition-graph edges and connectivity, and compare the twenty
\(A_4\)-graph lines with the field lines entry by entry. These checks
validate this small model; the normalization proof above is ordinary
mathematics and is not derived merely from the computed counts.
