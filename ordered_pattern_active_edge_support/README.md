# Active-edge support and the flip threshold for ordered pattern cliques

## Result

Let \(P\) be an \(r\)-partite \(r\)-pattern.  Normalize its block
orientation vector to

\[
\epsilon=(\epsilon_1,\ldots,\epsilon_r)\in\{+1,-1\}^r,\qquad
\epsilon_1=+1,
\]

and let

\[
f(P)=\#\{i<r:\epsilon_i\ne\epsilon_{i+1}\},\qquad h=f(P)+1.
\]

Fix \(m\ge2\), \(s\ge0\), and \(N=rm+s\).  Call an \(r\)-edge of
\([N]\) *active* if it belongs to at least one order-preserving copy of
\(P^{(m)}\).  Then the number of active edges is exactly

\[
\boxed{
A(P;m,s)
=m\binom{r+s}{r}
 -(m-1)\binom{r+s-f(P)-1}{r},
}
\tag{1}
\]

where the second binomial coefficient is zero when its upper argument is
less than \(r\).

Consequently, an edge-disjoint family of
\(\binom{r+s}{r}\) copies of \(P^{(m)}\) on \([N]\) exists if and only if
\(s\le f(P)\).  More generally, every edge-disjoint family has size at
most

\[
\binom{r+s}{r}
-\left\lceil
\frac{m-1}{m}\binom{r+s-f(P)-1}{r}
\right\rceil .
\tag{2}
\]

The selected-copy construction in the earlier flip-depth theorem attains
the required family for \(s\le f(P)\).  Formula (1) proves that its failure
at \(s=f(P)+1\) is global: no exchange or alternative choice of copies can
produce a packing of the conjectured blocker size.

For a one-flip pattern at the first unresolved boundary \(N=rm+2\),

\[
A(P;m,2)=m\binom{r+2}{r}-(m-1).
\]

Thus at most \(\binom{r+2}{r}-1\) canonical copies can be pairwise
edge-disjoint.  This rules out the proposed one-exchange repair of the
packing proof.

## Proof

### Canonical copies and a universal selected family

On \([rm]\), number the \(m\) edges of the unique canonical clique by
\(j=1,\ldots,m\), and put

\[
p_i(j)=
\begin{cases}
j,&\epsilon_i=+1,\\
m+1-j,&\epsilon_i=-1,
\end{cases}
\qquad
b_i(j)=(i-1)m+p_i(j).
\tag{3}
\]

Every copy of \(P^{(m)}\) on \([N]\) is uniquely determined by the
\(s\)-set \(X\) omitted from \([N]\).  Let \(\phi_X:[rm]\to[N]\setminus X\)
be the increasing bijection.

For a weakly increasing \(s\)-tuple
\(Q=(q_1,\ldots,q_s)\) from \(\{0,\ldots,r\}\), define

\[
X_Q=\{q_t m+t:1\le t\le s\},\qquad
c_Q(i)=\#\{t:q_t<i\}.
\tag{4}
\]

These are valid omitted positions, and the corresponding selected copy has
edges

\[
E_{j,Q}=\{b_i(j)+c_Q(i):1\le i\le r\}.
\tag{5}
\]

The selected family contains \(\binom{r+s}{r}\) copies.

It also contains every active edge.  Indeed, take an arbitrary omitted set
\(X\), a rank \(j\), and write

\[
e_i=\phi_X(b_i(j)),\qquad c_i=e_i-b_i(j).
\]

The insertion counts satisfy
\(0\le c_1\le\cdots\le c_r\le s\).  Define

\[
\mu_0=c_1,\quad
\mu_i=c_{i+1}-c_i\ (1\le i<r),\quad
\mu_r=s-c_r.
\tag{6}
\]

Then \(\mu=(\mu_0,\ldots,\mu_r)\) is a weak composition of \(s\).
Taking \(Q\) to contain \(\mu_t\) copies of \(t\) gives
\(c_Q(i)=c_i\), so (5) is exactly the original edge.  The reverse
inclusion is immediate because every selected edge lies in its selected
copy.

### The composition-orbit invariant

Represent \(Q\) by its multiplicity composition
\(\mu_Q=(\mu_0,\ldots,\mu_r)\).  Define

\[
\delta=(\epsilon_1,\epsilon_2-\epsilon_1,\ldots,
\epsilon_r-\epsilon_{r-1},-\epsilon_r)\in\mathbb Z^{r+1}.
\tag{7}
\]

Coordinatewise comparison in (5) gives the exact collision criterion

\[
E_{j,Q}=E_{k,R}
\quad\Longleftrightarrow\quad
\mu_R-\mu_Q=(j-k)\delta.
\tag{8}
\]

Hence an active edge is encoded injectively by

\[
\lambda=\mu_Q+j\delta,
\]

and active edges are in bijection with

\[
\bigcup_{j=1}^{m}\bigl(\mathcal C_s+j\delta\bigr),
\qquad
\mathcal C_s=\{\mu\in\mathbb Z_{\ge0}^{r+1}:|\mu|=s\}.
\tag{9}
\]

The positive and negative parts of \(\delta\) each have mass
\(h=f(P)+1\): the two endpoints of (7) contribute total absolute mass
\(2\), and every sign change contributes \(2\).

Two adjacent translates in (9) therefore intersect in a copy of
\(\mathcal C_{s-h}\), of size
\(\binom{r+s-h}{r}\), with the convention that this is zero for \(s<h\).
Moreover, if a point of \(\mathcal C_s+j\delta\) lies in
\(\mathcal C_s+k\delta\) for \(k<j\), its nonnegative representative in
the latter translate forces its representative \(\mu+\delta\) in the
immediately preceding translate to be nonnegative.  Thus every overlap
with an earlier translate is already an overlap with the adjacent one.
Adding the translates successively gives (1).

### Packing consequence

Every copy has \(m\) active edges.  If \(K\) copies are pairwise
edge-disjoint, their \(Km\) edges are distinct members of the active
support, so \(Km\le A(P;m,s)\).  Taking the integer part gives (2).
When \(s\ge h\), the subtracted binomial coefficient is positive, and
(2) is strictly smaller than \(\binom{r+s}{r}\).  When \(s\le f(P)\),
the previously constructed selected copies are pairwise edge-disjoint,
giving the converse.

## What this does and does not settle

Anastos, Jin, Kwan, and Sudakov conjectured

\[
\operatorname{ex}_{<}(n,P^{(m)})
=\binom nr-\binom{(n-r(m-1))_+}{r}
\]

for every \(r\)-partite pattern \(P\).  They proved the lower bound, every
\(m=2\) case, and all \(n\) for the alternating pattern.  The conjecture
remains open in general.

The result here is an exact support and packing theorem, not a
counterexample to that extremal conjecture.  The desired transversal lower
bound need not admit a proof through an edge-disjoint packing.  In
particular, the one-flip \(rm+2\) case now requires a genuinely non-packing
lower bound for the transversal number.

Primary source:
Michael Anastos, Zhihan Jin, Matthew Kwan, and Benny Sudakov,
*Extremal, enumerative and probabilistic results on ordered hypergraph
matchings*, Forum of Mathematics, Sigma 13 (2025), e55,
[DOI](https://doi.org/10.1017/fms.2024.144);
[open manuscript](https://arxiv.org/abs/2308.12268).
The source states the general formula as Conjecture 1.20 and defines the
ordered-pattern framework used here.

The graph-local predecessors are the \(rm+1\) boundary theorem and the
flip-depth theorem.  A targeted primary-literature and Discovery Net search
through 2026-09-20 found no earlier active-support formula or global packing
threshold of the form (1)--(2).  This is a search-relative novelty statement,
not a priority claim.

## Reproduction

Requires only Python 3.11 or later.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
sha256sum -c SHA256SUMS
```

The verifier independently constructs every canonical copy for a bounded
test box, unions their actual edges, and compares that support with the
selected family and formula (1).  It also audits the collision invariant,
translated-simplex intersections, packing threshold, and sharp collision
witnesses.  Exact integer and set operations only are used.

The computation corroborates the proof; it is not a substitute for the
parameter-free argument above.
