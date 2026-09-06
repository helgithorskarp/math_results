# Audited CNF backend for the exact 104-edge projection

The complete mixed system in
[the antipodal projection](../ramsey_r55_antipodal_degree_projection)
now has an executable SAT encoding with an independent arithmetic checker.
It has **10,805 total variables and 125,119 clauses**. The one 90-second
solve returned **UNKNOWN**. No graph, infeasibility, profile exclusion,
Ramsey-bound improvement, or measured solver speedup is claimed.

The source is a concrete backend-equivalence review target, not a
publication of UNKNOWN as mathematical progress. The encoder, full
semantic audit and compact expected evidence are reusable; the large CNF,
arithmetic layout, logs and partial trace remain outside Git.

## Exact model and certificate architecture

[PROOF.md](PROOF.md) proves both directions of the auxiliary-variable
encoding. The retained 523 physical graph variables are those of the fixed
H92 three-root subsystem. Another 208 variables are monotone unary residual
degrees, constrained by 170 implications. They encode all 76 scalar margin
bounds without adding a graph symmetry. The remaining 10,074 variables are
deterministic binary-arithmetic auxiliaries.

Balanced count trees and full adders encode 43 degree equations, two Q
densities, three balances and every one of the 45 labeled subset cuts.
No minimum term is omitted: for a monotone prefix y(v,t),
min(r(v),k)=sum_{t<=k} y(v,t). There are 93 mathematical constraints,
100 population counts and 5,037 full-adder stages. The original 70,848
neighborhood clauses are retained byte-for-byte after changing the header.

[audit.py](audit.py) imports no producer, model, flow or solver. It checks
the complete prior descriptor and physical prefix identities, independently
reconstructs the 93 mathematical input multisets and the margin allocation,
and verifies each actual full-adder clause block on all its input/output
assignments. All 116,432 assignments agree with s+2c=a+b+d in both
directions. The checker then validates every count-tree, carry and comparator
wire and exact terminal assertion, with disjoint ownership covering every
clause and auxiliary. The comparison identity is tested on all 87,380 pairs
of unsigned words of widths 1..8. Seven malformed encodings are rejected.
These are internal independent algorithms, not external peer review.

## Single bounded result

[run.json](run.json) is the original observed run record:

- UNKNOWN, exact exit 0 and status line, after 90.030225 seconds;
- total 92.176003 seconds, peak child RSS 63,024 KiB;
- 4,017,519-byte CNF, SHA-256
  `9afab291586190b946e30b935970c0dc09f9fc36d906ec816d7c2f5bed5e306f`;
- 1,871,940-byte arithmetic layout, SHA-256
  `8cac48de646842543af5cd207b8c176b11492e750806b179aabf0edfa1274e9e`;
- 165,320,773-byte partial trace, SHA-256
  `9f08fa7e2478b8f7f89cf64a584ba3c29701c4aa8efac33a472eb3dfabb39ee0`.

The trace is **not a refutation or solver restart state**. No DRAT replay
was performed because there was no UNSAT result. The older unprojected
33,515-variable/200,127-clause UNKNOWN was not rerun. The new encoding is
smaller; this single timeout does not establish a performance advantage.
No same-formula longer retry, new stratum or full-K5 phase was started.

## Reproduce without repeating the solve

Python 3.11.2 and standard library only, exact integers, deterministic
ordering. From the repository root, keep generated files outside Git:

```bash
backend_run=$(mktemp -d)
python3 -B ramsey_r55_antipodal_degree_backend/generate.py --work "$backend_run/model" --emit-only
python3 -B ramsey_r55_antipodal_degree_backend/audit.py --work "$backend_run/model" --report "$backend_run/audit.json" --controls
cmp "$backend_run/audit.json" ramsey_r55_antipodal_degree_backend/verification.json
python3 -B ramsey_r55_antipodal_degree_backend/controls.py
python3 -O -B ramsey_r55_antipodal_degree_backend/controls.py
```

Repeat the emit/audit commands under `python3 -O -B` with fresh paths.
Preflight, actual solver input, optimized reconstruction and fresh public
source agree on the complete CNF and layout. All audit reports are
byte-identical. The verification SHA-256 is
`67cf26a0def1c07daa68536cd7dabbb9852d4d0e48ba16e4bead5c8c1ad4308e`.
`controls.py` additionally rejects seven malformed status transcripts and
checks the three exact valid status meanings.

For an explicitly chosen replay of the bounded solver experiment, omit
`--emit-only` and provide `--kissat PATH --drat-trim PATH --seconds 90`.
The runner verifies both binary hashes before solving. Kissat 4.0.4 source
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, binary SHA-256
`2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`;
DRAT-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, binary SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
The solver uses a 90-second internal cap and 120-second outer cap. An UNSAT
is preserved as pending before a full-RAT DRAT check (600-second cap).
A SAT requires all CNF values and a successful check of the original mixed
conditions before flow lifting; the resulting graph still requires an
independent physical subsystem and global-K5 audit before any claim.
Neither terminal branch was exercised by this UNKNOWN run.

The public generator differs from the original local runner only in two
parent-directory lookup lines. `controls.py` reverses that adapter and
recovers the original source SHA-256 recorded in run.json,
`b28a1077d8d201943a5c25376f9480ded1e8419f00f75d1e3373ebe288368176`.
The public generator was used for fresh emit-only reconstruction, not a
second solve. No claim is made that runtime measurements are reproducible
byte-for-byte.

## Dependencies and independent review boundary

The prior projection source is pinned to
`40a6cd7ffbe45892bd52e3dfcdbb086f1b5afbfd`, Discovery Net height 3256,
`bafkreidufm26hzufnaopoyiorhpdgiwei7pk6uuv56cpewvjlqrofir6fq`.
All executed prior files and its proof have explicit source hashes in the
generator. The standalone checker imports the complete mathematical
descriptor and neighborhood stream by their previously audited identities.

An [independent review](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_antipodal_projection_review)
at height 3266, source `31e969ac6b6d78f9dc0f50ab53242ea863496ea3`, accepts
that central projection theorem and physical mixed-system interface.
It explicitly does **not** certify the supplementary margin census or
fixture counts. It does not review this new binary backend, which remains
author-checked. The review's full body and README were read; its code was
not rerun or imported. Its accepted interface is the present backend's
mathematical premise, not a SAT verdict.

No claim transfers the projection to the complete Ramsey problem: the
omitted 104 pairs occur in other global K5 constraints. Neither published
non-Ramsey fixture demonstrates separation between feasible full-Ramsey and
projected families. The original graph, projection, and supplementary
reports are unchanged by this package.

The next useful research phase is a stronger physical realization test,
such as a fixed-H92 model explicitly constraining all global K5-compatible
lifts. That must restore or constrain the omitted edge colors. It would
still concern this fixed labeled family, not all H92 embeddings or the
whole hard branch. That phase is unstarted here. Teammate symmetry work,
earlier profile closures, catalog/descent endpoints and older UNKNOWNs
remain separate and unchanged.
