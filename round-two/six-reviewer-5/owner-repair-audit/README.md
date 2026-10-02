# Independent saturated-base repair audit

Actual reviewer: **six-reviewer-5**, independent mathematical reviewer.

The [review and full ordinary bridges](REVIEW.md) confirm LEMMA9446:
any packing retaining at least 63 words of a point relabeling of a saturated
fixed-point C5 68-word base has at most 68 words. The antecedent base census
is imported and credited. No symmetry is required of the repaired packing.
The classical base additionally permits retention 62. A short ordinary
proof gives the same six-omission bound for any Steiner S(3,5,v) after
adding one point. No unrestricted A(18,6,5) endpoint is improved.

The independent checker uses unique owned physical triples and full-domain
filtering, imports no author code, and checks all 3,833 critical five-deletion
domains. The [input manifest](INPUTS.json) records four original positive
JSON inputs at source `770d5148b39ab8f3ad90e87ad19cfcdb47456cb1`; no large
inputs, generated corpora or private files are required.

From this directory, using Python 3.12.14 and its standard library, choose
new input and output directories. Fetch the fixed small inputs once:

```sh
python3 -B fetch_inputs.py --output inputs
```

Run serially with native threads one and a fixed 60-second outer guard:

```sh
timeout 60s env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -B verify.py --inputs inputs --work work/normal --check-expected
timeout 60s env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -B -O verify.py --inputs inputs --work work/optimized --check-expected
```

`timeout` is a Unix command; an equivalent fixed parent-process timeout may
be used elsewhere. A guard interruption is incomplete verification and
establishes no mathematical result. No timeout was hit in the recorded runs.
The four inputs may instead be read from the corresponding pinned author
checkout, using its directory as `--inputs`.

Both modes produce the same complete `EXACT_RESULT.json`, SHA-256
`dfeb7885560e51145330d93ef7d9cb4a79ee3dc5df368995de3466a39d71e505`.
Expected summary: 3833 critical domains, 674053 local physical pair checks,
seven semantic damages rejected, and classical radius six verified.
The seven damage controls bypass input/expected hash checks and reject for
mathematical reasons. The final driver also reproduces both historical seals.
See [validation](VALIDATION.json) and late [author corroboration](CORROBORATION.json).

`first-record.json` and the seal metadata describe the original independent
phases: they do not assert that fixtures remain unread during subsequent
replays. The historical core modules remain unchanged. The later point-bit
bridge and classical refinement are explicitly post-seal additions.
Trust includes the prior classification, the ordinary written reductions,
exact Python semantics and execution. No proof-assistant formalization is
claimed, and the seven-deletion failure witness is a boundary for one color
field rather than proof of a 69-word repair.
