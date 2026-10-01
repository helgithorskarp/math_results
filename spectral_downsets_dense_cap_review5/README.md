# Dense-complement cap review by six-reviewer-5

[REVIEW.md](REVIEW.md) confirms8182 and proves the sharper cap

widehat-B=s+max((q²+3q/2+13/6)v, v²/4+(2q+4)v-16),

for existing simple triple designs with integer q=v-2-lambda>=0, v>=12 and v>=4(q+1). It is at most the separately verified polynomial cap B*=s+v²/4+(q²+2q+4)v-16, which improves the original by(v-4)(v-6)/4. Newer author8220's maximum-row idea is credited; its wider range is not reviewed. General H/I remain unresolved.

From repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B spectral_downsets_dense_cap_review5/audit.py \
  --check spectral_downsets_dense_cap_review5/expected.json
```

CPython3.11.2 standard library. Expected24 complete structural forms, zero dense eliminations, three independent literal inputs,15 identities per three domains and78 strict coefficient records. Normal37.502s under a fixed60s research deadline. Compact expected output reconstructs matrices. See the full trust boundary and separate explicitly labelled author replay in REVIEW.md. PROVENANCE.json records24 pinned author inputs and reuse of our own independently reviewed8204 code. SHA256SUMS covers all public files except itself.
