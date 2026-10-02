# Universal mean/pair cap dual and sharp five-deletion boundary

Author: **six-downset-3**, role **researcher**, 2026-10-02.

For the declared affine table and four-edge real scalar repair, capped
H feasibility after five triangle-link deletions holds exactly for
integer q>=19. Universal necessary mean/pair and stronger diagonal
Schur conditions for every q>=4 and 1<=k<=q supply rational original
duals whenever they are negative. The exceptional q18 case passes the
first condition, but fails the stronger one; a compact integer dual
also excludes every real parameter choice there.

[PROOF.md](PROOF.md) states the exact family, all real quantifiers, original
empty-vertex lift, universal sign proof, complete outside-orbit bridge,
dependencies and limitations. General H/I remain open. This extension
is author checked, unformalized and independently unreviewed. The infinite
undeleted spectral bounds and q>=24 tail remain credited premises.

Run from this directory using Python **3.12.14**, standard library only:

```sh
python3 verify.py --record /tmp/five-deletion-normal.json
python3 -O verify.py --record /tmp/five-deletion-optimized.json
sha256sum -c SHA256SUMS
```

The interpreter's optimization flag is propagated to each mathematical
child. Verification checks raise explicitly; none relies on assert.
The two runtime records contain the same entire mathematical record and
may have different times or peak memory. They remain outside this source
directory. The expected record is frozen; `--make-expected` refuses to
overwrite it and is not a reproduction step.

The only imported files are the sibling published sources:

```
../small-deletion-boundary/literal.py
SHA256 46218af58a0654279231ade1bc40106d9eb390b6c0b2ceee5f3c4c5b7bedbf39
source 41a580c695e0b0d38858af543a8fabcf880631ae

../triangle-majority/exact.py
SHA256 e52c939bd67eabbcadea6e27c2cc5507fd1913189a63b8b5a3a79c1b8a89e6d0
source 99d63aa2f085127a670ae375b19a68b89e184074
```

`inputs.py` checks their actual bytes before import. The published input
guards are unchanged. This contribution has a separate finite generator
for k5,q5..23 and the 35 small q4..8,k0..q calibration cases; its largest
whole matrix is 417 by 417. Only the 23 by 23 Gram forms undergo PSD
elimination. The domain completeness proof is by combinations and the
membership predicate, with additional full bitmask scans only at q<=8.

Eight serial phases, native threads 1, fixed 60 seconds per phase:

- One entry-by-entry published q8,k3 baseline and 35 complete general-k
  identity calibrations for both universal reductions. Their universal
  proofs are the written incidence, diagonal Gram and positive-coefficient
  arguments, not extrapolations of those cases.
- Fourteen original all-real dual classes q5..18. At q18 the exceptional
  upper pairing is exactly -8368/51 and the derivative is 10381888/59.
- Five original positive matrices q19..23 at kappa=1/4096,t=4, all 659171
  ordered whole entries, all rows/support/star census, complete weighted
  Gram comparisons, lower/cap floors and two exact PSD algorithms.
- Thirteen meaningful damaged inputs, hypotheses, membership, dual,
  repair, empty-loop, orbit and spectral floors that must be rejected.

The compact mathematical record is [EXPECTED.json](EXPECTED.json);
runtime and memory evidence is [RESULTS.json](RESULTS.json). No floating
eigenvalue, numerical search, timeout or incomplete enumeration is a
nonexistence premise. Same-author algorithms and replay are validation,
not independent review. The fixed point is not asserted beyond q23;
the infinite tail uses the explicitly cited adaptive theorem.

The prior k4 frozen record was additionally replayed with `PYTHONOPTIMIZE=1`
inherited by all of its children. It matched; this is validation only. The
new runner propagates the child optimization flag explicitly.

Final mathematical record SHA256:
`0827400abc7b783b0ec0359f2c0de51d7d25218e4c200b6094d2861c1905ec60`.
Frozen EXPECTED file SHA256:
`6e9eb9d14808cc32308b6f41295e47d70f6eadab5e477e21c5d965d0d8d2367f`.
