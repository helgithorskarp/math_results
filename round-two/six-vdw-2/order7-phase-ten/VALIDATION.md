# Completed exact validation

**six-vdw-2, researcher; 2026-10-02.** Separate author algorithms;
independent review and proof-assistant formalization are unclaimed.

All 24 retained initial native proposals and conversions passed the
unchanged 50000-conflict/30-second native and 25-second internal/
30-second external converter guards. The highest retained conflict
count was 43011. Every actual CNF definition and proposed positive-RUP
certificate was checked in both Python modes before packaging.

The complete compact source then regenerated every canonical model and
strictly replayed candidate CNF/LRAT bytes in normal and optimized Python.
This used `reproduce.py --certificate-cache`, not trusted cached acceptance
flags. The default command proposes fresh proofs on the same canonical
CNFs. The completed compact replay took **107.670 seconds** with peak
parent/child RSS **25772/72148 KiB**, serial with every thread fixed to one.

```json
{
  "status": "EXACT_H7_PHASE_ENDPOINTS_9_35_EXCLUDED",
  "endpoint_phase_weights_excluded": [9, 35],
  "nonconstant_phase_band": [10, 34],
  "agreement_point_range": [140, 476],
  "total_checked_additions": 400568,
  "total_hints": 6672402,
  "all_proof_bytes_reproduced": true,
  "global_W_bound": false,
  "whole_H7_exclusion": false
}
```

All canonical CNF bytes, expected proof bytes and expected counts
reproduced. The 24-row [EXPECTED.csv](EXPECTED.csv) has SHA256
`7c49b367048be2c93820492959705600b82b3e5b8c416b3089be4e1039cb1c20`.
Hashes/counts are reproduction aids, not the mathematical proof. The
auditors compare whole clause multisets with actual field arithmetic,
and the strict kernel checks every live propagation hint and the empty
conclusion. Both complete Python-mode results agree.

The exact-seven close and majority controls each check 181244 small
prefix-threshold cells and 4092 signed exact-count inputs. The exact-six
following-minority controls check 172540 cells and 4092 inputs. The
independent length-five deficit census covers 39294 rooted sum35/max5
profiles, of which 20952 have minimum at most one; the directed successor
bound three leaves zero. The written disjoint-pairing argument proves
the exclusion without relying only on this census.

Twenty damages reject in **13.943 seconds**, peak parent/child RSS
**20504/66456 KiB**. For each Python mode:

- Omitted distance-three background, maximum-seven background,
  length-six next-minority7 background and length-five next-minority10
  background are rejected as incomplete required coverage.
- Flipped exact-seven/exact-six final units reject by counter semantics,
  even when their recorded CNF digest is repaired.
- Weakening the directed successor bound from three to four rejects
  in the independent gap census; the looser numerical condition admits
  the explicitly checked positive-control tuple.
- An altered imported helper rejects by its source pin before execution.
- Unsupported empty conclusions and missing live hints reject.

Two valid tiny RUP refutations provide positive controls. These checks
supplement the general normalization, prefix induction and pairing
arguments. They are not independent-author audits.

The earlier unsplit maximum-six b=0 model returned UNKNOWN at 50000
conflicts and was stopped. It gives no exclusion and was not retried
or given larger limits. The different following-minority reduction
supplies complete positive evidence. A private full 32-certificate
direct cover also passed; its eight extra length-five branches are
unnecessary for the published pairing proof and are omitted.

Large models, proof traces, native logs and exploratory corpora stay
outside Git and regenerate from source. The interval 3704 target,
remaining nonconstant phases 10..34, full H7 classification and
unrestricted W(2,7) remain unresolved.
