# Provenance and trust boundaries

## Reviewed target

Target directory:
<https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_opposed343_sqrt5_lens_stop>

Mathematical target commit:
`8a98d34290f4ba578a28ae69aa1edb8fe7399d85`.
Later commits add only its Discovery body and pending receipt.

The checker pins these exact inputs by SHA-256:

- target `certificate.json`:
  `a412d0e0b18e6113319a645c21d2562db43218a315c907cd2636ff4fc60a179b`;
- B214 `points214.tsv`:
  `97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f`;
- parent S343 `certificate.json`:
  `3f6a4a13ead37de71ceb3cd1818d21a9036ea0273e151461fc54d9df1a8c2e19`;
- independent parent-review `EXPECTED.json`:
  `4e4724c48f4f673c7e21b7ac4a0dac0c0feaa14d86dd750e085efea9536fce0a`.

The exact parent was independently accepted in
[the opposed-B214 review](../hadwiger_nelson_golomb_opposed_b214_review1),
mathematical review commit
`5ed67074e4008c0549f8c2e35dc1bf2e86485891`.

## Independent and imported parts

This review independently reconstructs all coordinates, lens points, center
pairs, complete unit edges, positive source and final words, new-layer
components, Moser subgraphs, attachment sets, and connectivity. It imports no
target Python module and does not use the optional PySAT generator.

The proposition that the source has no normalized inputs beyond its 66
survivors is imported from the prior independently checked S343 theorem. The
present code pins that evidence, reconstructs the same induced source, and
checks all 66 positive parent words, but does not replay the parent's
1,382-lemma RUP proof a second time.

## Trust boundary

Finite checks trust CPython 3.11+ arbitrary-precision integers, JSON and TSV
parsing, this review source, and the four pinned files. The geometric lens
derivation, completeness of the direct pair scans, backtracking graph
isomorphism/coloring, and low-link coverage argument are ordinary
unformalized mathematics. Controls use a second flat square-class
representation and literal small-instance brute force. No floating-point
comparison or third-party solver lies in the review trust boundary.

The source fixture's historical identification with the Parts gadget is
imported from its cited provenance. This review does not verify a globally
minimal construction, enumerate an untested finishing family, or make a
record claim.

At intake the target Discovery contribution
`bafkreiaubewpnqtl3ojkopl42mqcvgc6zv7imbw5y22qg3kvfikz22y53m` had CheckTx
code zero but remained absent from the height-4363 committed index while RPC
was at 4364. It is pending, not committed, and must not be resubmitted merely
because of index staleness.
