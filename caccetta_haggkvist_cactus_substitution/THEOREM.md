# A cactus-substitution theorem for Caccetta--Haggkvist

## 1. Definitions

All digraphs below are finite and loopless.  A pair of opposite arcs is
allowed inside a module.  A quotient `Q` is an **orientation** of a simple
undirected graph, so its quotient pairs never contain opposite arcs.

For a digraph `D`, write `d_D^+(v)` for the outdegree of `v`,
`delta(D)` for its minimum outdegree, and `g(D)` for its directed girth.  Put
`g(D)=infinity` when `D` is acyclic.

Fix an integer `k>=2`.  Call `D` **k-CH** when

```text
delta(D) >= |D|/k  implies  g(D) <= k.
```

Thus the Caccetta--Haggkvist conjecture says that every finite digraph is
`k-CH` for every `k>=2`.

Let `Q` have vertices `1,...,q`, and let `H_1,...,H_q` be nonempty digraphs
on disjoint vertex sets.  The **substitution**

```text
D = Q[H_1,...,H_q]
```

keeps all internal arcs of every `H_i` and, for every quotient arc `i->j`,
adds every arc from `V(H_i)` to `V(H_j)`.

A directed cycle `C` of `Q` is **out-packing** if every quotient vertex is
the head of at most one arc whose tail lies on `C`:

```text
|N_Q^-(x) intersect V(C)| <= 1             for every x in V(Q).
```

## 2. The abstract out-packing substitution lemma

**Lemma.**  Fix `k>=2`.  Suppose every module `H_i` is `k-CH`.  If `Q` has
at least two vertices, has no sink, and contains an out-packing directed
cycle, then `Q[H_1,...,H_q]` is `k-CH`.

**Proof.**  Put

```text
n_i = |H_i|,
a_i = delta(H_i),
e_i = sum_{i->j in A(Q)} n_j,
N   = sum_i n_i.
```

Every vertex of `H_i` has its internal outdegree plus exactly `e_i` external
outneighbors.  Hence

```text
delta(D) = min_i (a_i+e_i).                 (1)
```

Assume `delta(D)>=N/k` and, for a contradiction, that `D` has no directed
cycle of length at most `k`.  No module has such a cycle.  Since `H_i` is
`k-CH`, the contrapositive gives the strict inequalities

```text
a_i < n_i/k                                (2)
```

for every `i`.

Let `C` be an out-packing directed cycle of `Q`, of length `ell`.  If
`m_C(j)` denotes the number of arcs from `C` to `j`, then the out-packing
condition says `m_C(j)<=1`.  Therefore

```text
sum_{i in C} e_i
  = sum_j m_C(j)n_j
  <= N.                                     (3)
```

Summing (1) over the vertices of `C`, and then using (2) and (3), yields

```text
ell*N/k <= ell*delta(D)
          <= sum_{i in C}(a_i+e_i)
          <  sum_{i in C}n_i/k + N
          <= N/k + N
          =  (k+1)N/k.
```

Thus `ell<k+1`, so `ell<=k`.  Choosing one arbitrary vertex from every
module indexed by `C` lifts `C` to a directed cycle of the same length in
`D`, a contradiction.  This proves the lemma.  `square`

The strict inequality is important.  It comes from applying the `k-CH`
implication inside every module before doing the quotient count.

## 3. Why cactus quotients supply the certificate

An undirected graph is a **cactus forest** if every edge belongs to at most
one simple cycle.  Equivalently, every nontrivial block is an edge or a
cycle.

**Packing-cycle lemma.**  Let `Q` be an orientation of a cactus forest.  If
`Q` has no sink, then it contains an out-packing directed cycle.

**Proof.**  Following outgoing arcs in a finite sinkless digraph eventually
repeats a vertex, so `Q` contains a directed cycle `C`.

A vertex on `C` has exactly one inneighbor on `C`: its predecessor.  A chord
would put a cycle edge in a second undirected cycle, which is impossible in
a cactus.  A vertex outside `C` cannot be adjacent to two distinct vertices
of `C`, since the two incident edges together with either intervening path
on `C` would again create an undirected cycle sharing edges with `C`.
Consequently every vertex has at most one inneighbor on `C`.  `square`

## 4. Main closure theorem

**Theorem.**  Let `Q` be an orientation of a cactus forest and let every
`H_i` be a nonempty `k-CH` digraph.  Then

```text
Q[H_1,...,H_q] is k-CH.
```

**Proof.**  The one-vertex quotient is just its module.  Otherwise suppose
`delta(D)>=N/k` and that no module has a cycle of length at most `k`.  As in
(2), `a_i<n_i/k`.  Equation (1) then gives

```text
e_i >= N/k-a_i > (N-n_i)/k > 0,
```

because `q>=2` and all modules are nonempty.  Thus `Q` has no sink.  The
packing-cycle lemma and the abstract substitution lemma finish the proof.
`square`

**Corollary 1 (full CH closure).**  If every `H_i` satisfies the
Caccetta--Haggkvist conjecture for all `k`, then so does their substitution
over an oriented cactus quotient.

**Corollary 2 (recursive class).**  Start with one-vertex digraphs and
repeatedly substitute already constructed digraphs into oriented cactus
quotients.  Every digraph in the resulting unbounded recursive class
satisfies the Caccetta--Haggkvist conjecture.

These are closure statements, not a bounded-order verification.

## 5. Sharp weighted blow-ups and equality

Take independent modules of positive orders `n_i`; call the resulting
digraph `B`.  If `delta(B)>0`, the quotient has no sink.  For any quotient
directed cycle `C` of length `ell`, the packing count alone gives

```text
ell*delta(B)
  <= sum_{i in C} e_i
  <= |B|.
```

The lifted cycle has length `ell`, and hence

```text
g(B)*delta(B) <= |B|.                       (4)
```

This is slightly stronger than the ceiling form of Caccetta--Haggkvist.

**Equality classification.**  Suppose the underlying cactus quotient is
connected.  Equality holds in (4) if and only if `Q` is a consistently
directed cycle and all module orders are equal.

To prove the nontrivial direction, equality forces equality in the packing
count for a quotient directed cycle `C`.  Since all module orders are
positive, every quotient vertex must receive exactly one arc from `C`.
Every vertex outside `C` therefore has exactly one neighbor on `C`, with the
arc directed from `C` to that vertex.  The graph induced outside `C` is a
forest: an outside cycle, together with its mandatory attachments to `C`,
would violate the cactus condition.  Positive minimum outdegree would then
force every vertex of this finite forest to have an outneighbor within the
forest, which is impossible (following such arcs would create a cycle).
Thus there are no outside vertices and `Q=C`.

If the successive module orders on this directed `ell`-cycle are
`n_1,...,n_ell`, then

```text
delta(B)=min_i n_i,
|B|=sum_i n_i.
```

Equality `ell*min_i n_i=sum_i n_i` holds exactly when all `n_i` are equal.
The converse is immediate.  This supplies a sharp infinite family.

## 6. Boundary of the mechanism

The out-packing-cycle certificate is not automatic for planar quotients.  On
the wheel with rim `0-1-2-3-0` and hub `4`, orient the arcs as

```text
1->0, 0->3, 3->2, 2->1,
0->4, 2->4, 4->1, 4->3.
```

This orientation is strongly connected, but every directed cycle has a
vertex receiving arcs from at least two of its vertices.  The verifier checks
this directly.  This shows why the cactus overlap condition is doing real
work.  It does **not** refute Caccetta--Haggkvist or rule out a different
substitution proof for broader planar or series-parallel quotients.

## 7. Literature and novelty boundary

The general Caccetta--Haggkvist conjecture remains open.  Blow-ups and
iterated blow-ups of directed cycles are standard extremal constructions,
and substitution-stable oriented classes occur in the surrounding
literature.  The nonuniform-degree viewpoint is also established.

The specific fixed-`k` substitution lemma, its cactus closure, and the sharp
nonuniform independent-blow-up equality statement were not located in
targeted searches of the sources below or in searches for Caccetta--Haggkvist
with substitution, lexicographic products, cactus quotients, and modular
blow-ups.  This is search-relative evidence only; no historical-priority
claim is made.

Primary context:

1. L. Caccetta and R. Haggkvist, *On minimal digraphs with given girth*,
   Congressus Numerantium 21 (1978), 181--187.
2. B. D. Sullivan, *A Summary of Problems and Results related to the
   Caccetta--Haggkvist Conjecture*, arXiv:math/0605646.
3. R. Aharoni, E. Berger, M. Chudnovsky, H. Guo, and S. Zerbib,
   *Non-uniform degrees and rainbow versions of the Caccetta--Haggkvist
   conjecture*, SIAM J. Discrete Math. 37 (2023), 1704--1714,
   arXiv:2110.11183.
4. A. Grzesik, *On the Caccetta--Haggkvist Conjecture with a Forbidden
   Transitive Tournament*, Electron. J. Combin. 24(2) (2017), P2.19.
