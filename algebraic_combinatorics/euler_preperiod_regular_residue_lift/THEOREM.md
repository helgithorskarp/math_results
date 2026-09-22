# Exact cyclotomic lift on every Bernoulli-regular tangent residue

## 1. Statement

Let `A_n` be defined by

```text
sec(z)+tan(z) = sum_(n>=0) A_n z^n/n!.
```

Fix an odd prime `p`.  Let `j` be even with

```text
2 <= j <= p-3,
```

and suppose that `p` does not divide the numerator of the Bernoulli number
`B_j`.  For every positive even integer `m` satisfying

```text
m = j (mod p-1),
```

we have

```text
v_p(A_(m-1)) = v_p(2^m-1).                         (1)
```

Put

```text
d   = ord_p(2),
w_p = v_p(2^(p-1)-1).
```

Because `d | p-1`, equation (1) is equivalently

```text
v_p(A_(m-1)) = 0                 if d does not divide j,
v_p(A_(m-1)) = w_p + v_p(m)      if d divides j.    (2)
```

Thus on every interior residue at which the Bernoulli factor is a `p`-adic
unit, all higher divisibility is exactly cyclotomic.  In the terminology of
the local preperiod classification, if

```text
O_p={j: ord_p(2) divides j},
B_p={j: p divides numerator(B_j)},
```

then every `j in O_p - B_p` has the uniform valuation

```text
v_p(A_(m-1)) = w_p+v_p(m)
```

throughout its entire congruence lift.

## 2. Proof

Since `m` and `j` are positive even integers, are congruent modulo `p-1`,
and are not divisible by `p-1`, Kummer's congruence gives

```text
B_m/m = B_j/j (mod p).                             (3)
```

The congruence takes place in the localization at `p`.  Our range gives
`p`-integrality, and the hypothesis on `B_j` says that the right side is a
unit.  Hence

```text
v_p(B_m/m)=0.                                      (4)
```

For even `m`, the odd-index up/down number is the tangent number, so the
classical tangent--Bernoulli identity is

```text
A_(m-1)=(-1)^(m/2-1) 2^m (2^m-1) B_m/m.           (5)
```

The sign and `2^m` are `p`-adic units.  Combining (4) and (5) proves (1).

It remains only to make (1) explicit.  The definition of `d` gives

```text
p | 2^m-1  iff  d | m.
```

Since `m=j (mod p-1)` and `d | p-1`, this is equivalent to `d | j`.  If it
fails, the valuation is zero.  If it holds, odd-prime LTE gives

```text
v_p(2^m-1)=v_p(2^d-1)+v_p(m/d).                   (6)
```

Both `d` and `(p-1)/d` are prime to `p`.  Applying the same formula to
`2^(p-1)-1` shows

```text
v_p(2^d-1)=v_p(2^(p-1)-1)=w_p,
```

and `v_p(m/d)=v_p(m)`.  This proves (2).

## 3. Exact preperiod sieve

Use positive representatives modulo `p-1`.  The committed local
classification says that an even-interior modular triple begins at an even
residue `u` with

```text
2 <= u <= p-5,
u,u+2 in E_p,  and  u+2 in T_p=B_p union O_p.
```

If its central tangent condition is order-only, namely

```text
j=u+2 in O_p - B_p,
```

then for any exponent `r` in this residue class the middle term is

```text
A_(r-2),  with m=r-1=j (mod p-1).
```

Guelec's exact preperiod criterion says that a failure of
`s(p^r)>=r-2` requires `p^2 | A_(r-2)`.  Formula (2) therefore gives the
necessary condition

```text
w_p+v_p(r-1) >= 2.                                (7)
```

For an odd-interior modular triple, put `j=u+1`; its first term is tangent:

```text
A_(r-3),  with m=r-2=j (mod p-1).
```

If `j in O_p-B_p`, the same criterion requires `p^3 | A_(r-3)`, and hence

```text
w_p+v_p(r-2) >= 3.                                (8)
```

For `w_p=1`, (7) forces `r=1 (mod p)`, while (8) forces
`r=2 (mod p^2)`.  Together with the already fixed residue modulo `p-1`, the
Chinese remainder theorem confines the two subcases to one class modulo
`p(p-1)` and `p^2(p-1)`, respectively.  If `w_p=2`, (7) is automatic but
(8) still forces `r=2 (mod p)`.  The statements retain the valuation form
(7)--(8) so that no unproved assertion about higher-order Wieferich primes is
needed.

## 4. Sharp boundaries

Both exclusions in the theorem are real.

1. At `j=p-1`, von Staudt--Clausen gives
   `v_p(B_j)=-1`, not a unit.  The separate boundary theorem accordingly
   gives `v_p(A_(q(p-1)-1))=w_p-1`, rather than (2).
2. At a Bernoulli-irregular pair the Bernoulli factor can add divisibility.
   For example, `p=37,j=32` has `37 | numerator(B_32)` while
   `ord_37(2)=36` does not divide `32`.  Nevertheless
   `v_37(A_31)=1`; the cyclotomic factor alone has valuation zero.

Thus this result does not control `B_p` residues, nor the secant terms in the
three-term obstruction.  It is exactly the uniform invariant for the
order-only tangent part of the other structural classes.

## 5. Status and scope

Kummer congruences, LTE, and the tangent--Bernoulli identity are classical.
No novelty is claimed for those ingredients or for equation (1) viewed in
isolation.  The search-relative contribution is the explicit all-lift
formulation (2), the sharp separation of cyclotomic and Bernoulli mechanisms,
and its consequences (7)--(8) for the named Euler-preperiod frontier.

This does not prove `s(p^r)>=r-2`, classify Bernoulli-irregular lifts, exclude
higher-order Wieferich primes, or replace the exact frequency criterion.  It
also does not support another catalogue of primes or offsets.
