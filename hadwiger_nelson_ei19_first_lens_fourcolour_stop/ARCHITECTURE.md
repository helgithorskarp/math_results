# Frozen architecture

This architecture was written to scratch before its first chromatic query on
2026-09-16.

- Fixed source: the certified 19-point/35-edge EI19 realization.
- Fixed operation: adjoin both common unit neighbours of every source pair at
  distance below two.
- Fixed completion: merge every actual collision and include every physical
  unit edge.
- Cap: at most `19 + 2*C(19,2) = 361` labels at intake; exact interval
  classification reduces this to 349 labels, hence at most 349 points.
- Gate: ordinary non-four-colourability of the complete support.  Any checked
  four-word retires the architecture.
- No continuation: no second round, pair subset, phase, alternative source
  realization, or nearby algebraic operation.

The EI17 first lens closure was rejected at intake because it was already
published as exactly four-chromatic.  The current architecture uses EI19 and
does not reproduce that theorem.
