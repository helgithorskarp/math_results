# Provenance and source integrity

The reviewed mathematical target is commit
`1e77997bef918a691b3ffb075025bfabb1b633d3`. Later changes in its directory
only add the pending Discovery receipt and its manifest entry. The target
producer regenerated `certificate.json` byte-for-byte. Normal and optimized
target verification agreed, and the current target manifest passed.

Selected target SHA-256 values:

```text
e0102aac8d80a266566a475cba75d70f7f738885e3abc19a0973cf7091bc2c5f  README.md
b1209b0a7336fe90f2b76af70686ff7ad4b45fdeb58f1f2e749fb55307f5a71a  PROVENANCE.md
3d8084d108cace6b9555204af95c60627d7329819e0f0b1daf9ca66ebed792e4  certificate.json
cbb30949c390ad93ff68a84e64b0bd5a21140141c552571418ff0dbf6430c32a  expected.json
7335de4c69a44e8c6bd7449e0d8614f961d27622d52d0578c0ead657c9b33808  produce.py
d8621ca16f906e3abcc47c13dd8a963a5e56194778c7c298a7ca3dbce3f48bad  verify.py
```

The three target-pinned parent hashes match the current repository exactly,
and the parent manifest passes:

```text
e21c45ca9ebf3bb33c2ed4d74c24a1c69188ff5c29c50cc4c19532863a79b207  certificate.json
430dc6ff7e81dde10856f7164caf9470d231c5f31c1dee26f0bdc62df330f207  verify.py
da98080800d4be73b1e2f7f50147b9f70870c80442b41c1ffc2a09dd887d8cd9  README.md
```

The independent checker reads none of those executable or certificate files.
It reconstructs the parent formulas and obtains both published source-stream
hashes and both target completion hashes. Its fresh completion three-word has
SHA-256
`f456d629b3c3ec073ef3c1642f954a4f408aa5b69e16e2b0cb29a10842e41763`.

The bounded committed Discovery refresh found the parent realization at
height 3,457 and the later boundary repair at 3,471. The parent depends on the
independently reviewed four-clause theorem at 3,427. No committed review or
objection addressed the exact new F3 completion. The target contribution
`bafkreifmivdqvmwlgr6vrphhlq2wimxinq62ubtmxnglpfn7diugky7vpy` remains
pending and unindexed.

The local index reported height 4,363, the RPC height 4,364, and the last
block time 2026-09-11. This stale view was not treated as current, and no
pending artifact was resubmitted. Repository, teammate and primary-record
context were refreshed on 2026-09-16 UTC before publication.
