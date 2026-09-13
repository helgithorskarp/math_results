# Exact width obstruction for the literal Ramsey encoding

The result concerns graphs of constraints, not the existence of Ramsey
graphs. It rules out the proposed small-separator premise for one exact
decision architecture. It gives no Ramsey exclusion and no lower bound on
the running time of arbitrary SAT, symbolic, or mathematical algorithms.

## 1. An exact incidence subdivision criterion

For `n>=5`, let `E` be all unordered pairs of `[n]`. The one-color
Ramsey incidence graph has one variable vertex for each `e in E`, and
one clause vertex for each five-subset `S`. Join `e` to `S` when `e` is
contained in `S`. Thus the clause forbids all ten edges of `S` being red.

**Theorem 1.** There is a subdivision of `K_(binom(n,2))` in this incidence
graph, with the edge variables as branch vertices and each subdivided
edge having length two, if and only if `n>=23`.

An edge of the desired subdivided clique corresponds to an unordered pair
of different physical edges `e,f`. Assign to each such pair a *different*
five-set containing `e union f`. This is a bipartite matching problem.
If the physical edges meet, their union has size three and has
`binom(n-3,2)` extensions to a five-set. If they are disjoint, it has
`n-4` extensions.

Give each pair total fractional weight one, distributed equally among
these extensions. A five-set contains 30 meeting pairs and 15 disjoint
pairs of its ten edges. Its total received weight is exactly

```
lambda(n) = 30/binom(n-3,2) + 15/(n-4)
          = 15(n+1)/((n-3)(n-4)).
```

For `n=23+t`, the denominator minus the numerator is
`t^2+24t+20`, so `lambda(n)<1` for all `n>=23`. For any set `X` of left
vertices, its total weight is `|X|`, all received by its neighboring
right vertices, each receiving at most one. Hence `|N(X)|>=|X|`.
Hall's condition gives the required injection. Equivalently, a maximum
matching that missed a left vertex would have an alternating reachable
set `X` with `|N(X)|=|X|-1`, contradicting the weight inequality. This
also proves termination of the augmenting-path construction used here.

Conversely, for `5<=n<=22` there are fewer available clause vertices than
required internal subdivision vertices:

```
binom(n,5) / binom(binom(n,2),2)
  = (n-3)(n-4)/(15(n+1)) < 1.
```

The inequality follows from `n(n-22)-3<0`. Thus the stated length-two
subdivision, using *all* edge variables as branch vertices, is impossible
there. No claim about other clique minors at these smaller orders is made.

At `n=43`, `lambda=11/26`. Deleting any subset of the variable vertices
preserves the injection restricted to the remaining pairs. In particular,
the theorem applies to the 860 edges outside a fixed Hamilton cycle.

## 2. Application to the complete Hamilton-normalized receiver

R3's source-published Hamiltonicity theorem gives a red Hamilton cycle in
every good43. Its inputs are the independently accepted complete-class
connectivity theorem and the classical Chvatal--Erdos theorem. Relabel the
cycle as `0,1,...,42,0`. Only those 43 edges are fixed red; all 860 chords
are independent physical variables. This is an existence-preserving
normalization, without any graph automorphism assumption.

Every red five-clique prohibition remains after this substitution. Its
scope consists of all noncycle pairs in its five-set. Every vertex of a
five-set has at most two incident cycle edges and therefore at least two
incident free edges in this scope. Consequently the scope determines the
entire five-set. Different five-sets give different clauses, and none of
these red clauses subsumes another: scope containment would imply
five-set containment and hence equality. The subdivision is therefore
present even after duplicate-clause and subsumption removal of these
literal red clauses.

**Theorem 2.** The primal and variable--clause incidence graphs of the
literal Hamilton-normalized physical formula both have treewidth exactly
859. This already holds for its red-clique prohibitions alone.

Any two free edges belong to a five-set, so the primal graph is `K_860`.
For the incidence lower bound, Theorem 1 supplies a subdivision of
`K_860`. Contracting its internal vertices gives that clique as a minor,
so the treewidth is at least 859. The explicit computation below supplies
the entire subdivision rather than only invoking matching existence.

For completeness, treewidth does not increase under taking a minor:
deletion removes labels from bags; contraction replaces the two endpoint
labels by one, and their bag subtrees intersect in a bag containing the
contracted edge. A clique of size 860 requires a bag of size 860 because
its vertex subtrees pairwise intersect, and connected subtrees of a tree
have the Helly property. These facts give the lower bound directly.

For the upper bound, use a central bag containing all 860 variable
vertices. For each clause, attach a leaf bag consisting of that clause
vertex and its scope of at most ten variables. Every graph edge is covered
and each vertex's bags form a connected subtree. The maximum bag size is
860. This works for both colors together, proving the exact upper bound.

The unnormalized literal formula similarly has primal and incidence
treewidth 902, using all 903 physical edges. This follows from the same
proof; no second large matching computation is required.

## 3. Local clause factorization cannot remove this graph obstruction

Consider replacing each clause vertex by a connected gadget, with
disjoint internal vertices for different clauses, retaining a connection
from every original incident variable to that gadget. Contract every
gadget to one vertex. The original incidence graph is a minor of the
new graph. Therefore its treewidth is still at least 859.

This statement includes local tree factorizations and fresh auxiliary
variables assigned separately to each clause, when their graph has the
stated contraction property. It does not include arbitrary reformulations
using shared auxiliary structure, semantic simplification, or learned
global relations. No equivalence between those wider classes of methods
and this gadget model is asserted.

## 4. Exact vertex-cut width of the free-edge host

A different proposed separator was a cut in the physical vertex set,
recording every crossing free edge. Its host graph is `K_43 - C_43`.

**Theorem 3.** This host has cutwidth exactly 420.

Every vertex ordering has a prefix of 21 vertices. Across that cut there
are `21*22` pairs, at most 42 of which are cycle edges, since every vertex
on the smaller side has cycle degree two. There are at least 420 free
crossing edges.

Order the vertices as `0,2,...,42,1,3,...,41`. For prefix size `a<=21`,
the prefix is independent in the fixed cycle, and there are exactly
`a(43-a)-2a=a(41-a)` free crossing edges. For `a>=22`, the remaining
`b=43-a<=21` vertices are independent in that cycle, giving `b(41-b)`.
Both expressions are at most 420, attaining 420 at sizes 20 and 21.
This proves the matching upper bound for every cut in that ordering.

This is a statement about a scheme explicitly retaining crossing edge
bits. It does not say that all `2^420` boundary assignments are feasible,
distinct modulo semantic equivalence, or necessary in every algorithm.

## 5. Exact certificate and validation

The certificate gives one five-set bitmask for each of the 369,370
unordered pairs of 860 free physical edges, in lexicographic pair order.
The producer uses a deterministic augmenting-path algorithm. The checker
imports no producer, Ramsey generator, or matching library. It verifies
that every record is a five-set on `[43]`, contains both free edges, and
is different from every other chosen five-set. Thus every required path
exists and all internal clause vertices are distinct.

The checker also counts the fractional Hall load at all 962,598 red
five-sets, checks its exact maximum `11/26` and total 369,370, and
reconstructs the full red-clause width histogram. It checks all 42 cuts
of the explicit optimal vertex ordering. All operations use integers
or exact rational numbers.

There is an essential scope control: setting every chord blue satisfies
the red-only formula, despite its width 859. The resulting fixed cycle
violates the full Ramsey formula on the blue five-set `{0,2,4,6,8}`.
Thus even the exact width theorem is not a satisfiability obstruction or
a general running-time lower bound. It refutes the proposed small-width
premise, not the existence of a good43.

## 6. Decision consequence and failed final gate

A dense primal elimination scheme organized solely by syntactic scopes
faces 859 remaining bits in its first output scope, or `2^859` table
entries. Static separator conditioning to reduce that complete interaction
graph to width at most `w` requires deleting at least `859-w` variables.
This is graph deletion accounting only: value-dependent simplification
can change the scopes, so it is not a lower bound on actual search.

Neither the incidence representation, local clause gadgets, nor the
literal vertex-cut layout provides the required small interfaces. A
successful continuation would require new semantic compression or a
different mathematical theorem with a demonstrated terminal consequence.
No such finishable global residual was established in this pass. All 431
preserved maximum-codegree cases remain unresolved. The final contracted
endpoint gate is missed, and this slot should be reassigned within R(5,5).
