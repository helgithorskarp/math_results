# Provenance and source integrity

The fixed inputs are sibling files in
`hadwiger_nelson_overlapping_forcing_seed`, originally added by commit
`5b28dad38f14e0979a10feb436c95e453dbb34d5` and unchanged in this review:

```text
certificate.json
3a487318d1d417e812791a1fd66d679151a7816fcf325a5bfd6a0351a0663237

mandatory_vertices.json
f0cea2d38b8d43e22bf82cba23ee65fb971cd031918015c9061ee499485cac2d
```

The complete E477 spindle classification was published at commit
`9e7765b8a748642071e2e252218ac425e3846cdf`; its prior independent review was
published at commit `9d06fc04abe594391710b5eb671d70defba4c12d` and is committed in Discovery Net
as `bafkreicjd47riesukjp227qrs4mcwwpndshykqsqjpzt7kbaozr4nnvnqi`.

Immediately before this publication, the prior review's checksum manifest
passed and `independent_check.py` reproduced `verification.json`, including
all 16 exact plane frames, 3,625,216 cross-pair tests, and the imported
terminal-equality audit.  Relevant current-file hashes were:

```text
classification README.md
f9a15319c712d2bcd0d4f2d84a528e4de8b1f6192b215b7cbb9748be6efb24ce
classification verify.py
431d4cc53a68659d90b17e5e347b274f49e42ff5558d8cc26b56c26c14ab0fe6
classification separating_basis.json
dc6034eff3b3059c73b76373f8176e810cf3ffdf448b6ce98edb571dad67dc4d
review1 independent_check.py
c58b1ebfc92c0f621828bc97654ed743b5c67f2de9945c9b72b03abce09ee939
review1 verification.json
f7593d3493cba8fbf6eb88121e1f0fc62879be81e1e62145b65d2986812db69f
```

Review runtime was CPython 3.11.2 on Linux.  The package needs no third-party
dependency.  Mathematical publication commit:
`MATHEMATICAL_COMMIT_TO_BE_RECORDED`.
