# Exact proof of the residual factor-clean bridge

## 1. Pinned finite interface

The proof uses h4091's 800-system exact classification, including the
distinct-root interval correction recorded by h4093, and h4085's fixed list
of 62 four-colour words.  All input certificates and the corrected h4091
verifier are hash-pinned.  The h4091 certificate identifies precisely 15
survivor components, at pair indices

```text
5, 6, 20, 30, 33, 36, 83, 85, 101, 109, 115, 194, 322, 347, 360.
```

They have 48 distinct real embeddings, and h4091 proves that every such
embedding is nonaligned, injective, and has all 343 labels.  Thirteen
components have degree four and two have degree six.

For a survivor row, h4091 supplies a shear `t=x+s*y`, a squarefree component
polynomial `m(t)`, and a shape equation

```text
A(t)y + B(t) = 0,       gcd(A,m)=1.
```

Thus in `K=Q[t]/(m)` we reconstruct

```text
y = -B/A,               x = t-s*y.
```

The standard-library verifier recomputes the inverse of `A` by extended
Euclid and checks the inverse identity.  The optional full-dependency mode
first runs h4091's corrected verifier, which independently rebuilds all 800
Groebner bases and all root intervals.

## 2. Factor cleanliness

h4065's exact source factorization supplies 972 event factors after deleting
the two positive Cayley denominators and sixteen alignment factors.  Every
non-Cartesian squared-distance-one polynomial factors into these source
factors (possibly with alignment or denominator factors), while the 1,764
Cartesian wheel-product edges are parameter independent.

For every survivor component and every one of the 972 factors `f`, the
verifier evaluates

```text
f(x(t),y(t)) mod m(t)
```

and computes its monic gcd with `m` over the rationals.  The factor is a unit
in `K` exactly when this gcd is one; this implication does not require `m` to
be irreducible.  Across all 15 components, exactly two factors per component
are nonunits, and they are exactly the h4071 representative pair defining
that component.  Moreover their residues are zero, while every other factor
has gcd one.  The verifier performs all `15*972=14,580` checks.  The canonical
gcd stream has SHA-256

```text
101e706d01104156ab2d09b8b8da3977a99c3c3c166889786ba59f6d589d33ae.
```

Therefore no other event factor can vanish at any complex root of `m`, hence
at any of its real roots.  Combined with h4091's nonalignment and injectivity
checks, the strict labelled unit graph is constant throughout each component:
its edges are precisely the Cartesian edges plus source pairs whose exact
factorization contains one of the two defining factors.

The verifier reconstructs these edge sets from h4065 rather than trusting
stored graphs.  Their SHA-256 hashes are pairwise distinct, so the 48
embedding-level possibilities collapse to 15 distinct labelled graph types.
This does not claim the 15 are pairwise nonisomorphic as abstract graphs.

## 3. Exact colour-word interface

For a four-colour word `w`, let `B(w)` be the set of nonalignment event
factors occurring in a monochromatic labelled pair.  The verifier reconstructs
all `B(w)` from the 58,653 labelled pairs and checks each word on the 1,764
Cartesian edges.  It also checks that h4085's first thirteen words are exactly
h4065's original thirteen.

On a factor-clean survivor with defining pair `{p,q}`, a word is proper if
and only if

```text
B(w) intersect {p,q} = empty.
```

Indeed, avoidance makes every possible monochromatic non-Cartesian event
factor a unit, so no such edge exists.  Conversely, if `p` or `q` belongs to
`B(w)`, its zero residue witnesses a monochromatic unit edge throughout the
component.  Thus the test is both necessary and sufficient, not merely a
sufficient modular witness.

The certificate records the complete list of proper h4085 word indices for
each of the 15 components.  None of indices 0 through 12 occurs, reproducing
the defining all-thirteen-failure property.  Twenty-four of h4085's 49 added
words are useful on at least one survivor.

## 4. Minimum cover and conclusion

Treat each of the 62 words as a 15-bit incidence mask and exhaust every subset
in increasing cardinality.  No subset of size at most three covers all 15
components.  Exactly three subsets of size four do, namely

```text
{18,24,34,40}, {24,31,34,40}, {24,31,40,47}.
```

The first cover colours respectively 5, 3, 6, and 1 components under the
canonical first-applicable assignment, accounting for 16, 10, 18, and 4 real
embeddings.  Hence four of h4085's already-published words give a complete
component-uniform cover of the entire h4091 residual interface, and four is
minimal within h4085's word library.

This proves a new exact factor-clean condition and a compact bridge between
h4091 and h4085.  It does not search for colourings, make an independent claim
about h4085's nonresidual branches, or improve the 509-vertex record.  The
complete three-wheel architecture remains four-colourable with zero candidate
classes.  Reviewer-1 has independently accepted that complete h4085 theorem;
this newer factor-clean bridge has not itself received a separate review.

## 5. Producer, verifier, and trust boundary

`produce.py` uses SymPy polynomial substitution and gcd over `QQ[t]`.
`verify.py` uses `fractions.Fraction`, explicit polynomial division, extended
Euclid, and exact pair enumeration; it imports neither SymPy nor a solver.
Both reconstruct factor and edge inventories from h4065 through h4071's
standard-library source interface.  `controls.py` rejects a missing survivor,
a missing nonunit, a false proper word, a changed graph hash, and a false
three-word cover, and checks hand-sized common-root/coprime gcd examples.

The trust boundary is CPython integer/rational arithmetic, the pinned h4065,
h4071, h4085, and corrected h4091 artifacts, and the written reduction above.
This is author-checked computer-assisted mathematics, not proof-assistant
formalization or an independent reviewer-1 verdict.
