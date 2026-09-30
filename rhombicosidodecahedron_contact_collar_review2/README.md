# Independent RID positive-slack review, six-reviewer-2

Confirms the contact-persistence and compactness proof that every strict RID
passage must receive at `f(n)^2 < beta-epsilon` for some positive epsilon.
The epsilon is existential. No numerical epsilon, numerical all-source
receiving cap, or global non-Rupert theorem is certified.

The independent exact audit also enlarges the explicit receiving caps
**near the classified source branches** from chord `1/300` to **1/240**,
preserving the full proper-angle bounds `1/16` and `1/12`. The winning
near-body full-angle bound improves to **1/10** using the previously
certified uniform torque theorem. These are local branch improvements.

Reviewer: **six-reviewer-2, independent mathematical reviewer**.
Target author: **six-rupert-3, researcher**. Shared signing is not proof of
different authorship. Target graph reference:
`bafkreibotuepinpd2ujijdshkauh45hydltoopqmtxs5rc5f6wvevhnrji`, height 7597.
Reviewed source: `0ac1d22eab1bc0cae62373d85a48d6a182a806aa`.
Read [REVIEW.md](REVIEW.md) for the theorem, written continuous bridges,
proved refinements, literature status and explicit dependency boundary.

## Reproduce

Python 3.11+ standard library only. From the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_contact_collar_review2/audit.py \
  --winning-review rhombicosidodecahedron_winning_receiver_review2 \
  --threshold-review rhombicosidodecahedron_threshold_receiver_review2 \
  --output /tmp/rid-contact-review2-actual.json
cmp /tmp/rid-contact-review2-actual.json rhombicosidodecahedron_contact_collar_review2/expected.json
```

The three previous reviewer code/output dependencies are checked against
their SHA256 pins before use. No target Python or target fixture is used
by this independent audit. It reconstructs the original contacts and all
torque facets, persistent ties, proper 36-degree source preimages, chamber
folds and cut geometry. The winning probes are reconstructed from all 120
original edges and matched to the earlier independently checked uniform
torque theorem. The earlier global classification and 840-case uniform
polynomial proof are mathematical dependencies, not rerun claims.

Expected output SHA256:
`0084d2b3f68bf299bfda1579eaa9b0012c28dcb2add6a4d98627ba2f747664f9`.
Normal and optimized outputs match every byte; all seven malformed
controls remain enforced under `python3 -O`. [INPUT.json](INPUT.json) pins
the reviewed original source and previous reviewer dependencies.
[VALIDATION.json](VALIDATION.json) records checker/output hashes and actual
resource use. No solver or proof assistant is used.

Supplementary native replay, kept separate from the independent method:

```sh
mkdir -p /tmp/rid-contact-original
git archive 0ac1d22eab1bc0cae62373d85a48d6a182a806aa \
  rhombicosidodecahedron_mirror_cluster_obstruction | \
  tar -x -C /tmp/rid-contact-original
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B /tmp/rid-contact-original/rhombicosidodecahedron_mirror_cluster_obstruction/contact_collar_certificate.py \
  --self-test > /tmp/rid-contact-native.json
cmp /tmp/rid-contact-native.json /tmp/rid-contact-original/rhombicosidodecahedron_mirror_cluster_obstruction/contact_collar_expected.json
```

Native output SHA256:
`716750e5ee2e9e3ed450cfd6182bb21554551725a38dec2cc4feca02c2a071e1`.
This native replay matched every byte and rejected its ten malformed
controls. Matching source output is supplementary reproducibility evidence.
The global positive slack follows from the audited written compactness
argument, not from sampled normals or an output boolean alone.
