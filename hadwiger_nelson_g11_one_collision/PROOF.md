# Proof of the one-collision theorem

## 1. Source, quotients and chromatic transfer

Write `V=F_11^2`, `N(x,y)=x^2+y^2`, and join `u,v` when
`N(u-v)=1`. This defines `G_11`. The preceding exact certificate proves
`chi(G_11)=5`.

Let `u,v` be distinct nonadjacent vertices and let `Q_(u,v)` be the simple
graph formed by identifying `u` and `v`, retaining an edge between two blocks
when `G_11` has an edge between them. Because the identified pair is a
nonedge, no loop is created. The quotient map

```text
pi : G_11 -> Q_(u,v)
```

is a graph homomorphism. Thus a four-colouring of the quotient would compose
with `pi` to four-colour `G_11`, so `chi(Q_(u,v)) >= 5`. The certificate also
contains a proper five-colouring of every representative quotient; hence all
the quotients considered below have chromatic number exactly five.

Any edge-preserving map from the 121 source vertices to exactly 120 distinct
plane points has exactly one fibre of size two and all other fibres of size
one. The two vertices in that fibre cannot be adjacent. It therefore induces
an injective unit-distance drawing of one of these quotient graphs. It is
enough to rule out every `Q_(u,v)`.

## 2. Completeness of the nine representatives

Translations are automorphisms of `G_11`, so translate `u` to zero and write
`w=v-u`. The nonzero vector `w` does not have norm one. Moreover, `-1` is a
quadratic nonresidue modulo 11. If `N(w)=0` and the second coordinate is
nonzero, its quotient would give a square root of `-1`; the remaining cases
are immediate. Hence `N(w)` is one of `2,3,...,10`.

The orthogonal group is transitive on the vectors of each nonzero norm. One
way to see this without classification is to identify `(x,y)` with `x+i y`
in `F_121=F_11[i]`, where `i^2=-1`. If nonzero `w,z` have the same norm,
then `z/w` has field norm one. Multiplication by `z/w` is `F_11`-linear and
preserves `x^2+y^2`, so it is an orthogonal transformation sending `w` to
`z`. The verifier also checks this directly: it enumerates the 24 matrices
`A` with `A^T A=I` and confirms that the orbit of each listed representative
is the full 12-vector norm shell.

There are consequently exactly nine orbits of unordered allowable collision
pairs, represented by the vectors in the table in `README.md`.

## 3. Unit four-cycles are rhombi

Suppose four distinct plane points occur in cyclic order `a,b,c,d` and the
four cycle edges have length one. The points `b,d` are two distinct common
points of the unit circles centred at `a,c`. Injectivity makes `a,c`
distinct. Two distinct intersections of equal-radius circles are exchanged
by the half-turn about the midpoint of their centres, so their midpoint is
also the midpoint of `a,c`. Therefore

```text
p_a + p_c = p_b + p_d.                         (1)
```

This argument also excludes the tangent case, where the two circles would
have only one intersection. Chords elsewhere in the graph do not affect
(1).

For a quotient with `n=120` vertices, form the integer matrix `M` with one
row

```text
e_a - e_b + e_c - e_d
```

for each selected four-cycle. In any injective unit-distance drawing, each
Cartesian coordinate vector belongs to `ker_R(M)` by (1).

## 4. Exact rank lift from F_2

Every row of `M` has coefficient sum zero. Hence the all-ones vector lies in
its kernel and `rank_R(M) <= 119`.

Modulo two, signs disappear, so the row becomes the four-bit incidence vector
of its certified cycle. The independent checker verifies by XOR elimination
that the 119 stored rows in each quotient have rank 119 over `F_2`. Therefore
some `119 x 119` minor has determinant one modulo two. The same integer minor
has odd, hence nonzero, determinant. It follows that

```text
rank_R(M) >= 119.
```

Thus the real rank is exactly 119 and its kernel is the span of the all-ones
vector. Both Cartesian coordinate vectors of a purported drawing would be
constant. All 120 quotient vertices would occupy one point, contradicting
injectivity and the presence of unit edges. No representative quotient has
an injective unit-distance drawing. Sections 1 and 2 prove the theorem for
every edge-preserving source map with exactly 120 images.

## 5. Certificate and trust boundary

The producer enumerates all quotient four-cycles and greedily stores a basis.
The verifier does not import it. It reconstructs the graph and quotients from
the norm definition, checks that every stored row is an actual four-cycle,
recomputes its rank, and independently enumerates the complete orbit and
four-cycle counts. Because the stored rows themselves are witnesses, the
geometric conclusion does not rely on trusting the producer's claim that no
cycle was omitted.

The explicit quotient five-colourings are inherited from the predecessor
source colouring after certified orthogonal transformations and are checked
edge by edge. The lower bound `chi(G_11)>4` is imported from the pinned RUP
certificate in that package and can be rechecked with the first command in
`README.md`.

Trust remains in the written Euclidean rhombus lemma, the elementary
finite-field and graph-homomorphism arguments, CPython's exact integer and
JSON operations, the two checker implementations, and the already published
RUP verifier. Nothing here is a proof-assistant formalization or an
independent peer review.
