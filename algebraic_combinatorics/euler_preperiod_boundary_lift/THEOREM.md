# Exact boundary-lift theorem

## 1. Valuation formula

Let `p` be an odd prime, `q>=1`, and

```text
m = q(p-1).
```

Since `m` is positive and even, `A_(m-1)` is a tangent number.  The standard
tangent--Bernoulli identity is

```text
A_(m-1) = (-1)^(m/2-1) 2^m (2^m-1) B_m/m.           (3)
```

Every factor in (3) is rational, but the product is the integer
`A_(m-1)`.  Take normalized `p`-adic valuations.

First, because `p-1 | m`, the von Staudt--Clausen theorem places `p`
exactly once in the reduced denominator of `B_m`.  Therefore

```text
v_p(B_m) = -1.                                       (4)
```

Second, LTE applies to `(2^(p-1))^q-1` and gives

```text
v_p(2^m-1)
  = v_p(2^(p-1)-1) + v_p(q).                         (5)
```

Finally, since `p` does not divide `p-1`,

```text
v_p(m) = v_p(q).                                     (6)
```

The sign and `2^m` are `p`-adic units.  Substituting (4)--(6) into (3)
cancels the two copies of `v_p(q)` and proves

```text
v_p(A_(q(p-1)-1))
  = v_p(2^(p-1)-1) + v_p(q) - 1 - v_p(q)
  = v_p(2^(p-1)-1) - 1.
```

This proves the main theorem.  Notice that assuming `p` does not divide `q`
would hide the main uniformity: (4) is unchanged, while the extra lift in
`2^m-1` cancels the division by `m` exactly.

## 2. Preperiod corollary

Guelec's exact criterion states, for `1<=k<=r-1`,

```text
s(p^r) <= r-k
iff
p^j | A_(r-j) for every 1<=j<=k.                    (7)
```

Suppose `r>=4` and the conjectured inequality `s(p^r)>=r-2` fails.  Since
the preperiod is integral, (7) with `k=3` gives

```text
p^3 | A_(r-3),  p^2 | A_(r-2),  p | A_(r-1).        (8)
```

Now also assume `r=1 mod (p-1)` and write `r-1=q(p-1)`.  Formula (1) says

```text
v_p(A_(r-2)) = v_p(2^(p-1)-1)-1.
```

The middle condition in (8) therefore forces

```text
v_p(2^(p-1)-1) >= 3,
```

or equivalently `p^3 | 2^(p-1)-1`.  Its contrapositive is (2).

## 3. Relation to the local obstruction theorem

Under positive reduction modulo `p-1`, the three modular zero positions in
(8) begin at

```text
r-3 = p-3 mod (p-1)
```

exactly when `r=1 mod (p-1)`.  The accepted local classification identifies
this as its even-boundary class and proves two additional necessary modular
conditions:

```text
p = 1 mod 4,       p | A_(p-3).
```

The present theorem is not another classification modulo `p`: it resolves
the missing middle `p^2` lift uniformly for every exponent in that boundary
class.

## 4. Limitations

For the three other modular classes, `r-2+1=r-1` is not generally a
multiple of `p-1`, so the von Staudt denominator and LTE cancellation above
do not apply in this form.  The theorem neither rules out order-three
base-two Wieferich primes nor controls the remaining `p^3` divisibility of
`A_(r-3)` when such a prime exists.
