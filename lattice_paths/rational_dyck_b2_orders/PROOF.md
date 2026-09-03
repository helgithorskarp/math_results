# Proof of the complete `D(a,2)` classification

Let `a>2` be coprime to `2`.  Write `a=2m+1`, and let `F_0=0`, `F_1=1`,
`F_(n+1)=F_n+F_(n-1)`.  We also use the convenient matrix convention
`F_(-1)=1`.

## 1. The paths

Every rational-Dyck word in `D(a,2)` starts with `R`.  It also ends with `U`:
otherwise the prefix before a final `R` would contain `a-1` right steps and
both up steps, contradicting `a*2 <= 2(a-1)`.

If the two up steps are adjacent, they must therefore be the final two steps,
giving

```text
H = R^a U^2.
```

Every other path has the form

```text
W_r = R^r U R^(a-r) U.
```

The only nonfinal prefix ending in an up step contains `r` right steps and one
up step.  Thus the rational-Dyck condition is exactly `a <= 2r`, or
`m+1 <= r <= 2m`.  Hence

```text
D(a,2) = {W_(m+1), ..., W_(2m), H}.                 (1)
```

## 2. Matching scores

Put `s=a-r` and `d=r-s`.  The four-block difference identity of
Apruzzese--Cong, specialized to the two unit up-blocks, gives

```text
M(H) - M(W_r) = 2 F_(2s) F_(2r-2).                 (2)
```

For `s>=2`, subtracting two consecutive instances of (2) and applying
d'Ocagne's identity gives

```text
M(W_(r+1)) - M(W_r)
 = 2(F_(2s)F_(2r-2) - F_(2s-2)F_(2r))
 = 2 F_(2(r-s))
 = 2 F_(2d) > 0.                                   (3)
```

Equation (2) is positive also at `r=a-1`, so the matching scores increase
strictly in the order displayed in (1), with `H` last.

## 3. Exact Lagrange formula

For `c` in `{1,2}`, put

```text
T(c) = [[c,1],[1,0]],    A=T(1),    B=T(2).
```

The finite adjacency word of `W_r` and its period matrix are respectively

```text
A^(2r-2) B^2 A^(2s-2) B,
P_(r,s) = B A^(2r-2) B^2 A^(2s-2) B.               (4)
```

Recall

```text
A^n = [[F_(n+1),F_n],[F_n,F_(n-1)]].               (5)
```

Let `M_(r,s)=M(W_r)`, with the same continuant notation allowed even when
the cyclically exchanged linear word is not rational-Dyck.  Direct
multiplication in (4), followed by (5) and

```text
F_j F_(k-1) - F_(j-1) F_k = (-1)^k F_(j-k),        (6)
```

gives two useful identities:

```text
M_(s,r) - M_(r,s)
 = 2(F_(2r-2)F_(2s-3) - F_(2r-3)F_(2s-2))
 = 2F_(2d),                                         (7)

tr(P_(r,s)) - 3M_(r,s)
 = 2(F_(2r-2)F_(2s-1) - F_(2r-3)F_(2s))
 = 2F_(2d-2).                                       (8)
```

Here (6) remains valid at `s=1` under `F_(-1)=1`.

The period contains four coefficients equal to `2`.  At the four cyclic
cuts beginning with such a coefficient, the lower-left entries of the
rotated period matrices are, two times each,

```text
M_(r,s), M_(s,r).                                   (9)
```

This follows directly from (4) and reversal invariance of a continuant.
Since `d>=1`, (7) says that the smaller distinguished denominator is
`M_(r,s)`.

Apruzzese--Cong prove that for a nonconstant periodic word over `{1,2}`, the
maximum in the Lagrange formula is attained at a cut beginning with `2`.
All cyclic period matrices have the same trace, and (4) has even length and
determinant one.  If a rotated period matrix is `[[p,*],[q,t]]`, the squared
difference of its two fixed points is therefore

```text
((p-t)^2 + 4rq)/q^2 = ((p+t)^2-4)/q^2.
```

Using (8) and (9), we obtain the exact formula

```text
L(W_r)^2
 = (tr(P_(r,s))^2-4)/M_(r,s)^2,

tr(P_(r,s))/M_(r,s)
 = 3 + 2F_(2d-2)/M_(r,s).                           (10)
```

## 4. Strict Lagrange monotonicity

Write `M_d=M_(r,s)` and `Delta_d=2F_(2d-2)`.  Increasing `r` by one decreases
`s` by one and replaces `d` by `d+2`.  Equation (3) says

```text
M_(d+2) = M_d + 2F_(2d) > M_d.                     (11)
```

The coefficient word defining `M_d` has length `2a-1` and all coefficients
are positive.  Its continuant is at least the all-one continuant, so

```text
M_d >= F_(2a) > F_(2d),                             (12)
```

where `d<=a-2`.  Now

```text
Delta_(d+2) M_d - Delta_d M_(d+2)
 = 2((F_(2d+2)-F_(2d-2))M_d
       - 2F_(2d-2)F_(2d)).                         (13)
```

Since `F_(2d+2)-F_(2d-2) > 2F_(2d-2)`, (12) makes (13) strictly positive.
Thus `Delta_d/M_d` increases strictly with `d`.  By (10), so does
`tr(P_(r,s))/M_d`.  At the same time (11) shows that `-4/M_d^2` increases.
Consequently

```text
L(W_r)^2 = (tr(P_(r,s))/M_d)^2 - 4/M_d^2
```

increases strictly with `r`.

Apruzzese--Cong's maximum theorem gives `L(W_(a-1))<L(H)`.  Together with
(1), (3), and the strict monotonicity just proved, this establishes

```text
W_(m+1) < W_(m+2) < ... < W_(2m) < H
```

simultaneously for both score orders.  Every level is a singleton, so the
consecutive pairs in this chain are exactly all covers in both orders.

