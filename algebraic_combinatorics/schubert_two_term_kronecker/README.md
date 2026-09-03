# Identity inflation of two-term Schubert polynomials

## Result

For a permutation \(w\in S_n\), write

\[
\Upsilon_w=\mathfrak S_w(1,1,\ldots,1),
\]

and let \(w\otimes 1_k\in S_{kn}\) be the permutation whose matrix is
the Kronecker product of the permutation matrix of \(w\) and the
\(k\times k\) identity matrix.  Equivalently, each entry \(w_i\) is
replaced by the increasing block

\[
k(w_i-1)+1,\ldots,kw_i.
\]

**Theorem.** If \(\Upsilon_w=2\), then, for every \(k\geq 1\),

\[
\boxed{\quad
\Upsilon_{w\otimes 1_k}
=s_{(k^k)}(1^{2k})
=\prod_{i=1}^k\prod_{j=1}^k
  \frac{k+i+j-1}{i+j-1}.
\quad} \tag{1}
\]

The product is the number of plane partitions in a
\(k\times k\times k\) box.  In particular, for every \(k\geq2\),

\[
\Upsilon_{w\otimes 1_k}>2^{k^2}=\Upsilon_w^{k^2}. \tag{2}
\]

Thus the Morales--Pak--Panova identity-inflation conjecture holds,
strictly, on the first nontrivial specialization stratum
\(\Upsilon_w=2\).  Equation (2) also proves the natural all-\(k\)
extension recorded as Problem 14 in Worley's tableaux problem notebook
on this stratum.

The first values in (1) are

\[
2,\ 20,\ 980,\ 232848,\ 267227532,\ldots
\qquad (k=1,2,3,4,5,\ldots).
\]

## Proof

Let

\[
c_r(v)=\#\{s>r:v_s<v_r\}
\]

be the Lehmer code.  We use three standard facts.

1. A permutation \(v\) is dominant (equivalently, 132-avoiding) if
   and only if
   \(\mathfrak S_v=\prod_r x_r^{c_r(v)}\).
2. Weigandt's 132-bound, together with Stanley's two-term argument,
   says that \(\Upsilon_w=2\) if and only if \(w\) has exactly one
   132 occurrence.
3. If the unique occurrence is
   \(w_i,w_{i+1},w_j\), then \(u=ws_i\) is dominant and

   \[
   c_i(u)=c_{i+1}(u)+2. \tag{3}
   \]

For completeness, the last equality is immediate: among entries to
the right of positions \(i,i+1\), exactly one lies strictly between
\(w_i\) and \(w_{i+1}\), while entries below \(w_i\) contribute to both
code coordinates.  The adjacency and dominance statements are the
elementary reduction in Stanley's proof.

Put \(W=w\otimes1_k\) and \(U=u\otimes1_k\).  Inflation by increasing
blocks preserves 132-avoidance, so \(U\) is dominant.  Moreover, each
code coordinate is repeated \(k\) times and multiplied by \(k\):

\[
c_{k(r-1)+a}(U)=k c_r(u),
\qquad 1\leq a\leq k. \tag{4}
\]

Let \(y_1,\ldots,y_{2k}\) denote the variables in the two adjacent
inflated position blocks corresponding to \(i,i+1\), and put
\(d=kc_{i+1}(u)\).  By (3)--(4), the part of the dominant monomial
\(\mathfrak S_U\) involving these variables is

\[
(y_1\cdots y_{2k})^d(y_1\cdots y_k)^{2k}. \tag{5}
\]

The permutation \(U\) is obtained from \(W\) by interchanging these
two adjacent blocks.  This block interchange is the Grassmannian
permutation

\[
\tau=(k+1,\ldots,2k,1,\ldots,k)
\]

of length \(k^2\).  Applying the corresponding divided-difference
operator to \(\mathfrak S_U\) therefore gives \(\mathfrak S_W\).
All factors outside (5), as well as the first factor in (5), are
invariant under the local simple reflections and pass through the
divided differences.  The remaining standard Grassmannian calculation
is

\[
\partial_\tau (y_1\cdots y_k)^{2k}
=s_{(k^k)}(y_1,\ldots,y_{2k}). \tag{6}
\]

Indeed, (6) is exactly the Schubert-polynomial calculation for
\(132\otimes1_k\), whose sole descent is at \(2k\) and whose associated
partition is the \(k\times k\) rectangle.  Evaluating the resulting
factorization at all variables equal to one and applying the
hook-content formula gives (1).

It remains to prove the inequality without relying on numerical data.
In the last product in (1), group factors by
\(t=i+j-1\).  The multiplicity of \(t\in\{1,\ldots,2k-1\}\) is
\(m_t=\min(t,2k-t)\), and the corresponding factor is \(1+k/t\).
For \(1\leq t<k\), pair \(t\) with \(2k-t\).  Then

\[
\left(1+\frac{k}{t}\right)
\left(1+\frac{k}{2k-t}\right)-4
=\frac{3(k-t)^2}{t(2k-t)}>0. \tag{7}
\]

Each member of this pair has multiplicity \(t\), while the middle
factor \(t=k\) is \(2\) with multiplicity \(k\).  Consequently

\[
s_{(k^k)}(1^{2k})
>\prod_{t=1}^{k-1}4^t\,2^k
=2^{k(k-1)+k}=2^{k^2}
\]

for \(k\geq2\), proving (2).  \(\square\)

## Exact finite evidence beyond the theorem

The accompanying transition-recurrence implementation exhaustively
checks the identity-inflation inequality in the following regimes:

* \(k=2\), every \(w\in S_n\) for \(n\leq7\) (5,913 permutations);
* \(k=3\), every \(w\in S_n\) for \(n\leq5\) (153 permutations);
* \(k=4\), every \(w\in S_n\) for \(n\leq4\) (33 permutations).

There is no counterexample.  After excluding the dominant stratum
\(\Upsilon_w=1\), the smallest ratio is always attained on
\(\Upsilon_w=2\), and is the quotient of (1) by \(2^{k^2}\).  In
particular the exhaustive \(k=2\) check extends the \(n\leq5\) range
reported with the original conjecture through \(n=7\).

The transition verifier uses the exact Lascoux--Schuetzenberger
recurrence with integer addition.  A separate implementation of
Macdonald's descent recurrence uses different mathematics--weighted
descent deletion and exact divisibility--and independently reproduces
the full \(k=2\) census through \(S_6\).  The latter check is more
resource-intensive because its memoized weak-order ideals contain
about 8.8 million states.

Run the main census from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  algebraic_combinatorics/schubert_two_term_kronecker/verify_transition.py
```

Run the independent descent audit (the default stops at \(S_5\); the
published full audit used \(S_6\)):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  algebraic_combinatorics/schubert_two_term_kronecker/verify_descent.py \
  --max-n 6
```

Both programs use only exact Python integers, tuples, and rational-free
integer recurrences.  They use no external package, floating point,
randomness, solver, or generated input.  The universal theorem rests on
the divided-difference proof above; the computations provide finite
evidence and implementation-level checks, not an extrapolation.

The main run ends with

```text
k=4: verified 33 permutations through S_4; cache_states=866858
all requested exact transition censuses passed
```

and its complete standard output has SHA-256
`bf7fdcd40772ac33e73486b55d8445e089b7457681a31d37f8292f0b1391a52d`.
The independent `--max-n 6` run ends with

```text
independent Macdonald-descent audit passed for 873 permutations through S_6; cache_states=8756040
```

and its complete standard output has SHA-256
`315c76fe63b671fe1be572aa9278f55e850ad1e10cb2066a5cc29a3761e9abbe`.
These are compact output digests; the run logs themselves are deliberately
not stored in the repository.

## Sources and novelty scope

* A. H. Morales, I. Pak, and G. Panova, *Asymptotics of principal
  evaluations of Schubert polynomials for layered permutations*,
  Algebraic Combinatorics **2** (2019), Conjecture 4.1.
  <https://arxiv.org/abs/1805.04341>
* A. Weigandt, *Schubert polynomials, 132-patterns, and Stanley's
  conjecture*, Algebraic Combinatorics **1** (2018), Corollary 1.2.
  <https://arxiv.org/abs/1705.02065>
* R. P. Stanley, *Some Schubert shenanigans* (2017), Section 4.
  <https://arxiv.org/abs/1704.00851>
* D. Anderson, G. Panova, and L. Petrov, *Computation and sampling for
  Schubert specializations* (2026), Sections 2.2--2.4.
  <https://arxiv.org/abs/2603.20104>
* D. R. Worley, *On the combinatorics of tableaux---a notebook of open
  problems* (version 3, 2026), Problem 14.
  <https://arxiv.org/abs/2509.25446>

Targeted searches of these sources, citations around the
identity-inflation conjecture, two-term Schubert polynomials, rectangle
specializations, and the committed Discovery Net graph found no prior
statement of formula (1) or this specialization of the conjecture.  The
novelty assessment is therefore search-relative and is not a historical
priority claim.
