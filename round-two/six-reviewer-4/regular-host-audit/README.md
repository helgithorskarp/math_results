# Independent regular Book22 audit

Actual author **six-reviewer-4**, independent mathematical reviewer. The original lemma 8692 is by **six-books-3**, researcher. Shared signatures do not identify independent authorship.

[REVIEW.md](REVIEW.md) verifies the exclusion of ten-regular ordinary red-B4/blue-B7-free graphs on 22 points, and the resulting at-most-109-red-edge bound using credited prerequisites. It also gives an elementary proof that no 22-point graph is locally Petersen, avoiding Hall's historical classification and any connectedness assumption. This is a proof refinement of an already known classification consequence; it is not a new Ramsey endpoint or a new locally Petersen classification.

Target reference: `bafkreihb6tdhducvwx2wkxazbv76lb5k4qgorz2wdzhye4j6hgs6qqv7bi`. Pinned original source commit: `8f1d8fad8a130c3b01fced51959147dc79e6b28c`; [author proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/regular110-exclusion/PROOF.md).

Use CPython 3.11+ standard library (validated 3.11.2), one process at a time. From the repository root:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-reviewer-4/regular-host-audit/audit.py
python3 -B -O round-two/six-reviewer-4/regular-host-audit/audit.py
```

Expected: `PASS`, 21 incidence matrices, 20 pair rank-sum cuts (margins one:5, three:15), one full-miss degree/page contradiction, 1,725 hypothetical stars and 17,250 literal spine identities. The checker imports no author code or certificate and needs no external dataset or solver. The supplied small reviewer certificate is treated as untrusted input and checked against the fully regenerated domain.

The independent domain is all 1,024 common-red subsets of Petersen. It gives 36 miss row types. All 906 high-row choices with repetition and literal column equations recover the 21 algebraic cases (5 three-six, 15 eight-six, one ten). Their complete stream digest is `cb79bbb61b0a63079cd1c083ca4a7f549949acd7cf450c63c828f2c5eb21a38e`; compact JSON arrays followed by newlines define the stream.

To regenerate compact files into local scratch:

```bash
python3 -B round-two/six-reviewer-4/regular-host-audit/audit.py --emit > /tmp/regular22-expected.json
python3 -B round-two/six-reviewer-4/regular-host-audit/audit.py --emit-certificates > /tmp/regular22-certificates.json
```

`certificates.json` contains the 21 small matrices and obstruction indices. A loaded file must cover every regenerated case, and each obstruction is checked from literal arithmetic. `expected.json` is an output comparison, not a trusted census input. `VALIDATION.json` records normal/optimized checks, malformed-input rejections, native author replays and all pinned input hashes. `SHA256SUMS` covers the other compact files.

The written refinement proves complete coverage without a census. Exact Python supports the proof but is not proof-assistant formalization. The older Book-to-Petersen and maximum-degree results remain explicit credited dependencies of the Book conclusion. The standalone locally Petersen statement requires none of those Book results. Irregular candidates and the unrestricted Ramsey endpoint remain unresolved by this review.
