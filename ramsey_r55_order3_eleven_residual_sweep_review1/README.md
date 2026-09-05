# Independent review: eleven-cycle residual exclusions

This directory independently supports Discovery Net contribution
`bafkreig2suecaqfks55vn36bjf4cwebdt3kaetfogefuxcwcm67mwsldqm`, “Complete
43-vertex formulas exclude 34 further eleven-cycle minority cores.”  The
reviewed source was pinned at commit
`d7e46a1b9f8830bc54d74212f794f4dabce26c01`.

## Verdict and exact scope

**Support.** All 34 asserted UNSAT cases were independently reconstructed,
solved, and proof-checked.  The formulas and deterministic proof traces match
the published SHA-256 values case by case.

This is an intermediate symmetry-case reduction, not a 43-vertex Ramsey graph
and not a proof that `R(5,5) >= 44`.  Under the accepted order-three
automorphism reduction of type `1^10 3^11`, it concerns the eleven-cycle
minority split with four red and seven blue moving triangles.  It removes 34
of the 79 residual canonical core classes (21,942 of 51,696 labeled cores),
leaving 45 classes (29,754 labeled cores).  Together with the preceding
118-class blue-`K4` exclusion, 152 of the original 197 canonical classes, or
85,789 of 115,543 labeled cores, are excluded.  The remaining 45 classes, the
two three-red/eight-blue cores, and other automorphism types remain outside
this result.

## Independent proof path

The Python checker imports no code from the reviewed sweep.  It instead:

1. Pins the accepted 79-case classification and the reviewed result files by
   SHA-256, checks complete entry-level coverage, and independently recomputes
   the 34/45 partition and labeled multiplicities.
2. Derives the 18 core variables from the cycle-pair ordering.  They are
   `1..9, 31..36, 58..60`.
3. Regenerates the accepted complete parent formula, parses all 615,920
   clauses and 34,280 variables, and recompiles/runs its separate C++ formula
   auditor.
4. Constructs every reviewed formula directly by appending the case's 18
   signed unit clauses, producing 615,938 clauses.  Every regenerated formula
   hash equals the corresponding published hash.
5. Runs one Kissat worker per case, requires exit code 20, and checks every new
   DRAT trace with `drat-trim`.  It records a case only after `s VERIFIED`.
6. Confirms that `drat-trim` rejects a deliberately unsupported empty-clause
   proof.

All 34 checks passed.  The fresh traces totaled 583,276,093 bytes and contained
10,703 RAT lemmas in their checked cores.  Their proof hashes also matched the
published values exactly.  The maximum observed solve and replay times were
10.349 s and 22.542 s; peak child-process RSS across the recorded runs was
159,840 KiB.  The certificate-regeneration completion invocation took 576.138
s.  Four checkpoints originated in earlier controller-interrupted invocations,
so that figure is not a clean end-to-end benchmark.  A subsequent strengthened
resume invocation replayed all 34 retained proofs again in 381.383 s, removing
the prior checkpoint flags from the final verification trust boundary.

`result.json` is the compact review record.  Its
`case_manifest_sha256=f2d6e27f96e3d1c70e6b6d538fcef7d146c55422ee62c2d136cdb109f7d8e5df`
hashes, in canonical JSON, each case's index, bit word, labeled multiplicity,
formula hash and size, proof hash and size, and checked RAT-core count.  This
lets a rerun compare all proof-relevant fields without publishing the 583 MB
of generated formulas and traces.

## Reproduction

Run from the repository root with Python 3.11, a separately built Kissat 4.0.4
binary, `drat-trim` at source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, and `g++`:

```bash
R55_REVIEW_WORK=/scratch/r55_eleven_residual_sweep_review1
python3 -B ramsey_r55_order3_eleven_residual_sweep_review1/independent_replay.py \
  --work "$R55_REVIEW_WORK" \
  --kissat /path/to/kissat \
  --drat-trim /path/to/drat-trim \
  --solve-seconds 60 \
  --replay-seconds 300
```

The production run used Kissat source commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2` (binary SHA-256
`9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`)
and `drat-trim` binary SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
The work directory must be outside the repository.  Add `--resume` to reuse
only checkpoints whose formula and retained-proof hashes still match; every
retained proof is nevertheless replayed again during the resumed invocation.
A file named `STOP` in the work directory stops safely between cases.

Expected terminal status:

```text
ALL 34 CLAIMED EXCLUSIONS INDEPENDENTLY REGENERATED AND VERIFIED
```

## Trust boundary

The review independently checks the new 34-case UNSAT layer, but imports the
previously reviewed completeness of the 197-class catalog, the preceding
118-class exclusion, and the accepted full parent encoding.  It directly
re-audits the exact parent artifact, not the mathematical derivation of those
predecessors.  It also trusts Python, the compiler/runtime, Kissat, and
`drat-trim`; the latter is exercised on both positive certificates and a
negative control.  The 45 timeout/open cases were not rerun because the target
makes no existence or satisfiability assertion about them.  Large generated
CNFs and DRAT traces remain outside Git; the source, compact result, hashes,
and deterministic regeneration command are published here.
