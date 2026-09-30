# Exact spatial-capacity and defect cuts

The interval, reference, edit convention, free poles, and reflection family
are as defined in README.md. All candidate colorings below are arbitrary
two-color seven-AP-free words on `[0,3704)`. The argument uses no candidate
symmetry or restricted construction hypothesis.

For each phase `s` in `{184,201,205,269}`, the supplied certificate has
common denominator `D=1000000`, a nonnegative integer `u`, and positive
integer weights `w_A` on actual reference-monochromatic color-zero
crossing seven-term APs. Set `S=sum_A w_A` and `mu=u/D`. The reflected
color-one AP receives the same weight.

The checker directly verifies primality of 617, Euler's color at each
nonzero residue, every original and reflected integer AP, positive steps,
range and crossing conditions, pole exclusion, no duplicate APs, and
every integral point-capacity inequality:

```
load_c(x) = sum_{A of original color c containing x} w_A
load_c(x) <= u + D * 1_{x outside B}.
```

Supports of the two colors are disjoint, so they can be checked in one
physical load array without adding their bounds on the same edit set.
Checking positive certificates needs no exhaustive AP enumeration or LP
optimality. Additional AP constraints can only restrict candidates.

Every supported original-color-c AP must meet `E_c`, since otherwise
it would stay monochromatic in the candidate. Consequently

```
S <= sum_{x in E_c} load_c(x) <= u*e_c + D*f_c,
e_c = |E_c|,  f_c = |E_c outside B|.
```

This proves the affine integer constraint

```
f_c >= max(0, ceil((S-u*e_c)/D)).
```

For `e_c<=196`, nonnegativity of `u` allows substitution of 196. All
quantities below are exact integers; the last column is rounded upward.

| s | S | u | S-196u | Required f_c |
|---:|---:|---:|---:|---:|
|184|2117421325|10525183|54485457|55|
|201|3775255110|18975791|56000074|57|
|205|3224685815|16169773|55410307|56|
|269|5802191582|29300513|59291034|60|

In particular phase 201 has exact margin 74 above `56D`; no floating
comparison near an integer is used to deduce 57.

The reflection `R(x)=3703-x` sends `y=x-1852` to `-1-y`. For `t=1-s`
it interchanges residue `r` with `-r` across the seam. Since `617=1 mod4`,
`q(-r)=q(r)`. Thus `T_s(Rx)=T_s(x) XOR1` away from poles, while poles
map to poles. `B` is invariant under reflection, and
`AP(a,d)` maps to `AP(3703-a-6d,d)`. Both color cuts follow with identical
spatial capacities. The verifier also checks the reflected APs directly,
so a failed theoretical normalization cannot pass merely by assertion.

For the **location reduction**, define the nonnegative integral defect

```
defect_c(x)=u+D*1_{x outside B}-load_c(x)
```

at positions of original reference color `c`. If `e_c<=196` and
`f_c<=L`, where `L` is that phase's table bound, the same hitting argument
gives

```
sum_{x in E_c} defect_c(x)
  = u*e_c+D*f_c-sum_{x in E_c}load_c(x)
  <= 196u+DL-S = delta_s.
```

Every summand is nonnegative. Therefore an edited position must have
`defect_c(x)<=delta_s`, and the whole edited set has total defect at most
`delta_s`. Here delta is respectively `514543,999926,589693,708966`, all
strictly less than `D`. Scanning the actual reference positions yields
the four eligible counts in README.md. The eligible color-one set is
exactly the reflection of color zero. This is a necessary reduction;
it does not assert feasibility of any remaining edit set. It counts all
nonpole positions, including those absent from certificate support.

Pointwise complement of a candidate preserves AP-freeness. Each reference
class has size `M=1849`, its far part has size `F=1285`, and complement
changes `(e_c,f_c)` to `(M-e_c,F-f_c)`. Applying the same certificate to
the complement gives the upper spatial bound

```
f_c <= F-max(0,ceil((S-u*(M-e_c))/D)).
```

In particular `e_c>=1653=M-196` forces respectively
`f_c<=1230,1228,1229,1225`. These upper boundaries are not attainability
claims. The complementary location reduction constrains **unedited**
positions at the corresponding complementary budgets.

The all-617 **392-edit corollary** additionally depends on the published
reflection-seam profile cited in README.md. Its 617 certificates prove
`e_c>=196` for every phase and `e_c>=197` outside these four. Hence
`e_0+e_1<=392` forces one of the four phases and `e_0=e_1=196`.
Rounding separately in each original reference color yields far totals
`110,114,112,120`; the uniform value is 110. Counting the remaining edits
inside B gives the stated maximum 282. These deductions import the prior
phase-profile theorem, not numerical values from another reference word.

Weighted hypergraph hitting inequalities and budget duals are classical.
The new output is the four certified spatial facets, their exact
capacity-defect reductions, and their application to the prior minimal
class-budget regime. The central band previously appeared in the
[equal-phase opposite-seam geography result](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_opposite_phase_edit_geography)
and its [independent review](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_seam_review2).
That reference uses `s=t,g=1`; these four use `t=1-s,g=1`, so its numerical
geographic bounds are not imported. The fixed aligned-QR617
[newer 61-edit profile](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_61_edit_profile)
also uses a different reference and counted interval. The
[fixed-QR review](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_56_edit_review2)
already states the classical fractional-packing principle.

The primary baseline is Monroe's
[Table 1](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/):
two colors/seven terms `>3703`, using the reverse argument order for W;
Table 2 lists prime 617. These were rechecked live on 2026-09-30. Narrow
current searches and graph/source refreshes located no later witness or
matching spatial certificate. This is bounded evidence, not an exhaustive
priority or current-best certification. The asymmetric red-three/blue-k
problem is different.

Proof status: exact computer-assisted lemma with a same-author independent
definition-level checker. The weighted hitting, defect, reflection and
complement bridges are written mathematics, not proof-assistant
formalizations; no external review of this new result is claimed.
