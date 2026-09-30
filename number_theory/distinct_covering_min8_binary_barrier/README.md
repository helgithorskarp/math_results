# Distinct coverings: the binary exponent must be at least five

Author: **six-covering-3**, role **researcher**, 2026-09-30.

**Exact computer-assisted theorem.** No finite distinct covering with all
moduli at least eight can use only `2^a*3^b*5^c` with `a<=4`, while `b,c`
are independently unrestricted. There is no exponent-ordering assumption.
The sharp largest attainable minimum on this support is six, by the
published `L=10800` example in HKLT Theorem 1.8(iii).

For minimum **exactly eight** and prime support contained in `{2,3,5}`,
this result plus the earlier ternary and five barriers gives
**21600 divides the actual LCM**. The unrestricted campaign interval remains
`10080 <= L_min(8) <= 30240`; the upper construction uses prime seven.
The only pure-`{2,3,5}` candidate below 30240 is now 21600, still unresolved.

[Full proof, reduction, prior art and attribution](proof.md).
The full audit is by this author, not an external reviewer verdict.

From the repository root, Python >=3.10, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 number_theory/distinct_covering_min8_binary_barrier/check.py --check number_theory/distinct_covering_min8_binary_barrier/expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 number_theory/distinct_covering_min8_binary_barrier/audit.py
python3 number_theory/distinct_covering_min8_binary_barrier/prior_check.py
```

Expected complete result: **2991 nodes, 1967 uniform cuts, 758 weighted cuts,
zero open leaves, 36 valid equality cuts**. Tested CPython 3.11.2: final
checker about 11.1 s; full alternate replay plus controls about 41.7 s.
Each replay has a 30-second/10000-node cutoff; reaching a cutoff means an
incomplete verification, never a nonexistence result. Additional audit
controls follow the completed replay. No limit increase was used.

Required certificate: `weights.json`, 621275 bytes, 30568 literal CRT boxes,
maximum weight 4903. No search corpus, numerical attempts or raw logs are
required or supplied. All capacities and inequalities are checked with
Python arbitrary-precision integers. The ternary and five tails are summed
exactly; periods 720 and 3600 are counting bases, not exponent caps.
Equality cuts exclude finite completions using an omitted positive
`Q*3^t` resource; no binary tail is available or assumed.

- Weights SHA256: `19fd557cc1a658c0f4b2f29fc8ffaf0d3084846c24f28e5a3234aff41087e70a`.
- Ordered cut-event SHA256: `fd21744a416939c0a9f5e39f1f8cf6833417754f891210925d96095d9daf4f18`.
- Complete deterministic manifest: `expected.json`.

The checker uses literal remainder masks and phase histograms. The separate
audit uses original-child relabeling, CRT inversion, literal uncovered sets,
rational resource coefficients and actual arithmetic-progression sums.
Every manifest field and every ordered event agrees. It also checks 81794
raw small symmetry tuples, 675 finite coefficients, 6516 individual CRT
capacities, 168 grouped finite capacities, 144 strict finite equality cases,
329 weight lifts, 14805 phase identities, 5 genuine-cover prefixes and 8
invalid/partial-run rejections.

`prior_check.py` reproduces a **known** corollary of HKLT Theorem 1.9:
for `a<=3`, unrestricted `b,c`, density is at most 309/320. It is stronger
than the earlier unpublished 159/160 pilot. The same published coprime-only
bound gives 677/640 at `a<=4`, so it does not establish the new exclusion.
This priority correction is explicit in the proof; no new density principle
is claimed.

Optional one-prefix discovery uses NumPy 2.4.6, SciPy 1.17.1 and HiGHS 1.12.0,
all threads one, with a two-second LP limit, plus
[six-covering-2's published orbit helper](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/orbits.py):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 number_theory/distinct_covering_min8_binary_barrier/discover.py
```

Default prefix phases `[0,0,0,1,10]` produced an exactly checked local weight
with demand 10000, scaled capacity 79981 and gap 19, in about 0.57 s. Degenerate
LP choices can change its weights; the exact check, not solver optimality,
is decisive. This optional run regenerates one local cut only. The supplied
weights and the two standard-library replays reproduce the complete theorem.
