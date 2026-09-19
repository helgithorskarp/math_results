# Identity inflation of three-term Schubert polynomials

## Result

For a permutation \(w\), put

\[
\Upsilon_w=\mathfrak S_w(1,1,\ldots,1),
\]

and let \(w\otimes1_k\) be the permutation obtained by replacing each
entry \(w_i\) by the increasing block
\(k(w_i-1)+1,\ldots,kw_i\).

**Theorem.**  If \(\Upsilon_w=3\), then for every \(k\geq1\),

\[
\boxed{\quad
\Upsilon_{w\otimes1_k}
=\operatorname{PP}(k,k,2k)
=\prod_{i=1}^k\prod_{j=1}^k
  \frac{2k+i+j-1}{i+j-1}.
\quad} \tag{1}
\]

Here \(\operatorname{PP}(a,b,c)\) is the number of plane partitions in
an \(a\times b\times c\) box.  Consequently, for \(k\geq2\),

\[
\Upsilon_{w\otimes1_k}>3^{k^2}=\Upsilon_w^{k^2}. \tag{2}
\]

Thus the Morales--Pak--Panova identity-inflation conjecture, and its
natural all-\(k\) extension, hold strictly on the complete
\(\Upsilon_w=3\) stratum.  The first values in (1) are

\[
3,\ 105,\ 41580,\ 184225041,\ 9095857138368,\ldots
\qquad(k=1,2,3,4,5,\ldots).
\]

This is the next specialization stratum after the two-term theorem in
the neighboring directory `schubert_two_term_kronecker`.

## The two-move classification

Write \(c(w)\) for the Lehmer code, and call a permutation dominant if
it is 132-avoiding.  The following small classification is the
structural input.

**Two-move lemma.**  If \(\Upsilon_w=3\), there are a dominant
permutation \(u\), an index \(r\), and one of the following three
reduced ascent words taking \(w\) to \(u\).  Only the displayed code
coordinates matter; \(a\geq0\).

\[
\begin{array}{c|c|c}
\text{word from }w\text{ to }u&\text{local code of }u&
  \text{local factor of }\mathfrak S_w\\ \hline
s_r&(a+3,a)&h_2(x_r,x_{r+1})\\
s_r s_{r-1}&(a+3,a+\epsilon,a),\quad\epsilon\in\{0,1\}&
  x_{r-1}^{\epsilon}h_1(x_{r-1},x_r,x_{r+1})\\
s_r s_{r+1}&(a+2,a+2,a)&e_2(x_r,x_{r+1},x_{r+2}).
\end{array} \tag{3}
\]

In the middle line the displayed monomial is absent when
\(\epsilon=0\).  Every line may also have a common monomial factor,
which is irrelevant at principal specialization.

Here is a proof included to make the scope of the lemma explicit.
Weigandt proved

\[
\Upsilon_w\geq 1+p_{132}(w)
\]

by constructing a simple-ladder-move path from the bottom to the top
reduced pipe dream with exactly \(1+p_{132}(w)\) vertices.  Dominant
permutations have specialization one, and her two-term corollary says
that specialization two is equivalent to one 132 occurrence.  Hence
\(\Upsilon_w=3\) forces \(p_{132}(w)=2\), and the constructed
three-vertex path exhausts all reduced pipe dreams of \(w\).

Consider its two directed simple ladder moves.  If two different
moves were available at either nonterminal vertex, the alternative
edge would give a fourth reduced pipe dream.  The second move is
therefore either a second move of the same crossing, or a move of a
crossing which becomes available only when the first crossing vacates
its old cell.  In the latter situation that vacated cell is one of the
three empty cells required by the second simple move.  Thus, at the
level of row weights, the two moves have exactly the following forms:

\[
\begin{array}{ccl}
x_{q+2}&\longmapsto x_{q+1}\longmapsto x_q,
 &x_q+x_{q+1}+x_{q+2};\\
x_{q+1}^2&\longmapsto x_qx_{q+1}\longmapsto x_q^2,
 &h_2(x_q,x_{q+1});\\
x_{q+1}x_{q+2}&\longmapsto x_qx_{q+2}
  \longmapsto x_qx_{q+1},
 &e_2(x_q,x_{q+1},x_{q+2}).
\end{array} \tag{4}
\]

Here is the corresponding code calculation.  Row \(i\) of the bottom
pipe dream consists of the cells \(1,\ldots,c_i(w)\).  Its rightmost
cross can move simply into row \(i-1\) precisely when
\(c_{i-1}(w)<c_i(w)\).  The unique first move therefore lies at the
unique relevant code ascent; write its two row lengths as \(a<b\).

If the second move uses the next cross in the same row, exactly two
crosses protrude past the row above, so the local code of \(w\) is
\((a,a+2)\).  Swapping the corresponding adjacent ascent gives the
dominant local code \((a+3,a)\).

If the same cross moves twice, only one cross protrudes, so
\(b=a+1\).  The row above the destination has length at least \(a\)
(otherwise it supplies another initial move) and at most \(a+1\)
(otherwise the second move is blocked).  Thus the local code of \(w\)
is

\[
(a+\epsilon,a,a+1),\qquad \epsilon\in\{0,1\}.
\]

The two adjacent ascent swaps change it to
\((a+3,a+\epsilon,a)\).

In the remaining case, the second cross comes from the row below.  It
must be the rightmost cross directly below the vacated cell: the cell
immediately to its left is still occupied.  Hence the local code of
\(w\) is \((a,a+1,a+1)\), and the two ascent swaps change it to
\((a+2,a+2,a)\).  At the outer boundaries, a failure of weak decrease
would expose an additional simple move at the bottom or intermediate
diagram.  The three reconstructed codes are therefore weakly
decreasing, hence dominant.  Reading the swaps in the usual
pipe-dream word gives exactly (3).  This also proves the row-weight
factors there.  Notice that the four minimal polynomial models are

\[
1243,\quad2143,\quad1423,\quad1342;
\]

the middle line of (3) supplies the first two.

## Inflation and rectangular Schur functions

Let \(A,B,C\) be consecutive blocks of \(k\) variables, and let
\(\Delta_{AB}\) denote the divided difference for the minimal
permutation interchanging blocks \(A\) and \(B\).  It has length
\(k^2\).  Put \(p_A=\prod_{x\in A}x\), and similarly for the other
blocks.  Inflating the four minimal models in the two-move lemma gives
the standard Grassmannian divided-difference identities

\[
\begin{aligned}
\Delta_{AB}p_A^{3k}
  &=s_{((2k)^k)}(A\cup B),\\
\Delta_{BC}\Delta_{AB}p_A^{3k}
  &=s_{(k^k)}(A\cup B\cup C),\\
\Delta_{BC}\Delta_{AB}(p_A^{3k}p_B^k)
  &=p_A^k s_{(k^k)}(A\cup B\cup C),\\
\Delta_{AB}\Delta_{BC}(p_A^{2k}p_B^{2k})
  &=s_{(k^{2k})}(A\cup B\cup C).
\end{aligned} \tag{5}
\]

For completeness, these identities can be checked directly from the
definition of divided differences.  More conceptually, their left
sides are the Schubert polynomials of

\[
1423\otimes1_k,\quad1243\otimes1_k,\quad
2143\otimes1_k,\quad1342\otimes1_k,
\]

respectively.  The first, second, and fourth are Grassmannian with the
three displayed rectangular shapes.  The third has the fixed factor
\(p_A^k\), after which it is the same rectangle as the second.

Inflation of a dominant permutation is dominant, and its code is
obtained by repeating every code coordinate \(k\) times and
multiplying it by \(k\).  Therefore the common \(a\)-part in every
line of (3) becomes invariant under the block divided differences and
passes through them.  All variables outside the displayed blocks do
the same.  Equation (5) consequently shows that, up to a monomial
factor, \(\mathfrak S_{w\otimes1_k}\) is one of

\[
s_{((2k)^k)}(1^{2k}),\qquad
s_{(k^k)}(1^{3k}),\qquad
s_{(k^{2k})}(1^{3k}). \tag{6}
\]

By the hook-content formula these are, respectively, the plane
partition counts for boxes

\[
k\times2k\times k,\qquad
k\times k\times2k,\qquad
2k\times k\times k.
\]

MacMahon's product is symmetric in the three box dimensions, so all
three values equal the product in (1).

Finally, group the factors in (1) by \(t=i+j-1\), whose multiplicity
is \(m_t=\min(t,2k-t)\).  The middle factor \(t=k\) is \(3\), and for
\(1\leq t<k\),

\[
\left(1+\frac{2k}{t}\right)
\left(1+\frac{2k}{2k-t}\right)-9
=\frac{8(k-t)^2}{t(2k-t)}>0. \tag{7}
\]

Pairing \(t\) with \(2k-t\) in (1) now gives

\[
\operatorname{PP}(k,k,2k)
>\prod_{t=1}^{k-1}9^t\,3^k=3^{k^2}
\]

for \(k\geq2\), proving (2).

## Exact finite checks

`verify.py` implements the exact Lascoux--Schuetzenberger transition
recurrence.  It checks the two-move code classification for every
permutation through \(S_8\), and checks (1) in the following regimes:

* \(k=2\), every three-term permutation through \(S_7\);
* \(k=3\), every three-term permutation through \(S_6\);
* \(k=4\), every three-term permutation through \(S_5\).

It also checks the necessary pattern consequences used in the proof:
every three-term permutation in the range has exactly two 132
occurrences and no 1432 occurrence.  The converse is false (already
for \(35142\), whose specialization is four), and is not asserted.

Run from the repository root with Python 3.11 or later:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  algebraic_combinatorics/schubert_three_term_kronecker/verify.py
```

`verify_descent.py` is an independent implementation of Macdonald's
weighted descent recurrence.  It reproduces the \(k=2\) formula
through \(S_6\):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  algebraic_combinatorics/schubert_three_term_kronecker/verify_descent.py \
  --max-n 6
```

Both programs use only exact Python integers and rational arithmetic.
They use no external package, generated input, floating point,
randomness, or solver.  The theorem is the uniform divided-difference
argument above; the programs audit the local classification and its
predicted specialization in finite ranges.

With CPython 3.11.2, the complete standard output of `verify.py` has
SHA-256
`f233e7a39de8c73bed2afe2045f599d7e380c1c77c87946120d33c5f63d2cee6`
and ends with

```text
all exact checks passed; transition_cache_states=148225
```

The complete output of `verify_descent.py --max-n 6` has SHA-256
`d02e5dcf6497fc70c9c3ee5196e41c991573c6e3b3d77bb5d6ad276372b33483`
and ends with

```text
independent Macdonald-descent audit passed for 124 three-term permutations through S_6; cache_states=789486
```

## Sources and novelty scope

* A. H. Morales, I. Pak, and G. Panova, *Asymptotics of principal
  evaluations of Schubert polynomials for layered permutations*,
  Algebraic Combinatorics **2** (2019), Conjecture 4.1.
  <https://arxiv.org/abs/1805.04341>
* A. Weigandt, *Schubert polynomials, 132-patterns, and Stanley's
  conjecture*, Algebraic Combinatorics **1** (2018), Theorem 1.1.
  <https://arxiv.org/abs/1705.02065>
* Y. Gao, *Principal specializations of Schubert polynomials and
  pattern containment*, European Journal of Combinatorics **94**
  (2021), Theorems 2.1 and 4.1.
  <https://arxiv.org/abs/1910.08872>
* R. P. Stanley, *Some Schubert shenanigans* (2017), Section 4.
  <https://arxiv.org/abs/1704.00851>
* M. Bona, *Permutations with one or two 132-subsequences*, Discrete
  Mathematics **181** (1998), 267--274.
  <https://doi.org/10.1016/S0012-365X(97)00062-9>

Targeted searches of these sources, the recent Schubert-specialization
literature, citations around the identity-inflation conjecture, and
the committed Discovery Net graph found no prior formula (1) for the
three-term stratum.  The novelty assessment is search-relative, not a
claim of historical priority.
