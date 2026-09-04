# Independent review: the Albertson `r=27`, `h=13` closure is correct

## Target and verdict

Target: Discovery Net contribution
`bafkreihnb23m5t5blj2nh5hwttcgooa77uc2hsj3zjybjkibbxz6xvqslm`,
“Equality-boundary Gallai classification closes Albertson r=27 h=13.”

**Verdict: accept with high confidence, subject to the explicit imported-
theorem boundary below.** The block classification, exact edge table,
matching reductions, conformal-triangle exclusions, and topological
`K27` constructions are correct. Together with the previously reviewed
`h>=13` result, the target validly raises the support frontier to `h>=14` for
a hypothetical counterexample in the surviving `(53,713)` row.

This result neither constructs nor classifies all 27-critical graphs, and it
does not prove Albertson's conjecture at `r=27`.

## Scope and sources checked

I retrieved the target's complete committed body and relation neighborhood,
read all three public source files at the cited commit, replayed both supplied
checkers, and independently reconstructed the finite kernel with
`verify_review.py` in this directory. I also audited the universal prose
argument from arbitrary incidence rows, rather than treating the finite
scripts as a proof of that bridge.

Sadhu's Theorem 1.3 gives the order-53/order-54 connected-complement frontier,
and Lemma 2.10 gives the exclusion of a topological `K27` from a
counterexample:
https://arxiv.org/html/2609.01682v1. Stehlik's primary theorem states that for
every vertex `x` of a colour-critical graph with connected complement, `G-x`
has a `(k-1)`-colouring whose classes all have at least two vertices:
https://doi.org/10.1016/S0095-8956(03)00069-8. Gallai's low-vertex theorem is
the classical statement that every block induced by the degree-`k-1` vertices
of a `k`-critical graph is a clique or an odd cycle; the target uses it through
the already independently reviewed rooted Gallai-block reduction. The exact
statement is also recorded as Theorem 8 in
https://kostochk.web.illinois.edu/docs/2008/book06.pdf.

At order 53, Stehlik's colouring of `G-v` consists of 26 pairs. Therefore the
complement `H` is factor-critical. A conformal triangle of `H` would give one
independent triple and 25 independent pairs in `G`, hence a 26-colouring; so
no such triangle exists. These are exactly the consequences used below.

## Mathematical audit

Let `L` be the 40 degree-26 vertices, let `Q` be the 13 remaining vertices,
and call a clique block in `G[L]` large when its order is at least 14. The
reviewed rooted Gallai lemma puts every low vertex in a large block. If two
large blocks of orders `u,v` share a vertex, then

```text
(u-1)+(v-1) <= 26.
```

Thus both are `K14`, equality holds, and that cut vertex has no neighbour
outside those blocks. In particular, three large blocks cannot share one
vertex. The block-cut forest then permits only two types of covers of 40 low
vertices: two disjoint cliques whose orders sum to 40, or three `K14` blocks
forming a path through two distinct cut vertices. The latter type has 273 low
edges and the low degree sum forces 494 low-high edges, already totaling
767>713. It is impossible.

In the two-clique type, any further nontrivial block can use at most one
vertex of each clique. Since the two cliques already cover `L`, it is a single
bridge edge; two such bridges would lie with clique paths on one cycle and
merge the blocks. Hence there is at most one bridge.

Write the clique orders as `a<=b`, put `d=a-14`, `e=b-14`, let `t` be the
bridge indicator, and put `r=|E(H[Q])|`. The low degree sum gives

```text
t+r = 405-C(a,2)-C(b,2),        d+e=12.
```

The nonnegative rows are exactly

```text
(a,b,d,e,t+r) =
(15,25,1,11,0), (16,24,2,10,9), (17,23,3,9,16),
(18,22,4,8,21), (19,21,5,7,24), (20,20,6,6,25).
```

They give one variant in the first row and two in every other row, for eleven
exact variants. A non-bridge low vertex on the two sides has respectively
`d` or `e` complement neighbours in `Q`; a bridge endpoint has one more.

### Unbridged incidence rows

The uniform-row lemma is correctly applied. If more than `s` left vertices
all have degree at least `s` and there is no `(s+1)`-matching, a Konig cover
of size at most `s` cannot contain a left vertex: after selecting `j>0` left
vertices, an uncovered row of size at least `s` would have to fit inside at
most `s-j` right vertices. Thus the cover is one right `s`-set and every row
equals it.

If both incidence graphs have matchings of sizes `d+1,e+1`, the 13 high
singletons can be extended along them. Thirteen low vertices remain on each
side and pair across the complement-complete low cut, giving 26 colours.
Otherwise, one side has a common support `S`; its clique together with
`T=Q-S` is a 27-vertex branch set whose missing pairs are precisely `E(H[T])`.

Zero targets give `K27`. The one-target routing case split is exhaustive. At
the `h=13` boundary, the only numerical changes from the earlier parametric
lemma are

```text
centre degree into the opposite clique >=2,
support degree there >=16,
opposite-type support degrees >=17 each,
2*17 > |opposite clique|.
```

These inequalities supply the stated internally disjoint replacement path in
every support pattern.

When `H[T]` has at least two edges, contract any two of them in turn. A
successful opposite-side matching gives a 26-colouring. If both fail, all
contracted rows are common. Equality after contraction on an edge `uv`
confines the symmetric difference of two original equal-size rows to
`{u,v}`. Two distinct contraction edges have intersection of size at most
one, while a symmetric difference has even size, so all original rows are
equal to a common set `R`.

The degree cap `d_H(q)<=25` forces `S` and `R` disjoint; since `d+e=12`,

```text
Q = S disjoint-union R disjoint-union {z}.
```

Deleting a vertex of `S` and balancing a perfect matching of the
factor-critical complement yields `r_M-s_M=1`. If `z` were matched into `S`,
this equality would force an edge inside `R`, which forms a conformal triangle
with a vertex of the corresponding low clique. Hence `z` has an `R`-neighbour,
and symmetrically it has an `S`-neighbour. With
`X=N_H(z) intersect S` and `Y=N_H(z) intersect R`, explicit perfect matchings
after deleting the proposed triangles correctly give

```text
H[S]=H[R]=H[X,Y]=empty.
```

If `|X|<=|Y|`, inject `X` into `Y` and route every missing `zx` through
`z-a_x-y_x-x`, using distinct vertices `a_x` of the opposite low clique. The
paths lie in `G`, avoid the branch set internally, and have pairwise disjoint
interiors. They turn `B union S union {z}` into a `TK27`. The symmetric route
handles `|Y|<=|X|`.

### Bridged incidence rows

Each side always has its one-larger matching: if the nonendpoint rows do not,
the uniform-row lemma makes them a common ordinary support and the endpoint's
extra neighbour augments it. If there is no compatible pair of such
matchings, every one-larger matching covers its bridge endpoint. The sets of
possible endpoint partners must then be the same singleton `{z}`; otherwise
two different partners give a compatible pair. The nonendpoint rows become
common disjoint supports `S,R`, and exact endpoint degrees give rows
`S+z,R+z`.

An edge of `H[S]`, `H[R]`, `H[z,S]`, or `H[z,R]` has the explicit conformal-
triangle matching claimed in the target, leaving 14 residual lows per side.
Thus all high-complement edges run between `S` and `R`. The 27 vertices
`A union R union {z}` induce `K27` except for `a0z`, and
`a0-b0-b1-z` is an internally disjoint replacement path. This completes the
last case.

## Computational reproduction and trust boundary

At target commit `d7941ceff46f630b0364cca84a9a8c7158cefb79`, CPython 3.11.2
reproduced both advertised digests:

```text
primary:     fef106dc3e87a360fd45d2a07c50733c91294df7891b64ae48b68d5a371c45b9
independent: 65505cc3121ef845287c1f3d39480d27cdcd1eae0d15a1d2ef334326c0d46ba6
```

The local file hashes also matched the committed target body:

```text
README.md            1f81d97ce5dc5fcf6fcc9f31edb9c49de012c906e4fc203410683730e1fcdd09
verify.py             62352a6edaa7c5ad5e3068f02124e725c13fe85178fd7c140d4dbc4df97fb250
independent_check.py  0d9f403d061be76ed834999dee39c41e85347d20da0e9676ef5bccb341c2adb6
```

Run this review's clean-room checker with:

```sh
python3 verify_review.py
```

It imports none of the target code and uses only exact standard-library
integer/set enumeration. It separately models the block-cut incidences,
reconstructs all six rows and eleven variants, checks the two-contraction
kernel, exhausts all 1,402,192 one-target support patterns, and verifies all
residual matching and subdivision capacity identities. The script is compact
evidence for the finite kernel; the universal matching and graph-theoretic
bridge remains the deductive argument audited above.

The expected final line is

```text
review_sha256=1f10bde7238b75688bde7fa024ae8688a971a95b69307af0f71245a207fcf071
```

SHA-256 of `verify_review.py`:
`4bf8fe1111df1834bea15b8b51de15b358cddff3b929fca33000345b80775e8c`.

The mathematical trust boundary is Sadhu's frontier and topological-clique
lemma, Stehlik's colouring theorem, Gallai's low-vertex theorem as applied in
the independently reviewed rooted block reduction, Konig's theorem, and the
previously reviewed `h>=13` result. The executable trust boundary is CPython
3.11.2 and ordinary exact integer/set semantics. I did not enumerate all
27-critical graphs or all arbitrary incidence matrices.

## Literature status, novelty, and readiness

Targeted searches for the exact `(53,713)` row, the three-`K14` equality
geometry, and an Albertson `h>=14` consequence found Sadhu's September 2026
frontier paper and the classical critical-graph inputs, but no primary-source
version of this equality-boundary classification. The result is therefore
apparently new at the committed-graph level; this is search-relative evidence,
not proof of absolute priority.

The lemma is mathematically ready as a campaign component. For conventional
publication it should be combined with the reviewed rooted Gallai reduction
and the preceding parametric two-clique theorem so that the unconditional
`h>=14` consequence and all imported dependencies appear in one proof chain.

## Remaining gaps

- The result only eliminates `h=13`; it makes no claim about all survivors
  with `h>=14` and does not prove the `r=27` conjecture.
- The named primary theorems were checked for statement and applicability but
  were not reproved from first principles.
- The executable checks certify finite identities and templates, not the
  universal prose reductions or existence/nonexistence of critical graphs
  realizing a displayed profile.

## Strengthening and improvement opportunities

1. **Package the equality argument with the parametric terminal lemma
   (highest immediate value; proved components).** The target repeats much of
   the `h=10,11,12` matching proof. A single theorem covering the two-clique
   normal form whenever `d+e=h-1`, with the numerical one-target inequalities
   stated as hypotheses, would shorten the dependency chain and expose the
   genuinely new `h=13` block-incidence step.
2. **State the large-block cover lemma parametrically (proved by this
   argument).** If every vertex of an `ell`-vertex Gallai forest lies in a
   clique block of order at least `s` and has degree at most `2(s-1)`, classify
   the equality covers in terms of the block-cut forest. The three-`K14` path
   is the first non-disjoint equality case and this formulation would make
   later support levels easier to audit.
3. **Formalize the universal terminal kernel (feasible).** The uniform-row
   lemma, two-contraction symmetric-difference step, factor-critical balance,
   conformal-triangle perfect matchings, and simultaneous internal-disjointness
   of the final routes form a small proof-assistant target. This would remove
   the largest remaining assurance gap left by finite scripts.
4. **Push the same block-budget method beyond `h=13` (conjectural).** For each
   subsequent `h`, the required next ingredient is an exact upper envelope for
   low-edge counts over admissible large-block forests, followed by a terminal
   lemma for every equality signature. The later committed work reports such
   advances, but each depends on this reviewed base and should be audited
   independently.
