# Multiplicity one excluded for the two unsaturated points at 71

Actual author: **six-code-1, researcher**, 2026-10-01.

For a 71-word A(18,6,5) packing with exactly two points below
replication20, those two points must occur together at least twice.
The new ordinary proof excludes multiplicity one; the absent-pair
exclusion is credited prior work. See [PROOF.md](PROOF.md) for all
hypotheses, the two cases and the injection that closes the count.

This is an unformalized author proof using explicit published local
premises, with new independent review pending. The global interval
69--71 is unchanged. Imported classifications are credited premises,
not recomputed discoveries or a new review.

From the root of a full clone, CPython3.11 standard library:

```sh
python3 -B round-two/six-code-1/multiplicity_one_exclusion/verify_inputs.py
python3 -B -O round-two/six-code-1/multiplicity_one_exclusion/verify_inputs.py
```

The wrapper checks pinned public files, all 2346 literal pairs in
[acl69.txt](acl69.txt), and replays the published universal theorem
and three shared-hub certificates. The optimized invocation also runs
the imported scripts under optimized Python. No source is mutated,
and there is no network call, solver or private input. Numerical
threads are set to one and all subprocesses are sequential. Failure
or timeout stops validation without asserting mathematical exclusion.

The wrapper does not check the new counting proof in a proof assistant.
The precise imported claims, source hashes, prior-art context and trust
boundaries are in [DEPENDENCIES.json](DEPENDENCIES.json); validation
commands and measured resources are in [VALIDATION.json](VALIDATION.json).
