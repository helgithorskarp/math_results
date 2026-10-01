# Equilateral hat with imbalanced quartic boundary bows

Author: **six-heesch-3**, role **researcher**, 2026-10-01.

Replace each unit port of Tile(1,1) by its inward-normal graph
`a_i*t^2*(1-t)^2`, with all fourteen amplitudes nonzero and sufficiently
small. If any magnitude occurs unequal numbers of times with positive
and negative signs, both Kaplan's hole-free Hc and outermost-holes-
permitted Hh are at most one, under arbitrary Euclidean motions and
reflections. Sixteen specified equal-amplitude sign words attain one.
The smallness threshold is proved to exist, but no numerical amplitude
bound is certified. Flat ports are outside the result.

This closes a candidate family for the finite-Heesch-seven search.
It is an intermediate obstruction, not a new record. Balanced alternating
words give the published Spectre construction, which tiles the plane.

Read [proof.md](proof.md) for the full geometric bridge and scope.
The key steps are polynomial open-arc rigidity, fully covered vertex
locking, a finite uniform overlap-persistence argument, exhaustive
first-prefix enumeration, and independently read single-sector cuts.
Contacts between unfilled final-corona tiles are not assumed to match.
The reduction to auxiliary binary words covers arbitrary nonzero
amplitude classes, not just equal-amplitude profile signs.

Reproduce with CPython 3.11 and the standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B round-two/six-heesch-3/equilateral_hat_bows/check.py --expected
```

The reader checks 3,412 raw vertex-alignment poses, 664 reference
neighbours, 6,476 positive-imbalance words, and two exhaustive independent
enumerations of all 25 necessary first surrounds. All 26 surround/word
pairs have a checked local cut. A balanced eight-copy disk surround
calibrates the model. Seven altered certificates reject. No timeout,
partial-hole prune, solver or external atlas occurs in the reader.
Normal and optimized Python outputs agree. The optimized expected replay
was measured at 57.1 seconds and 44,260 KiB peak RSS on one CPU with
CPython 3.11.2. No native numerical-library threads are used.

Files:

* `geometry.py`: exact Q(sqrt(3)) geometry and primitive-port labels.
* `check.py`: independent pose arithmetic, two cover searches, cut reader,
  disk-boundary reader and malformed controls.
* `certificate.json`: all 25 small first prefixes and their 26 local cuts.
* `expected.json`: deterministic counts and certificate SHA256.
* `proof.md`: analytic all-motion and topological arguments.

Certificate SHA256:
`0d6391245ecefd86c77e56e88da7d5a397460c452e4494b3541c99c6992a8e5d`.

The primary polygon, balanced curved construction and their tilability
are Smith--Myers--Kaplan--Goodman-Strauss prior art:
[A chiral aperiodic monotile, Section 2 and Lemma 2.1](https://arxiv.org/html/2305.17743v2).
Quartic primitive-arc locking and network transfer are also
[published campaign results](https://github.com/helgithorskarp/math_results/blob/main/heesch_weighted_matching_obstruction/quartic_realization.md).
The new conclusion is the imbalanced equilateral-hat exclusion and its
finite-pose protected-interface bridge.
No current finite-seven construction has been found here.
