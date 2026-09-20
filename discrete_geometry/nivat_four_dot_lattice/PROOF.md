# Binary four-dot systems: a lattice criterion and exact witness windows

## Definitions and statement

All configurations take values in \(\mathbb F_2\) on \(\mathbb Z^2\).
For a finite nonempty set \(D\), let
\[
 P_c(D)=|\{(c(z+d))_{d\in D}:z\in\mathbb Z^2\}|.
\]
A configuration is periodic if it has at least one nonzero translation
period. A subshift has the **generalized Nivat property** (GNP) if every
configuration in it satisfying \(P_c(D)\leq |D|\) for some finite nonempty
set \(D\) is periodic. No convexity or rectangularity is imposed on \(D\).

Write \(X^w=X^{w_1}Y^{w_2}\), and let a Laurent polynomial act on
configurations by convolution: \((fc)(z)=\sum_w f_w c(z-w)\).
For linearly independent integer vectors \(u,v\), put
\[
 L=\mathbb Zu+\mathbb Zv,\qquad q=|\det(u,v)|,\qquad
 X_{u,v}=\ker((1+X^u)(1+X^v)).
\]

**Theorem 1.** \(X_{u,v}\) has GNP if and only if \(q=1\).

The positive implication imports the ordinary binary four-dot theorem
of Kari and Moutot [KM, journal Theorem 11; author manuscript Theorem 10].
The negative implication generalizes their separated-line construction
[KM, journal Theorem 12; manuscript Theorem 11].
The following proof gives the exact window language for every \(D\subset L\),
including the smallest low-complexity windows for this construction.
It does not resolve the original rectangular Nivat conjecture.

## The unimodular implication

If \(q=1\), the map \(U:\mathbb Z^2\to\mathbb Z^2\),
\(U(a,b)=au+bv\), is a bijection. For \(c\in X_{u,v}\), define
\(\widetilde c(a,b)=c(U(a,b))\). The constraint becomes
\((1+X)(1+Y)\widetilde c=0\).
Every finite window and every translating vector correspond bijectively:
\[
 P_{\widetilde c}(U^{-1}D)=P_c(D),\qquad |U^{-1}D|=|D|.
\]
By the cited ordinary four-dot theorem, low complexity makes
\(\widetilde c\) periodic. Its nonzero period maps to a nonzero period of
\(c\). This proves the positive implication.

## A separated-coset construction at every larger index

Suppose \(q>1\), and fix any \(t\in\mathbb Z^2\setminus L\). Define
\[
 c(z)={\bf1}_{\mathbb Zu}(z)+{\bf1}_{t+\mathbb Zv}(z)
 \quad\hbox{in }\mathbb F_2. \tag{1}
\]
These two arithmetic lines lie in distinct \(L\)-cosets, so their supports
are disjoint. The first summand has period \(u\), and the second has
period \(v\). Commutativity of the shift operators gives
\((1+X^u)(1+X^v)c=0\). Thus \(c\in X_{u,v}\).
The vectors need not be primitive.

**Lemma 2 (a two-point certificate against every proposed period).**
For each nonzero \(w\in\mathbb Z^2\), there is a support point \(z\)
with \(c(z+w)=0\). If \(\det(u,w)\ne0\), one can choose \(z\in\{0,u\}\).
Otherwise one can choose \(z\in\{t,t+v\}\).

**Proof.** In the first case both \(w\) and \(u+w\) are off the real line
\(\mathbb Ru\). Their difference is \(u\), which is not parallel to \(v\),
so at most one belongs to \(t+\mathbb Rv\). At least one therefore belongs
to neither supporting real line. The original points \(0,u\) both have
value one. In the other case \(w\) is parallel to \(u\), hence is not
parallel to \(v\). Both \(t+w,t+v+w\) are off \(t+\mathbb Rv\), and at
most one is on \(\mathbb Ru\). Again one translation changes a one to a
zero. This proves the lemma and the nonperiodicity of (1). \(\square\)

## Exact window complexity

For a nonempty finite \(D\subset L\), let
\[
 A=\{(a,b)\in\mathbb Z^2:au+bv\in D\}.
\]
Let \(r\) be the number of distinct second coordinates (rows), \(s\) the
number of distinct first coordinates (columns), and \(i\) the number of
points of \(A\) that are alone in both their row and their column.

**Theorem 3.** For the configuration (1),
\[
 \boxed{P_c(D)=1+r+s-i.} \tag{2}
\]
Its full window language consists of the zero pattern, each nonempty
row indicator of \(A\), and each nonempty column indicator of \(A\).

**Proof.** A translate \(z+D\) lies in the single coset \(z+L\).
If \(z=\alpha u+\beta v\in L\), its ones occur exactly at the sites with
\(b=-\beta\). If \(z=t+\alpha u+\beta v\in t+L\), its ones occur exactly
at the sites with \(a=-\alpha\). Every other coset gives the zero pattern.
Even when there are only two cosets, the zero pattern occurs by choosing
\(-\beta\) outside the finite row set in the first coset.
All row and column indicators are attained by these choices of shifts.
Different nonempty rows have different masks, as do different columns.
A row mask can equal a column mask only when both consist of their unique
intersection point. Such coincidences are counted exactly by \(i\).
The zero pattern is distinct from all of them, proving (2). \(\square\)

Take \(A=\{0,1,2\}\times\{0,1\}\). Then \(|D|=6\) and \(P_c(D)=6\).
Together with Lemma 2 this disproves GNP whenever \(q>1\), and completes
Theorem 1.

## Sharp size thresholds within the construction

The following assertions concern the specific configuration (1) and
windows \(D\subset L\). They are not global assertions about arbitrary
configurations or windows meeting several \(L\)-cosets.

Represent \(A\) by its simple bipartite incidence graph: one vertex per
occupied row, one per occupied column, and one edge per point.
Put \(e=|A|\). A point counted by \(i\) is precisely an isolated-edge
component. Removing all such components leaves a graph with
\[
 e'=e-i,\qquad n'=r+s-2i,\qquad
 P_c(D)-e=1+n'-e'. \tag{3}
\]
The empty residual graph is allowed and has \(e'=n'=0\).

**Corollary 4.**

1. The smallest possible size with \(P_c(D)\leq |D|\) is six.
   At size six this holds exactly when the incidence graph is \(K_{2,3}\),
   with either choice of its bipartition. In this case \(P_c(D)=6\).
2. The smallest possible size with \(P_c(D)<|D|\) is eight.
   At size eight this holds exactly for \(K_{2,4}\) or \(K_{3,3}\) with
   one edge removed, up to swapping the two parts. In both cases
   \(P_c(D)=7\).

The row and column coordinates need not be consecutive.

**Proof.** A bipartite graph on \(n'\) vertices has at most
\(\lfloor(n')^2/4\rfloor\) edges. If \(e'\leq5\), then \(e'\leq n'\):
for \(n'\leq4\) use this bipartite bound; for \(n'\geq5\) use \(e'\leq5\).
Thus (3) rules out low complexity when \(e\leq5\).
If \(e=6\) and low complexity holds, \(i=0\), since otherwise the residual
graph has at most five edges. Equation (3) gives \(n'\leq5\).
The bipartite bound forces \(n'=5\), part sizes two and three, and all six
edges.

If \(e'\leq7\), then \(e'\leq n'+1\):
for \(n'\leq5\) use the bipartite bound; for \(n'\geq6\) use \(e'\leq7\).
Thus (3) rules out strict low complexity at size at most seven.
At size eight strict low complexity again forces \(i=0\), and \(n'\leq6\).
Eight edges force \(n'=6\); the possible part sizes are two and four,
or three and three. Eight edges then give exactly the two graphs in the
statement. Formula (2) verifies all the asserted equalities. \(\square\)

## A factor obstruction even when the total support spans the lattice

**Corollary 5.** If \(f\in\mathbb F_2[X^{\pm1},Y^{\pm1}]\) is divisible by
\((1+X^u)(1+X^v)\) with \(|\det(u,v)|>1\), then \(\ker f\) fails GNP.

**Proof.** The configuration (1) is in the kernel of the divisor and
therefore in \(\ker f\). Its nonperiodicity and its six-site window do
not depend on the additional factor. \(\square\)

In particular, if a product of binomials \(\prod_j(1+X^{w_j})\) has GNP,
every linearly independent pair of its direction vectors must have
determinant of absolute value one. No converse for three or more factors
is asserted here.

Consider the concrete example
\[
 f=(1+X)(1+XY^2)(1+Y).
\]
Its support is
\[
 \{(0,0),(0,1),(1,0),(1,1),(1,2),(1,3),(2,2),(2,3)\}.
\]
It contains \(0,(1,0),(0,1)\), so its support differences generate all of
\(\mathbb Z^2\). Moreover, \(f\) is square-free in the Laurent polynomial
ring. Indeed each of its three direction vectors is primitive, so a
unimodular monomial change takes its binomial to \(1+X\), a prime
polynomial. The three directions are nonparallel, so these prime factors
are nonassociate.

Nevertheless the pair \(u=(1,0),v=(1,2)\) has determinant two.
With \(t=(0,1)\), formula (1) gives a nonperiodic member of \(\ker f\)
whose six-site window has six patterns. Thus full generation by the
support differences, even together with square-freeness and primitive
binomial factors, is not sufficient for GNP.

This example still inherits its failure from a proper-sublattice
divisor. It is not a new mechanism avoiding such divisors, and it does
not answer any strengthened question that excludes them.

## What the computation checks

The proof above is an ordinary mathematical proof, conditional in its
positive direction on the cited ordinary four-dot theorem. The script
does not prove infinite nonperiodicity by a finite search.

For each finite coordinate set \(A\), it takes
\[
 N=2+\max\{\max a-\min a,\ \max b-\min b\}
\]
and evaluates every translation of a periodized configuration on
\(\mathbb Z^2/(NL)\). On the coset \(L\) this configuration has ones when
the \(v\)-coordinate is zero modulo \(N\); on \(t+L\) it has ones when
the \(u\)-coordinate is zero modulo \(N\); it is zero elsewhere.
Because \(N\) exceeds each coordinate span and the number of occupied
coordinates, its window language is exactly the row/column/zero
language of (1). There is no modular merging of distinct rows or
columns, and a blank residue is available. This justifies comparison of
the finite quotient language with the infinite-window formula.

The quotient computation uses physical integer coordinates and exact
Cramer numerators for membership in \(L\). A separate incidence-mask
calculation gives the proposed language. The verifier compares the
complete sets, not just their cardinalities. It also checks finitely
many explicit annihilator equations and period separators, the sharp
small-window classifications on a finite grid, the displayed polynomial
expansion, and rejection of three invalid construction inputs.
These finite checks corroborate the written arguments; the universal
quantifiers follow from the proofs, not an enumeration of all lattices.

[KM] J. Kari and E. Moutot, *Nivat's conjecture and pattern complexity in
algebraic subshifts*, Theoretical Computer Science 777 (2019), 379–386.
[Author manuscript](https://emoutot.perso.math.cnrs.fr/static/publi/karimoutot19.1.pdf).
