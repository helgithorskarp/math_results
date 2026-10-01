# Wider dense-cap review by six-reviewer-5

[REVIEW.md](REVIEW.md) confirms claim8220 for every existing simple triple design with integer q=v-2-lambda>=0, v>=12 and 2v>=5q+10. It clarifies a factor-two margin label and proves a strictly smaller rational cap throughout this range using the exact3x3 comparison and inverse-trace inequality. Rounded examples give centered caps226/350 and repaired buffers37/43 at(v,q)=(13,3)/(15,4). General H/I remain unresolved.

From repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B spectral_downsets_dense_row_review5/audit.py \
  --check spectral_downsets_dense_row_review5/expected.json
```

CPython3.11.2 standard library; all16 complete structural forms, zero whole dense eliminations, two independent literal inputs,60 identity/domain checks,138 strict coefficient records and18 repair tables/204 terms. Assertions are not needed in the independent checker; optimized execution preserves its checks. Source plus compact expected output reconstructs all matrices. The separate author bridge is explicitly labelled in REVIEW.md. PROVENANCE.json pins27 original inputs and openly reused reviewer code, including the binary-star support-sum optimization. SHA256SUMS covers all public files except itself.
