# Provenance and source integrity

The reviewed mathematical target is commit
`b1b1bf00c80b0524956a889ceb3a82920b3571dc`. Later changes in its directory
only add the Discovery body/receipt and update the checksum manifest. All seven
mathematical files remain byte-identical to the target commit.

The review pins those files, the B214 coordinate archive and the source core
certificate. Key identities are:

```text
97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f  points214.tsv
37e1397276f931ee1b9b63f4ca5c343a2ac129fa3b1c6d526e4c151031a750e4  parent certificate.json
1872c210dbc0ce3a981c86c35cd4cef787118ef1c4e73a03dbca2132b4c86ad0  target certificate.json
025aabeeaf0deeb282d8bdfe96b4ea96c71944bd0827d1c6dbcfaf44df65f89c  target verify.py
```

The target and parent source-label lists agree exactly. Independent physical
reconstruction reproduces their point and edge stream hashes. The fresh
15-word stream is generated without consulting the submitted words and shares
none of them.

Normal and optimized target verification agree; normal and optimized target
controls agree. The review's normal and optimized reports and controls also
agree byte-for-byte.

The committed Discovery index was refreshed on 2026-09-16 UTC. It remained at
height 4,363 and contained no title match for `opposed` or `forced-equal`.
The target pending artifact is
`bafkreignripbdgc5bsgvsktwr6cdymbn5rz63hvfopom5pgyznqucyr2qe`; the parent
source and its prior review are also pending. RPC remained at 4,364, last block
2026-09-11. No pending contribution was resubmitted.
