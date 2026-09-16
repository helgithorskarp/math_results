# Provenance and evidence boundary

Reviewed target: sibling directory
hadwiger_nelson_e477_core_translation_union_stop, mathematical commit
621db0ad3b4be24ba7c76e1cbd7d57026d5b7669.

Pinned target bytes at that commit:

    certificate.json 3f1d0f52816eead604c1c2370c347dfe7bd56e25ba9c8fab71bf2daba82f9aad
    EXPECTED.json    3f723bfffafd65d532914a813e335af5cbeff71b3dd4624ce3914bc907dd1bea
    PROOF.md         3bf723d9fde69f4608d313e4637e833e87c0afa337300e36f20c7bb1f4b739ab
    README.md        00e9ce2fde74226029e7940363b0f05fe8b56a46ad40b59155cdc1bd82c429af
    controls.py      ec7ad288a71f3ef6b8b7630900da93cbf1861d73527376fdcfcf1945b7cfca8f
    verify.py        4a713d9d46ea718e08dfa4a8bbeee920b0c9e5290e0db8554cd986f54eb67488

Pinned source inputs from hadwiger_nelson_overlapping_forcing_seed:

    certificate.json
    3a487318d1d417e812791a1fd66d679151a7816fcf325a5bfd6a0351a0663237

    mandatory_vertices.json
    f0cea2d38b8d43e22bf82cba23ee65fb971cd031918015c9061ee499485cac2d

The target manifest passed. Its normal and optimized verifier outputs were
byte-identical and semantically matched EXPECTED.json; that expected file
uses a compact one-line selected-translation array, so it is not literally
byte-identical to the pretty-printed verifier output. Normal and optimized
target controls were byte-identical and matched CONTROLS_EXPECTED.json.
All five target corruption fixtures were rejected.

The same source was previously audited through all 477 points, all 2,458
edges, and the E477 marked-pair geometry. The committed Discovery review is
bafkreicjd47riesukjp227qrs4mcwwpndshykqsqjpzt7kbaozr4nnvnqi. The later
mandatory-support strengthening at commit
97b79af1b2b8ad71caabf3f98f07b495621ec007 is pending/unindexed; this review
therefore pins and rechecks the needed positive deletion evidence directly.

Review host: CPython 3.11.2 on Linux, standard library only. The independent
checker does not import target code and uses no solver. Its mathematical
publication commit is 6523d59fdf9b7a46e44f9e005b30275c5b45677b.
