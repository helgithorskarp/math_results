# Independent all-multiplicity H review and missing-STS cap

**six-reviewer-5**, independent mathematical reviewer. [Complete mathematical verdict and proof](REVIEW.md). Reviewed8082 at source5924fcb7ff82d701dad1986fef8a77560ac6abb8, conditional on an existing simple2-(v,3,lambda) design,v>=13,lambda>=2. Smaller-order8122 is outside this verdict. General H/I remain open; historical priority is not claimed.

The review confirms ordinary maximal rank and qualified caps, sharpens the generic cap to27lambda^2v/16, and proves capv^2+8v-18 for full triples minus an existing STS. The latter provides capped maximal factors outside the original generic range.

Reproduce from repository root, CPython3.11+ standard library (tested3.11.2), one process/thread:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B -O spectral_downsets_lambda_review5/audit.py \
 --check spectral_downsets_lambda_review5/expected.json
```

Expected: status passed,29 named identities,53 positive coefficient records,six complete structural PSD forms; canonical result SHA256b1962bacb1ed1f77ba364cfca910134040a905a54189360f90201d02444e0a25. Normal and optimized runs match; about21s/51MiB measured. The complete decomposition, incidence identities, strict Schur margins and norm comparison are the mathematical certificate. These are not six dense eliminations. Earlier dense attempts stopped at fixed600s/180s caps; neither supplied upper verification. No resource setting changed. Reproduction cost is not guaranteed.

- [audit.py](audit.py): independently constructed literal fixtures, entrywise definition and principal-factor checks, incidence/complement identities, kernel Gram ranks and malformed-input controls.
- [certificates.py](certificates.py): complete constant/mean-zero Schur and operator-norm certificates. Its preconditions are the literal entry, star and principal-factor checks in audit.matrices.
- [scalar.py](scalar.py), [symbols.py](symbols.py): independently derived dense exact rational polynomial certificates, including33 Schur coefficients and the improvements.
- [exact.py](exact.py): this reviewer's reused Fraction utilities; [fraction_free.py](fraction_free.py): independently written Bareiss control checker. Backend controls use729 complete principal-minor comparisons and two rational Gram cross-checks.
- [expected.json](expected.json): compact fixtures, certificate metadata, exact coefficients and matrix hashes; not a large matrix corpus.
- [PROVENANCE.json](PROVENANCE.json): authorship, pinned source hashes, versions, resource/trust scope. [SHA256SUMS](SHA256SUMS) covers every public file except itself.

Optional pinned-author reproduction bridge, **assertions enabled**:

```sh
review_author_dir=$(mktemp -d)
git archive 5924fcb7ff82d701dad1986fef8a77560ac6abb8 \
 spectral_downsets_steiner_triples | tar -x -C "$review_author_dir"
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B spectral_downsets_lambda_review5/source_bridge.py \
 --author-dir "$review_author_dir/spectral_downsets_steiner_triples" \
 --check spectral_downsets_lambda_review5/source_bridge_expected.json
```

Expected20 pinned files, four matched centered/repaired matrix hashes,27 original identities,30 original certificates,33 matching Schur coefficients; canonical bridge SHA256428760d7dafc5c1e88d448c5d31d7876fe5420cfa4221cca0df6553735ee68bc. About0.8s measured. This intentionally imports original code in a separate process and is a source bridge, not independent evidence or a replay of its full12-form dense suite. Extra archived files are ignored; required pinned files must match exactly.

Ordinary unformalized proofs and CPython exact arithmetic are the trust boundary. Finite inputs do not prove an unbounded theorem without the written complete decomposition. No CAS, solver, floating eigenvalue test, credential, private ledger, hidden large certificate or formal proof is required.
