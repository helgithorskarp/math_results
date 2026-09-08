# Arithmetic five-colouring of VND case 10

An explicit algebraic colouring completes the accepted lower bound for the
64,513-point VND source to **chromatic number exactly five**. Removing the
origin gives **chromatic number exactly four**, on 64,512 vertices and 542,328
edges. This reproduces the known chromatic claim; it does not reduce the order
or improve the 509-vertex record.

Both halves have natural F4 residue colourings. All 120 joining edges connect
residue-zero vertices. Swap colours 0 and 1 on the second half and give the
origin a fifth colour. The [proof](PROOF.md) also derives a positive boundary
constraint: every four-colouring of either half gives the origin's colour to
at least one of its 120 joining ports. No individual pair-forcing claim or
smaller module is established.

With Python 3.11, from the repository root:

```sh
python3 -B hadwiger_nelson_vnd_residue_interface/prepare_inputs.py --work /tmp/vnd-residue
python3 -B hadwiger_nelson_vnd_residue_interface/verify.py --work /tmp/vnd-residue --check-expected
```

The first command downloads the pinned author data and uses the sibling
package's safe parser to normalize coordinates. The second uses only the
standard library, reconstructs the assignment from the compact
[certificate](CERTIFICATE.json), and checks every one of the 542,472 edges.
It also checks the origin-deletion colouring, all 24 relative palette
permutations, and five rejected corruptions. Expected status:
`VERIFIED_VND_RESIDUE_FIVE_COLOURING_AND_ORIGIN_DELETION`.

For an independent production path, in an environment with python-flint 0.8.0:

```sh
python3 -B hadwiger_nelson_vnd_residue_interface/produce.py --work /tmp/vnd-residue --output /tmp/vnd-residue/five_colours.bin
python3 -B hadwiger_nelson_vnd_residue_interface/verify.py --work /tmp/vnd-residue --producer-word /tmp/vnd-residue/five_colours.bin --check-expected
```

The producer uses polynomial arithmetic in Q(zeta24); the checker uses two
integer linear forms and direct edge checks. The colour word is regenerated
outside Git. Its SHA256 is
`29c1812533c1c173c1491fe88dc7f358477c92dec0d5b4ce2abe21be0d473f36`.
No solver call occurs in any command above.

Exact unit geometry and non-four-colourability are imported from the
[verified source](../hadwiger_nelson_vnd_case10_verified_gate/README.md),
independently [accepted here](../hadwiger_nelson_vnd_case10_review1/REVIEW.md).
The original [paper](https://arxiv.org/html/2106.11824) already reports the
five-colouring strategy. See [PROVENANCE.json](PROVENANCE.json) for source
identities and [VALIDATION.json](VALIDATION.json) for this replay.

The fixed proof-base retention route remains closed. This milestone
consolidates the positive source and its boundary information; no <=508
construction gate has been justified by it.
