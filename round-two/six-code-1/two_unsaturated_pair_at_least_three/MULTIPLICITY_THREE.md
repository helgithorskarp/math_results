# A residual restriction at hub-pair multiplicity three

Actual author: **six-code-1, researcher**, 2026-10-01.

**Conditional structural theorem using the already published local inputs.**
Let `F` have71 five-subsets of eighteen points, intersections at most two,
and replication multiset `(16,19,20^16)`. Let `u,v` have replication16,19,
and assume `lambda_uv=3`. In the notation of [PROOF.md](PROOF.md), suppose
the saturated internal deficits are all zero or one (`X=0`), and none of
the points deficient to both hubs lies in the three common-word tails
(`c=|T intersect C|=0`). Then the shortened nineteen-block `v`-star
**must have an uncovered pair between replication-five points**.

Equivalently, at multiplicity three at least one of the three conditions
holds: an internal saturated deficit exceeds one; a both-hub-deficient
point lies in a common-word tail; or the nineteen-star has a low-low
leave edge. These alternatives are necessary, not asserted realizable.
This statement uses no new nineteen-star classification as a premise.

## A general nineteen-block subset identity

Let `Q` be any nineteen-quadruple pair packing on seventeen points.
Mark a point `u` of replication `q<=4`. Let `W` be all other deficient
points (replication below five), and put `p=|W|`. Let `mu` count
leave edges between replication-five points, and let `c_W` count points
of `W` sharing a covered pair with `u`. If `b_j` counts quadruples
containing exactly `j` points of `W`, then

```
b0+b3+3b4 = choose(p,2)-5p+17+q-mu-c_W.                 (1)
```

To prove it, the deficient set has size `p+1`, and its deficits sum9.
The leave-degree identity is `e-mu=p+6`. Its `u-W` leave has `p-c_W`
edges, so its `W-W` leave has `6+mu+c_W` edges. Consequently

```
sum_j j*b_j = 5p-4-q,
sum_j choose(j,2)*b_j = choose(p,2)-6-mu-c_W,
sum_j b_j = 19.
```

Subtracting the first identity from the other two gives (1), because
`1+choose(j,2)-j` is `1,0,0,1,3` for `j=0,...,4`.
In particular

```
5p+mu+c_W <= 17+q+choose(p,2).                          (2)
```

This is a direct incidence identity, without an imported classification.
The checker validates it on100 deficient marks across all20 single-line
deletions from the affine plane of order four with one unused point.
Those are positive controls, not complete nineteen-star coverage.

## Apply it to the three-common-word boundary

Assume for contradiction that the `v`-star has `mu=0` as well as `X=c=0`.
Its marked point `u` has replication three. The common-word tails have
size9. The published incidence identity8497 gives `Z subset C` and
residual homogeneous charge budget `R=3-z`. The saturated support graph
`G` has27 edges. Put `a_C=|A intersect C|`, `b_C=|B intersect C|`, and
`p=|B union T|<=7`.

The same covered-low-point charge from PROOF applies under the current
assumption `mu=0`, giving `a_C+2z<=3` and `b_C=9-a_C-z`.
The `W-W` leave count and (2), with `q=3,c_W=b_C`, give

```
6+b_C <= choose(p,2),      5p+b_C <=20+choose(p,2).       (3)
```

These constraints force

```
p=7,     z=0,     a_C=3,     b_C=6.
```

For completeness, `b_C>=6+z` gives `p>=6`. If `p=6`, the second
inequality gives `b_C<=5`, impossible. For `p=7` it gives `b_C<=6`,
forcing the displayed values. The three covered-low-point charges
exhaust `R=3`. Hence the saturated cohort `A`, of size9, has no
one-hub homogeneous incidence and is independent by exactly the
isolated-hub argument and the three published star-pair lemmas in PROOF.

Its degree sum `D` satisfies

```
D=5*9-19+w_u(T) >=26.
```

At every `A` center all its `g` high-leave edges have two saturated
neighbors, outside `A`, and yield `g` actual uncovered triples.
Thus the `A` centers require `D` uncovered triples on pairs of the
other seven saturated points. Those pairs have total uncovered capacity

```
choose(7,2)+3|E(G[V(G)\A])| =21+3*(27-D),
```

because every internal deficit is zero or one, and independent `A`
meets exactly `D` of the27 edges. Counting these triples by their
outside pair gives

```
D <=21+3*(27-D),        4D<=102.
```

This contradicts `D>=26`, proving the stated alternative.

## Scope and verification

The written incidence/capacity argument uses the reviewed universal20
link theorem, the existing two-unsaturated charge identity, and the
three published shared-isolated-hub incompatibilities cited in PROOF.
The new nineteen-star census is complementary and is **not** needed
for this conditional statement. All quantifiers, the conditions `X=c=0`,
and the no-low-low assumption are retained. No arbitrary multiplicity-
three code is excluded, and no global bound70 is claimed.

`verify.py --check` exhausts the small integer inventory (3), checks
the exact capacity contradiction `104>102`, and checks (1) on the
explicit positive controls. Imported local proofs and ordinary bridges
are separate trust boundaries. No independent review or formalization
of this transfer is asserted.
