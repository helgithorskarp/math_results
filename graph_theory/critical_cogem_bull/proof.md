# An exact independent-set obstruction in critical graph classes

All graphs are finite, simple and nonempty, and all forbidden subgraphs are
induced. A graph is **vertex-critical** if deleting any vertex decreases its
chromatic number. The notation `crit_k(F)` refers to k-vertex-critical graphs
avoiding the members of F. A join makes two disjoint graphs complete to each
other. A module is a vertex set seen completely or not at all by every outside
vertex; a prime graph has no nontrivial module.

This is an ordinary, unformalized proof with explicitly cited structural
inputs. The finite checks accompanying it are controls, not the proof of its
unbounded quantifiers. No independent peer review is claimed.

## 1. Main theorem

Let C be a hereditary graph class with the following property:

> Every prime graph in C is perfect or has independence number at most two.

**Theorem 1.** If G is a noncomplete vertex-critical graph in C, and
`a=alpha(G)`, then G contains an induced

\[
P_4+(a-2)P_1.
\]

Consequently, for every integer ell>=0, a vertex-critical graph G in C is
`(P4+ell P1)`-free if and only if `alpha(G)<=ell+1`.

Equivalently, for a noncomplete critical graph in C,

\[
\max_{Q\cong P_4}\alpha\bigl(G[V(G)\setminus (Q\cup N(Q))]\bigr)
=\alpha(G)-2.
\tag{1}
\]

The maximum is over induced four-vertex paths; N(Q) consists of outside
vertices adjacent to at least one vertex of Q. Thus (1) specifies the exact
largest independent set anticomplete to an induced P4.

### Criticality and modules

We use the standard modular decomposition: if G and its complement are
connected, the maximal proper modules partition V(G), and contracting them
gives a prime induced subgraph, its skeleton. See the discussion of Gallai's
decomposition in [BH, Section 3]. We also use the standard replication lemma
for perfect graphs: replacing vertices of a perfect graph by cliques preserves
perfection.

Here are the elementary criticality facts needed with that decomposition.

1. A vertex-critical graph is connected. Otherwise a component of maximum
   chromatic number is a proper induced subgraph with the same chromatic number.
2. Every nonempty module M of a critical graph induces a critical graph. If
   deleting x from M did not decrease chi(G[M]), a coloring of G-x could color
   M using the same set of colors: each outside vertex sees all or none of M.
   This would contradict criticality of G.
3. For modules M_i with `r_i=chi(G[M_i])`, replacing M_i by K_{r_i} preserves
   chromatic number. A coloring amounts to choosing a palette of at least r_i
   colors for each module, with disjoint palettes on adjacent modules.
4. If G is critical, this clique replacement H is also critical. Deleting a
   vertex of M_i decreases its chromatic number by exactly one. The resulting
   palette demand is therefore the same as deleting one vertex from the
   replacement K_{r_i}, so chi(H-v)=chi(G)-1.
5. If a critical graph is a join of graphs, every join factor is critical,
   and chromatic numbers add. Its independence number is the maximum of those
   of the join factors.

In particular, the skeleton of a connected, co-connected, noncomplete critical
graph cannot be perfect. If it were, its clique replacement H would be perfect
and critical, hence a clique: a maximum clique in a perfect critical graph
must contain every vertex. But the skeleton has a nonedge, which survives in
H. This is a contradiction.

### Proof of Theorem 1

Proceed by induction on the number of vertices. A noncomplete critical graph
has independence number a>=2 and contains an induced P4: a P4-free graph is a
cograph, hence perfect, and a perfect critical graph is complete. This proves
the assertion whenever a=2.

Suppose a>=3. If the complement of G is disconnected, write G as a join of its
complement components. Choose a factor J with alpha(J)=a. It is a smaller
noncomplete critical member of C. The induction hypothesis inside J supplies
the required induced subgraph of G.

It remains that G is connected and co-connected. Let M_1,...,M_t be its
maximal proper modules and Q its prime skeleton. The criticality facts above
show that Q is not perfect. By the hypothesis on C, alpha(Q)<=2. Also Q has no
universal vertex, since its complement is connected.

Choose a maximum independent set S of G. It meets at most two modules,
because its occupied modules form an independent set of Q. It cannot meet
only one module M_i: a vertex in a module nonadjacent to M_i could be added
to S. Hence S meets exactly two anticomplete modules M_i and M_j. Put
`a_i=alpha(G[M_i])` and `a_j=alpha(G[M_j])`. Maximality of S gives
`a=a_i+a_j`. Since a>=3, one of these, say a_i, is at least two.

The graph G[M_i] is a smaller noncomplete critical member of C. By induction
it contains `P4+(a_i-2)P1`. Adjoin an independent set of a_j vertices from
M_j. All these vertices are anticomplete to M_i, so the result is
`P4+(a-2)P1`, as required.

For the equivalence, an induced `P4+ell P1` contains an independent set of
size ell+2. Conversely, if alpha(G)>=ell+2, the theorem supplies that induced
subgraph, after discarding excess isolated vertices. Complete graphs satisfy
the equivalence as well. Finally any independent set anticomplete to a P4
can be joined to an independent pair of the P4, proving the upper bound in
(1); the theorem supplies equality. **QED.**

## 2. Applications to bull and banner restrictions

The bull is the triangle abc with pendant edges ax and by. The banner is a
four-cycle with one pendant vertex. Their complements are respectively the
bull and the hammer. The house is the complement of P5.

The published structural results of Karthick, Maffray and Pastor [KMP] give:

- Theorem 5.2: a prime (house,bull)-free graph is triangle-free or
  (P5,C5)-free.
- Theorem 4.2: a prime (house,hammer)-free graph is triangle-free or perfect.

Complementation gives the hypothesis of Theorem 1 for both (P5,bull)-free and
(P5,banner)-free graphs. For the first statement, a graph avoiding house, P5
and C5 is perfect: every odd hole of length at least seven contains P5, and
every odd antihole of length at least seven contains house; length five is
excluded. Apply the Strong Perfect Graph Theorem [SPGT]. For the second
statement perfection is invariant under complementation, and a triangle-free
complement means independence number at most two.

Alternatively, the newer [BH, Corollary 2.8] states the stronger prime
(P5,bull)-free dichotomy into bipartite graphs and graphs of independence
number at most two. The proof here needs only the published weaker input
from [KMP], not the new preprint's finiteness theorem.

**Corollary 2.** For H equal to bull or banner, and all k>=1 and ell>=0,

\[
\operatorname{crit}_k(P_5,H,P_4+\ell P_1)
=\operatorname{crit}_k(P_5,H,(\ell+2)P_1).
\tag{2}
\]

Every graph in these classes satisfies

\[
\alpha(G)\le\ell+1,\qquad
|V(G)|\le(\ell+1)(k-1)+1.
\tag{3}
\]

The order bound follows by coloring G-v with k-1 colors, each of which
contains at most ell+1 vertices. For k=1 the graph is K1. No optimality of
the order bound for general ell is claimed.

This gives an explicit linear bound in k and the exact forbidden-independent-
set characterization, rather than only finiteness. For the bull family,
[BC26, Corollary 3] previously establishes finiteness throughout the same
two-parameter range. The proof of (2) is the new deduction recorded here;
the structural inputs and the previous finiteness result are prior work.

The banner instance is only an illustration of the general theorem, not a
claimed improvement: [BGS, Theorem 3(i)] already proves the stronger statement
that every critical (P5,banner)-free graph has independence number at most two.
Our new quantitative application and sharpness claim concern the bull family.

## 3. Consequence for the selected co-gem problem

The co-gem is `P4+P1`. Both P5 and the bull have an independent triple.
Therefore (2) at ell=1 says

\[
\operatorname{crit}_k(P_5,\mathrm{bull},\mathrm{co\text{-}gem})
=\operatorname{crit}_k(3P_1)
=\operatorname{crit}_k(P_3+P_1).
\tag{4}
\]

The second equality is the known result of [CHS, Theorem 3.1]: a critical
`P3+P1`-free graph has independence number at most two. The reverse inclusion
is immediate. Thus (4) holds for every k and every order, and its graphs have
at most 2k-1 vertices. In particular, the **P5-free portion** of the seven-
critical co-gem/bull class is exactly the known D-free class on at most 13
vertices. Its prior census is not repeated here.

The campaign target remains

\[
\operatorname{crit}_k(\mathrm{co\text{-}gem},\mathrm{bull})
\stackrel{?}{=}\operatorname{crit}_k(P_3+P_1)\quad\text{for all }k.
\tag{T}
\]

Equation (4) proves an additional bridge: **(T) is equivalent to excluding
P5 from every critical co-gem/bull-free graph.** One direction uses (4);
the other uses the independent triple in P5 and the known D-free critical
characterization. This does not prove that P5-exclusion statement. No order
cap, including 13 at k=7, is established for a P5-containing candidate.

## 4. Sharpness of the independence bound

For every integer a>=1 there exists a vertex-critical (P5,bull)-free graph
T_a with alpha(T_a)=a. The following recursion supplies exact examples,
showing that `ell+1` in (3) cannot be decreased uniformly over k.

Let T_1=K1. Given T_a with chromatic number t, let epsilon be zero if t is
odd and one otherwise, and put `J=T_a join K_epsilon` and `r=t+epsilon`.
Here K_0 means that no vertex is added. Thus r is odd, J is r-critical, and
alpha(J)=a. In a five-cycle, replace vertex 0 by J and each of vertices
1,2,3,4 by K_r. Call the result T_{a+1}. Then

\[
\chi(T_{a+1})=(5r+1)/2,\quad
\alpha(T_{a+1})=a+1,\quad
|V(T_{a+1})|=|V(T_a)|+\epsilon+4r.
\tag{5}
\]

To verify criticality without relying on a weighted-coloring formula, write
`r=2s+1`. A color can occur in at most two of the five modules, so their total
palette demand 5r requires at least `(5r+1)/2` colors. After deletion of one
vertex, rotate the cycle labels so that module 0 has demand r-1 and the other
four modules have demand r. For each independent pair `{i,i+2}` modulo five,
allocate the following numbers of separate colors, in the order i=0,...,4:

\[
(s,\ s+1,\ s+1,\ s,\ s).
\]

These pair palettes meet demands `(r-1,r,r,r,r)` exactly, using `(5r-1)/2`
colors. Each module has a coloring with its assigned palette because its
constituent graph is critical. Adding back the deleted vertex in a fresh
color colors the full graph with `(5r+1)/2` colors. Every deletion lowers the
chromatic number, establishing (5). A maximum independent set consists of a
maximum independent set in J and one vertex from a nonadjacent clique module;
all other possibilities have size at most two.

P5 and the bull are prime, so substitution preserves avoidance of each: an
induced copy crossing substitution modules would have a nontrivial module
unless it used at most one vertex per module; in the latter case the copy
would already occur in the skeleton. Joins also preserve avoidance, since
the complements of both forbidden graphs are connected. Induction therefore
proves the required avoidance for all T_a.

For ell>=0, take T_{ell+1}. Its independence number is ell+1, so it cannot
contain `P4+ell P1`, which has independence number ell+2. The bound in (3) on
independence number is attained. This construction is used to certify
sharpness of the new bound; no priority is claimed for the general operation
of substituting critical graphs into a five-cycle.

## References

- [KMP] T. Karthick, F. Maffray and L. Pastor, *Polynomial Cases for the Vertex
  Coloring Problem*, Algorithmica 81 (2019), 1053–1074, Theorems 4.2 and 5.2.
  [Author manuscript v2](https://arxiv.org/pdf/1709.07712v2),
  [journal](https://doi.org/10.1007/s00453-018-0457-y).
- [BH] M. Belavadi and C. T. Hoàng, *Structural description of (bull,
  house)-free graphs*, 2026 preprint, Corollary 2.8 and Section 3.
  [Full manuscript](https://arxiv.org/html/2604.27594v1).
- [BC26] I. Beaton and B. Cameron, *Vertex-critical graphs in subfamilies of
  (P4+ell P1)-free graphs*, 2026 preprint, Corollary 3.
  [Full manuscript](https://arxiv.org/html/2604.06999v1).
- [CHS] B. Cameron, C. T. Hoàng and J. Sawada, *Dichotomizing k-vertex-critical
  H-free graphs for H of order four*, Discrete Applied Mathematics 312 (2022),
  106–115. [Author PDF](https://www.cis.uoguelph.ca/~sawada/papers/kcritical.pdf).
- [SPGT] M. Chudnovsky, N. Robertson, P. Seymour and R. Thomas, *The strong
  perfect graph theorem*, Annals of Mathematics 164 (2006), 51–229.
  [Journal](https://doi.org/10.4007/annals.2006.164.51).
- [BGS] C. Brause, M. Geißer and I. Schiermeyer, *Homogeneous sets,
  clique-separators, critical graphs, and optimal chi-binding functions*,
  Discrete Applied Mathematics 320 (2022), 211–222.
  [Author manuscript v3](https://arxiv.org/pdf/2005.02250v3).
