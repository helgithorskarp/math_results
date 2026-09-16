# Exact support and positive colouring certificate

Let `w=(1+i sqrt(3))/2`, `v=(5+i sqrt(11))/6`, and
`eta=i sqrt((415+79 sqrt(33))/8)`, with the displayed positive real square
roots. The 27 rows `(a,b,c,d)` of `seed.json` give `a+bw+cv+dwv`.
The two added points, first in the implementation label order, are

```
p = 3 + (17/8)w - (7/8)v + 2wv
    + sqrt(5)(-1/4 + w/8 - v/8 + wv/4),
q = 11/4 + (13/8)w - v/8 + 2wv + (eta/8)(-w + v + wv).
```

These are the published Snail formulas, not coordinates inferred from a
picture. The source has 29 distinct points and 51 unit edges. The optional
source provenance and symbolic reconstruction are recorded in the earlier
[Snail package](../hadwiger_nelson_snail_dihedral/PROOF.md).

Use `A=i sqrt(3)`, `B=i sqrt(11)`, `C=sqrt(5)`, `E=8 eta`. Their equations are

```
A^2=-3, B^2=-11, C^2=5, E^2=-3320+632AB.
```

The square classes -3,-11,5 are independent, so the first three generators
give an abelian degree-eight extension K0. If E were in K0, its pure-imaginary
property and the centrality of complex conjugation would make every conjugate
of E purely imaginary. But the automorphism reversing A sends E^2 to
`-3320+632 sqrt(33)>0`, contradicting that property. (The inequality follows
from `632^2*33>3320^2`.) Thus the full field has degree 16 and the coefficient
vectors on `A^i B^j C^k E^l`, exponents 0 or 1, are unique. Complex conjugation
negates A,B,E and fixes C.

For an ordered pair `(a,b)` sent to `(c,d)`, set

```
u = (d-c)/(b-a),       t=c-u*a               (direct),
u = (d-c)/conj(b-a),   t=c-u*conj(a)         (reflected).
```

Nonzero pair length, equal squared norms, `u*conj(u)=1` and both endpoint
images are checked exactly. A motion is `x -> t+u*x` or `t+u*conj(x)`.
Inverse and word composition are checked in the number field. The fixed
17 words are listed literally in `CONTRACT.json`; there is no isometry
sampling, optimization or implicit family expansion.

All coordinates are exact rational coefficient vectors. Equal vectors are
merged, and the distinct vectors are sorted lexicographically in the A basis.
This yields the canonical vertex order used by both saved words. The canonical
coordinate hash is

```
9a791b88edea7cf47f09ca6ee0e8f00c04c4ea839558a56dbbe9e42a1df2305b
```

For every unordered pair, the exact test is `(x-y)*conj(x-y)=1`. A residue
specialization rejects most nonedges efficiently. Each denominator must be
invertible modulo the selected prime, and the specialized generators must
satisfy every defining equation. An exact unit pair must pass this test;
therefore rejection cannot discard an edge. Every pair passing the residue
test receives a full rational-coefficient norm check. There are no false
positive residue pairs in either run. The complete edge hash is

```
0d330ba2a693f0d81233bdf089d6b9b1e812884a455c34f943517e92f8a9cfad
```

The producer uses the A basis with prime 1,000,000,321. The checker constructs
the seed, motions, collisions and edges afresh in the w basis, where
`w^2=w-1` and `E^2=-3320-632B+1264wB`, using prime 1,000,000,411. Its polynomial
reduction differs from the producer's quadratic-tower multiplication.
Conversion `w=(1+A)/2` supplies an entrywise audit. All 444 coordinates,
493 address IDs and 890 edge entries agree.

The certificate lists a colour at each of the 444 vertices. Verification
requires one of exactly four allowed colours per vertex, all four used, and
different colours at the endpoints of every complete unit edge. This directly
proves ordinary four-colourability. The fifth-colour word is checked on exactly
the same edges and does not provide a chromatic lower bound.

For discovery, the CNF has variables `x[v,c]` for four colours. Each vertex
has exactly one colour and each physical edge forbids its endpoints from
sharing a colour. Fixing the first vertex to colour zero only chooses a global
colour permutation. Decoding a SAT model is followed by the direct edge
check above, so solver soundness is unnecessary for the positive theorem.

The trust boundary is the explicit source formulas, the elementary field-degree
argument, the pinned arithmetic source and Python exact integer/rational
computations. The argument is not proof-assistant formalized. No asymptotic
fractional-colouring theorem, unverified UNSAT claim or floating-point test
is used to prove this graph's colourability.
