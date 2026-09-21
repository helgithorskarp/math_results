# Stable transitivity of local-order tournaments

## 1. Definitions

An ordinary tournament `T` on a finite vertex set `V` is **locally
transitive** if both `T[N+(v)]` and `T[N-(v)]` are transitive for every
vertex `v`.  These tournaments are also called **local orders**.

Write a total order and its transitive tournament interchangeably.  The
**stable-transitivity number** `m(T)` is the least `a>=0` for which there are
orders `P_1,...,P_a` and `Q_1,...,Q_(a+1)` satisfying

```text
T + P_1 + ... + P_a = Q_1 + ... + Q_(a+1)          (1)
```

as directed multigraphs.  In particular, `m(T)=0` exactly when `T` is
transitive.

## 2. A rooted switching lemma

For a tournament `T` and a vertex `v`, put

```text
L = {v} union N+(v),       H = N-(v).
```

Let `P` be obtained from `T` by reversing every arc between `L` and `H`, and
no arc within either side.

**Lemma 1.** If `T` is locally transitive, then `P` is transitive.

**Proof.**  The tournament on `L` is transitive: `T[N+(v)]` is transitive and
`v` precedes all its vertices.  The tournament on `H` is transitive by local
transitivity.  Consequently, a directed triangle in `P` would have to meet
both sides.

First suppose such a triangle has `x,y in L` and `z in H`.  After cyclically
naming it, its arcs in `P` are

```text
x -> y -> z -> x.
```

The cut reversal says that the corresponding arcs of `T` are

```text
x -> y,       z -> y,       x -> z.                (2)
```

Neither `x` nor `y` is `v`: the first possibility contradicts `z->v`, and
the second contradicts `v->x`.  Now `z,v,x` all lie in `N-(y)`, while

```text
z -> v -> x -> z.
```

This contradicts transitivity of `T[N-(y)]`.

The other case has `x in L` and `y,z in H`, with the triangle named
`x->y->z->x` in `P`.  In `T` this gives

```text
y -> x,       y -> z,       x -> z.                (3)
```

Here `x` is not `v`, since every vertex of `H` dominates `v`.  The three
vertices `z,v,x` lie in `N+(y)` and induce the directed triangle
`z->v->x->z`, again a contradiction.  Thus `P` has no directed triangle.
Every nontransitive tournament contains a directed triangle, so `P` is
transitive. `square`

This also proves the useful half of the classical characterization of local
orders as the tournaments switching-equivalent to a transitive tournament.
For completeness, the converse is direct.  If `P` is a total order and `T`
is obtained by reversing one cut `(L,H)`, then, for `x in L`,

```text
N+_T(x) = (L after x in P) union (H before x in P).
```

All vertices in the first displayed part precede all vertices in the second
part under `T`, and each part retains its `P`-order.  This is a transitive
order of `N+_T(x)`.  The in-neighborhood and the two cases with `x in H`
are identical with the roles reversed.  Hence `T` is locally transitive.

## 3. Exact stable-transitivity theorem

**Theorem 2.** For every locally transitive tournament `T`,

```text
m(T) = 0  if T is transitive,
m(T) = 1  otherwise.                               (4)
```

More explicitly, choose any root `v`, and obtain `L,H,P` from Lemma 1.  Let
`P_L` and `P_H` be the restrictions of the total order `P` to the two sides,
and define the total orders

```text
A = P_L followed by P_H,
B = P_H followed by P_L.
```

Then

```text
T + P = A + B.                                     (5)
```

Indeed, within either side all four tournaments in (5) agree with `P`.
Across the cut, `T` and `P` give the two opposite orientations, as do `A`
and `B`.  Thus (5) is a degree-one stable-transitivity witness, proving
`m(T)<=1`.  If `T` is nontransitive then `m(T)!=0`, which proves (4).

The construction is root-flexible: every choice of `v` gives a (not
necessarily distinct) degree-one witness.

## 4. Closed formula for carousel tournaments

Let `R_(2q+1)` (`q>=1`) be the carousel tournament on
`{0,1,...,2q}` in which

```text
i -> j  iff  1 <= (j-i mod (2q+1)) <= q.
```

Set

```text
L = (0,1,...,q),             H = (q+1,q+2,...,2q),
P = (0,q+1,1,q+2,...,q-1,2q,q),
A = (0,1,...,2q),            B = (q+1,...,2q,0,...,q).
```

Then `T+P=A+B` for `T=R_(2q+1)`.  To check the only nontrivial pairs, take
`i in L` and `j in H`.  The carousel has `i->j` exactly when `j-i<=q`,
whereas `P` has `i->j` exactly when `j-i>=q+1`; so these orientations are
opposite.  The orders `A` and `B` are also opposite on every cross pair.
Within each side all four orientations are increasing.  Since every
`R_(2q+1)` is nontransitive,

```text
m(R_(2q+1)) = 1.                                  (6)
```

## 5. Substitution-closure consequence

Let `C` be the least class of tournaments that contains every locally
transitive tournament and is closed under tournament substitution.  The
previously proved substitution law

```text
m(Q[T_1,...,T_r]) = max(m(Q),m(T_1),...,m(T_r))    (7)
```

implies the following rank-uniform extension.

**Corollary 3.** Every tournament in `C` has stable-transitivity number at
most one, and every nontransitive member has stable-transitivity number
exactly one.

The upper bound follows by structural induction from (4) and (7).  The lower
bound for a nontransitive member is again the definition of `m=0`.

Theorem 2 and the carousel formula do not depend on (7).  Only Corollary 3
uses the earlier substitution theorem.

## 6. Proof and computation boundary

Theorem 2 is a universal combinatorial proof.  `verify.py` is a separate
definition-level audit: it exhausts all labelled tournaments through order
six, tests the rooted construction for every locally transitive tournament
and every root, checks cut switches independently, and verifies the carousel
formula through a declared finite range.  Those checks guard conventions and
implementation details; they are not used to infer the unbounded theorem.
