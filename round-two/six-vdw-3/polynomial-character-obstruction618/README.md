# Degree<=3 character repair at period 618

**six-vdw-3, researcher.** Every nonzero polynomial of degree at most
three over F103, combined by XOR with any binary six-phase row, requires
at least **eight edited nonroot columns** to avoid monochromatic cyclic
seven-term APs. All polynomial roots may be colored freely. The bound
also holds on every integer interval of length at least2472 with
arbitrary nonperiodic colors inside edited/root columns.

The complete affine normalization covers317 templates; all three
nonzero cube classes are included. Eight disjoint root-avoiding actual
APs per template certify the bound. The proof also derives necessary
distance and correlation cuts for arbitrary0..3-hole XOR618 orientations.
This is a restricted construction-family obstruction, not a3704 coloring,
an optimum repair theorem or a numerical W(2,7) improvement.

Use CPython3.11 or later; only the standard library is required. Run from
this directory, with an empty work directory outside it:

```sh
python3 reproduce.py --work /tmp/polynomial618-check
```

The serial wrapper checks every source pin before executing helpers,
then regenerates and independently checks the complete certificate in
normal and Python-O modes. Each child has a fixed20-second timeout and
numerical thread variables set to one. Failure or timeout leaves
incomplete evidence and proves no exclusion. Expected success status:
`FRESH_COMPLETE_POLYNOMIAL618_SOURCE_RECONSTRUCTION`.

Manual stages, if desired:

```sh
python3 generate.py --out /tmp/polynomial618.csv
python3 check.py --certificate /tmp/polynomial618.csv --out /tmp/polynomial618.json
```

The CSV has317 rows plus a header. Coefficients are in ascending order;
each of eight pairs(a,d) means(a+j*d) modulo618, j=0..6, start0..617,
step1..309. Nonunit steps and regular field zero are retained. Every
canonical row is covered; the list is not an exact affine orbit count.

Read [PROOF.md](PROOF.md) for universal normalization, phase/CRT/lift and
masking bridges, and [VALIDATION.md](VALIDATION.md) for finite checks and
trust boundaries. [certificate.csv](certificate.csv) and
[expected.json](expected.json) are compact evidence. The generator is
not trusted by the independent literal checker; greedy optimality is
neither required nor asserted. Public source contains no solver models,
native proofs, search checkpoints, keys, private ledgers or large corpora.
