# Native thirteen-input H21 binary-first barrier

**six-sorting-2, researcher**, 2026-10-02. Restricted author proof with
exact computation and separate same-author algorithms; external review and
formalization are not supplied.

[PROOF.md](PROOF.md) proves that a standard sorter extending literal H21
with at most44 comparators must have a singleton first strict ordinary
pruning-mass increase on at least one side. It excludes the complete native
both-first-binary cover, with arbitrary preparation length and depth.
Unrestricted44..45 and the native244-state eleven-input/23-gate completion
problem remain open.

Use Python3.11.2, standard library only, one process/native thread:

```bash
cd round-two/six-sorting-2/native-binary-barrier
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 generate.py
python3 verify.py
python3 -O generate.py
python3 -O verify.py
```

The generator writes the compact certificate deterministically. The checker
imports no generator, profiler, sibling source, solver or graph package. It
reconstructs full original conditional cubes with numeric distinct ranks,
bottom-up binary forests, complete pruned carrier functions and heap
aggregation. Its validation conditions use explicit exceptions and remain
active with `-O`. Incomplete coverage or insufficient mass raises an error.

Expected:405 length31 fronts,403 distinct nine-core images of size75..102,
13-gate remainder;5020 selected original3+3 domains,372 nested occurrences
and278 distinct selected inner words. All405 selected masses exceed2^44;
the minimum is17660905521152, ratio257/256. The checker also verifies the
3150-state necessary profile projection and the135-function prior B23
subcover, validates positive7/11/13 sorters, and rejects14 damaged controls.
Exact finite counters are in [checks.json](checks.json).

Certificate276957 bytes, SHA256
`a4026fbc3263c470d8ad40defd5181e76c24621a4ac60e7fd08c7f3094a608cb`.
Original/inner truth tables and exploratory complete-domain arrays are not
stored; both algorithms reconstruct all data needed for the theorem.
The97 original proposal domains are selectors, not an exhaustive premise.

Universal pruning/commutation/threshold bridges and imported optimal sizes
are the stated trust boundary. [SOURCE-CREDITS.md](SOURCE-CREDITS.md) records
copied code and earlier mathematical scopes; prior negative conclusions or
review verdicts are not used as native certificates.
