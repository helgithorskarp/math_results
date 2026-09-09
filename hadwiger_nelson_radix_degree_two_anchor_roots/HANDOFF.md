# Exact post-h4185 audit for HN2

HN2 h4185 supersedes this pass's pre-cutoff survivor allowance: it proves all
six first-step anchor circles three-colourable at every active count. There
are therefore **no live HN2 survivor orbits from this 400-system stratum**.
Do not send the 574 pre-h4185 root-orbit slots to chromatic search.

The present result gives an independent exact geometric audit of the h4185
interface. It finds all physical common roots of the 400 post-h4181 exact-five
pair representatives containing a degree-two anchor, marks previously closed
loci, and proves exact set equality with h4185's 400 exact-five removals. The
same six curve IDs occur:

```text
591, 592, 1277, 1278, 2208, 2209.
```

The 400-pair digest is
`6863828c9a609ad2dcc2d1bb6e6669f3135972c05e2da464ea838da0f544a5c3`.
HN2's full 424-row removal has 24 additional at-least-six rows. Allowances
reconcile as `2,330+574+108=3,012`, exactly h4185's deletion total.

To regenerate the interfaces and check this integration from the repository
root:

```sh
python3 -B hadwiger_nelson_radix_degree_two_anchor_roots/verify.py \
  --check-expected --export-interface /tmp/hn-degree-two-roots.json
python3 -B hadwiger_nelson_radix_five_active_orbits/produce.py \
  --out /tmp/hn-h4185-source.json \
  --export-interface /tmp/hn-h4185-source-interface.json
python3 -B hadwiger_nelson_radix_incidence_geometry/verify.py \
  --export-interface /tmp/hn-h4185-incidence.json
python3 -B hadwiger_nelson_radix_first_step_anchor/frontier.py \
  --interface /tmp/hn-h4185-source-interface.json \
  --incidence /tmp/hn-h4185-incidence.json \
  --export-interface /tmp/hn-h4185-frontier.json --check-expected
python3 -B hadwiger_nelson_radix_degree_two_anchor_roots/crosscheck_h4185.py \
  --roots /tmp/hn-degree-two-roots.json \
  --anchor /tmp/hn-h4185-frontier.json --check-expected
```

All output paths must not exist. The root interface file SHA-256 is
`94cee1fd30d8273b2631f74afcbb0d746b3fd2c9b9a3fa85b476a604648f4c1c`;
its canonical object SHA-256 is
`8a20abdaeee5b06d4c2851945ae03cae8b56879afca5f7af59be675a88475c64`.
The h4185 interface's canonical object SHA-256 is
`5496087ac2e75104443c73022ec58bdcc71bb3bafb4605c79aed487fdd3f1da3`.

The current h4185 frontier, unchanged by this audit, is:

| Mode | Pair systems | Possible non-four orbit allowance |
|---|---:|---:|
| Exact-five compatible | 123,240 | 3,614,164 |
| Requires at least six | 7,692 | 229,528 |
| Whole frontier | 130,932 | 3,843,692 |

The representatives remain global and cannot be combined with a separate
fundamental-chamber restriction. HN2 retains physical/chromatic candidate
ownership; this package performs no chromatic search and does not independently
review h4185's colouring certificates.
