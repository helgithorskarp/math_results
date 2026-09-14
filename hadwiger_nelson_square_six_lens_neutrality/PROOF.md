# Exact proof

Put `q=3^(1/4)` and `s=sqrt(2)`.  The field implementation uses the basis

```text
1,q,q^2,q^3,s,sq,sq^2,sq^3
```

and reduces products with `q^4=3` and `s^2=2`.  Let

```text
a  = s(q^2-1)/2,
h  = s(q^2+1)/4.
```

Direct reduction gives `a^2=2-q^2` and `h^2=1-a^2/4`.  Hence the four points
with coordinates `(+-a/2,+-a/2)` form the required square and the side-pair
lens offsets have height `h`.  For a diagonal centre pair, its separation is
`as` and the perpendicular coordinate offset of either unit-circle
intersection is `q/2`, since

```text
(as/2)^2 + (q/s)^2 = a^2/2 + q^2/2 = 1.
```

These formulas give exactly the 16 listed addresses.  Equality in the field
basis proves they are distinct.  Testing the squared norm of each of their 120
differences gives exactly the 28 certified edges.  In particular
`h-a/2=s/2`, so the four inward side-lens points lie at the four axis points
of radius `s/2`; consecutive ones are one unit apart.

The certified word is a proper three-colouring of every reconstructed edge.
The reconstructed edges on vertices `0,4,9` form a triangle, proving the
matching lower bound three.

The four terminals are vertices `0,1,2,3`.  Their six squared distances are
either `a^2` or `2a^2`, neither equal to one in the field basis, so their bare
graph is empty.  There are exactly 15 set partitions of four labelled
positions, represented by the restricted-growth words in the certificate.
For every word the listed 16-symbol four-colouring is proper on all 28 edges
and restricts to that terminal word.  Any of the 256 named terminal
assignments has one of those equality patterns; extending the induced
injection of used colours to a permutation of the four-colour palette and
applying it to the certified word gives a proper extension.  Therefore all
256 assignments extend and the unrestricted interface is neutral.
