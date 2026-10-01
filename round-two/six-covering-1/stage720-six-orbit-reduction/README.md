# Period-720 construction stage: twelve necessary target shapes

Author: **six-covering-1, researcher**. Date:2026-10-01.

The24 original divisor labels m|720,m>=8, normalized at8:5/9:6, can leave
holes inside(a mod18) union(c mod6) only at twelve of the108 target pairs.
Those twelve form six affine orbits. They are necessary candidates;
no covering existence or global numerical improvement is claimed.

Read [proof.md](proof.md) for the complete hypothesis, induction and scope.
[certificate.json](certificate.json) specifies every excluded target,
two resource partitions and the strict count envelopes199<200,156<160.
[expected.json](expected.json) freezes the complete deterministic replay.

Python3.11+ standard library only. Run serially from this directory:

```sh
python3 -B check.py --expected expected.json
python3 -B -O check.py --expected expected.json
python3 -B audit.py
python3 -B -O audit.py
python3 -B -O controls.py
sha256sum -c SHA256SUMS
```

The production replay uses integer bitsets. The separate same-author
audit imports no production code: it constructs literal physical point
sets and evaluates its own set-union/count recurrence. This is algorithm
independence within one author's work, not independent peer review.
All certificate guards use explicit exceptions and remain active under-O.
Damage controls reject wrong fixed classes, missing labels, an invalid
anchor order, a false strict upper bound, negative weights, repeated
resources, a missing target and an invalid affine transfer.

The original phase enumeration and written induction are the proof
mechanism. No solver status, objective, phase-assignment exhaustion or
whole-integer nonexistence conclusion is used. In particular this does
not determine L_min(8), which still has candidates10080/15120/20160.
No resource increase is needed: oneCPU, threads1, well below2GiB.

Author validation: production normal/-O 2.093/1.757s; separate audit 3.230/3.350s. Both pairs agree in complete deterministic output. The audit checks1686 physical anchor phase pairs and408368 original phase combinations for the scalar certificates. All eight damage controls reject under-O (6.488s). Peak child RSS across these checks88044KiB. The frozen expected file existed before both comparison replays; its initial generation was recorded separately.
