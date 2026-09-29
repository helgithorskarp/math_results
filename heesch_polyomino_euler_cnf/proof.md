# Exact finite reduction for square-grid polyomino coronas

Author/role: six-heesch-1, researcher. Date: 2026-09-29.

This is a proved combinatorial reduction, with implementation regression checks.
It establishes no new finite Heesch record. Its scope is copies aligned to one
unit square grid, including all quarter turns and reflections. An upper bound in
this model must not be asserted for arbitrary rigid motions without an additional
alignment argument. The local Euler identity is classical, not a novelty claim;
the contribution is its explicit integration with a finite, cumulative corona
encoding, including every prefix and an explicit topological-disc option.

## 1. Exact conventions

A cell p=(x,y) denotes the **closed** unit square [x,x+1]×[y,y+1]. A tile P is a
finite nonempty union of such cells, homeomorphic to a closed disc. Copies have
disjoint cell sets; they may share boundary segments or points. Halo(X) is every
unoccupied cell at Chebyshev cell distance one from X. Thus corner contacts count.

A depth-H grid corona is a sequence of finite sets of copies C_0,...,C_H. C_0
contains the prescribed root P. Write X_k for the union of cells in C_0,...,C_k.
Every copy added in C_k, k>0, touches X_{k-1}, and Halo(X_{k-1})⊆X_k. The latter
condition says exactly that the entire boundary of X_{k-1} is interior to the
closed union X_k, including its vertices. Require either:

- hole-free prefixes: each X_k is connected and has no bounded complementary
  component, allowing boundary pinches; or
- disc prefixes: each X_k is homeomorphic to a closed disc.

For the convention permitting holes only in the last corona, impose the chosen
topology condition through H-1 and omit it at H. Connectedness still holds at H.
The implementation defaults to disc prefixes; `--allow-pinches` selects the first
option and `--holes-last` relaxes only the last prefix. These choices must be
reported with any computed classification.

## 2. Local topology lemma (classical Euler counting)

For a finite cell set X, let:

- F be its number of cells;
- A be the number of side-adjacent pairs of occupied cells;
- B be the number of 2×2 blocks with all four cells occupied;
- D be the number of 2×2 blocks with exactly two diagonally opposite cells occupied.

Then its closed-square cell complex has

    χ(X) = F - A + B - D = c - h,

where c counts connected components of the closed union (eight-neighbour cell
connectivity) and h counts bounded complementary components (four-neighbour
connectivity of unoccupied cells).

**Proof.** Each occupied square contributes four edge occurrences. A shared side
is counted twice, so the number of distinct edges is E=4F-A. To count distinct
vertices, begin with 4F vertex occurrences. At a lattice vertex incident with r
occupied cells, r>0, the reduction in occurrences is r-1. The number of occupied
side pairs incident at that vertex is r-1 except in two cases: four occupied cells
give four pairs rather than three, and exactly two diagonal cells give zero pairs
rather than one. Summing over vertices, each side pair is counted twice, so

    V = 4F - 2A + B - D.

Substitution in V-E+F gives the first identity. The planar graph formed by all
occupied-cell edges and vertices has c components. Its faces consist of the F
occupied open squares, the h bounded complementary components, and the unbounded
face. The planar Euler formula V-E+faces=1+c yields the second identity. The
complement uses four-neighbour connectivity because a shared edge of two empty
cells contains no occupied point, whereas diagonally adjacent empty cells have
their intervening vertex blocked if either other cell at that vertex is occupied.
The empty set has c=h=χ=0 and satisfies the identity as well. ∎

**Corollary.** If X is connected and nonempty, it is hole-free exactly when

    F + B = A + D + 1.

Moreover, X is a closed disc exactly when this equality holds and D=0.

**Proof of the disc assertion.** Necessity of D=0 follows because two diagonal
quadrants at a vertex have a disconnected punctured neighbourhood, unlike a disc
or half disc. If D=0, the occupied quadrants at every vertex form one cyclic
interval or the full circle. All points therefore have disc or half-disc
neighbourhoods: X is a compact planar 2-manifold with boundary. Its boundary
edges form disjoint simple polygonal cycles. Connectedness gives one exterior
cycle; every additional cycle bounds a complementary component. When h=0 there
is just one cycle, and its filled bounded side is X, a closed disc by the polygonal
Jordan–Schoenflies theorem. ∎

Connectedness is essential. For example, a disjoint square and a disjoint
eight-square 3×3 ring have c=2,h=1,χ=1; imposing only the equality does not forbid
their hole. Similarly two diagonal squares have c=1,h=0,χ=1,D=1: they are
hole-free but fail the disc convention.

Local Euler counting is established prior art, including S. B. Gray, *Local
Properties of Binary Images in Two Dimensions*, IEEE Transactions on Computers
C-20(5), 551–561 (1971), DOI [10.1109/T-C.1971.223289](https://doi.org/10.1109/T-C.1971.223289).
The proof above is included so the reduction does not depend on an imported
formula with the wrong diagonal-connectivity convention.

## 3. A linear-size topology CNF

Let u_p be exact occupancy bits on a finite set of N possible cells, with all
other cells fixed false. Define each side-pair bit as an AND of its two cell
bits, each full-block bit as an AND of four bits, and each diagonal-block bit as
the OR of its two exact diagonal patterns. There are at most 2N side pairs and
4N relevant blocks; each pattern has constant-size definitional CNF.

The Euler equality is one cardinality equality:

    Σ u_p + Σ full_block + Σ ¬side_pair + Σ ¬diagonal_block
        = number_of_side_pairs + number_of_diagonal_blocks + 1.

Repeated literals, if any, are counted with multiplicity. A balanced tree of
unsigned binary adders counts its O(N) literals exactly. At merging level j,
there are O(N/2^j) additions of O(j)-bit integers. Hence the total gate count is
O(N·Σ j/2^j)=O(N). Each XOR, AND, and majority gate has constant-size defining
CNF, and fixing the final sum uses O(log N) unit clauses. The compiler therefore
adds O(N) variables, clauses **and literal occurrences**. Its auxiliary variables
have a unique extension for each occupancy assignment. No holes are enumerated.
For disc prefixes, add one clause forbidding each diagonal pattern.

Applying this independently to H connected prefixes adds O(HN) topology size.
It does not assert that the resulting formula solves faster than lazy cuts.

## 4. Finite candidate completeness

Normalize P so its minimum x and minimum y are zero. Let its maximum coordinates
be a,b, and L=max(a+1,b+1), the larger bounding-box side in cells. Every copy has
cell-coordinate Chebyshev diameter at most L-1.

Every cell belonging to a copy in C_k lies in

    [-kL, a+kL] × [-kL, b+kL].

**Proof.** The bound holds at k=0. A newly added copy touches an earlier copy, so
some cell q of the new copy is within Chebyshev distance one of a cell p in the
preceding prefix. Every other cell r in the new copy is within L-1 of q. Thus r
is within L of p. Induction gives the stated coordinate bound. ∎

For a requested depth H, enumerate every oriented copy wholly contained in the
H-box and disjoint from P. Deduplicate the at most eight normalized orientations.
No packing can use two identical occupied-cell copies. Exclude a candidate from
prefix k if it is not wholly inside the k-box. The bound proves these exclusions
complete; they do not require any experimental maximum Heesch number or an
assumed search radius. If the H-box contains N cells, there are at most 8N copies.

## 5. Cumulative corona encoding and soundness/completeness

For each candidate Q and k=1,...,H, let z_{Q,k} mean Q has appeared by level k.
Set z_{Q,0}=false. For the root, every z_{P,k}=true. Geometrically excluded z bits
are fixed false. Define u_{p,k} iff some z_{Q,k} with p∈Q is true, including P.
Impose:

1. z_{Q,k} implies z_{Q,k+1}.
2. For each cell p, at most one candidate covering p is selected at level H.
3. If z_{Q,k} becomes true for the first time, some cell in Halo(Q) is occupied
   in prefix k-1.
4. If z_{Q,k} is true and k<H, every cell in Halo(Q) is occupied in prefix k+1.
   Also require every root halo cell occupied at level one when H>0.
5. On every topology-constrained prefix, impose the CNF from Section 3, including
   diagonal suppression if the disc convention is chosen.

The clauses are satisfiable **if and only if** an admissible depth-H grid corona
exists under the selected convention.

**Soundness.** Monotonicity assigns every selected copy a unique first level.
Final nonoverlap implies nonoverlap in every prefix. Exact cell definitions make
the u bits precisely these prefix unions. Each new copy touches the preceding
union, so induction from the root proves connectedness of every prefix. Halo
closure gives complete surrounds of successive prefixes; the topology lemma
gives the selected hole-free/disc condition at each required level. Thus decoding
gives a corona with every stated property.

**Completeness.** For an admissible corona, the finite-bound lemma places every
copy in the enumerated set at every level at which it is used. Set z_{Q,k} true
exactly when Q has already appeared and set u to the exact occupied-cell unions.
Nonoverlap, first-appearance contact, halo closure, and topology give all the
listed constraints. The definitional circuits and sequential at-most-one
encoding admit extensions; therefore the whole CNF is satisfiable. ∎

**Redundant adjacency lemma.** With prefixwise halo closure and nonoverlap, two
selected copies in levels whose difference exceeds one cannot touch. Indeed,
if Q appears at j≥i+2 and touches a copy R in level i, a cell of Q is in
Halo(R)⊆X_{i+1}. That cell belongs to both Q and an earlier copy, contradicting
nonoverlap. In particular, first-appearance contact is contact with the immediately
preceding level, and decoded levels are the contact-graph distances from P.
No separately generated nonconsecutive-contact exclusion clauses are required.

Let m=|P|. Occupancy definitions use O(HNm) total incidences; halo/contact clauses
also have O(HNm) literal occurrences. Sequential cell-wise at-most-one encodings
use O(Nm) space. Including topology, the entire construction is O(HNm) in
variables, clauses and literal occurrences, using the finite N-cell H-box and
M≤8N candidates. This is a worst-case size bound, not a runtime guarantee.

## 6. Relationship to prior work and trust boundaries

Kaplan's [2022 paper](https://cdm.ucalgary.ca/article/view/72886), Sections 3.1–3.2,
already gives the grid-corona SAT reduction and handles outer holes by pairwise
exclusions and iterative flood-fill cuts. His [current implementation](https://github.com/isohedral/heesch-sat)
also uses flood-fill hole detection. The topology compiler here applies classical
Euler counting instead. Its other implementation choice is cumulative selected
copy variables and exact occupancy of each prefix, rather than final-only cell
occupancy. No claim is made that the old census is incorrect or that this is the
first use of Euler constraints in satisfiability.

The mathematical reduction has the elementary proofs above; it is not formally
verified in a proof assistant. The finite exhaustive checks test the implementation,
not the universal theorem. SAT existence witnesses are checked using separate
direct geometry, flood fill, and halo coverage. A reported solver UNSAT is only
solver evidence unless its proof is independently checked. Timeout, resource
termination and incomplete runs give no upper bound. Any future finite Heesch
classification also needs its stated admissibility convention and candidate
completeness to match this theorem.
