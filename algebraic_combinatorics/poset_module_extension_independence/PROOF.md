# Product decomposition for linear extensions of lexicographic sums

## Statement

Let `S` be a finite poset.  For each `s in S`, let `Q_s` be a nonempty
finite poset, and let

```text
R = S(Q_s : s in S)
```

be their lexicographic sum: relations inside a block are those of `Q_s`,
and every member of `Q_s` is below every member of `Q_t` whenever `s<t` in
`S`.

Write `n_s=|Q_s|`.  An admissible block word is a word `w` on alphabet `S`
in which `s` occurs `n_s` times and every occurrence of `s` precedes every
occurrence of `t` whenever `s<t` in `S`.  Denote the set of these words by
`W(S;n_s)`.

There is a canonical bijection

```text
L(R)  <-->  W(S;n_s) x product_(s in S) L(Q_s).       (1)
```

Consequently, for a uniform random linear extension `L` of `R`:

1. its block word is uniform on `W(S;n_s)`;
2. all induced internal orders `L|Q_s` are mutually independent;
3. each `L|Q_s` is a uniform linear extension of `Q_s`;
4. the tuple of internal orders is independent of the block word.

Equivalently, for arbitrary sets `E_s subseteq L(Q_s)`,

```text
P(L|Q_s in E_s for every s) = product_s |E_s|/e(Q_s).   (2)
```

This is the simultaneous conditional-independence form of the locality
table in Lemma 2.3 of Dolores-Cuenca--Guzman-Saenz--Kim.  The underlying
product bijection is prior art.  The decision-transcript formulation below
is an explicit corollary, not a claim of priority.

## Proof of the bijection

Take a linear extension `ell` of `R`.  Replace each entry from `Q_s` by its
block label `s`; this gives a block word `w`.  Each label occurs the right
number of times.  If `s<t` in `S`, every element of `Q_s` is below every
element of `Q_t`, so every `s` in `w` precedes every `t`.  Thus `w` is
admissible.  Reading only entries from `Q_s` gives a linear extension
`ell_s` of `Q_s`.  This defines the forward map in (1).

Conversely, start from an admissible block word `w` and internal extensions
`ell_s`.  Scan `w` from left to right and replace the `k`-th occurrence of
`s` by the `k`-th element of `ell_s`.  Internal relations are respected
because `ell_s` is a linear extension.  Cross-block relations are respected
because admissibility places all of `Q_s` before all of `Q_t` when `s<t`.
The resulting word is therefore a linear extension of `R`.

The two maps undo one another entry by entry, proving (1).  Uniform measure
on a finite Cartesian product is the product of the uniform measures on its
factors, which proves all four independence statements and (2).

## Autonomous subsets

A subset `A` of a poset `P` is autonomous (a module) if every `z` outside
`A` is below all of `A`, above all of `A`, or incomparable with all of `A`.
Collapsing `A` to one point produces a quotient poset, and `P` is its
lexicographic sum with block `P[A]` and singleton blocks elsewhere.
Applying (1) gives

```text
P_P(x before y) = P_(P[A])(x before y)    for x,y in A. (3)
```

Hence the balance constant satisfies `delta(P)>=delta(P[A])` whenever
`P[A]` is not a chain.  In particular, if `P` were a minimum-order
counterexample to the 1/3--2/3 conjecture, every proper autonomous subset
of `P` would induce a chain: a nonchain `P[A]` would be a smaller poset, so
minimality and (3) would lift one of its balanced pairs to `P`.

## Arbitrary local comparison transcripts

Let a deterministic comparison tree ask only questions whose two elements
belong to the same block.  Its full transcript is a deterministic function
of the tuple `(ell_s)_s` and is independent of the block word.  If `T_tau`
is the set of internal-extension tuples reaching a node or leaf `tau`, then
the number of global linear extensions reaching it is exactly

```text
|W(S;n_s)| * |T_tau|.                                 (4)
```

Thus every node probability, every leaf probability, and every inequality
between transcript counts transfers exactly from the independent internal
experiment to the full lexicographic sum.  This contains pair-probability
transfer and the two-comparison Gold Partition transfer as special cases,
but also applies to comparison trees of arbitrary finite depth and to trees
that adaptively switch among blocks.

## Why autonomy cannot simply be dropped

Let `P={a,b,c}` have the sole relation `a<c`, and take `A={a,b}`.  The
induced poset `P[A]` is a two-element antichain, whose two linear extensions
occur once each.  The three linear extensions of `P` are

```text
a b c,   a c b,   b a c.
```

Their restrictions to `A` have multiplicities `2` and `1`.  Thus the
restriction is not uniform.  The outside point `c` distinguishes `a` from
`b`, so `A` is not autonomous.  This order-three example shows that the
module hypothesis cannot be removed from a general restriction theorem.
