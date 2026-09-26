# Exact peak pruning of Gaussian beta rows

A certified common normalized density peak M signs every beta entry with
**j+2 >= M(N+2)**, for an arbitrary R3 contraction. The rational checker
computes M directly from finite centers, masses and variance. For fixed
M<1 this certifies a growing block of each row without computing moments.

[PROOF.md](PROOF.md) derives the rule from Aishwarya--Li's existing PC2
comparison, with the necessary extension beyond the attained density range.
It also proves why this rule alone cannot close the compact frontier:
at most A target centers force M>=1/A, leaving the indices
j<ceil((N+2)/A)-2 unresolved by this criterion.

The complete input class with target-cluster masses at most1/10, distinct
cluster separation at least1 and variance at most1/128 has M<=13/85.
It passes the first open entry b_(7,0). The compact fixture also certifies
1862702051761 entries of a much larger row. These are actual sign
certificates, not evaluations of positive sample integrals.

**Author proof; independent review pending. Full majorisation remains open.**
No strictness, optimal peak, full-row hierarchy, new KP consequence or
historical priority claim is made. The reviewed universal q<=6 strip is a
separate input; it is not a premise of this certificate.

From this directory, using Python3.11 or later, standard library only:

```sh
python3 certify.py INPUT.json --rows 7 2199023255549
python3 certify.py INPUT.json --verify CERTIFICATE.json
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Expected control status: `PRESSURE_BETA_BLOCK_EXACT_CONTROLS_PASS`.
[EXPECTED.json](EXPECTED.json) records the exact counts and hashes.
The small [certificate](CERTIFICATE.json) records both peak estimates and
complete index ranges. Only those ranges are certified. All input numbers
must be integers or fraction strings; zero masses and target collisions
are handled explicitly. See [SOURCES.md](SOURCES.md) for provenance and the
unformalized analytic trust boundary. The complete controls take about a
second on the author's host; large-row certification does not scale with N.
