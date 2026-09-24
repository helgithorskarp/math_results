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
arbitrary-entry searches at distances one and two, this proves the original
radius-four classification and the first two arbitrary shells.  Section 8
extends the arbitrary-entry conclusion through distance three.

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

## 8. Arbitrary-entry covering quotient at radius three

At exactly three edited positions there are
`binom(253,3)*10^3 = 2,667,126,000` matrices when every new entry may be any
of the ten alternatives in (1).  Direct labeled enumeration is unnecessary.
The component generator in Section 7 produces exactly one representative of
each underlying three-position edit set under `Aut(G0)`.  It produces 73,707
orbits under the normal subgroup (15), and quotienting by `S3 x C2` leaves
8,887 representatives, exactly the independently computed Burnside count
`N_3` from Section 6.

For every underlying representative, `radius3_arbitrary.cpp` tests all
`10^3=1,000` ordered assignments of alternative legal values to its three
sorted positions.  This gives 8,887,000 determinant evaluations.  It is a
cover rather than an asserted canonical quotient of valued edits: the
stabilizer of an underlying representative may identify two assignments.
Completeness is nevertheless immediate.  Given any labeled valued edit,
choose an automorphism carrying its underlying position set to the generated
representative; transporting the three values along the same automorphism
produces one of the 1,000 assignments tested there.

The 48-prime sieve assigns a first nonresidue witness to 8,882,175
evaluations and leaves 4,825 survivor encodings.  The independent checker
rebuilds `G0` from `record23.txt`, validates the encodings, and evaluates all
4,825 full 23-by-23 determinants by fraction-free Bareiss elimination.  Every
survivor is a square.  There are 880 distinct roots, and the largest is

\[
2740715520000000<L=2779447296000000.
\]

Thus no legal three-position edit has square determinant at least `L^2`.
Together with Sections 3--4, this proves part 1 of the lemma in `README.md`
through arbitrary distance three.

## 9. Memory-bounded canonical generation at radius six

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

## 10. Exact radius-six survivors

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

## 11. Exact sign-column obstructions

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

## 12. Symmetry-compressed sign-column certificate

The full `2^22` Gray-code check in Section 11 has a much smaller exact
quotient.  Write `G_1,G_2` for the two exceptional Grams in the order displayed
in Section 10.  Direct inspection of the edited edges gives the following
row-permutation subgroups:

\[
H_1=C_2^2\times(S_4\mathop{\rm wr}C_2),\qquad |H_1|=4608,
\]

where the two `C2` factors swap `(3,4)` and `(9,10)`, and

\[
H_2=C_2^3\times(S_4\mathop{\rm wr}C_2),\qquad |H_2|=9216,
\]

where the three `C2` factors swap `(3,4)`, `(7,8)`, and `(11,12)`.  In both
cases `S4 wr C2` independently permutes the two four-sets
`{15,16,17,18}` and `{19,20,21,22}` and exchanges the sets.  Every other
vertex is fixed.  In particular, both groups fix vertices zero and one.
`candidate_orbit_obstructions.py` checks each displayed generator directly
against both `G_i` and its exact scaled inverse numerator `P_i`.

Consequently a normalized sign vector is classified under `H_i` by:

- its signs on every fixed vertex other than vertex zero;
- the number `0,1,2` of negative signs in each interchangeable pair; and
- the unordered pair `(a,b)`, with `0<=a<=b<=4`, of negative counts in the
  two interchangeable four-sets.

There are 15 possibilities for `(a,b)`.  Hence the complete normalized cube
for the first candidate has only

\[
2^{10}3^2\cdot15=138240
\]

canonical representatives.  For the second obstruction, the forbidden
condition `v_0v_1=-1` becomes `v_1=-1` after normalizing `v_0=1`; since
`H_2` fixes vertex one, it leaves only

\[
2^7 3^3\cdot15=51840
\]

representatives.  Orbit multiplicities are elementary: a pair with `k`
negative signs contributes `binom(2,k)`; the two four-sets contribute
`binom(4,a)^2` when `a=b` and
`2 binom(4,a)binom(4,b)` when `a<b`.  Summing these products gives exactly
`2^22` normalized columns in the first census and `2^21` columns in the
forbidden second census, so this is an exact quotient rather than a sample.

Exact evaluation of `v^T P_i v` on the canonical representatives finds no
solution for `G_1` and none in the forbidden `v_1=-1` half for `G_2`.  As a
positive and multiplicity control, the unrestricted `G_2` quotient has
103,680 representatives and exactly two solution orbits, of sizes 32 and 16.
Their union is exactly the 48 columns found by the independent Gray-code
enumeration.  `verify_candidate_orbit_obstructions.py` reconstructs that full
enumeration, expands the two reported orbits from explicit generators, and
requires exact equality of the two 48-element sets.  This supplies a compact
structural certificate for both contradictions in Section 11.

### Retained SAT experiment

As a separate certificate experiment, write `v_i=(-1)^{x_i}` and
`y_ij=x_i xor x_j`.  If `q_+` is the all-plus value, then

\[
v^T P v=q_+-4\sum_{i<j}P_{ij}y_{ij}.
\]

`candidate_sat_certificates.py` converts this exact weighted equality to a
34- or 35-bit Tseitin ripple-adder CNF.  CaDiCaL 3.0.1 proved the two target
instances UNSAT, while the unrestricted second-candidate control was SAT and
its model satisfied every clause and the decoded integer quadratic identity.
The respective CNF SHA-256 values are
`1b4feba975193380c1e0d7e5b161c43e6a87454dadbd373b3accb3ea9c727019`,
`2af668ee1f3ae525cde318ded8ba5989249c4a2ff1c31ca71e2ade27ca31f822`,
and `383532438d208952cd5bee6a844fd8f0887f212c202179a1149b8fa23e7b2248`
for the positive control.
The binary DRAT traces had sizes 35,664,691 and 34,108,768 bytes.  Their
SHA-256 values were
`afef22e578dc70bddab625ee250fcc028bbff7add0f0eb1a50e0842b2c69e8ee`
and `cf7e1d3abfa0cdb286f5b91e780544a305800fb82672b0af44b98e0fb057d2fe`.
Independent `drat-trim` verification succeeded, but core extraction produced
still larger 67 MiB and 60 MiB ASCII proofs.  Those bulky generated traces are
deliberately not published; the generator, exact CNF hashes, solver versions,
and negative size result are retained to make the abandoned certificate
direction reproducible.  The compact symmetry quotient above is the published
proof artifact.

## 13. A second H-class over the same Gram center

Two sign matrices are Hadamard-equivalent when one is obtained from the other
by signed row and column permutations.  `record23_class2.txt` gives a second
matrix `R1`.  Exact elimination in `verify_multicenter.py` and two-prime exact
CRT reconstruction in `multicenter.cpp` independently give

\[
|\det R_1|=|\det R_0|=2779447296000000.
\tag{23}
\]

The two-prime reconstruction is exact because the prime product exceeds
twice the order-23 Hadamard bound.  Both primes are checked at runtime.

### Structured switch census

Use the three blocks from (6), now written as ordered pairs of twin pairs:

\[
B_0=(\{7,8\},\{9,10\}),\quad
B_1=(\{3,4\},\{5,6\}),\quad
B_2=(\{11,12\},\{13,14\}).
\tag{24}
\]

For every core vertex `c` independently choose a block `B_m`, one of its two
pairs `C`, and one of its two pairs `D`.  Flip the two entries in row `c` and
columns `C`, and the two entries in column `c` and rows `D`.  Each core has
`3*2*2=12` choices, giving exactly `12^3=1728` specified matrices.  Direct
exact determinant evaluation finds 770 distinct absolute values.  The maximum
is the record (23), attained by exactly two labeled choices; all other choices
are smaller.  The choice

```text
((block 1, pair 1, pair 0),
 (block 0, pair 1, pair 0),
 (block 2, pair 1, pair 0))
```

is exactly `R1`, so the witness is generated rather than inserted without a
derivation.

### Signed Gram congruences

Let `G1=R1 R1^T`.  In zero-based notation define

```text
p = (0,1,2,5,6,11,12,9,10,3,4,13,14,7,8,15,16,17,18,19,20,21,22)
s = (1,1,1,-1,-1,1,1,-1,-1,1,1,-1,-1,1,1,1,1,1,1,1,1,1,1).
```

Entrywise exact multiplication verifies

\[
(G_1)_{ij}=s_i s_j(G_0)_{p_i p_j}.
\tag{25}
\]

The analogous column-Gram identity uses

```text
p' = (1,2,0,5,6,11,12,9,10,3,4,13,14,7,8,15,16,17,18,19,20,21,22)
s' = (1,1,1,1,1,-1,-1,1,1,-1,-1,1,1,-1,-1,1,1,1,1,1,1,1,1).
```

Thus both Grams of `R1` lie in the same signed-permutation classes as those
of `R0`.  In particular, applying (25) transports the radius-six local Gram
theorem to this second matrix class.

### Exact H-inequivalence

Hadamard equivalence bijects the `k`-by-`k` minors and preserves their
absolute determinants.  Exhausting all
`binom(23,4)^2=78,411,025` four-minors gives

| matrix | `|det|=0` | `|det|=8` | `|det|=16` |
|---|---:|---:|---:|
| `R0` | 45,245,701 | 31,659,704 | 1,505,620 |
| `R1` | 45,247,429 | 31,657,400 | 1,506,196 |

The counts in either row sum to 78,411,025; their disagreement proves that
`R0` and `R1` are not H-equivalent.  The C++ checker obtains each 4-minor by
normalizing its first row and column and reducing it to eight times the
determinant of a 3-by-3 zero-one matrix.

For an independent invariant, fix four rows and regard every column sign
pattern modulo complement, giving eight projective patterns.  Canonicalize
the eight-bin histogram under all 192 signed permutations of the selected
four rows, then take the multiset over all 8,855 row subsets.  Signed row and
column permutations preserve this multiset.  The canonical signature

```text
(2,3,3,2,3,3,3,4)
```

has multiplicity 2,508 for `R0` and 2,460 for `R1`.  The complete profiles
have respectively 29 and 31 signature types and SHA-256 values
`7c65ef560b5f9f212909c2bb8e982dfbee240ec989031fcbf4b752bff357c90b`
and
`b5fd7c94de3fe7d27f7e9bf40054584a6710f8e322ac2237138586de8bc792c9`.
This second certificate is definition-level Python and does not rely on
nauty or another graph-isomorphism implementation.

## 14. Complete sign decompositions of the record Gram

Let `G=G0` and write its exact inverse as `G^-1=P/Q`, where the integer
table in `order23_inverse.hpp` has `Q=170492220`.  If a sign matrix `R`
satisfies `R R^T=G`, then

\[
R^T G^{-1}R=I.
\tag{26}
\]

Column negation does not change a Hadamard class, so normalize every column
`v` by requiring `v_0=1`.  Equation (26) says that every normalized column
must satisfy

\[
v^T P v=Q,
\tag{27}
\]

and two distinct columns must satisfy `v^T P w=0`.  Conversely, suppose 23
normalized sign vectors obey (27) and are pairwise orthogonal for this
bilinear form.  The matrix `V` having these vectors as columns satisfies
`V^T G^-1 V=I`, so it is invertible and

\[
G^{-1}=V^{-T}V^{-1},\qquad G=VV^T.
\tag{28}
\]

Thus no extra decomposition condition remains: the decompositions are
exactly the 23-cliques in the compatibility graph below.

### Exact compatibility and clique census

`gram_decompositions.cpp` traverses all `2^22` normalized sign vectors by a
Gray code and evaluates (27) with signed 64-bit integer arithmetic.  It finds
exactly 1,382 candidates.  Encoding their Gray-code traversal order as one
decimal mask per line gives SHA-256

```text
bc8cd93dff3f9d88ffddcf428f4d107d452be4a197ec902fc53364f3cfd05ecb
```

The compatibility graph joins `v` and `w` precisely when `v^T P w=0`.  It
has 338,582 edges and degree distribution

| degree | vertices |
|---:|---:|
| 440 | 864 |
| 569 | 512 |
| 946 | 6 |

The clique recursion greedily partitions each current candidate set into
independent color classes.  The number of colors is therefore an upper bound
on the size of any extension.  Processing vertices in reverse color order,
intersecting with the chosen vertex's neighborhood, and deleting that vertex
from the current set enumerates every 23-clique exactly once.  The complete
search visits 9,804,083 recursive nodes and finds exactly 552,960 cliques.

`verify_gram_decompositions.py` independently rebuilds the 1,382-vertex
graph with arbitrary-precision Python integers and repeats the clique
recursion using one unbounded integer as each bit set.  It obtains the same
edge, degree, recursive-node, and clique counts.  It also reconstructs every
reported representative as a sign matrix and verifies (28) and the record
determinant by exact Bareiss elimination.

### From decomposition orbits to H-classes

After column signs and column order have been removed, the remaining action
on decompositions of this fixed `G` is its signed row stabilizer.  Every
off-diagonal entry of `G` is nonzero.  Taking absolute values shows that the
permutation part of a signed stabilizer preserves the `3`-edge graph and
hence belongs to `Aut(G)` from Section 5.  Removing that permutation leaves
a diagonal sign matrix `D` with `DGD=G`; the nonzero off-diagonal entries
force all signs of `D` to be equal.  The resulting global row negation is
removed again by the normalized-column convention.  Consequently the
effective action is exactly `Aut(G)`, of order 442,368.

The thirteen generators from Section 5 induce four orbits of candidate
columns, of sizes 6, 432, 432, and 512.  Exact orbit traversal on the full
clique set gives fourteen orbits:

| number of orbits | orbit size | stabilizer order |
|---:|---:|---:|
| 6 | 18,432 | 24 |
| 8 | 55,296 | 8 |

Their sizes satisfy

\[
6\cdot18432+8\cdot55296=552960,
\tag{29}
\]

so the orbits exhaust the independent clique census.  The canonical mask
tuple for every orbit appears in `gram_decomposition_certificate.json`.
The published matrix `R0` lies in class 14 and the matrix `R1` from Section
13 lies in class 13.

This proves exactly fourteen H-classes among the sign decompositions of the
specified published Gram `G0`.  It does not prove that every order-23 matrix
at the record determinant has a Gram signed-permutation-equivalent to `G0`,
nor does it determine `D(23)`.

## 15. Transpose duality of all fourteen classes

Let `R_i`, for `1<=i<=14`, be the canonical representative reconstructed
from class `i` in `gram_decomposition_certificate.json`.  For every `i`, the
new certificate gives permutations `p_i,q_i` of `{0,...,22}` and sign
vectors `d_i,e_i` such that, entrywise,

\[
(R_{\tau(i)})_{p_i(a),q_i(b)}
   =d_i(a)e_i(b)(R_i^T)_{a,b}.
\tag{30}
\]

These are ordinary signed row and column operations, so (30) is an explicit
Hadamard equivalence rather than an invariant-based identification.  Direct
integer checking gives

\[
\tau=(1\ 11)(2\ 12)(3\ 7)(4\ 8),
\tag{31}
\]

with `5,6,9,10,13,14` fixed.  Equation (31) is an involution, as it must be
because transposing twice returns the original matrix.  Section 14 proves
that the fourteen representatives are exhaustive and mutually
H-inequivalent among decompositions of `G0`; hence (31) is the complete
transpose action on those classes, and its six fixed points are exactly the
self-dual classes.

There is also a Gram consequence.  Write (30) as
`R_tau(i)=A_i R_i^T B_i` for signed permutation matrices `A_i,B_i`.
Since every representative has row Gram `G0`,

\[
G_0=R_{\tau(i)}R_{\tau(i)}^T
   =A_i(R_i^T R_i)A_i^T.
\tag{32}
\]

Thus the column Gram of every one of the fourteen representatives is
signed-permutation-congruent to `G0`.  In particular, both the row and column
versions of the radius-six local theorem apply throughout this complete
fixed-center family.

The producer obtains (30) constructively.  It switches signs in `R_i^T R_i`
so every magnitude-three entry is positive and every magnitude-one entry is
negative.  The magnitude-three graph always has components of orders
`15,4,4` and the degree structure from Section 5, yielding an explicit
permutation to `G0`.  It then traverses the thirteen known generators of
`Aut(G0)` until the normalized columns equal a canonical representative and
extracts the final column signs and order.  None of that search logic is
trusted by the new conclusion: `verify_transpose_duality.py` independently
reconstructs the input and target matrices from their masks, checks that all
reported maps and signs have the required types, and verifies all
`14*23^2` entries of (30) directly.

## 16. A four-orbit factorization of the decomposition census

The thirteen generators of `Aut(G0)` partition the 1,382 candidate columns
into four orbits `O_0,O_1,O_2,O_3`, ordered here by sizes

\[
(|O_0|,|O_1|,|O_2|,|O_3|)=(6,512,432,432).
\tag{33}
\]

Counting, for one vertex in each orbit, its neighbors in all four orbits
gives the equitable quotient

\[
\begin{pmatrix}
2&512&216&216\\
6&131&216&216\\
3&256&73&108\\
3&256&108&73
\end{pmatrix}.
\tag{34}
\]

Exact clique searches in the four induced graphs give the following table.
The fourth column is independently obtained by fixing one vertex; orbit
transitivity then recovers the third column by double-counting
vertex--clique incidences.

| orbit | clique number | maximum cliques | through a fixed vertex |
|---:|---:|---:|---:|
| `O_0` | 3 | 2 | 1 |
| `O_1` | 8 | 276,480 | 4,320 |
| `O_2` | 6 | 11,520 | 160 |
| `O_3` | 6 | 11,520 | 160 |

The anchored checker also finds no clique of the next size in the fixed
vertex neighborhood.  By transitivity this proves the displayed clique
numbers.  In particular,

\[
3+8+6+6=23,
\tag{35}
\]

so every 23-clique in the full compatibility graph must attain all four
induced bounds.  The graph on `O_0` is exactly two disjoint triangles, whose
mask triples are

```text
(3901,15602,4181043), (12541,16142,4190223).
```

Now fix either triangle `T` and any maximum 8-clique `K` in `O_1`.  In each
of `O_2` and `O_3`, intersect the 216 vertices compatible with `T` with the
neighborhoods of all eight vertices of `K`.  Exhaustion of the 276,480
possibilities gives exactly six vertices in each intersection.  Each
six-set is a clique, and the two six-sets are cross-complete.  They therefore
give a decomposition, and (35) shows that they are the only possible
completion of `(T,K)`.  Consequently projection onto `(T,K)` is a bijection
and independently yields

\[
2\cdot276480=552960
\tag{36}
\]

full decompositions.

The maximum cliques of `O_1` form ten automorphism orbits: two of size
9,216, four of size 27,648, two of size 55,296, and two of size 18,432.
For each middle-clique orbit, consider the action on oriented pairs `(K,T)`.
For six orbits the stabilizer of `K` interchanges the two triangles, so their
two extensions merge into one full orbit.  For four orbits it does not, so
the two extensions remain separate.  Hence the number of full orbits is

\[
6+2\cdot4=14.
\tag{37}
\]

The resulting full orbit sizes are six copies of 18,432 and eight copies of
55,296, agreeing with Section 14.  `gram_factorization_certificate.json`
records the ten canonical middle cliques, stabilizer orders, merge/split
flags, and corresponding full-class labels.  The producer uses greedy-color
branch-and-bound on the four induced graphs.  The independent checker instead
uses elementary ordered recursion only inside one fixed vertex neighborhood,
expands the ten reported group orbits, and checks both forced completions of
each representative.  Thus (36)--(37) do not depend on the original
9,804,083-node 23-clique search.

## 17. Multiplicity-first generation at radius seven

Canonical augmentation of the 30 connected six-edge shapes is complete by
the same edge-or-leaf deletion argument as Section 9.  It gives

| vertices | 5 | 6 | 7 | 8 | total |
|---:|---:|---:|---:|---:|---:|
| connected seven-edge shapes | 4 | 19 | 33 | 23 | 79 |

The last 23 shapes are precisely the unlabeled trees on eight vertices.
Scanning all `11^8` color words for each tree is unnecessary.  Let `A` be
the automorphism group of a fixed uncolored shape, let `H=S3 x C2` be the
outer color group, and let `n(c)` be the color-multiplicity vector of a
coloring `c`.  The actions of `A` and `H` commute, and `A` fixes `n(c)`.
Choose one lexicographically least multiplicity vector in each `H`-orbit.
If `H_n` is its stabilizer, then the full `(A x H)`-orbits whose chosen
multiplicity vector is `n` are exactly the `(A x H_n)`-orbits of distinct
multiset assignments with multiplicities `n`.  Indeed, any full orbit first
has a unique chosen multiplicity-vector orbit, and two assignments above its
chosen representative are full-equivalent exactly when the color action lies
in `H_n`.  This proves both coverage and uniqueness of the multiplicity-first
quotient.

The implementation enumerates every capacity-bounded vector, takes its exact
`H`-minimum, enumerates its distinct multiset assignments, and compares each
assignment under `A x H_n`.  As a regression test, applying this new method
to all 30 connected six-edge shapes gives exactly 4,361,518 classes, matching
the independent radius-six generator.  On an asymmetric eight-vertex tree,
the new method visits 11,832,590 assignments rather than `11^8` raw words.

The component partition `(6,1)` is handled by adjoining a disjoint edge to
each six-edge shape.  Its automorphism group is the direct product of the
six-edge shape automorphisms and the endpoint transposition.  Thus the same
multiplicity argument applies even when the resulting shape has nine
vertices.  Every other disconnected partition of seven has components of at
most five edges and is generated from the stored catalogue of Section 7.
The connected-component multiset is unique, so these three cases are
disjoint and exhaustive.

The exact counts are

| case | pre-quotient assignments represented | full symmetry classes |
|---|---:|---:|
| connected seven-edge shapes | 321,458,435 | 75,778,019 |
| partition `(6,1)` | 1,225,628,975 | 158,015,168 |
| remaining disconnected partitions | 14,527,883,922 | 1,269,767,232 |
| total classes | -- | 1,503,560,419 |

For the first two rows the middle column counts assignments above canonical
color-multiplicity vectors; for the third it counts internally canonical
colored component multisets, so those middle entries are not intended to be
added as one common orbit statistic.  The final class count is exactly the
radius-seven Burnside coefficient from Section 6.

The computation is divided into 32 disjoint shards.  For multiplicity-first
cases, the canonical multiplicity-vector ordinal chooses the shard.  For a
stored-component partition, the first canonical component index chooses it.
Every generated full orbit therefore belongs to exactly one shard.  The
merger requires all shard labels once, sums every category and first-prime
witness count, rejects duplicate survivors, and requires the Burnside total.

## 18. Exact radius-seven survivors and sign obstructions

First-nonresidue witnesses among the same 48 checked primes reject
1,503,557,476 radius-seven classes and leave 2,943.  Independent fraction-free
Bareiss elimination proves that every survivor determinant is a square.
There are 2,436 distinct square roots, no root equals the record `L`, and the
largest root below it is

\[
2777874432000000<L.
\tag{38}
\]

Exactly 26 square roots exceed `L`; the largest is

\[
2838233088000000.
\tag{39}
\]

All 23 leading principal minors of all 26 candidates are positive.  For each
candidate `G`, `radius7_candidate_obstructions.py` checks an exact scaled
inverse `G^{-1}=P/Q`, verifies `GP=QI`, and exhausts all `2^22` normalized
sign vectors using the Gray-code update (21).  Eleven candidates have no
vector satisfying `v^T P v=Q`.  For fourteen candidates, every admissible
vector has one fixed pair product `v_i v_j=s`, but `23s` differs from the
required entry `G_ij`.  These 25 matrices therefore cannot be sign Grams.

The remaining candidate toggles edge indices

```text
(0,2,10,15,38,55,172)
```

and has square root `2799304704000000`.  It admits 424 normalized columns.
Every one satisfies the exact identity (with zero-based row subscripts)

\[
1+v_{11}v_{13}+v_{11}v_{14}+v_{13}v_{14}=0.
\tag{40}
\]

If 23 such columns formed a sign matrix `R`, summing (40) over the columns
would give zero.  But the three corresponding entries of this candidate
Gram are all 3, so `RR^T=G` would instead make the sum

\[
23+G_{11,13}+G_{11,14}+G_{13,14}=23+3+3+3=32,
\tag{41}
\]

a contradiction.  Thus all 26 record-beating square Gram orbits are
indecomposable.  Combined with the radius-six equality classification, this
proves graph-valued local sign maximality and record-equality classification
through distance seven.

`verify_radius7.py` independently recomputes the Burnside coefficient, all
2,943 determinants, the survivor-stream hash, every scaled inverse, all 26
full normalized sign cubes, and each displayed obstruction.  The modular
sieve never certifies a square; it only reduces the list on which exact
integer arithmetic is performed.

## 19. Arbitrary legal entries through radius four

At exactly four edited positions, allowing any of the ten alternatives in
(1) gives

\[
{253\choose4}10^4=1666953750000
\tag{42}
\]

labeled matrices.  The colored-component construction of Section 7, stopped
after four edges, gives the following independent partition census:

| component partition | internally colored graphs | full edit-set orbits |
|---|---:|---:|
| `(4)` | 142,566 | 16,797 |
| `(3,1)` | 447,294 | 48,567 |
| `(2,2)` | 164,757 | 17,874 |
| `(2,1,1)` | 806,188 | 82,215 |
| `(1,1,1,1)` | 325,878 | 32,478 |
| total | 1,886,683 | 197,931 |

The last total is exactly the independently computed Burnside coefficient
`N_4` in (13).  For each underlying representative,
`radius4_arbitrary.cpp` tests all `10^4` assignments of alternative legal
values to its sorted edges.  Hence it evaluates

\[
197931\cdot10^4=1979310000
\tag{43}
\]

matrices.  As at radius three, this is a complete cover rather than an exact
valued-edit orbit quotient: transporting any labeled valued edit to its
generated underlying representative carries its values to one of the tested
assignments.  Stabilizers may cause harmless repetition but cannot cause an
omission.

The enumeration is divided into 32 disjoint shards.  A fixed 64-bit hash of
the sorted connected-component identifiers assigns each internally colored
component multiset to one shard before the outer `S3 x C2` test.  Thus every
internal object, and consequently every accepted full representative, is
assigned exactly once.  The merger requires every shard label once, the five
partition totals above, the Burnside total, and closed first-witness
accounting.

The 48-prime sieve rejects 1,978,319,590 assignments and retains 990,410.
For every survivor the merger evaluates the matrix determinant lemma exactly.
If the changed positions involve the vertex set `U`, of size at most eight,
and `E` is the supported perturbation, then the checked scaled inverse
`G0^-1=P/Q` gives

\[
\det(G_0+E)=L^2\frac{\det(QI+P_{U,U}E_{U,U})}{Q^{|U|}}.
\tag{44}
\]

Fraction-free Bareiss elimination over Python integers evaluates the small
determinant in (44); exact division by `Q^{|U|}` is required.  All 990,410
survivors are squares.  Exactly 990,408 have root below `L`, with largest
root `2760297676800000`.  One has root exactly `L`; its encoding belongs to
the explicit 12-element row-permutation orbit from Section 4.

The sole above-record square has edits

```text
(23,-21), (105,19), (110,-21), (178,-21)
```

and root `2791505920000000`.  It is not positive definite.  Exact
fraction-free Sylvester elimination finds its first nonpositive leading
principal minor at order 14, with value

\[
-43620761600000.
\tag{45}
\]

Every nonsingular sign Gram `RR^T` is positive definite.  Therefore (45)
eliminates the only arbitrary-entry radius-four square above the record;
the unique equality orbit is already realized by row permutations of `R0`.
Together with Section 8, this proves local sign maximality and equality
classification for every legal Gram edit through arbitrary distance four.

`verify_radius4_arbitrary.py` independently recomputes the Burnside
coefficient, both retained full 23-by-23 determinants, the equality
row-permutation encoding, and all leading minors through the obstruction in
(45).  Canonical SHA-256 digests bind the complete survivor stream and its
exact roots.  The modular sieve is only a lossless rejection stage; the final
claims use exact integer arithmetic throughout.
