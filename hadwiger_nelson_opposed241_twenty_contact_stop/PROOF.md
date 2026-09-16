# Proof and trust boundary

## Exact coordinate field

Put `r=sqrt(33)` and `K=Q(r)`. Every source point has the form
`(X,sqrt(3)Y)` with `X,Y in K`. Put

```text
T=(2+2r)/3,  t=sqrt(T)>0.
```

The quadratic norm of `T` is `-128/9`. If `T=z^2` for `z in K`, then
`Norm(T)=Norm(z)^2` would be nonnegative. Thus `T` is not a square and the
checker may compare coefficients in `L=K+Kt`.

For two source vectors `p,q`, write

```text
D = p dot q,
sqrt(3) J = cross(q,p),
C = (|p|^2+|q|^2-1)/2.
```

Solving `D cos(theta)+sqrt(3)J sin(theta)=C` together with unit norm gives
the two contact rotations. For source indices 45 and 65, the selected branch
has exactly the coefficients displayed in the README, and its discriminant
satisfies `3(D^2+3J^2-C^2)=T`. The verifier repeats these calculations over
`K` and checks `cos(theta)^2+sin(theta)^2=1` over `L`.

Rotation acts on coefficient pairs by

```text
(X,Y) -> (cos(theta) X - 3 (sin(theta)/sqrt(3)) Y,
          (sin(theta)/sqrt(3)) X + cos(theta) Y).
```

All collision and squared-distance decisions are therefore coefficientwise
equalities in the faithful basis `1,r,t,rt` (and `sqrt(3)` times that basis
for the second coordinate).

## Complete graph and colouring

The two 241-point images meet only at the origin, so their union has 481
points. Directly evaluating all unordered pairs yields 2,002 unit edges. Of
these, 991 lie in each copy and 20 join private vertices in different copies.
The stored list of 20 cross edges, canonical point hash, and canonical edge
hash are all checked after reconstruction.

The 481-symbol word in `certificate.json` differs across every one of those
2,002 edges. This proves four-colourability. The first ten source points form
the 18-edge Golomb graph. Fixing its triangle to colours `0,1,2` and exhausting
the remaining `3^7` assignments gives no proper three-colouring. Hence the
union has chromatic number exactly four.

Tarjan's algorithm finds no articulation or bridge. Iterative deletion of
vertices of current degree at most three deletes none; the full graph is its
four-core. These facts show that the failed coupling is not a one-point or
single-bridge decomposition, but they are not used to infer chromaticity.

## Trust and limitations

The conclusion trusts the hash-pinned source transcription, exact rational
arithmetic, the small checker, the displayed reduction from coordinates to
field coefficients, CPython, and ordinary hardware. It does not trust a SAT
UNSAT result, floating-point root, or omitted edge list. The source's earlier
conditional nonextension theorem is context rather than a premise of this
four-colour stop.

Only the frozen relative placement is decided. No statement is made about a
continuous rotation family or any other opposed-core composition.
