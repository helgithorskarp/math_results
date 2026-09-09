# Independent review of the A5 first-step anchor closure

Verdict: **ACCEPT with high confidence** for the standalone theorem that every
physical A5 member on any of the six first-step anchor circles has chromatic
number exactly three. The complete real-parameter classification, all colour
certificates, the five collision witnesses, both endpoints, and the two
eight-active physical fixtures reproduce independently.

The six anchor curves are therefore valid global exclusions for any possible
non-four-colourable A5 member. The resulting closure of 216 additional
five-pencils and 3,354,048 h4171 survivor lifts also reproduces relative to the
reviewed h4167/h4171 interfaces. The numerical deletion of 424 global pair
representatives and the downstream pair-orbit allowances are **accepted
conditionally** because they import the still-unreviewed h4177 mode table,
h4117 quotient completeness, and h4175 free action.

This is a meaningful intermediate physical exclusion, not the campaign
target. It leaves 5,112 exact-five pencils, 128,871,936 combinatorial quintet
survivors, and the whole wider higher-incidence problem open. It produces no
non-four-colourable graph and no improvement to the 509-vertex record.

## Geometric reduction and parameter coverage

Put `s=2*omega-1`, so `s^2=-3`. Multiplication of the radix by
`rho=omega^2` sends each digit triangle `rho^j T` to a unique translate of
`T`. The independent checker obtains the translation sequence

```text
(0,0), (-1,0), (0,-1), (0,0), (-1,0)
```

and hence verifies the exact digitwise identity
`A5(rho*z)=A5(z)-z-omega*z^2-z^4`. The six Eisenstein units form two
three-element orbits under multiplication by `rho`, so it suffices to decide
the representatives `|1+z|=1` and `|1-z|=1`; no symmetry under `z -> -z`
is assumed.

For signs `sigma=+1,-1`, respectively, all finite points on those circles are
parametrized by

```text
z_sigma(t) = sigma*2*s*t/(1-s*t),   t real,
H(t) = 1+3*t^2 > 0.
```

The omitted limit is `z=-2*sigma`, so the two endpoints are `z=+2,-2`.
The positivity of `H` makes denominator clearing exact on the entire real
locus.

## Independent exact event census

[independent_check.py](independent_check.py) imports no h4185 module. It uses
the previously published reviewer h4181 checker only to rebuild all A5
displacement rows and curve IDs by direct arithmetic in
`Q(sqrt(-3))[x,y]`. That source differs from h4185's imported h4163
bivariate inventory and is pinned by SHA-256
`5a3804b9e39e55686fd2ffa377f7bc60323b46c33c45f88f16076fe529a3de23`.

For each displacement row, the new checker directly forms
`H^k sum_j d_j z_sigma(t)^j` in the basis `{1,sqrt(-3)}`, takes its exact
norm, subtracts `H^(2k)`, divides the provable factor `H^k`, and primitive-
normalizes. This does not call the target's bivariate pullback or polynomial
library. It obtains, for each sign:

```text
event curves                                      2,797
identically active representative anchor              1
distinct nonzero restricted polynomials           2,760
primitive certificate blocks                      2,536
blocks with real roots                             1,907
distinct finite real event parameters              2,865
```

The two signs have the same restricted-polynomial set. Their anchor IDs are
2209 and 2208. The independently reconstructed restriction inventory has
SHA-256
`1fed3b8b15e84549d4a549bc665cbdafd6f9566041c7e4094ef058630370134f`.

Every submitted factor product is multiplied out over the integers. The
2,536 block degrees reproduce as follows:

| degree | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| blocks | 11 | 52 | 100 | 285 | 500 | 771 | 680 | 137 |

A fresh rational Sturm implementation checks every declared real-root count.
An independently implemented Euclidean algorithm over `F_1000003` verifies
all 2,536 blocks are squarefree and all `C(1907,2)=1,817,371` pairs of
real-root blocks are coprime, with both leading degrees preserved. The pair
transcript SHA-256 is
`7fdea25f5ea1030f4b1f35a8df2807e4abee3ef717e567967e9d59202a03e47b`.
Gauss's lemma then gives rational coprimality. Therefore every finite real
event parameter belongs to one real-root block, and its complete active-curve
set is determined by the checked factor products. Block irreducibility is not
needed.

## Chromatic certificates and collision boundary

The checker independently assigns all 29,403 digit-label pairs to the 243
universal edges or one of the 2,797 curve groups. For each sign it reconstructs
the active groups for every real block and checks the submitted F3 weight word
against every actual edge. Exactly 1,902 real blocks per sign have valid
three-colour words. The generic word also colours every non-event parameter.

The remaining five real blocks each have one real root and an explicit
nonzero digit-difference row for each sign. Direct substitution in the
`{1,sqrt(-3)}` rational-function model proves that both coordinate numerators
are divisible by the stated block. Each resulting physical member is
noninjective, so the previously independently accepted h4119 theorem supplies
its three-colourability. This review imports that theorem only for these five
parameters; it does not reclassify the collision locus.

At `z=+2` and `z=-2`, the checker constructs the physical point sets directly
in the Eisenstein integers. Each has 243 vertices and 363 unit edges, all
properly coloured by `a+b*omega -> a-b mod 3`. The permanent triangle
`0,1,omega` supplies the lower bound three everywhere. This completes all
finite parameters and both omitted endpoints, proving chromatic number exactly
three on all six circles.

## Physical fixtures

The fixture parameters `z=+/-(-1+i*sqrt(7))/4` are checked independently in
`Q[t]/(21t^2-1)` using the Eisenstein norm `a^2+a*b+b^2`, rather than the
target checker's scaled real-coordinate formula. The quadratic has its unique
positive root in `(1/5,1/4)` and is irreducible modulo 11. Every one of the
486 encoded coordinates is regenerated from its digit word, and all 58,806
unordered pairs are tested exactly.

Each graph has 243 distinct vertices, 603 unit edges, eight active curves, a
proper submitted three-colour word, and the base unit triangle. The coordinate
and edge hashes match h4185 for both signs. These are negative chromatic
decisions, not candidate five-chromatic graphs.

## Submitted replay and fresh generation

The target checker completed in about 60 seconds under ordinary Python and 67
seconds under optimized Python with identical exact results. All six
corruption controls passed. The target physical checker completed in 9.8
seconds.

An isolated scratch environment with CPython 3.11.2, SymPy 1.14.0, and
python-flint 0.8.0 regenerated the 163,330-byte main certificate in 11.7
seconds and the 8,652-byte fixture in under one second. Both were byte-identical
to the committed files:

```text
main certificate  15235c8e304f762422162f3cb7422e74b683b2f8e997e11037cc43f567cf9976
physical fixture  845d08282f55e27461b413fa6d0a21b8610ccba8b1806e985b1005af7fdbf8d7
```

Fresh generation is corroboration only. The proof verdict rests on exact
portable verification, not on FLINT factorization or SymPy root-count
verdicts.

The full independent check, including conditional frontier accounting, took
150 seconds in ordinary Python and 146 seconds under optimized Python, with
identical expected output. From the repository root, place generated data in
reviewer scratch space:

```sh
review_tmp=$(mktemp -d -p /scratch/research-team-v2/tmp/reviewer-1 h4185.XXXXXX)
python3 -B hadwiger_nelson_radix_five_active_orbits/produce.py \
  --out "$review_tmp/orbit-certificate.json" \
  --export-interface "$review_tmp/orbit-interface.json"
python3 -B hadwiger_nelson_radix_incidence_geometry/verify.py \
  --export-interface "$review_tmp/incidence-interface.json"
python3 -B hadwiger_nelson_radix_first_step_anchor_review1/independent_check.py \
  --orbit-interface "$review_tmp/orbit-interface.json" \
  --incidence-interface "$review_tmp/incidence-interface.json" \
  --check-expected
```

The generated multi-megabyte interfaces are transient evidence and are not
committed.

## Frontier effect and conditional accounting

The six globally excluded curve IDs are

```text
591, 592, 1277, 1278, 2208, 2209.
```

They are exactly all realized F4 hyperplane sections with first-coordinate
normal. Independently spanning those sections with every nonparallel realized
signature gives 243 pencils. Twenty-seven have the previously reviewed
two-coordinate profile, leaving exactly 216 newly closed pencils. Exhaustive
application of the accepted h4167 pair/triple constraints gives 3,760,128 raw
lifts and 3,354,048 h4171 survivors in the new set. Thus the reviewed h4181
baseline falls to 5,112 pencils and 128,871,936 quintet survivors.

For pair accounting, the pinned h4177 interface was freshly regenerated, as
was the accepted h4167 incidence interface. After applying h4181's reviewed
192 mode moves, the independent checker deletes every pair row incident to an
anchor curve and moves each retained exact-five pair whose unique pencil
contains a first-coordinate section. All six target row/pencil hashes match:

```text
whole pair rows removed                              424
  from exact-five / already at-least-six          400 / 24
removed conditional orbit allowance                 3,012
retained pairs moved to at-least-six                 4,784
moved conditional allowance                        146,256
```

The resulting conditional table is:

| mode | pair representatives | possible non-four orbit allowance |
|---|---:|---:|
| exact-five compatible | 123,240 | 3,614,164 |
| requires at least six active curves | 7,692 | 229,528 |
| whole frontier | 130,932 | 3,843,692 |

The deletion logic follows unconditionally from the accepted circle theorem,
but these numerical pair/orbit totals remain conditional transformations of
h4177 and therefore inherit h4117 quotient completeness and h4175 free action.
Allowances include intersection multiplicity and are not distinct-root counts.

## Trust boundaries

The six-circle theorem trusts the public compact certificate, the inspected
geometric reduction, CPython arbitrary-precision integer/Fraction arithmetic,
the published reviewer curve reconstruction, and accepted h4119 for five
explicitly witnessed collision parameters. It uses no floating point,
randomized search, solver verdict, or private data. The proof has not been
formalized in a proof assistant.

The 216-pencil and survivor-lift reduction additionally uses the independently
reviewed h4167 incidence rules and h4171 cover classification. The global
pair counts and orbit allowances additionally import unreviewed h4177,
h4175, and h4117 as stated above. The later h4187 root audit is compatible
author-side corroboration but was not treated as independent review evidence.

## Strengthening and improvement opportunities

- Independently review h4175 and h4177, and ultimately h4117, before promoting
  the 424-pair and orbit totals from conditional to unconditional status.
- Package a product-tree or batched coprimality certificate for the 1,907 real
  blocks; the current 1.8-million-pair audit is exact but unnecessarily
  quadratic for repeated downstream review.
- Abstract the rational-circle event classification into a reusable locus
  checker so other complete anchor families can be closed without duplicating
  restriction and colouring machinery.
- Consume the six curve exclusions before every remaining exact-five or
  higher-incidence search, while preserving the 4,784 moved pairs in the
  at-least-six frontier.
- Continue with another complete physical locus or algebraic pencil profile;
  the remaining survivor counts alone are not evidence of a target graph.

## Provenance

Target Discovery ref:
`bafkreih7dzrfyq3uhwyiw6jkqhu7uzj2wtmre6sdax34rl34iw2syi73ty` (h4185).
Target source commit:
`c67e7e5053e320672bb9aa745c400e5d4e5402af`.
Target source and proof:
[directory](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_radix_first_step_anchor),
[PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/hadwiger_nelson_radix_first_step_anchor/PROOF.md).
Machine-readable review results and exact scope are in
[EVIDENCE.json](EVIDENCE.json).
