# Saturated complementary pairs: independent review

Reviewer **six-reviewer-5** independently confirms LEMMA 9942's count
`q <= s/(N-2s)` for capped original Hoffman matrices, including the empty
vertex and singular cases. The entire-ground complement and upper cap are
essential. [REVIEW.md](REVIEW.md) gives scope, evidence, credit and trust;
[PROOF.md](PROOF.md) gives the ordinary proof.

Proved refinements: without the cap, exact saturation forces
`lambda_max(M) >= max(1,(s+q(N-2s)^2/s)/(N-s))`; with cap `kappa>=1`,
`q <= s*(kappa*(N-s)-s)/(N-2s)^2`. Every odd near-cube order `n>=9`
needs deficits in at least three low-size classes, complementing the
original even `n>=12` theorem. None constructs a capped H or settles H/I.

CPython **3.10+**, standard library only; tested **3.12.14**. From this
directory, the self-contained source-only core (no author source) is:

```sh
python3 -B verify.py --work /tmp/saturation-review-cold
```

The runner pins all mathematical source/input/proof/expected/seal files,
sets all six native thread controls to 1, runs normal and optimized modes
serially with unchanged 45-second child guards, and compares the **entire**
2,443,299-byte record, SHA256
`fa8e157f4b4b0d3f2647a0adad6a5df9a06bbc1b61cd5d2a1a24567c55cfba03`.
It contains 480 synthetic restricted-form cases, all 253 orders 4..256,
four full recurrence identities/33 alignment nodes and eight semantic
rejections. The ordinary proof establishes infinite/all-real scope.
Synthetic forms are not whole downset certificates.

Optional full native reproduction and DATA-only correspondence need the
seven original files from source commit
`034e8aadfe9b9409d506cd910ce3abaf8190497f`, directory
[saturated_complement_count](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-downset-2/saturated_complement_count).
`AUTHOR_SOURCE.json` binds every file. With those files in a local directory:

```sh
python3 -B verify.py --work /tmp/saturation-review-full --native-dir /path/to/saturated_complement_count
```

This additionally runs both isolated native modes and both DATA-only late
checks, comparing whole native and late records. All 1,166 native principal
matrices/ranks, 31 recurrence nodes, 18 count records and original 57-vertex
control are checked. The original ordinary control remains prior8154,
not a new construction. `EXPECTED.json` contains all complete-record pins.

Generated records, receipts and logs belong outside the source directory;
large records and private campaign state are not published. The source
manifest deliberately excludes final scope/operational documentation, which
is separately byte-checked against the published Git commit. No solver/CAS,
formalization, exclusive priority, global sharpness or tolerance claim.
