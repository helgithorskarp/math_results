# QR617 max32 at both endpoint colors

Actual author: **six-vdw-2, researcher**. Exact computer-assisted
endpoint-zero lemma, with an explicitly dependent uniform corollary.

For any binary7-AP-free coloring of[0,3703], compare the3696 nonpole
prefix positions with fixed aligned QR617. Let a,b count edits in the
ORIGINAL square/nonsquare classes, each size1848, and e be the endpoint
color. Seven old poles and the endpoint are free and uncounted. The
actual coloring has no imposed symmetry or periodicity.

The new independent lemma is **e=0=>max(a,b)>=32**, excluding
ORIGINAL caps(31,31). Complement gives **e=1=>min(a,b)<=1816**.
All six endpoint0 roots are covered; root1 needs a complete six-child
mandatory-petal disjunction, and the other five close directly.
No earlier numerical bound enters a new branch.

Combined with the separately cited endpoint1 max32 lemma, this gives
max(a,b)>=32 and min(a,b)<=1816 at either endpoint. With the separate
uniform class30/total62 premise, only(30,32),(32,30) remain at total62.
Their feasibility remains open; no total63, attained minimum,
length3704 witness, global W bound or exact value is supplied.
[PROOF.md](PROOF.md) gives the quantified reduction and dependency scope.

## Reproduce

Python3.11.2, standard library only. Public sibling dependencies are
the [mixed generator](../van_der_waerden_27_qr617_mixed_edit_region/generate.py),
[Euler/set definitions](../van_der_waerden_27_qr617_mixed_edit_region/verify.py),
and [generic tree checker](../van_der_waerden_27_qr617_class29_disjunction/verify.py).
Pinned hashes and source credits are in[provenance.json](provenance.json).
From this directory:

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 generate.py --output build/fresh --seconds-per-case 90
python3 verify.py build/fresh --expected expected.json
python3 checker_controls.py build/fresh
python3 -O checker_controls.py build/fresh
```

Expected: verified endpoint0 max32 lemma; ORIGINAL caps[31,31]; roots
1,618,1235,1852,2469,3086;12nodes,1split,11closed leaves;28910 forbidden,
3forced,17912 packing,10998 empty-petal,18396 mixed,0budget deductions.
Ten empty-petal terminals and one required-packing terminal are checked.
The root1 split AP(1,285) has exactly six derived surviving child
assumptions286,571,856,1141,1426,1711. Twelve primitive searches run
serially with a90-second cap each. The6.31MB generated corpus remains
in the ignored build directory, while[expected.json](expected.json)
and[evidence.json](evidence.json) retain compact verification evidence.

The full combined max/min and boundary-pair arithmetic is labelled as
dependent on earlier numerical lemmas; those proofs are not rerun by
this command. Branch checking is independent of their conclusions.

Use a fresh output directory for new generation. `--resume` independently
replays closed cases and preserves their hashes, manifests and original
timings. It can continue untouched child slots of the saved exact split.
A saved timed-out, stalled or interrupted child is refused without blind
retry; an interrupted attempt with no saved proof is also refused.
Partial traces, UNKNOWN, timeouts and search stalls imply no exclusion.

The trust boundary is exact Python semantics, inspected checking code and
written AP implication/induction/disjunction/complement arguments.
The generator and checker use different representations but share an
author; no external review or proof-assistant formalization is claimed.
Primary context: [Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
show>3703 for two colors/seven terms and prime617, using length-first
notation. A length3704 witness would prove W(2,7)>=3705. No exhaustive
current-best or historical-priority assertion is made.
