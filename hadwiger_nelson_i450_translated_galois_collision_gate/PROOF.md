# Proof and exact scope

An I450 coordinate row `(a,b,c,d)` represents

```text
((a*sqrt(3)+b*sqrt(11))/36, (c+d*sqrt(33))/36).
```

The marked rows are `O=(0,0,0,0)` and `V=(0,0,0,12)`.  Translate every
source row by

```text
h=(0,0,0,-6).
```

For signs `s3,s11` in `{+1,-1}`, let

```text
sigma_s3,s11(a,b,c,d)=(s3*a,s11*b,c,s3*s11*d).
```

These are the four real embeddings of `Q(sqrt(3),sqrt(11))`.  A proposed
pointwise image chooses one embedding independently at every source vertex
and maps `p` to `sigma(p+h)`.

For a row difference `(a,b,c,d)`, the exact squared distance is encoded by

```text
(3*a^2+11*b^2+c^2+33*d^2, 2*(a*b+c*d))/1296.
```

Thus distance one is exactly the coefficient pair `(1296,0)`.  A common
embedding preserves every source unit edge.  Mixed embeddings need not, so
the checker evaluates all 16 ordered state pairs for each edge.

After translation, `O` and `V` have rows `(0,0,0,-6)` and `(0,0,0,6)`.
Their images coincide precisely when the products `s3*s11` of their two
states have opposite signs.  This gives eight ordered collision state pairs.

Now restrict to the exact source path `0--10--16--1`.  In state order

```text
(+,+), (-,+), (+,-), (-,-),
```

the allowed ordered state pairs on each outer edge are

```text
00 03 11 12 21 22 30 33,
```

while the middle edge permits only

```text
00 11 22 33.
```

Exhausting the 256 four-state words leaves 16 that preserve all three edges.
Every one has endpoint sign products equal, whereas endpoint collision needs
them opposite.  Therefore none identifies `O,V`.  Any map preserving every
I450 edge would restrict to one of these path maps, proving the theorem.

The verifier additionally reconstructs the complete 450-point, 2,290-edge
source graph from all 101,025 point pairs.  Across its edges, 1,860 have four
allowed embedding pairs, 385 have eight, and 45 have all sixteen.  These
counts are validation context; the four-vertex path is the complete proof.

I450's separately published terminal relation makes an identifying map
construction-relevant: a four-colouring of the physical image would pull
back to a forbidden equal-endpoint four-colouring of I450.  This package does
not reprove that relation, produce an image, or claim any obstruction outside
the fixed translation and four pointwise embeddings.
