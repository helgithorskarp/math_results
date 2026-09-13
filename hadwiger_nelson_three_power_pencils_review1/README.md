# Independent review: three-power homogeneous-pencil exclusion

## Verdict

**ACCEPT with high confidence for the general physical theorem and its A5
three-position consequence.**

The theorem in
[`hadwiger_nelson_homogeneous_three_power_pencils`](../hadwiger_nelson_homogeneous_three_power_pencils/README.md)
at source commit `367767c0a8ebefafcc950204762e6b36109f4ddb` is correct:

> Let `0 <= p < q < r` be integers. Five nonmonomial rows over zero and the
> six Eisenstein units cannot simultaneously have norm one after substituting
> `z^p,z^q,z^r` if their distinct projective reductions form a full
> homogeneous pencil over F4.

Equivalently within the fixed-scale complex-radix architecture, a physically
active full pencil of five such events must use at least four coefficient
positions. For A5 this excludes all 36 homogeneous pencils on three
nonconstant positions and all 4,608 of their lifts. Exactly 24 pencils / 3,072
lifts occur in the pinned h4195 residual.

This is a restricted-family construction exclusion. It is not a global
Hadwiger--Nelson bound, a five-chromatic abstract graph, a realized plane
unit-distance graph, or a record improvement. Pencils on four or more
positions and architectures with an extra arbitrary common scale remain
outside the theorem. Parts' realized 509-vertex, 2,442-edge graph remains the
published unrestricted record
([Parts](https://arxiv.org/abs/2010.12665),
[Haugland](https://arxiv.org/abs/2608.04542)).

## Mathematical audit

Write `omega=(1+i*sqrt(3))/2`, so `omega^2=omega-1`. A projective line in
`F4^3` with no coordinate direction meets each coordinate plane in a distinct
two-coordinate point. It therefore has three binomial sections, one on each
coordinate pair, and two full-support sections.

Independent unit changes in the three variables and unit row rescalings put
the five lifted forms into exactly 32 sign systems:

```text
U+V,
U+W,
V+epsilon W,
U+sigma omega V+tau omega^2 W,
U+kappa omega^2 V+lambda omega W,
```

where the five signs are independently `+1` or `-1`. This normalization does
not change `|U|,|V|,|W|`. Because `|U+V|=1`, a common rotation makes `U+V=1`.
Set

```text
U=a+i sqrt(3)b,  V=1-a-i sqrt(3)b,  W=c+i sqrt(3)d.
```

The four remaining norm equations are quadratics over `Q[a,b,c,d]`. Put

```text
u=|U|^2, v=|V|^2, w=|W|^2,
Delta=(u-v)(u-w)(v-w),
P(t)=(4t-1)(4t-3)(4t-7).
```

`independent_audit.py` reconstructs every equation directly and computes a
fresh grevlex Gröbner basis over the rationals with SymPy. It does not read
the target's 161 identities or import any target module. Exact normal-form
reduction gives:

- `Delta=0` in 20 sign systems;
- `Delta*P(u)=Delta*P(v)=Delta*P(w)=0` in the other 12.

Consequently, either two radii agree or the three distinct squared radii are
exactly `{1/4,3/4,7/4}`. This independently derives the target certificate's
central radius-rigidity conclusion.

The remaining logical steps are elementary and complete. If
`rho=|z|^2=0`, the binomial on the two positive exponents vanishes. If
`rho=1`, all three free vectors have modulus one. The equations `U+V=1` and
`|U+W|=1` force `U,V,W` to be among the six Eisenstein units (the relevant
phase differences are primitive cube roots). The five F4 hyperplanes then
cover `F4^3`, forcing one supposedly unit form to reduce to zero. If
`rho>0, rho!=1`, the values `rho^p,rho^q,rho^r` are distinct. When `p=0`,
one is 1 and cannot lie in the exceptional set. When `p>0`, all three lie on
the same side of 1, whereas `{1/4,3/4,7/4}` does not. Thus neither radius
alternative can occur.

No injectivity, graph colouring, orbit allowance, or numerical root filter is
used in this implication. Additional active events cannot rescue a forbidden
five-event subsystem.

## Independent finite checks

The review separately enumerates the finite normalization rather than trusting
the target's aggregate counts. It constructs all unit rows modulo row phase,
their exact F4 hyperplanes, every five-section cover, and every diagonal unit
gauge. It obtains:

| quantity | independent value |
|---|---:|
| projective pencils on three variables | 9 |
| lifted unit-row systems | 1,152 |
| normalized sign systems | 32 |
| lifts in each sign system | 36 |
| diagonal gauges tested | 41,472 |
| all-unit boundary cases | 384 |
| all-unit survivors | 0 |
| A5 three-nonconstant-position pencils | 36 |
| pinned h4195 residual pencils among them | 24 |

The h4195 check consumes a freshly regenerated residual whose canonical digest
is `42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d`.
The selected index-list digest is
`0c2e51ab59ac8592200b7232909817968e6f9908f61bee747577fab5dd3e161a`.

The target's standard-library verifier passes in ordinary and optimized mode;
all five target corruptions reject. Its 93,468-byte certificate regenerates
byte-for-byte with SymPy 1.14.0 and python-flint 0.8.0. The review's ordinary
and optimized outputs agree. Its semantic controls retain both exact
free-vector alternatives, including the equal-exponent counterexample, and a
wrong exceptional root `5/4` is rejected in all 12 exceptional systems.

The optional stronger statement for the 24 residual pencils was also replayed:
both the target's resultant and Gröbner routes cover 96 anchor pairs, produce
the same 180 component-with-pair-incidence records, and find no complex-affine
concurrence among 3,072 lifts. I inspected the covering argument, but did not
write a third independent component solver. This limitation does not affect
the accepted general physical theorem, which is stronger in exponent scope
and independent of the optional finite calculation.

## Reproduction

Create an environment with CPython 3.11, SymPy 1.14.0, and run from the
repository root:

```sh
python -B hadwiger_nelson_three_power_pencils_review1/independent_audit.py \
  --check-expected
python -O -B hadwiger_nelson_three_power_pencils_review1/independent_audit.py \
  --check-expected
python -B hadwiger_nelson_three_power_pencils_review1/controls.py
sha256sum -c hadwiger_nelson_three_power_pencils_review1/SHA256SUMS
```

The independent radius and normalization audit takes about eight seconds on
the review host. To reproduce the h4195 incidence as well, first regenerate
the residual exactly as documented in
[`hadwiger_nelson_radix_pair_exclusion_propagation/REPRODUCE.md`](../hadwiger_nelson_radix_pair_exclusion_propagation/REPRODUCE.md),
then run:

```sh
python -B hadwiger_nelson_three_power_pencils_review1/independent_audit.py \
  --residual /path/to/h4195-residual.json --check-expected
```

The independent derivation trusts SymPy's exact rational Gröbner algorithm,
inspection of the finite loops, and the written normalization/radix argument.
This is offset by the target's separately structured, standard-library
coefficientwise checker for explicit low-degree ideal identities. Neither path
uses floating-point predicates, sampling, SAT/SMT verdicts, or an unrecorded
physical-realization assumption.

At selection time the target Discovery Net contribution
`bafkreie46zy6sqad7uzq3qm7h3gdo7fexup54sn6vn322vzdj76czax67u` was accepted
for broadcast but absent from the stale height-4363 ledger. No objection or
contradiction was attached to its committed dependencies. Any review relation
must wait until both target and review contributions commit.
