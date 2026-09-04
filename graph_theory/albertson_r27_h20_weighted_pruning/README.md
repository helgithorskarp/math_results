# Weighted-incidence pruning at the Albertson `r=27`, `h=20` boundary

This note advances the sole surviving Albertson frontier row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27.
```

Put

```text
L={v:d_G(v)=26},  Q=V(G)-L,  h=|Q|.
```

The preceding structural chain proves `h>=20`.  We classify and prune the
new equality boundary.  If `h=20`, every hypothetical counterexample has
exactly one of the following forms:

```text
D20: G[L] = an isolated K20 together with two K7 blocks meeting
            in one cut vertex,
     e(G[Q])=87,  chi(G[Q]) in {7,8,9,10};

D19: G[L] = an isolated K19 together with K7 and K8 blocks meeting
            in one cut vertex,
     e(G[Q])=75,  chi(G[Q])=8.
```

There are no other edges in `G[L]`.  These five form/colour cases are
necessary conditions, not existence claims.  In particular, this result
does not exclude `h=20`, improve the crossing lower bound `6071` by itself,
or prove Albertson's conjecture for chromatic number 27.

## Imported facts

We use the following established inputs.

1. Sadhu's September 2026 frontier and the subsequent committed closures
   leave only a 27-critical graph on 53 vertices and 713 edges whose
   complement is connected and which contains no subdivision of `K27`.
2. Gallai's theorem says that every block of `G[L]` is a clique or an odd
   cycle.
3. Stehlik's theorem makes the complement factor-critical.  In particular,
   a conformal triangle in the complement is impossible, since it and a
   perfect matching of the other 50 vertices would give a 26-colouring.
4. The independently reviewed rooted Gallai lemma puts every low vertex in
   a clique block of `G[L]` of order at least `27-h`.
5. Every high vertex has complement degree at most 25, because its graph
   degree is at least 27.
6. The committed and independently reviewed recolouring closure proves
   `h>=20`.  Its height-1927 review also states the general active/zero-class
   weighted-recolouring lemma used below.  We use the matching/conformal-
   triangle mechanism from the preceding two-clique reductions; its numerical
   hypotheses at `h=20` are checked below.

Set `h=20`.  Then `|L|=33`, every low vertex belongs to a clique block of
order at least

```text
s=27-h=7,                                                (1)
```

and the fixed low degree sum gives

```text
e(L,Q)=26*33-2e(G[L]),
e(G[Q])=e(G[L])-145,
e(G[L])>=145.                                            (2)
```

Call the clique blocks supplied by (1) *large*.

## The block-count reduction

Restrict the block-cut forest to the large-block nodes and their common cut
vertices.  If there are `b` large blocks and this restricted forest has `c`
components, put `q=b-c`.  Repeated cut vertices give

```text
sum_i |B_i|=33+q.                                        (3)
```

A block outside this family meets each direct component in at most one
vertex.  The connector blocks therefore form a hyperforest and contribute
at most `binom(c,2)` edges in total.  In every case below `c<=4`, so such a
connector cannot be an odd cycle of order at least five; it is a clique.

Six large blocks would have union order at least `6*7-5=37`, so `b<=5`.
One block cannot cover `L`, because a `K27` is already terminal.  For five
blocks, the only feasible values `q=2,3,4` give respective upper bounds

```text
108, 113, 120
```

on `e(G[L])`, all below (2).  For four blocks, `q=0,1,2,3` give caps

```text
135, 144, 155, 168.
```

The first two again contradict (2).  Exact enumeration of the remaining
integer partitions gives 5 and 14 rows for `q=2,3`.  If `c_Q=chi(G[Q])`,
the elementary critical-subgraph bound

```text
e(G[Q]) >= binom(c_Q,2)                                  (4)
```

shows in every one of these 19 rows that

```text
max_i |B_i| + c_Q <=22.
```

The chromatic number of a Gallai block graph is the maximum chromatic number
of a block.  Disjoint palettes therefore give a 26-colouring (in fact a
22-colouring), excluding all four-block forms.  Hence only two or three
large blocks remain.

## The two-block regime remains terminal

Two large blocks cannot meet: their orders would sum to 34, while a common
cut vertex of degree 26 would require their sum to be at most 28.  Thus they
are disjoint cliques `C=K_a,D=K_b`, with `a+b=33`, joined by at most one
bridge.  Write

```text
a=7+p,  b=7+q,  p+q=19.
```

An ordinary row of the complement incidence graph between `C` and `Q` has
size `p`, and the analogous `D`-row has size `q`; a bridge endpoint has one
additional complement neighbour.  Exact edge accounting leaves nine rows.
The last column is the sum of the bridge indicator and `e(complement(G[Q]))`.

| `(a,b)` | `(p,q)` | deficit |
|---|---|---:|
| `(8,25)` | `(1,18)` | 7 |
| `(9,24)` | `(2,17)` | 23 |
| `(10,23)` | `(3,16)` | 37 |
| `(11,22)` | `(4,15)` | 49 |
| `(12,21)` | `(5,14)` | 59 |
| `(13,20)` | `(6,13)` | 67 |
| `(14,19)` | `(7,12)` | 73 |
| `(15,18)` | `(8,11)` | 77 |
| `(16,17)` | `(9,10)` | 79 |

The previous parametric matching proof continues across this boundary.  We
record the exact slack so the continuation is explicit.  The uniform-row
lemma says that a bipartite graph whose left side has more than `r` vertices
and whose left degrees are at least `r` either has an `(r+1)`-matching or all
left rows are one common `r`-set.  This is the direct Konig vertex-cover
argument used in the earlier reductions.

Without a low bridge, simultaneous matchings of orders `p+1,q+1` give 20
singleton high colours and six residual pairs across the complement-complete
`C,D` cut, hence 26 colours.  Otherwise one side has a common support `S`.
Then `C union (Q-S)` is a 27-vertex clique apart from the target edges in the
complement on `Q-S`.  No target gives `K27`.  A unique target has an external
path by the same support-type construction as before: a target endpoint has
at least two graph neighbours in the opposite clique, a one-end support has
at least nine, and an opposite-type support has at least ten.  These are the
exact consequences of complement degree at most 25; all are sufficient for
the required distinct one- or two-clique-vertex route.  The special
`p=1` row again has an opposite `K25`.

With two target edges, contract either target.  A `q`-matching gives 19 high
colour classes and seven residual low pairs, again 26 colours.  If two
distinct contractions fail, equal-size row parity makes all opposite rows a
common `q`-set `R`.  The degree cap makes `S,R` disjoint, and

```text
Q=S disjoint-union R disjoint-union {z}.
```

Factor-critical matching balance and conformal-triangle exclusion give the
same terminal certificate as in the preceding proof: `z` has complement
neighbours in both supports, while the two internal support graphs and the
cross graph between those two neighbour sets are empty.  The resulting
missing branch edges route through distinct opposite low-clique vertices.
The conformal-triangle matchings leave eight low vertices on each side, so
the earlier construction loses no required vertex at `h=20`.

With one low bridge, the augmented endpoint rows either give compatible
one-larger matchings or force disjoint supports and a unique `z`.  In the
first case six residual cross-pairs can avoid the single bridge.  In the
second, the sole missing branch edge routes through the bridge and one
additional opposite-clique vertex.  Thus every two-block form is
26-colourable or contains a `TK27`, and is impossible for the counterexample.

## Three blocks and the isolated-clique obstruction

For three large blocks, `q=0,1,2`, and connector-edge totals are bounded by
`3,1,0`, respectively.  Intersecting blocks of orders `u,v` satisfy
`u+v<=28`.  For `q=2`, a common cut in all three would have

```text
sum_i (|B_i|-1)=32>26
```

low neighbours, so only a path with two distinct cuts remains.

Exact enumeration of (2)--(4) gives 76, 42, and 24 edge-budget rows for
`q=0,1,2`.  Disjoint palettes close all but 40.  Every exception has a unique
largest block.  If `c_Q` is replaced by its upper bound from (4), then for
each smaller block `K_t`,

```text
26-c_Q > t-1.                                            (5)
```

Fix an optimal colouring of `G[Q]` from a 26-colour palette, and give a low
vertex the colours absent from its `Q`-neighbourhood.  Its list has size at
least its low degree.  All `26-c_Q` unused colours lie in every list.  Thus
(5) gives a strict degree-list vertex in every component having a smaller
leaf block, and greedy list colouring closes that component.  The only
possible obstruction is an isolated copy of the unique largest block.

The largest block is isolated only in the following situations: no
connector; one bridge joining the two smaller disjoint blocks; or the two
smaller blocks meet directly and there is no connector.  Exactly 14 rows
remain:

| large-block orders | relation of smaller blocks | `e(G[Q])` |
|---|---|---:|
| `(7,7,19)` | disjoint / one bridge | 68 / 69 |
| `(7,8,18)` | disjoint / one bridge | 57 / 58 |
| `(7,9,17)` | disjoint / one bridge | 48 / 49 |
| `(8,8,17)` | disjoint / one bridge | 47 / 48 |
| `(7,7,20)` | one common cut | 87 |
| `(7,8,19)` | one common cut | 75 |
| `(7,9,18)` | one common cut | 65 |
| `(7,10,17)` | one common cut | 57 |
| `(8,8,18)` | one common cut | 64 |
| `(8,9,17)` | one common cut | 55 |

## Applying the reviewed active-class recolouring lemma

The height-1927 independent review of the `h=19` closure records the following
general form.  Let `X` be `c`-chromatic and let `w:V(X)->{0,...,b}`.  Suppose every proper
`c`-colouring has exactly `f` colour classes of total weight `b`, while all
other classes have weight zero.  Then

```text
0<w(x)<b  implies d_X(x)>=c-1,
w(x)=b    implies d_X(x)>=f-1.                           (6)
```

To prove this, move a positive-weight vertex `x` to a colour class it misses.
If its original class is a singleton, this is a forbidden `(c-1)`-colouring.
Otherwise it is another `c`-colouring.  Moving weight `a` between two active
classes changes `(b,b)` to `(b-a,b+a)`, which is impossible.  Moving it from
an active class to a zero class changes `(b,0)` to `(b-a,a)`, which has the
required profile only for `a=b`; then the active and zero colours exchange
roles.  This proves (6).  Notice that the statement permits any number
`c-f` of zero-weight colour classes.

Apply this to an isolated largest clique `B=K_b`, `X=G[Q]`, and

```text
w(x)=|N_G(x) intersect B|,       f=27-b.                 (7)
```

For every optimal colouring of `X`, the clique-list obstruction says that
the lists on `B` are one common `(b-1)`-set.  Equivalently, there are exactly
`f` active colours, and every vertex of `B` has one neighbour in each active
colour and none in the others.  Thus each active colour has total weight `b`
and each other colour has weight zero, as required above.  Also

```text
sum_x w(x)=bf.                                           (8)
```

If `w(x)=0`, criticality and the `33-b` low vertices outside `B` give

```text
d_X(x)>=27-(33-b)=b-6.                                  (9)
```

For each of the 14 rows and every integer `f<=c<=c_Q`, minimise the sum of
the degree floors (6),(9) over twenty integer weights in `[0,b]` satisfying
(8).  The exact values eliminate every case except

```text
(b,e(X),c)=(20,87,7),(20,87,8),(20,87,9),(20,87,10),
             (19,75,8).
```

For example, every positive-weight vertex has degree at least `f-1`.
This alone gives degree-sum floors 140, 160, and 180 for `b=19,18,17`,
closing all corresponding sparse rows except the `b=19,e(X)=75` row.  In
that row, `c>=9` raises the exact floor to 153, above `2e(X)=150`, so only
`c=8` remains.  For `b=20,e(X)=87`, the exact floors for
`c=7,...,13` are

```text
120, 134, 148, 162, 176, 190, 204.
```

Since `2e(X)=174`, precisely `c=7,8,9,10` survive.  Reading the two block
signatures back gives `D20` and `D19`, proving the opening reduction.

## Reproduction and trust boundary

Run under CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
python3 independent_check.py
```

The primary checker recursively enumerates the block-order signatures,
labelled direct-intersection geometries, connector-edge over-approximations,
palette exceptions, and all twenty-vertex weight totals.  It also checks the
nine two-clique rows, every terminal numerical margin, and all 35,910 ordered
pairs of distinct target contractions.

The independent checker uses combinations with replacement for the block
orders and minimises the weighted bound by zero/intermediate/full
multiplicities rather than by vertex dynamic programming.  Both use exact
CPython integer/set/tuple arithmetic, with no solver, randomness,
floating point, generated input, external data, or project import.  The
scripts audit the finite arithmetic.  The graph-theoretic bridge—including
the block-cut, list-colouring, recolouring, and subdivision arguments—is the
deductive proof above; no critical graphs or drawings are enumerated.

Expected certificate digests:

```text
primary:     69340ba8b26211a7c5d76d31f0a49730c7ac05cc5e3b565ac507155ccb176ec4
independent: 9a7353a0e13c3b9a0a901545182dccb335c497ca5a86b64075df6c7a7cc50035
```

The mathematical trust boundary is Sadhu's connected-complement frontier,
Gallai's low-vertex block theorem, Stehlik's colouring theorem, Konig's
theorem, the independently reviewed rooted Gallai lemma, and the committed
closures through `h=19`.  The `h>=20` input and its general active-class
lemma have now received an incoming independent verification and
reproduction at Discovery Net height 1927.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the order-53/54
  connected-complement frontier and exclusion of a topological `K27`.
* M. Stehlik, [*Critical graphs with connected
  complements*](https://doi.org/10.1016/S0095-8956(03)00069-8), JCTB 89
  (2003), 189--194.
* Gallai's low-vertex theorem, stated as Theorem 8 in A. Kostochka's
  [survey](https://kostochk.web.illinois.edu/docs/2008/book06.pdf).
* The preceding [`h=19` structural
  reduction](../albertson_r27_order53_h19_reduction/README.md), its
  [`h=19` closure](../albertson_r27_h19_recoloring_closure/README.md), and
  the earlier two-clique matching/conformal-triangle reductions.
* Discovery Net review
  `bafkreif3kq7g4nli7nm2e4nyefsudwzgg5kpjx2774ipixb2ma7taoc22u`, which
  independently verifies the `h>=20` input and first records the general
  active/zero-class version of the weighted-recolouring lemma used here.

The arXiv search for Albertson/crossing-number work was refreshed on
2026-09-04 and returned Sadhu's paper as the latest directly relevant
preprint.  The graph refresh through indexed height 1928 found the general
active-class lemma in the new review, so no novelty is claimed for that
standalone statement.  Targeted searches of Sadhu's paper, its cited
critical-graph sources, and the committed graph found no prior `h=20` block
classification or application reducing equality to the five cases above.
This is a search-relative assessment, not a claim of historical priority.
