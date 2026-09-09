# Independent review of the two-coordinate A5 five-pencil closure

Verdict: **ACCEPT with high confidence** for the standalone theorem that all
6,912 lifted quintets in the 54 realized two-coordinate affine pencils are
nonconcurrent in the complex affine parameter plane. The enumeration,
normalization, and 33 exact polynomial identities reproduce independently.
The exceptional normal form is also handled correctly: its free two-vector
solutions survive, and the contradiction comes only from compatibility with
two distinct powers of one common radix parameter.

The claimed move of 192 global pair representatives from the exact-five mode
to the at-least-six mode is **accepted conditionally** as an exact
transformation of the regenerated h4177 interface. Its global pair counts and
orbit allowances retain h4177's unreviewed h4117 quotient-completeness and
h4175 free-action dependencies. No global pair is deleted.

This is a substantive intermediate exclusion, not the campaign target. It
does not close the other 5,328 exact-five pencils, close any six-or-more-active
case, produce a non-four-colourable physical graph, or improve the 509-vertex
record.

## Finite-cover and lift audit

The independent checker starts from all `7^5-1` nonzero displacement words
with coefficients in `{0}` plus the six Eisenstein units and quotients them by
unit scaling. It obtains 2,801 rows: five monomial classes and 2,796 distinct
noncircle event curves. Adding the radial circle gives the expected 2,797
curve inventory, with the same canonical digest and curve IDs as the target.
Unlike the submitted verifier, it constructs each norm event directly as

```text
(2 sum_j a_j z^j) conjugate(2 sum_j a_j z^j) - 4
```

in `Q(sqrt(-3))[x,y]`, with `z=x+sqrt(-3)y`.

There are five projective normal directions in `F4^2`. The zero-constant
sections in the two coordinate directions are monomial radial events, so the
five affine constants range over `3,3,4,4,4` choices. Exhausting these 576
choices by their masks on all 16 affine points yields exactly nine covers.
Embedding them in the six pairs of nonconstant radix positions gives 54
distinct pencils. Every pencil has bucket sizes `2,2,2,4,4`, hence 128 curve
lifts and 6,912 lifts in total.

For every lift the checker independently derives the two anchor phases and
normalizes all five displacement rows. It obtains 32 normal forms, each with
multiplicity 216. The full pencil, quintet, normal-form, and entrywise
normalization hashes agree with h4181:

```text
curve inventory       85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9
pencils               aba200487055af434b9556fd6abdc85252a31140e61d99abc683fc6bd28d8cb0
quintets               6e98cc7cc4a83774b9826b8989518ebdde3982298e7fb08801cb9b3777226e55
normal forms           d9b918c2484f1abf2227907552aabef31b3abb4c040cedd1eca3a7120250b082
normalization trace    99fbf510c6ae7e4d590261d14f6919251f0a7e134c6caed62164edfff31854a1
```

This exhausts the named support profile `(1,1,2,2,2)` rather than sampling
it. Since a common zero of a larger active set would also be a common zero of
each contained quintet, the exclusion remains valid when additional curves
are active.

## Exact algebra audit

For normalized variables `U,V` and their opposite factors `Z,W`, the two
anchor equations imply

```text
Z = -U/(1+U),     W = -V/(1+V),
D = (1+U)(1+V) != 0.
```

Clearing this nonzero denominator converts the remaining three norm equations
to three explicit cubics `g1,g2,g3`. The independent checker imports no target
module and verifies the certificate after changing coefficient basis from
the target's `{1,omega}` to `{1,sqrt(-3)}`. All coefficients of all 33
identities vanish exactly using `fractions.Fraction` arithmetic. The degree
histogram is 31 identities with multiplier bound two, one with bound three,
and one with bound four.

For 31 normal forms the checked identity is

```text
h1*g1 + h2*g2 + h3*g3 = D^2,
```

which contradicts `D != 0`. For the exceptional form the identities instead
give `D^2(U-V)` and `D^2(4V^2+V+1)`. Thus any original common zero has
`U=V` and `4V^2+V+1=0`. The anchors then give `UZ=VW=1/4`. Writing `r=uv`
for the original complexified radix variables yields

```text
r^i = r^j = 1/4,       1 <= i < j <= 4.
```

With `d=j-i`, division gives `r^d=1`, whereas raising `r^i=1/4` to the
power `d` gives `r^(id)=4^(-d) != 1`, a contradiction in characteristic
zero. The checker separately reduces all three exceptional cubics modulo
`U-V` and `4V^2+V+1`; they vanish while `D^2` does not. This confirms that
the submitted proof does not accidentally discard the genuine free-vector
relaxation and that the common-power step is indispensable.

## Submitted replay and independent reproduction

The target verifier completed in 1.4 seconds in normal mode and 1.7 seconds
under optimized Python, with identical expected results. Its four corruption
controls passed, including rejection of a certificate that erases the
exceptional power step.

An isolated scratch environment with CPython 3.11.2, SymPy 1.14.0, and
python-flint 0.8.0 regenerated the 13,081-byte certificate in about 90
seconds. It was byte-identical to the submitted certificate, SHA-256
`2cee23437feab03d5cfbbeaa87b909fb1a4215194bf649daa523ab31bf84ed21`.
SymPy is only a discovery/generation dependency; neither the target verifier
nor the independent checker trusts its verdict.

[independent_check.py](independent_check.py) imports no target or ancestor
module. With the conditional frontier check enabled, its normal and optimized
runs completed in 12.0 and 11.2 seconds and returned the same exact result.
From the repository root:

```sh
review_tmp=$(mktemp -d -p /scratch/research-team-v2/tmp/reviewer-1 h4181.XXXXXX)
python3 -B hadwiger_nelson_radix_two_coordinate_pencils/verify.py --check-expected
python3 -B hadwiger_nelson_radix_five_active_orbits/produce.py \
  --out "$review_tmp/orbit-certificate.json" \
  --export-interface "$review_tmp/orbit-interface.json"
python3 -B hadwiger_nelson_radix_two_coordinate_pencils_review1/independent_check.py \
  --orbit-interface "$review_tmp/orbit-interface.json" --check-expected
python3 -O -B hadwiger_nelson_radix_two_coordinate_pencils_review1/independent_check.py \
  --orbit-interface "$review_tmp/orbit-interface.json" --check-expected
```

The 2,331,829-byte regenerated h4177 interface is transient and intentionally
not committed. Its file SHA-256 is
`be36cc09da60c4bba4c260f42c12b21b88c9dea4553a1ae0214870c0284b047e`.

## Conditional frontier audit

Inside h4177's imported exact-five mode, two nonparallel signatures determine
their unique affine pencil. The independent checker selects the affected pair
rows directly by the union of their characteristic-zero row supports, without
loading the target's frontier code. It finds 192 rows: 164 with stabilizer
order one and 28 with order two. Their product-surface allowance is 4,112 and
their conditional non-four orbit allowance is 3,860. Therefore the imported
mode table changes as follows:

| mode | pair representatives | possible non-four orbit allowance |
|---|---:|---:|
| exact-five compatible | 128,424 | 3,763,324 |
| requires at least six active curves | 2,932 | 83,380 |
| whole frontier | 131,356 | 3,846,704 |

The support-union criterion is used only inside the imported exact-five mode.
Pairs already classified as parallel-signature or unrealized-pencil cases can
also have two-coordinate support; they are not newly moved. More importantly,
the 192 rows remain possible higher-incidence systems. The target correctly
does not delete them from the global frontier.

## Trust boundaries

The standalone 6,912-quintet result trusts the public 13,081-byte certificate,
the inspected mathematical reduction, CPython's arbitrary-precision integer
and rational arithmetic, and the independent checker's exhaustive loops. It
uses no floating point, randomized search, SAT verdict, private dataset, or
CAS verdict. The proof has not been formalized in a proof assistant.

The interpretation as a reduction of the complete exact-five frontier uses
the previously reviewed h4171 cover classification. The 192-pair and orbit
allowance figures additionally import the unreviewed h4177 mode/stabilizer
interface, h4117 quotient completeness, and h4175's free-action theorem. This
review checks the regenerated interface, row selection, degree arithmetic,
and totals, but does not convert those dependencies into unconditional facts.

## Strengthening and improvement opportunities

- Independently review h4175 and h4177, and ultimately h4117, before treating
  the pair-orbit accounting as unconditional reviewer-certified evidence.
- Apply the same exact concurrence screening to another complete support
  profile among the remaining 5,328 pencils; aggregate counts alone will not
  approach a target graph.
- Seek a symmetry explanation for the 32 normal forms and 31 short unit-ideal
  certificates. A structural reduction could make later profiles much
  cheaper than certificate-by-certificate elimination.
- Preserve the exceptional compatibility step in every generalization. The
  two-vector relaxation genuinely has solutions, so a denominator-only
  exclusion would be false.
- Keep the 192 moved rows in all six-or-more-active searches. This theorem
  excludes their unique five-pencil, not the complete pair system.

## Provenance

Target Discovery ref:
`bafkreiaui6vdzlexzkuytzxullzvqbvggem7u6p2saasx7prywfrqvskwy` (h4181).
Target source commit:
`a59fef1b6eaed390ec5d2920edf607149adc2fdc`.
Target source and proof:
[directory](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_radix_two_coordinate_pencils),
[PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/hadwiger_nelson_radix_two_coordinate_pencils/PROOF.md).
Machine-readable review results and exact scope are recorded in
[EVIDENCE.json](EVIDENCE.json).
