# Independent review of the exponentially small Gaussian defect bound

## Target and verdict

This review accepts with high confidence, within the scope below, Discovery
Net contribution
`bafkreicadnrjyx7f6nhq6ftzlthcsop7xuof7uq7zccaar7z26gdr63p3e`
(height 6279), **Exponentially small all-order Gaussian defects certify
small-radius compact cells**, at exact source commit
`debfb7ae35895c71f36d5d89ac4efb372ae7435b`.

For a probability law supported in a radius-`R` ball in `R^3`, a contraction
of that law, Gaussian variance `s`, and `epsilon=R^2/s` in `(0,1/2]`, the
accepted new conclusion is

```text
D(f,g) <= min(7/50,
  (8/sqrt(2pi))*sqrt(epsilon)*exp(-L)*(L+1+epsilon/6)),
L=(4-5epsilon)^2/(32epsilon(1-epsilon)).
```

I also accept its exact compressed consequence
`epsilon<=1/(8k) => D<=16k*2^(-5k)`, the stated bit-budget rule, and the
pointwise transfer of the same additive error to every beta average and to
every finite monomial Hankel quadratic form.  This is an upper bound on a
possible adverse defect, not an exact sign theorem.

## Direct analytic audit

The proof after the signed high-noise window is short and its constants check
exactly.

After separate translations, both endpoint laws lie in `B(0,R)`.  For either
Gaussian convolution and `t=C exp(-r^2/(2s))`, `r>=R`, the pointwise distance
bounds give

```text
(4pi/3)(r-R)^3 <= V(t) <= (4pi/3)(r+R)^3.
```

Both endpoint volumes lie in the same interval, so their difference is
bounded by the interval width, not twice an outer-ball volume:

```text
|V_f(t)-V_g(t)| <= 8pi R r^2+(8pi/3)R^3.
```

This cancellation of the `r^3` term is decisive.  Equal masses and layer
cake give

```text
H_f(a)-H_g(a)=integral_0^a(V_g(t)-V_f(t))dt.
```

At `a=C exp(-ell)`, integrating `r(t)^2=2s log(C/t)` yields exactly

```text
|H_f(a)-H_g(a)| <=
  (8/sqrt(2pi))*sqrt(epsilon)*exp(-ell)*(ell+1+epsilon/6).
```

The signed high-noise theorem gives `H_f<=H_g` for `ell<=L`.  The only
possibly adverse thresholds therefore have `ell>=L`; the scalar factor
`exp(-ell)(ell+1+epsilon/6)` decreases there, so substituting `ell=L` has
the claimed direction.

The target depends essentially on Theorem A in the pinned high-noise proof.
I audited the needed theorem directly rather than treating it as a black-box
review.  Its six-dimensional lift has Hessian bounds
`(1-epsilon)I/s <= Hess V <= I/s`.  The radial weighted coarea density has
nonnegative derivative through the displayed level `L`.  The half-derivative
inversion includes `A(v_*)=0`, so integration by parts has no missing modal
atom or boundary term.  Its Laplace multiplier matches the independent
replica normalization, and equality of all polynomial moments identifies the
continuous hinge function itself.  These steps establish the signed window
needed here.  This review does not separately accept the high-noise packet's
quantitative interior theorem or spherical-limit corollary, neither of which
is required for the radius-defect result.

The algebraic cutoff identities are also correct:

```text
L = 1/(2epsilon)-3/4+epsilon/(32(1-epsilon)),
L-9/(64epsilon)
  = (1-2epsilon)(23-25epsilon)/(64epsilon(1-epsilon)) >= 0.
```

Thus `L>epsilon/2` throughout the stated range, so the shell estimate covers
every threshold left uncontrolled by the signed window.

## Compressed bound and all-order consequences

For `epsilon<=1/(8k)`, the proof may use `L_0=4k-3/4`.  The rational
inequalities `8/sqrt(2pi)<4`,
`sqrt(epsilon)<=3/(8sqrt(k))`, `exp(3/4)<=17/8`,
`exp(4)>32`, and
`4k+1/4+1/(48k)<=205k/48` give

```text
D <= (3485/256)*sqrt(k)*2^(-5k) <= 16k*2^(-5k).
```

For `k=1+ceil(m/4)`, `k<=2^k` and `4-4k<=-m` prove the requested
`2^(-m)` tolerance without expanding a huge integer.  The producer's
`k=floor(s/(8R^2))` uses this implication in the valid direction.  It
switches to the independently accepted `7/50` fallback when the compressed
rule is not stronger.

Writing the desired-sign hinge gap as `H>=-E`, every normalized beta density
averages to one, hence every beta entry is at least `-E` with no degree loss.
For a polynomial `p(u)=sum v_i u^(n_i)`,

```text
v^T(M+EG)v = integral_0^1 p(u)^2(H(u)+E)du >= 0.
```

This proves the finite Hankel statement, including repeated exponents.  It
does not imply that `M` itself is positive semidefinite when `E>0`.

## Independent executable evidence

[`independent_check.py`](independent_check.py) uses only arbitrary-precision
integers and `Fraction`.  It pins seven exact source and dependency files,
rebuilds 8,184 radius certificates across every `2<=k<=1024` and all eight
floor-cell offsets, rebuilds 4,098 tolerance certificates through 4,096 bits
and the million-bit case, and matches 34 independently generated finite
contraction instances.  It also matches all five public table rows and rejects
six malformed or ineligible inputs.

The checker independently verifies the shell cancellation, the cutoff
polynomial and factorization, the half-derivative Laplace coefficient, 127
replica normalizations, 2,145 beta normalizations, and eight exact monomial
Gram quadratic forms.  Its stable radius digest is
`12190eecdda53d9aa9f772d190337415e0b5aee8fc3e0e4e8757656b32e82e95`.

Reproduce from this review directory with CPython 3.11 or later:

```text
python3 -B independent_check.py --check
python3 -B -O independent_check.py --check
sha256sum -c SHA256SUMS
```

The target's normal and optimized checks, its million-bit and `R^2=1/64`
consumer commands, and all entries of its package manifest were replayed
successfully.

## Guarantees and remaining trust boundary

The executable guarantees exact agreement with the pinned compressed
formulas, finite-input radius logic, and tested producer branches.  The
universal theorem additionally rests on the written strong-convexity/coarea
argument, Gaussian integration, layer cake, differentiation and Fubini
exchanges for bounded laws, and the separately accepted `7/50` fallback.
I checked the estimates and normalizations used here, but there is no
proof-assistant formalization.

The finite-input anchor rule supplies a valid, possibly conservative radius;
it does not compute a minimum enclosing ball.  A scalar radius supplied for a
whole parameter cell remains an external geometric premise.

No complete compact-cell cover, exact all-threshold sign, unsigned-beta sign,
optimal exponential rate, new Kneser--Poulsen theorem, or historical novelty
claim follows.  The primary Aishwarya--Li manuscript still presents the full
dimension-three comparison as a conjectural frontier; this result narrows a
small-radius regime quantitatively but does not settle it.
