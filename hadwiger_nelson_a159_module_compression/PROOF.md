# Deleting any private A159 vertex removes every terminal constraint

Let A be the strict unit-distance graph of the pinned 159-point coordinate
file, with terminals T = {141,142,144} in zero-based file order. Its 646
unit edges are reconstructed exactly. The terminals form an equilateral
triangle of side sqrt(7). Put I = V(A) minus T, so |I| = 156.

**Theorem 1.** For every proper subset J of I, every function
f:T->{0,1,2,3} extends to a proper four-colouring of A[T union J].
The same holds after any further edge deletions.

For every v in I, the supplied certificate gives a colouring of A-v whose
three terminal colours are 000. The checker tests every retained unit edge.
Renaming the palette gives all four monochromatic assignments on T.
The inherited, directly rechecked full-A witnesses have terminal patterns
001, 010, 011, 012. Their palette renamings give all sixty nonmonochromatic
assignments, and restriction gives those assignments on A-v.
Thus every one of the 64 assignments extends to A-v for every v in I.
The checker also explicitly constructs and checks all 156*64 extensions.

Now fix any proper J. Choose v in I minus J and restrict the appropriate
colouring of A-v to T union J. This proves the theorem for all 2^156-1
proper private subsets without enumerating them. Removing edges cannot
invalidate a proper colouring.

**Corollary 1 (exact module cost).** Any subgraph of this pinned A that
contains T and forbids monochromatic T must contain every private vertex.
Hence its vertex order must be 159, with 156 private vertices. This is a
necessary statement; the proof does not require or establish that full A
actually forbids the monochromatic pattern. In particular, no reduction
with at most 100 private vertices can preserve that forcing relation.

This is a local compression obstruction for a specified coordinate gadget,
not a lower bound on all unit-distance gadgets with this terminal geometry.
No claim is made about deleting only edges while retaining all 159 vertices.

## From the local obstruction to the five-module construction

Consider k<=5 finite plane modules (Vi,Ti). Suppose each Ti has at least two
points, all distances within Ti are >2, and **every** four-colouring of Ti
extends through the strict unit graph on Vi. Suppose also that:

1. Vi intersect Vj is contained in Ti intersect Tj whenever i!=j.
2. Every unit edge of the union not internal to some module joins terminals.
3. There are no extra connector vertices outside the modules.

**Lemma 2.** The strict unit graph on the union of these modules is
four-colourable.

Let U be the strict unit graph on the terminal union. A vertex x lying in
r terminal sets has no unit neighbour in those sets. In any one of the
other k-r sets it has at most one unit neighbour: two would have mutual
distance at most 2 by the triangle inequality. Thus d_U(x)<=k-r<=4.
This remains true with shared terminals or repeated terminal sets.

The unit graph of distinct plane points has no K4, and hence no K5. Indeed,
after fixing a unit pair at (0,0),(1,0), the only two other points at unit
distance from both are (1/2,+sqrt(3)/2),(1/2,-sqrt(3)/2); these are sqrt(3)
apart. By the classical Brooks theorem, a finite simple graph of maximum
degree at most four with no K5 component is four-colourable. Components of
degree at most three also satisfy this directly by greedy colouring.
Therefore U has a proper four-colouring. Extend it independently through
each module. Hypothesis 1 ensures consistency on overlaps; hypothesis 2
accounts for every remaining edge. This proves Lemma 2.

The only external graph theorem here is Brooks' theorem. See
[Brooks (1941)](https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/abs/on-colouring-the-nodes-of-a-network/546AD533E0FDCFD02755AC34B0972D0E)
and the constructive treatment by
[Baetz and Wood](https://arxiv.org/abs/1401.8023). We apply it componentwise.
The certificate checker proves Theorem 1; it does not formalize this
classical theorem or the written geometric lifting argument.

**Corollary 2 (selected architecture).** Every terminal-only assembly of
at most five copies of proper terminal-preserving vertex reductions of A
is four-colourable. Copies may use different retained subsets and arbitrary
real translations, rotations and reflections, provided hypotheses 1--3
hold. There is no size restriction on this corollary. In particular it
excludes every such at-most-508 construction with at most 100 private
vertices in each of its five modules.

Theorem 1 supplies unrestricted extension for each reduced copy, and its
terminal separation sqrt(7)>2 supplies Lemma 2's geometric premise.

## Exact scope of the synthesis decision

The prior four-module theorem covers modules with universal *nonmono*
extension. Its five-module/eight-terminal handoff contemplated five modules
of 100 private vertices. The present result shows that such a forcing
module cannot be obtained by deleting vertices from this A159 source.
All five proper reductions are excluded even without the eight-terminal
restriction, because their terminals impose no residual colour relation.

This does not settle mixed assemblies containing both intact and reduced
A copies, six or more reduced modules, new connector graphs, interior
contacts or overlaps, altered coordinates, or replacement forcing modules
not obtained by vertex deletion. None of those phases is started here.
Full A159's advertised negative forcing property is never used. No
five-chromatic physical candidate and no record improvement are claimed.
