# Split-colour Hall closure forces `h>=21` at Albertson `r=27`

This note advances the sole surviving Albertson frontier row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27.
```

Put

```text
L={v:d_G(v)=26},  Q=V(G)-L,  h=|Q|.
```

The preceding weighted-incidence reduction proves `h>=20` and leaves five
form/colour cases at equality.  We prove that all five are impossible.
Consequently every hypothetical counterexample in the surviving row has

```text
h>=21.                                                     (1)
```

This closes only the `h=20` equality boundary.  It does not exclude `h>=21`,
improve the universal crossing lower bound by itself, or prove Albertson's
conjecture for chromatic number 27.

## Imported five-case frontier

Assume `h=20` and write `X=G[Q]`.  The height-1929 reduction leaves exactly
these possibilities, with no other edges in `G[L]`:

| form | `G[L]` | `e(X)` | `chi(X)` |
|---|---|---:|---:|
| D20 | isolated `B=K20`; two `K7` blocks meeting in one cut vertex | 87 | 7, 8, 9, or 10 |
| D19 | isolated `B=K19`; `K7,K8` meeting in one cut vertex | 75 | 8 |

Let `b=|B|`, `S=L-B`, and `f=27-b`.  For every optimal `c`-colouring of
`X`, the imported clique-list obstruction gives exactly `f` *active* colour
classes.  Every vertex of `B` has exactly one neighbour in each active class
and no neighbour in any other class.  Define the colouring-independent
column weight

```text
w(x)=|N_G(x) intersect B|,  0<=w(x)<=b.                  (2)
```

Each active class has total weight `b`, every other class has weight zero,
and hence

```text
sum_{x in Q} w(x)=bf.                                    (3)
```

The reviewed active-class recolouring lemma also says

```text
w(x)=b  implies  d_X(x)>=f-1.                            (4)
```

We retain all of these statements as imported hypotheses and add one new
operation: split one intermediate-weight vertex into a fresh colour.

## The split-colour Hall lemma

Fix an optimal colouring of `X`.  Suppose some vertex `x` has

```text
0<w(x)<b.                                                (5)
```

The colour class containing `x` is active and has total weight `b`, so it
contains another vertex.  Move only `x` to a fresh colour.  This remains a
proper colouring and uses `c+1` colours.

Before the split, every vertex of `B` sees the same `f` active colours.  A
vertex of `B` adjacent to `x` now sees the fresh colour in place of the old
colour of `x`; a vertex not adjacent to `x` still sees the old set.  Thus the
available-colour lists on the clique `B` have exactly two types.  Each list
has size

```text
26-f=b-1,                                                (6)
```

the two types differ by exchanging the old and fresh colours, and their
union has size `b`.  Both types occur by (5).

Hall's condition is immediate.  Any proper subset of the `b` clique vertices
has at most `b-1` members and sees a union of at least `b-1` available
colours.  The full set sees both list types and hence a union of `b` colours.
Therefore `B` has a system of distinct representatives and can be coloured.

It remains to colour `S`.  Since `B` is isolated in `G[L]`, colours used on
`B` may be reused on `S`.  Use only colours absent from the new colouring of
`X`: in D20 there are at least `26-11=15` of these colours for a 7-colourable
graph `S`, and in D19 there are `26-9=17` for an 8-colourable graph `S`.
This gives a 26-colouring of all of `G`, a contradiction.  Hence every
column weight is an endpoint:

```text
w(x) in {0,b} for every x in Q.                          (7)
```

## The terminal degree certificate

Equations (3) and (7) force exactly `f` full-weight vertices and `20-f`
zero-weight vertices.  A zero-weight vertex has no neighbour in `B`.  Since
it lies in `Q`, its degree in the 27-critical graph is at least 27, while it
has at most all `33-b` vertices of `S` as low neighbours.  Therefore

```text
w(x)=0  implies  d_X(x)>=27-(33-b)=b-6.                 (8)
```

Combine (4) and (8), then compare with the handshake identity:

| form | full / zero columns | degree-sum floor | exact `2e(X)` | margin |
|---|---:|---:|---:|---:|
| D20 (`b=20,f=7`) | 7 / 13 | `7*6+13*14=224` | 174 | 50 |
| D19 (`b=19,f=8`) | 8 / 12 | `8*7+12*13=212` | 150 | 62 |

Both floors contradict `sum_x d_X(x)=2e(X)`.  Thus neither low form exists,
which proves (1).

## Reproduction and trust boundary

Run under CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
python3 independent_check.py
```

The primary checker audits Hall's inequality for every possible nontrivial
split weight, both colour ranges, the endpoint incidence totals, and both
handshake contradictions.  The independently organized checker constructs
the two list types and finds an explicit maximum matching for every split.  It
also enumerates all `77,520` labelled D20 endpoint vectors and all `125,970`
labelled D19 endpoint vectors.

Expected certificate digests:

```text
primary:     d5d6742f19f96cb022dd844a2b6bfcb0aef0f7161e839bcf10971ec493c62181
independent: 6f22a1597313c1987fdb66a04fd6562eb67c416081555e4409adc75bc24bc185
```

SHA-256 of the executable sources:

```text
verify.py            b17e9076d73f9fa97fe1977623961f7feb4e6f3d7ccc7780435f69d661f21df6
independent_check.py  4a16176e9b660583654e9196453435e9e5df9b44166711ddf622c888aa87fc98
```

Both programs use only exact CPython integer, set, tuple, matching, and hash
arithmetic.  They use no solver, randomness, floating point, generated input,
external data, or project import.  The executable trust boundary is CPython;
the passage from the imported incidence statement through the colour split
to Hall's theorem is the deductive proof above.

The mathematical trust boundary is Sadhu's connected-complement frontier and
the committed structural chain through the five-case `h=20` reduction.  In
particular, the Gallai-block classification, the every-optimal-colouring
incidence statement, and the full-weight recolouring floor are imported rather
than recomputed here.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the order-53/54
  connected-complement frontier.
* The preceding [weighted-incidence `h=20`
  reduction](../albertson_r27_h20_weighted_pruning/README.md), Discovery Net
  contribution `bafkreiaf6feukmiwlfnvqgjfg4ihi6czm6qlsidw2qnqsnivrvpkrevb6a`
  at height 1929, verified source commit
  `7d64cb5445fdbaddea878964cdaa02496e290ff5`.

The arXiv search was refreshed on 2026-09-04 and returned Sadhu's paper as the
latest directly relevant preprint.  Searches of that paper, its critical-graph
sources, and Discovery Net through indexed height 1932 found no prior
split-colour Hall closure of these five cases.  This is a search-relative
novelty statement, not a claim of historical priority.
