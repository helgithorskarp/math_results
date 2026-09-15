# Provenance and source integrity

Reviewed target: sibling directory
`hadwiger_nelson_e457_hexagon_orbit_connector_stop`, mathematical commit
`a41aa85d3fed7c60a3065546b95ae7e9ca36f476`.

Pinned target bytes:

```text
DISCOVERY_BODY.md c54446a4204089e5fd78a7899c0d97dccd117a0fa4fb284faffe7682c3a3f388
README.md 1a4215aa93227c01ad890be99ccf90b281ae3458068a67abdb4f68d73069de2e
SHA256SUMS b10aa93cc92e7e82e367a583c7bbb7629f006fc26834bace7ec7c7085aef0cc6
VALIDATION.json 3e44de8c2c7a5f3e25464f22c1056238f5552692707308fe653d60d28130056b
controls.py 1adc9d428d3db337f7805b9ba19174f097004af6a153e284f6a6cb8b89d92848
expected.json b313421dc8b369ee0c377c8a3fbee0b30237d5d9cd988b1da2a9a60640b6a086
verify.py fdc58ed2787fe6fc78937c26eaafc378181768227fbd807902e724666b1d4d40
```

The target checksum manifest passed. Its normal and optimized verifier output
was byte-identical and matched `expected.json`; all eight target controls
passed.

The full-union audit reads the self-contained E457 input
`hadwiger_nelson_e457_equal_pair_source/core.json`, SHA-256
`d377e9526d13cc76aba6762ecd6a79bd04fe12d61e03a0b585a5ea38820d833b`.
The 457-point source and its terminal-equality theorem were independently
accepted in `hadwiger_nelson_e457_equal_pair_source_review1`; the present
positive union check needs only the hash-pinned coordinates and proper
equal-terminal four-colour word.

Review host: CPython 3.11.2 on Linux, standard library only. Mathematical
review commit: `48ac659cd8e9ed5323000cae785e3cdcad3b6718`.
