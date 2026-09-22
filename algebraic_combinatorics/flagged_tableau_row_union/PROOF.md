# Proof of the residue-tagged row-union injection

Rows and columns are indexed from one.  Trailing zero parts may be appended
to any partition.  A flag `b=(b_1,...,b_r)` is weakly increasing.

## Sorted matching lemma

Suppose two multisets of integers have the same size `m`, and there is a
bijection matching every element of the first multiset to a strictly larger
element of the second.  If their increasingly sorted lists are

```text
a_1 <= ... <= a_m,       c_1 <= ... <= c_m,
```

then `a_j<c_j` for every `j`.

Indeed, fix `j`.  Each of the `j` second-multiset elements at most `c_j` is
matched to a distinct first-multiset element strictly below `c_j`.  Hence at
least `j` first-multiset elements are strictly below `c_j`, so `a_j<c_j`.

We will also use the immediate observation that if the first multiset is
enlarged, its `j`-th smallest element can only decrease.

## Construction

Fix `k>=1`.  Let `lambda^(1),...,lambda^(k)` be partitions padded to `r`
rows, and let `T^(q)` belong to `SSYT(lambda^(q),b)`.  Define

```text
phi_q(t)=k(t-1)+q,                 1 <= q <= k.
```

For every row `i`, form the multiset

```text
M_i = multiset union over q of
      {phi_q(T^(q)_(i,j)) : 1 <= j <= lambda_i^(q)}.
```

Put the elements of `M_i` into row `i` in increasing order.  Call the
resulting filling `U`, and put

```text
mu_i = sum_q lambda_i^(q).
```

Since sums preserve weak decrease, `mu` is a partition.  The construction
makes every row of `U` weakly increasing.  Moreover,

```text
phi_q(T^(q)_(i,j)) <= k(b_i-1)+q <= k b_i,
```

so row `i` respects the flag `kb`.

## Column strictness

Fix adjacent rows `i` and `i+1`, and put `m=mu_(i+1)`.  For every source
`q` and every `1<=j<=lambda_(i+1)^(q)`, match the transformed lower entry

```text
phi_q(T^(q)_(i+1,j))
```

to the transformed upper entry in the same source column,

```text
phi_q(T^(q)_(i,j)).
```

The upper cell exists because `lambda^(q)` is a partition.  Semistandard
column strictness in `T^(q)` gives

```text
phi_q(T^(q)_(i,j)) < phi_q(T^(q)_(i+1,j)).
```

Thus the `m` lower entries are bijectively matched to a submultiset of `m`
upper entries, each matched upper entry being strictly smaller.  By the
sorted matching lemma, the `j`-th element of that sorted upper submultiset is
strictly below the `j`-th entry of row `i+1`.  Row `i` may contain additional
entries, and adding them can only lower its `j`-th smallest element.
Therefore

```text
U_(i,j) < U_(i+1,j),       1 <= j <= mu_(i+1).
```

All columns of `U` are strict, so `U` belongs to `SSYT(mu,kb)`.

## Explicit inverse on the image

For an entry `u` in a merged row, let

```text
q = 1 + ((u-1) mod k),
t = 1 + (u-q)/k.
```

Then `u=phi_q(t)`.  Separate each row by its residue `q` and apply the second
formula.  Within one residue class, `phi_q` is strictly increasing, so the
recovered values occur in precisely the weakly increasing order of the
source row.  Their prescribed row counts are `lambda_i^(q)`.  This recovers
every `T^(q)` entry by entry and proves injectivity.

Taking cardinalities proves

```text
F(lambda^(1)+...+lambda^(k),kb)
    >= product_q F(lambda^(q),b).
```

For `lambda^(1)=...=lambda^(k)=lambda`, the target shape is `k lambda`,
which gives `F(k lambda,kb)>=F(lambda,b)^k`.

## Coefficientwise refinement

Let the weight of a tableau be the product of one variable for each entry.
Under the residue substitution

```text
x_t in source q  |-->  y_(k(t-1)+q),
```

the weight of a source tuple is exactly the weight of its merged tableau:
row sorting changes no entries. Since the map is injective, it restricts to
an injection on every monomial fibre. Therefore

```text
s_mu^(kb)(y_1,y_2,...)
  - product_q s_(lambda^(q))^b(y_q,y_(k+q),y_(2k+q),...)
```

is coefficientwise nonnegative. Principal specialization gives the displayed
cardinality inequality.

## Exact scope of the Schubert consequence

The vexillary identity-inflation reduction uses

```text
D_k(lambda)=((k lambda_1)^k,...,(k lambda_r)^k),
D_k(b)=((k b_1)^k,...,(k b_r)^k).
```

The theorem above reaches the intermediate horizontal shape `k lambda` and
supplies one factor `k` of the desired exponent `k^2`.  It gives no injection
from further independent tableaux across the repeated-row boundaries.  The
small case `lambda=(1), b=(1), k=2` also disproves the tempting intermediate
count comparison: `F((2,2),(2,2))=1` but `F((2),(2))=3`.
