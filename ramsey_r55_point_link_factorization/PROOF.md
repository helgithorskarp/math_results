# Proof of the unrestricted point-link factorization

Color an edge red when its bit is one and blue when its bit is zero.  A
`good43` is a red/blue coloring of the edges of `K_43` with no monochromatic
`K_5`.

## Theorem 1: three branches are sufficient and necessary

There is a `good43` if and only if, for some `d` in `{18,19,20}`, there are
disjoint labeled sets `A,B` of orders `d,42-d`, red/blue colorings inside
`A` and `B`, and a zero-one matrix

```text
x_ab = 1 iff ab is red,       a in A, b in B,
```

satisfying Conditions 1--4 below.

1. `G[A]` contains neither a red `K_4` nor a blue `K_5`.
2. `G[B]` contains neither a red `K_5` nor a blue `K_4`.
3. Every active mixed clause below is satisfied.
4. If `e_A,e_B` are the internal red-edge counts, `p_a` is the red degree
   of `a` inside `A`, `q_b` is the red degree of `b` inside `B`, and
   `r_a=sum_b x_ab`, `c_b=sum_a x_ab`, then

```text
d-1-p_a <= r_a <= 23-p_a,                    a in A,
d-q_b   <= c_b <= 24-q_b,                    b in B,
d + e_A + e_B + sum_(a,b) x_ab <= 451.
```

The active red clauses are indexed by `S subset A`, `T subset B` such that
`|S|+|T|=5`, `|S|` is 1, 2, or 3, and every edge internal to `S` and to `T`
is red.  The clause is

```text
OR_(a in S,b in T) not x_ab.                              (R)
```

The active blue clauses are indexed in the same way, except `|S|` is 2, 3,
or 4 and every internal edge is blue.  The clause is

```text
OR_(a in S,b in T) x_ab.                                  (B)
```

Thus every inner clause has width four or six.

### Necessity and the exhaustive branch set

Start with a `good43`.  Exchange red and blue if necessary so that the red
graph has at most

```text
floor(choose(43,2)/2) = 451
```

edges.  Choose a vertex `v` of minimum red degree `d`.  The average-degree
bound gives

```text
d <= floor(2*451/43) = 20.                                (1)
```

The established equality `R(4,5)=25`, applied to either colored
neighborhood of any vertex, gives the familiar degree window

```text
18 <= degree_red(u) <= 24                                 (2)
```

for every vertex `u`.  In particular `d` is exactly 18, 19, or 20.  Put
`A=N_red(v)` and `B=N_blue(v)`.  A red `K_4` in `A` would extend with `v`
to a red `K_5`, while a blue `K_5` in `A` is already forbidden.  This proves
Condition 1.  Color reversal proves Condition 2.

Condition 4 is just (2), minimum degree, and the sparse-color edge cap.  For
example the total red degree of `a in A` is `1+p_a+r_a`, whereas that of
`b in B` is `q_b+c_b`.  The displayed intervals follow.

It remains to classify five-sets not containing `v` and meeting both sides.
A mixed red five-set cannot use four vertices of `A`, by Condition 1, so its
`A:B` split is `1:4`, `2:3`, or `3:2`.  Its internal edges activate (R),
and its cross edges would violate (R).  Similarly, Condition 2 prevents a
mixed blue five-set from using four vertices of `B`, leaving exactly the
splits `2:3`, `3:2`, and `4:1` in (B).  A good graph satisfies every such
clause.

### Sufficiency

Adjoin a new vertex `v`, make all `vA` edges red and all `vB` edges blue,
and use the matrix for the cross edges.  A monochromatic five-set containing
`v` would give a red `K_4` in `A` or a blue `K_4` in `B`.  A five-set wholly
inside one side is excluded by Conditions 1 and 2.  Every remaining five-set
meets both sides, and the preceding split classification says it is excluded
by (R) or (B).  The resulting physical coloring is a `good43`.

Notice that the degree and total-edge inequalities are redundant for this
reverse implication; they retain all normalized target graphs and prune the
construction problem.

## Exact dimensions

After the 42 root-edge colors have been fixed, 861 physical variables remain.
The master has `choose(d,2)+choose(42-d,2)` internal variables, and the inner
matrix has `d(42-d)` variables.  The master link constraints have

```text
choose(d,4) + choose(d,5) + choose(42-d,4) + choose(42-d,5)
```

clauses.  Consequently:

| `d` | `|A|+|B|` | master variables | inner variables | master clauses |
|---:|:---:|---:|---:|---:|
| 18 | 18+24 | 429 | 432 | 64,758 |
| 19 | 19+23 | 424 | 437 | 58,008 |
| 20 | 20+22 | 421 | 440 | 53,998 |

For fixed links, all unresolved physical choices are therefore a single
432--440-variable bipartite matrix.  This is a factorization of the complete
unrestricted problem, not a claim that the total number of variables has
fallen before a link is fixed.

If `c_i(H)` and `a_i(H)` count the `i`-cliques and `i`-independent sets of a
red graph `H`, the exact numbers of active clauses for fixed links are

```text
red  = c_1(A)c_4(B) + c_2(A)c_3(B) + c_3(A)c_2(B),
blue = a_2(A)a_3(B) + a_3(A)a_2(B) + a_4(A)a_1(B).
```

## Theorem 2: sound event-core feedback

Each active mixed event `E` has two parts:

* its **support** `P_E`, the signed internal-edge literals saying that every
  edge inside `S` and `T` has the activating color; and
* its cross clause `D_E`, equal to (R) or (B).

Fix a master link and let `U` be any collection of its active events.  If the
cross formula

```text
AND_(E in U) D_E
```

is unsatisfiable, then the following is a sound master clause:

```text
OR_(ell in union_(E in U) P_E) not ell.                  (L)
```

Indeed, any later master assignment satisfying every literal in the union
activates every event in `U`.  Its cross formula therefore contains the same
unsatisfiable subformula.  It cannot lift to a good graph.  Clause (L) removes
the entire internal-link subcube sharing those supporting edge colors, not
only the single link assignment.  A DRAT/LRAT proof, or a separately checked
finite certificate, for the cross unsatisfiability makes each such feedback
step auditable.

This theorem deliberately concerns a core of mixed-event clauses.  If a
solver also uses degree or total-edge cardinality constraints, those clauses
must either be included symbolically with their internal-edge dependencies or
excluded from the certified event core.  An `UNKNOWN` solver result licenses
no learned clause.

## Scope and trust

The proof imports only the established upper half `R(4,5)<=25` of the
classical equality.  It assumes no automorphism, regularity, catalog
completeness, carrier normalization, or local-search completeness.  The
factorization is a theorem and exact construction interface; it does **not**
produce a `good43`, eliminate any of the three branches, or improve the
published Ramsey bound by itself.

The earlier repository artifact
[`ramsey_r55_doubly_exact_cross_normal_form`](../ramsey_r55_doubly_exact_cross_normal_form)
is the direct conceptual predecessor: it gives the same mixed-clause idea for
a catalog-dependent balanced `21+21` hard branch.  The contribution here is
the catalog-free sparse-minimum normalization covering every unrestricted
candidate, the exact three-branch ledger, and the sound support-core feedback
rule.  No claim of historical priority outside the searched repository and
Discovery Net is made.
