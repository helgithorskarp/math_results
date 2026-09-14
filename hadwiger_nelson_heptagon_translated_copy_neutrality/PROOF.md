# Proof and certification scope

Let `t=exp(pi*i/21)`.  In `Q(t)` use the 21 points

```text
P_j = t^(6j)/(t^24-t^(-24))
Q_j = -t^(6j-7)/(t^6-t^(-6))
R_j = -t^(6j+7)/(t^12-t^(-12)),       0 <= j < 7.
```

They are ordered `P_0,...,P_6,Q_0,...,Q_6,R_0,...,R_6` and form the
Haugland motif `H`.  Fix `h_0=P_0` and the rotation `r=t^(-6)`.  The second
component is

```text
H' = {h_0 + r*(h-h_0) : h in H}.
```

Because multiplication by `r` shifts each sevenfold ring, the same set can
also be written `H+(h_0-h_6)`.  Thus the declared construction is both a
rotation of one component about a shared point and a translation of its
unlabelled support.  No numerical angle or coordinate is part of its
definition.

## Exact physical graph

The primary checker represents `Q(t)` on the power basis modulo

```text
t^12+t^11-t^9-t^8+t^6-t^4-t^3+t+1.
```

It constructs all 42 formal addresses, merges exact coordinate equality and
scans all 820 unordered physical pairs using
`(x-y)*conjugate(x-y)=1`.  Exactly the two addresses for `h_0` coincide.
The quotient therefore has 41 points and 105 unit edges.  The two factor
graphs contribute 84 distinct edge images and the scan finds 21 further
unit edges.  Hence the edge set is the complete strict physical unit graph,
not a prescribed abstract graph.

The independent audit works instead in the tensor basis
`Q(zeta_7,omega_6)`, using `t=zeta_7^6*omega_6`.  It reconstructs the seed
from geometric-series inverse identities, obtains the same collision classes
and the same complete edge stream, and uses no producer import or modular
distance filter.

## Complete component relation

Labels 0, 7 and 14 form a unit triangle in each component.  Every proper
four-colouring can therefore be renamed uniquely so that these labels have
colours `0,1,2`.  The primary search recursively enumerates every proper
normalized colouring of one component and obtains exactly 327,180 patterns.
For each pattern it separately pins all 21 vertices of `H` and then all 21
vertices of `H'`, for 654,360 projection queries.  It searches the remaining
vertices of the 41-point physical graph in fixed physical-label order.  Every
query returns a proper extension, checked on all 105 edges and against every
pin.  Hashes of the reconstructed full words make the deterministic result
stable.

The alternate checker enumerates the same normalized patterns in fixed label
order rather than the primary minimum-domain order and independently implements
the physical-label extension.  It again obtains 327,180 positive extensions in
each direction and hashes its different witness streams separately.  Colour
renaming then proves the unrestricted statement: every named proper
four-colouring of either component extends to the union.

Both checkers also test every physical pair.  Each of the 715 nonedges has one
proper colouring with equal endpoint colours and another with different
endpoint colours.  The 105 unit pairs necessarily allow only the different
state.  This pair result is not used to infer the stronger component theorem;
the complete component projection is checked directly.

Finally, an exhaustive `6^6=46,656` normalized three-colour census shows that
`H` has no proper three-colouring.  Since an explicit four-colouring occurs
among the extension witnesses, both `H` and the union have chromatic number
exactly four.

## Consequence and limitation

Adjoining this translated/rotated copy cannot strengthen any host relation
carried solely by the retained `H'` component: every four-colouring on that
component still extends.  All induced subgraphs are also four-colourable.
This closes only the displayed 41-point support.  It does not classify other
centres, rotations, translations, additional components, or hosts.  In
particular it is a restricted-family exclusion, not a five-chromatic graph,
not a lower bound for arbitrary unit-distance graphs, and not an improvement
on the 509-vertex record.
