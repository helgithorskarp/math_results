# Exact global branch and the certificate boundary

This task asks whether a graph on 43 vertices with binary adjacency rank at
most eight can have neither a clique nor an independent set of size five.
The family includes all graph labelings and imposes no automorphism on the
graph. Neither a saved graph nor a chosen physical neighborhood is fixed.
No coordinate orbit or other symmetry quotient is used in the computation.

## Alternating-form coverage

Over GF(2), a symmetric matrix A with zero diagonal is alternating. If a
nonzero residual matrix R has R[p,q]=1, let u=R[:,p] and v=R[:,q]. Then

    R' = R + u v^T + v u^T

has zero p and q rows and columns, and rank(R')=rank(R)-2. Indeed, the
span of e_p,e_q is a nondegenerate alternating plane. Replacing each
other basis vector e_i by e_i+R[i,q]e_p+R[i,p]e_q makes it orthogonal to
that plane. This invertible change of basis splits off the plane and
leaves R' on its complement. Iterating gives

    A = sum_j (u_j v_j^T + v_j u_j^T),   rank(A)=2r.

For r<=4 assign vertex i the coordinate (x_i,y_i) in GF(2)^4 x GF(2)^4,
where the j-th bits are (u_j)_i and (v_j)_i, padded by zero if necessary.
Then A[i,k]=B(c_i,c_k), where

    B((x,y),(z,w)) = x.w + y.z mod 2.

Conversely any graph defined by these coordinates has rank at most eight.
This standard factorization is the same general algebraic mechanism used
by the earlier rank-six obstruction; no new rank inequality is claimed.
The executable `factor_check.py` checks rank drops by a separate Gaussian
elimination and checks every entry of the reconstructed adjacency matrix.

For the **good43 hypothesis**, zero and repeated coordinates cannot occur.
The classical R(4,5)<=25 gives 18<=d(v)<=24 in both colors. A same-color
edge has at most 13 common neighbors of that color, by R(3,5)<=14.
A zero coordinate would be a red-isolated vertex. Two repeated coordinates
give nonadjacent vertices with identical red neighborhoods; they have
41-d(v)>=17 common blue neighbors, exceeding 13. This proves injectivity
and exclusion of zero specifically for a possible target. The algebraic
factorization itself permits zero and repeated coordinates.

The small Ramsey inputs are imported classical theorems. The primary
[McKay--Radziszowski paper](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf)
proves R(4,5)=25 and records R(3,5)=14. Its old catalogue and gluing
computations are not replayed or used as search inputs here.

Thus the global physical branch is equivalent to the following finite
selection problem: choose at least 43 distinct labels from 1..255,
identifying a label with its eight binary coordinates, and require no
five chosen labels to be pairwise B=0 or pairwise B=1. Any feasible larger
selection yields a good43 by retaining its first 43 labels. Every target
in the declared rank branch appears under some injective coordinate map.
The map is not an isomorphism quotient or an injective enumeration of
physical graphs; completeness for existence is the claim needed here.

## Complete forbidden-set counts

For B=0, count ordered tuples of distinct nonzero pairwise orthogonal
vectors by their span dimension d. With k vectors already chosen, the
span is isotropic. Exactly 2^d-1-k unused nonzero vectors are inside it,
and exactly 2^(8-d)-2^d vectors in its orthogonal complement lie outside
the span. The latter increase d by one. Start with one empty tuple and
iterate five times, then divide by 5!. This gives 6,409,935 blue five-sets.

For B=1 choose the first vector in 255 ways and the second in 128 ways.
There are 64 choices for the third. One is the sum of the first two;
that dependent triangle has no common B=1 neighbor and cannot extend to
a four-set. The other 63 are linearly independent. Their three affine
pairing equations give 32 choices for the fourth, all outside their span:
the odd-order Gram matrix has zero row sum, so its equations with right
side all ones have no solution inside that span. The four-set Gram
matrix has zero diagonal and ones elsewhere, is invertible over GF(2),
and has 16 common B=1 neighbors. Therefore the number of red five-sets is

    255 * 128 * 63 * 32 * 16 / 120 = 8,773,632.

The producer uses a recursive common-neighbor enumeration, separately
checked by counting four-set faces and all their extensions. The reverse
audit uses the displayed algebraic counts, checks all ten pairings of
every emitted five-set with a different coordinate implementation, and
requires strict lexicographic order within each color. Validity,
distinctness, and equality with the algebraic cardinality prove complete
coverage of the forbidden sets.

## Cardinality and whole-formula meaning

Variables y_1,...,y_255 select the coordinates. Each forbidden five-set
contributes its five negated selection literals. Prefix variable s[i,j]
means that at least j of the first i labels are selected, for j<=43.
The boundary values are s[i,0]=true and s[i,j]=false for j>i. Encode

    s[i,j] <=> s[i-1,j] OR (y_i AND s[i-1,j-1])

by all four clauses of this Boolean equivalence, substituting constants,
and require s[255,43]. Induction on i proves exact cardinality semantics,
including uniqueness of the auxiliary values for any selection.
`counter.py` exhausts all 16 local Boolean states and all 3,586 input
assignments/threshold choices of lengths one through eight.

There are 10,317 variables and 39,951 counter clauses, for 15,223,518
clauses in the complete formula. The formula SHA256 and size are recorded
in PREPARATION.json. A satisfying model must be decoded and its resulting
physical 43-vertex graph checked on all 962,598 five-subsets. A solver
UNSAT statement becomes a branch exclusion only after independent DRAT
verification. A timeout, resource failure, or unchecked proof leaves the
entire branch unresolved. No input formula, clause count, or encoding
audit alone establishes the required physical verdict.
