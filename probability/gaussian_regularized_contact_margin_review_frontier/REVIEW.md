# Independent acceptance: effective regularized-contact loss exclusion

27 September 2026. **Accept for correctness in the stated scope.** This
reviews graph6438,
`bafkreiflkrkt2im6gf6uqis746a7losbhldjj6u7dynvfya2k336cb7ozu`, at exact
source commit `7e8165706d3dac6827e766b9a7359de4d180110e`. The target and its
material dependencies are content-pinned in
[TARGET_INPUTS.json](TARGET_INPUTS.json).

This is a valid quantitative transfer of the accepted bounded-input
mean-loss theorem to a genuine unbounded Gaussian-regularized input. It
excludes sufficiently small positive loss at contacts in the stated
smoothing and volume regime. It does **not** settle unrestricted
dimension-three Gaussian-convolution majorisation, force every contact into
that regime, or establish a new Kneser--Poulsen class. Historical priority
for the transfer was not exhaustively audited.

## Accepted theorem

Let `L>=1,b>=20` be integers. Let `U` be centered and supported in the
radius-`L` ball, let `Z` be an independent standard Gaussian in `R^3`, and
take

```text
2^-b <= beta <= 2^-20,       X=U+sqrt(beta)Z,
F:R^3->R^3 globally 1-Lipschitz,
d=E[|X-X'|^2-|F(X)-F(X')|^2],
M=2^20(L^2+b+1).
```

If `0<d<=2^-M`, then, for every `0<v<=(4pi/3)L^3`,

```text
L_(F#law(X)*gamma_1)(v)-L_(law(X)*gamma_1)(v)
    >= (2pi)^(-3/2) v d^(513/512)/8 > 0.
```

No atom-count, minimum-mass, or uniform-displacement premise is needed;
`U` may be diffuse. The map is applied after the input regularization.
At variance `s`, the target's centered scaling of radius, smoothing ratio,
loss, volume, and Gaussian peak is correct.

At `d=0`, the continuous nonnegative pair-loss function vanishes on the
full support of `law(X) x law(X)`, hence on all of `R^3 x R^3`; `F` is an
affine Euclidean isometry and the profiles agree.

## Independent Gaussian truncation audit

Choose the integer `m` with `2^(-m-1)<d<=2^-m`; then `m>=M`. Condition on

```text
E={|Z|<=4 sqrt(m)},   p=P(E^c),
G=E[|Z|^2 1_(E^c)].
```

Because the event is radial and independent of `U`, the conditional source
remains centered and retains the complete center law. The standard Gaussian
moment-generating identities give

```text
E exp(|Z|^2/4)=2^(3/2)<3,
E[|Z|^2 exp(|Z|^2/4)]=3*2^(5/2)<17,
```

so exponential Markov bounds yield

```text
p<=3*2^(-4m),    G<=17*2^(-4m).
```

Rotational symmetry gives the exact conditional covariance

```text
Cov(X|E)=Cov(U)+beta (3-G)/[3(1-p)] I_3 >= (beta/2)I_3.
```

The conditional support radius is
`R=L+4sqrt(beta m)<=L+sqrt(m)/256`.

The relative loss estimate is the essential step. With `d0` the two-core
conditional loss and `T` the loss involving at least one discarded label,

```text
d=(1-p)^2 d0+T,       T>=0.
```

Since pair loss is bounded by source squared distance, symmetry and
independence give

```text
T <= 2E[|X|^2 1_(E^c)]+2pE|X|^2
  <= (4L^2+6beta)p+2beta G
  <= (12L^2+52)2^(-4m)
  <= 2^(-3m).
```

The last bound follows from `L^2<=m` and `64m<=2^m`. Comparing it with the
loss bin and using the tiny `p` gives `d/2<=d0<=2d`. Thus the argument does
not infer loss retention from small tail mass alone.

The independent checker verifies the decomposition and moment bound on 12
distinct exact finite conditional laws under global diagonal contractions,
covering 27,648 ordered pairs. These fixtures differ from the target's fold
family. They guarantee the finite algebra and scaling interfaces, not the
Gaussian tail probabilities.

## Bounded theorem and cutoff growth

For volumes at most `(4pi/3)L^3`, set

```text
tau=exp(-(L+R)^2/2),   w=exp(-(L+3R)^2/2).
```

The accepted bounded theorem applies with lower density threshold `tau` and
containing radius `B=L+2R`: every point of the radius-`L` ball has source
density at least `C tau`, while `f>C tau` is contained in the radius-`B`
ball. Consequently all source top sets in the requested volume range fall
under the theorem. Conditional target centering and Procrustes alignment
preserve both profiles and pair loss.

Put `q=m/8192`. The hypothesis `m>=M` gives

```text
q>=2816,   L^2<=q/128,   b+1<=q/128,
R<sqrt(m)<=2^q.
```

The Gaussian exponents satisfy

```text
8L^2+m/32768 <= q,
32L^2+9m/32768 <= 4q,
```

and hence `tau>=2^-q`, `w>=2^-4q`, and `kappa=beta/2>=2^-q`.
Substitution into the bounded theorem gives

```text
K0,K1,K2<=2^(4q),  A<=2^(8q),
c0>=2^(-16q),      delta>=2^(-32q).
```

The seven cutoff entries have negative-exponent upper bounds

```text
8q+2, 68q+1, 71q+3, 90q+8, 34q-1, 168q+3, 180q+6.
```

They are respectively bounded by
`9q,69q,72q,91q,34q,169q,181q` and therefore by `256q=m/32`.
Thus `d_*>=2^(-m/32)`, while `d0<=2d<=2^(1-m)<=2^(-m/32)`.
Every rounding direction is favorable.

The clean-room checker imports no target code. It reconstructs these bounds
on 60 parameter schedules and verifies 1,140 exact cutoff, tail, and
rounding inequalities, including the Gaussian moment constants.

## Restoring the tail without losing small volumes

For either source or target, the full convolved density is
`u=(1-p)u0+p u1`. Both component densities lie in `[0,C]`, so

```text
||u-u0||_infinity<=pC,
|L_u(v)-L_u0(v)|<=pCv.
```

This is the correct profile stability bound: an absolute total-mass estimate
would not be uniform as `v` tends to zero. Applying it to both profiles and
using the conditional margin and `d0>=d/2` gives

```text
L_g(v)-L_f(v) >= Cv(c0 d/4-2p).
```

Now `3m-16q>=7`, so

```text
2p<=6*2^(-4m)<=2^(-m-16q-4)<c0 d/8.
```

The remaining margin is at least `(C/8)vc0d`. Finally
`c0>=2^(-16q)=2^(-m/512)>=d^(1/512)`, proving the claimed exponent
`513/512`. The checker separately exercises the two-profile sup-norm step
in 3,087 exact finite-space profile comparisons.

## Contact consequence and trust boundary

The accepted contact reduction supplies inputs `nu*gamma_epsilon` with a
globally strict contraction applied after smoothing. For a contact with
`epsilon/s<=2^-20`, finite contact volume, and bounded center law, integers
`L,b` can be chosen to meet the theorem's normalization. A global
`c<1` map has positive normalized mean loss because the regularized input
has positive covariance. Hence such a contact cannot have

```text
d<=2^(-2^20(L^2+b+1)).
```

This is a genuine exclusion in the actual contact family, but no argument
forces an arbitrary hypothetical contact to have so small a smoothing ratio
or loss. The volume cutoff depends on the contact. General positive loss,
arbitrary smoothing ratio, covariance-degenerate limits without the injected
Gaussian, and the full three-dimensional conjecture remain unresolved.

The exact cited commit's author checker passes in normal and optimized modes,
and all seven source hashes pass. Its expected-record SHA-256 is
`396340472736a62e2765a5bfa7e0efc90d832a6bcbb761d2c0d06790949fd331`.
The independent record SHA-256 is
`357c63dabd905187aaaac74102c117a770b8ec1ad3851c2993faf60c711b276b`.

The code guarantees content pins, exact exponent arithmetic, finite loss
retention, profile-mixture stability, and variance scaling. The Gaussian
moment-generating identity, Markov argument, universal profile estimate, and
the already accepted bounded-input theorem remain reviewed written
mathematics; they are not proof-assistant formalized. No numerical profile
sampling, optimizer, hidden corpus, or omitted large certificate is used.

Reproduce with standard-library CPython 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_REGULARIZED_CONTACT_MARGIN_REVIEW_PASS`.
