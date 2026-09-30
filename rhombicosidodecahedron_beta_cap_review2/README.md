# Independent RID beta-cap review, six-reviewer-2

Confirms the original all-source receiving caps of chord radius **1/640**
and nonwinning squared-height slack **1/600**. Proves the larger closed
caps **1/480** and nonwinning slack **1/450**, hence squared-diameter slack
**2/225**. All source rotations, rolls, translations and scales at least
one are covered. The global RID Rupert question remains open.

[REVIEW.md](REVIEW.md) contains the theorem, continuous proof, exact margins,
strengthening opportunities and explicit trust boundary. A successor's
newly claimed numerical global slack is identified but not audited here.

## Reproduce

Python 3.11+ standard library only. In a full checkout of this repository:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_beta_cap_review2/audit.py \
  --output /tmp/rid-beta-cap-review2-actual.json
cmp /tmp/rid-beta-cap-review2-actual.json \
  rhombicosidodecahedron_beta_cap_review2/expected.json
```

The checker imports hash-pinned previous reviewer code from these sibling
directories, never the target researcher's code or witness fixtures:

- `rhombicosidodecahedron_winning_receiver_review2`
- `rhombicosidodecahedron_threshold_receiver_review2`
- `rhombicosidodecahedron_contact_collar_review2`

For a sparse checkout, hydrate these directories first, or pass explicit
`--winning-review`, `--threshold-review` and `--contact-review` paths.
Exact commits and file digests are in [INPUT.json](INPUT.json). If a pinned
dependency has advanced, extract it at that recorded commit and pass its
directory. The older full global classification is an explicit previously
reviewed dependency; it is not rerun. All new contacts, both complete remote
roll policies, and the stronger whole-circle winning reference gap are
regenerated with different exact root enclosures and interval evaluation.

The supplementary native replay requires the original target directory at
commit `7dec5c34b27552eaf8cbc8b06c06ed5e09a245bc`, with its pinned inputs:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B beta_cap_certificate.py --self-test > /tmp/rid-beta-cap-native.json
```

Compare parsed JSON with that commit's `beta_cap_expected.json`. The native
checker does not certify this review's enlarged caps. The independent
normal and optimized checks compare byte for byte, reject fourteen malformed
controls, and use one CPU with unchanged resource limits. Reproducibility
and resource measurements are in [VALIDATION.json](VALIDATION.json).

## Files and scope

[audit.py](audit.py) is the independent checker;
[expected.json](expected.json) is its compact regenerated certificate with
complete selected closed witness runs and record hashes. [INPUT.json](INPUT.json)
pins the original inspected source and reviewer dependencies. No solver,
floating mathematical predicates, private ledger, key or large corpus is
used or published. Continuous geometric arguments are written and remain
unformalized.
