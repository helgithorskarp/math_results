# Independent acceptance: complete Gaussian beta row twelve

## Verdict

**Accept for correctness in the stated scope.** Let `mu` be any
bounded-support Borel probability measure on `R3`, let `T` be 1-Lipschitz on
its support, and let `s>0`. For the normalized hinge difference and beta
coefficients defined in the target, every

```text
b_(N,j) >= 0,                    0 <= j <= N <= 12.
```

If `T` strictly shortens any support distance, every displayed inequality is
strict. There are no radius, covariance, atom-count, weight, variance, or
small-loss hypotheses. This is a universal finite cone of signed Gaussian
energies. It is not full Gaussian-convolution majorisation, a sign theorem for
all beta rows, unrestricted Hankel positivity, or a Kneser--Poulsen result.

The exact target is Discovery Net artifact
`bafkreicc53nkopfdrq5gi6ww4vnqlfagsgkskzbqlsavujucvi5f7x6hzy` at source
commit `a0147abea179b06e528f0bebdd511d5adeb07b00`. The material retained-iid
interaction dependency is original6362
`bafkreicp5fr5uoquxbrunjvq7idskx5rg47hsxedl4qnastmppakpngaba` at source
commit `49a7d4c0828418b342e209b91c8753173a51ed3b`. Nineteen exact source files
from those commits are content-pinned in `TARGET_INPUTS.json`.

## Analytic mechanism

For iid replicas, write

```text
delta_12 = |X1-X2|^2-|T(X1)-T(X2)|^2,
Q_k(t)   = sum_i |Z_i(t)-mean_k Z(t)|^2,
B_k      = E delta_12 integral_0^1 exp(-Q_k(t)/(2s)) dt.
```

The common positive lift measure `eta` on `[0,1]` satisfies

```text
integral u^ell d eta = B_(ell+2)/(ell+2)^3,
integral_0^1 u^ell H(u)du = B_(ell+2)/(4s(ell+2)^(5/2)).
```

The normalization follows by completing the square in the six-dimensional
Gaussian product, and differentiation in `t` followed by pair exchangeability
gives the second identity. The checked product normalization agrees with
equation (61) of the cited
[Aishwarya--Li source](https://arxiv.org/html/2609.07041v2). Tonelli and
differentiation are justified by bounded support and the stated integrability.

The retained-interaction inequality used by the target is valid. Conditional
on the first `m` replicas, the increment for `ell` iid displacements is

```text
sum_i (n-1)|U_i|^2/n - (2/n) sum_(i<j) U_i.U_j,
n=m+ell.
```

After a common Gaussian tilt, independence gives
`E(U_i.U_j)=|E U|^2>=0`; Jensen therefore retains, rather than discards with
the wrong sign, the cross interaction. A second Jensen step compares the
one-replica factors because

```text
alpha=(n-1)(m+1)/(nm)=1+(ell-1)/(nm) >= 1.
```

The final Jensen step against the common positive marked base measure proves

```text
B_(m+ell)/B_m >= (B_(m+1)/B_m)^p_(m,ell),
p_(m,ell)=ell(m+ell-1)(m+1)/(m(m+ell)).
```

For `ell=2` this gives
`B_(k+2)/B_k >= (B_(k+1)/B_k)^kappa_k`, with
`kappa_k=2(k+1)^2/[k(k+2)]`. The ordinary variance increment gives
`B_(k+1)<=B_k`. If one `B_k` vanishes, positivity of the exponential forces
the marked loss to vanish almost everywhere, so the undivided conclusion is
valid. This audit checks the full general retained-interaction theorem, not
only the four instances needed by row twelve.

## Multilevel scalar certificates

For `m=j+2`, `q=12-j`, set `d nu_m=u^(m-2)d eta` and

```text
P_(m,q)(u)=sum_(ell=0)^q (-1)^ell binom(q,ell)sqrt(m+ell)u^ell.
```

All shifted moments in the proof are moments of this same positive measure.
The scalar Young premise is also correct. If `kappa=p/d`,

```text
R^(p-d) >= (v/kappa)^d,
a >= v(1-1/kappa)R,
```

then the critical point of `r^kappa-vr+a` is at most `R`, proving
`B_(k+2)-vB_(k+1)+aB_k>=0`. With the stated normalization this is exactly the
integral of the target polynomial `Y_(m,ell)` divided by `k^3`.

The four new positions have independently reproduced positive margins:

| `j` | `m` | `q` | `gamma_m` | normalized margin `gamma_m/m^3` |
|---:|---:|---:|---:|---:|
| 1 | 3 | 11 | `1/500` | `1/13500` |
| 2 | 4 | 10 | `1/2500` | `1/160000` |
| 3 | 5 | 9 | `1/2500` | `1/312500` |
| 4 | 6 | 8 | `1/1500` | `1/324000` |

Every one of the thirteen rational Young premises holds. Subtracting their
nonnegative lifted polynomials and the monotonicity terms from `P_(m,q)`
leaves a strictly positive polynomial on `[0,1]` in all four cases. Thus the
four new beta entries have the quantitative lower bounds claimed by the
target.

The `j=0` entry is supplied by the retained-interaction endpoint

```text
b_(12,0) >= 13 sqrt(2)d_2/1000.
```

The review separately reconstructed both original6362 pointwise minorants
(`q=9` and `q=12`) and their final scalar signs, rather than trusting the
dependency's expected record. The eight entries `j>=5` use only the
previously independently accepted seven-factor theorem in its stated
`q<=7` range. The exact degree-elevation identity

```text
b_(N,j)=((N+1-j)/(N+2))b_(N+1,j)
       +((j+1)/(N+2))b_(N+1,j+1)
```

then descends through all lower rows; both coefficients are positive, and all
78 lower-row positions were checked. Strictness follows because a shortened
support pair has a positive-mass product neighborhood with `delta_12>0`, so
every `B_m>0`; all relevant margins are positive.

## Independent exact evidence and trust boundary

`independent_check.py` imports no target module. It reconstructs the dyadic
square-root enclosures, all thirteen Young premises, all four degree-twelve
power-basis minorants, the two retained-interaction endpoint minorants, and
the two endpoint scalar polynomials. Instead of the author's 64-cell
Bernstein/de Casteljau certificate, it adaptively subdivides `[0,1]` and uses
exact Taylor expansions about interval centers:

```text
p(c+y) >= p(c)-sum_(r>=1)|a_r|h^r.
```

Strict rational lower bounds certify the whole interval. The four new cases
need respectively 23, 26, 19, and 16 terminal intervals (maximum depth six).
The two dependency minorants need 15 and 14 intervals, and their final scalar
signs need 5 and 9. Three deliberately damaged certificates are rejected.

Reproduce with:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

The exact checker guarantees input provenance, all rational/root premises,
the finite polynomial signs, row coverage, and degree elevation. The Gaussian
product/differentiation identities, support-measure argument, retained-iid
Jensen proof, and reliance on the already accepted seven-factor theorem are
independently reviewed written mathematics, not proof-assistant output.
Historical priority and novelty beyond the inspected primary paper and graph
are not assessed.
