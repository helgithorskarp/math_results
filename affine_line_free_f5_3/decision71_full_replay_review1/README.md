# Independent full replay of the 71-point decision

This directory reviews the exact-value claim

\[
r_5(\mathbb F_5^3)=70
\]

in Discovery Net contribution
`bafkreic22u2qpq62lbr7vkt743ec37j4gygbnnufblyklm63o7rntyttja`, at
exact reviewed source commit `0df9ef5a2a1146f48283531290fac6c8c2a1459f`.

The decisive new review obligation is not another sample of the finite
domain.  It is a fresh proof and checker run for every one of the 109,676
direct CNFs.  This review also rechecks every trace with an ASan/UBSan build
after finding undefined behavior in DRAT-trim's optional warning printer.
The generated CNFs, binary DRAT traces, and logs need about 20 GB and are
intentionally kept outside Git.  This directory keeps only source, a compact
audit, and hashes.

## Independent evidence

[`independent_corpus_audit.py`](independent_corpus_audit.py) imports no
module from the reviewed directory.  It:

- reconstructs all 775 affine lines from unordered point pairs;
- independently writes every direct fiber-cardinality CNF and its affine
  hole gauge;
- checks all 109,676 case records, CNF bytes, proof bytes, and fresh
  stock-checker logs;
- checks all 109,676 disjoint ASan/UBSan recheck records and logs, including
  their exact input/proof hashes and absence of sanitizer diagnostics;
- checks that disjoint replay ranges cover the complete domain;
- recomputes ordered input and proof digest blocks and compares every input
  block with the published manifest; and
- directly checks that the cited 70-point set contains no affine line.

DRAT inference validity is supplied by separate processes rooted in the
pinned DRAT-trim source.  Every trace is checked once by the unmodified
ordinary build and again by an instrumented build with a frozen two-call
diagnostic patch.  The audit does not infer UNSAT from a solver verdict, log,
or digest alone.

[`sanitized_drat_recheck.py`](sanitized_drat_recheck.py) is a resumable,
disjoint second checker pass.  It rejects a binary without both ASan and
UBSan runtime symbols, sets both runtimes to halt on the first diagnostic,
and atomically records the exact CNF, proof, binary, and output hashes.
[`make_warning_safe_checker.py`](make_warning_safe_checker.py) accepts only
the pinned upstream source and makes exactly two raw-buffer printer changes.
[`CHECKER_PATCH_VALIDATION.json`](CHECKER_PATCH_VALIDATION.json) records the
unpatched failure, three patched positive controls, source/binary identities,
rejection controls, and the completed exhaustive second pass.
[`RESULT.json`](RESULT.json) is the compact result record for the complete
ordinary replay, complete instrumented replay, and independent corpus audit.

## Upstream diagnostic issue and safe mode

For a proof containing a deletion that is not present, stock DRAT-trim emits
an optional warning.  Its `printClause(buffer)` call reads `buffer[ID]`, even
though `buffer` is the raw parse buffer rather than an internal clause with
negative metadata slots.  ASan therefore reports a heap-buffer-overflow in
the warning formatter.  This read does not update proof state, and the code
immediately ignores the unmatched deletion.

Official option `-w` avoids the faulty call, but it is deliberately not used:
in the invalid-binary-prefix branch, the upstream `break` is inside the
warning-enabled condition, so `-w` changes more than output.  Instead, the
frozen patch adds a raw-clause printer without `clause[ID]` and redirects
exactly the two parser-buffer calls.  All warnings and control flow remain
enabled.  A sampled sanitizer run is still not enough for the review verdict.

A separate published control found that `addDependency` left-shifts a
negative signed integer on some rejected wrong-input paths.  The patch used
here deliberately does not repair that defect.  Instead, the complete
ASan/UBSan pass tests all 109,676 accepted production traces with only the
warning-printer patch and reaches no sanitizer diagnostic.  This establishes
that the signed-shift defect is not reached on this accepted production
corpus; it does not make stock DRAT-trim safe on arbitrary invalid inputs.

## Complete reproduction

Use Python 3.12, GCC 12, and the pinned dependency:

```sh
python3.12 -m venv /tmp/decision71-review-venv
/tmp/decision71-review-venv/bin/pip install -r \
  affine_line_free_f5_3/decision71_full_replay_review1/requirements.txt

git clone https://github.com/marijnheule/drat-trim.git /tmp/drat-trim
git -C /tmp/drat-trim checkout --detach \
  2e3b2dc0ecf938addbd779d42877b6ed69d9a985
sha256sum /tmp/drat-trim/drat-trim.c
gcc -std=gnu99 -O2 /tmp/drat-trim/drat-trim.c \
  -o /tmp/drat-trim/drat-trim
python3 \
  affine_line_free_f5_3/decision71_full_replay_review1/make_warning_safe_checker.py \
  --source /tmp/drat-trim/drat-trim.c \
  --out /tmp/drat-trim/drat-trim-warning-safe.c
gcc -std=gnu99 -O1 -g -fsanitize=address,undefined \
  -fno-omit-frame-pointer /tmp/drat-trim/drat-trim-warning-safe.c \
  -o /tmp/drat-trim/drat-trim-warning-safe-asan
nm -D /tmp/drat-trim/drat-trim-warning-safe-asan | \
  grep -E '__asan_init|__ubsan_handle_'
```

The checker source hash must be
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.
The generated warning-safe source hash must be
`12173598973df1d7d374cfedea977451c10d5a7aea7c90dc77f41c8cf2fad1b0`.
From the repository root, regenerate the complete domain:

```sh
/tmp/decision71-review-venv/bin/python \
  affine_line_free_f5_3/decision71/verify.py \
  --out /tmp/decision71-reduction
```

Run sixteen disjoint ranges into one generated directory:

```sh
for worker in $(seq 0 15); do
  start=$((109676 * worker / 16))
  stop=$((109676 * (worker + 1) / 16))
  /tmp/decision71-review-venv/bin/python \
    affine_line_free_f5_3/decision71/replay.py \
    --domain /tmp/decision71-reduction/orbits.json \
    --out /tmp/decision71-proofs \
    --drat-trim /tmp/drat-trim/drat-trim \
    --start "$start" --stop "$stop" \
    > "/tmp/decision71-worker-$worker.log" 2>&1 &
done
wait
```

Recheck all saved CNF/proof pairs using the independently resumable sanitizer
driver.  The sixteen ranges are identical to the generation partition:

```sh
for worker in $(seq 0 15); do
  start=$((109676 * worker / 16))
  stop=$((109676 * (worker + 1) / 16))
  python3 \
    affine_line_free_f5_3/decision71_full_replay_review1/sanitized_drat_recheck.py \
    --domain /tmp/decision71-reduction/orbits.json \
    --proofs /tmp/decision71-proofs \
    --out /tmp/decision71-sanitized-recheck \
    --upstream-checker-source /tmp/drat-trim/drat-trim.c \
    --checker-source /tmp/drat-trim/drat-trim-warning-safe.c \
    --checker-binary /tmp/drat-trim/drat-trim-warning-safe-asan \
    --start "$start" --stop "$stop" \
    > "/tmp/decision71-sanitized-$worker.log" 2>&1 &
done
wait
```

Then run both the author audit and the independent audit:

```sh
/tmp/decision71-review-venv/bin/python \
  affine_line_free_f5_3/decision71/audit.py \
  --domain /tmp/decision71-reduction/orbits.json \
  --proofs /tmp/decision71-proofs \
  --out /tmp/decision71-author-audit.json \
  --compare-inputs affine_line_free_f5_3/decision71/CERTIFICATES.json

python3 affine_line_free_f5_3/decision71_full_replay_review1/independent_corpus_audit.py \
  --domain /tmp/decision71-reduction/orbits.json \
  --proofs /tmp/decision71-proofs \
  --manifest affine_line_free_f5_3/decision71/CERTIFICATES.json \
  --known70 affine_line_free_f5_3/known70.json \
  --checker-source /tmp/drat-trim/drat-trim.c \
  --checker-binary /tmp/drat-trim/drat-trim \
  --sanitized-recheck /tmp/decision71-sanitized-recheck \
  --sanitized-checker-source /tmp/drat-trim/drat-trim-warning-safe.c \
  --sanitized-checker-binary /tmp/drat-trim/drat-trim-warning-safe-asan \
  --out /tmp/decision71-independent-audit.json
```

The independent status must be
`INDEPENDENT_COMPLETE_DIAGNOSTIC_SAFE_REPLAY_AUDITED`, with
`verified_records` equal to 109,676, `complete_family` true, and
`published_input_blocks_matched` true.  Fresh proof bytes need not match a
historical run; each must instead pass the selected checker against its
regenerated input.  The sanitized range summaries must separately form an
exact partition of all 109,676 indices.

The completed run produced 19,782,095,082 fresh proof bytes.  All 112 input
digest blocks match the published manifest; 85 of 112 full proof blocks also
match byte for byte, while 27 contain different but freshly accepted proofs.
The independent audit output has SHA256
`89db2dfa729b3ba8c022fcd1df266727486a55ae2456fb1f161efdfef02eb45e`.
Its source has SHA256
`6086fc9faf7663eecbbe8a849c97ef5ac44287d39db73f02f7d9d2c27df9845c`.
