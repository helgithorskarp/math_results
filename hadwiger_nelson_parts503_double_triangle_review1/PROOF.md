# Proof and review analysis

## 1. Exact ambient geometry

Coordinates use denominator 288 and the ordered basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165)
```

on each axis. The basis index is the three-bit subset of `{3,5,11}`. For
basis indices `i,j`, multiplication has basis index `i xor j`, multiplied by
the product of primes in `i and j`. Linear independence of the eight basis
terms makes equality coefficientwise.

The review computes the rational coefficient of every squared distance first.
If it is not `288^2`, the distance cannot be one. For every survivor it
computes all seven irrational coefficients exactly. This is an exact early
exit, not the target's finite-field modular filter. All 1,388,611 ambient pairs
are visited.

The 509 parent points and 1,158 pool points are mutually distinct. The scan
finds 11,074 unit pairs, agreeing entry for entry with the pinned ambient edge
table. Restriction gives the strict 509-point, 2,442-edge parent. Its only six
degree-four vertices are

```text
310,313,316,319,322,325,
```

and they are independent. Deleting them gives the claimed 503-point,
2,418-edge host.

## 2. A common chromatic lower bound

Parent vertices

```text
0,398,408,459,397,407,470
```

all survive the deletion. Their induced unit graph has eleven edges.
Exhausting all `3^7=2,187` colour assignments finds no proper word. Thus the
host, and hence every five-point augmentation in the family, has chromatic
number at least four.

## 3. Complete finite family

Build the strict graph on the 1,158 pool points from the ambient scan. The
review enumerates all 625 unit triangles. For every pair whose vertex sets
meet in exactly one point, take the five-point union and merge duplicate
unions. This gives 1,401 supports.

Independently, for every possible shared centre, enumerate unit edges among
its pool neighbours and choose every pair of disjoint such edges. The
five-point sets from the two definitions agree exactly. Therefore every
five-subset in the declared family, including sets with extra contacts or
multiple triangle descriptions, is present once.

All ambient points were already proved distinct, so every support has
`503+5=508` physical points. Its complete edge set is the host edges together
with all ambient host--new and new--new pairs on the selected indices. Edge
counts range from 2,439 to 2,452.

## 4. Complete fixture-extension check

The 22 pinned strings are checked directly on all 2,418 host edges. For a
pool point and a host word, its available mask is the complement of the
colours on every reconstructed host neighbour.

For each support, enumerate all `4^5=1,024` assignments of its new vertices,
retain those proper on every new--new edge, and test them against the five
available masks. This is the definition of extension and has no search cutoff
or solver premise. At least one supplied host word extends on every support.
Combining that word with its local assignment proves a proper four-colouring
of the complete physical graph.

Together with the common seven-point lower bound, every one of the 1,401
supports has chromatic number exactly four.

The full support/fixture survival histogram is

```text
survivors: 10 11 12 13 14 15 16 17 18 19 20 21 22
supports:   1  1  9  9 13 48 68 80 137 204 251 287 293.
```

Hashing each sorted support, its complete internal-edge mask, old-contact
count and complete surviving fixture list yields
`3d6a2084e17d852dad98812b11ba1410fda1425283261278b46360e80811236c`.
The analogous first-positive-witness stream hashes to
`f95e48873db8990a03ee7367a9ac48c616758a53e6e2ee67482aec9aeb756ba6`.

## 5. Selected partial obstruction

Minimizing the number of surviving fixtures and breaking ties
lexicographically selects pool indices `(38,54,529,561,953)`. A fresh
all-pairs scan of its 508 points finds 2,450 edges, decomposing as 2,418 host,
26 old--new and six new--new edges.

Exactly fixtures

```text
3,5,8,9,12,13,14,16,17,18
```

extend. The other twelve are actual complete host colourings that do not
extend to this support. For rejected fixtures 6, 10 and 11, every individual
new vertex has a nonempty available list; deleting all new--new edges would
therefore allow an extension. Fixture 6 has lists

```text
{0}, {1}, {1}, {1}, {0,3},
```

and the internal constraints make them inconsistent. This proves that
private physical contacts contribute essentially to those three fixture
failures. It does not claim that every one of the six internal edges is
individually essential.

The target 508-symbol word and a fresh word from fixture 18 are checked on all
2,450 edges. The fresh word differs in 394 positions.

## 6. Scope and trust boundary

The positive words prove four-colourability without importing the parent's
five-chromaticity. The lower bound uses only the displayed retained
seven-vertex subgraph. The theorem trusts the four hash-pinned public inputs,
the standard multiquadratic basis fact, Python arbitrary-precision integers,
the finite enumeration code, and ordinary hardware.

The 22 host words do not exhaust all 503-vertex host colourings. They arose
from a separate list-interface classification at the deleted vertices, and
the selected replacement sees other host vertices. Consequently twelve
fixture failures prove neither exclusion of their former interface classes
nor a strict reduction of the complete host relation. Likewise, the finite
1,158-point pool is not asserted to contain every plane replacement point.

No floating-point predicate, probabilistic filter, SAT solver, negative solver
response, or omitted certificate enters the reviewed result.
