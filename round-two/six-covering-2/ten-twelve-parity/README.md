# Original ten/twelve parity at period10080

Actual author: **six-covering-2, researcher**. [Proof and scope](proof.md).
Author-checked exact conditional lemma; written bridge unformalized, independent
review not claimed.

For a distinct covering whose moduli divide10080 and minimum is EXACTLY8,
an ORIGINAL PRESENT10 or12 class has parity opposite to8. This removes the
last exceptional common-parity cell and reduces the credited five-class
frontier 14 to 13. Global candidates 10080/15120/20160 remain unchanged; only20160
is witnessed. This does not exclude period10080 or address minimum-at-least8.

`reproduce.py` directly checks the NEW roots with prescribed20 phases2/4/5,
credits the published intrinsic/original-class reduction8963 and its earlier
premises, and reconstructs the entire13-root application inventory. It does
not replay older proofs. No private tree, environment, ledger or solver trace
is published. All 2428 integer vectors are regenerated from source.

Run from a checkout of math_results containing the sibling dependencies:

```sh
python3.12 -m venv /tmp/min8-discovery
/tmp/min8-discovery/bin/pip install -r round-two/six-covering-2/requirements-discovery.txt
/tmp/min8-discovery/bin/python -B round-two/six-covering-2/ten-twelve-parity/reproduce.py --generate --generated /tmp/min8-three-roots --require-manifest
```

Author discovery: CPython3.12.14, NumPy2.4.6, SciPy1.17.1, all threads1.
The wrapper runs jobs serially, each with unchanged180s/700-new-node limits.
Its default12 batches per root are a voluntary regeneration allowance;
exhaustion returns INCOMPLETE, not nonexistence. Resume with the same output
path. Numeric versions/timing may produce a different valid tree; omit
`--require-manifest` to check its exact proof without requiring author hashes.
No theorem is printed until ALL three complete roots pass literal checking.

Check already generated trees with standard-library Python alone:

```sh
python3 -B round-two/six-covering-2/ten-twelve-parity/reproduce.py --generated /tmp/min8-three-roots --require-manifest
```

The independent author replay used CPython3.11.2. Expected aggregate:4050nodes,
458expansions,3592strict leaves,2428integer vectors,10002raw phases,
9226positive transports,3335669pair-phase entries; remaining forms13.
Each root's detailed hashes and every actual import pin are in
[manifest.json](manifest.json). [SHA256SUMS](SHA256SUMS) covers this compact
source/fixture bundle.

Credited source commits, recorded as provenance:

- Engine/checker8557:2d66a2b1ed2d5549e1316117d1def22a474bb179.
- Affine24-form frontier8606:433efdee31eb6f95e5ab0a753b78bb5601245714.
- Twelve-presence result8728:b1d33a7c2b7ab8091d58508033107e0f88e61c80.
- Exceptional phase alignment8837:8b66736c06f585a486c78600772b7f9513c09851.
- Original sixteen alignment8923:2dbb49922ab1266e61fbd1f003dd5e183a88d309.
- Original ten/twenty reduction8963:4b3948c7142e763d13b9cf1147b9e1323ebe2d20.

Application inventory: all 13 literal five-class residuals; all60 unused
resources and four completely free TOPs. An OPEN label means no covering or
exclusion is established here. Grouped-budget limitations and UNKNOWN solver
probes are not exclusion premises. Exact-eight and at-least-eight remain
separate throughout.

Author integrated wrapper matched the manifest in145.275s/78852KiB. The complete120960-tuple frontier agrees normally and under Python-O. Twelve damaged root domains and ten damaged application inventories reject in both modes (22 controls); guard checking is separate from the literal exclusions. The final application guard is the factored form of the integrated-run comparison and has its own positive/negative controls.
