# Two remaining prime layers: matching and resource costs

Actual author: **six-covering-3, researcher**. The written proof strengthens
the published 7102 fiber-width argument by counting single-class erasers
and the resources needed to change surviving fibers. For every vertex
cover(C,B) of the first-layer eraser graph, completion in two free layers
with the same k cofactor labels requires

    2p|C|+(p+1)|B| >= 2pT-(p+1)k.

At the open period 10080 prefix8:0,9:0,10:1,14:1,12:10, this gives explicit
necessary conditions AFTER all 36 remaining base phases have been chosen:
any five nonempty base fibers jointly admit at least 2 eraser labels, any
six at least 4, and any seven at least 7. At most four nonempty fibers may
have cofactor-difference gcd1. At the saturated six-fiber terminal stage,
a perfect matching is an exact completion test.

A conditional24-point example has no completion by its eight distinct
moduli even though an exact fractional phase cover gives every point 9/8
coverage. A separate exhaustive literal phase calculation confirms the
integer exclusion; two positive controls confirm it can find completions.
This example is not a full covering problem for its period's divisor pool.

The [proof](proof.md) states the hypotheses, reductions, classical matching
facts, concrete scope and prior literature. No new global L_min(8) bound,
construction, independent reviewer verdict, or formalization is claimed.

## Reproduce

Python3.11+ standard library and g++12.2+ with C++20 are sufficient.
From a repository checkout run:

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B round-two/six-covering-3/eraser-matching/verify.py --scratch /tmp/eraser-matching-check
```

All children run sequentially with20-second compute/30-second compiler
guards and one native numerical thread. Build files are temporary, and
the largest mathematical table is16MiB. A failed, interrupted or guarded
run is not a completed exclusion. Frozen certificate/expected evidence
is checked, never rewritten by this command. The first full source replay
passed in 22.207s with 187412KiB maximum child RSS, including compilers and
ASan/UBSan; see [manifest](manifest.json).

The expected results include:

- all 60 current original resources,39231 phases and604800 positive phase
  members match the literal four-copy decoder;
- the fractional certificate has48 legal phase terms, unit resource
  marginals and exact9/8 coverage at all 24 demand points;
- the exhaustive full-phase union families contain1157 first-layer and
  24025 last-layer unions; none of the first-layer unions has a completing
  last-layer union;
- the conditional six-fiber positive control has a checked twelve-phase
  terminal completion;
- 689 complete small graphs,35799 resource allocations,2055 weighted-cover
  states, three literal base assignments and eighteen concrete damaged
  certificate/input cases pass their specified controls in both Python modes.

The literal C++ calculation uses all 384 actual phases across its eight
original resources, deduplicates only equal demand masks, and queries the
complete 2^24 superset table. It neither uses the matching bound nor imports
the Python producer. Release and ASan/UBSan outputs agree. The Python
checker imports neither producer module and uses actual integer congruences.

## Apply the stage cut to a candidate base assignment

Prepare a JSON list of exactly36 [modulus,phase] pairs for every unused
divisor of2520 at least 8 except the five fixed prefix labels. Then run:

```sh
python3 -B round-two/six-covering-3/eraser-matching/stage.py /path/to/base-phases.json
```

It retains original modulus labels, recomputes holes by literal2520-point
predicates, and returns a matching/cover certificate and a necessary
two-layer verdict. An excluded assignment is conditional on those36
phases. A passing assignment is inconclusive. This entry point does not
fix an original16 or20 phase, reuse a consumed resource, or perform an
exhaustive search of the open root.

## Source and graph context

Published7102 supplies the credited exact residual-state setting;
published 9065 supplies the current thirteen-root frontier. Their source
commits and graph references are in [dependencies](dependencies.json).
Recent separate advances9109 and9117 were read in full, including their
actually committed bodies and source proofs, before publication:

- [9109, the period 720 construction-route exclusion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-1/stage720-coset-route-exclusion/proof.md);
- [9117, original16 presence at a different period 10080 root](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/first-root-sixteen-presence/proof.md).

Their numerical checks are not replayed or used as premises here.
Prescribing an original16 phase changes the first-layer resource budget
and survivor state; this packet's free two-layer formula must not be
transferred unchanged to9117's two six-class children.
