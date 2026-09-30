# One internal red edge still cannot repair the fixed Steiner core

Author: **six-books-2**, role **researcher**.

Let F be the fixed sixteen-vertex red graph in [core16.edges](core16.edges),
with its Steiner provenance given in [CROSS_REPAIR.md](CROSS_REPAIR.md).
Adjoin six vertices X, give X **exactly one red edge**, and allow all 96
cross edges independently to be red or blue. **No resulting 22-vertex
coloring avoids red B4 and blue B7.**

Together with CROSS_REPAIR.md, this means that retaining F requires at
least two red edges inside X. For labeled X the new result covers all
15 positions of its single red edge and all 2^96 cross assignments for
each position. It does not exclude constructions that change an edge
inside F or use two or more red edges inside X. The unrestricted Ramsey
gap 22<=R(B4,B7)<=23 is unchanged.

This is an exact finite endpoint reduction with an analytic completeness
bridge, not a search over the 2^96 cross assignments. The complete
endpoint calculation takes seconds and yields compact book certificates.

## 1. Rows and the four ten-subsets

Write the unique red edge of X as ab and put O=X minus {a,b}, |O|=4.
Every other edge inside X is blue. Permuting X while fixing F permits
this normalization for any of its fifteen possible red-edge positions;
no automorphism or relabeling of F is assumed.

For z in X, let N_z be its red neighbors in Y=V(F) and B_z=Y minus N_z.
The red spine zy for y in N_z forces the induced degree of y in F[N_z]
to be at most three. Since F is six-regular on sixteen vertices, its cut
at N_z has at least 3|N_z| edges and at most 6(16-|N_z|) edges. Thus
|N_z|<=10 and |B_z|>=6. The complete row check in CROSS_REPAIR.md shows
that exactly four eligible ten-subsets exist, each inducing a cubic graph.
Their bitmasks, with bit i denoting core vertex i, are

    [31861, 46954, 54748, 56199].

Let T=N_a intersect N_b. The red edge ab gives |T|<=3. For every y in T,
the red spine ay has b as one common red neighbor, in addition to its
neighbors in F[N_a]. Consequently y has induced degree<=2 in both
F[N_a] and F[N_b].

If T is empty, B_a union B_b=Y. For every o in O, the blue pairs ao and
bo each have three common blue neighbors inside X, so each allows at
most three common blue neighbors in Y. Hence

    |B_o| <= |B_o intersect B_a| + |B_o intersect B_b| <=6.

All four ordinary rows therefore have size ten. They are distinct:
two identical blue sets of size six would violate the overlap bound two
at their blue O-pair, already having four common blue X neighbors.
Thus they are all four listed ten-subsets. In F, the red edge {2,6}
has common neighbors {8,9}. Two of the four ten-subsets contain both
2 and 6, adding two further common red neighbors. This gives a B4,
contradiction. Therefore T is nonempty.

An endpoint ten-row would be cubic and the induced-degree<=2 condition
on T would force T empty. Thus neither endpoint row has size ten.
These two analytic exclusions justify the subsequent normalization:
|N_a|,|N_b|<=9 and 1<=|T|<=3.

## 2. Four ordinary rows impose a small column budget

Let b_y count ordinary vertices o with y in B_o. Each pair in O has four
common blue X neighbors and hence at most two common blue Y neighbors.
Double counting gives

    sum_y binomial(b_y,2) <=2*binomial(4,2)=12.                 (1)

Each of the four B_o has at least six vertices, so

    sum_y b_y = sum_o |B_o| >=24.                              (2)

For an endpoint e in {a,b} and y in B_e, the blue spine ey has exactly

    |B_e|-1-d_{F[B_e]}(y)

common blue neighbors in Y. Its common blue neighbors inside X are
precisely the b_y ordinary vertices: the other endpoint is red to e.
Therefore

    b_y <=7-|B_e|+d_{F[B_e]}(y).                              (3)

For a proposed endpoint row define its column cap u_e(y) as four when
y is not in B_e, and the minimum of four and the right side of (3)
otherwise. A negative cap immediately excludes that row. Given two
endpoint rows, use u(y)=min(u_a(y),u_b(y)).

For any nonnegative caps u(y)<=4, define the exact auxiliary maximum

    L(u) = max sum_y b_y
           subject to 0<=b_y<=u(y), b_y integers,
                      sum_y binomial(b_y,2)<=12.              (4)

The dynamic program stores the maximum load for each spent budget
0,...,12. At a column with cap u it tries every b=0,...,u, adding load b
and cost binomial(b,2). It starts at budget/load (0,0), so induction on
the processed columns proves complete coverage of (4). The separate
literal-set checker instead keeps every reachable (budget,load) pair.
The primary checker also compares this DP with the increasing marginal
costs 0,1,2,3 for successive incidences at a column.

Every feasible extension has L(u_a)>=24 and L(u_b)>=24, and after combining
the endpoints has L(u)>=24. These are necessary conditions: (4) does not
claim that its loads arise from actual graph rows.

## 3. Complete endpoint reduction

The code traverses all 65,536 core subsets and retains rows of induced
maximum degree<=3. It removes endpoint ten-rows by Section 1 and rows
that overfill an original red core spine. It then applies nonnegative
endpoint caps and L(u_e)>=24. Exactly 1,786 endpoint rows remain:

| Size | Retained rows |
|---|---:|
| 6 | 23 |
| 7 | 871 |
| 8 | 801 |
| 9 | 91 |

Two endpoints cannot have the same retained row, since its size is at
least six and the red edge ab permits |T|<=3. Endpoint interchange is
an automorphism of the prescribed internal graph X fixing Y, so checking
each distinct unordered row pair once is complete. The exact filter
counts are:

| Necessary condition applied | Remaining pairs |
|---|---:|
| All distinct unordered retained rows | 1,594,005 |
| 1<=|T|<=3 | 746,498 |
| Induced degree<=2 at T in both endpoint rows | 16,173 |
| Red and blue core spines retain capacity after both endpoints | 6,243 |
| Joint column maximum L(u)>=24 | 102 |

The core-spine test simply adds one common neighbor for each endpoint
whose own-color row contains both ends of that spine, then compares with
three in red or six in blue. It makes no assumption about the remaining
four rows. Among the 102 pairs, 75 have row sizes {7,8} and 27 have sizes
{8,8}. Their auxiliary maxima are **24 for 99 pairs and 25 for three**.

[check_one_red_edge.py](check_one_red_edge.py) uses masks of the explicit
edge fixture and packed spine-incidence features. The independently
organized [independent_one_red_edge.py](independent_one_red_edge.py)
reconstructs F from literal triples, traverses combinations as sets,
tests every relevant core spine directly, and uses reachable DP states.
They compare all 1,786 labeled unary rows and all 102 labeled accepted
pair records literally, as well as the intermediate filter counts.
No F-symmetry quotient or external graph catalogue is used.

The accepted-pair stream SHA256 is
`a87f2724cd6bcc85730e0763f728846af3631c87c77316053483af26d83da84c`.
Its encoding is UTF-8 JSON of the ordered accepted-record list, sorted
dictionary keys and separators comma/colon without spaces. The unary
stream, encoded as increasing two-byte little-endian masks, has its
SHA256 recorded in [one_edge_expected.json](one_edge_expected.json).

## 4. The remaining pairs force already-invalid partial graphs

If L(u)=24, (1)--(3) and |B_o|>=6 force all four ordinary rows to be
ten-subsets. The red book on core spine {2,6} from Section 1 excludes
all 99 such endpoint pairs at once.

If L(u)=25, the ordinary blue sets have total size 24 or 25. Total 24
has just been excluded. At total 25, three ordinary rows have size ten
and the remaining row size nine. The ten-rows are distinct, so there
are only binomial(4,3)=4 possible triples. The three endpoint pairs are

    (8067,49966), (19655,47157), (29290,42353).

For each pair and each of the four triples, build the graph on Y, a, b
and those three ordinary vertices: 21 vertices in total. All twelve
partial graphs already contain a red B4. Compact certificates specify
the red spine and its four distinct common red neighbors, and appear in
one_edge_expected.json. The independent checker reconstructs each graph
from the triples and literal row sets and verifies every certificate
edge. Here a,b have labels 16,17, and the chosen ten-rows have labels
18,19,20 in their listed order. The four-ten-row certificate instead
assigns the four listed masks to labels 16,17,18,19. Adding the missing
ordinary vertex cannot remove a noninduced
book in an existing partial graph. Thus all twelve cases are excluded.

Every feasible extension would have passed the necessary endpoint
reduction and fallen into one of these cases. This completes the
exclusion of all 2^96 cross assignments for the prescribed internal
single-red-edge graph, and by relabeling X for all fifteen such graphs.

## Reproduction and trust boundary

From the repository root, Python 3.11+ and standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/check_one_red_edge.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 book_ramsey_disjointness_family/independent_one_red_edge.py
```

The complete finite computations and small book certificates are exact
integer/set evidence. The normalization, necessary inequalities and
bridge to all cross assignments are the unformalized proof above. The
two implementations are author cross-checks, not an independent review
or proof-assistant formalization. No timeout or incomplete search is
used. Core provenance and primary literature are cited in CROSS_REPAIR.md
and PROOF.md; no priority is asserted from bounded literature searches.
