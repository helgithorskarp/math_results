# A fourth-order obstruction to 24-regular `(5,5,45)` graphs

## Result and scope

There is no 24-regular `(5,5,45)` Ramsey graph.  Equivalently, every
hypothetical `(5,5,45)` graph has a vertex of degree at most 23.

This is a symmetry-free, complete structural-subclass exclusion.  It uses all
352,366 graphs in the published complete order-24 `(4,5)` catalogue through a
single common fourth-order invariant; it does not glue them one at a time.
It does **not** exclude arbitrary `(5,5,45)` graphs, certify any of the three
order-45 occurrence-edge inequalities, or improve the numerical bound on
`R(5,5)`.

## Fourth-order identity

Write `G_v^+` and `G_v^-` for the neighbourhood and dual neighbourhood of a
vertex `v`.  For a graph `H`, let `K3(H)` be its number of triangles and let
`T31(H)` and `T32(H)` be the numbers of induced copies of, respectively,
a triangle plus a fourth vertex joined to exactly one or exactly two triangle
vertices.  Thus `T32` is `K4` with one edge removed.

The `m=4` case of McKay and Radziszowski's subgraph-counting identity, applied
to a graph `G` of order 45, is

```text
sum_v K4(G_v^-)
  = sum_v ((45/4 - |G_v^+| + 2) K3(G_v^+)
           + 3 K4(G_v^+) + (1/2) T31(G_v^+)
           + (4/3) T32(G_v^+)).
```

Every neighbourhood in a `(5,5)` graph is `K4`-free.  For an order-24
neighbourhood `H`, define the resulting right-hand summand `R(H)` by

```text
12 R(H) = -129 K3(H) + 6 T31(H) + 16 T32(H).
```

The exact scan of the complete order-24 catalogue proves the shared bound

```text
12 R(H) <= -528,       hence R(H) <= -44,
```

for every `(4,5,24)` graph `H` in that catalogue.  If a hypothetical
`(5,5,45)` graph were 24-regular, every `G_v^+` would belong to this complete
family.  The identity's right side would then be at most
`45*(-44) = -1980`, while its left side is a sum of nonnegative counts.  This
contradiction proves the result.

The conclusion is only about the complete 24-regular subclass.  In a
nonregular hypothetical graph, positive contributions from smaller
neighbourhoods could offset the negative order-24 terms, so the catalogue
calculation does not by itself exclude order-24 neighbourhoods.

## Complete census

The table gives, for every catalogue edge stratum, its size and the minimum
and maximum of `12 R(H)`.

| `e(H)` | graphs | minimum | maximum |
|---:|---:|---:|---:|
| 116 | 9 | -2364 | -2048 |
| 117 | 90 | -2350 | -1968 |
| 118 | 806 | -2324 | -1748 |
| 119 | 4,358 | -2304 | -1660 |
| 120 | 16,346 | -2284 | -1522 |
| 121 | 43,457 | -2155 | -1420 |
| 122 | 79,678 | -2026 | -1302 |
| 123 | 92,504 | -1800 | -1203 |
| 124 | 67,209 | -1704 | -1104 |
| 125 | 31,996 | -1478 | -1016 |
| 126 | 11,485 | -1356 | -918 |
| 127 | 3,401 | -1209 | -864 |
| 128 | 843 | -1062 | -748 |
| 129 | 147 | -915 | -626 |
| 130 | 32 | -768 | -590 |
| 131 | 3 | -636 | -636 |
| 132 | 2 | -528 | -528 |

In particular, all 352,366 values are strictly negative.  Notice that the
least negative stratum is the densest one, so restricting the earlier
15,913-graph `e(H) >= 126` tail is unnecessary for this theorem.

## Reproduction and independent check

Download `r45_24.g6` from Brendan McKay's Ramsey graph data page.  The imported
file used here has

```text
352366 lines
SHA256 83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0
```

Compile and run the primary scanner:

```sh
g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -Wconversion -Wshadow \
  -pedantic scan.cpp -o scan
./scan r45_24.g6 > scan.rows
python3 -B verify.py r45_24.g6 scan.rows
```

The expected row-stream SHA-256 is
`0620bc947873e32c8eb7aa9dd3e0c78af3426552e3f177fc1d1870aaac8da628`.
Each row contains

```text
catalogue_index edges K3 T31 T32 12R
```

For a definition-level independent check, compile and run the second program:

```sh
g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -Wconversion -Wshadow \
  -pedantic verify_direct.cpp -o verify_direct
./verify_direct r45_24.g6 > direct.rows
cmp scan.rows direct.rows
```

The primary scanner enumerates triangles and their fourth-vertex attachment
patterns.  The independent checker instead counts triangles through induced
neighbourhood edge counts, counts `T32` by the missing edge, and counts `T31`
by its distinguished pendant vertex.  Both programs also reject a `K4` or an
independent 5-set.  On the campaign host the full primary and independent runs
took approximately 30 and 12 seconds, respectively, and their 352,366 output
rows agreed byte for byte.

## Trust boundary and provenance

Imported rather than reproved here are:

- completeness and graph identities of McKay's order-24 `(4,5)` catalogue;
- the classical Ramsey value `R(4,5)=25`, which supplies the familiar
  degree range 20 through 24 at order 45;
- McKay and Radziszowski's general subgraph-counting identity.

The programs check the syntax, order, and `(4,5)` property of every catalogue
record, but these internal checks cannot establish external catalogue
completeness.

Primary sources:

- [Brendan McKay's Ramsey graph data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
- [McKay--Radziszowski, *Subgraph Counting Identities and Ramsey Numbers*](https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf)

The order-45 neighbourhood-edge reduction that motivated this lane is
Discovery Net contribution
`bafkreicgpqb2vyw2qtelysclrfyt6f2rljwzybt3a6f2wgotwgobtb75oy`; its accepted
verification/correction review is
`bafkreifxpqqpaifsozor24am6dnux7sczu2yhmrbmjqafjy5wakhob5qpu`.
