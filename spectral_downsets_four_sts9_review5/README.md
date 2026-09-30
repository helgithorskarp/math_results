# Independent four-STS(9) review

Reviewer: six-reviewer-5, independent mathematical reviewer. See
[REVIEW.md](REVIEW.md) for the complete verdict, proof bridges, strengthening
and limitations. No author code is imported. General H and I remain open.

Use Python 3.11.2, standard library only, one process at a time. From the
repository root, reproduce the independent census, matrices and stronger
gap using the existing compact public seed:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
mkdir -p scratch/four-sts9-review5
python3 spectral_downsets_four_sts9_review5/audit.py \
  --input spectral_downsets_steiner_triples/four9_certificates.json \
  --input-sha256 8035b0ca8ae954922d649c67ab36aaa758fa9635960e067ef9312ff1bbaf7e99 \
  --output scratch/four-sts9-review5/audit.json
cmp scratch/four-sts9-review5/audit.json \
  spectral_downsets_four_sts9_review5/audit_expected.json
python3 spectral_downsets_four_sts9_review5/template.py \
  --input spectral_downsets_steiner_triples/four9_certificates.json \
  --output scratch/four-sts9-review5/template.json
cmp scratch/four-sts9-review5/template.json \
  spectral_downsets_four_sts9_review5/template_expected.json
```

Expected: 840 labelled systems, 192 fixed-first candidates, 10,048 actual
unions/decompositions, 12 distinct point-isomorphism types, 2,068,080 labelled
unions, 2,110,080 labelled decompositions. All 12 seeds have centered rank
84 and gap 16; the new mixture has rank 85, epsilon 1/419 and gap 8.
The original matrix hashes also match. Fifteen literal designs and nine
universal rational-function identities plus one fixed arithmetic identity
confirm the scoped seven-weight obstruction; a positive-coefficient
certificate proves its negative eigenvalue on the full parameter range.

Measured final census/matrix audit: 49.627 seconds, 23,744 KiB child RSS;
optimized replay: 46.128 seconds, 26,072 KiB, identical JSON. Template check:
0.667 seconds, 17,348 KiB. These are measurements, not runtime guarantees.
`python3 -O` also retains all checks: explicit exceptions are used.
Do not run the two CPU jobs simultaneously. No solver or native numerical
library is required. Neither private ledgers, keys nor classification files
are inputs. The public seed is external untrusted data, fully decoded and
checked with its exact hash. If it changes, recover the reviewed version
from the provenance commit and do not bypass the hash requirement.

The source proves finite coverage through its documented exhaustive
algorithms; the universal obstruction and tensor statements also require
the written bridges in REVIEW.md. This is an exact computer-assisted and
ordinary mathematical proof, without proof-assistant formalization.
