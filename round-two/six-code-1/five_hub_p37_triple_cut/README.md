# Conditional P37 five-hub triple cut

Actual author six-code-1, researcher. Assuming71 five-subsets of18 with
intersections at most2 and profile19^5,20^13, hub-pair total37 forces
one or two covered hub triples. No word contains four hubs. The new
actual HH population cap and disjoint column arguments are in
[PROOF.md](PROOF.md); hypotheses, prior credit and trust boundaries are explicit.
P37/T1/2 and the unrestricted69..71 gap remain open. External review is pending.

Use Python3.11 with its standard library, from a full repository checkout:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 round-two/six-code-1/five_hub_p37_triple_cut/verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -O round-two/six-code-1/five_hub_p37_triple_cut/verify.py
```

Run serially with one native thread. Each coefficient and column branch
retains its fixed100,000-state/10-second guard; the reproducible wrapper
limit is30 seconds per complete replay. A failure or timeout is incomplete,
not mathematical nonexistence. No solver or network is used by the proof
program. The shared parent three files and their exact commit/hashes are
listed in [DEPENDENCIES.json](DEPENDENCIES.json); sparse checkouts must include
`round-two/six-code-1/five_hub_pair_total36`.

Both engines compare all92 cases,4,393 full51-entry count vectors and every
certificate. The compact [EXPECTED.json](EXPECTED.json) preserves branch
counts, the two actual residues, positive ordered-column controls and the
WHOLE regenerated record checksum. [FIRST_SEAL.json](FIRST_SEAL.json) records
source frozen before the first packaged output; [VALIDATION.json](VALIDATION.json)
records cold normal/optimized runs, time and memory. A first prototype's
outputs were visible before packaging; this is not a blind or external review.
Source-first publication is separate from proof status. Large private output
corpora and the paused broader census are neither shipped nor premises.
