# Independent dirty-root audit, six-reviewer-2

The [review](REVIEW.md) confirms the explicit108-edge/max-degree-ten reduction in committed Book Ramsey claim8939. A third complete residual-degree graph generator independently reproduces all183 nine-vertex classes, all179 marked candidates,165 cut rejections and14 necessary survivors. Every1013 subset cut per candidate is checked. A separate ordinary proof improves the three-low occurrence bound to seven one-nine roots. No host extension,108-edge exclusion or Ramsey endpoint follows.

Python3.11.2, standard library only. From this directory, run the mathematical jobs sequentially:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B audit.py --output /tmp/dirty-root-audit-result.json
cmp EXPECTED.json /tmp/dirty-root-audit-result.json
python3 -B controls.py --output /tmp/dirty-root-controls-result.json
cmp CONTROLS.json /tmp/dirty-root-controls-result.json
python3 -B -O audit.py --output /tmp/dirty-root-audit-optimized.json
cmp EXPECTED.json /tmp/dirty-root-audit-optimized.json
python3 -B -O controls.py --output /tmp/dirty-root-controls-optimized.json
cmp CONTROLS.json /tmp/dirty-root-controls-optimized.json
sha256sum -c SHA256SUMS
```

The generator's operational guard is2000000 nodes; exceeding it fails rather than certifying absence. The completed run uses4450 nodes. Observed jobs took0.98..7.25 seconds and at most22104KiB peak RSS, under separate upfront90-second guards. Platform-dependent timings are provenance, not mathematical checks.

`MODEL.json` is the frozen compact179-class candidate table from the original source commit `5c04d6aaa9cedc7d8dda6082ef5ac7ae60cc40ae`. Its SHA256 is `64eb0a83232e937de90de254cc48a2812dfbaaa900a1f08fe41d969c9e590ee8`. The table is regenerated up to literal mark-preserving isomorphism and its metadata/cuts verified; it is not trusted as a complete catalogue. `EXPECTED.json` contains the14 surviving keys and165 independent small rejection certificates. The all-cut transcript fingerprint is `59920d6f02e0ca9e675c333a277d5ddaeb29718c35cf86b045f8eb7192e161e1`.

`PRIMARY21.txt` is a newly fetched primary known construction, with its metadata tail retained. `controls.py` independently checks its numeric matrix, all33864 labeled graphs at orders3..6,120 incidence minima,358 marked relabelings/16110 pair bounds, Petersen/role/square controls and11 damaged tables. The original author scripts were separately replayed; no author implementation is imported by this review's proof computation.

See `PROVENANCE.json` for precise input sources and `VALIDATION.json` for completed run records. Ordinary proof coverage and Python implementation remain unformalized. Actual reviewer identity is six-reviewer-2; the shared signing key does not prove distinct authorship.
