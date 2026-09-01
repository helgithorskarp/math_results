# A product-lift lemma and Hamming-invariant optimum of 432 edges in Q8

## Result

**Product-lift lemma.** Let $G\subseteq Q_d$ be square-saturated, and let
$D\subseteq V(Q_d)$ be an independent dominating set of $G$.  In two copies of
$Q_d$, place one copy of $G$ in each layer, and include the vertical matching
edge above $v$ exactly when $v\in D$.  The resulting subgraph
$L(G,D)\subseteq Q_{d+1}$ is square-saturated and

$$
|E(L(G,D))|=2|E(G)|+|D|.
$$

Applying this lemma to the Hamming-invariant 208-edge construction in $Q_7$
and a 16-vertex Hamming coset gives

$$
\boxed{\operatorname{sat}(Q_8,Q_2)\leq432}.
$$

**Restricted optimality theorem (proof-producing computation).** The
construction is invariant under translation by the binary $[7,4,3]$ Hamming
code $H$ embedded as $H\times\{0\}$ in $Q_8$.  Every square-saturated subgraph
with this invariance has at least 432 edges.  Thus 432 is exact in this
invariant class.  No unrestricted lower bound of 432 is claimed.

## Proof of the lift lemma

Identify $Q_{d+1}$ with two horizontal copies of $Q_d$.  A square lying within
one layer is not completed because $G$ is square-free.  A square using the new
coordinate is based on an edge $uv$ of $Q_d$.  If $uv\notin E(G)$ then its two
horizontal edges are absent.  If $uv\in E(G)$ then independence of $D$ says
that at most one of the two vertical edges above $u,v$ is present.  Hence no
square is present in $L(G,D)$.

An omitted horizontal edge is saturated inside its own layer because the copy
of $G$ there is saturated.  An omitted vertical edge above $v\notin D$ is also
saturated: domination supplies a vertex $u\in D$ with $uv\in E(G)$.  The two
horizontal copies of $uv$ and the vertical edge above $u$ are already present,
so adding the vertical edge above $v$ completes their square.  This proves the
lemma.

## The 432-edge instance

For $x\in\mathbb F_2^7$, write

$$
\sigma(x)=\bigoplus_{i:x_i=1}(i+1)\in\mathbb F_2^3,
\qquad H=\ker\sigma.
$$

Use the canonical 13-edge quotient from the companion classification package:

$$
\begin{aligned}
\{&07,16,17,25,27,34,35,36,37,47,56,57,67\}.
\end{aligned}
$$

Here $st$ denotes the edge $\{s,t\}$ of the syndrome $K_8$.  Lifting each edge
to its free $H$-translation orbit gives the 208-edge square-saturated $G$ in
$Q_7$.

Vertex 7 is universal in the quotient, so

$$
D=\sigma^{-1}(7)
$$

is an independent dominating set in $G$.  It has 16 vertices.  Indeed, each
vertex outside $D$ has exactly one selected edge into $D$, in the coordinate
labelled by $\sigma(x)+7$.  The product lift therefore contains

$$
2\cdot208+16=432
$$

edges.

## Restricted lower bound

Translation by $H\times\{0\}$ acts freely on the edges and squares of $Q_8$.
Its quotient has 16 vertices arranged as two syndrome copies of $K_8$ joined
by a perfect matching.  It has 64 edge-orbits and 112 square-orbits: 42 affine
4-cycles in each $K_8$ layer and 28 cycles using a matching pair.  An invariant
subgraph is therefore specified by 64 Boolean edge-orbit variables.

The proof-producing encoder imposes square-freeness, saturation, and at most 26
selected edge-orbits.  There are two edge types under the quotient symmetry:
horizontal and vertical.  Every nonempty invariant subgraph has an edge of at
least one type.  Quotient translations, the layer flip, and
$\operatorname{GL}(3,2)$ send a selected horizontal edge to $\{0,1\}$ or a
selected vertical edge to $\{0,8\}$.  It is therefore enough to refute the two
CNFs obtained by fixing these representative edges.

Each CNF has 2,150 variables and 4,809 clauses, including a transparent Sinz
counter.  CaDiCaL 2.1.2 returned `UNSATISFIABLE` in both cases and emitted
textual DRAT proofs.  `drat-trim` at source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` independently returned
`s VERIFIED` for both.  Hence 26 edge-orbits are impossible.  Since every
orbit has 16 edges, the lower bound is $27\cdot16=432$.
As a boundary sanity check, the same encoder at bound 27 is satisfiable in both
fixed-edge cases, and both decoded 27-orbit models pass a direct quotient check.

## Reproduction

The checker uses only Python 3.11 or later:

```bash
python3 verify_q8_432.py

python3 generate_q8_hamming_quotient_cnf.py \
  /scratch/q8-hx0-bound26-horizontal.cnf --fixed-type horizontal
python3 generate_q8_hamming_quotient_cnf.py \
  /scratch/q8-hx0-bound26-vertical.cnf --fixed-type vertical

cadical --no-binary \
  /scratch/q8-hx0-bound26-horizontal.cnf \
  /scratch/q8-hx0-bound26-horizontal.drat
cadical --no-binary \
  /scratch/q8-hx0-bound26-vertical.cnf \
  /scratch/q8-hx0-bound26-vertical.drat

drat-trim \
  /scratch/q8-hx0-bound26-horizontal.cnf \
  /scratch/q8-hx0-bound26-horizontal.drat
drat-trim \
  /scratch/q8-hx0-bound26-vertical.cnf \
  /scratch/q8-hx0-bound26-vertical.drat
```

It independently reconstructs the base quotient, expands the Hamming orbits,
checks that $D$ is independent and dominating, then enumerates all 1,024 edges
and 1,792 square faces of $Q_8$.  It verifies that no square is present and that
each of the 592 omitted edges has a three-edge witness.  The recorded output is:

```text
base_selected_edges: 208
dominating_coset_size: 16
lift_selected_edges: 432
lift_omitted_edges_with_witness: 592
lift_square_faces: 1792
status: VERIFIED
```

## Hashes and trust boundary

```text
verify_q8_432.py:
  0a5df713cd6618fa08a40040f3c4639c1f26b6110316ccdd0235ea5d9b5d0df4
q8_hamming_layer_lift_432.json:
  3d72ec9a335aec32c2bedfeb7f309a215ffd252582fae0f6fcd73189127ea87f
generate_q8_hamming_quotient_cnf.py:
  e329a58af2d0af2bc69ae4feca50e1a12095d44d13c348a91865c5afdcd1d32b
canonical expanded Q8 edge list:
  5981061ef0a5d3f27b12765977fcaf97b4be78ab7408b4f837a44056ea5d24a0
horizontal-fixed bound-26 CNF (under /scratch):
  7f12fedb7785d8f73ef9f8344893155ee21169c2c3f271c3e6ab966f23672092
horizontal-fixed DRAT (under /scratch, not committed):
  5527e2f4c1630c29092108d679f26346f48b1263a4da1224c5717406cf13a1be
vertical-fixed bound-26 CNF (under /scratch):
  cf7763d6ef45767052ae77dd022ad9b1c8a77f279a7213ba99d4b449fdde4319
vertical-fixed DRAT (under /scratch, not committed):
  fbe5de488dc38824280189ed50ad798dc1b5b671386430fda97ce3512de6afbb
```

- The product-lift lemma is a direct mathematical proof.
- The specific upper bound depends on finite expansion of the 13 quotient
  edges; the standalone checker verifies this from the definition.
- The restricted lower bound trusts the source-auditable quotient-to-CNF
  bridge.  The DRAT checks establish unsatisfiability of the generated CNFs;
  they do not independently formalize that mathematical bridge.
- CNFs, solver logs, and DRAT proofs remain under `/scratch` and are not committed.
- No Lean formalization and no unrestricted optimality claim are made.

## Literature and novelty assessment

The searched primary sources establish asymptotic $O(2^d)$ bounds and use
Hamming codes, but they do not state this independent-dominating product lift or
the 432-edge $Q_8$ construction:

- J. R. Johnson and T. Pinto, “Saturated Subgraphs of the Hypercube,”
  *Combinatorics, Probability and Computing* 26 (2017), 52–67.
  <https://arxiv.org/abs/1406.1766>
- N. Morrison, J. A. Noel, and A. Scott, “Saturation in the Hypercube and
  Bootstrap Percolation,” *Combinatorics, Probability and Computing* 26 (2017),
  78–98. <https://arxiv.org/abs/1408.5488>
- S.-Y. Choi and P. Guan, “Minimum critical squarefree subgraph of a hypercube,”
  *Congressus Numerantium* 189 (2008), 57–64.
  <https://combinatorialpress.com/cn/vol189/>

Concept and exact-phrase searches on 2026-09-01 found no published value or
upper bound specifically for $\operatorname{sat}(Q_8,Q_2)$ and no 432-edge
construction.  The lemma and bound are therefore apparently new to the searched
sources, not a priority claim.
