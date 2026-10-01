# Independent native-prefix sorting audit

Actual reviewer: **six-reviewer-5**, role **independent mathematical reviewer**,
2026-10-01. Target: committed lemma 8690 by **six-sorting-2, researcher**.

The literal native 24-comparator prefix has a standard sorting extension of
total size at most 44 if and only if one of 39 published nine-wire Boolean
images can be sorted with at most 12 further standard comparators. Arbitrary
suffix depth and comparator order are covered. These are partial input images,
not the full nine-wire Boolean cube. No surviving target is solved here.

[REVIEW.md](REVIEW.md) independently checks the arbitrary-length route
argument and complete finite reduction, and proves that only the published
lower bound S(11) >= 35 is needed: S(12) and the global S(13) lower bound can
be removed from the dependency list. It also verifies that the surviving
images form an antichain under literal and reversal-plus-complement inclusion.

Our code imports no researcher module. It propagates a separate exact set of
packed rank states for every original clamping family, compressing duplicates
after each gate. Kernel trees are built backwards by dyadic capacity splitting;
all topological orders are then enumerated and checked. This differs from both
the author's truth-function generator and forward merge-order/scalar checker.

From repository root, CPython 3.11+, standard library only:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-reviewer-5/native-prefix-audit/fetch_inputs.py --dest /tmp/six-reviewer-5-native-inputs
python3 -B round-two/six-reviewer-5/native-prefix-audit/audit.py --input-dir /tmp/six-reviewer-5-native-inputs
```

The two original public inputs total 287,638 bytes; [INPUTS.json](INPUTS.json)
authenticates them by length and SHA256. The source commit is recorded separately.
They are fetched into local scratch rather than duplicated in this publication.
Changed input bytes cause failure. [EXPECTED.json](EXPECTED.json) is the complete
stable output, never an input to the audit. [VALIDATION.json](VALIDATION.json)
records normal/optimized executions, versions, resources and output hash.

Expected status: `INDEPENDENT_NATIVE24_AUDIT_PASSED`. Checks reconstruct all
338 original histories and their 745,472 free assignments, all 45 kernels and
39 surviving images, all 900 kernel orders with 115,200 Boolean function
controls, the six explicit exclusion records, and all published snapshots.
Four certificate corruptions are rejected. The exact finite reconstruction
supports the written arbitrary-length proof; it does not replace that proof
or re-run Harder's original Isabelle-checked lower-bound corpus.

No global 44-versus-45 result, new sorting construction, historical priority,
or classification of arbitrary thirteen-wire prefixes is claimed.
