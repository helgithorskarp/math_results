# Coarsest-resource covering review and pair-overlap refinement

Independent reviewer: **six-reviewer-5**. See [REVIEW.md](REVIEW.md) for the
complete verdict, hypotheses, proof, literature and strengthening section.

The committed coarsest-top shared-label inequality and its exact
period-43200 prefix cut are confirmed. A proved pair-overlap correction
reduces the same certificate's capacity from 596930 to 596075, increasing
its margin from 70 to 925. The full period and global LCM bound remain open.

From the repository root, CPython 3.11+, standard library only:

```sh
python3 -B number_theory/distinct_covering_coarsest_block_review5/check.py
python3 -B -O number_theory/distinct_covering_coarsest_block_review5/check.py
```

Both commands must reproduce [expected.json](expected.json). The fresh
checker imports no target code and checks every actual resource phase.
The attributed [input.json](input.json) is the exact 1564-byte target
certificate, source `959893f7358905bc46ddb01fdcaaffa8086ffe3f`.
The proof uses exact block counting; no solver or external search data is
required. No historical priority or proof-assistant verification is claimed.
