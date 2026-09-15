# Provenance

Review target: `hadwiger_nelson_parts136_mixed_native_transfer_stop` at commit
`e68a1e0496c9d82da079847cd7675e87136e9f92`.

Target certificate SHA-256:
`2714c9bfebc2a88775ad0f512c5cdcbb510f7eb22caddc451d28504608c48cf2`.

The coordinate tables are byte-identical to these earlier repository inputs:

- `parts509.tsv` = `hadwiger_nelson_parts136_reverse_receiver/points.tsv` at
  commit `119e7444ff958ce30e017dbff9fddfe45f5915f2`, SHA-256
  `f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50`;
- `points159.tsv` and `points214.tsv` = the corresponding files in
  `hadwiger_nelson_nonmono159_214_lowden2`, available at commit
  `fa6f78f998ba36a40a8077f2c00d3656d0b40322`, with SHA-256 respectively
  `4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02`
  and `97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f`.

The latter package documents the coordinate transcription from Jaan Parts's
public `v159e646.vtx` and `v214e977.vtx` data. This review relies on that
provenance and independently checks the repository copies and complete
physical graph; it does not repeat the original archive transcription.

The review implementation imports no code from the target. Its arithmetic
representation differs from the target verifier. The review certificate is a
fresh positive colour witness rather than a geometry dump.

Review certificate SHA-256:
`5313f8881c2650ca8bdeb7e844cbfe6947bdae7e20570508ae6742e3ffcfb8f1`.
