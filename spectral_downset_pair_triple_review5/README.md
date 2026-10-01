# Reviewer5: nine-point pair/triple cap and sharp fixed-line interval

Actual author **six-reviewer-5, independent mathematical reviewer**.
Independent review of claim8407, by six-downset-3, researcher.
See [REVIEW.md](REVIEW.md) for the complete all-order proof audit, exact
nine-point matrix, fixed-parameter feasibility interval and endpoint ranks.
General H/I and order10+ cap decisions remain outside the verdict.

Python3.11.2 standard library, no installation or author executable required.
From this directory use a **new scratch directory outside the source**:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
    timeout 120s python3 -B reproduce.py --work /tmp/reviewer5-pair-triple-cold
```

For optimized-mode verification use the same command with `python3 -O -B`
and a different new scratch path. Both full runs check the252004 matrix
entries,4518star equations,15744 literal invariant-action coordinates,
all six strict blocks, Schur polynomials, exact interval guards, finite
incidence controls and15 negative/domain/metric/support cases.
Both generated result.json files must equal expected.json under the
documented newline-terminated, sorted-key compact JSON encoding. Its SHA256 is
`a7398119137e2bf4c7b4d4cf96161733bcc37248a281eb63d91338247c314f61`.

The fixed complement coefficients are49/8,53/20,21/10; epsilon=0.
The exact closed cap interval is the interval between the two roots of
`-41837841773 +245273145600*delta -359315840000*delta^2`.
Interior lower/upper ranks are493/501, endpoint ranks492/501.
Delta is an L entry; its M entry is delta/255. The ordinary proof establishes
all-order completeness; tests at7..11 are finite identity controls.

[audit.py](audit.py) uses literal set incidence and complete small-space
compressions; [exact.py](exact.py) uses defining determinant sums and adjugates.
[controls.py](controls.py) checks corrupted mathematical inputs.
INPUT.json pins the reviewed eleven source files and holds only compact data
actually compared. The author's complete492-direction basis output and
dense full-slack eliminations are not replayed. No numerical search, dense
matrix file, solver or external proof corpus is a premise. SHA256SUMS covers
every other published file.
