# Proof of the local Gram classification

## 1. Necessary Gram entries

After parity normalization, the row Gram matrix `G` of an order-23 sign
matrix has

\[
G_{ii}=23,\qquad G_{ij}\equiv23\equiv3\pmod4.
\]

If the sign matrix is nonsingular, two rows cannot agree up to sign, so
`|G_ij|<23`.  The complete allowed off-diagonal set is therefore

\[
\{-21,-17,-13,-9,-5,-1,3,7,11,15,19\}.
\tag{1}
\]

Direct multiplication of the published record matrix gives a Gram matrix
`G0` with 208 off-diagonal entries `-1` and 45 entries `3`, and exact Bareiss
elimination gives

\[
\det G_0=L^2,
\qquad L=2779447296000000.
\tag{2}
\]

## 2. Low-rank determinant certificate

The exact inverse reconstructed in both checkers has the form

\[
G_0^{-1}=P/Q,
\qquad Q=170492220,
\tag{3}
\]

where `P` is the integral matrix embedded in `enumerate.cpp`.  Both programs
check `G0 P = Q I` rather than trusting the table.

Let `E=M-G0`, and let `U` be the set of row indices incident with an edited
off-diagonal position.  Write `m=|U|`.  Since `E` is supported on `U x U`,
the matrix determinant lemma gives

\[
\frac{\det M}{\det G_0}
=\det(I+G_0^{-1}E)
=\frac{N}{Q^m},
\quad
N=\det(QI_m+P_{U,U}E_{U,U})\in\mathbb Z.
\tag{4}
\]

Because `det(G0)=L^2` is already a square, `det(M)` can be an integer square
only if the rational number `N/Q^m` is a rational square.  Equivalently,

\[
NQ^m \text{ is an integer square}.
\tag{5}
\]

For every prime `p` not dividing `Q`, condition (5) implies

\[
NQ^m\pmod p
\]

is zero or a quadratic residue.  Thus a single prime for which it is a
nonresidue is an exact nonsquare certificate.

## 3. Exhaustive domains

There are `binom(23,2)=253` off-diagonal positions.  Each entry of `G0` has
ten alternative values in (1).  Hence the arbitrary-edit searches contain

\[
253\cdot10=2530,
\qquad
\binom{253}{2}10^2=3187800
\]

matrices.  The graph-valued neighborhood toggles `-1` and `3`, giving

\[
\binom{253}{3}=2667126,
\qquad
\binom{253}{4}=166695375
\]

matrices at distances three and four.  As an auxiliary overlapping control,
choosing four of the 45 existing `3`-edges to delete gives

\[
\binom{45}{4}=148995.
\]

Within each domain the loops use increasing edge indices, so every matrix
occurs exactly once.

For every matrix, `enumerate.cpp` computes (4) modulo each of 48 primes until
it finds the first nonresidue witness.  The program verifies primality by
trial division, checks that no prime divides `Q`, and validates the record
determinant modulo every prime.  It also checks the complete vector of first-
witness counts stored in `certificate.json`; those counts plus the survivor
count equal the domain size in every case.

## 4. Exact survivors and equality classification

The residue sieve leaves no one-edit or four-deletion matrix.  It leaves 756
two-edit matrices, 24 three-toggle matrices, and 372 four-toggle matrices.
`verify.py` applies direct 23-by-23 integer Bareiss elimination to all 1,152
matrices.  Every survivor does have square determinant, so the modular sieve
loses no further information.  There are 13 determinant values in the
two-edit case, two in the three-toggle case, and five in the four-toggle
case; `certificate.json` records every value, square root, and multiplicity.

The largest roots are respectively

\[
2743271424000000<L,
\qquad
2740715520000000<L.
\]

Among the four-toggle survivors, 360 have root at most

\[
2760297676800000<L.
\]

The remaining twelve have root exactly `L`.  The `3`-edge graph of `G0`
contains the three blocks

\[
\{3,4\mid5,6\},\qquad
\{7,8\mid9,10\},\qquad
\{11,12\mid13,14\}.
\tag{6}
\]

Within each block all four vertices form a clique.  The two vertices to the
right have the same two neighbors in the core triangle, while the two on the
left have neither core neighbor.  Transposing one left vertex with one right
vertex therefore removes two core edges and adds two core edges, changing
exactly four Gram entries.  There are `3*2*2=12` such transpositions, and
simultaneously applying one to the rows and columns gives

\[
M=\Pi G_0\Pi^T=(\Pi R_0)(\Pi R_0)^T.
\tag{7}
\]

The Python checker constructs the edit set of every transposition in (6)
directly from `G0` and verifies that these are exactly the twelve survivors
with root `L`.  Hence every graph-valued square determinant at least `L^2`
through distance four is permutation-congruent to `G0`.  Together with the
arbitrary-entry searches at distances one and two, this proves the
radius-four portion of the lemma in `README.md`.

## 5. The full permutation automorphism group

Regard an off-diagonal entry `3` as an edge.  The resulting graph has three
connected components, on the vertex sets

\[
\{0,\ldots,14\},\qquad \{15,16,17,18\},\qquad
\{19,20,21,22\}.
\tag{8}
\]

In the first component, `0,1,2` are exactly the degree-six vertices and form
a triangle.  For each core vertex `c`, there is a four-clique split into two
inactive twins and two active twins: the inactive pair has no core neighbor,
while the active pair is adjacent to the two core vertices other than `c`.
These are precisely the three blocks in (6), indexed by their missing core
vertex.

Consequently an automorphism of the 15-vertex component first permutes the
core triangle, which forces the corresponding permutation of the three
four-cliques, and then independently swaps each of the six twin pairs.  All
these choices preserve the graph, so this factor is

\[
C_2^6\rtimes S_3,\qquad |C_2^6\rtimes S_3|=64\cdot6=384.
\tag{9}
\]

The other two components are indistinguishable copies of `K4`.  Their
automorphism group is

\[
(S_4\times S_4)\rtimes C_2=S_4\mathop{\rm wr}C_2,
\qquad |S_4\mathop{\rm wr}C_2|=24^2\cdot2=1152.
\tag{10}
\]

Component sizes preclude mixing either `K4` with the 15-vertex component,
and every cross-component Gram entry is `-1`.  Thus

\[
\operatorname{Aut}(G_0)
=(C_2^6\rtimes S_3)\times(S_4\mathop{\rm wr}C_2),
\qquad |\operatorname{Aut}(G_0)|=442368.
\tag{11}
\]

`symmetry.py` reconstructs this description from `record23.txt`, explicitly
generates all 384 and 1,152 factor elements, verifies that each preserves
`G0`, and verifies that the stated 13 elementary generators close to the two
complete factors.

## 6. Burnside counts for edit sets

Every automorphism of `G0` induces a permutation of the 253 unordered vertex
pairs.  If the induced cycle lengths of an element `g` are
`l_1,...,l_t`, the number of size-`k` edit sets fixed by `g` is

\[
[x^k]\prod_{i=1}^t(1+x^{l_i}).
\tag{12}
\]

The first and second factors have respectively 17 and 16 distinct combined
vertex/pair action types.  For a vertex cycle of length `a` in the first
factor and one of length `b` in the second, their Cartesian product on cross
pairs consists of `gcd(a,b)` cycles of length `lcm(a,b)`.  This constructs
the complete induced action and gives 154 distinct pair-action cycle types.
Averaging (12), with exact integer arithmetic, proves the orbit counts in
`symmetry_certificate.json`.  For example,

\[
N_4=197931,\qquad N_5=4132509,\qquad N_6=81094402.
\tag{13}
\]

Because simultaneous row/column permutation preserves the determinant, one
determinant evaluation per edit-set orbit is sufficient.  Equation (13)
therefore reduces the radius-five search from
`binom(253,5)=8,301,429,675` labeled sets to 4,132,509 symmetry classes.

Finally, `symmetry.py` applies its 13 generators directly to the 372
distance-four survivors emitted by `enumerate.cpp`.  They split into six
orbits:

| square root of determinant | orbit size |
|---:|---:|
| 2,779,447,296,000,000 | 12 |
| 2,760,297,676,800,000 | 24 |
| 2,760,297,676,800,000 | 24 |
| 2,722,666,905,600,000 | 24 |
| 2,696,085,504,000,000 | 96 |
| 2,695,954,432,000,000 | 192 |

The orbit sizes sum to 372.  In particular, the record-equality shell is one
orbit, while equality of determinant does not merge the two distinct
24-element orbits at the next determinant value.

## 7. Canonical generation at radius five

The Burnside calculation predicts the number of orbits but does not produce
representatives.  `radius5.cpp` uses a different, constructive quotient.
View a five-toggle set as a simple graph `H` with five edges, omitting its
isolated vertices.  Each connected component with `e` edges has at most
`e+1` vertices.  Exhausting all simple graphs on at most six vertices and
canonicalizing under the full symmetric group gives the following numbers
of connected unlabeled shapes:

| edges | 1 | 2 | 3 | 4 | 5 |
|---:|---:|---:|---:|---:|---:|
| connected shapes | 1 | 1 | 3 | 5 | 12 |

Thus there are only 22 connected shapes relevant through radius five.  This
small shape census is generated at runtime rather than stored as an input.

The component structure in Section 5 divides the 23 vertices into 11 bins:

\[
(C_c,I_c,A_c)\quad(c=0,1,2),\qquad K_0,K_1,
\tag{14}
\]

with capacities `(1,2,2)` for each indexed triple and capacities `(4,4)`
for the two `K4` bins.  The normal subgroup

\[
N=C_2^6\times S_4^2
\tag{15}
\]

acts as the complete symmetric group within every bin.  Consequently,
`N`-orbits of edit graphs are exactly isomorphism classes of graphs whose
vertices carry the 11 bin colors, subject to the capacities in (14).

For each of the 22 connected shapes, the generator exhausts all valid color
assignments and takes the lexicographically least assignment under the exact
automorphism group of that shape.  It then takes all multisets of colored
connected components whose edge counts form an integer partition of `k` and
whose combined occupancies respect (14).  The uniqueness of connected
components and the nondecreasing order imposed on repeated component types
give exactly one representative of every `N`-orbit.

The quotient `Aut(G0)/N` is `S3 x C2`: `S3` permutes the three indexed
triples in (14), while `C2` swaps `K0` and `K1`.  Keeping the least of the 12
images therefore gives exactly one representative of every full
`Aut(G0)`-orbit.  This proves both coverage and absence of duplicates in the
canonical generator.  The intermediate and final counts are

| `k` | internally colored graphs | full symmetry classes |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 63 | 16 |
| 2 | 2,445 | 380 |
| 3 | 73,707 | 8,887 |
| 4 | 1,886,683 | 197,931 |
| 5 | 42,883,999 | 4,132,509 |

The last column agrees entry-for-entry with the independent cycle-index and
Burnside computation in Section 6.

For each of the 4,132,509 radius-five representatives, `radius5.cpp`
reconstructs a labeled edit set and applies the low-rank exact modular test
of Section 2.  Its edge-index convention is
`index(i,j)=i(i-1)/2+j` for `0 <= j < i < 23`.  The first nonresidue
witnesses account for 4,132,482 classes,
leaving 27 representatives.  `verify_radius5.py` evaluates all 27 determinants
directly by fraction-free Bareiss elimination.  Every survivor is a square,
but the largest square root is only

\[
2743153459200000 < L=2779447296000000.
\tag{16}
\]

The same checker independently traverses each survivor orbit using the 13
generators from Section 5.  The 27 orbit sizes sum to 14,784 labeled edit
sets.  Hence no graph-valued Gram matrix at distance five has square
determinant at least `L^2`.  Combined with Section 4, this proves the
graph-valued assertion in `README.md` through distance five.

## 8. Memory-bounded canonical generation at radius six

Every connected simple graph with six edges is obtained from a connected
five-edge graph in one of two ways.  If it contains a cycle, remove an edge
of that cycle and then add that edge back.  If it is a tree, remove a leaf
and its incident edge and then add the leaf back.  Canonical augmentation of
the 12 five-edge shapes in Section 7 therefore gives the complete six-edge
shape census:

| vertices | 4 | 5 | 6 | 7 | total |
|---:|---:|---:|---:|---:|---:|
| connected six-edge shapes | 1 | 5 | 13 | 11 | 30 |

The 11 seven-vertex shapes are precisely the unlabeled trees on seven
vertices.  `radius6.cpp` independently canonicalizes every augmentation under
the full symmetric group and computes the exact automorphism group of every
resulting shape.

For an edit graph with more than one connected component, every component has
at most five edges, so the stored radius-five colored-component catalogue can
be reused unchanged.  Only the one-part partition `(6)` needs the new shapes.
Their valid color orbits are streamed one shape at a time, and the quotient by
`S3 x C2` is taken before the determinant test.  Thus the radius-six extension
does not materialize a large colored six-edge catalogue.

The exact intermediate counts are

| component case | internally colored graphs | full symmetry classes |
|---|---:|---:|
| connected | 43,702,833 | 4,361,518 |
| disconnected | 844,837,661 | 76,732,884 |
| total | 888,540,494 | 81,094,402 |

The final total is exactly the independent Burnside coefficient `N_6` from
(13).  This agreement checks both coverage and absence of duplicate full
orbits.

## 9. Exact radius-six survivors

The modular determinant sieve tests one representative of each of the
81,094,402 classes.  First-nonresidue witnesses account for 81,094,043, leaving
359 representatives.  `verify_radius6.py` directly evaluates all 359
determinants by fraction-free Bareiss elimination.  Every survivor is a
square.  Independent traversal under the 13 generators proves that the 359
representatives are in distinct full orbits whose sizes sum to 420,647.
There are 298 distinct square roots.

Exactly two roots exceed the published record:

| edge indices | square root | orbit size |
|---|---:|---:|
| `(10,22,38,47,89,92)` | 2,823,605,452,800,000 | 96 |
| `(2,11,36,38,46,78)` | 2,783,182,848,000,000 | 48 |

Here `index(i,j)=i(i-1)/2+j` as in Section 7.  All 23 leading principal minors
of both matrices are positive, checked exactly, so the two exceptional Grams
are positive definite.  The next largest square root is

\[
2771425689600000<L.
\tag{17}
\]

## 10. Exact sign-column obstructions

Let one of the exceptional matrices be `G`, and suppose `G=R R^T` for an
invertible sign matrix `R`.  Then

\[
R^T G^{-1}R=R^T(RR^T)^{-1}R=I.
\tag{18}
\]

Consequently every column `v` of `R` must satisfy

\[
v^T G^{-1}v=1.
\tag{19}
\]

Column negation preserves (19) and the Gram decomposition, so normalize
`v_0=1`.  There are exactly `2^22` normalized sign vectors.  For the two
candidates, `candidate_obstructions.py` computes and verifies integral scaled
inverses `G^{-1}=P/Q` with

\[
Q=51563888640\quad\hbox{and}\quad Q=18035310240,
\tag{20}
\]

respectively.  It checks `GP=QI` entry by entry and enumerates the normalized
cube in binary-reflected Gray order.  When coordinate `k` is flipped, the
integer quadratic form `v^T P v` is updated exactly using

\[
q(v-2v_ke_k)=q(v)-4v_k\sum_{j\ne k}P_{kj}v_j.
\tag{21}
\]

For the larger candidate, no normalized sign vector satisfies
`v^T P v=Q`, so it cannot contain even one column of a decomposition.  For
the smaller candidate exactly 48 normalized vectors satisfy the equation,
but every one has `v_0v_1=1`.  If 23 such columns formed `R`, then

\[
G_{01}=\sum_{a=1}^{23}R_{0a}R_{1a}=23,
\tag{22}
\]

contrary to the actual candidate entry `G_01=3`.  Thus neither record-beating
square Gram candidate is sign-decomposable.  As an encoding control, the same
checker reconstructs the published `R0`, computes its scaled inverse, and
verifies (19) for all 23 of its actual columns.  This completes the
graph-valued sign-Gram classification through radius six.
