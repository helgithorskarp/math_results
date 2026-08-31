# Complete abelian degree-six obstruction for exact 7-step domination

## Result

Let \(\Gamma=\operatorname{Cay}(A,X)\) be a connected Cayley graph of a
finite abelian group, where \(X=-X\), \(0\notin X\), and \(|X|\le 6\).
Then \(\Gamma\) has no exact \(7\)-step dominating set of cardinality \(4\)
or \(6\).

The degree-at-most-five cases and all degree-six cases containing an
involution were proved in the preceding contributions. The cyclic pure
three-pair case was also proved separately. The new exhaustive case here is

\[
X=\{\pm g_1,\pm g_2,\pm g_3\}
\]

in an arbitrary **noncyclic** finite abelian group. Thus the combined theorem
closes every abelian Cayley graph of degree at most six. It does not settle
nonabelian Cayley graphs, non-Cayley graphs, or the value of \(m(7)\).

## Finite quotient reduction

Put

\[
\Sigma_7=\{a\in A:d_\Gamma(0,a)=7\}.
\]

If \(S\) is an exact \(7\)-step dominating set with \(k\in\{4,6\}\)
centers, then the translates \(s+\Sigma_7\), \(s\in S\), partition \(A\).
Consequently

\[
|A|=k|\Sigma_7|.
\]

The map

\[
\pi:\mathbb Z^3\longrightarrow A,
\qquad e_i\longmapsto g_i
\]

is onto. Its kernel \(L\) is an index-\(|A|\) sublattice, and graph distance
from zero is the minimum Lee norm of a preimage. The three-dimensional Lee
shell of radius seven has

\[
4\cdot 7^2+2=198
\]

vectors. Hence \(|\Sigma_7|\le198\), \(|A|\le1188\), and \(|A|\) is
divisible by four or six.

Conversely, every finite-index sublattice \(L\le\mathbb Z^3\) gives the
marked quotient \(\mathbb Z^3/L\). Requiring the six images
\(\{\pm e_1,\pm e_2,\pm e_3\}\) to be nonzero and distinct is exactly the
simple degree-six condition. Thus finite-index sublattices give a complete
parametrization of the remaining Cayley graphs.

## Hermite-normal-form universe

Every such lattice has a unique column Hermite normal form

\[
H=
\begin{pmatrix}
a&x&y\\
0&b&z\\
0&0&c
\end{pmatrix},
\qquad
a,b,c>0,
\quad 0\le x,y<a,
\quad 0\le z<b.
\]

Its index is \(abc\). Therefore the number of index-\(N\) HNFs is

\[
\sum_{abc=N}a^2b.
\]

If \(d_1\mid d_2\mid d_3\) are the Smith factors of \(H\), the gcd of its
\(2\times2\) minors is \(d_1d_2\). The quotient is cyclic exactly when this
gcd equals one. Independently, the number of index-\(N\) lattices with cyclic
quotient is

\[
\frac{J_3(N)}{\varphi(N)},
\]

because their kernels are epimorphisms
\(\mathbb Z^3\twoheadrightarrow\mathbb Z/N\mathbb Z\), modulo the free
postcomposition action of the unit group. Summed over the eligible orders,
these formulas give

```text
eligible_hnfs=563799191
cyclic_quotient_hnfs=443174739
noncyclic_quotient_hnfs=120624452
```

The enumerator obtains the same first and third counts by direct HNF scanning.

## Lossless signed-permutation filter

Permuting the three generators or changing any signs preserves the connection
set. To avoid evaluating most marked copies of the same graph, the enumerator
attaches to an oriented generator triple the ordered list of element orders
for these thirteen coefficient forms:

\[
e_i,\qquad e_i\pm e_j\ (i<j),\qquad
e_1\pm e_2\pm e_3\quad\text{modulo global negation}.
\]

It retains an HNF when its identity-orientation signature is lexicographically
minimal among all signed coordinate permutations. This is lossless: in every
signed-permutation orbit, transform a lattice by an orientation attaining the
minimum and then take its unique HNF. That HNF occurs in the scan and passes
the filter. Global negation fixes every lattice, so the signed-permutation
action has at most 24 effective images. Signature ties are deliberately all
retained; the reported signature count is not claimed to be an orbit count.

After rejecting cyclic quotients and nonsimple connection sets, the complete
enumeration gives

```text
eligible_hnfs=563799191
noncyclic_hnfs=120624452
degree_six_hnfs=118667394
signature_representatives=15797397
four_center_counting_candidates=3062
six_center_counting_candidates=73645
four_center_tilings=0
six_center_tilings=0
```

For every retained HNF, the enumerator maps all 377 coefficient vectors of
Lee norm at most six and all 198 vectors of norm seven into the quotient.
The sphere is exactly the set of shell images not represented by a shorter
vector.

Only the 76,707 HNFs satisfying \(|A|=k|\Sigma_7|\) enter the tiling test.
Writing \(D=\Sigma_7-\Sigma_7\), sphere translates with shifts \(u,v\) are
disjoint exactly when \(u-v\notin D\). After fixing one shift at zero, the
enumerator performs a complete compatibility-clique search. The counting
identity turns pairwise disjointness into coverage.

## Independent checker

The checker uses different decisive algorithms.

1. It derives the full HNF and cyclic-kernel totals from the two formulas
   above, independently of the enumerator's scan.
2. It validates every descriptor, its noncyclic quotient, its HNF bounds, and
   its six distinct nonzero steps, and rejects duplicate HNFs.
3. It reconstructs every radius-seven sphere by full graph BFS rather than
   coefficient images.
4. It replaces the difference-clique test by direct first-uncovered translate
   exact cover.

It reports

```text
eligible_hnfs=563799191
cyclic_quotient_hnfs=443174739
noncyclic_quotient_hnfs=120624452
candidate_hnfs=76707
four_center_candidates_checked=3062
six_center_candidates_checked=73645
four_center_tilings=0
six_center_tilings=0
```

## Reproduction

The complete runs used GCC 12.2.0 on Debian 12. Candidate files and command
output belong under `/scratch`, not in the repository.

```bash
g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  enumerate_noncyclic_degree6.cpp \
  -o /scratch/enumerate_noncyclic_degree6

g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  check_noncyclic_degree6_candidates.cpp \
  -o /scratch/check_noncyclic_degree6_candidates

/scratch/enumerate_noncyclic_degree6 1 624 \
  /scratch/noncyclic-degree6-1-624.txt &
/scratch/enumerate_noncyclic_degree6 625 784 \
  /scratch/noncyclic-degree6-625-784.txt &
/scratch/enumerate_noncyclic_degree6 785 900 \
  /scratch/noncyclic-degree6-785-900.txt &
/scratch/enumerate_noncyclic_degree6 901 988 \
  /scratch/noncyclic-degree6-901-988.txt &
/scratch/enumerate_noncyclic_degree6 989 1064 \
  /scratch/noncyclic-degree6-989-1064.txt &
/scratch/enumerate_noncyclic_degree6 1065 1132 \
  /scratch/noncyclic-degree6-1065-1132.txt &
/scratch/enumerate_noncyclic_degree6 1133 1188 \
  /scratch/noncyclic-degree6-1133-1188.txt &
wait

/scratch/check_noncyclic_degree6_candidates \
  /scratch/noncyclic-degree6-1-624.txt \
  /scratch/noncyclic-degree6-625-784.txt \
  /scratch/noncyclic-degree6-785-900.txt \
  /scratch/noncyclic-degree6-901-988.txt \
  /scratch/noncyclic-degree6-989-1064.txt \
  /scratch/noncyclic-degree6-1065-1132.txt \
  /scratch/noncyclic-degree6-1133-1188.txt
```

The seven files contain 76,707 lines. Their ascending-range concatenation has
SHA-256

```text
172ac46cc9113a90461a788f72aded876c105bf8d19c2922068cc94793e30d50
```

Source SHA-256 values after the final clean build are

```text
enumerate_noncyclic_degree6.cpp          d29ab217da704d02dbd5f4006468f7bb714da806dbcdef23e21d72cb7c9ae36b
check_noncyclic_degree6_candidates.cpp   c9982a6c7cd8e88459f96a3d746fc19ac5668e062044242cd84d8fc0bb921229
```

## Dependencies, status, and trust boundary

This theorem depends on the separately verified degree-at-most-five,
involutory degree-six, and cyclic degree-six obstructions in adjacent source
directories. It strictly generalizes the immediately preceding rectangular
three-torus obstruction. That special case has a shorter polynomial/profile
proof for its three surviving counting candidates; the present HNF theorem
does not supersede the explanatory value of that proof.

This is an exact computer-assisted theorem. Its trust boundary consists of
the translate-partition and Lee-shell reductions, HNF completeness, the
Smith-minor cyclic test, the losslessness of the order-signature filter,
selection of counting candidates by the transparent enumerator, the two
finite implementations, and the compiler/runtime. The checker independently
counts the full HNF universe and validates every emitted candidate, but it
does not independently rescan all 118,667,394 simple noncyclic HNFs. All
decisive operations use exact integers; no heuristic result, SAT solver,
proof log, or external certificate decoder enters the theorem.

Targeted searches through 2026-08-31 found the foundational exact-step papers
and work using other exact-distance conventions, but no prior obstruction for
all abelian Cayley graphs of degree at most six. The combined theorem is
therefore apparently new to the searched sources, not a priority claim.

- P. Hersh, *On exact n-step domination*, Discrete Mathematics 205 (1999),
  235--239, <https://doi.org/10.1016/S0012-365X(99)00024-2>.
- L. K. Williams, *On Exact n-Step Domination*, Ars Combinatoria 58 (2001),
  13--22,
  <https://combinatorialpress.com/article/ars/Volume%20058/volume-58-paper-2.pdf>.
- S. Das, S. Das, and A. Sadhukhan, *Exact-Distance Domination in Grid
  Graphs*, arXiv:2607.29648 (2026), <https://arxiv.org/abs/2607.29648>.
