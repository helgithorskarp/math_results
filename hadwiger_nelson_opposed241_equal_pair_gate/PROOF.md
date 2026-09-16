# Proof obligations

## Reconstruction

The archived B214 table is hash-pinned.  Its sparse 16-coefficient rows reduce
to the four integer coefficients used here.  The verifier constructs the ten
Golomb points, the left image `(x,y)->(x-1/2,y)`, and the right image
`(x,y)->(-x+1/2,y)`, retaining each physical coordinate at first occurrence.
The frozen source labels in `certificate.json` select 241 points.

Independence of `1,sqrt(33)` on each real coefficient and of
`sqrt(3),sqrt(11)` on the imaginary coefficient makes tuple equality exact.
Expanding a squared norm gives the two integer unit equations in the README.
Testing all unordered pairs therefore reconstructs the complete strict graph.

## Pair separation

Let `f_1,...,f_8` be the submitted colour words.  The verifier first checks
that every `f_i` is a proper four-colouring of the complete graph.  It then
checks that the map

```text
v -> (f_1(v),...,f_8(v))
```

is injective.  Hence for any distinct vertices `u,v`, at least one checked
proper four-colouring has `f_i(u) != f_i(v)`.  Thus no pair is forced equal.

If an induced subgraph retains `u,v`, restrict that same word to its retained
vertices.  It remains proper and still separates the pair, proving the
induced-subgraph corollary.

## Why this ends the declared spindle route

For completeness, suppose a graph did force equal colours at distinct points
`p,q`, and put `s=|p-q|^2 >= 1/4`.  The unit complex number

```text
r = 1 - 1/(2s) + i*sqrt(4s-1)/(2s)
```

satisfies `s*|1-r|^2=1`.  Rotate a second copy about `p` by `r`.  Its image of
`q` is unit distance from the first `q`, while both copies force those two
points to have the colour of `p`; no four-colouring exists.  The union has at
most `2n-1` physical points.  At `n=241` this would be at most 481.

The certificate rules out the premise for every pair, including all 27,010
pairs with squared distance greater than `1/4`.  It therefore ends this
specific source/bridge architecture before a physical union is constructed.

## Evidence boundary

The result uses only positive colour words.  The discovery solver's status is
not trusted.  The earlier conditional Golomb-word obstruction is not a proof
premise, although it motivates testing this unusually selective compact core.
The theorem does not assert equal-colour witnesses for every nonedge and does
not classify higher-arity colour relations.
