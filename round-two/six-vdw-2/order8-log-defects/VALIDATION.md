# Validation and limits

Actual agent: **six-vdw-2**; role: **researcher**.

Fresh full reproduction on2026-10-01 used CPython3.11.2,
GCC12.2.0 (`-O2 -std=gnu99` for the untrusted converter),
python-sat1.8.dev24, six1.17.0 and its CaDiCaL1.9.5.
Source-only generation and checking use the Python standard library.
Every child job ran serially with all native thread limits set to one.

* Exact CNF:1078 variables,48556 clauses. The direct auditor checked every
  (a,d) in F617 x F617*, including375760 retained and4312 omitted pairs.
  All23177 complete coset supports matched entry by entry.
* The counter checked3586 exhaustive inputs with1..8 variables and all
  admissible bounds; the equality gadget checked all eight assignments.
* Fresh proposal:105671 conflicts,116398 decisions and4833554 propagations,
  under the150000-conflict limit. Proposal stage14.303s; conversion11.519s.
* Exact RUP replay:84215 additions,132727 deletions and2000751 propagation
  hints. Normal and optimized Python results agree, including trace hashes.
* Proof controls covered all256 families of nonempty nontautological clauses
  on two variables.161 UNSAT families had accepted exact RUP refutations;
  forged refutations for all95 SAT families were rejected.
* Nine production corruptions were rejected: nonexistent hint, negative
  RAT hint, out-of-domain literal, missing terminator, no empty conclusion,
  nonexistent deletion, omitted counter-bound unit, reversed bound unit,
  and a replaced field-AP clause. All controls passed in normal and -O modes.
* A one-conflict proposal returned UNKNOWN and emitted no proof artifact.

The complete fresh sequence took65.752s, parent peak54776KiB,
largest child109120KiB. Timing is machine-dependent; source reproduction
does not assume identical timings. Each child has a30s external timeout;
the converter also has25s internally. Proof checking itself is exact and
uses no floating-point mathematical decisions.

Hash expectations and reference RUP counts are in expected.json.
Regenerated proofs need not match bytes if solver/platform behavior changes:
the CNF must match, and the separate exact checker must validate the entire
proof and its empty conclusion. A changed proof is not accepted merely for
having the same counts. The final status is issued only after all checks.

Exploratory probes are deliberately outside the public source directory:
the rank<=5 subsystem was SAT, including a three-defect model, and its
model fails a direct full AP check. The rank<=6 system returned UNKNOWN at
200000 conflicts. The unrestricted normalized full system timed out at30s.
A library-cardinality E<=13 probe returned UNKNOWN at150000 conflicts.
The E<=9 and new explicit-counter E<=11 contradictions were checked;
only the stronger E>=13 claim is published here. These other probes establish
no exclusion or attainment at the remaining frontier.

The known QR617 word was separately reconstructed: its3703-position prefix
has no monochromatic AP among1140833 progressions. The chosen3704-word
has exactly(a=2,d=617,color0) among1141450 progressions. This validates the
known seed and endpoint convention; it is not new research and is not a
premise for the order-eight cut.

No proof assistant, global interval exclusion, minimum defect attainment,
independent reviewer verdict, latest-record priority, new W bound or
3704-point witness is asserted.
