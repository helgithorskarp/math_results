# The one-quotient separator theorem

## Setup

Let `C` be an integer matrix with `n` columns and let

```text
L=row_Z(C) <= Z^n.
```

Let `T` be a finite nonempty subset of `Z^n`.  In the sequenceability search,
the rows of `C` are relations assumed on a branch.  A label assignment in an
abelian group `G` is a homomorphism `phi:Z^n -> G`, and it respects the branch
exactly when `L` is contained in `ker(phi)`.  The elements of `T` encode
forbidden vanishings.

## Theorem

The following are equivalent.

1. `T` is disjoint from `L`.
2. There is an integer `m>=2` such that `T` is disjoint from
   `L+mZ^n`.
3. There is one finite abelian group `G` and one homomorphism
   `phi:Z^n -> G` such that `L<=ker(phi)` and `phi(t)!=0` for every `t` in
   `T`.

When these conditions hold, condition 3 is witnessed by the single
congruence quotient

```text
G_m=Z^n/(L+mZ^n) = A/mA,       A=Z^n/L.              (1)
```

The least valid modulus

```text
m_*(L,T)=min{m>=2:T intersect (L+mZ^n) is empty}      (2)
```

therefore exists and depends only on `(L,T)`.

If `T` contains every basis vector `e_i` and every difference `e_i-e_j`,
then the labels `phi(e_i)` in (1) are pairwise distinct and nonzero.  Any
additional compression target in `T` also remains nonzero.

## Proof

The implication 2 to 3 is immediate from the quotient map in (1), and 3 to 1
is immediate because every element of `L` lies in every permitted kernel.
It remains to prove 1 to 2.

Use the structure theorem for finitely generated abelian groups to choose an
isomorphism

```text
A = Z^d direct-sum K,
```

where `K` is finite.  Let `E` be the exponent of `K`, with `E=1` when
`K=0`.  Write the image of each target as

```text
bar(t)=(z(t),tau(t)) in Z^d direct-sum K.
```

Because `t` is not in `L`, this pair is nonzero.  Let

```text
B=max{|z_j(t)|:t in T, 1<=j<=d},
```

with `B=0` if `d=0`.  Choose a positive multiple `m` of `E` with `m>B`.
If `E=1` and `B=0`, then `A` would have no free or torsion part and could not
contain the nonzero image of any target, so in every actual case one may take
`m>=2`.

Now

```text
mA=mZ^d direct-sum mK=mZ^d direct-sum 0.             (3)
```

If `tau(t)` is nonzero, (3) shows immediately that `bar(t)` is not in `mA`.
If `tau(t)=0`, then `z(t)` is nonzero.  Some coordinate has absolute value
between one and `B<m`, so `z(t)` is not in `mZ^d`.  Thus no target image lies
in `mA`, which is equivalent to `T` being disjoint from `L+mZ^n`.  This proves
1 to 2 and the equivalence.

Moreover, if

```text
K = Z/d_1 direct-sum ... direct-sum Z/d_s,
1<d_1 | d_2 | ... | d_s,
```

then `E=d_s` and one explicit choice is the least positive multiple of `E`
strictly larger than `B`.  The resulting certificate group has order

```text
|G_m|=m^d product_i d_i.                              (4)
```

This also proves finiteness and gives a Smith-data size bound.

## Exact certificate dichotomy

The theorem makes the logical quantifiers in a search terminal completely
checkable.

- If some `t in T` lies in `L`, an integer vector `u` satisfying `uC=t` is
  a positive terminal certificate.  Every permitted assignment kills `t`.
- If no target lies in `L`, a modulus `m` satisfying condition 2 is a
  countermodel certificate.  Membership tests against the stacked integer
  matrix `[C;mI_n]` verify that every target is nonzero in `G_m`.

Therefore

```text
every permitted finite-group assignment kills some target
    iff T intersects L.
```

The reverse direction now uses one explicitly presented finite quotient,
rather than a product of separately chosen residual-finiteness quotients.

## The two defective branches

For the characteristic-two branch, the four rows have rational rank four and
top determinantal divisor two.  Direct congruence reduction shows their row
subgroup in `(Z/2)^6` has order eight and avoids all 21 basis/difference
targets.  Hence its quotient has order eight and is `F_2^3`; the least
separator modulus is two.

For the odd-torsion branch, the five rows have rational rank five, Smith
torsion order three, and mod-three row subgroup order 81.  The quotient has
order nine and is `F_3^2`; again all 21 basis/difference targets survive.
The least separator modulus is three.

Thus both earlier hand-built countermodels are recovered canonically as the
quotient map (1).  More importantly, the same construction applies to every
future branch and every finite compression-target list.

## Limitations

This theorem does not show that a proposed ordering exists and does not make
the original large search complete.  It supplies the exact two-sided local
certificate needed by a corrected search.  Queue exhaustion, the correct
interval rule, and a certificate for every pruned branch would still be
required to establish a cardinality theorem.
