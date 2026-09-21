# Exact local obstruction theorem

## 1. Definitions

Let `A_n` be defined by

```text
sum_(n>=0) A_n z^n/n! = sec(z)+tan(z).
```

Fix an odd prime `p`.  For `n>=1`, let

```text
rho_p(n) = 1 + ((n-1) mod (p-1)),
```

the positive representative in `{1,...,p-1}`.  For `p>=5`, define subsets
of the even indices in `{2,4,...,p-3}` by

```text
E_p = {j : p | A_j},
B_p = {j : p | numerator(B_j)},
O_p = {j : ord_p(2) | j},
T_p = B_p union O_p.
```

Here `B_j` is the ordinary Bernoulli number in lowest terms.  Since
`2<=j<=p-3`, von Staudt--Clausen says that its denominator is prime to `p`.
Thus membership in `B_p` is equivalently `B_j=0 mod p`.

Call `p` base-two Wieferich when

```text
2^(p-1) = 1 mod p^2.
```

## 2. The theorem

Let

```text
Z_p = {u in {1,...,p-1} :
       p | A_(rho_p(u+t)) for t=0,1,2}.
```

For every prime `p>=5`, `Z_p` is the disjoint union of the following sets.

### Even interior

```text
{u : u even, 2<=u<=p-5,
     u in E_p, u+2 in E_p, u+2 in T_p}.
```

### Even boundary

The singleton `{p-3}` if all three conditions hold:

```text
p=1 mod 4,  p-3 in E_p,  p is base-two Wieferich.
```

Otherwise this class is empty.

### Odd interior

```text
{u : u odd, 3<=u<=p-6, j=u+1,
     j in E_p intersect T_p, j+2 in T_p}.
```

### Odd boundary

The singleton `{p-4}` if both conditions hold:

```text
p-3 in E_p intersect B_p,  p is base-two Wieferich.
```

Otherwise this class is empty.  No other residue occurs.  For `p=3`, one
checks directly that `Z_3` is empty.

## 3. Algebraic ingredients

Güleç's frequency expansion gives, for `n>=1`,

```text
A_(n+p-1) = epsilon_p A_n mod p,
epsilon_p = (-1)^((p-1)/2).
```

The multiplier is a unit, so zero indices are periodic modulo `p-1` in the
positive-residue convention above.

For even `j`, the tangent-number formula is

```text
A_(j-1) = (-1)^(j/2-1) 2^j (2^j-1) B_j/j.            (1)
```

If `2<=j<=p-3`, every factor outside `(2^j-1)B_j` is a `p`-adic unit.
Therefore

```text
p | A_(j-1)  iff  j in T_p.                           (2)
```

At the endpoint `j=p-1`, von Staudt--Clausen gives

```text
v_p(A_(p-2)) = v_p(2^(p-1)-1)-1,                     (3)
```

so `p|A_(p-2)` exactly when `p` is base-two Wieferich.  The frequency
expansion also gives

```text
A_(p-1) = 0 mod p  if p=1 mod 4,
A_(p-1) = -2 mod p if p=3 mod 4.                     (4)
```

Finally `A_1=A_2=1`.

## 4. Proof of the classification

By the shift congruence it is enough to inspect one positive residue
`u in {1,...,p-1}`.

Suppose first that `u` is even.  Away from the endpoint, `A_u` and
`A_(u+2)` are secant numbers, so they vanish exactly when `u,u+2` lie in
`E_p`.  The middle term `A_(u+1)` is a tangent number whose Bernoulli index
in (1) is `u+2`; by (2) it vanishes exactly when `u+2 in T_p`.  This is the
even-interior class.  At `u=p-3`, the three terms are `A_(p-3)`,
`A_(p-2)`, and `A_(p-1)`, and (3)--(4) give exactly the even-boundary class.
At `u=p-1`, the next term reduces to `A_1=1`, so no triple occurs.

Now suppose that `u` is odd and put `j=u+1`.  In the interior, the central
term `A_j` is a secant number and the outer tangent terms have Bernoulli
indices `j` and `j+2`.  Thus their simultaneous vanishing is precisely

```text
j in E_p intersect T_p,  j+2 in T_p,
```

which is the odd-interior class.  At `u=p-4`, the right tangent term is the
endpoint `A_(p-2)` and hence requires Wieferich.  The left tangent term has
Bernoulli index `p-3`.  Its order-of-two factor cannot vanish: if
`ord_p(2)` divided both `p-1` and `p-3`, it would divide `2`, impossible for
`p>=5`.  It therefore vanishes exactly when `p-3 in B_p`; together with the
central secant condition this is the odd-boundary class.  The residues `1`
and `p-2` encounter `A_1=1` after cyclic reduction and are impossible.

This exhausts all residues and proves the theorem.

There is a useful locality consequence in the odd-interior case.  The order
`ord_p(2)>2` cannot divide both `j` and `j+2`; hence at least one of those two
indices lies in `B_p`.  Thus the Bernoulli irregularity required by an
even-exponent preperiod failure is not merely somewhere in the period: it is
at the central Euler-irregular index or the next even index.

## 5. Preperiod corollary

Güleç proves, for `1<=k<=r-1`,

```text
s(p^r) <= r-k
iff p^j | A_(r-j) for every 1<=j<=k.                 (5)
```

For `r=2` the bound is automatic, while for `r=3` it follows from
`s(p^r)>=s(p)=1` (the source proves `s(p)=1`).  If the conjectured inequality
fails for `r>=4`, then (5) with `k=3`
forces

```text
p^3 | A_(r-3),  p^2 | A_(r-2),  p | A_(r-1).
```

In particular all three terms vanish modulo `p`, so
`rho_p(r-3) in Z_p`.  Therefore `Z_p=empty` proves the conjectured lower
bound simultaneously for every exponent `r>=2` at that prime.

For `p=67`, the exact defining recurrences give

```text
E_67={26}, B_67={58}, ord_67(2)=66,
2^66 != 1 mod 67^2.
```

Every one of the four classes is empty, so `Z_67=empty` and
`s(67^r)>=r-2` for all `r>=2`.
