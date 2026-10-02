# Two-layer allocation with an original sixteen already prescribed

**Proved combinatorial refinement:** after all core phases are selected at
either open period-10080 child with original16 phase2 or4, every nonempty
parent subset I satisfies

    8|I| - 3|union of Div(g_i)| <= 32 + 4*1[marked parent in I].

Here g_i is the gcd of315 and the hole differences in that parent. Six
unmarked nonempty parents therefore need at least six collective eraser
labels, compared with four when16 is free. This accounts for the consumed
original resource, and does not exclude the prefix or change L_min(8).

Author: **six-covering-2, researcher**. [Proof and attribution](proof.md).
The underlying equal-resource argument is six-covering-3's published
[two-layer theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/eraser-matching/proof.md).

From the repository root, Python>=3.10, standard library only:

```sh
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B round-two/six-covering-2/prescribed-sixteen-allocation/controls.py --expected round-two/six-covering-2/prescribed-sixteen-allocation/expected.json
```

The full frozen result includes 1,400 complete small models, 8,477 vertex
covers and 130 feasible equality cases. A 48-point fixture has a literal
24-tail-class covering with16 free and a strict deficit with16:2 fixed.
The fixture is a subset of the fixed root's holes; realization by the
remaining core phases is unproved. Repeat the command with python3 -O -B;
explicit guards remain active and the entire result must match.

The all-size theorem follows from the written counting proof. These are
author controls, with separate feasibility and eraser-graph algorithms,
and are not an independent reviewer verdict or a formalization. No solver,
external generated certificate or large proof corpus is required. Tests
take under one second, one process at a time in the existing1CPU/2GiB scope.
Both original16 children and the global exactly-eight problem remain open.
