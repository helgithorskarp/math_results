# Independent all-cube private-triangle audit

Reviewer **six-reviewer-4**, independent mathematical reviewer. Confirms
LEMMA10111/0 at all integer n>=3,h>=2, preserving all original vertices and
empty loop. Read `REVIEW.md` for scope and `PROOF.md` for the complete ordinary
proof. The written target was exposed; the target's executable, arithmetic,
certificate, expected record and controls were never opened. This packet uses
fresh independent source, with no producer-module or prior reviewer arithmetic
import. Shared model/Python/machine/key infrastructure is disclosed.

The portable replay uses CPython3.11+ standard library only. It checks the entire
coefficient certificate and all original N40/N52/N56 matrix/frame/principal
fixtures. Certificate generation additionally needs SymPy1.14.0/mpmath1.3.0,
using a workspace virtual environment; generation is optional for verification.

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
python3 -B verify.py --manifest --check EXPECTED.json
python3 -B -O verify.py --manifest --check EXPECTED.json
python3 -B controls.py
python3 -B -O controls.py
```

Each mathematical child has a fixed30s guard; run each whole replay/control
phase under a fixed45s external guard. Children are serial, numerical threads
one, process scope1CPU/2GiB. Work stays in ignored `work/`. A timeout, kill,
UNKNOWN or incomplete calculation is never a mathematical verdict. Literal
n<=5/h<=3/N<=56 guards restrict the implementation controls, not the theorem.

`CERTIFICATE.json` retains eleven smaller exact blocks; the 3+2 even and
1+2+1 odd splits share a single trace block. The portable checker covers all66
original obligations through40 distinct entries,22 cross zeros and4 repeated
trace identities;18 pivots/21 updates,398 numerator and284 denominator positive
shifted coefficients. `rational.py` independently binds original rows and
metrics by exact coefficient identities, without CAS. `polycheck.py` verifies
every linked elimination and binomial shift using independent sparse Fraction
arithmetic. `literal.py` rebuilds every original set, physical Gram, full basis,
frame, empty lift, support, star, principal inverse and both repairs. Every
entire generated record must equal `EXPECTED.json`, not a selected digest.

Optional regeneration, with the pinned SymPy environment:

```sh
mkdir -p work
for block in mu alpha beta leaf standard even_old trace odd_old odd_mean old_plus old_minus; do
    python3 -B generate.py "$block" "work/$block.json"
done
python3 - <<'PY'
import json
from pathlib import Path
names='mu alpha beta leaf standard even_old trace odd_old odd_mean old_plus old_minus'.split()
data=[json.loads(Path('work',n+'.json').read_text()) for n in names]
raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
if raw!=Path('CERTIFICATE.json').read_bytes():
    raise ValueError('entire regenerated certificate mismatch')
PY
```

`INDEPENDENCE.json` seals11 primary files before subsequent source-only replay
and context updates. `VALIDATION.json` records whole normal/O and cold replay,
semantic failures, time guards and actual measurements. `MANIFEST.json` hashes
all final source files except itself; whole pinned/main source checks bind the
manifest externally. No native producer implementation is certified, no proof
assistant is used, and ordinary spanning/symmetry/spectral/Schur bridges remain
unformalized. The credited larger repair is independently validated for all
these cubes; no optimal endpoint or historical-priority claim is made.
