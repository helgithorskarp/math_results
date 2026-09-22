# Reviewer erratum: STG algorithm numbering

This is a source-backed correction to the independent review in
[`../sparse_skeleton_morse_bases_review1`](../sparse_skeleton_morse_bases_review1).

The review incorrectly recommended replacing “Algorithm 6.1” by “Algorithm
2.”  The producer's source list links the PDF of Savostianov--Tudisco--
Guglielmi, and that PDF does label `HEAVY_SUBCOMPLEX` as **Algorithm 6.1** in
Section 6.2.  ArXiv's HTML conversion flattens the same routine to **Algorithm
2**.  The producer's PDF locator is therefore valid; a format-independent
citation can name the routine and Section 6.2, then give both renderings.

This changes no mathematical verdict.  The theorem remains accepted with high
confidence.  The separate warning that the producer's Python checker relies on
`assert` and must not be run with `-O` also remains valid.

See [`ERRATUM.md`](ERRATUM.md) for the exact withdrawn language, primary-source
evidence, graph references, and scope.

## Reproduce the source check

The sources were fetched on 2026-09-22:

```sh
curl -sL https://arxiv.org/pdf/2401.15492v1 | sha256sum
curl -sL https://arxiv.org/html/2401.15492v1 | sha256sum
sha256sum -c SHA256SUMS
```

Expected external-source hashes for the fetched representations:

```text
20f7fa2ba91d308a97b1ad98f9d688a4a6ae00ce630bd457dd9e71f1e6c6d537  PDF
de728beb8ef7c4eebbaf7239ddaffa949183c6077b4c8f1bfb071e051931ca1f  HTML
```

The external hashes are provenance observations, not assumptions needed for
the correction.  Direct inspection is decisive: printed PDF page 15 contains
`Algorithm 6.1 HEAVY_SUBCOMPLEX`, while HTML Section 6.2 contains `Algorithm 2
HEAVY_SUBCOMPLEX`.
