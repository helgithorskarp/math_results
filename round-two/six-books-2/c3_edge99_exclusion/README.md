# Ordinary C3/99-edge exclusion by deficits and parity

Actual agent **six-books-2**, role **researcher**, 2026-10-02.

PROOF.md excludes every ordinary valid22 graph with99 red edges and
an automorphism of cycle type3^7 1. New ordinary arguments handle the
three-pair and exceptional degree-seven profiles; three explicitly cited
published cohort exclusions handle the other profiles. Crediting8971,
this leaves exactly102 edges for this cycle type. The Ramsey endpoint
and this remaining branch are open. New independent review is pending.

Python3.11+ standard library only, one CPU, no C++/solver dependency:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 round-two/six-books-2/c3_edge99_exclusion/reproduce.py --work scratch/c3-edge99-cold
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -O round-two/six-books-2/c3_edge99_exclusion/reproduce.py --work scratch/c3-edge99-optimized
```

Expect **REPRODUCTION_PASS**, entire deterministic mathematical record
**7665 bytes**, SHA256
**d6db64da2d4c618a200d3b0142b5f40d1378b1f65292af561038bfb1c93aa6d4**.
The source checks all1128 ordered degree-sum matches against a distinct
full16384-word domain scan, all174 relevant local words against literal
capacities, the58 parity words,14784 literal22-spine controls,1890 odd
column row checks and nine corruption rejections. Normal/O receipts and
whole records are regenerated in the selected scratch directory.

These checks validate ordinary proof identities and finite scalar domains.
The proof does not need a local-class or whole-host completion census.
DEPENDENCIES.json explicitly identifies published theorem premises and
which conclusions are consumed. The reproduction does not replay those
earlier entire computations, import their executables, or transfer an
independent review verdict. Counts are labeled scalar/identity controls,
not counts of valid hosts or isomorphism classes.

reproduce.py enforces serial one-thread child execution, a25-second
mathematical guard and30-second child deadline. Failure or interruption
is incomplete validation, never nonexistence. Generated domains and
receipts stay in scratch; no private ledger, key or large corpus is a
public input. The fixed primary21.rows fixture is the known literature
construction, not a new witness. evidence.json records exact cold checks
and sealing; the original graph claim records the verified source commit.
