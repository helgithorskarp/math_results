# One finite quotient certifies every nonterminal Graham-search branch

Let `C` be an integer relation matrix accumulated on a
Graham/Alspach sequenceability-search branch, let

```text
L = row_Z(C) <= Z^n,
```

and let `T` be its finite forbidden-target set.  This includes the basis
vectors and pair differences when labels must be nonzero and distinct, and
may also include compression targets.

The earlier accepted graph objection proved that a branch is universally
terminal over finite abelian groups exactly when `T` meets `L`; rational row
span is insufficient.  The result here strengthens its abstract residual-
finiteness converse:

> If `T` is disjoint from `L`, then one congruence quotient
> `Z^n/(L+mZ^n)` keeps every target in `T` nonzero simultaneously, for some
> integer `m>=2`.

Consequently each branch has a two-sided exact certificate.  A terminal
branch supplies an integer combination `uC=t` for one forbidden target.  A
nonterminal branch supplies one modulus `m`; exact membership tests in the
row lattice of `[C;mI_n]` verify that every target survives.  If the target
set contains all basis vectors and differences, the images of the standard
basis give pairwise distinct nonzero labels satisfying every recorded
relation.

The least working modulus is an invariant of `(L,T)`.  The proof gives an
explicit bound from any Smith decomposition of `Z^n/L`.  See
[THEOREM.md](THEOREM.md).

## Decisive applications

For the reviewed characteristic-two false terminal, the least modulus is
two and

```text
Z^6/(L+2Z^6) = F_2^3.
```

For the later odd-torsion false terminal, the least modulus is three and

```text
Z^6/(L+3Z^6) = F_3^2.
```

In each quotient all 21 basis/difference targets survive, so the quotient
map itself recovers a valid six-label countermodel.  No assignment search is
needed.

## Reproduction

Only the Python standard library is required:

```bash
python3 verify.py --max-width 5 --maximum-rows 3 --check-expected
python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The checker uses exact determinantal divisors for integer row-lattice
membership and direct subgroup generation modulo `m` for the independent
finite-quotient decision.  It audits the two published defective branches
and all 5,640 binary row families of width at most five with at most three
relations.  Among these, 610 avoid every basis/difference target over the
integers; each is separated by its least modulus, with histogram
`2:86, 3:464, 4:60`.

Finite testing corroborates the implementation and examples.  The universal
claim follows from the finitely generated abelian-group decomposition, not
from the census.

## Scope

This theorem repairs the *certificate architecture* identified by the graph
review.  It does not rerun the large search, certify the claimed cardinality
bounds, or resolve the Graham/Alspach or CMPP conjectures.  The underlying
finite-abelian decomposition is classical; novelty is claimed only for the
graph-guided application and explicit one-quotient certificate formulation,
and only relative to the searched sources.

See [SOURCES.md](SOURCES.md) for the primary-source boundary.
