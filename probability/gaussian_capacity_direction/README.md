# Direction matters in a Gaussian posterior transport certificate

[PROOF.md](PROOF.md) derives an exact forward coupling identity and proves
that its natural nonnegative-exponent certificate cannot settle the full
Gaussian-majorisation question, even after optimization over all feasible
kernels. This is a complete author proof; independent review is pending.

The kernel takes Lebesgue measure on an actual source top set of volume v
to a target selector with density at most one and the same volume. The
certificate retains both a positive posterior pair-distance term and the
full nonnegative information discarded by mixing. At any smaller volume
where the normalized target profile exceeds the source by d, its exponent
obeys

```text
beta <= log(C_g(v)/C_f(v)) - min(d/(2c), d^2/2),
c = a_g(w)/(a_g(w)-a_g(v)),  0<w<v.
```

Thus it has a strict negative gap at an ordered contact with a stricter
upper part. If C_g(w)>C_f(w) at any fixed w, the optimized exponent stays
negative for all sufficiently large v. A known positive two-atom collapse
is an exact bounded R3 control. The isometry control has optimized exponent
zero. This rules out a global use of this particular direction of coupling;
it does not refute Gaussian majorisation or the existing global criterion.

The next analytic obligation is a law-dependent construction that avoids
making the candidate target less concentrated than the source. Target-to-
source mixing with latent-label recoupling is a proposed direction only.
No new map family or isolated threshold certificate is proposed.

The derivation is analytic and includes critical levels. No solver, Gaussian
integration, finite experiment or large generated artifact is a premise.
The sole reproduction command checks source identity, not mathematical truth:

```sh
sha256sum -c SHA256SUMS
```

Expected: the three listed Markdown files each report `OK`.
[SOURCES.md](SOURCES.md) records classical ingredients and exact team input
versions. The full bounded-law dimension-three question remains open.
