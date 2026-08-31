# Family-excess rigidity for a hypothetical 28-word LD code in Q_7

## Theorem

Let `C` be a locating-dominating code of cardinality 28 in the binary
7-cube.  Then all of the following necessary conditions hold.

1. At least 50 vertices have singleton identifying sets.
2. At least 22 codewords are isolated in `Q_7[C]`.
3. The induced graph `Q_7[C]` has at most seven edges.
4. There are at least 44 unordered codeword pairs at Hamming distance two.
5. A complete search may translate an isolated codeword to zero and set all
   seven unit vectors to non-codewords.  Thus the preceding four-case
   minimum-degree normalization collapses to its degree-zero branch.

This is a conditional rigidity theorem, not a nonexistence proof.  It reduces
the unresolved size-28 question to one highly sparse exact branch.

## Family arithmetic

For a vertex `v`, put

\[
E(v)=|I_C(v)|-1.
\]

The Honkala--Laihonen--Ranto family partition has three types of parts:

- points with excess zero;
- codeword couples, each consisting of two excess-one codewords; and
- families, each consisting of an `F_i` father with `i>=3` codewords in its
  identifying set and at most `binom(i,2)` excess-one sons.

Because the published lower bound is 28 in dimension seven, a hypothetical
28-word code is optimal.  Hence no codeword has identifying set of size eight,
and every father has `3<=i<=7`.

Let `p` be the number of excess-zero points, `q` the number of couples, and
write `s_j` for the number of sons of a father covered by `i_j` codewords.
Define

\[
D=\sum_j(i_j-2).
\]

The total excess is

\[
8|C|-2^7=96.
\]

Counting vertices and excess in the partition gives

\[
\begin{aligned}
128&=p+2q+\sum_j(1+s_j),\\
96&=2q+\sum_j(i_j-1+s_j).
\end{aligned}
\]

Subtracting yields the exact identity

\[
p=32+D. \tag{1}
\]

Let `a` be the number of isolated codewords.  Each codeword labels at most one
singleton identifying set of a non-codeword, and exactly the `a` isolated
codewords themselves have singleton identifying sets.  Therefore

\[
p\le 28+a,
\qquad a\ge4+D. \tag{2}
\]

Couples use two non-isolated codewords, so

\[
2q\le28-a\le24-D. \tag{3}
\]

The number `M` of vertices in families consequently satisfies

\[
M=96-D-2q\ge72. \tag{4}
\]

Put `d=i-2`, so `1<=d<=5`.  An `F_i` family contains at most

\[
h(d)=1+\binom{d+2}{2}\le\frac{22}{5}d
\]

vertices.  Thus `M<=22D/5`, and (4) first gives `D>=17`.

The equality frontier is rigid.  A finite integer optimization using

\[
h(1),\ldots,h(5)=(4,7,11,16,22)
\]

shows that total defect 17 supports at most 74 family vertices.  (The
standard-library verifier exhausts every partition with parts in `1,...,5`.)
Equations
(2)--(4) force `q=3` and `M=73`; the only father-defect partitions capable of
reaching 73 are

\[
(d_j)=(5,5,5,2)
\quad\text{or}\quad
(5,5,5,1,1).
\]

Their maximum family sizes are respectively 73 and 74.  Consequently there
are three `F_7` fathers and at least two of their `F_7` families are full.

At most one codeword lies in all the families in either equality case.  An
`F_7` father that is itself a codeword would bring its six codeword neighbors
into the family partition, so every `F_7` father is a non-codeword.  For
such a father `x`, all seven vertices of `N(x)` are codewords, all 21 vertices
at distance two from `x` are its sons when its family is full, and none of the
35 vertices at distance three from `x` is a codeword.  Consequently every
other `F_7` father is at Hamming distance at least five from a full `F_7`
father: distances one and two meet the fixed code/son shells, while at
distances three and four its open neighborhood meets the non-codeword spheres
two and three.

Apply this to the two full `F_7` fathers and the third `F_7` father.  The three
centers would be pairwise at distance at least five.  But there cannot be
three such words in `Q_7`: after
translating one to zero, the other two have supports of size at least five,
so their supports intersect in at least three positions and their mutual
distance is at most four.  This excludes both `D=17` patterns.  Hence

\[
D\ge18,
\qquad p=32+D\ge50,
\qquad a\ge4+D\ge22.
\]

This proves the first, second, and fifth claims.

## Induced-edge consequence

Every induced code edge has two non-isolated endpoints.  Since at most six
codewords are non-isolated, all induced edges lie in a cube subgraph on at
most six vertices.  The standard cube edge-isoperimetric inequality

\[
e(S)\le\frac{|S|\log_2|S|}{2}
\]

gives

\[
e(C)\le
\left\lfloor\frac{6\log_2 6}{2}\right\rfloor=7.
\]

For completeness, the inequality follows by induction after splitting `S`
across a coordinate: cross edges form a matching, and the needed scalar
inequality is the binary-entropy bound `H(t)>=2t` for `0<=t<=1/2`, itself the
concave chord between `(0,0)` and `(1/2,1)`.

## Distance-two consequence

Let `b=28-a<=6` be the number of non-isolated codewords.  The number of
singleton signatures on non-codewords is

\[
o=p-a=p+b-28\ge22+b.
\]

At most `b` of these orphans can belong to non-isolated codewords.  Hence at
least

\[
o-b=p-28=4+D\ge22
\]

isolated codewords have an orphan neighbor.

Fix such an isolated codeword `c`, and label its seven neighbors by the seven
coordinates.  Put an edge `ij` in a graph `H_c` when `c+e_i+e_j` is a
codeword.  The orphan coordinate is the unique isolated vertex of `H_c`.
Every other coordinate has positive degree, since its cube neighbor must have
a signature different from the orphan's `{c}`.  Moreover, `H_c` has no
two-vertex connected component: the endpoints of such a component would both
have signature `{c,c+e_i+e_j}`.  Covering six non-isolated vertices by
components of order at least three takes at least four edges.  Therefore each
of these codewords has at least four codewords at distance two.  Double
counting yields the parameterized bound

\[
A_2(C)\ge2(p-28)=2p-56\ge44
\]

unordered distance-two codeword pairs.

## Exact search encodings

`search_q7_ld28.py` preserves a PySAT encoding and
`search_q7_ld28_mip.py` an independent HiGHS 0-1 formulation.  Both can add
the proved singleton, isolation, edge, and symmetry constraints.  Solver
timeouts are not results and no proof log is archived here.

The strongest preserved SAT branch is generated by

```bash
python search_q7_ld28.py 0 \
  --solver cadical195 \
  --isolated-bound --singleton-bound --edge-bounds --lex-generators \
  --write-cnf /scratch/q7-ld28-branch0.cnf
```

The independent 0-1 model is generated by

```bash
python search_q7_ld28_mip.py 0 \
  --isolated-bound --singleton-bound --distance-two-bound \
  --mps /scratch/q7-ld28-branch0.mps
```

The successful build checks used Python 3.11.2, PySAT 1.9.dev15, and HiGHS
1.15.1.  The requirements files pin the two non-standard-library packages.
The displayed SAT command deterministically produces 11,706 variables and
194,891 clauses with DIMACS SHA-256
`0536684ed109f2bdb86fbb6d792e1791feeb450ab5a911f624d49ef27076a001`.
The displayed MIP command produces 1,728 binary variables and 6,927
constraints.  These are input-build checks, not solver verdicts.

Source SHA-256 hashes are

```text
search_q7_ld28.py           e0bcf44d38bf36abb2c3242d3e07c6f07f4e3ce3e73fea6d2eee2c6422231a31
search_q7_ld28_mip.py       3b45cab789f4000372c617a8f5f04316ace0095e09923aec8e4c7f5d681406a6
verify_family_reduction.py  7c2f101fc89e2c8a876b40aaae1d340049cc43369a26137bdc7f27d2ae9a6129
```

Only distance-two vertex pairs need explicit separation clauses.  If equal
nonempty signatures belonged to two non-codewords, their closed
neighborhoods would intersect, so their distance would be at most two.
Adjacent non-codewords have closed-neighborhood intersection consisting only
of the two non-codewords, hence cannot have equal nonempty signatures.  This
leaves exactly

\[
\frac{2^7\binom72}{2}=1344
\]

essential pair clauses.

The arithmetic verifier uses only the Python standard library:

```bash
python3 verify_family_reduction.py
```

It enumerates all abstract father-defect partitions, checks the two rigid
`D=17` patterns, exhaustively verifies that `A(7,5)=2`, and checks the
cube pair and edge-bound arithmetic.

## Scope and novelty

The theorem does not exclude a 28-word code and says nothing directly about
size 29.  Exact SAT and MIP attempts on the remaining branch have not yet
returned a verdict.

Honkala, Laihonen, and Ranto introduced the family partition and proved the
general lower bound.  Junnila, Laihonen, and Lehtila still recorded the lower
bound 28 for `Q_7` in 2021/2022.  Targeted searches through 2026-08-31 found no
specialization forcing 22 isolated codewords, 50 singleton signatures, or a
single sparse branch.  These refinements are therefore apparently new to the
searched sources, not a historical-priority claim.

- I. Honkala, T. Laihonen, and S. Ranto, "On Locating-Dominating Codes in
  Binary Hamming Spaces," *DMTCS* 6(2), 2004, 265--282.
  https://doi.org/10.46298/dmtcs.322
- V. Junnila, T. Laihonen, and T. Lehtila, "Improved Lower Bound for
  Locating-Dominating Codes in Binary Hamming Spaces," *Designs, Codes and
  Cryptography* 90, 2022, 67--85.
  https://doi.org/10.1007/s10623-021-00963-8
