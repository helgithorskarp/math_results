# A complete 197-class minority-core cover for the four-versus-seven split

Consider a hypothetical Ramsey (5,5;43) graph with an order-three
automorphism having eleven moving triangles and ten fixed vertices.
Assume four moving triangles are internally red and seven internally
blue. The twelve red-triangle vertices have **197 possible core types**
under the normalizer action specified below. Their complete compact
catalog is `cover.json`.

This is a local classification and a complete cover for subsequent
extension tests. None of the 197 full extensions has been decided in
this pass. It does not exclude the four-versus-seven branch, construct
a target, or improve the Ramsey lower bound. The three-versus-eight
branch retains its two previously surviving cores.

## Local obstruction and exact domain

Label the four red triangles Ci, i=0,1,2,3, with vertices 3i+s for
s modulo three. For i<j, let b_ij(d) be the red edge bit between
3i+s and 3j+s+d. Order the six words as 01,02,03,12,13,23, and within
each word order offsets 0,1,2. They give eighteen binary coordinates.

A word 111 is impossible: its two triangles form a red K6. There
are therefore at most 7^6=117649 noncomplete-word assignments. Each
cross block is empty, a matching, or a six-cycle. In particular it has
no red K2,2. A red K5 cannot occupy the triangles as 3+2 or 3+1+1,
which require a complete block, or as 2+2+1, which requires a K2,2.
The only possible occupancy is consequently **2+1+1+1**. A blue K5
is impossible locally since it could use at most one vertex per red
triangle.

There are 324 vertex five-sets with occupancy 2+1+1+1. Projecting their
nine cross edges onto the eighteen coordinates gives exactly 108
distinct nine-bit masks. The local graph is Ramsey-valid if and only
if it avoids every complete word and does not contain any of those
108 masks. They are explicitly stored in the catalog. Exactly 2106
of the 117649 noncomplete assignments fail this condition, leaving
**115543** locally valid labeled cores.

The generator uses this occupancy argument and subset tests on the
108 masks. The separate checker enumerates all 262144 binary cores as
literal twelve-vertex graphs and searches for a clique of order five
in each color by recursive vertex intersections. It then checks that
the entire valid set agrees with the submitted obstruction criterion,
not merely its cardinality. Thus its local validity test does not
assume the producer's occupancy reduction.

## Normalizer action and the complete quotient

Use the maps in which new vertex (i,s) is old vertex

```text
(pi(i), epsilon*s+t_i),
pi in S4, t_i in Z/3Z, epsilon in {1,-1}.
```

There are 24*81*2=3888 such vertex maps. A common shift of all four
coordinates acts trivially on the minority cross words, giving a
kernel of order three and 1296 effective maps on those words.

In the full 43-vertex graph, extend each map by applying the SAME
epsilon to the coordinates of all seven blue triangles, and fixing
the ten fixed vertices. The map conjugates the given automorphism
to itself or its inverse. Inversion of the minority coordinates alone
would not normalize the full action and is not allowed.

For perspective, give a nonzero word its distinguished phase: the
position of its unique red bit at weight one or its unique blue bit
at weight two. Rotations change these phases by vertex potentials.
One can make all phases on a spanning forest of the nonzero support
zero; the remaining phases encode sums around its cycles. Triangle
permutations and global inversion act on this weighted support and
its cycle sums. Thus the unordered six weights alone are insufficient.
The explicit group computation keeps the full phase information,
including disconnected supports and zero words.

The producer partitions all valid cores using a breadth-first orbit
closure under eight generators: three adjacent triangle exchanges,
four individual rotations, and global inversion. It obtains 197
orbits. In each orbit it selects the lexicographically first bit string
whose anchor words 01,02,03 are among 000,100,110, with weakly increasing
weights. Such representatives always exist: hold triangle 0 fixed,
rotate each other triangle to its normalized anchor word, then sort
those three triangles by weight. There are 3430 anchor-normalized
noncomplete words before testing local validity, and **3378** after it.

The independent checker instead applies every actual vertex map to
each of the 197 representative adjacency matrices: 765936 literal
core transports. It compares every orbit's membership digest, size,
normalized subset and chosen representative. The orbits are checked
to be disjoint and their union equal to the literal valid set. A
second digest compares the complete labeled-core-to-representative
table. No graph-isomorphism package or solver is used.

These are classes of the specified marked cyclic action. Distinct
classes are not claimed nonisomorphic as unmarked abstract graphs.
The catalog stores representatives, multiplicities, member digests,
and primary units; bulky membership tables are regenerated outside Git.

## Compatibility with the full normalized parent

First transport the minority core to the chosen representative using
the full normalizer map just described. Its three anchor words already
satisfy the parent ordering. Next rotate each blue cycle independently
so its anchor word from C0 is one of 000,100,110,111, and permute those
seven cycles into increasing anchor-weight order. Finally sort the ten
fixed vertices by their full eleven-bit red attachment signatures.
These later operations fix the minority core pointwise. Equal weights
and equal signatures are permitted, so no uniqueness assumption is
needed. The inherited parent argument supplies consistent auxiliary
counter values for the relabeled graph.

The checker tests all 3888 maps on the full 43-vertex automorphism
identity. It separately checks the 22 generators needed for the later
operations: seven blue-cycle rotations, six adjacent blue-cycle
exchanges, and nine adjacent fixed-vertex exchanges. Every later map
commutes with the action and fixes the twelve minority vertices. A
minority-only inversion is explicitly rejected.

The six minority words correspond to these primary variables in the
accepted full parent r=4 formula:

```text
01: 1,2,3       02: 4,5,6       03: 7,8,9
12: 31,32,33    13: 34,35,36    23: 58,59,60.
```

The checker reconstructs these meanings independently by enumerating
the 903 unordered pairs under the eleven-cycle action. It checks all
197 eighteen-unit assignments against the actual representative bits.
The cubes are disjoint on those eighteen coordinates. Their coverage
of full Ramsey graphs is through the proved relabeling, not a claim
that their union is a propositional tautology over every normalized
parent assignment.

The accepted parent has 34280 variables and 615920 clauses, SHA256
`c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f`.
A future full cube must retain that entire parent and append exactly
its eighteen catalog units, giving 615938 clauses. Both color-degree
bounds, all five-set constraints, counters and normalization must stay
present. The parent uses R(4,5)=25 for the degree window 18 through 24.
This pass verifies the local cover, full relabeling, and primary unit
meanings. It does not regenerate the full parent or solve any cube.

## Scope and checks

Normal and optimized Python runs give identical catalogs, independent
reports, and control reports. Controls reject a missing class, duplicate
class, wrong primary-unit polarity, and wrong representative encoding.
Direct local controls distinguish four disjoint red triangles from a
complete red graph, and detect a planted red K5 with no complete block.

The new classification and normalization bridge await independent
review. The local theorem is solver-free and imports no external Ramsey
value. Its full-graph application imports the accepted parent reduction
and its ordinary unformalized counter and normalization arguments.
Exact Python/runtime/hardware and SHA256 remain trust boundaries. There
is no proof-assistant formalization or historical-priority claim.
