# Exact full-source J74 receiving rectangle

six-rupert-2, researcher. The receiving domain is the ENTIRE CLOSED raw
rectangle of halfwidth 1/1000 about
`((101sqrt(5)-183)/58,(329-109sqrt(5))/58,-1)`, normalized to both unit
normal orientations. It is not a unit-normal chord radius of 1/1000.

[PROOF.md](PROOF.md) states the complete physical quantifiers and explains
the geometric bridges. Every proper source rotation, every original
receiving-plane translation, all scales at least one, every receiving
boundary and every source half-turn are retained. The conclusion is
closed-fit equality in exactly twelve named proper motions. Global J74
Rupert property remains **OPEN**. Author checking is unformalized and
independently unreviewed.

## Dependencies and finite proof inputs

Use Python 3.11 or newer with its standard library only. No NumPy, solver,
network call, private store or floating-point sign is used by the exact
checker. Run from a checkout of the authorized source repository retaining
the adjacent `full_source_cap` directory and the original J74 model.
[DEPENDENCIES.json](DEPENDENCIES.json) checks six inherited source hashes
BEFORE their import. The original named body is the unit-edge model from
source `25fc9695745b6832d068d18544452b7852b5847f`; the parent contact
certificate is source `dc5c677266b22d09baafa372894dd6cfbf59d3b0`, LEMMA9345.

[certificate.json](certificate.json) supplies the compact dyadic forest,
actual original indices and stress indices. Its canonical SHA256 is

    56467904ce9c0daf031e8ed100ad01eb75b259691a3fd603d0fe472b1ccdaf54

The frozen exact forest has 8,925 source leaves: 8,848 joint cuts and
77 derived equality gates, in four full closed quaternion cubes. There
are 2,152,143 strict exact coefficient signs. [expected.json](expected.json)
contains fixed complete local, chunk and aggregate records. Every chunk
regenerates its coefficients from actual originals and emits exact
minima and the digest of its complete ordered coefficient stream.
These digests bind replay records; a digest alone is not a proof of its
coefficient signs.

## Sequential bounded reproduction

The following script runs the local bridge, independent conversion audits
and damaged controls, twelve contiguous full chunks, and complete journal
assembly. It repeats the same sequence with Python optimization and
compares EVERY entire output byte for byte. Child jobs run sequentially,
with numerical threads set to one and a 130-second guard. Use a machine
with the tested performance stated in [VALIDATION.json](VALIDATION.json);
a timeout establishes no mathematical conclusion. Do not increase campaign
resource limits to evade a timeout.

From the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
import os, subprocess, sys

checker = Path('round-two/six-rupert-2/full_source_rectangle/check.py')
env = dict(os.environ)
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
            'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    env[key] = '1'
base = Path('scratch/j74-rectangle-reproduction')
for optimized in (False, True):
    mode = 'optimized' if optimized else 'normal'
    journal = base / mode
    journal.mkdir(parents=True, exist_ok=True)
    tasks = [('local', ['--local']), ('controls', ['--self-test'])]
    tasks += [(f'chunk-{i:02d}', ['--chunk', str(i)]) for i in range(12)]
    tasks += [('aggregate', ['--aggregate', str(journal)])]
    for label, args in tasks:
        command = [sys.executable] + (['-O'] if optimized else [])
        command += [str(checker)] + args
        result = subprocess.run(command, env=env, capture_output=True,
                                check=True, timeout=130)
        target = journal / (label + '.json')
        target.write_bytes(result.stdout)
        if optimized and result.stdout != (base / 'normal' / target.name).read_bytes():
            raise RuntimeError('ordinary/optimized record mismatch: ' + label)
        print(mode, label, 'passed', flush=True)
PY
```

For a single full chunk, use `python3 check.py --chunk N` from this
directory, where N is 0 through 11. `--local --print-record` emits the
entire exact local weight/error record, whose canonical digest is also
checked. A profile such as `--chunk 0 --profile-leaves 128` is explicitly
partial and cannot be assembled into the theorem.

`--aggregate JOURNAL` checks the complete local record and all twelve
fixed, contiguous, nonpartial chunk records. It does not replay absent
coefficients or manufacture missing evidence. The whole continuum result
uses their actual exact executions AND the ordinary argument in PROOF.md.
`--no-expected` is an author-development option; it does not relax exact
geometry, positivity or cover gates, and it does not rewrite the fixed
expected records.

## Scope and remaining work

The raw rectangle contains an entire CLOSED projective unit-normal
chord cap of radius 1/9000 about the normalized center, by the ordinary
ratio bound in PROOF.md. Thus it strictly extends the entire earlier
radius-10^-9 projective chord cap. No optimal inscribed radius is claimed.
Its receiving normals remain more than 1/3 in
projective unit-normal chord from all six minimum-area axes. The four
partial-shadow branches in the six-member base inventory remain
legitimate, alongside their proper moving companions.

The floating discovery program proposed only covering paths and actual
labels. No floating discovery output is accepted as a mathematical
bound. Generated journals and the multi-million-coefficient data stay
in local scratch; the compact public source independently regenerates
every exact sign. The next frontier is continuation toward an actual
receiver support-phase wall or classification of an adjacent phase.
No global named-solid non-Rupert proof or exact passage is claimed.
