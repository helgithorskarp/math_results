# Review: isometric-reference Gaussian transfer and zero rigidity

## Verdict and exact target

**Accept with high confidence.**  The exact reviewed source is commit
`3a70618cd4611e258dcd275bdf45a139fd44e459`, corresponding to Discovery Net
contribution
`bafkreie5ibd7vpcrllaf45oz3oxoqirtj5gcigalzrzyz4kgzhhl4q7a4u`.

The accepted theorem concerns a compact `K` in `R^n`, a contraction `T`, and
a reference law `sigma` on whose support `T` agrees with an affine Euclidean
isometry `S`.  For a positive superlevel set `A` of `sigma*gamma_s` and
`B=S A`, it proves pointwise transfer to `B`, classifies every zero minimizer
of the optimized common-set gap, and identifies `B` as the unique dual set.

This is a special-set boundary theorem in every finite dimension.  It is not
a sign theorem for arbitrary source sets, a quantitative stability estimate,
or a proof of the full dimension-three Gaussian-majorisation frontier.

## Independent proof audit

### 1. Normalization and maximizing sets

Pulling target coordinates back by `S` makes `T` fix `supp(sigma)`; translating
a fixed reference point to zero then makes the affine normalization linear.
Neither operation changes the gap or the relevant distances.

For a compactly supported Gaussian mixture `p`, positivity, decay, and real
analyticity imply that every positive level set is bounded and every level
surface `{p=h}` has measure zero.  If `A={p>h}` and `|E|=|A|`, then

```text
integral_A p - integral_E p
  = integral (1_A-1_E)(p-h) >= 0.
```

Equality forces `E=A` modulo null sets.  Continuity and strict monotonicity of
`h -> |{p>h}|` also justify the claimed unique level for every finite positive
volume.

### 2. Pointwise transfer and its strict equality case

Fix `x`, put `a=x`, `b=Tx`, and let `H` be the halfspace of points nearer `b`
than `a`.  Since every reference center `c` is fixed and `T` is a contraction,
`|b-c|<=|a-c|`; hence every such `c` lies in the closed halfspace `H`.
Reflecting across its boundary gives, for `z in H`,

```text
f_sigma(z) >= f_sigma(Rz),
1_A(z) >= 1_A(Rz),
gamma_s(z-b) > gamma_s(z-a).
```

Pairing reflected points yields the exact identity

```text
Psi_A(b)-Psi_A(a)
 = integral_H [1_A(z)-1_A(Rz)]
              [gamma_s(z-b)-gamma_s(z-a)] dz >= 0.
```

If all reference distances are equal, every reference center lies on the
bisector and the mixture, hence `A`, is reflection invariant.  Conversely,
one strict reference distance puts positive reference mass in the open
halfspace, making `f_sigma(z)>f_sigma(Rz)` throughout `H`.  The inward normal
derivative is positive on the bisector.  Thus every global maximizer is in
`H`; following the outward normal ray from it to the first `h`-level crossing
produces an open positive-measure region where the two factors above are both
strict.  This proves

```text
q(x)=0  iff  all distances from x to supp(sigma) are preserved.
```

The argument does not require `h` to be a regular value.

### 3. Strictly positive transverse derivative

Let `U=span(supp(sigma))` and `V=U^perp`.  In normalized coordinates,

```text
f_sigma(u,w)=p_U(u) gamma_s^V(w),
```

so each nonempty transverse section of `A` is a centered ball `B_R` in `V`.
For

```text
F_R(w)=integral_(B_R) gamma_s^V(z-w) dz,
```

radial differentiation and reflection on the sphere give, for `r>0`,

```text
-F_R'(r)
 = integral_(|z|=R,z.e>0) (z.e/R)
     [gamma_s^V(z-re)-gamma_s^V(z+re)] dS(z) > 0.
```

Dividing by `r` has the positive continuous limit

```text
a_R(0)=2/(Rs) integral_(|z|=R,z.e>0)
                    (z.e)^2 gamma_s^V(z) dS(z).
```

This remains correct in one transverse dimension with counting surface
measure.  Since `F_R'(0)=0` and the `L1` norm of the directional Gaussian
Hessian is at most `2/s`, the mean-value estimate gives `0<a_R(r)<=2/s` for
`R>0`.  Convolution in the `U` variables therefore yields a continuous
coefficient `alpha(u,r)>0` everywhere with

```text
grad_V Psi_A(u,w)=-alpha(u,|w|)w.
```

This verifies the delicate `r=0`, `dim(V)=1`, and singleton-reference cases.

### 4. Zero minimizers force one joint isometry

The target competitor `B` gives

```text
J_A(mu) >= integral q dmu >= 0.
```

If `J_A(mu)=0`, both inequalities are equalities.  Continuity and positivity
give `q=0` on `supp(mu)`, and the normalized set `A` is a maximizing set for
the target density.  Distance equality to every reference point implies

```text
x=(u,w),   Tx=(u,z),   |w|=|z|.
```

Every translation of `A` is an admissible volume-preserving competitor.
Differentiating the target integral in transverse directions has the sign

```text
0 = integral_A grad_V g_mu
  = -integral grad_V Psi_A(Tx) dmu(x)
  = integral alpha(u,|z|) z dmu(x).
```

Because `|w|=|z|`, the same strictly positive weight
`a(x)=alpha(u,|w|)=alpha(u,|z|)` applies to both endpoints.  Normalize
`a dmu` to a probability law `mu_hat`; it has the same support as `mu` and
`E_hat z=0`.  For two independently sampled supported labels, contraction
and the preceding coordinate form give the nonnegative pair loss

```text
d(x,x') = |x-x'|^2-|Tx-Tx'|^2
        = 2(z.z'-w.w') >= 0.
```

Its expectation is simultaneously

```text
E_hat d = 2(|E_hat z|^2-|E_hat w|^2)
        = -2|E_hat w|^2 <= 0.
```

Hence the expectation and every continuous pair loss on the product support
vanish.  Distances are preserved within `supp(mu)` as well as between it and
the reference support.  Gram polarization then extends this partial
isometry to an ambient orthogonal map.  The map fixes `U`, preserves the
reference mixture and `A`, and converts target optimality of `A` to source
optimality.  This proves both necessity conditions in the theorem.

Conversely, a common ambient isometry on the two supports fixes the reference
mixture and preserves `A`; if `A` is source-optimal, an orthogonal change of
variables makes the gap zero.  Thus the minimizer classification is exact,
including diffuse laws and zero-dimensional `V`.

### 5. Unique dual set

For every measurable `D` with `|D|=v`, averaging its pointwise dual slack
against `sigma` gives

```text
min_K q_D <= integral_D g_sigma - integral_A f_sigma <= 0.
```

The set `B` attains zero by pointwise transfer.  If another `D` attains zero,
its minimum and therefore its reference average are nonnegative; the display
forces equality.  Uniqueness of Gaussian superlevel maximizers then gives
`D=B` modulo null sets.  No minimax interchange is hidden here.

## Edge cases and assumptions checked

- `V={0}`: reference-distance equality already gives `Tx=x` in normalized
  coordinates, so no transverse calculation is needed.
- `U={0}` and singleton references: the transverse ball formulas and the
  reweighted expectation argument remain valid.
- `dim(V)=1`: the sphere calculation reduces to the two interval endpoints.
- Diffuse `sigma` and `mu`: compact support, Fubini, dominated differentiation,
  and continuity of pair loss suffice; no atomic reduction is used.
- Coincident target points are allowed.  They can occur away from a zero
  minimizer, while zero rigidity rules them out unless source distances also
  vanish.
- The stated affine isometry is only required on the reference support; the
  proof constructs an ambient extension only after all relevant distances
  have been shown equal.

## Trust boundary, literature, and remaining gaps

The accepted theorem rests on standard finite-dimensional Gaussian calculus,
reflection pairing, the measure-zero property for nonzero real-analytic level
sets, dominated differentiation, and elementary Euclidean Gram rigidity.
There is no numerical, solver, or generated-data premise.  The source hashes
at the exact commit all verified.

The cited primary sources were checked directly.
[Aishwarya--Alam--Li--Myroshnychenko--Zatarain-Vera,
arXiv:2210.12842v2](https://arxiv.org/abs/2210.12842v2), Theorem 2.4 and its
proof contain the radially symmetric singleton-reference ball mechanism.
[Solynin, arXiv:1102.1004](https://arxiv.org/abs/1102.1004), Section 3 records
polarization as a classical tool.
[Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/abs/2609.07041v2) is the
motivating Gaussian-majorisation source.  I did not conduct an exhaustive
novelty search, so priority for the general equality classification remains
uncertain.

This review does **not** verify the later quantitative common-set coercivity
claim, which depends on positive floors and constants beyond this qualitative
theorem.  It also does not show that arbitrary maximizing source sets are
isometric-reference superlevel sets, supply a uniform sign neighborhood,
control arbitrary hinge tests, or resolve the dimension-three headline.
