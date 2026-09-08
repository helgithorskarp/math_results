# No punctured Cayley graph of order 44 is good

Write red for an edge and blue for a nonedge. A graph is **good** when neither
color contains a complete graph on five vertices.

## 1. Puncturing a Cayley graph cannot remove every obstruction

Let `X=Cay(G,S)` be an undirected Cayley graph: `1` is not in `S`, and `S` is
closed under inversion. Suppose a five-set `F` is monochromatic in `X`, and
fix a vertex `v`. Left translation acts regularly on the vertices and
preserves both colors. Among the `|G|` translates `gF`, exactly five contain
`v`: for each `f` in `F` there is one `g` with `gf=v`. Hence, when `|G|=44`,
there are 39 translations of `F` avoiding `v`.

It follows that if `X-v` is good, then `X` itself is good. Conversely, a good
`X` plainly has a good puncture. Therefore deciding all good Cayley graphs of
order 44 decides the entire one-vertex-puncture family.

## 2. The four groups of order 44

Let `G` have order `44=4*11`. Its number of Sylow 11-subgroups divides four
and is congruent to one modulo eleven, so the subgroup `N` of order 11 is
unique and normal. Let `P` be a Sylow 2-subgroup. Then `N` intersects `P`
trivially and `NP` has order 44, so

```text
G = C11 semidirect P,       P = C4 or V4.
```

Conjugation maps `P` to `Aut(C11)=C10`. Its image has order one or two. For
`P=C4`, this gives the trivial action or the action in which a generator acts
by inversion. For `P=V4`, a nontrivial action has a kernel of order two; all
three such kernels are equivalent under `Aut(V4)`. Thus the four isomorphism
types are

```text
C11 x C4,
C11 x V4,
C11 semidirect C4       (the action factors through inversion),
C11 semidirect V4       (one V4 generator acts by inversion).
```

The producer and independent auditor build all four multiplication tables.
The auditor checks associativity on every ordered triple, both identity laws,
and the unique two-sided inverse of every element.

## 3. Exact inverse-orbit formulas

For a fixed group, partition its 43 nonidentity elements into orbits under
inversion. Assign one Boolean variable `x_i` to each orbit, true precisely
when that orbit belongs to `S`. This parametrizes every simple undirected
Cayley graph exactly once as a labeled connection set. The four variable
counts are 22, 23, 22, and 33.

It is enough to inspect five-sets containing the identity. For every

```text
F = {1,a,b,c,d},
```

collect the variables belonging to the ten differences `u^-1 v`, with
duplicates removed. If this set of variables is `I(F)`, then the two clauses

```text
OR over i in I(F) of not x_i,
OR over i in I(F) of     x_i
```

forbid respectively a red and blue copy on `F`. Every monochromatic
five-set translates to one containing the identity, so these clauses are
necessary and sufficient. The generator processes all
`binom(43,4)=123,410` rooted sets and removes duplicate clauses.

The independent auditor uses separately written group operations, checks the
complete group tables, reconstructs all rooted physical events, and compares
the exact clause sets. Formula order and literal order are irrelevant.

## 4. Compact physical cores and exhaustive decision

The complete formulas have the following sizes:

| group | variables | distinct clauses | core clauses |
|---|---:|---:|---:|
| `C11 x C4` | 22 | 22,462 | 1,118 |
| `C11 x V4` | 23 | 21,222 | 1,179 |
| `C11 semidirect C4` | 22 | 20,342 | 1,148 |
| `C11 semidirect V4` | 33 | 46,412 | 12,409 |

Each committed core is a subset of its exact physical formula. The auditor
checks this clause by clause after canonicalizing literal order. Consequently,
UNSAT of a core implies UNSAT of the corresponding complete formula.

`dpll_check.py` is a separate exact decision procedure. At a state it first
applies forced unit literals. A falsified clause closes the state. Otherwise
it chooses an unassigned variable and recursively checks both truth values.
Each branch assigns a new variable, so recursion terminates after at most the
number of variables. If both children are UNSAT, their union covers every
completion of the parent. Induction on the number of unassigned variables
therefore proves the returned UNSAT result.

The four cores are all UNSAT. Hence no Cayley graph of order 44 is good, and
the puncture lemma excludes every 43-vertex member of the declared family.

## Scope

This proof classifies connection sets, not all vertex-transitive graphs or
all structured graphs on 43 vertices. It gives no forcing theorem placing a
hypothetical good43 in this family. The h3931/h3935 hereditary result and the
subsequent `C5[C5]` extension obstruction are contextual and are not premises.
No good43 graph or Ramsey-bound improvement is claimed.
