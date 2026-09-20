# Every order-15 tournament has a strong Seymour vertex

For a vertex `x` in a tournament, put

```text
A = N+(x),  B = N-(x),
Gamma_x(S) = {b in B : s -> b for some s in S}.
```

A vertex is **strong Seymour** when the bipartite directed link from `A` to
`B` has a matching saturating `A`.  It is **ordinary Seymour** when
`|N++(x)| >= |N+(x)|`.

## Theorem

Every tournament on 15 vertices has a strong Seymour vertex.

The proof is by contradiction.  Assume `T` has order 15 and no strong
Seymour vertex.  Every tournament has an ordinary Seymour vertex; choose one
and call it `x`.  The preceding certified
[`size-five exclusion`](../strong_seymour_order15_hall_size5) proves that

```text
d+(x) = 7,
```

and that every inclusion-minimal deficient Hall set at `x` has size exactly
six.  Fix such a set `S`.

## The remaining local structure

Write

```text
R = Gamma_x(S),   C = A \ S,   D = B \ R.
```

Inclusion-minimality of `S` gives `|R|=|S|-1=5`.  It also says every member
of `R` has at least two predecessors in `S`: otherwise removing the unique
predecessor would leave a deficient proper subset.  Since both `A` and `B`
have size seven,

```text
|S|=6,  |R|=5,  |C|=1,  |D|=2,  D -> S.          (1)
```

Ordinaryness gives `N++(x)=B`.  No member of `S` sends an arc to `D`, so the
unique member `c` of `C` must reach both members of `D`:

```text
c -> D.                                           (2)
```

For `v in S`, define

```text
p(v) = d+_{T[S]}(v),       q(v) = |N+(v) intersect R|.
```

The only possible out-neighbor of `v` outside `S union R` is `c`.  The
inherited global minimum-out-degree bound `delta+(T)>=6` therefore yields

```text
p(v) + q(v) >= 5.                                 (3)
```

## Nineteen exhaustive signatures

There are two branches.

If equality holds in (3), choose one tight vertex and relabel it as vertex 1.
Its internal score is one of

```text
p(1) = 0, 1, 2, 3, 4, 5,
```

and necessarily `q(1)=5-p(1)`.  These are six tight signatures.  No other
arc incident with `S` is fixed by this classification.

If equality never holds, then

```text
p(v) + q(v) >= 6  for every v in S.               (4)
```

Because `q(v)<=5`, every internal score `p(v)` is positive.  Relabel `S` so
that its score sequence is nondecreasing.  Landau's tournament-score
criterion says that a nondecreasing integer sequence
`p_1,...,p_6` is realizable precisely when

```text
sum p_i = 15,
sum_{i=1}^k p_i >= binom(k,2)  for 1 <= k <= 6.
```

Among positive sequences, this leaves exactly thirteen possibilities:

```text
(1,1,1,3,4,5)  (1,1,1,4,4,4)  (1,1,2,2,4,5)
(1,1,2,3,3,5)  (1,1,2,3,4,4)  (1,1,3,3,3,4)
(1,2,2,2,3,5)  (1,2,2,2,4,4)  (1,2,2,3,3,4)
(1,2,3,3,3,3)  (2,2,2,2,2,5)  (2,2,2,2,3,4)
(2,2,2,3,3,3).
```

For a fixed sequence, the formula fixes only the six internal degrees and
imposes `q(v)>=6-p(v)`; it leaves every realizing tournament on `S` free.
Thus score sequences are complete signatures rather than proxies for
isomorphism types.

The six tight and thirteen strict signatures are disjoint and exhaustive.
Independently of Landau's theorem and of the SAT generator,
`check_signatures.py` enumerates all `2^15=32768` labeled tournaments on six
vertices.  It recovers exactly the displayed positive sequences, with
labeled counts

```text
240, 80, 720, 1440, 2880, 1680, 1680,
1680, 8640, 2400, 144, 2400, 2640.
```

Their sum is 26,624, the number of labeled six-vertex tournaments having no
score-zero vertex.  The newline-separated comma-form sequence list has
SHA-256

```text
f58605f97fb4ee29323660d0ba50c33f52cf1c674762346426517620b93e8ad1.
```

This establishes the finite structural gate without enumerating `S`--`R`
link patterns or order-15 tournaments.

## Exact exclusion of all signatures

`generate_cases.py` imports the all-vertex no-strong encoding from
`strong_seymour_order15/generate_cnf.py`.  The imported formula enforces the
global minimum degree, encodes a minimal deficient Hall witness at every
degree-six or degree-seven vertex, and normalizes the selected degree-seven
root and its size-six witness.  Each of the 19 extensions adds only:

1. the two root-ordinaryness arcs in (2);
2. the defining tight or strict signature; and
3. harmless relabeling arcs within still-symmetric parts.

In a tight case, the chosen vertex is label 1, while the other five members
of `S` remain freely relabelable.  In a strict case, the score sequence sorts
the labels; within every equal-score block, one representative internal arc
can be oriented because that block remains freely relabelable.  The sets `R`
and `D` are independently relabelable in every case.  These symmetries do not
remove any isomorphism class satisfying the signature.

The exact formulas have 20,666--20,768 variables and 47,345--47,552 clauses.
CaDiCaL 3.0.1 returns UNSAT for every formula.  `drat-trim` independently
verifies all 19 binary DRAT traces, with zero RAT lemmas in each checked core.
The traces total 733,799,202 bytes.  Exact formula and proof hashes and core
statistics are recorded in `EXPECTED.json`; the canonical verification-record
manifest has SHA-256

```text
41cc552e669658832e5e4010e813f75ee173c3334097dfc70cf1e35e0c2cae4e.
```

Every hypothetical size-six witness satisfies one of the six tight
signatures or one of the thirteen strict signatures.  Since all 19 are
impossible, no such witness exists.  This contradicts the inherited theorem
that an order-15 counterexample has exactly such a witness at an ordinary
root, and proves the theorem.

## Corollary and trust boundary

Combining this theorem with the exact order-at-most-14 result proves that
every tournament on at most 15 vertices has a strong Seymour vertex.

The local reduction and signature completeness are human-readable above;
the standard-library checker supplies a separate exhaustive audit of the
only finite classification.  The global step trusts the inspected base
generator, PySAT's sequential cardinality encodings, CaDiCaL, and
`drat-trim`.  The proof checker establishes UNSAT only for the exact hashed
formulas, not for an informal or changed encoding.
