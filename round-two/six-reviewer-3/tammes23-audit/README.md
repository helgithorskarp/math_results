# Independent audit of Tammes lemma 8835

Actual agent **six-reviewer-3**, independent mathematical reviewer. See
[REVIEW.md](REVIEW.md) for the complete scoped verdict, geometric proof,
primary literature, prior-art credit, dependency boundaries and proved
strengthenings. The 15-point endpoint completion remains conditional on
separate lemma 8755.

The checker imports no author/prerequisite code. It reconstructs all four
orientations by Gram linear systems and rational square extraction, checks
157 rational functions and every unit/contact identity, and certifies all
closed-interval signs by primitive Sturm chains. All 54 remaining pairs
are strictly below 23/50 by radical elimination on the whole interval.

From a full clone, use CPython 3.11+; only its standard library is needed:

```bash
python3 -B round-two/six-reviewer-3/tammes23-audit/audit.py \
  --certificate round-two/six-tammes-2/twenty-three-contact-core/certificate.json
python3 -B round-two/six-reviewer-3/tammes23-audit/replay.py \
  --certificate round-two/six-tammes-2/twenty-three-contact-core/certificate.json
```

For a sparse checkout, download the single 18,082-byte input from the pinned
revision specified in [INPUTS.json](INPUTS.json) and pass its local path with
`--certificate`. The checker verifies its raw SHA-256 before decoding.
No shared ledger, signing key, solver, algebra package, or network connection
is needed once this one file is present.

Use `audit.py --output FILE` to save complete exact evidence. Its printed
summary omits the detailed Sturm certificates and per-pair routes; those
are retained in the full output and [EXPECTED.json](EXPECTED.json).
The replay compares the **complete** normal and optimized outputs, including
all certificates and pair routes, and applies a fixed 180-second guard to
each serial child. Optional `--output FILE` saves resource validation;
`--evidence-output FILE` saves the agreed complete evidence. Peak child RSS
is a cumulative upper observation, not a subtraction-based estimate.

The fixture's inequalities are exact rational statements rather than
numerical samples. The written geometry remains an ordinary proof and is
not formalized in a proof assistant. [VALIDATION.json](VALIDATION.json)
records the actual reviewed run.
