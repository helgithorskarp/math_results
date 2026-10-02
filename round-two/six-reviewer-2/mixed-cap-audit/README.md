# Independent mixed-facet capped H audit

Actual reviewer **six-reviewer-2**, independent mathematical reviewer,
2026-10-02. This compact evidence confirms LEMMA9408's uniform n>=3
triangle-facet/other-mark pendant cap and greatest lower rank, and proves
a larger certified seed/raw mixing interval. Read [REVIEW.md](REVIEW.md)
and the complete ordinary [PROOF.md](PROOF.md) for exact scope.
Neither the interval's optimality nor general spectral H/I is claimed.

Run from this directory with CPython3.12.14 and its standard library:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B certificate.py --expected SYMBOLIC-EXPECTED.json
python3 -B -O certificate.py --expected SYMBOLIC-EXPECTED.json
python3 -B physical.py --expected PHYSICAL-EXPECTED.json
python3 -B -O physical.py --expected PHYSICAL-EXPECTED.json
```

Run serially. Each program has a fixed60s POSIX SIGALRM guard. Every check
uses explicit exceptions and remains active under -O. This is exact
integer/Fraction arithmetic, with no CAS, solver, external dataset or
floating arithmetic. Five reviewer modules and both complete records plus
the ordinary proof were sealed before author executable/RESULTS inspection.
[PROVENANCE.json](PROVENANCE.json) records the seal, credits and the pre-seal
primitive-Gram quotient correction. [VALIDATION.json](VALIDATION.json)
records whole-output comparisons and resources.

Expected evidence:13 uniform positive leading-minor polynomials/459 positive
coefficients/463 exact identity evaluations;4 complete original families,
400 physical Gram+400 complete-frame positions,52 high+48 low eigenactions,
16 repaired whole-matrix checks and15 semantic damages across both phases.
The degree-bounded identity argument and complete-space proof establish
the unbounded theorem; finite controls alone do not.

Independent symbolic normal/O1.788/1.906s, physical6.593/7.097s; observed
peak26152KiB, serial native1 and unchanged1CPU2GiB scope. Complete stdout
SHA256 values are the SHA256SUMS entries for both expected JSON files.
Full record comparison, rather than a summary digest alone, is enforced.

Optional late comparison against the pinned author RESULTS.json:

```sh
python3 -B compare_original.py /path/to/original/RESULTS.json --expected COMPARISON-EXPECTED.json
python3 -B -O compare_original.py /path/to/original/RESULTS.json --expected COMPARISON-EXPECTED.json
```

Pinned original source: `f8255e1d617237421c32b3d1e13dd865bffd50c4`.
[AUTHOR-INPUTS.json](AUTHOR-INPUTS.json) contains all12 exact source-file
hashes. Obtain RESULTS from that exact commit; later branch changes are
not substituted for the original. No target executable is imported by
the adapter. It reconstructs all13 coefficient fingerprints/row factors,
all four native fixture fields and all nine scalar-control records, including
eight complete matrix-encoding SHA values/15232 entries after actual-set
order transport. The whole author matrix corpus is not an external proof
input. Late normal/O9.601/9.459s and full frozen record agreement pass.

The unchanged original verifier, run only after the independent seal,
also passes normal/O8.226/8.624s with stable whole record
`9c4803c6333dd9174d54511227a298cb84553c77d09b118319b2e3c981af4b4b`.
This is later corroboration, not independent generation of the evidence.

The earlier reviewer-owned [linear.py](linear.py) is reused unchanged from
the ordinary attachment audit, source
`07e9cde0c4181ed67c565ef24ed366a34566b739`. The other five Python modules
are new reviewer source. The defining displayed construction and prior
ordinary closure/structural lift are credited; no algorithmic priority
claim is made. No proof assistant or bulky omitted certificate is required.
