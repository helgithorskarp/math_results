# Coordinate provenance

`points.tsv` is an exact integer-basis transcription of Jaan Parts'
`v159e646.vtx` from the public data folder accompanying the graph-minimization
work:

<https://www.dropbox.com/sh/o5jdo163zycx5sc/AAB7ll1DfO36ILTISP4G0TX9a?dl=1>

The downloaded archive had SHA-256

```text
5463ebae9639235024ca29034bfc321c1dfb079c277581a6251eed72be4f6741
```

Its `graphs.txt` identifies `v159e646` as a 159-vertex, 646-edge
square-root-seven nonmonochromatic-triple gadget. Each TSV row uses the exact
eight-coefficient basis documented in `README.md`, with denominator 12. The
included verifier independently recovers the 646 strict internal edges.
