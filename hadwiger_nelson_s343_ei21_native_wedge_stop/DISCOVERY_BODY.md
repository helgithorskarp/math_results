**Exact computer-assisted finding (strict scoped construction stop).**  Put
the reviewed 343-point opposed-B214 support S343 and the reviewed 21-point
EI21 contact source in their displayed native coordinate frames.  They share
exactly their origin.  The complete collision-merged strict plane
unit-distance graph has 363 vertices and 1,821 edges and chromatic number
exactly four.

Exact outward rational intervals decide all 6,840 private cross pairs.  Every
such squared-distance interval excludes both zero and one, with certified
margins greater than 1/100000.  Together with complete reconstruction of the
58,653 S343 pairs and 210 EI21 pairs, this decides all 65,703 pairs of the
union.  The origin is the unique articulation vertex; deleting it leaves
components of orders 342 and 20.  A literal proper four-colour word is checked
on the canonical complete edge stream, while the embedded Golomb graph
excludes three colours.

This is the separability stop for one frozen native-frame mixed composition.
It is not five-chromatic, not a sub-509 record candidate, and not a theorem
about other relative isometries, EI21 roots, or mixed-source placements.  No
adjacent phase, translation, rotation, deletion, or contact sweep is implied.

Reproducible source:
https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_s343_ei21_native_wedge_stop

Verified mathematical source commit:
`c6bb45a2268c60b48b95919203963a87126743fa`.

Replay from the repository root with CPython 3.11 or later:

```sh
python3 -B hadwiger_nelson_s343_ei21_native_wedge_stop/verify.py
python3 -O -B hadwiger_nelson_s343_ei21_native_wedge_stop/verify.py
(cd hadwiger_nelson_s343_ei21_native_wedge_stop && python3 -B controls.py)
(cd hadwiger_nelson_s343_ei21_native_wedge_stop && sha256sum -c SHA256SUMS)
```

Canonical edge-stream SHA-256:
`3fa1c4a97d2294323041612e4a3ddf1d62992cc8e72376a5d0dcc879c917d613`.
Four-word SHA-256:
`8d91715e8eeb2c1ea3a843be3f6722014fe0b3f32d9a26841b568a4519dd5e8d`.

The checker uses exact multiquadratic arithmetic for S343 and the published
rational contraction box for the unique EI21 root.  Trust remains in the
written interval reduction, the hash-pinned public source inputs, CPython
integer/Fraction semantics, and ordinary hardware.  No SAT verdict,
floating-point incidence test, omitted trace, or numerical root finder is a
proof premise.  This is author-side evidence, not an independent review.
