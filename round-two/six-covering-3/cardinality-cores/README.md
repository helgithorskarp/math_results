# Exact cardinality cores at the owned period 10080 root

Actual author **six-covering-3**, role **researcher**.

The full q=3 cheap-erasure cut family from committed lemma 9241 is equivalent
to fifteen local support predicates, with empty fibers included. This gives
a complete finite necessary-core encoding on the shared36 original base
phases at 8:0,9:0,10:1,14:1,12:10. See [proof.md](proof.md) for the statement,
table, resource-domination argument and encoding equivalence.

The compact [certificate](certificate.json) maps all 638 nontrivial cardinality
predicates to the fifteen rows. [check.py](check.py) imports no producer,
model or encoder code. [stage.py](stage.py) evaluates all fifteen predicates
at one supplied list of36 original [modulus,phase] pairs.

Python standard library only, CPython 3.11.2 tested, compatible Python >=3.10.
From this source directory:

```sh
python3 -B verify.py --scratch /tmp/cardinality-cores-replay
python3 -B encode.py --out /tmp/necessary-core.cnf
python3 -B encode.py --only-B13 --out /tmp/B13-core.cnf
```

Expected: `ALL SOURCE CHECKS PASSED`; every frozen exact evidence entry and
certificate byte matches in normal/O. The full CNF has 46333 variables and
103984 clauses; its body SHA256 is
`4cbef87311f79b71d1aad3282026b7c79288ddf21cff237aa6ecc025a99f7f33`.
Generated formulas, model maps and logs belong in scratch and are omitted
from the published source. They are regenerated without external input.
Children run sequentially under 20-second guards with all numerical threads 1.
An operational limit is not an exclusion.

The frozen [core-control.json](core-control.json) is a fully specified original
base assignment satisfying the B={1,3} subproblem. Literal original10080
enumeration and every subproblem Boolean clause pass. Seven of the fifteen
necessary predicates reject the same assignment. The base proposal came
from a bounded solver that timed out with an incumbent; its numerical
status and optimality are not proof inputs. SciPy/HiGHS are not needed
for any published replay.

The ordinary proof is unformalized; tests are same-author checks with separate
literal and resource-order algorithms, not independent peer review. This
directory proves no complete covering, root exclusion or numerical L_min(8)
improvement. Predicate witnesses are local ability tests and do not license
reuse of a tail resource across actual fibers. No logical irredundancy of
the fifteen conditions is claimed. The prescribed16 unequal-pool case has
different budgets and is outside this adapter's scope.
