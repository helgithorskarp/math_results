# Provenance and source integrity

## Reviewed target

- Mathematical target commit:
  `f0eb1800e26a053190b5ef18bb5190304072d05b`.
- Geometry certificate SHA-256:
  `4e94704ca1f96743f1bb950393ff4fadd6377d8a33697f0debb484722d8cd162`.
- Self-sum certificate SHA-256:
  `983e7f2da0ef236d2c9fd2e26cda93649c8873c04940183877e62cbded0e88a8`.

The review pins immutable bytes rather than accepting a moving branch tip.

## External construction source

The EI21 parametrization is adapted from Jeremy Tan Jie Rui's Shibuya
repository at commit `218097c9971db2b60ab94a0b8dae20d76741cc43`:

- [`pegg.py`](https://github.com/Parcly-Taxel/Shibuya/blob/218097c9971db2b60ab94a0b8dae20d76741cc43/shibuya/graphs/pegg.py),
  retrieved SHA-256
  `2ba335b24fd02294030595d9b0ae055b30b10b4dfc886f183eb27321c0de75c1`;
- [`generators.py`](https://github.com/Parcly-Taxel/Shibuya/blob/218097c9971db2b60ab94a0b8dae20d76741cc43/shibuya/generators.py),
  retrieved SHA-256
  `f80d80994c712049aedfcac1c635a0f6691d9c296e2ac42cbe7981394359f500`.

The review reconstructs the 38 source edges from the `ei21_vertices` operation
sequence rather than merely trusting the certificate label.  The package's
included MIT licence matches the upstream repository licence.

## Record boundary

The bounded live literature and graph-evidence refresh on 2026-09-15 still
supports Jaan Parts's 509-point, 2,442-edge plane unit-distance construction
as the smallest published five-chromatic example.  Haugland's August 2026
paper independently calls that the smallest while studying the distinct
Moser-spindle-free frontier.  A recent 509-vertex, 2,259-edge certificate
changes the edge frontier at the same order, not the vertex record.

- Parts, [*Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*](https://arxiv.org/abs/2010.12665).
- Haugland, [*A Moser-spindle-free 5-chromatic unit distance graph on 2131
  vertices in the plane*](https://arxiv.org/abs/2608.04542).
- Amer, [509-vertex edge-reduction data](https://github.com/md-amer/hadwiger-nelson-e5).

The present self-sum is four-chromatic and makes no priority, minimality, or
record claim.
