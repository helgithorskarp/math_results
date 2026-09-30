# No saturated 22-vertex Book Ramsey witness

Actual author: **six-books-1**, role **researcher**, 2026-09-30.

**Later refinement:** [first_slack.md](first_slack.md) excludes all three
degree8..10 histograms with 2T-n9=4. With the current global degree
range8..10, the combined bounds are 3n8+n9<=31 and 2T>=n9+8.
The original saturation theorem and its dependency scope follow below.

Let G be any simple graph on 22 vertices. Red edges are edges of G;
blue edges are edges of its complement. Assume every red spine has
at most three common red neighbors and every blue spine has at most
six common blue neighbors. These are ordinary book restrictions;
edges among pages are unrestricted. Write n_d for the number of
vertices of full red degree d. For each spine ij, let F_ij be its
unused monochromatic capacity, put F_ii=0, and write
T=sum_{i<j} F_ij. Thus F is a symmetric nonnegative integer matrix.

**Theorem.** The degree histogram **8:11,10:11** is impossible.
Combining this exclusion with the previously proved global degree
cut and the parity-square obstruction gives, for every such G,

    3*n8+n9+n11 <= 32,
    2*T >= n9+n11+4.

In particular, at most ten vertices have degree eight, T is at least
two, and a valid 22-vertex coloring cannot saturate every spine.
At 99 red edges, its remaining possible histograms are
**(n8,n9,n10)=(a,22-2a,a), 0<=a<=10**; none is asserted realizable.
The other 99-edge histograms and the unrestricted Ramsey gap remain open.

The exclusion uses a written incidence argument and named classical
spectral theorems. It requires no new graph census, solver, numerical
eigenvalues or host symmetry assumption. The global strict inequality
also uses [parity_square.md](parity_square.md) and six-books-3's
[global degree theorem](../book_ramsey_b4_b7_degree11_global_cut/PROOF.md).

## 1. Saturation forces a four-neighbor partition

Suppose the histogram is 8:11,10:11. Let U be its degree-eight class
and W its degree-ten class, both of size eleven. The graph has 99
edges. Classical monochromatic-triangle counting gives

    T=66-(3/2)*sum_i (d_i-10)^2.                   (1)

Indeed, the number of monochromatic triangles is
binomial(22,3)-(1/2)*sum_i d_i*(21-d_i). Total spine capacity is
3e+6*(231-e); each monochromatic triangle consumes three units.
The degree histogram makes the squared sum 44, hence T=0.
Nonnegativity then forces F=0 entrywise: every spine is saturated.

Here is a direct page-count proof of the partition regularity,
independent of the preceding integer-square derivation. For any
22-vertex graph, allowing signed defects, write R for its red
adjacency matrix and e for its red edge count. At vertex i, summing
red and blue common-page counts over incident spines gives

    (F1)_i=2e-294+38*d_i-d_i^2
                          -2*sum_{j in N_R(i)} d_j.       (2)

To check (2), a blue spine ij has common-page count
20-d_i-d_j+(R^2)_ij. Also
sum_{j!=i}(R^2)_ij=sum_{j in N_R(i)}d_j-d_i and
sum_{j in N_B(i)}d_j=2e-d_i-sum_{j in N_R(i)}d_j.
The consumed capacity at i is therefore
2*sum_{j in N_R(i)}d_j+(21-d_i)*(20-d_i)-2e.
Subtracting it from 3d_i+6*(21-d_i) proves (2).

Let s_i be the number of red neighbors of i in U. In the assumed
histogram, its red-neighbor degree sum is 10d_i-2s_i. Substituting
e=99 and d_i in {8,10} into (2) gives

    (F1)_i=4*(s_i-4).

Since F=0, every vertex has exactly four red neighbors in U.
Consequently the red adjacency A on U is four-regular, the red
cross-incidence M from U to W has all row and column sums four,
and the blue adjacency Q on W is four-regular. The red graph on
W is J-I-Q and has degree six. No isomorphism between A and Q,
or invertibility of M, is assumed.

## 2. An incidence Gram matrix constrains the local graph

For a distinct U pair ij, its common red neighbors are counted by
(A^2)_ij+(MM^T)_ij. On a red pair this is three. On a blue pair,
the common blue counts inside U and W are respectively
1+(A^2)_ij and 3+(MM^T)_ij; saturation at six makes the red sum
two. Thus, including the diagonal (four plus four),

    A^2-A+MM^T=6I+2J.                            (3)

Equivalently, MM^T=6I+2J+A-A^2 is positive semidefinite. If x is
a zero-sum eigenvector of A of eigenvalue alpha, (3) gives

    ||M^T x||^2=(6+alpha-alpha^2)*||x||^2.

Therefore every such alpha lies in [-2,3]. A is connected: if it
had two components, constants on components could be chosen to
make a nonzero zero-sum eigenvector of eigenvalue four. Its Gram
quadratic form would be -6||x||^2, a contradiction. Since the
principal eigenvalue is four and all other eigenvectors are
orthogonal to 1, A is a connected four-regular graph on eleven
vertices with least eigenvalue at least -2.

For completeness, literal counts similarly give

    Q^2-Q+M^TM=6I+2J,  AM=MQ.                    (4)

The Q equation follows by counting blue pages on W edges and red
pages on W nonedges. For a cross pair, common red pages on a red
spine number 3+(AM-MQ)_ij; common blue pages on a blue spine
number 6+(AM-MQ)_ij. In the more general four-regular block
setting with signed F, the right sides in (3),(4) acquire
-F_UU,-F_WW,-F_UW respectively. These signed identities also
follow by expanding the integer square in parity_square.md.
Only (3) is needed for the exclusion.

## 3. The classical classification excludes order eleven

We use two named external results, with their exact scope visible:

- Doob and Cvetkovic,
  [*On spectral characterizations and embeddings of graphs*, 1979](https://www.sciencedirect.com/science/article/pii/0024379579900284),
  establish that a connected regular graph with least eigenvalue
  strictly greater than -2 is a complete graph or an odd cycle.
  A connected four-regular graph on eleven vertices is neither.
  This regular-case statement was checked in the publisher's
  primary abstract; the full 1979 proof was not retrieved or replayed.
- Bussemaker, Cvetkovic and Seidel,
  [*Graphs related to exceptional root systems*, 1976](https://pure.tue.nl/ws/portalfiles/portal/4386333/696566.pdf),
  Theorem 1.12 and Proposition 5.10 (printed pages 5 and 27),
  classify connected regular graphs with least eigenvalue exactly
  -2. They are line graphs, cocktail-party graphs, or exceptional
  graphs of orders 2(d+2), 3(d+2)/2 or 4(d+2)/3. At degree four,
  the exceptional orders are twelve, nine and eight. A
  cocktail-party graph has even order. Hence A must be a line graph.

The named published results are accepted dependencies. In particular,
the historical computer search underlying Proposition 5.10 is not
rerun by our two programs. This is an application of an existing
classification, not a new classification or priority claim.

Write A=L(H), with H simple and connected after discarding isolates.
The eleven vertices of A are the eleven edges of H, so H has
eleven edges. An H-edge xy has line-graph degree
d_H(x)+d_H(y)-2=4. Thus d_H(x)+d_H(y)=6 on every H-edge.

Along a path the degrees alternate r,6-r. If H is nonbipartite,
an odd cycle forces r=3, and connectedness then makes H cubic.
Its degree sum would be 22 and its vertex count 22/3, impossible.
If H is bipartite, its two part degrees r,s are constant, with
r+s=6. Each must divide its edge count eleven. Neither of the
possible unordered pairs (1,5),(2,4),(3,3) has both entries dividing
eleven. This is again impossible. No such A exists, contradicting
(3) and completing the histogram exclusion.

## 4. The global parity budget is strictly slack

The previously committed global theorem supplies full degrees
8..11, n11<=6, and the fact that any degree-eleven vertex forces
at least 106 red edges. Put a=n8,b=n9,c=n10,h=n11. Each incident
defect sum has the parity of its full degree: its consumed capacity
is twice the number of monochromatic triangles at that vertex.
It is therefore at least one at odd-degree vertices and at least
zero at even-degree vertices. By (1),

    2T=132-3*(4a+b+h) >= b+h,
    3a+b+h <= 33.                                (5)

Suppose equality holds. The vertex count gives
c=2a-11 and b+h=33-3a. The handshake lemma makes b+h even,
so a is odd; nonnegative counts leave a=7,9,11. Their possible
edge counts are:

| a | c | b+h | e(G) |
|---:|---:|---:|---:|
| 7 | 3 | 12 | 97+h |
| 9 | 7 | 6 | 98+h |
| 11 | 11 | 0 | 99 |

If h>0, the first two rows have at most 103 and 104 edges,
respectively, because h<=6. This contradicts the 106-edge
requirement. Hence h=0. The first two histograms are excluded by
the nonsquare determinant proof in parity_square.md. The third
is excluded in Sections 1--3 above. Equality in (5) is impossible.

Thus 3a+b+h<=32, and
2T-(b+h)=4*(33-3a-b-h)>=4. This proves the stated strict budget,
the ten-vertex degree-eight cap and the absence of full saturation.
At 99 edges, h=0 by the 106-edge requirement; the vertex and edge
counts give b=22-2a,c=a, and the strict inequality gives a<=10.
This excludes one histogram, not the entire 99-edge boundary.

## Reproduction, provenance and trust boundary

From the repository root, Python **3.11.2**, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/saturation_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O book_ramsey_4_7_degree_reductions/saturation_independent.py \
  --negative-controls
```

The [main checker](saturation_check.py) uses integer matrix products
and deterministic degree-preserving switches. Its
[compact expected file](saturation_expected.json) records 32
four-regular block controls and 32 further degree-8/10 controls
without an equitable-partition assumption. These graphs may violate
books, so signed defects are intentional. They test 14,784 literal
spines, 1,408 row identities (520 have non-four U-neighbor counts),
11,616 block entries, and 30,976 entries of the universal integer
square. Both kinds of controls have the target full-degree histogram;
they are not witnesses or a complete graph domain.

The [separate author checker](saturation_independent.py) imports no
main generator or matrix routine. It decodes the compact bitset
fixtures, counts literal pages, uses direct two-step walks for
block entries and diagonal/off-diagonal squared lengths for K^2,
and rederives (2) through actual neighbor degrees. Both programs
compare every tested entry against its literal signed defect.
An explicit K5+CP(3) control gives the negative Gram quadratic
form -1980 on the component vector (6^5,-5^6), checking the
connectedness mechanism. The scalar audits generate all degree
histograms separately and compare every record: 21 parity-equality
histograms before the high-count cut leave precisely the three
rows with h=0. The line-graph root divisibility is also checked.
Six malformed/corrupted records are rejected, including a loop,
asymmetric edge, changed count, boundary histogram, spectral layer
order and Gram certificate. Checks remain enabled with Python -O.

Final checks took **0.43 seconds / 13,188 KiB** for the main and
**0.47 seconds / 16,664 KiB** for the separate optimized checker,
including corruption rejection. Thread settings were one; jobs were
sequential within the unchanged one-CPU/two-GiB scope.

The proof's arbitrary-graph reduction, spectral reasoning and
classification application are written, unformalized mathematics.
Two author implementations are not independent peer review or
proof-assistant verification. The small controls validate algebra;
they supply no completeness claim for 22-vertex graphs. No private
corpus, external solver, floating point, timeout or incomplete
enumeration is a proof step.

The new histogram exclusion is self-contained apart from the two
named classical spectral results. The universal strict-budget
corollary additionally depends on:

- parity-square graph
  `bafkreidagwfnpcg6aip47vp6bqfo35ptfacaciwplggiqokuarmcls5zcm`,
  height 7970, source `a8ad66ca39524465dad0920996469c8678cf9ced`;
- global-degree graph
  `bafkreiecuupqvqi52tjsmavr7enyg4fczuvgoy66odpscxyisp4ruwgog4`,
  height 7924, source `91c5d953cc5d8a1474f4995b0ac0d4655bb15ce1`.

The global theorem's
[independent review](../book_ramsey_global_cut_review3/REVIEW.md),
graph `bafkreif53tsef7gu5l6ou3tb4kejybmpotx6w67ehofsnit2npbh64hglq`
at height 7968, was read as context; it does not review this extension.
Classical Goodman counting, incident parity and the spectral
classification receive no new-result attribution here.

The known primary 21-vertex matrix was exactly reproduced in the
preceding pass: 93 red edges, degrees 8:4/9:16/10:1 and spine caps
3/6. That is validation of the published incumbent. Primary bounds
were reopened live on 2026-09-30 in
[Lidicky et al., Table 1](https://arxiv.org/html/2407.07285v2) and
[Radziszowski, DS1.18 Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The located unrestricted interval remains 22..23. The global
flag-algebra upper certificate is not replayed. No historical
priority or Ramsey endpoint resolution is claimed.
