# Proof and exact reduction
## 1. Atoms and field

Represent a complex point by `(a,b,c,d)` meaning

```
a + b*sqrt(33) + i*c*sqrt(3) + i*d*sqrt(11).
```

The multiplication table in `arithmetic.py` follows by squaring the three
radicals and using `(sqrt(33))(i sqrt(3))=3 i sqrt(11)` and its cyclic
companions.  Complex conjugation negates the last two coefficients.  Thus
equality, conjugation, division by a nonzero element, and the squared Euclidean
norm `z*conjugate(z)` are exact rational operations.

Put

```
omega = (1+i*sqrt(3))/2,
eta   = (5+i*sqrt(11))/6.
```

The Moser atom is

```
M = {0,1,omega,1+omega,eta,eta*omega,eta*(1+omega)}.
```

The ten Golomb coordinates are listed definition-first in `geometry.golomb`.
Direct exact scans give 11 and 18 strict unit edges respectively.  Both begin
with the unit triangle `(0,1,omega)`.

## 2. Complete isometry enumeration

Every Euclidean plane isometry has exactly one of the forms

```
T(z)=t+r*z,             T(z)=t+r*conjugate(z),       |r|=1.
```

Suppose a copy `T(A)` contains two distinct seed points `b_a,b_b`.  Their
preimages are two distinct atom points `a_i,a_j`, and

```
|a_j-a_i| = |b_b-b_a|.
```

Conversely, choose either orientation type, an ordered distinct atom pair and
an ordered seed pair with equal exact squared distance.  Then

```
r = (b_b-b_a)/(a_j-a_i),       t = b_a-r*a_i
```

has `|r|=1` and gives the unique isometry of that type realizing the two
coincidences.  `copies_on_seed` enumerates precisely these finite choices and
deduplicates complete point sets.  Therefore it contains every and only
congruent or reflected copy sharing at least two seed points.  Copies with
three or more shared points are automatically included rather than assumed
generic.

The resulting copy counts, classified by the actual number of shared seed
points, are:

| Closure | Sharing-count distribution |
|---|---|
| Moser self | 2:107, 3:38, 4:6, 7:1 |
| Golomb self | 2:180, 3:42, 4:25, 7:3, 10:1 |
| Mixed, Moser copies | 2:246, 3:61, 4:29, 5:6, 7:1 |
| Mixed, Golomb copies | 2:260, 3:64, 4:25, 5:8, 6:2, 7:3, 10:1 |

## 3. Strict graphs and colour certificates

For each closure, take the set-theoretic union of the seed and every
enumerated copy.  The canonical point order keeps the seed first and sorts
all remaining exact field tuples.  Every unordered pair is checked for the
exact equality

```
(x-y)*conjugate(x-y) = 1.
```

This constructs the complete strict unit-distance edge set, not merely the
edges inherited from atom copies.  The point and edge streams are pinned by
SHA-256 in `certificate.json`.

The certificate supplies one symbol from `{0,1,2,3}` per canonical point.
`verify.py` checks its length and alphabet and directly tests unequal colours
on every reconstructed strict edge.  It obtains the three rows in `README.md`.
No solver soundness or UNSAT result is used in this verification.

Finally, any subassembly of allowed copies is a point subset of the full
closure.  Restricting the full closure's proper four-colouring gives a proper
four-colouring of its complete induced unit-distance graph and hence of every
edge subgraph.  This proves the stated family exclusion, including all
subassemblies through 508 vertices.
