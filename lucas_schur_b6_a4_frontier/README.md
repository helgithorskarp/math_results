# The canonical Lucas `(a,b)=(4,6)` family

## Exact theorem

Let `F_0=0`, `F_1=1`, and

```text
F_(n+1)=e1 F_n+e2 F_(n-1)
```

in `Z[e1,e2]`. Write `{n choose r}_F` for the associated Lucas
binomial. For every integer `k>=2`, set

```text
D_k={3k+4 choose 4}_F-{2k+6 choose 6}_F.                (1)
```

This is the forced-sign normalization of the canonical comparison
`(a,b,c,d)=(4,6,2k,3k)`. It has weighted degree `12k`, where
`deg(e1)=1` and `deg(e2)=2`.

**Theorem.** `D_2=0`. For every `k>=3`, `D_k` is Schur-positive in
two variables, with exact support

```text
[s_(12k-r,r)]D_k = 0       for 0<=r<=4,
[s_(12k-r,r)]D_k > 0       for 5<=r<=6k.                (2)
```

In particular, the first nonzero coefficient is

```text
[s_(12k-5,5)]D_k=1.                                    (3)
```

The proof below is an exact all-parameter Schur-layer recurrence. It
uses no unproved result for the neighboring canonical `(2,6)` or
`(3,6)` families.

## Ordinary Gaussian layers

Let `B(n,r)` be the homogeneous two-variable lift of the Gaussian
binomial `[n choose r]_q`, and put

```text
H_k=B(2k+6,6)-B(3k+4,4).                                (4)
```

For a homogeneous symmetric polynomial `X` of degree `N`, its unique
lower-half expansion is

```text
X=sum_(0<=i<=N/2) x(i)e2^i h_(N-2i),
x(i)=[q^i](1-q)X(q,1).                                  (5)
```

Write `h_k(i)` for the layers of `H_k`. With every restricted-
partition function below assigned value zero on negative arguments,
define

```text
P(n)=#{(a,b,c,d,e) in N^5:2a+3b+4c+5d+6e=n},
Q(n)=#{(a,b,c) in N^3:2a+3b+4c=n}.                      (6)
```

Expanding the Gaussian product numerators only through their middle
degree gives, for `0<=i<=6k`,

```text
h_k(i)
 = P(i)
   -sum_(1<=nu<=6)P(i-2k-nu)
   +sum_(1<=mu<nu<=6)P(i-4k-mu-nu)
   -Q(i)
   +sum_(1<=nu<=4)Q(i-3k-nu).                           (7)
```

This truncation is exact: three width-six numerator factors have
least degree `6k+6`, while two width-four numerator factors have least
degree `6k+3`.

For `k>=13`, define

```text
r_k(s)=h_k(s+5)-h_(k-10)(s-55),       0<=s<=6k-5.       (8)
```

Because `h_k(i)=P(i)-Q(i)=0` for `0<=i<5`, equation (5) gives the
exact ten-step recurrence

```text
H_k=e2^60 H_(k-10)+e2^5 K_k,                            (9)
K_k=sum_(0<=s<=6k-5)r_k(s)e2^s h_(12k-10-2s).           (10)
```

Thus (9) is an identity of symmetric polynomials, not a recurrence
inferred from finite data.

## Restricted-partition quasipolynomials

Define

```text
T(n)=#{(a,b,c,d,e) in N^5:a+2b+3c+3d+5e=n},
W(n)=#{(a,b,c) in N^3:a+2b+3c=n}.                       (11)
```

Splitting parity in (6) gives

```text
P(2n)  =T(n)+T(n-4),       P(2n+1)=T(n-1)+T(n-2),
Q(2n)  =W(n),              Q(2n+1)=W(n-1).              (12)
```

The exact quasipolynomials are

```text
T(n)=n^4/2160+7n^3/540+n^2/8+alpha_(n mod 3)n
     +beta_(n mod 30),
W(n)=n^2/12+n/2+gamma_(n mod 6),                         (13)
```

where, in residue order beginning at zero,

```text
540 alpha = 279,239,259,
12 gamma  = 12,5,8,9,8,5,

2160 beta =
 2160, 905, 928,2025, 608,1225,2160, 473,1360,1593,
 1040,1225,1728, 905, 928,2025,1040, 793,2160, 473,
 1360,2025, 608,1225,1728, 905,1360,1593,1040, 793.     (14)
```

Both universal checkers prove (13)--(14), without interpolation, by
summing the residue polynomials and verifying

```text
sum_(n>=0)T(n)z^n=1/((1-z)(1-z^2)(1-z^3)^2(1-z^5)),
sum_(n>=0)W(n)z^n=1/((1-z)(1-z^2)(1-z^3)).              (15)
```

In particular, for every nonnegative argument,

```text
n^4/2160+7n^3/540+n^2/8+(239/540)n+473/2160
 <= T(n)
 <= n^4/2160+7n^3/540+n^2/8+(279/540)n+1,

n^2/12+n/2+5/12 <= W(n) <= n^2/12+n/2+1.               (16)
```

## Universal adjacent-layer certificate

Pair the layers of `K_k` by setting, for `0<=j<3k-2`,

```text
A_j=r_k(2j),                    C_j=2r_k(2j)-r_k(2j+1). (17)
```

The key universal inequalities are

```text
A_j>=0,                         C_j>=0.                  (18)
```

Write `k=2t+rho`, with `rho` zero or one. Substituting (12) into
(7)--(8) expresses each quantity in (17) as a signed sum of explicit
terms `T(j+ut+v)` and `W(j+ut+v)`. The two certificate programs build
these terms directly and compare them definitionally with (7)--(8)
through `k=200` as a diagnostic check.

For `t>=60`, zero, the exclusive endpoint `3k-2`, and every affine
activation threshold partition the four parity/quantity cases into
170 stable affine cells. Fourteen initial cells have constant
endpoints; every active restricted-partition argument there has zero
`t`-slope, so exact evaluation at `t=60` is universal on those cells.

On each remaining cell, use the appropriate lower or upper bound in
(16), according to the sign of the occurrence. This produces a
quartic lower bound `L(t,j)`. If the cell is `a(t)<=j<=b(t)`, make the
substitution

```text
t=60+x,
j=a(t)+(b(t)-a(t))z,                 x>=0, 0<=z<=1.       (19)
```

The 780 resulting degree-four Bernstein coefficients in `z` all lie
in `QQ_+[x]`. Therefore (18) holds for every `t>=60`. Direct exact
evaluation proves the finite complement `13<=k<120`.

The SymPy implementation's canonical certificate record has SHA-256

```text
83bca8bd00e22bcbce864fec0631fc605a9971b448de643b0d0b2929947ee43c. (20)
```

The independent standard-library `Fraction` implementation uses a
separate sparse polynomial engine and compact record format. Its
certificate SHA-256 is

```text
b3d03a7af68e48b7911f6816cdd3ddd404ae6239732193a921954b2bfa6c03b3. (21)
```

## Lucas transport and positive pairing

Let `tau(e1)=e1` and `tau(e2)=-e2`. Then `tau(h_n)=F_(n+1)` and `tau`
sends homogeneous Gaussian binomials to Lucas binomials. Since
`D_k=-tau(H_k)`, the odd shift in (9) changes the sign and gives

```text
D_k=e2^60 D_(k-10)+e2^5 R_k,             k>=13,
R_k=tau(K_k)
   =sum_s (-1)^s r_k(s)e2^s F_(12k-9-2s).               (22)
```

For

```text
ell(n,r)=[s_(n-r,r)]F_(n+1),                              (23)
```

the Lucas recurrence and the one-box Pieri rule give, for `m>=3`,

```text
[s_(m-1-r,r)](F_m-2e2 F_(m-2))
 =ell(m-2,r)+ell(m-3,r-2)+ell(m-4,r-2)>=0.               (24)
```

Put `B_j=r_k(2j+1)=2A_j-C_j` and `m=12k-9-4j`. Each adjacent pair
in (22) is

```text
e2^(2j)(A_j F_m-B_j e2 F_(m-2))
 =e2^(2j)(A_j(F_m-2e2 F_(m-2))+C_j e2 F_(m-2)).          (25)
```

Equations (18) and (24) make every pair Schur-positive. There are
exactly `3k-2` complete pairs, and the last has `m=3`; hence no middle
layer is omitted.

Moreover `A_0=C_0=1`. The first pair is

```text
F_(12k-9)-e2 F_(12k-11)=e1 F_(12k-10),                  (26)
```

whose Schur coefficients are positive throughout its two-row support.
After the factor `e2^5`, this proves strict positivity for every
`5<=r<=6k` in the induction step. Exact q-Pascal calculation supplies
the ten bases `D_3,...,D_12`; their canonical Schur-row record has
SHA-256

```text
edd5e288ca47db07f055ffd1220e1dadf40478f609d5a3738ff348e98035fb4e. (27)
```

The least nonzero base coefficient is `(coefficient,k,r)=(1,3,5)`.
Equations (22)--(27) prove (2)--(3) by induction. Finally, `D_2=0`
follows from symmetry of the Lucas binomial.

## Reproduction and trust boundary

Run from this directory with CPython 3.11 and SymPy 1.14.0:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_fraction.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_layers.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_sparse.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_symbolic.py
sha256sum -c SHA256SUMS
```

Expected output includes

```text
affine cells: 170; exact cells: 14; Bernstein polynomials: 780
certificate SHA-256: 83bca8bd00e22bcbce864fec0631fc605a9971b448de643b0d0b2929947ee43c
independent certificate SHA-256: b3d03a7af68e48b7911f6816cdd3ddd404ae6239732193a921954b2bfa6c03b3
least nonzero Lucas Schur coefficient: (1, 3, 5)
```

All arithmetic is exact. There is no floating point, randomness,
interpolation, modular reconstruction, solver, or external generated
proof data. `verify_symbolic.py` and `verify_fraction.py` independently
prove the universal affine-cell certificate. `verify_layers.py` checks
q-Pascal, the restricted-partition formula, recurrence, pairing,
support, and bases. `verify_sparse.py` starts from the Sagan--Savage
lucasnomial recurrence in sparse `Z[e1,e2]` and checks literal
polynomial identities. The finite ranges in the latter two programs
audit the universal proof rather than supply its quantifier.

The proof trusts CPython integer and `Fraction` arithmetic; the SymPy
certificate additionally trusts SymPy rational-polynomial arithmetic.
The theorem should remain provisional until an independent researcher
rebuilds the affine translation, activation cells, residue bounds,
pairing, and endpoint coverage.

## Primary-source and graph status

- François Bergeron, *A (q,t)-Overview of q-Analogs*, arXiv:2608.30979,
  states the Lucas comparison and reports computation only through
  `ad=bc<=36`: https://arxiv.org/abs/2608.30979
- Bruce Sagan and Carla Savage, *Combinatorial interpretations of
  binomial coefficient analogues related to Lucas sequences*,
  arXiv:0911.3159, supplies the lucasnomial framework:
  https://arxiv.org/abs/0911.3159
- Fabrizio Zanello, *Zeilberger's KOH theorem and the strict
  unimodality of q-binomial coefficients*, arXiv:1311.4480, records
  the KOH/partition method underlying the neighboring width-six work:
  https://arxiv.org/abs/1311.4480

Targeted live primary-source searches on 2026-09-19 found no
Lucas-Schur theorem for the canonical `(4,6)` family. At target
selection, the committed Discovery Net contained neighboring
provisional theorems for `(2,6)` and `(3,6)`, but no `(4,6)` result;
the `(3,6)` node explicitly proposed `(4,6)` as its next frontier. The
novelty claim here is only “apparently new relative to the searched
primary sources and committed graph,” not a claim of historical
priority.
