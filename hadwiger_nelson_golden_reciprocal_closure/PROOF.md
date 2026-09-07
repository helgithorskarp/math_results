# Exact proof and finite verification

## 1. The pentagonal source

Put

\[
 \zeta=e^{2\pi i/5},\qquad
 q=|1-\zeta|^{-1},\qquad
 \phi=(1+\sqrt5)/2.
\]

Then the five points `q, q*zeta, ..., q*zeta^4` form a regular pentagon
with side 1 and diagonal `phi`.  We store a point without the common factor
`q`.  In the order of Parts's labels 1 through 16, the coefficient rows are

```text
(0,0,0,0,5) (1,0,0,0,4) (0,0,0,1,4) (1,0,0,1,3)
(0,1,0,0,4) (0,0,1,0,4) (1,0,1,0,3) (0,1,0,1,3)
(1,1,0,0,3) (0,0,1,1,3) (1,1,0,1,2) (1,0,1,1,2)
(0,1,1,0,3) (1,1,1,0,2) (0,1,1,1,2) (1,1,1,1,1).
```

A row `(a0,...,a4)` denotes `sum(a_k*zeta^k)`.  Every row sums to five,
so these are 16 of the 126 five-fold pentagonal Minkowski sums described in
the source.  Direct exact distance reconstruction gives exactly the 28
unit-edge labels and 28 golden-edge labels printed in Parts's paper.  The
verifier compares the two complete edge lists, not just their counts.

The labels 1, 2, 3, 5, 6 induce a `K5`.  The certificate also contains the
proper five-colouring

```text
1 3 2 0 4 0 1 1 2 4 3 2 3 4 0 1
```

so this finite two-distance graph has chromatic number exactly five.  This
source fact motivates the conversion; it does not assert that the ordinary
unit-distance subgraph has chromatic number five.

## 2. The complete reciprocal-overlay family

Let `B` be the physical point set obtained from the rows above.  For
`s` equal to `phi` or `1/phi`, let `C_s` consist of every point set

\[
 C=sR(B)+t
\]

where `R` is an orientation-preserving or orientation-reversing Euclidean
isometry fixing the origin, `t` is a translation, and at least two distinct
points of `C` coincide with points of the fixed set `B`.  Define the full
closure

\[
 X=B\mathbin\cup\bigcup_{C\in C_\phi\cup C_{1/\phi}} C.
\]

The enumeration of each `C_s` is finite and complete.  Choose two source
indices `a<b` in a moved copy and two target indices `i<j` in `B`.  They can
coincide only if

\[
 |B_j-B_i|^2=s^2|B_b-B_a|^2. \tag{1}
\]

Conversely, whenever (1) holds, the two choices of endpoint correspondence
and the two choices of orientation determine all possible similarities.  A
copy satisfying the two-coincidence hypothesis supplies at least one such
quadruple, because a similarity is injective.  Thus iterating all unordered
source and target pairs, both endpoint correspondences, and both orientations
is exhaustive.  Exact point-set deduplication removes the multiple
descriptions of copies with three or more coincidences.

For each scale there are 5,568 labelled specifications and 328 distinct point
sets.  Their numbers by exact intersection size with `B` are

| intersection size | 2 | 3 | 4 | 5 | 6 | 7 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| copies | 186 | 64 | 16 | 24 | 20 | 18 |

There are no copies with a larger intersection.  The scale-`1/phi` and
scale-`phi` closures each have 780 points; they meet in 174 points.  The
combined closure therefore has 1,386 points.

This classification includes arbitrary rotations and reflections.  The two
coincidences determine the transformation, so there is no unenumerated
continuous parameter.

## 3. Exact arithmetic

All calculations take place in

\[
 K=\mathbb Q(\zeta),\qquad
 1+\zeta+\zeta^2+\zeta^3+\zeta^4=0.
\]

The producer represents a field element in the power basis
`1,zeta,zeta^2,zeta^3` with rational coefficients.  Multiplication reduces
by the cyclotomic polynomial, conjugation sends `zeta` to `zeta^-1`, and
inversion is exact rational Gaussian elimination on the four-dimensional
multiplication matrix.  In this basis

\[
 \phi=-\zeta^2-\zeta^3,
 \qquad |1-\zeta|^2=3+\zeta^2+\zeta^3. \tag{2}
\]

For an orientation-preserving placement, the multiplier is

\[
 m=(B_{j'}-B_{i'})/(B_b-B_a),
\]

with `(i',j')` one of the two endpoint orders.  For a reflected placement,
the denominator and every moved difference are conjugated.  Equation (1),
checked exactly using (2), proves that `|m|=s`.

Every closure coordinate lies in `(1/11) Z[zeta]`.  The producer therefore
checks unit edges by integer multiplication after clearing the common
denominator.  Since physical coordinates are `q` times the stored values,
two stored points differ by a physical unit exactly when

\[
 (z-w)\overline{(z-w)}=|1-\zeta|^2. \tag{3}
\]

All `binom(1386,2)=959805` point pairs are tested against (3); the strict
unit-distance graph has 4,380 edges.  This includes accidental edges between
different moved copies.

The verifier derives the same field through the different representation

\[
 z=(A+B\sqrt5)+i\sqrt{10+2\sqrt5}(C+D\sqrt5),
 \quad A,B,C,D\in\mathbb Q.
\]

Every enumerated coordinate has all four coefficients in `(1/88) Z`.
Squared norms reduce to pairs in `Q(sqrt5)` using integer arithmetic after
clearing 88.  A unit difference is exactly the integer pair
`(19360,-3872)`, representing `88^2(5-sqrt5)/2`; a golden difference is
`(19360,3872)`.  The verifier has its own similarity enumeration, point
deduplication, and all-pairs edge reconstruction.

The canonical coordinate order is lexicographic in the four cleared integer
coefficients `(88A,88B,88C,88D)`.  Entrywise digests bind both implementations
to every copy point set, every closure point, and every unit edge.  The controls
also compare all 656 copy point sets entry by entry and compare conjugation,
norm, and inversion for all 120 source differences.

## 4. Four-colouring and consequence

`certificate.json` gives a 1,386-character word over `{0,1,2,3}` in the
canonical point order.  The verifier reconstructs all 4,380 strict unit edges
and checks different characters at every edge.  Hence `X` is four-colourable.

For any subcollection `D` of the 656 permitted copies, its physical point set
is a subset of `X`.  Every unit edge on that subset is an edge of the strict
unit-distance graph on `X`.  Restricting the certified colouring therefore
properly four-colours

\[
 B\cup\bigcup_{C\in D}C.
\]

This proves the claim for every subcollection simultaneously, with no bound
on the number of selected copies; repetitions do not change the point set.
In particular every member of order at most 508 is four-colourable.

## 5. Trust boundary and scope

The finite proof uses the written two-coincidence reduction, cyclotomic and
nested-quadratic arithmetic, exhaustive loops over finite pairs, direct colour
comparisons, SHA-256, Python's arbitrary-precision integers and rational
arithmetic, and the execution host.  The producer's DSATUR routine supplies
the colour word but is not trusted: the verifier checks the positive witness
definitionally.  There is no floating point, numerical root test, external
solver, or omitted generated input.

The theorem requires every moved copy to overlap the original fixed `B` in at
least two points.  It does not cover chains in which later copies overlap only
earlier moved copies, other scale factors, a deformed source, or the distinct
31-point six-chromatic construction from the same paper.  The negative result
therefore retires this precise reciprocal-overlay mechanism, not all uses of
pentagonal geometry.
