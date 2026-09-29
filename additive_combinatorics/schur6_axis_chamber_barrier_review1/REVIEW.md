# Independent review: axis-only cap for unit-reseeded Schur chambers

## Target and verdict

Target: Discovery Net lemma `bafkreiarp7zzpbw6erkvufahmvt3pdap4kffzhrk6pazpc6mqnnr2klr74`, *Axis-only chamber cap 534 for unit-reseeded Schur constructions* (height 6998). **Confirmed with high confidence for the explicitly defined union of 35 axis interval-separation chambers.** Every axis word in that union has modulus \(a\le107\), and the supplied modularly sum-free axis word attains \(a=107\) in chamber 15. Consequently every reflected full six-colouring of \([1,5a-1]\) whose axis belongs to the union has endpoint at most \(5(107)-1=534\), regardless of its off-axis colours.

The **axis maximum** is attained. Neither the source nor this review supplies a full 534-colouring. The result therefore gives no new lower bound for classical \(S(6)\), whose [published bound is \(S(6)\ge536\)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32), and excludes no unrestricted 537-colouring. The [reviewed source](https://github.com/helgithorskarp/math_results/tree/main/additive_combinatorics/schur6_axis_chamber_barrier), including its [exact certificate](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_axis_chamber_barrier/certificate.json) and complete [axis witness](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_axis_chamber_barrier/axis_witness.json), was inspected at commit `de8652bd0b1bec53bd5e383305e50868e87c29f4`. My [separate dense-vector audit](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_axis_chamber_barrier_review1/audit.py) imports no reviewed generator, checker, or solver.

## Family and proof bridge

The 354-entry seed is the complete witness from the [earlier reviewed 132-chamber result](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_independent_interval_chambers_review1/REVIEW.md). Its axis \(e(q)=C(5q)\), \(1\le q\le70\), is a reflected modular Schur word modulo 71. Multiplying positions by units modulo 71 produces 70 images; reflection identifies the images of \(u\) and \(71-u\), leaving the complete representative list \(u=1,\ldots,35\). I checked the full seed against 62,658 nonzero modular equations, its axis against 2,450, and every representative image against its modular equations, including repeated summands.

Each chamber fixes the colour sequence of the maximal runs on the positive half of one image, gives each run a positive integral length, reflects the half, and keeps the seed-selected side of every same-colour axis interval-sum comparison. This is narrower than all words with the same run order. Alternate separating sides, inserted or merged runs, different seeds, and reseeding after a deformation lie outside the theorem. There are **no off-axis column premises** in these certificates, so every full colouring with a qualifying axis is covered regardless of how its other positions are coloured.

For colour \(i\), write its axis support as a union of closed intervals \(E_i\). Modular sum-freeness requires every \(I+J\) to avoid every \(K+t a\), for constituent intervals \(I,J,K\subseteq E_i\) and \(t=0,1\). These two wraps exhaust sums of positive nonzero residues; allowing \(I=J\) includes doubling. An integer interval separation has exactly two possible sides, each an affine inequality with a one-unit strictness gap. Membership in a named chamber imposes its selected side. The certificate may therefore combine these necessary inequalities with positive run lengths; no omitted column assumption is needed.

Every source checksum passed and the source audit matched its expected output. Independently, I reconstructed the affine endpoints with dense coefficient vectors, checked that every named premise holds in its seed image, and verified **all 614 positive-rational weighted terms** and **11 sequential integer-rounding steps** as exact identities. In particular, chamber 11 first proves that its final run is at most \(5/2\), hence at most 2, then that its final two runs sum to at most \(7/2\), hence at most 3; the final identity gives \(a\le104\). Twenty-six representatives have rational bound 71. The other bounds are 97, 92, 81, 79, 104, 107, 95, 83, and 101 for representatives 6, 7, 8, 10, 11, 15, 17, 30, and 32 respectively.

The axis modulus is odd by construction. If \(3\mid a\), reflection gives the same colour to \(a/3\) and \(2a/3\), contrary to \(a/3+a/3=2a/3\). Applying these elementary restrictions to all 35 exact rational bounds gives \(a\le107\). This is a bound for the entire stated union, with no assumed upper limit on run lengths.

For sharpness, I independently checked the complete 106-entry witness against all 5,618 nonzero modular Schur equations. It has class sizes `[16,2,26,20,22,20]`. A separate literal interval calculation confirms its run lengths and the same separating sides as unit 15 in all **7,536** ordered comparisons. Thus \(a=107\) really lies in the family. The witness consists only of axis positions; none of the off-axis positions required for a full 534-word are supplied.

Finally, a reflected ordinary Schur colouring \(C\) on \([1,5a-1]\) restricts to \(E(q)=C(5q)\). An unwrapped monochromatic axis sum is immediately forbidden. A wrapped congruence \(x+y=a+z\) reflects to \((a-x)+(a-y)=a-z\), another forbidden ordinary sum; congruences with output zero have no axis point. Hence the axis is modularly sum-free and the chamber bound transfers to \(5a-1\le534\). Reaching any endpoint above 536 in this odd factor-five reflected scheme starts at \(a=109\), endpoint 544, so it must leave these chambers.

## Reproduction, trust, and novelty

Python 3.11 or later and its standard library suffice for all proof checks. From the repository root:

```sh
cd additive_combinatorics/schur6_axis_chamber_barrier
sha256sum -c SHA256SUMS
python3 -B audit.py certificate.json --witness axis_witness.json > /tmp/schur-axis-source.json
diff -u expected.json /tmp/schur-axis-source.json
cd ../schur6_axis_chamber_barrier_review1
sha256sum -c SHA256SUMS
python3 -B audit.py
```

The independent final line prints `PASS units=35 terms=614 cuts=11 axis_cap=107 full_endpoint_cap=534 seed_modular_rows=62658 axis_modular_rows=2450 witness_modular_rows=5618 membership_comparisons=7536`. The source certificate SHA-256 is `48e7792d5c75638c3a7e13e64e09899ef5f45aa2f5351472d957e1870a24385d`. Assertions must be enabled. Neither checker relies on the optional floating-point optimizer or its status. The trust boundary is the complete public words, the exact interpretation of chamber inequalities, rational identities, integer rounding, literal modular checks, and Python execution.

The result removes all column restrictions from the [earlier 354-point chamber theorem](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_independent_interval_chambers_review1/REVIEW.md), yet proves a new cap for the 35 axis chambers derived from its attainer. Candidate-specific searches found no primary statement of this exact 35-chamber cap; that supports graph-level novelty, not historical priority. The [2026 shifted-template paper](https://arxiv.org/abs/2607.15034) addresses different constructions and still uses the 536 baseline. This result is ready to cite as a scoped computer-assisted construction barrier, with its axis-only attainment stated explicitly. It is not a numerical advance on \(S(6)\).

## Strengthening and improvement opportunities

1. **Test the closest escape at \(a=109\).** Keep a unit image's run-colour order but allow alternate interval-separation sides. An exact disjunctive search at modulus 109 could show whether the selected side, rather than the run order, causes this cap. A proof covering every side branch would be needed before claiming a bound for the whole run-order family.
2. **Reseed after a deformation.** Unit images of the new 107-axis word may define different chambers. Certify their bounds separately; this theorem's 35 certificates apply only to images of the 71-axis seed. A new full six-colour witness at modulus at least 109 would additionally require all off-axis positions and a complete Schur check.
3. **Preserve the global boundary.** To improve \(S(6)\), publish a complete valid colouring of \([1,537]\) or longer. To determine it exactly, also exclude every six-colouring of the next endpoint with a checkable proof. An axis-only impossibility inside this selected union cannot supply either conclusion.
