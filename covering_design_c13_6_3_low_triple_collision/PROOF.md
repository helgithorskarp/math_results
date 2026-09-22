# Proof of the low-triple collision theorem

## 1. Conditional incidence system

Assume that a 20-block `(13,6,3)` covering has point-degree profile
`(12,9^12)`, and let `h` be its degree-12 point.  Delete `h` from each block
that contains it.  This gives two families on the twelve low points:

- `A`: twelve rows of size five, every low point occurring five times;
- `B`: eight rows of size six, every low point occurring four times.

The column sums follow from the classified optimal links: each low point has
total degree nine and occurs five times with `h`.  Rows inside either family
are distinct.  Otherwise the original 20-block family would contain a
repeated block, whose deletion would contradict the known lower bound 20.

We import the preceding exact theorem that no low triple occurs in three
rows of `A`.  Write `alpha_T` and `beta_T` for the multiplicities of a low
triple `T` in `A` and `B`, respectively.  Thus `alpha_T <= 2`.  Put

```text
r_T = alpha_T + beta_T.
```

Because the original family covers every low triple, `r_T >= 1`.

## 2. Two maximum-intersection parameters

For two `A` rows, let their intersection size be `s_ij`.  Double-counting a
point together with a pair of its incident `A` rows gives

```text
sum_{i<j} s_ij = 12 binomial(5,2) = 120.
```

There are `binomial(12,2)=66` pairs, so some intersection has size at least
two.  Distinct size-five rows intersect in at most four points.  Therefore

```text
k = max_{i<j} s_ij belongs to {2,3,4}.
```

Similarly, if `t_ij` are the intersections of two `B` rows, then

```text
sum_{i<j} t_ij = 12 binomial(4,2) = 72.
```

There are `binomial(8,2)=28` pairs.  Some intersection has size at least
three, while distinct size-six rows intersect in at most five points.  Hence

```text
l = max_{i<j} t_ij belongs to {3,4,5}.
```

Choosing a pair attaining each maximum is a global normalization.  No local
row orbit or incidence catalogue is involved.

## 3. Collision sums

For every nonnegative integer `s`,

```text
binomial(s,3) >= s-2.                                      (1)
```

For an `A`-row pair with intersection `s`, the number of low triples shared
by that pair is `binomial(s,3)`.  Consequently

```text
C_A = sum_{i<j in A} binomial(|A_i intersect A_j|,3)
```

is at least 0, 1, or 4 according as `k=2,3,4`: a pair attaining the maximum
alone contributes `binomial(k,3)`, and all other terms are nonnegative.

For `B`, summing (1) over its 28 row pairs gives the base bound

```text
C_B >= 72 - 2*28 = 16.
```

The surplus in (1), namely `binomial(s,3)-(s-2)`, is 2 at `s=4` and 7 at
`s=5`.  A pair attaining the maximum therefore strengthens the bound to

```text
C_B >= 16, 18, 23  for l=3,4,5, respectively.
```

Finally consider the 96 ordered cross-family pairs `(A_i,B_j)`.  Their
intersection sizes `u_ij` satisfy

```text
sum_{i,j} u_ij = 12*5*4 = 240,
```

because each low point belongs to five `A` rows and four `B` rows.  Applying
(1) gives

```text
C_AB = sum_{i,j} binomial(|A_i intersect B_j|,3)
     >= 240 - 2*96 = 48.
```

## 4. Triple multiplicity identity

Counting a pair of blocks through the same low triple in the other order
gives

```text
C_A + C_B + C_AB = sum_T binomial(r_T,2).                  (2)
```

There are `binomial(12,3)=220` low triples.  The twenty rows supply

```text
12 binomial(5,3) + 8 binomial(6,3) = 120+160 = 280
```

low-triple incidences.  Since every low triple is covered,

```text
sum_T (r_T-1) = 280-220 = 60.                              (3)
```

Subtracting (3) from (2), and using

```text
binomial(r,2)-(r-1) = binomial(r-1,2),
```

yields

```text
sum_T binomial(r_T-1,2) = C_A+C_B+C_AB-60.                 (4)
```

Substitution of the three lower-bound lists into (4) gives

```text
                    l=3   l=4   l=5
              k=2     4     6    11
              k=3     5     7    12
              k=4     8    10    15.
```

Every entry is positive, so some `r_T >= 3`.  The imported inequality
`alpha_T <= 2` then forces `beta_T >= 1` for such a triple.  Thus at least one
of its incident blocks avoids `h`.

## 5. Audit and limitations

The exact audit minimizes `sum binomial(s,3)` over every integer intersection
histogram having the relevant pair count, intersection sum, and prescribed
maximum.  It recovers minima `0,1,4` for `A`, `16,18,23` for `B`, and 48 for
the cross pairs.  This independently checks all arithmetic in the table.
The histogram minima need not themselves be realizable as incidence
systems; only their universal lower-bound property is used.

This theorem identifies an unavoidable higher-multiplicity low triple and a
nine-class global frontier.  It does not prove that any class is extendible
or impossible, exclude the `(12,9^12)` profile, or change the recorded global
interval `20 <= C(13,6,3) <= 21`.  Exploratory SAT and CP-SAT searches that
terminated without a decision are not evidence and are intentionally absent
from the certificate.

