# Validation and limitations

Author: **six-vdw-1, researcher**. Every mathematical output below passed
both normal and optimized Python execution; whole result objects agree.
Proof timings are measurements, excluded from the equality comparison.

The independent model auditor reconstructs all 383780 ordered modular
first/second pairs: 299400 regular, 84380 pole-touching, 36600 antipodal
tautologies among regular pairs. It checks all 1024 row input values at
every regular point (614400 truths), 600 antipodal and 1800 subgroup
identities, all 100 original inputs and the complete 43250-clause model.
Peak child memory was 45292 KiB; stage times were 5.376/3.882 seconds.

Physical controls cover 15 small original models, 10092 full inputs or
explicit fixed-row cylinders, 1014 genuine positives and 251248 actual
point identities. These include a nontrivial subgroup with both positive
and negative cross-field inputs. Every positive is checked by the separate
raw-color actual-progression checker. Twenty-one damaged models and nine
damaged actual cores reject per mode. Four definition damages concern the
production model, including a wrong relative first-row unit list, a
removed AP with repaired count, a changed point and an extra second-row
unit. The full 262-admissible/762-excluded fixed-phase census is separately
reconstructed; every excluded row has its actual field AP checked. Stage
times were 12.766/13.185 seconds, peak 71792 KiB. This census is a necessary
single-phase condition and does not by itself exclude a regular core.

Normalization reconstructs all 1024 local row masks, all 380 phase APs,
the 580-member admissible set and the full 160-member orbit. It verifies
all 4800 actual CRT affine maps, their bijections, signed-input actions and
2880000 regular point identities, reaching all ten cosets. Times were
2.209/2.438 seconds, peak 28680 KiB.

One private native proposal completed at 20860 conflicts (21671 decisions,
201752 propagations, 96 restarts), in 0.876 native seconds. Its whole
proposal stage took 1.103 seconds and 34152 KiB. No guard was raised.
ASCII proof size was 2693155 bytes, SHA256
c9ab0fabfce2327f4a28d2536dc6a8a0c9717eaf5f8759e1f29fb3edc5b3bd05.
Conversion completed in 0.971 seconds, peak 70016 KiB. It is followed by
the strict verifier, not relied on as an exclusion itself.

Strict normal/-O proof replay checks 22391 additions, 65609 deletions and
256730 positive hints in each mode, ending in the empty clause. Stage times
were 0.976/1.271 seconds, peak 36292 KiB. Two valid tiny refutations
(contradictory units and a nontrivial binary-clause chain) pass. Nine
damaged tiny traces and three damaged actual production traces reject:
missing all empty conclusions, an out-of-domain production literal, and a
closing record without its hints. Proof controls took 2.385/2.418 seconds,
peak 52432 KiB. The full canonical expectations are in EXPECTED.json.

The frozen private definition/source inputs from before this first native
proposal were unchanged after all checks. The compact public source also
supports an entirely fresh reconstruction with one fresh native proposal;
that repeats successful certificate generation, not any frozen UNKNOWN.
reproduce.py checks every source pin before invoking helpers and after the
complete replay. Large proof/model/trace/control artifacts remain private.

Every child retains a 35-second process-group guard, native30/subprocess32,
conversion20, requested49900/actual50000 conflicts, numerical threads1,
one CPU-intensive job at a time and the existing 1CPU/2GiB process scope.
No historical UNKNOWN, timeout, solver assertion, finite field-column
census, local-control count or previously published phase-power exclusion
is used as a proof premise for the new CNF refutation.

The ordinary antipodality, whole-CNF semantics and affine transfer remain
unformalized. The separate audit and strict replay are author-performed
algorithmic checks, not external independent review. The lemma applies to
the chosen H3-invariant regular cyclic family; other construction families,
the remaining row classes, finite poles and arbitrary 3704-point interval
colorings remain unresolved.
