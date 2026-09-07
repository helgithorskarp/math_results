# Independent review of the de Grey 1581 residue-section exclusion

Verdict: **accepted with high confidence for the stated affine-hyperplane
extraction family**.

The reviewed theorem defines an eight-component residue map on an exact
1,581-point realization of de Grey's original construction. Every affine
hyperplane whose selected support has at most 508 vertices is claimed to induce
a four-colourable strict unit-distance graph. This directory supplies an
independent exact audit of the source construction, geometry, projection,
candidate-space completeness, and all positive colouring words.

This is an intermediate construction-family exclusion. It is not a
five-chromatic graph below 509 vertices and does not classify arbitrary
at-most-508 subsets, different projections or moduli, or other geometric
placements.

## Independent audit

[`audit.py`](audit.py) imports no code from the reviewed package and uses two
materially different implementations.

1. The 39 seed rows were independently transcribed from Section 6 of
   [de Grey's paper](https://arxiv.org/html/1804.02385v2). SymPy constructs the
   twelve rotation/reflection images and performs the two complex affine
   assemblies symbolically. This recovers intermediate orders 397, 395, 791,
   and 1,581 and proves that the two outer copies meet only at `(-2,0)`.
   Coordinates are collected in the displayed 16-element radical basis at
   scale 3,072.
2. All 1,248,990 pairs are rejected through two new exact ring homomorphisms,
   modulo 3,061 and 3,251. Every survivor is then checked in SymPy's exact
   primitive field `QQ<sqrt(3)+sqrt(5)+sqrt(7)+sqrt(11)>`. This recovers 7,877
   unit edges and the target's complete coordinate and edge hashes. Modular
   equality never certifies an edge.
3. Rather than assuming a leading-digit convention, the audit enumerates all
   19,680 nonzero affine equations in `F_3^8` and quotients by simultaneous
   multiplication of the normal and level by 2. The resulting 9,840 classes
   contain 2,118 admissible descriptions and 2,100 distinct supports, including
   32 descriptions of order exactly 508.

The exact independent graph checks the base colouring of all vertices except
the zero-residue endpoint `(2,0)`. Every nonzero-level section omits that
endpoint and therefore inherits this colouring. The 120 exception words are
proper on, and exactly cover, the distinct admissible zero-level supports. In
total, 133,146 selected-edge colour inequalities are checked. No SAT result or
search-completeness claim belongs to the proof.

The target's own normal and optimized verifiers and controls also passed,
including 2,816 exhaustive small subset/threshold fixtures, 256 basis-product
checks, equality of its two full reconstructions, and 18 malformed-certificate
rejections.

## Reproduction

From the repository root:

```bash
python3 -m venv /scratch/degrey-section-review-venv
/scratch/degrey-section-review-venv/bin/python -m pip install \
  -r hadwiger_nelson_degrey1581_residue_sections_review1/requirements.txt
/scratch/degrey-section-review-venv/bin/python -B \
  hadwiger_nelson_degrey1581_residue_sections_review1/audit.py \
  --target hadwiger_nelson_degrey1581_residue_sections \
  --expected hadwiger_nelson_degrey1581_residue_sections_review1/expected.json
```

Expected final field: `"accepted": true`. The audit is single-threaded and
uses no network or solver.

## Provenance and trust boundary

Reviewed Discovery contribution:
`bafkreigqgtqu6jjrk556jya6xxyukjbwji4griq37dwfvhhkezkvrwkzka`.

Reviewed source commit: `2ffd62ff75a87c13b91d15150fa655eeb77dbb4a`.
The reviewed directory was unchanged at the review commit. The source and
certificate digests are frozen in the audit.

The remaining trust base is the independently transcribed primary-source seed
table, the stated construction and residue definitions, elementary finite-field
projective equivalence, CPython and SymPy's exact symbolic/number-field
implementations, and this checker. No proof-assistant formalization was used,
and no historical-priority claim for the extraction heuristic is made.
