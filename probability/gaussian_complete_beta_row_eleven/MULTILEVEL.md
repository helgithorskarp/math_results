# Multilevel replica inequalities complete beta row twelve

27 September 2026. Complete author proof with exact scalar certificates;
independent mathematical review and formalization are pending. This is a
supplement to the [row-eleven proof](PROOF.md). The unrestricted R3
Gaussian-majorisation question remains open.

## 1. The endpoint and the new averaging step

Let mu be a bounded-support Borel probability measure on R3, let T be
1-Lipschitz on its support, and let s>0. Write

```
C=(2 pi s)^(-3/2),  f=mu*gamma_s,  g=(T#mu)*gamma_s,
H(u)=integral(g-Cu)_+ - integral(f-Cu)_+,
b_(N,j)=(N+1) binom(N,j) integral_0^1 u^j(1-u)^(N-j) H(u)du.
```

**Theorem.** Every b_(N,j) is nonnegative for 0<=j<=N<=12.
All these inequalities are strict if T shortens any distance between
points of supp(mu). There are no restrictions on radius, covariance,
atom count, positive masses, variance or size of the distance loss.

The new work signs the four entries j=1,2,3,4 of row12. The entry j=0
is a credited retained-interaction result; the entries j>=5 follow from
the credited seven-factor theorem. In particular no isolated entry is
being substituted for complete row coverage.

The averaging step combines valid scalar Young inequalities at several
replica counts against the same positive lifted measure. It uses both
the count m=j+2 and higher counts. This enlarges the one-base dual used
in the earlier proof. The individual Young inequalities and the Gaussian
lift are classical or credited inputs; their multilevel combination below
gives the stated complete-row endpoint. No new pointwise sign for an
individual conditional replica configuration is assumed.

Define B_m as in Section2. Set

```
gamma_3=1/500,  gamma_4=1/2500,
gamma_5=1/2500, gamma_6=1/1500.
```

For j=1,2,3,4 and m=j+2 the quantitative conclusion is

```
b_(12,j) >= 13 binom(12,j) gamma_m B_m/(4s m^3).       (1)
```

This extends the finite cone of signed beta energies. It does not prove
an infinite beta diagonal, all convex energies, full majorisation,
unrestricted Hankel positivity or a new Kneser--Poulsen class.

## 2. The common measure and the credited moment bounds

With iid X_i of law mu set Y_i=T(X_i), and define

```
delta_12=|X1-X2|^2-|Y1-Y2|^2 >=0,
Z_i(t)=(sqrt(1-t)X_i,sqrt(t)Y_i),
Q_k(t)=sum_i |Z_i(t)-mean_k Z(t)|^2,
B_k=E delta_12 integral_0^1 exp(-Q_k(t)/(2s))dt.
```

The credited Gaussian product identity and positive R6 lift give a
finite positive measure eta on [0,1] such that

```
integral u^ell deta(u)=B_(ell+2)/(ell+2)^3,
integral_0^1 u^ell H(u)du=B_(ell+2)/(4s (ell+2)^(5/2)). (2)
```

Explicitly, put K_x(t,z)=exp(-|z-Z_x(t)|^2/(2s)),
q_t(z)=E K_X(t,z), and M_t(z)=E delta_12 K_X1(t,z)K_X2(t,z).
The measure eta is the pushforward under q_t(z) of
(2 pi s)^(-3) M_t(z) dz dt. This defines a single measure for all the
replica counts used below. Completion of the square proves the first
identity in (2); differentiation of the Gaussian product formula along
t and pair exchangeability prove the second. These identities are
recorded in the [retained-interaction source](../gaussian_replica_interaction/PROOF.md).

For m>=2 define dnu_m(u)=u^(m-2)deta(u) and

```
P_(m,q)(u)=sum_(ell=0)^q (-1)^ell binom(q,ell) sqrt(m+ell) u^ell.
```

Then

```
integral u^ell dnu_m=B_(m+ell)/(m+ell)^3,
integral_0^1 u^(m-2)(1-u)^q H(u)du
             =(1/(4s)) integral P_(m,q) dnu_m.          (3)
```

The credited retained-interaction theorem supplies, for every k>=2,

```
B_(k+1)<=B_k,
B_(k+2)/B_k >= (B_(k+1)/B_k)^kappa_k,
kappa_k=2(k+1)^2/[k(k+2)],                if B_k>0.     (4)
```

For clarity, (4) keeps the interaction of two extra iid replicas. Given
the first k replicas, subtract their centroid from the next two to get
U,V. The variance increment is

```
[(k+1)/(k+2)](|U|^2+|V|^2)-2U.V/(k+2).
```

Under the common Gaussian tilt,
E(U.V)=|E U|^2>=0. Jensen for the interaction exponential, for the
one-replica power, and finally for the common positive marked base
measure gives the second inequality in (4). This is the existing proof,
not a new interpolation assertion. The first inequality follows from
the nonnegative variance increment on adding one point.

If one B_k=0, positivity of the exponential implies delta_12=0 almost
everywhere, so all B_k vanish. Equation (2), polynomial approximation
and continuity of H then give H=0. Otherwise all B_k>0. Boundedness
justifies all the Gaussian integrals and the finite sums in this proof.

## 3. Multilevel Young inequalities

Here is the reusable scalar mechanism. For k>=2 write kappa=kappa_k=p/d
in lowest terms. Choose rational v>0, R>0 and a such that

```
R^(p-d)>=(v/kappa)^d,
a>=v(1-1/kappa)R.                                    (5)
```

The convex function r^kappa-vr has its unique minimum on r>=0 at
r_*=(v/kappa)^(1/(kappa-1))<=R. Consequently

```
r^kappa-vr+a >= a-v(1-1/kappa)R >=0  for every r>=0.
```

Combining with (4) proves the homogeneous averaged inequality

```
B_(k+2)-v B_(k+1)+a B_k >=0.                          (6)
```

For a base m and a shift ell>=0 put k=m+ell and define

```
Y_(m,ell;v,a)(u)
 =u^ell [((k+2)/k)^3 u^2-v((k+1)/k)^3 u+a],
G_(m,ell)(u)=u^ell [1-((k+1)/k)^3 u].
```

The common moment measure in (3) is essential: it gives simultaneously

```
integral Y_(m,ell;v,a) dnu_m
 =[B_(k+2)-v B_(k+1)+a B_k]/k^3 >=0,
integral G_(m,ell) dnu_m=[B_k-B_(k+1)]/k^3 >=0.        (7)
```

Thus any finite list of parameters satisfying (5), multipliers
lambda_i,theta_h>=0, and a scalar inequality on [0,1],

```
P_(m,q)(u) >= gamma
           +sum_i lambda_i Y_(m,ell_i;v_i,a_i)(u)
           +sum_h theta_h G_(m,h)(u),                 (8)
```

gives

```
integral P_(m,q) dnu_m >= gamma B_m/m^3.               (9)
```

All parameters are fixed constants, independent of mu,T,s and B.
The following certificates make (8) concrete at every remaining row12
position. No feasibility or optimality assertion about a numerical
optimization problem is needed.

## 4. Exact scalar certificates

[MULTILEVEL_CERTIFICATE.json](MULTILEVEL_CERTIFICATE.json) specifies every
rational parameter in (5)--(8). Here is its coverage:

| m | q | gamma | Young shifts, with multiplicity | Monotonicity shift |
|---|---|---|---|---|
| 3 | 11 | 1/500 | 0,0,6 | 11 |
| 4 | 10 | 1/2500 | 0,0,6,7 | 11 |
| 5 | 9 | 1/2500 | 0,0,7 | 11 |
| 6 | 8 | 1/1500 | 0,0,8 | 11 |

There are thirteen Young inequalities. The fields `slope`,
`critical_upper`, `intercept`, and `multiplier` mean v,R,a,lambda,
respectively. Both inequalities (5) are verified with rational powers
of integer exponent. This avoids evaluating fractional powers.

For each integer n needed in P_(m,q), let D=2^48 and choose integers
k_n=floor(sqrt(n D^2)). Set L_n=k_n/D and U_n=(k_n+1)/D, taking U_n=L_n
when equality holds. Squared integer comparisons prove
L_n<=sqrt(n)<=U_n. In P replace each positive coefficient's square root
by L_n and each negative coefficient's root by U_n. Subtract the right
side of (8). The resulting rational polynomial is a lower bound for
the desired difference on [0,1]. Its degree is twelve in all four cases.

On each of the 64 intervals [i/64,(i+1)/64], this polynomial has strictly
positive coefficients in the degree-twelve Bernstein basis. There are
4*64*13=3328 coefficients. The nonnegative Bernstein basis functions
sum to one, so the certificates cover the entire closed interval.

The exact checker constructs every coefficient by both affine power
substitution and six midpoint de Casteljau subdivisions; the results
agree entry by entry. It also checks 3328 rational polynomial identity
controls. Those controls check identities only; coefficient positivity
is the sign proof. Five deliberate corruptions are rejected: an omitted
case, an excessive margin, an invalid critical-point bound, an insufficient
intercept and a negative multiplier.

[multilevel_verify.py](multilevel_verify.py) uses standard-library
integers and fractions. Its shared polynomial routines are the unchanged
[verify.py](verify.py) from the row11 packet. The exact record and all
coefficient-array hashes are in
[MULTILEVEL_EXPECTED.json](MULTILEVEL_EXPECTED.json). An exploratory
floating LP suggested the rational constants; its grid, package and
optimization status are not proof premises.

## 5. Row coverage, descent and strictness

For j=1,2,3,4 take m=j+2 and q=12-j. Equations (3), (8) and (9) give (1).
For j=0 use the credited retained-interaction bound

```
b_(12,0)>=13 sqrt(2) d_2/1000,
d_2=C^(-1) integral(g^2-f^2)=B_2/(8 sqrt(2)s).
```

For j=5,...,12 the credited seven-factor theorem applies since 12-j<=7.
This proves the entire row. The exact identity

```
b_(N,j)=((N+1-j)/(N+2)) b_(N+1,j)
        +((j+1)/(N+2)) b_(N+1,j+1)
```

then gives every lower row. Both coefficients are strictly positive
and sum to one; the checker audits all 78 lower-row positions.

If a support pair is strictly shortened, continuity gives a product
neighborhood of positive mu^2 mass with delta_12>0. Hence every B_m>0.
The positive constants in (1), the strict credited endpoint bounds and
degree elevation give strictness at all stated positions. Conversely,
distance preservation makes delta_12 vanish, hence all the signed
moments and hinges vanish. Point laws and repeated atoms are included.

The analytic input (4) and Gaussian integrations are written mathematics,
not formalized by the scalar checker. The proof stays compatible with
the accepted rank-six conditional obstruction: (6)--(7) concern averaged
replica laws. No conclusion about all remaining beta obligations or the
unrestricted coupling defect follows. See [SOURCES.md](SOURCES.md) for
dependency status and attribution.
