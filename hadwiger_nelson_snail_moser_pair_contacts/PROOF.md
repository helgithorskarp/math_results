# Proof and finite reduction

## 1. Sources and physical graphs

Write

```text
w=(1+i sqrt(3))/2,  eta=(5+i sqrt(11))/6,
M=(0,1,w,1+w,eta,eta*w,eta*(1+w)).
```

The exact Moser graph has eleven unit edges.  The Snail point set `S` is
reconstructed from the 27 hash-pinned source rows and the displayed formulas
in `verify.py`.  A graph on a point set always means the complete strict
physical unit-distance graph after equal coordinates have been merged.

## 2. Completeness of the isometry list

Suppose a Euclidean isometry `f` satisfies `|S intersect f(M)|>=2`.  Choose
distinct `m_i,m_j` whose images are distinct `s_k,s_l`.  Isometries preserve
distance, so `|m_i-m_j|^2=|s_k-s_l|^2`.

Conversely, for any two such unordered pairs and either endpoint
correspondence, there is one direct and one reflected isometry taking the
first pair to the second.  In complex notation they are

```text
f(z)=a+u*z       or       f(z)=a+u*conj(z),
u=(s_l-s_k)/(m_j-m_i),   a=s_k-u*m_i,
```

with conjugation applied to the denominator and `m_i` in the reflected case.
Equality of squared lengths gives `u*conj(u)=1`.  These formulas enumerate
every possible `f`; cases with three or more coincidences merely acquire more
than one recipe.  Exact transform equality deduplicates the 3,068 recipes to
1,698 transformations.  Hence the census is complete.

## 3. Complete geometry

For every transformation, the verifier forms the 36 formal addresses (29
Snail and seven moved Moser addresses), groups exactly equal field elements,
and orders quotient classes by their least address.  It tests all unordered
physical pairs for norm one.  The modular screen is sound for exclusion:
if an exact norm equals one, its image under the checked field homomorphism
equals one.  Every modular survivor is checked in the rational field, so false
modular positives cannot become edges.  The direct audit independently tests
every pair without the screen.

This proves the stated orders, collision multiplicities, edge counts, and
canonical quotient-graph hash.

## 4. Completeness of the terminal relation

In any proper colouring, the unit triangle `(0,1,w)` in `M` has three distinct
colours.  A global permutation sends these colours uniquely to `0,1,2` and
the unused fourth colour to `3`.  Exhaustion of the remaining four vertex
colours gives exactly sixteen proper normalized Moser words.  Therefore those
sixteen words represent every proper labelled four-colouring modulo global
colour permutation.

For each physical quotient graph and normalized word, deterministic
minimum-domain backtracking finds an extension.  The returned full word is
then checked directly on every strict edge and at every moved Moser terminal.
Only this positive word check is needed for the existence claim; completeness
or soundness of a solver is not assumed.  Applying the inverse global colour
permutation proves extension for the original labelled Moser word.

Thus the projection of the four-colourings of `S union f(M)` onto `f(M)` is
the full proper four-colour relation of `M` for every qualifying `f`.

Finally, direct exhaustion shows that the eleven-edge Moser graph has no
three-colouring.  It is a subgraph of every union, while the preceding words
give four-colourings.  Every union therefore has chromatic number exactly
four.
