# Independent J74 projection audit

Actual author **six-reviewer-4**, role **independent reviewer**, 2026-10-01.

[REVIEW.md](REVIEW.md) independently confirms committed lemma8551's exact
J74 area extrema, closed minimum fits and physical common-shadow cone.
It also proves that the strict-fit scale supremum is **strictly below**
the area-ratio bound `((641+67sqrt5)/722)^(1/4)`, because compactness
attains the largest closed scale while minimum and maximum shadows have
incompatible 12/18-corner counts. This is a qualitative gap, with no new
decimal bound or global Rupert decision.

Target reference:
**bafkreig4wvsmlau4koaib63i3cefofih67cczseu3hgdv2r6r54ga572aq**.
Actual target author six-rupert-2/researcher; pinned source commit
**25fc9695745b6832d068d18544452b7852b5847f**. The later receiving-cap
lemma8602 is read and cited as context, not audited by association.

From the repository root, CPython3.11+ standard library, one process:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O round-two/six-reviewer-4/j74-projection-audit/audit.py
```

Expected PASS: 62 body facets, 1,568 brightness-zonotope vertices,
22 proper minimum-fit configurations, two 18-corner maximum shadows.
The default run independently reconstructs the two-cupola model and
inspects all34,220 supporting triples; it imports no author program and
requires no external data. It regenerates all613 minimum candidates,
every brightness chamber, physical polygon areas, proper fits and360
closed-cone gates.

Append `--emit` to print the complete regenerated record. Complete record
SHA256: **ad0eca4deff6ab018746ecc7c1a2da2a8f24b0430797db6cb2d08f6e9764fcd1**.
`--expected PATH` checks a supplied record. Optional `--author-source DIR`
reads the pinned author's `model.py` and `expected.json`, without executing
them, to compare all60 vertex entries,62 facet sets,613 spectrum entries
and22 proper matrices. Use the files at the recorded commit for this
optional bridge; the author's main directory may contain later work.

Source arithmetic uses common integer denominators and exact signs in
Q(sqrt5); geometry uses complete supporting triples, lexicographic
infinitesimal signs, Jarvis boundary walks and spatial frame inverses.
[VALIDATION.json](VALIDATION.json) separates independent runs from the
original author's replay and records rejection of three corrupted inputs
under optimization. [SHA256SUMS](SHA256SUMS) covers the compact files.

The finite coverage, geometry and compactness arguments remain ordinary
written mathematics. No proof assistant, solver, approximate predicate,
external hull catalogue, omitted large dataset or failed search is used.
