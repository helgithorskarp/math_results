# Exact validation record

**six-vdw-3, researcher**, 2026-10-01. CPython 3.11.2,
GCC (Debian 12.2.0-14+deb12u1) 12.2.0, python-sat 1.8.dev24 / CaDiCaL195.
The full reproduction completed in **35.985 seconds**, peak parent/child
**95868 KiB**, sequentially with solver/BLAS/OpenMP thread counts one.
No larger resources or concurrent CPU computation were used.

```sh
scratch/solver-env/bin/python round-two/six-vdw-3/signed-phase-defects/reproduce.py --workdir scratch/signed-defect-reproduction
```

Result: `VERIFIED_ONE_EXCEPTION_EXCLUSION_AND_SIGNED_DEFECT_REDUCTION`.
The public README gives a fresh virtual-environment command independent of
these workspace paths. Generated source, binaries, models, logs and proofs
remain outside the public directory.

The independent audit imports neither generator nor solver and passes normal
and optimized Python with exactly the same complete outputs:

- all 2187 signed local vectors; 129 without a conflicting pair;
- 2064 explicit stable realizations validating the written local-boundary proof;
- all 896 local single-exception truth assignments;
- all 5253 field supports and all 5253 unordered field pairs, each pair in 21 supports;
- every one of the 35394 CNF clauses reconstructed by a separate method;
- all 618 one-exception ternary skeletons under the complete normalization;
- 36 nearest-phase and 108 baseline-translation truth entries;
- 63654 CRT point/affine identities, with a verified unit multiplier;
- exhaustive normalized orientations at q=7 (64) and q=13 (4096), testing both
  comparison and one-exception phases, including 8239 actual negative AP
  witnesses and 81 complete positive cyclic checks;
- three malformed model controls rejected in both Python modes.

The small counts are (separable, one-exception) = (21,8) at q=7 and (52,0)
at q=13. The positive cyclic q=7 fixture is `0100000` with exception at zero.
Its period is 42; it is not a length-3704 witness. These finite controls are
not target bound improvements or independent peer reviews.

A separate next-frontier test of the constant-skeleton cut model, normalized
by affine pullback and color exchange to v(0)=0,v(1)=1, returned UNKNOWN after
200002 reported conflicts in 27.670 seconds under a 200000-conflict cap.
It establishes no exclusion and is not an input to the one-exception proof.
That exploratory job and source remain in private workspace scratch.

The initial 20000-conflict probe was UNKNOWN (20002 reported conflicts,
2.418 seconds) and established no exclusion. The separate 200000-conflict
probe returned a candidate refutation after 64271 conflicts, 77325 decisions,
26679226 propagations and 972 restarts. Fresh full reproduction used identical
stats and proof bytes. Initial solve timing was 14.658 seconds; fresh timing
was 8.876 seconds. Solver timings are operational measurements, not proof.

The checksum-pinned converter's initial pass took 6.095 seconds. Its LRAT
output was independently replayed by the credited positive-RUP checker:
50662 additions, 86012 deletions, 1960881 propagation hints, and an empty
clause. Initial replay took 5.168 seconds. Normal and optimized replays in
the fresh wrapper agree on all counts and hashes. Eight invalid generic
proofs and two corrupted production proofs were rejected. A one-conflict
solve returned UNKNOWN and was not reported as a mathematical exclusion.

CNF: 633071 bytes, SHA256
`ea4df0d39af79b7e8c59a317acd24bb7c9f26f4e388f30286f56b63d52b05dd8`.

Regenerated DRAT: 6882465 bytes, SHA256
`69e5a1e8d9d18958a59bdccecb50565b7f08082435bdb188bf2e4ffcd434ef91`.

Checked LRAT: 15039613 bytes, SHA256
`c186c5a0c87025f7d62dd7a154a06d6609c5794130f30419f42c355c04a40daa`.

Only compact source, proof text and expected metadata are published. The
checker is separate from the solver and encoding generator, and is reused
with explicit provenance from six-vdw-1. This does not claim that another
researcher has reviewed this new theorem. The written mathematical bridges
are unformalized. The full separable 103-column and unrestricted interval
construction questions remain open.
