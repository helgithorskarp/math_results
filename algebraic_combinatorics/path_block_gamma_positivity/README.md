# Gamma-positivity of path block polytopes

## Result

Let \(H=(X\sqcup Y,E)\) be a finite bipartite graph without isolated
vertices.  For \(a\geq 1\), let \(H[K_a]\) denote its uniform clique
blow-up: every vertex \(u\) is replaced by a clique
\(B_u=\{b_{u,1},\ldots,b_{u,a}\}\), and the two cliques over the endpoints
of every edge of \(H\) are joined completely.

**Theorem.** The stable-set polytope of \(H[K_a]\) has a
γ-nonnegative Ehrhart \(h^*\)-polynomial.  Its degree is

\[
 a\bigl(|V(H)|-2\bigr).
\]

In particular, the path block polytopes
\(\mathcal P_m^{(a)}\) of Jiang--Yang--Zhong have

\[
h_{m,a}^*(z)
=\sum_{j=0}^{\lfloor a(m-2)/2\rfloor}
  \gamma_j z^j(1+z)^{a(m-2)-2j},
\qquad \gamma_j\geq0,
\]

for all \(m\geq2\) and \(a\geq1\).  This answers Problem 1 in their
paper.  The same conclusion holds for their even cyclic block
polytopes (for even \(m\geq4\)).

There is also a direct descent interpretation.  The construction below
gives a graded poset \(P_a(H)\).  For any natural labeling ω, if a linear
extension is read as its word of ω-labels, then

\[
h^*_{\operatorname{STAB}(H[K_a])}(z)
=\sum_{\pi\in\mathcal L(P_a(H))}z^{\operatorname{des}(\pi)}.
\tag{1}
\]

Thus, for paths, (1) supplies a concrete descent interpretation on
canonically ordered color-labeled block vertices, in the direction of
Problem 2 of the same paper.

## Proof

Make every block \(B_u\) a chain

\[
b_{u,1}<b_{u,2}<\cdots<b_{u,a}.
\]

For each edge \(xy\in E\), where \(x\in X\) and \(y\in Y\), put every
element of \(B_x\) below every element of \(B_y\).  Call the resulting
poset \(P_a(H)\).  There are no further cross-block comparabilities:
cross-block arrows always go from an \(X\)-block to a \(Y\)-block, so a
directed chain cannot pass through a \(Y\)-block into another block.
Consequently, the comparability graph of \(P_a(H)\) is exactly
\(H[K_a]\).

The only cross-block cover relations are
\(b_{x,a}\lessdot b_{y,1}\) for \(xy\in E\).  A rank function is

\[
\rho(b_{u,j})=
\begin{cases}
j-1,&u\in X,\\
a+j-1,&u\in Y.
\end{cases}
\]

Because \(H\) has no isolated vertices, every maximal chain consists
of all \(a\) elements of one \(X\)-block followed by all \(a\) elements
of an adjacent \(Y\)-block.  Hence \(P_a(H)\) is graded of rank
\(2a-1\).

Stable sets in a comparability graph are precisely antichains.  It
follows from Stanley's vertex description of a chain polytope that

\[
\operatorname{STAB}(H[K_a])=\mathcal C(P_a(H)).
\tag{2}
\]

Stanley's transfer map gives identical Ehrhart polynomials, and hence
identical \(h^*\)-polynomials, for the chain and order polytopes of a
poset:

\[
h^*_{\mathcal C(P_a(H))}(z)=h^*_{\mathcal O(P_a(H))}(z).
\tag{3}
\]

Brändén's theorem says that the order polytope of every graded poset
has a γ-nonnegative \(h^*\)-polynomial.  Applying it to \(P_a(H)\) and
using (2)--(3) proves γ-nonnegativity.  The standard degree formula
for a graded-poset order polytope gives

\[
|P_a(H)|-\operatorname{rank}(P_a(H))-1
=a|V(H)|-(2a-1)-1
=a(|V(H)|-2).
\]

Finally, Stanley's linear-extension formula for the \(h^*\)-polynomial
of an order polytope, together with (2)--(3), gives (1).

For \(H=P_m\), the graph \(H[K_a]\) is the graph
\(G_m^{(a)}\) used by Jiang--Yang--Zhong, and their paper identifies
\(\mathcal P_m^{(a)}=\operatorname{STAB}(G_m^{(a)})\).  This proves the
path corollary.  Taking \(H=C_m\) with \(m\) even proves the even-cycle
corollary.  □

## Exact checks

The accompanying standard-library Python program performs three
definition-level checks.

1. It reconstructs all eight path \(h^*\)-polynomials tabulated by
   Jiang--Yang--Zhong from exact lattice-point counts.
2. It independently enumerates linear extensions of \(P_a(H)\) by an
   ideal-state recurrence, records descents, and compares (1) entry by
   entry with the Ehrhart numerator.  The checks cover paths, even
   cycles, \(K_{1,3}\), its \(K_2\)-blow-up, and \(K_{2,3}\).
3. It converts path and even-cycle \(h^*\)-polynomials to the γ-basis
   over a wider finite parameter sweep and checks every coefficient is
   nonnegative.

From the repository root, run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  algebraic_combinatorics/path_block_gamma_positivity/verify.py
```

The implementation uses exact arbitrary-precision Python integers,
has no dependencies outside the standard library, and uses no floating
point, randomness, solver, or generated input.  The computation is a
finite audit of the structural identifications; the universal theorem
rests on the proof above.

With Python 3.11.2, the run ends with

    path (m=5, a=2): h*=[1, 32, 203, 368, 203, 32, 1] gamma=[1, 26, 84, 24]
    path (m=4, a=3): h*=[1, 27, 162, 282, 162, 27, 1] gamma=[1, 21, 63, 10]
    all exact checks passed

The complete standard output has SHA-256
1f85fb2b8b6dd122533f12efc1770cf3f8aadbb9e1463035bb35c23caabc2114;
the verifier source has SHA-256
2def05130ccc924ffd002c22c53be4e3cf6ce56e41c517b64acc38f6f1546694.
The output log is deliberately kept outside the repository.

## Sources and novelty scope

- X. Jiang, S. Yang, and Y. Zhong, *Transfer Matrices and Ehrhart Theory
  for Path and Cyclic Block Polytopes* (2026), especially Theorem 1.3
  and Problems 1--2. <https://arxiv.org/abs/2607.22008>
- R. P. Stanley, *Two poset polytopes*, Discrete & Computational
  Geometry **1** (1986), 9--23. <https://doi.org/10.1007/BF02187680>
- P. Brändén, *Sign-graded posets, unimodality of W-polynomials and
  the Charney--Davis conjecture*, Electronic Journal of Combinatorics
  **11** (2004), R9, especially Theorem 4.2.
  <https://arxiv.org/abs/math/0406019>
- A. D'Alì and A. Higashitani, *Order polytopes of graded posets are
  gamma-effective* (2025), which restates Brändén's theorem and proves
  an equivariant strengthening. <https://arxiv.org/abs/2505.07623>

The proof is an application of established chain/order-polytope and
graded-poset theorems.  Targeted searches for the path block polytope,
its open γ-positivity problem, clique blow-ups of bipartite graphs, and
the graded-poset bridge found no prior statement of this application or
of the bipartite blow-up theorem.  This is a search-relative novelty
assessment, not a historical priority claim.
