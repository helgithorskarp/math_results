# Provenance and integrity

The reviewed mathematical target is commit
`bcb699cc9890480c93c24716155a7fb5f4b5cea1`. The current versions of all nine
mathematical target files are unchanged from that commit. Later target-folder
changes only add the Discovery body/receipt and update its checksum list.

Pinned target hashes are embedded in `independent_check.py`, including:

```text
5bc6df88afed13c6ccff2154c749fc1f5e74a9892b6b13f79ab08bbc49cd2e17  h632.csv
9a68a448527fafd9ea02b31eee6f2b97e2f0430595b29984aa5c79f6ce97c121  points.csv
c6b4b06b5883d1d8d94693413ff3314148130f3255044f6ecee707ab0fc5d646  edges.csv
ad0d6ed39a1c40d0b3233025b907709947412ad4fc6159fb1d443ee0b38da986  certificate.json
40ee6f68d1142ca8b096a7bab1ac60e77f0d4912d8911fcb6bf4c1efc4f5484a  verify.py
b4c54106aef03486ffba7e4fabcd9a35f46f411c9dad80f9c997f8a29e7b71df  reproduce.py
```

The four original input files also match the hashes frozen by the target:

```text
3f60fe94c7cd3d9c70b7cc52124fa185d4b46d54bb59b21bca0c45d2b181fd51  H516 SOURCE.json
89345930e1bea184ce2457b0e14a015bcd9a2901cfc609a6468cf050234a8317  fresh_candidates.json
3a22660e40329c0aef34e108b91747f529adb046cf687df5b05b3531ca17e35b  H560 certificate.json
bc8e0f5f5ec7fa5f2376cc77ba0e65f6023b340cf48990370d5eda575d30ae79  H510 certificate_H510.json
```

Normal and optimized runs of the author verifier were byte-identical. The
reviewer checker reads the data and literal certificate but imports neither
author executable. Its independently reconstructed H632 and final point/edge
streams agree entry-for-entry, and its fresh four-word differs from the
published word.

The bounded Discovery refresh on 2026-09-16 UTC reported committed height
4,363 and no contribution with `coupled-edge` in its title. Direct lookup of
the target's first broadcast artifact returned null. RPC was at 4,364 with
last block time `2026-09-11T02:40:58.067131057Z`. Accordingly the broadcast
is recorded only as pending and was not resubmitted.
