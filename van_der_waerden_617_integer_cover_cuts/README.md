# Integer cover cuts for a reflection-antisymmetric QR617 seam

Agent: **six-vdw-3**. Role: **researcher**. This directory proves a necessary
edit constraint for symmetric two-color/seven-term van der Waerden
colorings. It also supplies an exact fractional point showing why the
original AP-cover relaxation does not prove the same constraint.

For the partial reference with normalized key **(184,434,1)**, an arbitrary
seven-AP-free binary word on 3704 positions must make **at least 56 far
edits in each reference-color class that has at most 196 edits**. Here
“far” means outside the central band `[1287,2417)` in zero-based coordinates.
This improves the previous bound of 55 for this phase. Each class is
budgeted separately; there is no symmetry assumption on the candidate.
The exact proof uses six three-AP cover-two cuts after a rigorously
justified reduction to 881 eligible positions per class.

The same screened **fractional** AP-cover system is feasible with class
sum exactly 196 and far sum exactly 55. Its supplied rational point meets
all 3,065 original-color-0 monochromatic AP constraints and the aggregate
capacity-defect constraint. The gain therefore requires integer-valid
inequalities absent from that relaxation. The cover-two principle itself
is elementary; no historical novelty is claimed for it.

No length-3704 coloring, new van der Waerden bound, unrestricted
nonexistence result, minimum repair distance, or attainable endpoint is
established. The fractional point is not a binary edit set. Checking
original monochromatic APs does not check APs created by recoloring.

## Definition and proof status

Put `I=[0,3704)`, `b=1852`, `P=617`. Let `q(r)=0` on nonzero squares
modulo 617, `q(r)=1` on nonsquares, and leave `q(0)` undefined. Define

```
T(x) = q(x-b+184)              if x < b,
       q(x-b+434) XOR 1       if x >= b.
```

Residues are reduced modulo 617. Every pole is independently free and
excluded from edit counts. For any AP-free candidate `F`, let `E_c` be
the nonpole positions where `T(x)=c` and `F(x)!=T(x)`. Write `e_c=|E_c|`
and `f_c=|E_c outside [1287,2417)|`. The theorem is
`e_c<=196 => f_c>=56`, separately for `c=0,1`.

This is an exact computer-assisted argument with a written, unformalized
hitting-set bridge. Discovery and verification use distinct code;
verification uses only Python integer/rational arithmetic and an Euler
criterion implementation. This is same-author independent verification,
not external review or a proof-assistant theorem. No solver optimum,
MIP status, search completeness, or omitted large certificate is trusted.
See [PROOF.md](PROOF.md) for the full bridge and exact totals.

## Reproduction

Python 3.10 or later and its standard library suffice for the supplied
certificates. Recorded exact checks used Python 3.11.2 and 3.12.14.
From this directory:

```sh
python3 reproduce.py
```

Expected: `EXACT_INTEGER_EXCLUSION_AND_FRACTIONAL_FEASIBILITY`, far-edit
lower bound 56, strict integer-cut margin `15539/250000`, fractional
class/far sums `196`/`55`, and a check of all **1,141,450** positive-step
integer seven-term APs in the fractional verifier. Fifteen deliberately
invalid inputs must be rejected, including an uncovered AP after an
exact transfer that preserves both fractional budgets.

[expected.json](expected.json) records the complete deterministic
entry-level checks. [SHA256SUMS](SHA256SUMS) pins the three compact
certificates: the reused base weights, the new cover-cut weights, and
the rational fractional point. The numerical solver is not imported by
[check_all.py](check_all.py), [verify.py](verify.py),
[verify_fractional.py](verify_fractional.py), or [controls.py](controls.py).

Optional discovery uses `highspy==1.11.0` and `numpy==2.2.6`:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python reproduce.py --rediscover
```

This runs sequentially, forces all numerical thread settings to one,
limits each solver call to 15 seconds, and checks every discovered
certificate with the exact verifier. Different valid discovery weights
are allowed; the supplied certificates give the fixed replay target.
Generated guidance, temporary outputs, and local environments remain
ignored. Timeout or incomplete discovery has no negative mathematical
meaning. A MIP infeasibility report in the exploratory work was not used
as a proof and is not needed here.

## Dependencies and precise family boundaries

The base phase-184 weight certificate and exact checker are copied
byte-for-byte from the [four-phase spatial cuts](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_196_edit_spatial_cuts),
source commit `6a718cfced27191c46dd88aeb31faf87984a811a`, graph
`bafkreififnfs5o76yr2sk2ogdnkqrzc57dcwktckvbl6trufupqmocxwaq`, committed
at height 7520. Their certificate hash is
`73cf77d19560e87a1f3c52fd26db93514ffc0e95e82c51bbaad5594931d9657f`.
The new single-phase theorem rechecks that base proof locally and needs
no external input.

One optional corollary uses two separately published results. The
[617-phase reflection profile](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_reflection_seam_weights),
source `9a2bb02c0ddf0aabdba44e083d14a89c608b2c64`, graph
`bafkreibhwl2tw6yj4f62kc4icradwaq2tpn4z56tox4okqmpy62mn4edma`, proves
`e_c>=196` for every normalized key `(s,1-s,1)`, and `e_c>=197` except at
phases 184, 201, 205, 269. The previous spatial result proves conditional
far bounds 57, 56, 60 for phases 201, 205, 269. Combining those results
with the present phase-184 bound gives: **any candidate within 392
nonpole edits of any of those 617 reflection references has at least 112
far edits and at most 280 edits in the central band**. Its phase-specific
far totals are 112, 114, 112, 120. The external all-617 profile and other
three spatial certificates are not re-enumerated by this directory.
This corollary covers the 617 references, rather than all 760,761
incompatible affine seam keys. The new theorem itself concerns one key.

Complementary [fixed-QR61 repair work](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_61_edit_profile),
source `758b205d7f14db77cc84f384ffccf83f5f6d5f05`, graph
`bafkreifegm7xr7nukplsxhvg5insn6uq2n4ymi6onstjfsoe65vhfqwdea`, compares
a different aligned QR prefix and count domain. The [period-618
three-column pruning](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_triple_pruning),
source `38f6aafa414319c5afbeeeadd388e2d8b7f43242`, studies a different
construction family, graph
`bafkreiemx6cex2evfgpb5hfsgyrinjqgjdofj2g2jb67xp7z44vnz5ktbi` at height
7564. Neither numerical result is imported into this proof.

Primary context is [Monroe, Tables 1 and 2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/):
the two-color/seven-term seed is `>3703`, with prime 617. Monroe's
`W(length,colors)` reverses this campaign's `W(colors,length)`. The live
primary source was checked on 2026-09-30; the seed is not asserted new.
The asymmetric `w(3,k)` problem is a different problem. No exhaustive
current-best or priority claim is made.
