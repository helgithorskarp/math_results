# H7: a minority run of six forces six runs

**six-vdw-2, researcher.** In an H7-invariant punctured-field AP7-free coloring over
F617, at phase weight 11 or 33 a longest minority run of six forces the profile
(6,1,1,1,1,1). All 120 normalized five-run cases have strict refutations.
See [PROOF.md](PROOF.md) for definitions, lossless reductions and limitations.
The 1,876 remaining necessary normalized six-run phases per background are not
excluded. This gives no phase-endpoint, whole-H7, or numerical W(2,7) bound.
Independent-person review is pending.

Use Python 3.11+ with python-sat 1.8.dev24 / CaDiCaL 1.9.5 and a locally built
drat-trim whose source SHA256 is
d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee
(upstream commit 2e3b2dc0ecf938addbd779d42877b6ed69d9a985).
From this directory in a repository checkout:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python reproduce.py --work /tmp/h7-run6-five-runs-fresh --converter /path/to/drat-trim
```

The work path must be unused. Generation uses twenty disjoint six-case batches,
and definitions use twenty independent six-case batches in each Python mode.
The driver checks the entire actual field, signed CNFs, metadata, phase/scalar
coverage and 83 damage controls per mode before checking all certificates twice.
Expected status is EXACT_H7_ELEVEN_LONGEST_SIX_FORCES_SIX_RUNS, with
154289 additions, 5469674 deletions and 1203622 hints per mode.
All children have the fixed caps in PROOF.md. A timeout, UNKNOWN or incomplete
enumeration gives no exclusion; failed inputs are not automatically retried.

If a completed directory holds candidate LRAT files for the EXPECTED.csv stems,
add `--certificate-cache /path/to/candidates`. This avoids new native proposals
while retaining all source, model, definition, damage and strict certificate checks.
Every cached candidate is untrusted and bound to the freshly reconstructed CNF.
This source reconstruction has 305 bounded child stages.

EXPECTED.csv pins all 120 complete model and certificate hashes and exact counts.
VERIFICATION.json pins the canonical whole mathematical audit by SHA256 rather
than publishing a redundant record corpus. SOURCE_PINS.json and SHA256SUMS bind
all source before mathematical imports. Generated corpora are omitted and ignored.
Portable replay needs only the eight listed published physical helper and premise
or context files; it uses no campaign, signer, account or ledger. The ordinary proof
bridges and imports remain unformalized. Author checking and source replay do not
constitute independent-person review or a historical-priority claim.
