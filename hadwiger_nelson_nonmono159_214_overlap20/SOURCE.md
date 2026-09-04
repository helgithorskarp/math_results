# Coordinate provenance

`points159.tsv` and `points214.tsv` are exact integer-basis transcriptions of
Jaan Parts' `v159e646.vtx` and `v214e977.vtx`, respectively. Both source files
occur in the public data folder accompanying the graph-minimization work:

<https://www.dropbox.com/sh/o5jdo163zycx5sc/AAB7ll1DfO36ILTISP4G0TX9a?dl=1>

The downloaded archive had SHA-256

```text
5463ebae9639235024ca29034bfc321c1dfb079c277581a6251eed72be4f6741
```

Its `graphs.txt` identifies `v159e646` as a 159-vertex, 646-edge
square-root-seven nonmonochromatic-triple gadget and `v214e977` as a
214-vertex, 977-edge distance-three nonmonochromatic-pair gadget. Each TSV row
uses the eight-coefficient field basis stated in `README.md`, with denominator
12. The included programs independently recover the strict internal edge
counts.
