# Independent review: Hadwiger numbers of co-degree-two graphs

This directory records an independent review of the theorem in
[`../hadwiger_max_degree_two_complements`](../hadwiger_max_degree_two_complements).
For every nonempty finite simple graph `H` of maximum degree at most two, the
theorem determines the Hadwiger number of `complement(H)` exactly, with eight
explicit isolate-extended exceptional families, and deduces Hadwiger's
conjecture for the whole class.

The verdict is **accept with high confidence in the stated scope**.  The
proof reconstruction, human premises, completeness reductions, adversarial
examples, literature boundary, and limitations are in
[`REVIEW.md`](REVIEW.md).

[`independent_check.py`](independent_check.py) deliberately avoids the
producer's canonical forbidden-graph certificates.  It generates component
multisets from integer partitions and computes each Hadwiger number directly
from the branch-set definition.  A distinguished unused block makes every
candidate `K_t` model a restricted-growth partition of `n+1` objects.  It
also computes independence and chromatic numbers from definitions and audits
the auxiliary matching boundary by a separate bit-mask dynamic program.

Reproduce with standard-library Python 3.11 or later:

```sh
./run_checks.sh
```

Expected runtime is about five seconds in the review environment.  The
checker is finite evidence through order 12; the universal theorem still
rests on the written forbidden-graph reduction and Dirac argument.
