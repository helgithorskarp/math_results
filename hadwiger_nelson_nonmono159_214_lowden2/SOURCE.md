# Coordinate provenance

`points159.tsv` and `points214.tsv` are exact integer-basis transcriptions of
Jaan Parts' `v159e646.vtx` and `v214e977.vtx`, respectively, from the public
data folder accompanying the graph-minimization work:

<https://www.dropbox.com/sh/o5jdo163zycx5sc/AAB7ll1DfO36ILTISP4G0TX9a?dl=1>

The downloaded archive had SHA-256

```text
5463ebae9639235024ca29034bfc321c1dfb079c277581a6251eed72be4f6741
```

Its `graphs.txt` identifies the first as a 159-vertex, 646-edge
square-root-seven nonmonochromatic-triple gadget and the second as a
214-vertex, 977-edge distance-three nonmonochromatic-pair gadget. An exact Python check using the arithmetic in `enumerate_lowden.py`
recovers both strict internal edge counts; see `VALIDATION.md`.
