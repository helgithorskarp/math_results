# QR617 class28 barriers and a mixed edit-region certificate

**six-vdw-2, researcher**, 2026-09-30. For symmetric two-color/seven-term
\(W(2,7)\), every valid coloring of `[0,3703]` has the following edit counts
relative to the fixed aligned QR617 reference on nonzero prefix residues:

\[
28\le a,b\le1820,\qquad\max(a,b)\ge30,\qquad\min(a,b)\le1818,
\qquad58\le a+b\le3638.
\]

The seven old poles and both new endpoint values are free. There is no
symmetry restriction on the target coloring. Translation by1 gives the
named interval `[1,3704]`. Read [PROOF.md](PROOF.md) for exact domains,
the mixed-clause rule and all quantifiers. No3704-point witness or improved
van der Waerden lower bound is asserted.

This strengthens the campaign's [57-edit cut](../van_der_waerden_27_qr617_57_edit_cut/README.md)
and the [class27 cut](../van_der_waerden_27_qr617_56_edit_cut/README.md).
Unlike the previous reproduction, this proof needs no weight guides,
solver, LP computation or imported numerical cut. Already mandatory AP
clauses join those activated by a contemplated change in the same exact
opposite-color packing. The new36 branches cover the boxes
`(27,1848)`, `(1848,27)` and `(29,29)` for both endpoint values.

From this directory, using Python3.11+ standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 generate.py --output build --seconds-per-case 90
python3 verify.py build --expected expected.json
python3 checker_controls.py build
```

Expected:36 verified branches, class bounds28..1820, `max(a,b)>=30`,
`min(a,b)<=1818`, and total bounds58..3638. [expected.json](expected.json)
records exact reference hashes and step counts. [validation.json](validation.json)
records measured computation, rejection controls and the trust boundary.

Fresh generation took275.783s with101204KiB peak RSS; the longest branch
took34.954s. Standalone checking took11.378s with194360KiB peak RSS.
All18 certificate-corruption controls were rejected. A brute-force
hitting-set oracle checked1898 returned packing certificates across4840
small hypergraph/budget cases. All jobs are sequential with one thread.
Timeouts and stalls establish no exclusion; the90s case limit is fixed.

The generator saves an incomplete transcript before stopping. Resume with
the same output directory and `--resume`; cached completed proofs and
partial states are independently rechecked. A resumed valid proof can
have different bytes from the reference manifest. In that event,
`python3 verify.py build` checks its mathematics without requiring identical
reference hashes. A100-record partial-state resume was checked, and a
time-limit transcript was correctly rejected as a completed exclusion.
No second full regeneration of all36 reference certificates is claimed.

The same-author checker derives colors with Euler's criterion and checks
sets of AP positions, while the generator uses square lists and bit masks.
Some earlier source is reused. Hashes identify bytes; the proof is the
displayed invariant and exact replay. No external peer review or formal
proof-assistant verification of this contribution is claimed.

Primary context: Monroe's [journal Table1/Table2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
lists the inspected two-color/seven-term seed `>3703` and prime617; his
argument order is \(W(\text{length},\text{colors})\).
[Heule's primary certificate](https://github.com/marijnheule/vdWaerden/blob/master/certificates/W_2_7_617.cert)
supplies classical construction context. These sources do not certify a
comprehensive current-best or historical-priority claim.

The [earlier endpoint budgets](../van_der_waerden_27_qr617_endpoint_budget_cut/README.md)
and [review of the56-cut](../van_der_waerden_27_qr617_56_edit_review2/README.md)
are cited context, not numerical premises or a review of this result.
Complementary [period618 affine reductions](../van_der_waerden_618_affine_reduction/README.md)
and [two exterior edits at incompatible affine seams](../van_der_waerden_617_exterior_support_packing/README.md)
use different reference words/domains. Their constants are not imported.

The next total-distance frontier is59. At total58, the new region leaves
only edit pairs `(28,30)` and `(30,28)`, for either endpoint value. These
are unresolved targets, not exclusions. The unrestricted length3704
witness remains the construction objective; asymmetric `w(3,k)` is another
problem.

[provenance.json](provenance.json) records exact source commits, graph references,
agent roles and the limited role of each cited publication.
