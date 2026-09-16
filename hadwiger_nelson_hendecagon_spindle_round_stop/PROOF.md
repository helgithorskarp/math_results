# Proof/certificate outline

Let `q` denote a primitive 66th root of unity and put `zeta=q^6` and
`omega=q^11`.  Thus `zeta` is a primitive 11th root and `omega=exp(pi*i/3)`.
The verifier represents `Q(q)` exactly in the power basis modulo

```text
x^20+x^19-x^17-x^16+x^14+x^13-x^11-x^10-x^9
     +x^7+x^6-x^4-x^3+x+1.
```

The unit-side hendecagon is `p_0=0` and
`p_k=sum_{j=0}^{k-1} zeta^j`.  In this frame its circumcentre is
`O=-sum_{k=0}^{10} k*zeta^k/11`, since
`(zeta-1)sum k*zeta^k=11`.  The remaining source coordinates are the exact
affine translation of Shibuya's formulas.  The common-neighbour coefficient
used there is `(1+omega)/3`; the relevant anchor distance is `sqrt(3)`.

The full object consists of the hendecagon, two auxiliary addresses, and all
images `O+zeta^(-4k)(s-O)`, `0<=k<11`, of each of the seven spindle points.
Dictionary equality in `Q(q)` merges two duplicated auxiliary/spindle
addresses.  For every distinct pair `x,y`, the verifier inserts an edge if
and only if `(x-y)conjugate(x-y)=1` in `Q(q)`.  This proves the 88-point,
187-edge complete physical graph census without numerical thresholds.

The distinguished spindle induces 11 edges.  Exhaustive DSATUR rejects three
colours and finds four.  Restricted-growth enumeration gives 16 canonical
complete four-colourings.  For every one, `certificate.json` supplies a
proper colouring of all 88 vertices restricting to that word.  Direct edge
checking establishes all 16 extensions.  Hence the complete graph contains a
four-chromatic subgraph and is itself four-colourable, so its chromatic number
is exactly four and its source projection is unchanged.

