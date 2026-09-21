# Exact boundary profiles for Fan--Raspaud triples under 2-edge sums

This note isolates the complete interface carried by a Fan--Raspaud triple
across a 2-edge-cut.  It also gives an exact min-plus composition law for the
number of uncovered edges.  The result is uniform in the orders of the two
graphs; the accompanying computation only audits the definitions on small
examples.

## Definitions

All graphs below are finite, loopless cubic multigraphs.  A **regular
3-array** of a graph `X` is an indexed triple

\[
   \mathcal M=(M_1,M_2,M_3)
\]

of perfect matchings, with repetitions allowed, such that
`M_1 intersection M_2 intersection M_3` is empty.  Thus it is the same object
as an FR-triple, with indices retained.  Let

\[
 u_X(\mathcal M)=|E(X)\setminus(M_1\cup M_2\cup M_3)|.
\]

For an edge `e` of `X` and `k in {0,1,2}`, define the extended boundary
profile

\[
 \rho_k(X,e)=\min\{u_X(\mathcal M):\mathcal M\text{ is regular and }
                      |\{i:e\in M_i\}|=k\},                 \tag{1}
\]

where the minimum of the empty set is infinity.  Put

\[
 \widehat{\operatorname{rdf}}(X)=\min_{k=0,1,2}\rho_k(X,e).
\]

The right side is independent of `e`.  When `X` has an FR-triple, this is
the usual regular colouring defect.  The hat merely records infinity when
there is no regular array, instead of adopting the finite fallback convention
sometimes used in the literature.

The indexed convention agrees with the frequency formulation of
Mkrtchyan--Vardanyan.  Repetitions matter only for the transparent-lobe
construction below: if a regular triple has two equal entries, the graph is
already 3-edge-colourable.

Let `A` and `B` be bridgeless cubic graphs with distinguished edges
`a=x_1 x_2` and `b=y_1 y_2`.  Their **2-edge sum** `G=A(a)*B(b)` deletes `a`
and `b` and adds `x_1 y_1,x_2 y_2`.  The crossed pairing gives the same
statements.

## Boundary-profile bijection

For a regular array `mathcal M` on `(X,e)`, retain the full boundary support

\[
 I_e(\mathcal M)=\{i\in\{1,2,3\}:e\in M_i\}.
\]

**Theorem 1 (exact gluing).**  Regular arrays of `G=A(a)*B(b)` are in
bijection with pairs of regular arrays `(mathcal A,mathcal B)` on `A,B`
satisfying

\[
 I_a(\mathcal A)=I_b(\mathcal B).                          \tag{2}
\]

Under this bijection,

\[
 u_G(\mathcal M)=u_A(\mathcal A)+u_B(\mathcal B).          \tag{3}
\]

Consequently,

\[
 \boxed{\quad
 \widehat{\operatorname{rdf}}(A(a)*B(b))
   =\min_{k\in\{0,1,2\}}
      \bigl(\rho_k(A,a)+\rho_k(B,b)\bigr).
 \quad}                                                    \tag{4}
\]

The formula is independent of the choice of straight or crossed pairing.

### Proof

Let `D` be the two new edges of the sum and let `N` be a perfect matching of
`G`.  Since `|V(A)|` is even, the matching-cut parity identity gives

\[
 |N\cap D|\equiv |V(A)|\equiv0\pmod2.
\]

Thus `N` uses either no edge of `D` or both edges.  In the first case its
restriction is a perfect matching of `A` avoiding `a` and a perfect matching
of `B` avoiding `b`.  In the second case, delete the two cut edges and insert
`a` and `b`; this produces perfect matchings of both factors containing their
marker edges.  These operations are inverse.  Applied independently in the
three indexed rows, they give a bijection between all 3-arrays on `G` and
pairs of 3-arrays having equal boundary support.

An internal edge is triply covered before gluing exactly when the
corresponding internal edge is triply covered afterwards.  Each new cut edge
is triply covered exactly when the two marker edges have support
`{1,2,3}`.  Hence restricting and gluing preserve regularity, proving the
bijection in Theorem 1.

It remains to check uncovered edges.  If the common support is nonempty,
the two deleted marker edges and the two new cut edges are all covered.  If
the support is empty, the two deleted marker edges were both uncovered and
the two new cut edges are both uncovered.  In either case the total number
of uncovered edges is unchanged, proving (3).

For a fixed support `I`, the least possible cost is
`rho_|I|(A,a)+rho_|I|(B,b)`: permuting the three rows shows that the minimum
depends only on `|I|`.  Taking the minimum over the seven proper supports
gives (4).  This also proves the assertion when one or more terms are
infinite.

## Consequences

Let

\[
 K(X,e)=\{k\in\{0,1,2\}:\rho_k(X,e)<\infty\}.
\]

The existence part of Theorem 1 is the exact obstruction

\[
 A(a)*B(b)\text{ has an FR-triple}
 \quad\Longleftrightarrow\quad
 K(A,a)\cap K(B,b)\ne\varnothing.                          \tag{5}
\]

This pinpoints why the existence of an FR-triple in each factor alone does
not presently prove closure under 2-edge sums: their available marker
frequencies still have to intersect.

There is one useful transparent class.  If `B` is 3-edge-colourable, take a
1-factorization `(F_1,F_2,F_3)` with `b in F_1`.  The regular arrays

\[
 (F_2,F_2,F_3),\qquad(F_1,F_2,F_3),\qquad(F_1,F_1,F_2)
\]

give marker frequencies `0,1,2`, respectively.  Therefore

\[
 A(a)*B(b)\text{ has an FR-triple}
 \quad\Longleftrightarrow\quad
 A\text{ has an FR-triple}.                               \tag{6}
\]

If `q=|V(B)|/2`, the same arrays give the quantitative bound

\[
 \widehat{\operatorname{rdf}}(A(a)*B(b))
 \leq\min\{\rho_0(A,a)+q,\ \rho_1(A,a),\ \rho_2(A,a)+q\}. \tag{7}
\]

In particular, a smallest counterexample to the Fan--Raspaud conjecture
cannot have a 2-edge-cut for which either standard shore closure is
3-edge-colourable.  Any surviving 2-cut in such a counterexample must join
two smaller FR-admitting factors whose boundary-frequency sets are disjoint.
This is a precise residual obstruction, not a proof that a smallest
counterexample is cyclically 4-edge-connected; that stronger assertion is
still identified as unknown in the cited primary literature.

## Reproduction

Run, with CPython 3.11 or later and no third-party packages,

```sh
python3 verify.py
```

and compare with [`EXPECTED_OUTPUT.json`](EXPECTED_OUTPUT.json).  The checker
enumerates perfect matchings directly, verifies the matching and regular-array
bijections row by row, checks uncovered-edge additivity for every regular
array, and checks (4) for

- `K4*K4`,
- `Petersen*K4`, and
- `Petersen*Petersen`.

It also rejects deliberately mismatched boundary supports.  These finite
examples audit the definitions and implementation; the universal theorem is
the parity-and-bijection proof above.

## Scope and status

The 2-cut connection and frequency language are standard, and the 2018
papers use compatible gluing inside reductions for stronger frequency
conjectures.  The contribution here is the explicit full-support bijection,
the exact extended-defect convolution (4), and its transparent-lobe
corollary.  A targeted primary-literature search on 2026-09-21 did not locate
this min-plus formula as a stated theorem.  No historical priority claim is
made.  This result neither proves the Fan--Raspaud conjecture nor removes the
case of a 2-cut joining two non-3-edge-colourable factors.

Primary-source details and the search boundary are recorded in
[`SOURCES.md`](SOURCES.md).
