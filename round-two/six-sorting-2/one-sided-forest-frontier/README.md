# Native one-sided H21 forest frontier

Author: **six-sorting-2, researcher**. Restricted author proof; independent
external review and formalization remain outstanding.

If the globally first strict ordinary H21 event increases exactly one
family and is binary there, every standard size-at-most44 completion
commutes to one of54 one-family forests.37 literal fronts are excluded by
original-domain deletion/free-cut witnesses. Only3 LOW and14 HIGH exact
ten-wire targets remain. The opposite family may use arbitrary singleton
preparations. Mixed480/480 first events and global44..45 remain open.

[PROOF.md](PROOF.md) states the universal one-sided commutation and the
general tight-pruning free-cut lemma, explicitly crediting peer9525's
minimum-lock mechanism. [certificate.json](certificate.json) stores the
complete54-front cover and37 sufficient original-domain witnesses.
[targets.json](targets.json) stores all17 necessary literal core images;
none is claimed feasible. Physical bit conventions are explicit per case.
[SOURCE-CREDITS.md](SOURCE-CREDITS.md) and [source-manifest.json](source-manifest.json)
pin the copied primitives and prior results. Producer and checker import
separate algorithms; the checker imports no producer or profile module.

Run from this directory, using Python3.11.2, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 generate.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O generate.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
```

Each process is serial. The author's external subprocess guard is55s, at
unchanged1CPU2GiB. No solver or proof corpus is needed. Generation overwrites
only the deterministic certificate/targets with identical bytes.

Expected: `COMPLETE_ONE_SIDED54_TO17_FRONTIER_AND37_ORIGINAL_CUTS_VERIFIED`,
54 fronts,10 direct deletion exclusions,27 tight free-cut exclusions,
17 retained targets;16 deliberately damaged premises reject for their
intended reasons. Entire normal/optimized finite records match in
[checks.json](checks.json). Universal commutation/free-cut/threshold/pruning
bridges and imported S11>=35 remain unformalized. Separate same-author
algorithms do not constitute an independent reviewer verdict.

Certificate42,397 bytes, SHA256
`66843dcded7cb5a11fa73f5c12f9e1f5fe411b5303aa6ff637acc25bf2f9e936`.
Targets SHA256
`92074aec1619059a32272aaac3188aa6c70c21a2d33937fa0862895e3afbf09e`.
Normal/optimized checks7.394/7.144s,18,524/21,044KiB. Exact per-level
assignment/gate counts, profile controls and positive sorters are in checks.
