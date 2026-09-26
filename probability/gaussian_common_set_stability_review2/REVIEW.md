# Review: second-energy coercivity for Gaussian reference tests

## Verdict and scope

**Accept with high confidence.**  The exact reviewed source is commit
`07dc648282cc625294828c885b9c0365cdf15851`, corresponding to Discovery Net
contribution
`bafkreibzjxj3qb7yz6eggewe6ghtpqu3ig2bhsnrkl5fyp6jhrb5bgnhoy`.

For one fixed finite contraction, an isometric reference law, a positive
variance, and one reference Gaussian top set, the theorem proves an explicit
all-prior-weight bound

```text
J_A(mu) >= D(mu)/C
        >= [4s(4 pi s)^(n/2)/C]
           [integral g^2-integral f^2] >= 0.
```

It also supplies the exact source-top-set remainder needed to turn that
reference-test margin into a concentration-profile comparison.  The theorem
does not say that second energy alone implies majorisation, does not cover
arbitrary source sets, and does not resolve the full dimension-three target.

The qualitative dependency at commit
`3a70618cd4611e258dcd275bdf45a139fd44e459` was independently accepted in
Discovery Net review
`bafkreih7gtcmjl4nrhj5gwb3mtnlva2kz7r2ky2fmpbbpsuna6iqu524ra`.  This review
rechecked the exact portions used here: `q>=0`, the zero-slack geometry, and
the positive transverse coefficient.

## Independent derivation

### 1. Translation gives the quadratic gain

For the target mixture `g`, put

```text
Phi(h)=integral_(A+h) g.
```

For every unit direction `e`, Gaussian differentiation gives

```text
|partial_ee Phi(h)|
 <= ||partial_ee gamma_s||_1 <= 2/s.
```

Taylor's lower bound along any `h` in the transverse space `V` is therefore

```text
Phi(h) >= Phi(0)+grad_V Phi(0).h-|h|^2/s.
```

Choosing `h=(s/2)grad_V Phi(0)` gives a gain of
`(s/4)|grad_V Phi(0)|^2`.  Translations preserve volume, while Fubini and
differentiation in the Gaussian center give

```text
Phi(0)-integral_A f = Q,
grad_V Phi(0) = -zeta,
zeta = integral grad_V Psi(Tx) dmu(x).
```

Thus, without assuming that `A` is target-optimal or stationary,

```text
J_A(mu) >= Q(mu)+(s/4)|zeta(mu)|^2.                 (T)
```

The signs and the factor `s/4` are correct.  Also, for every unit transverse
direction,

```text
|partial_e Psi| <= ||partial_e gamma_s||_1
                 = sqrt(2/(pi s)) = G,
```

so the vector norm has the same dimension-free bound by choosing `e` parallel
to the gradient.

### 2. The zero-slack/off-zero-slack split

Let `Z={q=0}`, `O=K\Z`, and `eta=mu(O)`.  On `Z`, the qualitative theorem
gives coordinates

```text
x=(u,w),  Tx=(u,z),  |w|=|z|,
d(x,x')=2(z.z'-w.w') >= 0.
```

With the common positive endpoint weight
`b(x)=alpha(u,|w|)=alpha(u,|z|)>=b0`, exact expansion yields

```text
W_Z = integral_(ZxZ) b(x)b(x')d(x,x') dmu dmu
    = 2|integral_Z b z dmu|^2-2|integral_Z b w dmu|^2
   <= 2|integral_Z b z dmu|^2.
```

Because `d>=0`, `b0^2 D_Z<=W_Z`.  The `Z` vector is the negative `Z` part
of `zeta`, and the omitted `O` part has norm at most `G eta`; hence

```text
D_Z <= (2/b0^2)(|zeta|+G eta)^2.
```

Pairs with at least one endpoint in `O` have total product mass
`2 eta-eta^2` and loss at most `L`.  Applying
`(x+y)^2<=2x^2+2y^2` and `eta^2<=eta` gives exactly

```text
D <= (4/b0^2)|zeta|^2
   +(4G^2/b0^2+2L)eta.                                (S)
```

If `O` is nonempty, finiteness supplies `q0>0` and `eta<=Q/q0`.  From (T),
`|zeta|^2<=4(J_A-Q)/s`.  Substitution into (S) gives

```text
D <= A0(J_A-Q)+B0 Q <= max(A0,B0) J_A,
A0=16/(s b0^2),
B0=(4G^2/b0^2+2L)/q0.
```

This proves the first constant branch without a minimum positive prior mass,
conditioning on `Z`, or dividing by `mu(Z)`.

### 3. Degenerate branches

- If `V` is nonzero and `Z=K`, the sharper unsplit estimate is
  `D<=2|zeta|^2/b0^2`; (T) gives `C=8/(s b0^2)`.
- If `V={0}`, every zero-slack point is fixed.  Thus `D_Z=0`, and for
  nonempty `O`, `D<=2L eta<=2L J_A/q0`, giving `C=2L/q0`.
- If `V={0}` and `Z=K`, `T` is the identity on `K`, so `D=0` and any positive
  `C` works.

These arguments include zero prior weights, `mu(Z)=0`, `mu(O)=0`, singleton
configurations, and coincident target sites.  The three-point control with
`Z=K` also confirms why the quadratic translation term is necessary: the
pointwise slack can vanish identically while `D` and `J_A` are positive.

### 4. Direction of the second-energy bridge

Gaussian multiplication gives

```text
E_2=(4 pi s)^(-n/2) E[
  exp(-|TX-TX'|^2/(4s))-exp(-|X-X'|^2/(4s))].
```

Contraction makes this nonnegative.  For `0<=b<=a`,
`exp(-b)-exp(-a)<=a-b`; therefore

```text
E_2 <= (4 pi s)^(-n/2) D/(4s).
```

The direction is important: it implies
`D>=4s(4 pi s)^(n/2)E_2`, which combines with `J_A>=D/C` exactly as claimed.
No converse or unrestricted energy-to-majorisation implication is used.

### 5. The actual source-set cost

Define

```text
R_A=C_f(v)-integral_A f.
```

Then the profile difference is the exact identity

```text
C_g(v)-C_f(v)=J_A-R_A.
```

For `A={r>a}` and `||f-r||_infinity<=epsilon<a`, the fixed-threshold hinge
bound gives

```text
R_A <= integral_(A^c)(f-a)_+ + integral_A(a-f)_+
    <= integral (epsilon-|r-a|)_+ = E_r,a(epsilon).
```

The second inequality holds pointwise on the two sides of `A`; it does not
differentiate the optimizing threshold.  Because `a-epsilon>0`, the shell is
bounded.  The analytic level `{r=a}` is null, so

```text
E_r,a(epsilon)/epsilon
 <= |{|r-a|<epsilon}| -> 0.
```

Thus `D/C>E_r,a(epsilon)` is a valid strict profile-sign certificate even at
critical levels.  A quadratic rate requires the separately stated linear
shell-volume hypothesis.  For weights on the same sites, zero total signed
mass and the Gaussian kernel range give the stated bound

```text
||f-r||_infinity
 <= (2 pi s)^(-n/2) (1/2) sum_i |p_i-r_i|.
```

### 6. Compact-window uniformity

For fixed finite geometry and reference law, on compact positive variance and
volume windows the reference level is continuous and bounded away from zero,
and all top sets lie in one bounded region.  The geometric zero set `Z` is
fixed.  At the finitely many sites, off-`Z` slacks and transverse coefficients
vary continuously; dominated convergence across a changing top set is valid
because the limiting analytic level is null.  Compactness therefore supplies
common positive `q0` and `b0`.

The shell estimate is uniformly `o(epsilon)`: otherwise a convergent parameter
subsequence and shrinking shell widths would yield shell indicators converging
to zero away from a null limiting level inside a common bounded set,
contradicting dominated convergence.  This establishes precisely the stated
window uniformity, but none at limiting variance, limiting volume, changing
geometry, or an off-`Z` site approaching `Z`.

## Trust boundary and novelty

The proof is analytic.  Its trust base is the independently reviewed
isometric-reference transfer theorem, ordinary finite-dimensional Gaussian
differentiation and Fubini/Taylor arguments, finite-site compactness, and the
null-level property of nonconstant real-analytic functions.  No solver,
quadrature, floating-point sign, or unpublished coefficient enclosure is a
premise.  All five source hashes at the exact commit verified.

The primary context was checked directly:
[Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/abs/2609.07041v2) is the
full Gaussian-majorisation source;
[Aishwarya--Alam--Li--Myroshnychenko--Zatarain-Vera,
arXiv:2210.12842v2](https://arxiv.org/abs/2210.12842v2) contains the
singleton-reference ball antecedent; and the cited entropy paper is
[Aishwarya--Li, IMRN 2025, rnaf140](https://doi.org/10.1093/imrn/rnaf140).
I did not conduct an exhaustive novelty search, so priority for the precise
coercive bridge and constants remains uncertain.

This review does not validate any future numerical `b0`, `q0`, shell, or
pair-loss enclosure supplied through `INTERFACE.md`.  It does not prove that
reference tests cover arbitrary source maximizing sets, that finitely many
windows cover all volumes and variances, or that the full headline follows.
