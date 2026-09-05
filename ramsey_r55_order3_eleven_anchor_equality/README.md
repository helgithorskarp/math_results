# Two empty fixed signatures at the four-versus-seven anchor

In a hypothetical Ramsey(5,5;43) graph with ten fixed vertices, four red
moving triangles and seven blue moving triangles, **every nine-vertex
union of three red moving triangles with no blue triangle has at least
two fixed vertices blue to its whole union**.

The two possible anchor types are `100,110,110` and `110,110,101` on
pairs01,02,12. Both full extensions with exactly one such fixed vertex
are refuted. The fourth internally red triangle remains unrestricted.
This is a new full-extension signature restriction, not an exclusion
of an entire core. **34 four-versus-seven classes remain**, covering
24,057 labeled cores; the three-versus-eight branch is unchanged.
No target graph or Ramsey lower-bound improvement is claimed.

Read [PROOF.md](PROOF.md) for the two-type classification, inherited sharp
signature equality, revised full normalization, exact formula bridge and
scope. In original four-triangle signature coordinates the consequence
is `z+x_i>=2` whenever the complement of triangle i has no blue triangle.
This holds for every such i, not just one selected anchor.

## Evidence and reproduction

- [anchor.py](anchor.py): phase-based 343-word census, all residual
  anchor maps, complete formula generation from the pinned r=4 parent.
- [audit.py](audit.py): literal graphs and pair-orbit reconstruction,
  whole-formula comparison, entrywise census/map checks and ten
  corruption controls; imports no producer.
- [run.py](run.py) and [verify.py](verify.py): fixed two-case computation
  and fresh full reconstruction with second DRAT replay.
- [anchors.json](anchors.json): 45 blue-triangle-free labeled anchors,
  in classes of sizes27 and18; all56 applicable complements across the
  34 remaining twelve-vertex representatives.
- [result.json](result.json) and [verification.json](verification.json):
  full contracts, formula/trace hashes and both replay outcomes.
- [controls.json](controls.json), [parent_controls.json](parent_controls.json):
  normal/optimized negative controls and inherited parent checks.

Run from this directory using CPython3.11.2 and GCC12.2.0:

```bash
python3 -B run.py --work /scratch/new-r55-r4-anchor/full \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim \
  --solve-seconds 60 --replay-seconds 300
python3 -B verify.py --source-work /scratch/new-r55-r4-anchor/full \
  --work /scratch/new-r55-r4-anchor/verification \
  --drat-trim /path/to/drat-trim --replay-seconds 300
sha256sum -c SHA256SUMS
```

Exactly two cases run, with two workers. A STOP file in the external run
directory prevents a case from starting; an in-progress case is allowed
to finish its bounded solve and proof check. `--resume` requires the
unchanged contract and retained evidence and replays saved refutations.
Verification requires a fresh external directory. UNKNOWN is explicitly
open and is never a certificate or solver restart state. A SAT result
must decode to a compact edge list and pass the inherited independent
literal 43-vertex checker before being treated as a target.

Kissat4.0.4 source: `8af8e56f174b778aef3aa45af9f739b2a5f492c2`.
drat-trim source: `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
Executable and all proof-relevant source/input hashes are in the run
contract. GCC uses `-std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror`.
Only the Python standard library is needed. Tool and host timing may vary;
every regenerated UNSAT result must meet its full certificate obligation.

Each formula has34,280 variables and615,956 clauses. It retains the full
accepted r=4 parent except for exactly three incompatible red-cycle
ordering clauses, then adds nine anchor and thirty equality-prefix units.
No Ramsey or degree constraint is omitted. The full parent is rebuilt
and audited before the weakened normalization is checked.

Both cases are UNSAT, with successful full replay. Solve times were
2.069610 and1.154673 seconds. Proofs total25,787,323 bytes and contain
254 and109 RAT core lemmas. Total run time including reconstruction and
controls was67.847626 seconds; largest reported child RSS261,672KiB.
The fresh verifier rebuilds both complete formulas and replays both
traces again. Its exact duration is in `verification.json`. These are
not speed-comparison claims against the earlier different formulas.

## Dependencies and limits

The full parent and counters are imported from
[`ramsey_r55_order3_eleven_cycle_obstruction`](../ramsey_r55_order3_eleven_cycle_obstruction),
with its accepted review. The local sharp signature lemma and equality
come from the accepted
[`ramsey_r55_order3_eleven_signature_bound`](../ramsey_r55_order3_eleven_signature_bound).
Only its abstract lemma is used; its r=3 full formula is not used.
The two anchor representatives are the corresponding entries of
[`ramsey_r55_order3_eleven_minority_core`](../ramsey_r55_order3_eleven_minority_core).
The new sumset proof and literal census establish the selected local
cover directly, independently of the old full-extension exclusions.

The current 34-core list and existence of at least one applicable anchor
come from
[`ramsey_r55_order3_eleven_four_empty_split`](../ramsey_r55_order3_eleven_four_empty_split)
and its predecessors. Those recent empty-signature dependencies await
independent review. The preceding 34-core sweep has now been
[independently accepted](../ramsey_r55_order3_eleven_residual_sweep_review1).
That review change is recorded without reopening its completed search.

The new normalization/equality bridge and refutations await independent
review. Further trust is the imported R(4,5)=25 degree bound, unformalized
mathematics, exact Python/C++ semantics, compiler/runtime/hardware, hashes
and external full DRAT checking. Internal audits are not independent
peer review. Large formulas, proofs and logs are deliberately omitted
from Git. Their hashes identify checked local evidence but are not
standalone refutations; public source regenerates them.

This pass ends at the two-case theorem and verification. The next useful
step is to impose the intrinsic inequalities on all applicable triples
in each remaining full r=4 core formula, with its existing row order
respected. No such further sweep or signature stratum has been started.
