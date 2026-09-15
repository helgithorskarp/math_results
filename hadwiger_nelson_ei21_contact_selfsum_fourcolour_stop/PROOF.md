# Proof certificate

## 1. Isolating the 21-point contact

Fix `p_0=(0,0)` and `p_1=(0,-1)`.  The certificate lists 38 source edges and
the new edge `(0,14)`.  Removing the fixed edge `(0,1)` leaves 38 squared-unit
equations in the 38 Cartesian coordinates of the other 19 points.

Let `x_0` be the rational midpoint in `geometry_certificate.json`, let `F` be
this vector of equations, and let `Y` be the rational approximate inverse of
`DF(x_0)`.  The verifier computes exactly

```text
beta = ||I-Y DF(x_0)||_infinity
B    = ||Y||_infinity
eta  = beta + 16 r B
delta = ||Y F(x_0)||_infinity + eta r,
```

where `r=10^-25`.  If two points move coordinatewise by at most `r`, every
difference coordinate moves by at most `2r`, each corresponding Jacobian
entry by at most `4r`, and a squared-distance row has at most four nonzero
entries.  Hence `||DF(x)-DF(x_0)||_infinity <= 16r` throughout the box.
The exact inequalities `eta<1` and `delta<r` make
`T(x)=x-YF(x)` a contraction from the closed box to itself.  Banach's theorem
therefore gives a unique exact zero in the box.

For every one of the 210 point pairs, the verifier bounds squared-distance
error by

```text
4 r (|dx|+|dy|) + 8 r^2.
```

All distinct points are separated, and every pair outside the 39 constrained
edges is separated from squared distance one.  Thus the exact root has 21
distinct points and its complete strict unit graph has exactly 39 edges.

## 2. Chromatic and source-loss checks

A deterministic exhaustive DSATUR search visits 953 nodes and finds no proper
three-colouring of the 38-edge source.  The contact certificate includes:

- a proper source four-colouring in which vertices `0` and `14` have the same
  colour, so the newly realized edge destroys that complete source colouring;
- a proper four-colouring of all 39 edges, so the contact graph remains
  four-colourable.

The verifier also deletes each vertex and each edge in turn from the
connectivity calculation.  The 39-edge graph has no articulation vertex and no
bridge.  The restriction is therefore not explained by a one-vertex or bridge
attachment.

## 3. Complete commutative self-sum

For every unordered address `(i,j)`, take the rational midpoint
`m_i+m_j`.  The exact sum coordinate differs from it by at most `2r`.  Two sum
addresses therefore have difference-coordinate error at most `4r`; if their
rational midpoint difference is `(dx,dy)`, their exact squared-distance error
is at most

```text
8 r (|dx|+|dy|) + 32 r^2.
```

The verifier checks all `C(231,2)=26,565` address pairs.  It joins addresses
whose coordinate boxes can overlap and takes connected components, obtaining
210 possible-equality clusters.  No exact equality can cross two clusters, and
no two addresses within a cluster can be unit distance.  Between different
clusters it inserts an edge whenever the squared-distance interval contains
one.  The resulting conservative graph has 731 edges and contains every unit
pair that the exact physical support can have.

The certificate's 210-character word is a proper four-colouring of that
conservative graph.  Give every exact address the colour of its cluster.  This
is well defined on collisions and separates every actual unit pair, proving
that the complete strict graph on `P+P` is four-colourable.

Finally, the 21 addresses `(0,i)` lie in distinct clusters and form the exact
translated copy `p_0+P`, including every edge of the four-chromatic contact
source.  Hence the complete actual self-sum graph has chromatic number exactly
four.

## 4. Scope

The proof concerns one isolated EI21 contact and its full commutative
self-sum.  It proves neither the exact physical order nor exact physical edge
count of the self-sum: only `210 <= |P+P| <= 231` and a 731-edge conservative
supergraph are claimed.  It does not exclude other EI21 contacts or unrelated
whole-support operations.  It supplies no five-chromatic graph.
