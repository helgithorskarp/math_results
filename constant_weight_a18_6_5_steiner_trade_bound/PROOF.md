# Steiner seed trade capacity

Agent: **six-code-2**. Role: **researcher**. Date: 2026-09-30.

Let \(D\) be a Steiner \(S(3,k,v)\), \(k\ge5\), on \(V\), with \(b\)
blocks. Add a point \(x\), and let \(F\) be any family of \(k\)-subsets
of \(V\cup\{x\}\) whose distinct members intersect in at most two points.
Define

- \(R=|D\setminus F|\), the number of removed design blocks;
- \(s\), the number of blocks of \(F\) avoiding \(x\) and outside \(D\);
- \(a\), the number of blocks \(\{x\}\cup Q\in F\) with \(Q\) contained
  in a block of \(D\);
- \(t\), the number of remaining blocks through \(x\).

With \(L=\binom{k-1}{3}\) and \(M=\binom{k-2}{3}+1\), we prove

\[
 R\ge a+\left\lceil\frac{tL}{M}\right\rceil,
 \qquad |F|\le b+s+t-\left\lceil\frac{tL}{M}\right\rceil. \tag{1}
\]

Since \(L>M\), a packing whose blocks avoiding \(x\) all belong to
\(D\) has size at most \(b\), with a strict loss when \(t>0\).
For \(k=5,6\), \(L=2M\), so \(|F|\le b+s-t\).
The unrestricted family may have \(s>0\); (1) is a conditional trade
bound and supplies no unrestricted upper bound of \(b\).

## Local capacity

Suppose \(H\) is a family of subsets of a \(k\)-set, with sizes
between 3 and \(k-2\), and any two members of \(H\) intersect in at
most one point. Then

\[
 \sum_{S\in H}\binom{|S|}{3}\le M. \tag{2}
\]

For a nonempty family choose a largest member \(A\), of size \(m\),
and put \(r=k-m\). Any other member \(S\) meets \(A\) in at most one
point. Writing \(j=|S\setminus A|\), we have \(2\le j\le r\), and

\[
 \binom{|S|}{3}\le\binom{j+1}{3}
   =\frac{j+1}{3}\binom{j}{2}
   \le\frac{r+1}{3}\binom{j}{2}.
\]

The pairs in \(S\setminus A\) are disjoint between different \(S\).
Their total number is at most \(\binom r2\). Thus the contribution
of members other than \(A\) is at most \(\binom{r+1}{3}\). Finally,

\[
 M-\binom m3-\binom{k-m+1}{3}
   =\frac{(k-1)(m-3)(k-2-m)}2\ge0
\]

for \(3\le m\le k-2\). This proves (2); the empty case is immediate.
The bound is attained by a \((k-2)\)-set and a 3-set consisting of
one of its points and the two outside points.

## Allocate old triples

For two different blocks through \(x\), their old subsets \(Q\)
intersect in at most one point. A contained \(Q\) lies in a unique
design block \(C\), since it contains a triple, and \(C\) must be
removed. If another \(Q'\) met \(C\) in at least three points,
it would meet \(Q\) in at least two: \(Q\) omits only one point of
\(C\). This is impossible. Therefore the \(a\) contained words
reserve distinct removed design blocks, and no noncontained \(Q'\)
has a triple in one of them.

For a noncontained \(Q\), an intersection \(Q\cap C\) of size at
least three has size at most \(k-2\). For a fixed \(C\), these
intersections form a family of the kind in (2). Every one of the
\(L\) triples of each noncontained \(Q\) belongs to exactly one
design block, which must be removed because it conflicts with
\(\{x\}\cup Q\). Summing (2) over removed blocks gives

\[
 tL\le (R-a)M.
\]

Take the integer ceiling and use \(|F|=b-R+s+a+t\) to obtain (1).
Also \(L-M=\binom{k-2}{2}-1>0\) for \(k\ge5\).

## Small numbers of new words when k=5

A noncontained old 4-set \(Q\) has four triples, each in a different
design block. A design block covers triples of at most two such
\(Q\), by (2). Two compatible old 4-sets share at most one blocking
design block. To see this, disjoint 4-sets cannot both have triples
in a 5-set. Otherwise their common point is \(p\). A shared blocking
block consists of \(p\), two points of \(Q\setminus\{p\}\), and two
points of \(Q'\setminus\{p\}\). Two different shared blocks would
meet in \(p\) and at least one point from each of these disjoint
3-sets, contradicting the Steiner property.

Consequently shared blocking blocks define a simple graph on the
\(t\) noncontained words, of maximum degree at most four. If it has
\(e\) edges, the union of their blocking blocks has exactly \(4t-e\)
members. It avoids the \(a\) reserved blocks. Therefore

\[
 R\ge a+\max\left(2t,4t-\binom t2\right). \tag{3}
\]

The deletion requirements \(R-a\) for \(t=0,1,2,3,4\) are
\(0,4,7,9,10\), respectively. Equation (3) requires \(2t\) for
\(t\ge5\). All arguments through (3) are ordinary combinatorial
proofs and hold for any \(S(3,5,v)\).

## Exact refinement for five words in the classical S(3,5,17)

`steiner.py` constructs the classical design as the distinct
\(\mathrm{PGL}(2,16)\) images of \(\mathbf P^1(4)\) in
\(\mathbf P^1(16)\). Its validity is checked directly by
pair intersections and all 680 triples. No uniqueness theorem
for inversive planes is needed.

There are 340 contained and 2040 noncontained old 4-sets. Form a
graph on the latter, joining two exactly when they intersect in at
most one point and have a shared blocking design block. `verify.py`
constructs every vertex and edge directly, then enumerates increasing
cliques without pruning based on an assumed upper bound. The census
is 134640 edges, 194480 triangles, 4080 four-cliques, and no five-clique.
Every four-clique has a common old point. For every four-clique the
checker examines every possible fifth vertex adjacent to any three
of its members, and tests compatibility with all four; none gives
nine shared blocking blocks.

If five compatible noncontained words shared at least nine blocking
blocks, their simple graph on five vertices would be \(K_5\), or
\(K_5\) with one edge deleted. Both possibilities contain a four-clique
and are covered by the two exhaustive checks. Thus \(e\le8\), and

\[
 t=5\quad\Longrightarrow\quad R\ge a+12. \tag{4}
\]

Equation (4) is an exact computer-assisted statement about this
classical design and its coordinate relabelings. The source supplies
ordinary finite reductions and a complete small enumeration, rather
than a solver verdict. It is not formally verified.

The checker also reconstructs valid packings attaining (3) for
\(t=1,2,3,4\) and (4) for \(t=5\), with \(a=s=0\). Hence among
all packings with \(s=0\) and a specified \(t\in\{0,\ldots,5\}\),
allowing arbitrary \(a\), the exact maximum sizes are

| t | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| maximum packing size | 68 | 65 | 63 | 62 | 62 | 61 |

The 68-word design attains the \(t=0\) entry. The remaining small
witnesses are listed as old-point masks in `expected.json`; the
checker removes their blocking circles and appends the new words,
then directly checks all resulting word pairs.

## Necessary cuts for a 70-word C5 construction

The permutation in `expected.json` multiplies finite field elements
by an element of order five and fixes points 0, 16 and 17. Its cycle
type is \(5^3 1^3\). There are three fixed 5-subsets. Thus an invariant
70-word code must consist of 14 full orbits and contain no fixed words.
Of all full block orbits, 1125 have mutually compatible members.
They each cover ten of the 163 nonfixed triple orbits; selecting 14
with disjoint covered rows is equivalent to constructing such a code.
The single fixed triple cannot occur in an admissible full block orbit.

For the original circle design write \(h,u,w\) for selected orbits of
old circles, contained words through point 17, and noncontained words
through point 17. Then \(R=68-5h\), \(a=5u\), \(t=5w\), and (1) gives

\[
 h+u+2w\le13. \tag{5}
\]

Swap point 17 with either of the other fixed points to obtain two
additional circle designs. Equation (5) applies to each of these
three seeds. `steiner.py` reproduces every orbit and all three weight
classifications. No search outcome or absence of an invariant 70-word
code is asserted.

## Literature and limits

[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html)
still gives \(69\le A(18,6,5)\le72\), checked 2026-09-30. The known
69-word construction is [Aw, Chee and Ling, 2003, Theorem 1 and
Appendix A](https://ymchee66.github.io/home/PDF/6cwc.pdf). The classical
68-circle design is existing mathematics. [Kiermaier, Krcadinac and
Wassermann, arXiv:2509.23483](https://arxiv.org/html/2509.23483v1)
documents the inversive-plane family; its extensions increase design
strength and block size, which is a different operation from the
fixed-block-size trades studied here. The exact quantitative trade
statements above were not located in the bounded primary-source
search; no priority claim is made.

The universal proof (1)--(3), the finite classical refinement (4),
and the exact symmetry reduction (5) have separate stated scopes.
The finite checks of the polynomial identity for \(5\le k\le100\)
corroborate the algebra; they do not prove its unbounded assertion.
Python 3.11.2 standard-library integer/set arithmetic is the computational
trust boundary. No floating point, solver, heuristic failure or
unpublished data is used in any proof. Independent review and
proof-assistant verification are not claimed. The global 69--72 gap
remains unresolved.
