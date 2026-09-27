# A complete Gaussian beta row beyond N=8

27 September 2026. Complete author proof with finite exact scalar
certificates. Independent review and formalization are pending.
The unrestricted dimension-three Gaussian majorisation question remains open.

## 1. The complete-row theorem

Let mu be a bounded-support Borel probability measure on R3, let T be
1-Lipschitz on its support, and let s>0. Put

```
C=(2 pi s)^(-3/2),  f=mu*gamma_s,  g=(T#mu)*gamma_s,
H(u)=integral(g-Cu)_+ - integral(f-Cu)_+,   0<=u<=1,
a_j=integral_0^1 u^j H(u)du,
b_(N,j)=(N+1) binom(N,j) integral_0^1 u^j(1-u)^(N-j) H(u)du.
```

**Theorem.** Every entry in row N=11 is nonnegative:

```
b_(11,j)>=0,                  0<=j<=11.                 (1)
```

Consequently every entry of every row N<=11 is nonnegative. All these
inequalities are strict unless T preserves every distance on supp(mu).
There are no radius, atom-count, weight, covariance, variance or small-loss
conditions. Diffuse laws and repeated atoms are included.

For clarity, the new scalar work closes the four leftmost entries of
row11. Its eight other entries are supplied by the credited seven-factor
theorem. The earlier eighth-row and retained-interaction results are
preserved inputs, not new claims of this packet. The advance is completion
of the entire row and its resulting cone of energy comparisons.

Here are quantitative bounds for the four entries. Define the marked
replica averages B_m in Section2, and put

```
epsilon_2=1/300,   epsilon_3=1/6000,
epsilon_4=1/30000, epsilon_5=1/60000.
```

For j=0,1,2,3, with m=j+2, the proof gives

```
b_(11,j) >= 12 binom(11,j) epsilon_m B_m/(4s).           (2)
```

This does not sign every row or every beta diagonal, imply unrestricted
Hankel positivity, prove full majorisation, or give a new Kneser--Poulsen
volume theorem. In particular, an arbitrary convex polynomial need not
belong to the finite cone proved here.

## 2. Credited replica identities and the retained-interaction input

Take iid X_i of law mu, put Y_i=T(X_i), and write

```
delta_12=|X1-X2|^2-|Y1-Y2|^2 >=0,
Z_i(t)=(sqrt(1-t)X_i,sqrt(t)Y_i),
Q_m(t)=sum_i |Z_i(t)-mean_m Z(t)|^2,
B_m=E delta_12 integral_0^1 exp(-Q_m(t)/(2s))dt.
```

The Gaussian product identity, differentiation in t and pair
exchangeability give the existing normalizations

```
d_m=C^(1-m) integral(g^m-f^m)=(m-1) B_m/(4s m^(3/2)),
a_j=d_(j+2)/[(j+1)(j+2)]=B_(j+2)/(4s (j+2)^(5/2)).     (3)
```

The positive lift measure eta on [0,1] from the earlier sources satisfies

```
integral u^ell deta(u)=B_(ell+2)/(ell+2)^3.              (4)
```

One explicit definition fixes the entire measure: for z in R6 set
K_x(t,z)=exp(-|z-(sqrt(1-t)x,sqrt(t)Tx)|^2/(2s)),
q_t(z)=E K_X(t,z), and M_t(z)=E delta_12 K_X1(t,z)K_X2(t,z).
Then

```
integral psi(u)deta(u)
 =(2pi s)^(-3) integral_0^1 integral_R6 psi(q_t(z))M_t(z) dz dt.
```

Completion of the square proves (4); eta has total mass B2/8. The measure
is positive because the pair loss is nonnegative. Boundedness and Tonelli
justify these identities for all the inputs under consideration.

We use two consequences of the credited retained-interaction theorem:

```
B_(k+1)<=B_k,
B_(m+2)/B_m >= (B_(m+1)/B_m)^kappa_m,
kappa_m=2(m+1)^2/[m(m+2)]>1,        if B_m>0.           (5)
```

The first follows from the variance increment on adding a replica. For
the second, a short recall of the existing argument makes the dependency
explicit. Condition on t and the first m replicas, and let U,V be iid
displacements of the next two from their centroid. Then

```
Q_(m+2)=Q_m+[(m+1)/(m+2)](|U|^2+|V|^2)-2U.V/(m+2).
```

Tilt the common extra-replica law by
h(U)=exp(-(m+1)|U|^2/(2s(m+2))). Under that common tilted law,
E(U.V)=|E U|^2>=0, so Jensen preserves a lower bound (E h)^2.
If r=E exp(-m|U|^2/(2s(m+1))), another Jensen inequality gives
(E h)^2>=r^kappa_m. Averaging with the common positive marked base
measure and applying Jensen once more proves (5). This proof and its
general added-block version were established in the retained-interaction
source; no new interpolation or quartic estimate is asserted here.

If one B_m vanishes, strict positivity of the exponential implies
delta_12=0 almost everywhere, so every B_k vanishes. We may therefore
divide by B_m whenever the loss is nonzero.

## 3. Shift the moment measure and use a scalar convex dual

For m>=2 define the positive measure dnu_m(u)=u^(m-2)deta(u). Its moments
and the relevant scalar polynomial are

```
integral u^ell dnu_m(u)=B_(m+ell)/(m+ell)^3,
P_(m,q)(u)=sum_(ell=0)^q (-1)^ell binom(q,ell) sqrt(m+ell) u^ell.
```

Using (3)--(4), with j=m-2,

```
integral_0^1 u^j(1-u)^q H(u)du
 =(1/(4s)) integral P_(m,q)(u)dnu_m(u).                (6)
```

For each integer ell>=0 put

```
G_(m,ell)(u)=u^ell-[(m+ell+1)/(m+ell)]^3 u^(ell+1).
```

Its integral is nonnegative by (5):

```
integral G_(m,ell)dnu_m
 =[B_(m+ell)-B_(m+ell+1)]/(m+ell)^3 >=0.               (7)
```

Suppose a,b,c>0 and lambda_ell>=0 give a scalar minorant on [0,1],

```
P_(m,q)(u)>=a-bu+cu^2+sum_ell lambda_ell G_(m,ell)(u). (8)
```

Set r=B_(m+1)/B_m in [0,1]. Combining (5)--(8) yields

```
integral P_(m,q)dnu_m >= B_m h_m(r),
h_m(r)=A-Br+D r^kappa,
A=a/m^3, B=b/(m+1)^3, D=c/(m+2)^3, kappa=kappa_m.      (9)
```

This scalar convex dual has an exact uniform bound. Its unique minimizer
on the nonnegative half-line is r_*=(B/(kappa D))^(1/(kappa-1)). If a
positive rational R is an upper bound for r_*, then

```
h_m(r)>=A-B(1-1/kappa)R   for every r>=0.              (10)
```

Indeed h_m(r_*)=A-B(1-1/kappa)r_*, and B(1-1/kappa)>0. Write
kappa=p/d in lowest terms. The root bound R>=r_* is equivalent to the
entirely rational inequality

```
R^(p-d) >= [B/(kappa D)]^d.                           (11)
```

Thus no fractional-power numerical optimization is a proof premise.
The useful averaging step is the application of (5) to each shifted
moment measure; (8) is not required to be a positive conditional kernel.

## 4. Four exact dual certificates

The following table specifies (8). Every entry a,b,c and every displayed
lambda numerator is divided by 10000. An entry ell:L means
lambda_ell=L/10000; all unlisted multipliers vanish.

| m | q | a numerator | b numerator | c numerator | Nonzero multipliers |
|---|---|---|---|---|---|
| 2 | 11 | 4348 | 28317 | 35514 | 3:29017 |
| 3 | 10 | 2372 | 11387 | 11635 | 4:10857 |
| 4 | 9 | 1720 | 6860 | 6163 | 4:866, 5:4627 |
| 5 | 8 | 1761 | 6225 | 5138 | 5:3568 |

Here are the convex-dual certificates (10)--(11):

| m | kappa | R | Certified lower bound epsilon_m |
|---|---|---|---|
| 2 | 9/4 | 869812/1000000 | 1/300 |
| 3 | 32/15 | 907663/1000000 | 1/6000 |
| 4 | 25/12 | 928934/1000000 | 1/30000 |
| 5 | 72/35 | 938627/1000000 | 1/60000 |

All eight inequalities (11) and A-B(1-1/kappa)R>=epsilon_m are checked
by exact rational arithmetic. They prove h_m>=epsilon_m without sampling.

For completeness here is the finite certificate for all four polynomial
minorants (8). Take D0=2^40. For 2<=n<=13 let
k_n=floor(sqrt(n D0^2)), L_n=k_n/D0, and U_n=(k_n+1)/D0, except that
U_n=L_n when n is an exact square on the grid. Integer square comparisons
verify L_n<=sqrt(n)<=U_n. In P_(m,q) replace a positive monomial's root
by L_(m+ell), and a negative monomial's root by U_(m+ell). Subtract the
rational minorant in (8), obtaining a rational polynomial R_(m,q)(u).
The desired difference is at least R_(m,q)(u) for u in [0,1].

For each of the 64 closed subintervals [i/64,(i+1)/64], write this
polynomial in the degree-q Bernstein basis. Every coefficient is strictly
positive. The four coefficient counts are respectively 768,704,640,576,
for a total of 2688. Since each Bernstein basis function is nonnegative,
this certifies (8) on the whole interval, including every boundary.

Explicitly, if R(u)=sum_j c_j u^j, its power coefficients on [a,a+h]
are p_k=sum_(j=k)^q c_j binom(j,k)a^(j-k)h^k. Its Bernstein coefficients
are beta_i=sum_(k=0)^i p_k binom(i,k)/binom(q,k). The checker constructs
each coefficient using this formula and independently by six midpoint
de Casteljau subdivisions; the arrays agree entry by entry. It also
checks the polynomial identity at q+1 rational points in each interval.
These identity controls do not infer a sign from point samples.

[CERTIFICATE.json](CERTIFICATE.json) contains exactly the rational tables
and subdivision specification. [EXPECTED.json](EXPECTED.json) records
the exact global minima, all four coefficient-array hashes, the rational
convex-dual bounds and complete row coverage. [verify.py](verify.py)
reconstructs the full finite certificate with standard-library integers
and fractions. No floating search result is imported by the checker.

## 5. Close the row and descend to all lower rows

For j=0,1,2,3 take m=j+2 and q=11-j. The four certificates, (6), (9)
and (10) prove (2). For j=4,...,11 one has 11-j<=7, and the credited
seven-factor theorem signs these entries. This proves every entry in (1).

Multiplying a beta kernel by u+(1-u)=1 gives the exact normalized
degree-elevation identity

```
b_(N,j)=[(N+1-j)/(N+2)] b_(N+1,j)
                       +[(j+1)/(N+2)] b_(N+1,j+1).     (12)
```

Both coefficients are positive and sum to one. Descending from row11
therefore signs every row N<=11. The checker verifies both binomial
normalizations and convexity in (12) for all 66 lower-row positions.

If T shortens a pair in supp(mu), continuity gives two neighborhoods
of positive product measure with positive squared loss. Hence every B_m
is positive, and (2) is strict. The credited seven-factor theorem is
also strict in this case. Equation (12) propagates strictness to every
lower row. If no support distance is shortened, all losses vanish and
(3) gives zero for every beta entry. This includes degenerate supports.

Equivalently, Gaussian convolution preserves the energy comparison for
every normalized curvature with a nonnegative Bernstein expansion of
degree11 on [0,1], and for all the lower-degree cones obtained by (12).
Linear terms in the energy cancel because f and g have equal mass.
One may set U(0)=U'(0)=0 and extend U linearly beyond1 after normalizing
the densities by C. This is a finite cone of energies at every input
scale, not all convex energies and not a restricted geometric class.

## 6. Attribution and trust boundary

The replica identities, positive lift, retained-interaction inequality
and seven-factor theorem are credited inputs. The shifted moment
argument and four scalar dual certificates complete a previously open
whole beta row. They do not strengthen the retired quartic/Hankel
interpolation estimate or rely on its non-effective constant.

The Gaussian integrations and Jensen arguments are written mathematics.
The finite scalar premises are computer-assisted, relying on Python's
arbitrary-precision integer and Fraction arithmetic. Normal and optimized
runs verify the same compact expected record. Four damaged certificates
(missing obligation, excessive minorant, false root bound, and false
margin) are rejected. Internal independent algorithms are not external
peer review. No simulation, solver optimality, sampled sign, hidden data
or omitted large artifact is a premise. See [SOURCES.md](SOURCES.md).
