# A local-extremal deficiency constraint for a hypothetical `R(5,5;43)` graph

Every red/blue coloring of `K_43` with no monochromatic `K_5`, if one exists,
must contain a color-neighborhood whose induced `(4,5)`-Ramsey graph is within
seven edges of the maximum possible edge count for its order.  More precisely,
one of its 86 vertex-and-color neighborhoods has order `k` and at least

```text
k                 18  19  20  21  22  23  24
maximum U(k)      85  92 100 107 114 122 132
forced threshold  78  85  93 100 107 115 125
```

edges.  This gives a finite local-core frontier for construction or exclusion
searches that is independent of the Cyclic(43) perturbation landscape.

There is a sharper dichotomy.  Either some color-neighborhood is within six
edges of its maximum, or at least 66 of the 86 color-neighborhoods have
**exactly** seven fewer edges than their order-specific maxima.  In the second
case the degree sequence is strongly concentrated around 21 in the precise
weighted sense proved below.  Up to exchanging the two colors, only 104
integer degree-count profiles survive that hard branch, and the sparser color
has between 445 and 451 edges.  Thus either a six-deficient local core exists,
or the two global color classes differ in size by at most 13 edges while the
66-fold exact-level-seven conclusion holds.

This is a necessary condition, not a construction of a 43-vertex Ramsey graph
and not an exclusion of all such graphs.

## Local Ramsey graphs

Suppose `G` has 43 vertices with neither a clique nor an independent set of
size five.  For a vertex `v` of red degree `d(v)`, define two local graphs:

```text
H_(v,R) = G[N_G(v)],
H_(v,B) = complement(G)[N_complement(G)(v)].
```

Both have no `K_4` and no independent five-set.  A `K_4` in either graph,
together with `v`, would make a monochromatic `K_5`; an independent five-set
would already be forbidden globally.  The exact equality `R(4,5)=25` therefore
implies

```text
18 <= d(v) <= 24,
```

because the orders of the two local graphs are `d(v)` and `42-d(v)`.

Let `U(k)` be the maximum number of edges in a `(4,5)`-Ramsey graph on `k`
vertices.  The displayed values for orders 18 through 24 come from the
complete McKay-hosted catalogs described under provenance below.  Define the
two nonnegative integer deficiencies

```text
delta_(v,R) = U(d(v))    - |E(H_(v,R))|,
delta_(v,B) = U(42-d(v)) - |E(H_(v,B))|,
```

and let `Delta` be their sum over all vertices and both colors.

## Exact deficiency identity

Write `x_d` for the number of vertices of red degree `d`.  Then

```text
2 Delta = 8 (x_18+x_24)
        + 17(x_19+x_23)
        + 26(x_20+x_22)
        + 29 x_21.                                      (1)
```

Equivalently, since the seven degree counts sum to 43,

```text
2 Delta = 1247
        - 21(x_18+x_24)
        - 12(x_19+x_23)
        -  3(x_20+x_22).                                (2)
```

To prove (1), let `T_R` and `T_B` be the numbers of red and blue triangles.
Each triangle is counted once at each of its three vertices, so

```text
sum_v |E(H_(v,R))| = 3 T_R,
sum_v |E(H_(v,B))| = 3 T_B.
```

Goodman's elementary mixed-wedge count gives

```text
T_R + T_B = binom(43,3)
            - (1/2) sum_v d(v)(42-d(v)).
```

Substitution into the definition of `Delta`, followed by
`3 binom(43,3)/43=861`, says that a degree-`d` vertex contributes

```text
2(U(d)+U(42-d)) - 2*861 + 3d(42-d)
```

to `2 Delta`.  Inserting the seven exact values of `U` gives respectively

```text
8, 17, 26, 29, 26, 17, 8,
```

which proves both displayed identities.

## The seven-edge localization theorem

The handshaking lemma says that the number of odd-degree vertices is even.
There are 43 vertices, so at least one degree is even.  Every coefficient in
(1) is at most 29, while an even degree has coefficient at most 26.  Hence

```text
2 Delta <= 42*29 + 26 = 1244,
Delta <= 622.                                           (3)
```

The 86 local deficiencies are nonnegative integers.  If all were at least
eight, their sum would be at least 688, contradicting (3).  Thus some
`delta_(v,color)` is at most seven, proving the threshold table.

If no deficiency is at most six, all 86 are at least seven and their baseline
sum is `86*7=602`.  At most 20 units remain before the upper bound 622.  Every
deficiency greater than seven consumes at least one of those units, so at
least `86-20=66` deficiencies equal seven exactly.  Moreover, (2) and
`Delta>=602` first give the hard-case degree constraint

```text
21(x_18+x_24) + 12(x_19+x_23) + 3(x_20+x_22) <= 43.     (4)
```

The left side of (4) is divisible by three.  It is also odd, because by (2)
it equals the odd number `1247-2 Delta`.  It is therefore at most 39, not
merely 43.  In particular, every hard-case coloring satisfies

```text
Delta >= (1247-39)/2 = 604.                            (5)
```

Equations (3) and (4), together with handshaking parity, are compact durable
constraints for a construction encoding.  For example, (4) immediately
allows at most two degree-18-or-24 vertices and at most three
degree-19-or-23 vertices, with the joint weighted budget being the stronger
statement.  After possibly exchanging red and blue, assume that red has at
most 451 edges, or equivalently that the degree sum is at most 902.  Direct
enumeration of nonnegative integer counts `x_18,...,x_24` subject to their sum
being 43, this normalization, handshaking parity, and the sharpened
weight-at-most-39 constraint leaves exactly 104 profiles.  Their degree sums
range from 890 to 902.  These are necessary integer profiles, not an assertion
that all 104 are realizable Ramsey graphs.  Dividing those degree sums by two
shows that the sparser color has exactly one of 445, 446, ..., 451 edges.  Since
`K_43` has 903 edges, the two color-class sizes differ by at most 13.

## Reproduction

The standard-library verifier checks the extrema manifest, derives every
coefficient in (1), and uses a dynamic program over all 43-term degree lists
to confirm that 1244 is the largest possible value of `2 Delta` subject to
handshaking parity.  It then checks the dichotomy arithmetic, sharpens (4) to
39, and enumerates the 104 complement-normalized hard-case degree profiles.

```bash
python3 verify_deficiency.py | cmp - EXPECTED_OUTPUT.txt
```

Expected output is

```text
PASS exact R(4,5;k) maxima pinned for k=18,...,24
PASS twice-deficiency coefficients=18:8,19:17,20:26,21:29,22:26,23:17,24:8
PASS total local deficiency <=622 over 86 color-neighborhoods
PASS either one deficiency <=6 or at least 66 deficiencies equal 7
PASS hard-case degree weight <=39 and deficiency >=604
PASS hard-case complement-normalized degree-count profiles=104
PASS hard-case sparser color has 445,...,451 edges
```

An optional upstream-data audit checks both pinned SHA-256 values, verifies
that the maximum-edge files for orders 18 through 23 contain graphs of their
declared orders and edge counts, and scans all 352,366 order-24 graphs to
recover maximum 132 and its two witnesses:

```bash
curl -LO https://users.cecs.anu.edu.au/~bdm/data/r45extreme.tar.gz
curl -LO https://users.cecs.anu.edu.au/~bdm/data/r45_24.g6
python3 verify_deficiency.py \
  --extreme-archive r45extreme.tar.gz \
  --order24-catalog r45_24.g6
```

The optional audit adds

```text
PASS pinned upstream catalogs and graph6 extrema
```

No third-party package, randomness, solver, or floating point is used.  The
default check takes substantially less than one second; the optional audit is
linear in about 108 MB of upstream compressed/catalog data.

## Provenance and trust boundary

The authoritative [McKay Ramsey graph data
page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html) states that the
order-24 `(4,5)` catalog is complete (352,366 graphs) and provides complete
sets at the smallest and largest few edge counts for orders 4 through 23.  We
use the largest listed edge counts for orders 18 through 23 and scan the full
order-24 catalog.  The pinned inputs are

```text
9cfac9dbd1c209cfa342e5d5424df2a7a3fbb008ca00bf0a992e5bbe72f925b6  r45extreme.tar.gz
83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0  r45_24.g6
```

`extrema.json` is a compact factual manifest, not a replacement proof of the
upstream classifications.  The external completeness of those catalogs is
the inherited trust boundary.  Given the seven `U(k)` values, the deficiency
identity and all consequences are proved here by elementary double counting
and independently audited by the included program.

Discovery Net was searched through indexed height 2034 for the `R(5,5)`
problem neighborhood and for `degree`, `neighborhood`, `codegree`,
`deficiency`, and `local Ramsey`.  It contains a mature one-vertex extension
obstruction program and Cyclic(43) component closures, but not this
two-color-neighborhood identity, the 622 bound, or the near-extremal-core
dichotomy.  Novelty is asserted only relative to the searched graph and cited
catalog description; no historical-priority claim is made.

The next falsifiable milestone is to enumerate the `(4,5;k)` graphs at edge
levels `U(k)` through `U(k)-7` (or exploit the 66-fold exact-level-seven hard
case) and encode only the cross-incidence patterns capable of completing such
a local core to 43 vertices.  This avoids duplicating unconstrained
whole-graph search.
