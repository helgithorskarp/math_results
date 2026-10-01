# Independent Book Ramsey root-defect-eight audit

Actual reviewer: **six-reviewer-4**, independent mathematical reviewer.
Original claim: **six-books-1**, researcher, graph8426,
`bafkreibyw66n6vgrgz45rjzsvcdtv3o7c65qj2awm3ap4yjae5w4kc6muq`.
Reviewed author commit: `ff45238df47d0f180436c87ed9963c46acff18c3`.

[REVIEW.md](REVIEW.md) confirms the conditional ordinary-book theorem:
in a valid 22-point graph with degree histogram (4,16,2), total incident
defect on the six even-degree roots is at least eight. It gives a simpler
finite proof: no active-defect placement enumeration is needed. This leaves
the complete histogram and R(B4,B7) unresolved.

CPython 3.11.2, standard library only. From this directory, run sequentially:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 audit.py --expected expected.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -O audit.py --expected expected.json
python3 controls.py --expected controls_expected.json
python3 -O controls.py --expected controls_expected.json
sha256sum -c SHA256SUMS
```

Both main runs take about 50 seconds and less than 36 MiB peak RSS in the
review environment. They rebuild all 13 root-profile/weight cases and all
199 incidence forms, compare every labeled local star and active defect
against a different decoder, and replay every reciprocal deletion. All
199 forms are excluded: 115 already have an empty local domain; the other
84 empty under synchronous reciprocal pruning. The 56 weight-two forms
are included without the author's correlation-based rejection.

The main command also exhausts 1,653 two-row incidence multisets and all
3,375 nonempty three-point row-domain systems, including 2,397 with a
symmetric solution. These are completeness/false-exclusion controls, not
additional 22-point Ramsey cases. The separate controls validate signed
identities on 16 graphs, reject a fabricated supported deletion, and check
the known positive 21-point construction. Signed controls violate the book
hypotheses and are not constructions for the target.

[incidence.py](incidence.py) uses ordinary integer quotas and ordered row
recursion; [spines.py](spines.py) constructs literal 22-point root spines;
[reference.py](reference.py) scans all 65,536 binary masks independently for
each labeled vertex. Neither the author code, author runtime records, a
supplied list of incidence forms nor expected-output hashes determine the
proof domain. The two compact expected files are read only after rebuilding
the result. [INPUT.json](INPUT.json) and [VALIDATION.json](VALIDATION.json)
record exact provenance, completed commands and resources.

Optional passive comparison with the author's original 143 forms:

```sh
python3 audit.py --expected expected.json --export /tmp/book-reviewer-records.json
python3 -O ../book_ramsey_4_7_degree_reductions/degree98_root_four_check.py --records /tmp/book-author-records.json
python3 -O ../book_ramsey_4_7_degree_reductions/degree98_root_four_independent.py --records /tmp/book-author-records.json --report /tmp/book-author-check.json
python3 -O compare_author.py --author-records /tmp/book-author-records.json --reviewer-records /tmp/book-reviewer-records.json
```

Use the author files whose hashes are listed in INPUT.json. The original
9,152 multiplicity entries agree; all 12,693 original representative
mask/defect pairs belong to the reviewer's relaxed literal domains. This
comparison follows the standalone proof and supplies no exclusion premise.
Runtime incidence/domain corpora and logs are generated outside the public
directory and omitted from publication. Guards raise INCOMPLETE rather than
returning a mathematical negative result. A surviving reciprocal fixed point
raises an error rather than being claimed impossible.
