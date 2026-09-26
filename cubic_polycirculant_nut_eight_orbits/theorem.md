# A real-character obstruction for eight cyclic orbits

## Statement

All graphs in the theorem are finite, simple, and undirected. A **nut graph**
is a nontrivial graph whose adjacency matrix has nullity one and whose
nonzero null vectors have no zero coordinate. An **ell-circulant** graph
admits an automorphism consisting of ell cycles of one common length m.

**Theorem.** There is no cubic eight-circulant nut graph, for any integer
m >= 1.

The proof below is complete subject to the explicitly identified finite
integer computation. The included program generates the finite domain and
checks every case; its input is the integer eight.

## 1. Quotients and the real kernel character

A nut graph is connected: in a disconnected graph, either two components
are singular, giving nullity at least two, or a nonsingular component forces
zero coordinates in every global null vector.

Suppose G is a cubic nut graph and sigma is an automorphism with ell >= 3
cycles, each of length m. Label vertices `(i,t)`, with `1 <= i <= ell` and
`t in Z/mZ`, so sigma increments t. Since sigma commutes with adjacency, it
acts on the one-dimensional real kernel by a real scalar epsilon. Its finite
order implies epsilon is `+1` or `-1`; the latter is possible only for even m.
Thus a full null vector has the form

\[
x_{i,t}=\varepsilon^t w_i,\qquad w_i\ne0.
\tag{1}
\]

Define A_ij to be the number of neighbors in orbit j of a vertex in orbit i.
It is independent of the chosen vertex. Equal orbit sizes and undirectedness
imply that A is symmetric. Its entries are nonnegative integers and each row
sums to three.

For two distinct orbits, neighbors are given by shifts t -> t+a. A shift from
i to j is paired with shift -a from j to i. Three shifts between two orbits
would isolate those two orbits, contrary to connectedness and ell >= 3.
Consequently A_ij <= 2 for i != j.

Within one orbit, nonzero shifts occur in inverse pairs, except for the
possible involution m/2. Connectedness gives A_ii <= 2. If A_ii = 1, this is
the shift m/2, called a semi-edge in the quotient. If A_ii = 2, it is an
inverse pair a,-a, called a loop; there cannot be two distinct involutions
in a cyclic group. These are all possibilities. Discarding diagonal entries
and replacing each positive off-diagonal entry by one therefore gives a
connected simple subcubic support graph H.

On vectors constant on the orbits, adjacency acts by A. Thus ker(A) injects
into ker(Adj(G)), by repeating each coordinate m times. If A is singular,
it must itself have nullity one with a full kernel vector; otherwise the
injection contradicts the nut property of G. If A is nonsingular, (1)
forces epsilon = -1 and m even.

## 2. Symmetric signs and the common semi-edge sign

Suppose A is nonsingular. Restrict adjacency to vectors of the form
`x_(i,t)=(-1)^t w_i`. Its matrix B is real and symmetric: a shift a contributes
`(-1)^a`, and the inverse shift -a contributes the same sign.

If A_ij = 2, the two shift signs cannot cancel. Cancellation would give
B_ij = 0, and the cubic row equation would then consist of one remaining
term `+/-w_k=0`. This contradicts fullness in (1), including when k=i.
The same argument applies wherever a doubled neighbor could cancel.
For a loop, the two inverse shifts already have identical signs. Hence

\[
|B_{ij}|=A_{ij}\quad\hbox{for every }i,j.
\tag{2}
\]

Each semi-edge contributes the *same* sign

\[
 B_{ii}=(-1)^{m/2}\quad\hbox{whenever }A_{ii}=1.
\tag{3}
\]

Loop diagonal entries can be `+2` or `-2`. Every kernel vector of B lifts
injectively by the alternating formula, so B must have nullity one and a
full kernel vector. This implication is necessary only; no assertion that
an arbitrary such B is realized by a voltage assignment is needed.

Take a spanning tree T in H. Conjugation `B -> D B D` by a diagonal matrix
with entries in `{+1,-1}` preserves nullity and the zero pattern of a kernel
vector, and leaves the diagonal unchanged. Starting at a root, choose the
diagonal entries of D recursively to make every tree-edge entry positive.
Every allowed B is therefore represented by:

1. positive entries A_ij on T;
2. an independent choice of sign on each edge outside T;
3. an independent choice of sign on each loop entry of magnitude two;
4. one common choice of sign for all semi-edge entries of magnitude one.

The sign choices can overestimate the voltage realizations for a particular
m. Excluding this larger set excludes every m at once. When no semi-edge is
present, the common semi-edge choice is omitted to avoid duplication.

## 3. Complete generation of the finite quotient domain

The computation uses simultaneous permutation of rows and columns as matrix
isomorphism, and generates the 194 connected simple subcubic supports on
eight vertices without an external graph catalogue.

Start with one vertex. For each connected support on n-1 vertices, add vertex
n with any one, two, or three distinct neighbors whose existing degrees are
at most two. This generates all connected simple subcubic graphs: every
connected graph with at least two vertices has a vertex whose deletion
leaves it connected (take a leaf of a spanning tree), and deleting this vertex
preserves the maximum-degree bound. Relabelling identifies the smaller graph
with a generated representative, and every possible neighbor subset is tried.

Canonicalization first partitions vertices by diagonal entry and row sum.
It repeatedly refines each cell by the vector of row sums into the current
cells. When a cell is not a singleton, every one of its vertices is in turn
individualized; the procedure then continues recursively. The least full
matrix among the leaves is returned. Refinement and the set of branches are
isomorphism invariant. No branch is heuristically discarded, and two outputs
can coincide only if their matrices are permutation conjugate. Thus taking
a set of these outputs removes only isomorphic copies.

For each support H, choose the edges to double. They must form a matching:
a vertex incident to two such edges already has support degree at least two,
and doubling both would give degree at least four. Endpoints of a doubled
edge must have support degree at most two. Conversely, any matching of these
eligible edges is allowed in our quotient superset. Set doubled entries to
two, leave other support entries one, and set

\[
A_{ii}=3-\sum_{j\ne i}A_{ij}.
\tag{4}
\]

This diagonal is zero, one, or two. The interpretation in section 1 accounts
for every possible quotient: a vertex of off-diagonal degree one requires
a loop, and one of off-diagonal degree two requires a semi-edge. Canonicalize
again and discard isomorphic copies. Exactly 534 quotient matrices result.

## 4. The exact finite assertion

For a real symmetric n by n matrix M with det(M)=0, let c_i be its i-th
principal cofactor. If rank(M)=n-1 and v spans the kernel, symmetry and
`M adj(M)=0` imply

\[
\operatorname{adj}(M)=c\,vv^T,\qquad c\ne0.
\]

Therefore M has nullity one with a full kernel vector if and only if every
c_i is nonzero. When rank(M)<=n-2, its adjugate is zero. When rank(M)=n-1,
a zero principal cofactor is exactly a zero coordinate of v.

`verify.py` computes determinants and, when needed, all principal cofactors
using fraction-free Bareiss elimination over Python's arbitrary-precision
integers. Row pivoting is allowed; each division is asserted exact. It does
not use approximate rank tests. The verified finite assertion is:

| Matrices | Nonsingular | Nullity one, nonfull kernel | Nullity >= 2 | Full nullity-one kernel |
|---|---:|---:|---:|---:|
| 534 ordinary quotients A | 425 | 94 | 15 | 0 |
| Signed matrices B over the 425 nonsingular A | 6,104 | 112 | 0 | 0 |

All ordinary singular quotients are excluded by section 1. For each remaining
quotient, every necessary signed matrix is excluded by sections 2 and 4.
This proves the theorem. **QED (computer-assisted).**

## 5. Verification boundaries

The generation and its mathematical completeness proof are part of the
argument. Counts alone are not its certificate: the program checks each
matrix. `crosscheck.py` recomputes every determinant and cofactor by a distinct
subset dynamic program for the Leibniz formula, with no divisions or pivots,
and checks the ranks of all singular matrices by rational row reduction.
For a partial column set S, adding column j to the next row introduces
exactly `|{k in S:k>j}|` inversions; this gives the sign in that recurrence.

The crosscheck uses the same quotient/signing generator. Its catalogue
comparison uses the published 194-entry graph6 list, obtained from the
authors' nauty-based enumeration; equality is checked entrywise up to
isomorphism. The production generator itself needs no external input.
Exhaustive relabellings of the three- and four-vertex supports and controls
at orbit counts 3 through 7 provide additional checks, not replacements for
the completeness argument.

The proof has not been formalized in a proof assistant. It relies on the
mathematical lemmas above, the supplied short programs, and Python's exact
integer/rational operations. There is no imported solver certificate,
floating-point assumption, bounded orbit-length search, or omitted large
artifact.
