# Coordinate provenance

`points.tsv` is an exact integer-basis transcription of Jaan Parts'
`v159e646.vtx`. The source file occurs in the public data folder accompanying
Parts' graph-minimization work:

<https://www.dropbox.com/sh/o5jdo163zycx5sc/AAB7ll1DfO36ILTISP4G0TX9a?dl=1>

The downloaded archive had SHA-256

```text
5463ebae9639235024ca29034bfc321c1dfb079c277581a6251eed72be4f6741
```

and its `graphs.txt` identifies `v159e646.vtx` as a 159-vertex,
646-edge nonmonochromatic equilateral-triple gadget with side `sqrt(7)`.

Each TSV row contains eight coefficients for `x`, then eight for `y`, in the
basis documented in `README.md`; all coefficients share denominator 12.
The exact strict unit-distance census of the transcribed set is independently
recomputed by the included programs and equals 646.
