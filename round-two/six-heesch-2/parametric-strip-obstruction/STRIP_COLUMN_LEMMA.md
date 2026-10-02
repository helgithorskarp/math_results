# six-heesch-2 — researcher — six-column strip lemma

Ordinary proof, author checked, unformalized, independently unreviewed.
No historical priority is claimed. This lemma gives contact predicates; it does
not prove any uniform finite Heesch upper bound or a five-corona construction.

Use axial coordinates for unit regular hexagonal cells, with neighbor steps
`(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)`. For every integer k >= 1 let

\[
T_k=\{(0,0),(-2k,k-1),(-2k-1,k)\}\cup
\bigcup_{r=0}^{k-1}\{(-2r-1,r+1),(-2r-1,r+2),
                         (-2r-2,r+1),(-2r-2,r+2)\}.
\]

The unimodular coordinate change u=x+2y, v=y writes T_k as six columns:

| u | integer v interval |
|---|---|
| -2 | k-1 only |
| -1 | k only |
| 0 | 0 through k |
| 1 | 1 through k |
| 2 | 2 through k+1 |
| 3 | 2 through k+1 |

This follows by substituting the four cells of each r. The odd x column gives
u=1,3 and the even x column gives u=0,2; adjoining the initial cell extends
the u=0 interval to v=0. The two terminal cells give u=-2,-1. Hence
|T_k|=4k+3. Its closed cell halo W_k (T_k and its six neighbor translates)
lies in -4 <= u <= 5, because neighbor steps change u by +/-1 or +/-2.

Every lattice-preserving hexagonal isometry has a D6 linear part. In (u,v)
coordinates write its affine action as

\[
u'=\alpha u+\beta v+a,\qquad v'=\gamma u+\delta v+b.
\]

Direct conjugation of the twelve D6 matrices gives four with beta=0 and
eight with beta=+/-3. The four beta=0 matrices are
`[[1,0],[0,1]]`, `[[-1,0],[0,-1]]`, `[[1,0],[1,-1]]`,
and `[[-1,0],[-1,1]]`. They preserve the strip's spine direction. Thus
every nonparallel copy has beta=+/-3.

For such a copy, each of the four interval columns maps to an arithmetic
progression in u' with step magnitude three. At most two points of that
progression lie in the six integer columns -2 through 3; at most four lie
in the ten columns -4 through 5. The two singleton columns contribute at
most one each. Consequently, for every registered translation a,b and every
k >= 1,

\[
|g(T_k)\cap T_k|\le 10,\qquad |g(T_k)\cap W_k|\le18
\]

whenever the spine directions are nonparallel. Disjointness is not needed
for either bound. The second also bounds intersection with the open halo.

These facts give exact predicates without expanding the 4k+3 cells. For a
nonparallel image, solve the integer interval inequalities for u' within the
target u range. Each source column has at most two candidates for T_k, or
four for W_k. Test their v' against the target column intervals. For a
parallel image, u' is constant along a source column and delta=+/-1; its
v' values form one interval. Intersect this interval with the target
intervals. W_k is represented by shifting the six columns by the seven
steps (zero and the six neighbors) and merging intervals in each column.
There are at most 42 input intervals and ten output columns, independent of
k. Subtract the root intersection count from the closed-halo intersection
count to obtain the open-halo count. A copy is an admissible lattice contact
exactly when the root count is zero and the open-halo count is positive.

The number of integer arithmetic operations and stored intervals in these
predicates is bounded independently of k and of the translation. Integer
bit sizes and thus bit complexity still depend on the input parameters.
The companion `strip_columns.py` implements the predicates and compares
them with materialized cell sets on a bounded sample. Those comparisons
validate the implementation; the argument above supplies the all-k proof.

This is a possible starting point for a parametric contact-domain or
obstruction argument. Finite results for T4, T5, or T6 do not establish a
uniform upper bound, and no such inference is made. The all-motion bridge
from admissible coronas to registered lattice contacts is a separate
dependency (published graph8585 / sourcecf3b672f2bf53a076c057b44a6f1a087ef028fcd).
The predicates themselves concern registered copies only and need no
all-motion registration theorem.
