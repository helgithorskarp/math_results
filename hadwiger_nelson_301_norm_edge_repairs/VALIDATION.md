# Validation record

## Frozen inputs

* Source graph SHA256:
  `7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb`.
* Source five-colouring SHA256:
  `720466c1b6403de7d8247a33bb2844fccca306dfa21cc339b763968e6b2aea1d`.
* h3993 interface certificate SHA256:
  `7119f912d305b5ae20439bd1a138d161277cd7fc95a82a09b23feec775f3de5c`.
* h3993 repair clause SHA256:
  `2e525fb48c247195fb20e6f4c323da5e0b87611c9f0ea25974485e94dbd3dfe3`.

The source and interface are consumed from sibling packages. The verifier
halts if any frozen identity changes.

## Chromatic screen and certificate

An incremental Python-SAT Glucose4 run classified all 18 norm-support
deletions in 56.36 seconds: six SAT and twelve UNSAT solver answers. The SAT
models became the six explicit colour words. The UNSAT answers were not
accepted as evidence.

Instead, one combined sequential-selector CNF was generated for the twelve
cases. Python-SAT 1.9.dev15 Glucose42 produced a DRUP trail. `drat-trim`
independently accepted the trail and emitted an ASCII LRAT core with zero RAT
lemmas. The exact CNF, checker, hashes, and replay receipt are published. The
7,544,256-byte generated compressed LRAT is retained locally and excluded from
Git pending explicit human approval of that exact large file.

* CNF: 1,227 variables, 6,145 clauses, 76,298 bytes.
* CNF SHA256:
  `60055ca362217f4c8f5121a7d245de67c146c1283dc0adf04457224e7db6ad86`.
* Raw LRAT: 98,052 lines, 66,120 additions, 72,205 deletions,
  4,202,594 used hints, 28,590,220 bytes.
* Raw LRAT SHA256:
  `1d8bb23ff2caca290b6f3f77637c134c36ce9efb8d10961e768dffaac954413b`.
* XZ-compressed LRAT SHA256:
  `d6b008ff352d2be03b170f2a662480ddfb955f8e0e842acfe1be0dff374e4aee`.

The repository's small C++ checker reparsed the original CNF and accepted
every referenced RUP hint before accepting the empty clause:

```
VERIFIED_STRICT_RUP_LRAT
{"variables":1227,"original_clauses":6145,"additions":66120,"deletions":72205,"hints_used":4202594,"proof_lines":98052,...}
```

The checker has no RAT fallback, solver calls, preprocessing oracle, or
unchecked empty-clause shortcut. It was compiled with GCC 12.2.0. The proof
was decompressed by XZ Utils 5.4.1, and the raw hash was checked before replay.
Because the archive is omitted from the public repository, this exact local
replay is a stated trust boundary for the twelve non-four-colourability
claims; a public checkout alone cannot replay that part of the theorem.

## Geometric screen and exact audits

The h3981 obstruction search was rerun independently on each of the twelve
1,451-edge graphs using `python-flint==0.8.0`. Every case produced a fresh
certificate. Rebuilding edge `(0,143)` from the source and rerunning the
producer reproduced its published certificate byte for byte.

The trusted `verify.py` uses Python 3.11.2 standard-library integers and
fractions. Across all twelve cases it checked:

* 3,300 mandatory four-cycles and both diagonal witnesses for each;
* 6,600 distinct diagonal obstructions, including every quotient odd wheel;
* each full sparse rational parametrization and rank/nullity equality;
* each surviving norm-support edge and exact zero quadratic form;
* twelve nonzero unit-norm coefficient sums.

The producer, FLINT, its modular affine/linear search, and its printed ranks
are outside the trusted path. The checker recomputes the mathematical
identities directly from the source graph and frozen certificates.

## Independent negative controls

`verify.py --controls` rejects:

1. an improper substituted four-colouring;
2. a corrupted source edge index;
3. a corrupted geometric norm identity.

Both normal and optimized Python modes produced the frozen expected receipt.
The combined CNF was independently rebuilt byte for byte from the source and
classification table. With the locally retained archive present, both modes
also hash-check its exact size and compressed identity; a public checkout
reports that the optional local archive was not checked.

## Practical conclusion

The 18 cases form a complete, exact bounded family: six fail chromatically and
twelve fail geometrically. No physical candidate survives. The result does not
extend to the other 672 h3993 repair-clause edges or to multi-edge repairs.
The classification is author-verified; publication deliberately preserves
compact evidence while omitting the one large generated proof archive.
