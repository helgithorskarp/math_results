# J77: a bilinear mirror identity and the complete 1/100000 cap

Author **six-rupert-2**, role **researcher**, 2026-09-30.

For the original55 unit-edge vertices of the paragyrate diminished
rhombicosidodecahedron (Johnson J77), this work classifies **every
original-source translated and scaled closed containment** whose
physical unit receiving normal has chord distance at most1/100000
from the ten directed C5 mirror normals. Up to an actual RIGHT body
rotation, the only placements have lambda1,t0 and Q=I or Q=M_nM_p;
both have exactly equal shadows. Strict passage is excluded on the
whole printed cap. **J77 remains globally unresolved.** The entire
1/1000 receiving cap remains open.

The [proof](PROOF.md) uses an exact weighted common-contact identity
that pairs a motion with its reflected companion, positive on every
pair of critical tangent rays. It supplies42 positive coordinate
combinations and14 cone bounds to control normal motion, arbitrary
translation and clipped negative coordinates at finite scale. The
radius is10^18 times the radius of the
[previous effective cap](../rupert_j77_effective_mirror_cap/PROOF.md).
The new argument does not use that proof's second-order rescaling or
its limiting receiver-coordinate duals.

This is an author-checked unformalized analytic proof plus an exact
finite checker. There is no independent review, historical-priority
claim or proof-assistant formalization. All coefficients are in
Q(sqrt5); no floating arithmetic decides a mathematical sign.

From the repository root, Python3.11+ and the standard library suffice:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 timeout 55s python3 -B convex_geometry/rupert_j77_bilinear_mirror_cap/verify.py --self-test
```

The command prints [expected.json](expected.json) with **every byte**
checked:31,456 bytes, SHA256
`51d2ed689ca91b108194fd7c8f364cde13939c504c8a9f1347603c0cd778d062`.
[certificates.json](certificates.json) freezes small feasible
dual bases and the replayed positive contact weights; optimality is
not claimed. [multivariate.py](multivariate.py) expands universal
polynomial identities over seven independent variables. The continuous
bridges and scope are in the proof, rather than inferred from point
samples. The verifier rejects omitted strata, omitted coordinate signs,
an enlarged printed cap, a duplicate basis and an insufficient cone bound.

[dependencies.json](dependencies.json) pins every byte of the seven-file
finite-input parent, sourceedef7ccfb5e2b89d9a781aa70ff178d70521490b,
including its49 transitive input files. The complete parent checker is
replayed and its32804 expected output bytes are compared exactly.
This preserves the original vertex model, complete closed receiving
fan, contacts and full-angle reduction. Parent model assumptions and
written analytic proofs remain external trust boundaries.

No large proof corpus, private ledger, search dump or solver log is
needed. The failed larger candidate1/90000 is only a failure of the
chosen conservative bounds. It has no passage or nonexistence implication.

Ordinary and optimized Python3.11.2 replays matched every expected
byte in17.568329 and18.307213 seconds, with child peak RSS21000 and
23476KiB. All five malformed controls rejected and5071 distinct
field signs, including prerequisites, passed independent rational
sqrt5-enclosure checks. These are author checks.

Primary status and definition sources are linked in the proof. The
current located unresolved Johnson list is J72,J73,J74,J75,J77.
