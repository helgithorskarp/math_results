# The canonical Lucas `(a,b)=(5,6)` family

## Exact theorem

Let `F_0=0`, `F_1=1`, and

```text
F_(n+1)=e1 F_n+e2 F_(n-1)
```

in `Z[e1,e2]`. Write `{n choose r}_F` for the associated Lucas
binomial. For every integer `k>=1`, put

```text
D_k={5k+6 choose 6}_F-{6k+5 choose 5}_F.                (1)
```

This is the forced-sign normalization of the canonical comparison
`(a,b,c,d)=(5,6,5k,6k)`. Its weighted degree is `30k`, where
`deg(e1)=1` and `deg(e2)=2`.

**Theorem.** `D_1=0`. For every `k>=2`, `D_k` is Schur-positive in
two variables, with exact support

```text
[s_(30k-r,r)]D_k = 0       for 0<=r<=5,
[s_(30k-r,r)]D_k > 0       for 6<=r<=15k.               (2)
```

The first nonzero coefficient is

```text
[s_(30k-6,6)]D_k=1.                                     (3)
```

Together with the previously published canonical `(2,6)`, `(3,6)`,
and `(4,6)` results, this closes the last interior canonical `b=6`
ray. The proof below is independent of their positivity theorems.

## Exact ordinary Schur layers

Let `B(n,r)` be the homogeneous two-variable lift of the Gaussian
binomial `[n choose r]_q`, and set

```text
H_k=B(5k+6,6)-B(6k+5,5).                                (4)
```

For a homogeneous symmetric polynomial `X` of degree `N`, its unique
lower-half expansion is

```text
X=sum_(0<=i<=N/2)x(i)e2^i h_(N-2i),
x(i)=[q^i](1-q)X(q,1).                                  (5)
```

Write `h_k(i)` for the layers of `H_k`. With every restricted-
partition function assigned value zero on negative arguments, define

```text
P6(n)=#{(a,b,c,d,e) in N^5:2a+3b+4c+5d+6e=n},
P5(n)=#{(a,b,c,d) in N^4:2a+3b+4c+5d=n}.                (6)
```

Expanding the two Gaussian numerators through their middle degree
gives, for `0<=i<=15k`,

```text
h_k(i)
 = P6(i)
   -sum_(1<=nu<=6)P6(i-5k-nu)
   +sum_(1<=mu<nu<=6)P6(i-10k-mu-nu)
   -P5(i)
   +sum_(1<=nu<=5)P5(i-6k-nu)
   -sum_(1<=mu<nu<=5)P5(i-12k-mu-nu).                  (7)
```

This truncation is exact. Three width-six numerator factors have
least degree `15k+6`, while three width-five factors have least degree
`18k+6`.

Because `P6(i)=P5(i)` for `0<=i<6`, equations (5)--(7) give, for
every `k>=3`, the exact two-step recurrence

```text
H_k=e2^30 H_(k-2)+e2^6 K_k,                             (8)
K_k=sum_(0<=s<=15k-6)r_k(s)e2^s h_(30k-12-2s),          (9)
r_k(s)=h_k(s+6)-h_(k-2)(s-24).                         (10)
```

Thus (8) is an identity of symmetric polynomials obtained from all
lower-half layers, not a recurrence inferred from finite data.

## Restricted-partition quasipolynomials

Define

```text
T(n)=#{(a,b,c,d,e) in N^5:a+2b+3c+3d+5e=n},
U(n)=#{(a,b,c,d) in N^4:a+2b+3c+5d=n}.                 (11)
```

Splitting parity in (6) gives

```text
P6(2n)  =T(n)+T(n-4),       P6(2n+1)=T(n-1)+T(n-2),
P5(2n)  =U(n)+U(n-4),       P5(2n+1)=U(n-1)+U(n-2).    (12)
```

The exact period-30 quasipolynomials are

```text
T(n)=n^4/2160+7n^3/540+n^2/8+alpha_(n mod 3)n
     +beta_(n mod 30),
U(n)=n^3/180+11n^2/120+9n/20+delta_(n mod 30),          (13)
```

where, in residue order beginning at zero,

```text
540 alpha = 279,239,259,

2160 beta =
 2160, 905, 928,2025, 608,1225,2160, 473,1360,1593,
 1040,1225,1728, 905, 928,2025,1040, 793,2160, 473,
 1360,2025, 608,1225,1728, 905,1360,1593,1040, 793,

360 delta =
 360,163,248,243,136,275,288,163,248,171,
 280,203,288,163,176,315,208,203,288, 91,
 320,243,208,203,216,235,248,243,208,131.              (14)
```

Both universal checkers prove these formulas without interpolation by
summing all residue polynomials and checking

```text
sum_(n>=0)T(n)z^n=1/((1-z)(1-z^2)(1-z^3)^2(1-z^5)),
sum_(n>=0)U(n)z^n=1/((1-z)(1-z^2)(1-z^3)(1-z^5)).      (15)
```

In particular, for every nonnegative argument,

```text
n^4/2160+7n^3/540+n^2/8+(239/540)n+473/2160
 <= T(n)
 <= n^4/2160+7n^3/540+n^2/8+(279/540)n+1,

n^3/180+11n^2/120+9n/20+91/360
 <= U(n)
 <= n^3/180+11n^2/120+9n/20+1.                         (16)
```

## Universal adjacent-layer certificate

For each complete even/odd pair in (9), set

```text
A_j=r_k(2j),                    C_j=2r_k(2j)-r_k(2j+1). (17)
```

The universal inequalities are

```text
A_j>=0,                         C_j>=0.                  (18)
```

Write `k=2t+rho`, where `rho` is zero or one. The exclusive domains
are

```text
rho                0             1
A domain         j<15t-2       j<15t+5
C domain         j<15t-3       j<15t+5.                 (19)
```

For even `k`, the final `A` in (19) is the unpaired middle layer; all
earlier `A` values participate in complete pairs. For odd `k`, every
layer belongs to a complete pair.

Substitution of (12) into (7) and (10) expresses every quantity in
(17) as a signed sum of explicit `T(j+ut+v)` and `U(j+ut+v)` terms.
Both certificate programs build these terms directly and compare them
definitionally with (7)--(10) through `k=200` as a diagnostic check.

For `t>=60`, zero, the endpoints in (19), and every activation
threshold partition the four parity/quantity families into 216 stable
affine cells. Sixteen initial cells have constant endpoints; every
active argument there has zero `t`-slope, making exact evaluation at
`t=60` universal on those cells.

On every other cell, select the lower or upper bound in (16) according
to the sign of each occurrence. This gives a rigorous quartic lower
bound `L(t,j)`. For a cell `a(t)<=j<=b(t)`, substitute

```text
t=60+x,
j=a(t)+(b(t)-a(t))z,                 x>=0, 0<=z<=1.       (20)
```

The resulting 1,000 degree-four Bernstein coefficients in `z` all
lie in `QQ_+[x]`. Hence (18) holds for every `t>=60`. Direct exact
evaluation proves the finite complement `3<=k<120`.

The SymPy certificate record has SHA-256

```text
304a65abfeacfc29317c2cc4cdc8a9cc99d4c28c3d5bc8a777bff027348f88f5. (21)
```

The independent standard-library `Fraction` implementation uses a
separate sparse polynomial engine and compact record format. Its
certificate SHA-256 is

```text
3f68c7a42bcc579631f6a8053a841b9fea12f196ee562f88cfd496ac89e9d18c. (22)
```

## Lucas transport, pairing, and endpoints

Let `tau(e1)=e1` and `tau(e2)=-e2`. Then `tau(h_n)=F_(n+1)` and `tau`
sends homogeneous Gaussian binomials to Lucas binomials. Here
`D_k=tau(H_k)`. Both shifts in (8) are even, so

```text
D_k=e2^30 D_(k-2)+e2^6 R_k,              k>=3,
R_k=tau(K_k)
   =sum_s (-1)^s r_k(s)e2^s F_(30k-11-2s).              (23)
```

For

```text
ell(n,r)=[s_(n-r,r)]F_(n+1),                              (24)
```

the Lucas recurrence and one-box Pieri rule give, for every `m>=3`,

```text
[s_(m-1-r,r)](F_m-2e2 F_(m-2))
 =ell(m-2,r)+ell(m-3,r-2)+ell(m-4,r-2)>=0.               (25)
```

Put `B_j=r_k(2j+1)=2A_j-C_j` and `m=30k-11-4j`. Every complete pair
in (23) becomes

```text
e2^(2j)(A_j F_m-B_j e2 F_(m-2))
 =e2^(2j)(A_j(F_m-2e2 F_(m-2))+C_j e2 F_(m-2)).          (26)
```

Equations (18) and (25) make each pair Schur-positive. For odd `k`,
the last pair has `m=3`. For even `k`, the last complete pair has
`m=5`, followed by the nonnegative unpaired term

```text
r_k(15k-6)e2^(15k-6)F_1.                                (27)
```

Thus every endpoint is covered. Moreover `r_k(0)=1` and `r_k(1)=0`,
so the first complete block is `F_(30k-11)`, whose Schur coefficients
are strictly positive throughout its two-row support. After the factor
`e2^6`, it proves strict positivity for all `6<=r<=15k` and gives
(3).

The direct bases are `D_1=0` and `D_2`; their canonical Schur-row
record has SHA-256

```text
a81cde2c90ed902f5e0f02012969e532e497a9bcc4496169fffa96540be84ea9. (28)
```

The least nonzero base coefficient is `(coefficient,k,r)=(1,2,6)`.
Equations (23)--(28) prove the theorem by induction on each parity.

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
affine cells: 216; exact cells: 16; Bernstein polynomials: 1000
certificate SHA-256: 304a65abfeacfc29317c2cc4cdc8a9cc99d4c28c3d5bc8a777bff027348f88f5
independent certificate SHA-256: 3f68c7a42bcc579631f6a8053a841b9fea12f196ee562f88cfd496ac89e9d18c
least nonzero Lucas Schur coefficient: (1, 2, 6)
```

On the publication machine the two universal certificate programs
each require about nine minutes on one CPU core; the layer and sparse
audits take seconds. All arithmetic is exact. There is no floating
point, randomness, interpolation, modular reconstruction, solver, or
external generated proof data.

`verify_symbolic.py` and `verify_fraction.py` independently prove the
universal affine-cell certificate. `verify_layers.py` checks q-Pascal,
the restricted-partition formula, recurrence, pairing, both endpoint
regimes, strict support, and bases. `verify_sparse.py` starts from the
Sagan--Savage lucasnomial recurrence in sparse `Z[e1,e2]` and checks
literal polynomial identities. The finite ranges in the latter two
programs audit the universal proof rather than supply its quantifier.

The proof trusts CPython integer and `Fraction` arithmetic; the SymPy
certificate additionally trusts SymPy rational-polynomial arithmetic.
The theorem should remain provisional until an independent researcher
rebuilds the affine translation, 216 activation cells, residue bounds,
pairing, and the odd/even endpoints.

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
  the Gaussian partition method behind the neighboring width-six
  analysis: https://arxiv.org/abs/1311.4480

Targeted live primary-source searches on 2026-09-19 found no
Lucas-Schur theorem for the canonical `(5,6)` family. At target
selection, the committed Discovery Net contained the `(2,6)` and
`(3,6)` rays, while the source-published `(4,6)` result was absent
after an uncommitted graph receipt. No `(5,6)` contribution was found.
The novelty claim here is only “apparently new relative to the searched
primary sources and committed graph,” not a claim of historical
priority.
