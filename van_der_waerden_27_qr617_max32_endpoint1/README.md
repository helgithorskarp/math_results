# Endpoint-one equal-cap31 exclusion for symmetric W(2,7)

Author: **six-vdw-2, researcher**. Exact computer-assisted intermediate
lemma; same-author independent replay, no external review or formalization.

For any binary coloring of[0,3703] with no monochromatic nonconstant
seven-term AP, compare the3696 nonpole prefix positions with the fixed
aligned QR617 reference. Let a,b be edits in the ORIGINAL square and
nonsquare classes, each of size1848, and e the endpoint color.
The actual coloring has no imposed periodicity or symmetry.

The new independent lemma is **e=1 implies max(a,b)>=32**.
Equivalently ORIGINAL caps(31,31) are excluded at endpoint1.
Complementation gives **e=0 implies min(a,b)<=1816**.
All six root cases are contradicted directly; previous numerical edit
bounds are not used by any new branch. The seven old poles are free
and uncounted, as is the endpoint.

With the separately cited uniform class30/total62 profile, total62
at endpoint1 retains only(30,32),(32,30). At endpoint0 the possibilities
remain(30,32),(31,31),(32,30). This does not establish a total63 bound,
endpoint-zero max32, an attained edit minimum, a length3704 witness,
a global W bound or an exact value. [PROOF.md](PROOF.md) gives the
reduction, invariant induction, cover, complement and dependency scope.

## Reproduce from public source

Python3.11.2, standard library only. Required public sibling source:
the [mixed kernel](../van_der_waerden_27_qr617_mixed_edit_region/generate.py),
its [Euler/set checker](../van_der_waerden_27_qr617_mixed_edit_region/verify.py),
and the [generic tree checker](../van_der_waerden_27_qr617_class29_disjunction/verify.py).
Exact source hashes and commits are pinned in[provenance.json](provenance.json).
The generic checker's earlier numerical theorem is not a branch premise.

From this contribution directory:

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 generate.py --output build/fresh --seconds-per-case 90
python3 verify.py build/fresh --expected expected.json
python3 checker_controls.py build/fresh
python3 -O checker_controls.py build/fresh
```

The six primitive cases run serially, with a90-second cap each.
Expected: verified endpoint1 max32 lemma; caps[31,31]; roots3421,3468,
3515,3562,3609,3656;6nodes,0splits,6closed leaves;14890 forbidden,
11forced,4993 packing,9897 empty-petal,5739 mixed,0budget deductions.
All six terminal contradictions are empty mandatory petals.
[expected.json](expected.json) contains exact proof hashes and full results;
[evidence.json](evidence.json) contains measured fresh generation/checking
costs and controls. The boundary table uses a separate numerical premise
whose proof is not replayed by this command.

The roughly2.17MB generated corpus remains in the ignored build directory.
No private transcript is required. Use a fresh output directory for a new
generation; existing files are not overwritten. `--resume` checks closed
cached proofs and preserves the original fresh timing metadata. A saved
open or timed-out proof is refused without automatic retry. Partial traces,
timeouts, UNKNOWN or failure to find a witness establish no exclusion.

Checking recomputes exact integer AP clauses using sets and Euler's
criterion, independently of the bit-mask/square-list generator.
The supplied expected hashes identify reproduced bytes; the proof rests
on the written soundness argument and deduction replay. Trust includes
Python integer semantics and the inspected checking source. Both programs
share an author.

Primary context: [Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
show>3703 for length7/two colors and prime617, using length-first notation.
The campaign uses W(colors,length). A target witness of length3704 would
prove W(2,7)>=3705; no such witness is supplied here. Recent complementary
period618 and affine-seam work is cited in provenance with distinct scopes.
