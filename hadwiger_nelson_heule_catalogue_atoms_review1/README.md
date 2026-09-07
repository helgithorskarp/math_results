# Independent review of the Heule catalogue 21-block exclusion

Verdict: **accepted with high confidence, for the stated whole-block family**.

The reviewed result defines 21 blocks in the 711-point union of Heule's
archived `510.vtx`, `517.vtx`, `529.vtx`, and `553.vtx`. It claims that every
union of whole blocks having at most 508 vertices is four-colourable. This
directory records an independent exact audit of its geometry, block partition,
positive colouring words, and exhaustive weighted-family coverage.

The theorem is an intermediate construction-family exclusion, not a
sub-509 five-chromatic unit-distance graph and not a classification of every
at-most-508 subset of the 711-point host. A subset that splits any block, a
different relative placement, or another archive graph is outside its scope.

## Independent proof replay

[`audit.py`](audit.py) imports no code from the reviewed package. Its two main
checks differ materially from both author implementations:

1. SymPy 1.14 parses and rationalizes the coordinate expressions, then embeds
   the resulting coefficients in the exact primitive field
   `QQ<sqrt(3)+sqrt(5)+sqrt(11)>`. All 252,405 unordered pairs are squared in
   SymPy's `AlgebraicField`/`ANP` representation. This recovers 711 points,
   3,844 unit pairs, the published coordinate and edge hashes, and the stated
   21 block weights.
2. The selector audit splits the 21 weights into 10- and 11-bit halves and
   enumerates their Cartesian product. It finds 1,648,500 masks of order at
   most 508, 3,840 of order exactly 508, and 4,396 inclusion-maximal admissible
   masks. Every maximal mask is directly contained in one of the 50 coloured
   supports. Since all weights are positive, every admissible mask extends by
   adding blocks to a maximal admissible mask, so this proves coverage of the
   full family without the target's downward Boolean transform or Gray scan.

The audit checks the exact support and every induced unit edge of all 50 colour
words (165,644 inequalities). It separately reconstructs the named crossover:
the fixed-under-`sqrt(5)` part of P510 together with the nonfixed part of P553
has 508 vertices, 2,497 edges, and is the first certified support.

## Reproduction

From the repository root, first obtain the four pinned public inputs using the
reviewed package's downloader (the independent audit rechecks every byte count
and SHA-256 itself):

```bash
python3 -B hadwiger_nelson_heule_catalogue_atoms/native.py \
  --inputs /scratch/heule-catalogue-inputs --download
python3 -m venv /scratch/heule-catalogue-review-venv
/scratch/heule-catalogue-review-venv/bin/python -m pip install \
  -r hadwiger_nelson_heule_catalogue_atoms_review1/requirements.txt
/scratch/heule-catalogue-review-venv/bin/python -B \
  hadwiger_nelson_heule_catalogue_atoms_review1/audit.py \
  --inputs /scratch/heule-catalogue-inputs \
  --target hadwiger_nelson_heule_catalogue_atoms \
  --expected hadwiger_nelson_heule_catalogue_atoms_review1/expected.json
```

Expected final field: `"accepted": true`. On the review host, the public target
verifier and its normal and optimized control suites also passed. The SymPy
audit takes roughly 2.5 minutes on one CPU, dominated by exact all-pairs field
arithmetic.

## Provenance and trust boundary

Reviewed Discovery contribution:
`bafkreih2ngkfzmyvjigceoakihyf5eyanakkx3x7fspzay6yafsei3lgxi`.

Reviewed source commit: `2c3678a957519a6fd8d1d6b082fa7fa3387938b1`. The target directory remained
byte-identical at the review commit. The compact certificate SHA-256 is
`5733907c26804d6502fa8943d13071ee977d5e04d6c91027b5964adf4386291a`.

The remaining trust base is the four SHA-256-pinned upstream coordinate files,
the elementary positive-colouring and maximal-extension arguments, CPython and
SymPy's exact parsing/number-field implementation, and this audit code. No
proof-assistant formalization was performed. The certificate-generation SAT
solver is not trusted: only its explicit positive words are used.
