# Autonomous blocks are independent in uniform poset linear extensions

For a finite skeleton poset `S` and nonempty block posets `Q_s`, form the
lexicographic sum `R=S(Q_s:s in S)`.  A linear extension of `R` has two
pieces of data:

- its block word, recording only which block occupies each position;
- one internal linear extension of every block.

The main theorem gives the exact Cartesian-product bijection

```text
L(R) <--> W(S;(|Q_s|)_s) x product_s L(Q_s),
```

where `W` consists of multiset block words that put every copy of `s`
before every copy of `t` when `s<t` in `S`.  Therefore, in a uniform random
linear extension, the internal block orders are mutually independent and
uniform, and are independent of the block word.

## Consequences

- Restriction to an autonomous subset is a uniform linear extension of the
  induced subposet.
- Every internal pair probability is preserved exactly.  Thus
  `delta(P)>=delta(P[A])` for a nonchain autonomous subset `A`.
- A minimum-order counterexample to the 1/3--2/3 conjecture can have no
  proper autonomous nonchain subset.
- Every finite adaptive comparison tree whose queries stay within blocks
  has exactly the same transcript probabilities as the product experiment
  on independent uniform block extensions.  Every transcript count in the
  full poset is multiplied by the same block-word factor.
- The autonomy condition is essential in general: for the three-element
  poset with sole relation `a<c`, restriction to the non-autonomous
  antichain `{a,b}` has multiplicities `2:1`, not `1:1`.

The proof is in [PROOF.md](PROOF.md).

## Prior-art boundary

The product-table mechanism, Gold Partition transfer, and balance-constant
inequality are already established by Dolores-Cuenca, Guzman-Saenz, and Kim,
arXiv:2410.12494, Lemmas 2.3 and 2.5 and Corollary 2.7.  This package is an
independent, definition-level reproduction and a simultaneous probabilistic
formulation.  The arbitrary-depth adaptive transcript statement is an
immediate consequence of the same bijection.  No priority claim is made.

## Exact audit

The dependency-free Python checker:

- enumerates every naturally labelled poset through order six;
- finds every autonomous subset directly from its definition;
- verifies that every induced linear extension has the same number of
  ambient extensions;
- separately checks the simultaneous product coordinates for a bounded
  family of lexicographic sums; and
- confirms the minimal order-three non-autonomous failure.

Run with Python 3.11 or later:

```bash
./run_checks.sh
```

The universal theorem rests on the written bijection, not on finite
enumeration.  The checker uses exact Python integers, tuples, permutations,
and sets; there is no solver, floating point, randomness, external data, or
omitted catalogue.  Sources and search scope are in [SOURCES.md](SOURCES.md).
