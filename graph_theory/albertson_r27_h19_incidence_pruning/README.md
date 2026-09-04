# Incidence pruning of the Albertson `r=27`, `h=19` frontier

This note advances the sole surviving Albertson frontier row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27.
```

Put

```text
L={v:d_G(v)=26},  Q=V(G)-L,  h=|Q|.
```

The preceding structural reduction proves `h>=19` and, at equality, leaves
four possible forms for `G[L]`.  It also gives a rigid colour-incidence row
for an isolated large clique `B` in each form.  We prove the following
strict refinement.

## Lemma

If `h=19`, forms `A0` and `A1` of the four-form reduction are impossible.
In form `B`, `chi(G[Q])<=10`; in form `C`, `chi(G[Q])=9`.

Equivalently, every `h=19` survivor must occur in one of only these cases:

| form | blocks of `G[L]` | `e(G[Q])` | remaining `chi(G[Q])` |
|---|---|---:|---:|
| B | isolated `K19`; two `K8` blocks sharing a cut vertex | 56 | 8, 9, or 10 |
| C | isolated `K18`; `K8,K9` sharing a cut vertex | 46 | 9 |

This removes both three-component forms and four of the eight
form-and-chromatic subcases left by the preceding reduction.  It does not
exclude the four cases in the table and does not prove Albertson's conjecture
for `r=27`.

## Imported four-form conclusion

At `h=19`, every vertex of `Q` has degree at least 27 and `|L|=34`.  The
possible low graphs, their isolated large clique `B`, and the allowed
chromatic numbers `c=chi(G[Q])` are:

| form | `G[L]` | `|B|` | `e(G[Q])` | allowed `c` |
|---|---|---:|---:|---:|
| A0 | isolated `K18,K8,K8` | 18 | 38 | 9 |
| A1 | isolated `K18`; two `K8` joined by one bridge | 18 | 39 | 9 |
| B | isolated `K19`; two `K8` sharing a cut vertex | 19 | 56 | 8--11 |
| C | isolated `K18`; `K8,K9` sharing a cut vertex | 18 | 46 | 9--10 |

For every optimal `c`-colouring of `G[Q]`, there is a common set `F` of
`27-|B|` colours such that every vertex of `B` has exactly one neighbour in
each colour of `F` and no other neighbour in `Q`.  Hence the total number of
`B`--`Q` edges entering any colour in `F` is exactly `|B|`, while a colour
outside `F` receives none.

## A small chromatic-core observation

If a graph `X` has chromatic number `c`, it contains a `c`-critical subgraph
`R`.  Every vertex of `R` has degree at least `c-1`, so if `|R|>=c+1`,

```text
e(X) >= e(R) >= ceil((c-1)(c+1)/2).                 (1)
```

Consequently, if the left side is smaller than the last quantity, then
`|R|=c` and `R=K_c`.

We will use (1) in four cases:

| `(c,e(G[Q]))` | threshold in (1) | forced core |
|---:|---:|---:|
| `(9,38)` | 40 | `K9` |
| `(9,39)` | 40 | `K9` |
| `(11,56)` | 60 | `K11` |
| `(10,46)` | 50 | `K10` |

## Excluding A0 and A1

In either A form, `F` is the full set of nine colours.  A forced `K9` uses
all nine colours once.  The other ten vertices of `Q` occupy those same
nine colour classes, so some colour class contains one core vertex and at
least two vertices outside the core.  Fix such a triple `Z`.

There are respectively only two or three edges of `G[Q]` outside the `K9`.
The sum of the three `G[Q]`-degrees in `Z` is therefore at most

```text
A0: 8+2*2=12,
A1: 8+2*3=14.                                      (2)
```

Indeed the core vertex has its eight core edges, and every remaining edge
contributes at most two incidences to `Z`.

Let `S=L-B`, so `|S|=16`, and let `b(q)=|N_G(q) intersect B|`.  Since every
`q in Q` has degree at least 27,

```text
b(q) >= 27-|S|-d_{G[Q]}(q)=11-d_{G[Q]}(q).         (3)
```

Summing (3) on `Z` and applying (2) gives at least 21 `B`-incidences in A0
and at least 19 in A1.  But the rigid incidence row gives exactly 18
incidences to the whole colour class containing `Z`.  Both are
contradictions.

## Removing the top chromatic cases in B and C

Suppose form B has `c=11`.  Observation (1) forces a `K11` in `G[Q]`.
Here `|F|=8`, so a core vertex `q` has a colour outside `F` and consequently
has no neighbour in `B=K19`.  Only one edge of `G[Q]` lies outside the
`K11`, whence

```text
d_{G[Q]}(q) <= 10+1=11.
```

The remaining low set has order 15.  Thus `d_G(q)<=11+15=26`, contradicting
`q in Q`.

Suppose form C has `c=10`.  The same argument forces a `K10`.  Now `|F|=9`,
so one core vertex `q` again has a colour outside `F` and no neighbour in
`B=K18`.  There is one edge outside the core, and the remaining low set has
order 16.  Therefore

```text
d_G(q) <= (9+1)+16=26,
```

the same contradiction.  The imported range `9<=c<=10` leaves `c=9`.

## Reproduction

Run under CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
python3 independent_check.py
```

The primary checker reconstructs the four low forms, verifies their edge
counts and low degrees, checks all four chromatic-core thresholds, and audits
the incidence inequalities.  The independent checker explicitly enumerates
all placements of the two or three residual high edges for the A cases and
all placements of the one residual edge in the B and C endpoint cases.

Both scripts use exact integer/set arithmetic only.  They use no solver,
randomness, floating point, generated input, external data, or project
imports.  The executable trust boundary is CPython.  The graph-theoretic
bridge is the deductive proof above; the scripts audit its finite arithmetic
and extremal endpoint claims rather than enumerate critical graphs.

Expected result digests:

```text
primary:     34e557c7105ce427a60a0076852033f334c19231c97f5905ea45a48a99d05ffc
independent: 7b9441024d2ffc037a7413ade07bf85e5245ea51a3b2f4309c0fd9958e9a5e4e
```

## Scope, provenance, and sources

The imported boundary is Sadhu's September 2026 connected-complement
frontier and the committed four-form/rigid-incidence lemma, which itself
depends on Gallai's low-vertex theorem, Stehlik's theorem, Konig's theorem,
and the preceding committed closures through `h=18`.

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1).
* M. Stehlik, [*Critical graphs with connected
  complements*](https://doi.org/10.1016/S0095-8956(03)00069-8), JCTB 89
  (2003), 189--194.
* The preceding [four-form structural
  reduction](../albertson_r27_order53_h19_reduction/README.md).

Targeted searches of the September 2026 paper, its critical-graph sources,
and the committed Discovery Net found no prior version of this incidence
pruning.  This is a search-relative novelty statement, not a claim of
historical priority.
