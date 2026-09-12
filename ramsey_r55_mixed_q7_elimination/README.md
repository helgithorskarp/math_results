# Complete mixed-q7 elimination for the good43 carrier

Every good43 has a maximal-packing representative with **q=7,r=7 or
q>=8**. The two entire mixed-color q7 strata, covering all 640 cores
each, can be removed from the global representative union. The registry
shrinks from 2,189,178 to **2,187,898** task IDs. The preceding all-q
exchange normal form remains compatible.

The finite ingredient is sharp: every 19-vertex coloring has a red K5,
a blue K4, or two disjoint red K4s. All 640 catalog-core formulas have
independently checked DRAT proofs. A red-twin expansion of the Paley
graph gives the sharp 18-vertex control. Rubin's 2023 reported
classification already implies this local threshold; **historical
novelty for the threshold is not claimed**.

Read [the full proof and trust boundaries](PROOF.md) and
[the exact receiver contract](HANDOFF.md).

This is a complete global redirect, not 1,280 old-task UNSAT verdicts.
No original task verdict or owner queue is changed, and R(5,5) remains
unresolved. The reduction removes only 0.0584694% of task IDs and about
3.7178866e-16 of the unfiltered ordered carrier volume. It supplies no
new restriction on q8 in this pass. The old all-q result is preserved.

## Evidence

- `CERTIFICATES.json`: all 640 core records, formula/proof hashes,
  clause counts and checked verdicts. Manifest SHA256
  `c61ca3f18b386d82c8801acfd6cb7a6fc4c5e424daf283e8ded390d2133b1a79`.
- `EXPECTED.json`: complete finite-proof summary; 60 variables per case,
  22,150,762 clauses altogether.
- `encode.py` and `reference.py`: specialized and independent literal
  grounders. All 640 canonical formulas agree.
- `CONTROLS.json`: sharpness, essential hypotheses and 33,296 exhaustive
  small-assignment comparisons with graph definitions.
- `CONTROL_19.json`: genuine local good19 control with no blue K4 and
  832 disjoint red-four pairs. It is not a good43.
- `TRANSPORT_EXPECTED.json`: six full43 transports spanning both removed
  strata, permutations, 24 rejected corrupt packets and a physical-five
  return. These full43 fixtures are explicitly non-Ramsey graphs.
- `CARRIER.json`: all sixteen retained ranges and exact integer carrier
  comparison, not an estimated or sampled count.

The standalone solver/proof run took 114.61 seconds with four workers.
The 632,091,299 CNF bytes and 137,751,329 DRAT bytes are preserved outside
the repository. Source and compact hashes suffice to regenerate them.
The published source has not received external independent review.

## Reproduction

Run from the repository root. Python 3.11.2 and its standard library
suffice except for the external solver and proof checker. The unchanged
sibling dependencies are pinned in `DEPENDENCIES.json`.

Obtain the four pinned catalogs using the existing input downloader:

```sh
python3 -B ramsey_r55_global_maximal_packing/catalog.py /absolute/data --download
```

The upper-bound lemma uses only `r44_15.g6`. Its exact input SHA256 is
`53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1`.
The order-3,7,11 catalogs are used by the physical destination interface.
Catalog completeness is imported from McKay's author-maintained
[complete collection](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).

Build the official tools in scratch, not inside this contribution:

```sh
git clone https://github.com/arminbiere/cadical.git /absolute/tools/cadical
git -C /absolute/tools/cadical checkout 146207318796f094dcded87349a64f0c6927309e
cd /absolute/tools/cadical
./configure
make -j4
```

For DRAT-trim use
[the official source](https://github.com/marijnheule/drat-trim), commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, compiled with
`cc -O2 -o drat-trim drat-trim.c`. Tool source and binary provenance is in
`TOOLCHAIN.json`. No Python SAT library is required for the certified run.

Generate, independently ground and certify every case (fresh output path):

```sh
python3 -B ramsey_r55_mixed_q7_elimination/certify.py \
  /absolute/data/r44_15.g6 /absolute/proofs \
  /absolute/tools/cadical/build/cadical /absolute/tools/drat-trim/drat-trim \
  --workers 4
```

This command requires all 640 solver outputs to be UNSAT and every
DRAT check to print `s VERIFIED` with exit code zero. UNKNOWN, a timeout,
a missing proof or a failed check aborts. It writes fresh per-case CNFs,
ASCII traces, logs, hashes and expected summaries. No old run is resumed.

For the pinned archived traces, replay all proofs and mathematical controls:

```sh
python3 -O -B ramsey_r55_mixed_q7_elimination/reproduce.py \
  /absolute/data /absolute/replay \
  --proof-directory /absolute/proofs \
  --drat-trim /absolute/tools/drat-trim/drat-trim
```

The expected status is `COMPLETE_640_PROOF_AND_CONTROL_REPLAY_VERIFIED`.
This replay invokes no SAT solver and checks both saved hashes and proofs.
Compiler/platform changes can alter a newly generated valid proof. Such a
run is mathematically certified by `certify.py`, but is not a byte-identical
replay of the original trace manifest; do not silently replace that manifest.

Omitting the two proof options runs only the compact controls and reports
`COMPACT_CONTROLS_VERIFIED_NOT_UNSAT_REPLAY`. It does not reestablish the
UNSAT portion from hashes alone.

## Scope and next boundary

The complete residual q7 stratum is now all red. If a good43 admits no
red-maximal q>=8 representative, every maximal red-K4 packing has exactly
seven blocks and every uncovered fifteen-set is Ramsey(4,4). The proof
records this exact obstruction and its two-color version when the total
monochromatic packing number is seven. It is not yet excluded.

No historical order-5 automorphism exclusion, symmetric good43 search,
sampled carrier, or parked historical computation is used. This package
changes a complete covering family and preserves every earlier artifact.
