# Recolouring rigidity closes the Albertson `r=27`, `h=19` boundary

This note advances the sole surviving Albertson frontier row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27.
```

Put

```text
L={v:d_G(v)=26},  Q=V(G)-L,  h=|Q|.
```

The preceding structural chain proves `h>=19`.  At equality, its latest
refinement leaves only

```text
G[L] = an isolated K19 together with two K8 blocks
       meeting in one cut vertex,
e(G[Q])=56,
chi(G[Q]) in {8,9}.                                    (1)
```

We prove that neither value in (1) is possible.  Consequently every
hypothetical counterexample in the order-53, 713-edge row has

```text
h>=20.                                                   (2)
```

This closes the complete equality boundary left by the Gallai-block
classification.  It does not exclude `h>=20` and therefore does not prove
Albertson's conjecture for chromatic number 27.

## A weighted recolouring lemma

Let `X` be a `c`-chromatic graph and let

```text
w: V(X) -> {0,1,...,b}.
```

Suppose that every proper `c`-colouring of `X` has one of the following
weight profiles, where the weight of a colour is the sum of `w` over its
colour class.

* If every colour has weight `b`, then every vertex of positive weight has
  degree at least `c-1` in `X`.
* If exactly `c-1` colours have weight `b` and the remaining colour has
  weight zero, then a vertex of weight strictly between zero and `b` has
  degree at least `c-1`, while a vertex of weight `b` has degree at least
  `c-2`.

Indeed, fix a proper `c`-colouring and a positive-weight vertex `x` in a
colour class `P`.  If `x` misses another colour class `R`, move `x` from `P`
to `R`.  If `P={x}`, this would be a proper `(c-1)`-colouring, contrary to
`chi(X)=c`; otherwise it is another proper `c`-colouring.

In the all-active case, if `w(x)=a>0`, the two affected class weights change
from `(b,b)` to `(b-a,b+a)`, contradicting the assumed profile.  Thus `x`
meets every one of the other `c-1` classes.

In the one-zero case, the same argument applies when `R` has weight `b`.
If `R` is the zero-weight class, the affected weights change from `(b,0)`
to `(b-a,a)`.  This has the required profile only when `a=b`, in which case
the active and zero colours merely exchange roles.  Hence a vertex with
`0<a<b` meets all other `c-1` classes, and a vertex with `a=b` meets the
other `c-2` positive-weight classes.  This proves the lemma.

## Applying the lemma to the rigid `K19` incidence

Let `B=K19` be the isolated clique in (1), let `X=G[Q]`, and define

```text
w(q)=|N_G(q) intersect B|  for q in Q.                  (3)
```

The imported rigid-incidence conclusion says the following for **every**
optimal colouring of `X`.  There is a common set `F` of eight colours such
that every vertex of `B` has exactly one neighbour in each colour of `F`
and no neighbour in any other colour.  On summing over the 19 vertices of
`B`, every colour in `F` has weight 19 under (3), and every colour outside
`F` has weight zero.

If `chi(X)=8`, all eight colours are in `F`.  The all-active part of the
weighted recolouring lemma gives

```text
d_X(q)>=7 whenever w(q)>0.                              (4)
```

If `chi(X)=9`, eight colours have weight 19 and one has weight zero.  The
one-zero part gives `d_X(q)>=8` for `0<w(q)<19` and
`d_X(q)>=7` for `w(q)=19`.  In particular, (4) again holds.

It remains to control vertices of weight zero.  The set `L-B` has only 15
vertices.  Since every vertex of `Q` has degree at least 27 in the
27-critical graph `G`, (3) gives

```text
w(q)=0  implies  d_X(q)>=27-|L-B|=12.                  (5)
```

Let `z` be the number of zero-weight vertices in `Q`.  From (4)--(5),

```text
2e(X) = sum_{q in Q} d_X(q)
      >= 7(19-z)+12z
      = 133+5z
      >= 133.                                           (6)
```

But (1) gives `2e(X)=112`, a contradiction.  This excludes both chromatic
possibilities in (1) and proves (2).

## Reproduction and trust boundary

Run under CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
python3 independent_check.py
```

The primary checker constructs every recolouring transition for weights
`1,...,19` in the all-active and one-zero profiles, checks the exact degree
floors, and audits the final handshake contradiction.  The independently
organized checker exhausts labelled source/target colour pairs and all
possible numbers of zero-weight vertices, without importing the primary
checker.

Both programs use exact CPython integer, list, tuple, and hash arithmetic.
They use no solver, randomness, floating point, generated input, external
data, or project import.  They audit the finite profile arithmetic; the
graph-theoretic bridge is the deductive proof above.

Expected final digests under CPython 3.9 or later are

```text
primary:     29ea242143795857749654eb9cb83eed86397974c46a4a2da5aab2743adc7a58
independent: b29cd9d3412070da7ab78897c426f986409961ca967c05c16218eb15ea8d89e8
```

SHA-256 of `verify.py`:
`5789a76fbeb9e726fc3fb709908350e9a3982f355b3f657aa3b8e4d00edb1120`.
SHA-256 of `independent_check.py`:
`53942b38720ea3969a27007be791cf5c1ea043543c8c9d22a7fdf1e14b158404`.

The mathematical trust boundary is Sadhu's connected-complement frontier
and the committed, independently reviewed structural chain through the
four-form, incidence-pruning, and implicit-edge lemmas.  In particular, the
every-optimal-colouring incidence statement is imported rather than
reproved here.  No critical graphs are enumerated.

## Sources and novelty scope

* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the order-53/54
  connected-complement frontier.
* The preceding [four-form structural
  reduction](../albertson_r27_order53_h19_reduction/README.md), its
  [incidence pruning](../albertson_r27_h19_incidence_pruning/README.md), and
  the latest [implicit-edge
  closure](../albertson_r27_h19_implicit_edge_closure/README.md).

Targeted searches of the September 2026 paper, its cited critical-graph
sources, and the committed Discovery Net found no prior weighted-recolouring
closure of this boundary.  This is a search-relative novelty statement, not
a claim of historical priority.
