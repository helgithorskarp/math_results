# Exact family and certificate argument

For each ordered pair (m_i,m_j) of distinct spindle points, form

    A_ij = { (m-m_i)/(m_j-m_i) : m in M }.

Do the same with the conjugate spindle. For each unordered seed pair p,q
whose squared distance equals |m_j-m_i|², the set

    p + (q-p) A_ij

is a congruent spindle image. Conversely, every direct or reflected plane
isometry sharing at least two seed points occurs in this enumeration: choose
any two shared image points and their spindle preimages. Both preimage
orientations and both reflection choices are present. Normalized point-set
deduplication removes redundant descriptions, not placements.

The norm equality implies that the multiplier (q-p)/(m_j-m_i) has modulus
one. Division and complex conjugation remain in the exact seed field because
M is defined over its subfield E. Point-set equality is exact equality in the
specified quadratic extension of E. In particular no abstract edge
identification is used as a substitute for Euclidean coincidence.

Every normalized image has seven points; at least two are already in B.
Hence its added point set N has size at most five. Three images have at most
490+3*5=505 points, even when their new points overlap one another. The second
search checks the exact union cardinality against 508 at every step.

The contact filter is independent of the choice of a witness image for N.
If |N|<=3, every witness already shares at least four seed points and passes
the old-contact threshold. If |N| is 4 or 5, at most three image vertices are
old. The spindle has minimum degree three, so each such old vertex is
adjacent to a new vertex. Therefore every shared old vertex is already in
the set of seed unit-neighbours of N, which depends only on N. The other
filter, requiring a new point with fewer than four old neighbours, likewise
depends only on N. Deduplicating by N preserves the admitted physical family.

Let U be the union of B with all admitted N. Every admissible assembly, and
every vertex or edge subgraph of one, is a subgraph of the strict unit graph
on U. A proper four-colouring of U restricts to each such graph. The dense
host's supplied colour word is verified on every exact unit edge, proving
that stated family cannot improve509. No analogous word or non-four proof
was obtained for the GMM host, so its status remains UNKNOWN.

For coordinate z=(a,b,c,d)+(A,B,C,D)*sqrt(s), each quadruple represents
x_0+x_1 sqrt(33)+i*x_2 sqrt(3)+i*x_3 sqrt(11). Complex conjugation fixes s.
The native checker compares the four real coefficients of z*conj(z) with
one. Its second formula separately squares the real coordinate and the
imaginary coordinate, written as sqrt(3) times an element of
Q(sqrt(33),sqrt(s)). Both formulas are exact. The radicand is positive and
nonsquare in Q(sqrt(33)), so coefficient comparison is faithful.

Native input coordinates, shared denominators, and radicand numerators and
denominator are bounded by 10^9. Coordinate differences are bounded by
2*10^9. The degree-three integer expressions in the two norm formulas,
including their fixed constants, stay below10^33, hence within signed128-bit
range. The output capacity is checked before each edge write. Out-of-range
inputs are rejected rather than rounded. The larger vertex bound changes
loop/allocation counts, not arithmetic bounds.

The small-graph search uses four Boolean colour literals per point, one
at-least-one clause, and four exclusion clauses per edge. Three actual
triangle vertices are pinned to different colours to remove global colour
permutations. At-most-one clauses are unnecessary: choosing any true colour
for each point yields a proper colouring because adjacent vertices cannot
share any true literal. Every decoded word is checked. UNKNOWN is retained
as UNKNOWN; no solver UNSAT result occurred among the record-sized cases.

The search oracle tests whether a particular current colouring extends to
an insertion. It removes colours used on currently coloured neighbours and
solves the remaining at-most-five-vertex list-colouring problem exactly.
A zero answer forbids that word, not all colourings of the seed. The published
495-point fixture and its alternative four-colouring demonstrate that
logical distinction. Search width, query budgets, and retained DFS states
are operational restrictions; they do not give an exhaustive family theorem.
