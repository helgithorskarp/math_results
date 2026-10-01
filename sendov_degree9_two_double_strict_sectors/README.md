# Eleven strict two-double sectors and the remaining four-section frontier

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Ordinary written author proof, unformalized; independent review pending.

[PROOF.md](PROOF.md) proves J<=785753/1000<J* on all eleven closed
nonadjacent ordered sections of the six-level2+2+1^4 multiplicity cohort,
including reflection, permutation and every collision boundary. There is
a uniform gap J*-J>1/1250 and the conservative unit-direction bound
dist^2<=5000(J*-J). The scalar optimum and equality orbit are credited.
Combined with the [whole one-triple theorem](../sendov_degree9_one_triple_six_level_displacement/PROOF.md),
this enlarges the established angular domain and reduces possible
six-level J>=J* profiles to the four doubled-rank sections
(1,5),(1,6),(2,5),(2,6). They, seven/eight-level optimization and
unrestricted first power remain unresolved here.

A uniform transportation cover has39 complete simplices and81 section
vertices. All **583050** degree22 target coefficients are nonnegative,
with962 zeros; **234** full defining-matrix controls supplement the
complete coefficient reduction. The complete mathematical record has
610619 checks and canonical SHA256

    cf1111b7a91e60a092d89cd7feb96c6ac36e3496484db5338f08c11f47770656

The complete mandatory fixture expected.json is a compact361824-byte
record of literal vertices, exact defining controls and coefficient
hashes. All coefficients are regenerated from root forms; no raw
coefficient corpus is supplied or required. Hashes summarize after
complete regeneration and comparison, not in place of those operations.
[LITERATURE.md](LITERATURE.md) records precise inputs and review boundaries.

## Bounded reproduction

CPython3.11.2 standard library only. Keep both contribution directories
in the same clone. `cover.py` openly adapts and imports the prior public
one-triple arithmetic backend from its sibling directory; that executable
must have SHA256

    84db02a4d866aa94d400481e19ea84679c4e8d09e9de6085594e96a9aee6d2dd

The import is pinned and public. No private module, network proof input,
solver or floating arithmetic is used. Updating that dependency requires
explicit new verification; a mismatch stops before mathematical work.

From this directory, run the following finite sequential verification.
Each selected job regenerates its entire kernel, all14950 signs, all six
defining controls and the entire common geometry before comparison.
The timeout is an operational cap, not a mathematical exclusion.

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -I -B - <<'PY'
import json, subprocess, sys
from pathlib import Path
fixture=json.loads(Path('expected.json').read_text())['record']
for mode in ('normal','optimized'):
    directory=Path('case-replays')/mode
    directory.mkdir(parents=True,exist_ok=True)
    flags=['-I','-B']+(['-O'] if mode=='optimized' else [])
    outputs=[]
    for row in fixture['cases']:
        r,s=row['pair'];i=row['cell'];key=f'{r},{s}:{i}'
        output=directory/f'{r}-{s}-{i}.json'
        subprocess.run([sys.executable,*flags,'verify.py','--case',key,
                        '--write-case',str(output)],check=True,timeout=60)
        outputs.append(str(output))
    subprocess.run([sys.executable,*flags,'verify.py','--collect-cases',
                    *outputs,'--test-manifest-rejections'],check=True,timeout=60)
PY
```

A selected run reports **PASS_CASE only**,14950 coefficient entries,
six defining controls, a full case SHA256 and its mathematical check count.
No one selected case proves the whole39-cell statement. All39 successful
fresh cases plus the complete record gate are required in each mode.

The collector reports **PASS_RECORD_UNION**,583050 coefficient entries,
234 controls,39 kernels,11 sections,81 vertices,610619 mathematical checks,
the above complete record SHA256, and five rejected fixtures. It checks
every full case and common record,39 unique intended cases, same declared
source/fixture hashes and full assembled equality. It **does not regenerate
the cases or authenticate externally supplied records**. Record-union
success alone is insufficient evidence of fresh mathematical verification.

`--manifest PATH` selects another mandatory full fixture. Missing or
damaged fixtures reject explicitly under normal and optimized Python.
The five controls cover absence, changed coefficient digest, changed
physical vertex, changed defining Psi and incomplete cell coverage;
damaged fixture hashes are recomputed to exercise the actual comparison.

Exact integers/Fraction and the full coefficient cover provide the
computational certificate. Transportation coverage, projection, Rolle,
spectral-cluster continuity and credited scalar/one-triple results are
ordinary written proof, outside a formal kernel. Defining-matrix controls
are alternate author representations, not independent peer review.

## Author validation provenance

All39 normal author discovery pilots passed under separate60s caps before
building the complete fixture. They are generation evidence, not a
fixture-comparison verdict. The publication verifier then freshly rebuilt
all39 cases in both normal and optimized execution: **78 passed runs**.
Every entire payload agrees across modes. Both complete record unions
passed231 gates and all five missing/damaged fixtures rejected per mode,
for ten rejection controls. The mathematical record is unchanged.

Total selected-run time was589.804 seconds normal and620.834 seconds
optimized; the longest case was37.794 seconds, below its60s cap, and
largest child RSS was40852KiB. One mathematical child ran at a time,
all native/BLAS/OpenMP threads1, unchanged1CPU2GiB128tasks. One overly
broad read-only graph refresh hit its separate60s limit and was stopped;
no mathematical case timed out and no resource limits were increased.
The three executable/fixture files were frozen throughout all fresh
source runs. The collector audits supplied records and is not itself
fresh regeneration or independent review. No aggregate long run is
required or claimed.
