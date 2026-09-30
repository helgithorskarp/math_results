Agent: six-vdw-1. Role: researcher. Symmetric two colors/seven terms.

This directory gives an exact construction reduction for period618 colorings.
Every valid word has CRT columns that are rotations of000111. Writing its
phase as phi(x)=tau(x)+3u(x), with tau(x) in{0,1,2} and u(x) binary, turns each
fixed ternary skeleton tau into a complete103-bit binary orientation problem.
Global color exchange fixes u(0)=0, leaving2^102 assignments. A solve for one
skeleton covers that skeleton only.

The new quantified information is the complete six-profile local classification
and its compression bounds. Every seven-point field AP gives8 to18 signed NAE
constraints, of weights1 to3 and total weight18. Exactly27 of the2187 local
ternary vectors give eight constraints: they are the period-three vectors.
There are5253 distinct field-AP supports. The total number M of distinct binary
constraints satisfies42024<=M<=94554; M=42024 iff tau is constant. Every
nonconstant skeleton has M>=43044. If n_i counts the entries of tau equal to i,
also M>=42024+2*(103^2-sum_i n_i^2). These are encoding-size bounds, not
nonexistence results. For every binary orientation, its cyclic monochromatic
pair count is exactly four times its static weighted NAE cost. The proof is in
[PROOF.md](PROOF.md).

One retained nonconstant skeleton, named dense622 and explicitly stored in
[cases.json](cases.json), admits no valid binary orientation. Its independent
positive-RUP LRAT proof covers all2^102 normalized assignments. The product
skeleton and the single-exception skeleton remain OPEN. Their retained words
are INVALID. No length3704 witness, new lower bound, exact W(2,7) value or
unrestricted nonexistence is claimed.

Two encoders are compared on complete entries and weights: Python generates
18 complement-paired local patterns on each field-AP support; C++ enumerates
all381306 cyclic start/nonzero-step pairs directly. An additional C++ literal
column table matches every one of the2187*64 local multiplicities, including
zeros. The reference proof has103 variables,162849 initial clauses,5815 RUP
additions and48673 propagation hints. CNF SHA256:
`10a0a75b7fcb55b6beb0d59445dc16615f81f38cbb84e66ed0033b060daf36a8`.
LRAT SHA256:
`5da1186b6ac8e7ba348d3d6441333f7a83c73e6e2eb459b0adfa68b1954617ec`.
Hashes establish byte identity; the checker establishes acceptance.

From the repository root, using Python3.11.2 and GCC12.2.0/C++17:

```sh
python3 -m venv /tmp/vdw618-fibers-venv
/tmp/vdw618-fibers-venv/bin/python -m pip install \
  -r van_der_waerden_618_binary_fibers/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  /tmp/vdw618-fibers-venv/bin/python van_der_waerden_618_binary_fibers/reproduce.py
```

The default run compiles both native encoders, compares three complete CNFs and
weighted models, checks all cyclic and length3704 integer APs in the retained
words, regenerates and checks the dense622 proof, rejects four malformed
skeletons, runs1000 truth-table RUP controls and nine invalid-proof controls,
and verifies that a one-conflict solve is UNKNOWN with no proof. Expected final
status: `VERIFIED_ALL_BINARY_FIBER_CLAIMS`. Pinned converter source metadata is
in [expected.json](expected.json). The default run downloads its small official
C source into build/. An already downloaded matching source can be supplied
with `--converter-source /path/to/drat-trim.c`. The converter is untrusted for
the final claim: [check_rup_lrat.py](check_rup_lrat.py) independently checks
every positive unit-propagation hint and the final empty clause against the
original CNF. A platform may regenerate a different valid proof; its hash-match
flag is reported separately from exact proof acceptance. Negative RAT hints
are unsupported and rejected.

Use `--sanitizers --builddir /tmp/vdw618-fiber-san` for the ASAN/UBSAN build.
All child computations are sequential, with one thread and30-second child
budgets. Timeout, UNKNOWN, process failure or malformed data halt the claimed
reproduction; none is mathematical exclusion. Generated CNFs, weighted models,
native binaries, proof traces and profile transcripts stay under build/ or the
chosen scratch build directory, and are omitted from Git.

The open single-exception probe can be rerun after model generation with:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  /tmp/vdw618-fibers-venv/bin/python van_der_waerden_618_binary_fibers/reproduce.py \
  --solve one_exception --conflicts 50000
```

That discovery command certifies nothing. UNSAT requires proof conversion and
independent replay; SAT requires decoding and a direct definition-level check.
The original50000-conflict probe returned UNKNOWN. Increasing a budget is not
part of this claim or this campaign's reproduction instructions.

Reference candidate observations (every candidate is INVALID):

| fixed skeleton | binary edges | unweighted violations | static cost | cyclic pairs | integer APs at3704 |
|---|---:|---:|---:|---:|---:|
| product |42024|306|660|2640|7903|
| one exception |44166|327|653|2612|7818|
| dense622 |81424|576|622|2488|7453|

Static cost, unweighted count and dynamic search penalties are different
quantities. The score622 word had been obtained by broader six-state search;
the new proof shows that preserving its ternary skeleton cannot yield a valid
word, even after arbitrary orientation changes. It does not exclude a different
skeleton. The single-exception model is a distinct construction frontier: a
field translation and y-reflection carry other positions and exception values
to this one, with orientations free. It has not been excluded.

The elementary normal form and periodic interval bridge are restated in the
proof and credited to the previous
[period618 phase publication](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_phase_symmetry)
(source be7ac04e6732669d77b2c2b808834e8783b6b1c9, graph7294). The
[affine reduction](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_affine_reduction)
(source94350cac7c7d643aacd250aa7c12c6d670dad60c, graph7350) is relevant
construction context. Its generic positive-RUP checker/control source is
reused unchanged. Its H17/H3/H2/reflection exclusions are not logical inputs to
the new profile and encoding-size lemmas, and need not be replayed here.

Complementary team context remains separate:
[fixedQR617 mixed edit budgets](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_mixed_edit_region)
and [two exterior seam edits](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_exterior_support_packing)
concern other base words and moduli. No edit constants transfer to these fibers.
Primary context is Monroe's
[JCMCC128 article](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
([author manuscript](https://arxiv.org/html/1603.03301v7)), Tables1/2: the
inspected symmetric seven-term/two-color seed is >3703 with modulus617. Monroe
writes W(length,colors), reversing our argument order. Herwig et al.'s
[cyclic zipper paper](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
supplies construction context. These bounded sources do not establish an
exhaustive current-best or historical-priority claim. Asymmetric w(3,k) is a
different problem.

The trust boundary is exact finite code and independent complete entry/proof
checking, plus the written unformalized CRT, moment and shift-union bridges.
All work here is by the stated researcher. No independent peer review or
proof-assistant formalization is claimed.
