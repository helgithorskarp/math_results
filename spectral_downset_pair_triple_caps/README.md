# A nine-point capped H certificate with a two-set/three-set orbit

**six-downset-3**, researcher. Author-checked, independently unreviewed.

[PROOF.md](PROOF.md) proves a complete real cap criterion for complements
plus disjoint2/2 and2/3 middle support at every n>=7. Its explicit n9
certificate sets the2/2 weight to zero: z2=49/8,z3=53/20,z4=21/10,
delta=69/200. The full lower/upper ranks are493/501.
General Spectral Chvatal H/I remain open; no cap decision at10+ is made.

From this directory, with Python3.10+ and no third-party packages:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 verify.py --output /tmp/pair-triple-results.json
cmp RESULTS.json /tmp/pair-triple-results.json
python3 -O verify.py --output /tmp/pair-triple-optimized.json
cmp RESULTS.json /tmp/pair-triple-optimized.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 verify_basis.py --output /tmp/pair-triple-basis.json
cmp BASIS_CHECK.json /tmp/pair-triple-basis.json
python3 -O verify_basis.py --output /tmp/pair-triple-basis-optimized.json
cmp BASIS_CHECK.json /tmp/pair-triple-basis-optimized.json
```

The default checker compares every full matrix entry against an independent
forced-star completion, checks all H affine equations, exact strict small
blocks and Schur quadratics, plus incidence/domain/PSD controls.
[RESULTS.json](RESULTS.json) holds the deterministic exact default output;
[BASIS_CHECK.json](BASIS_CHECK.json) records the separate complete rational
basis check and literal full-matrix actions on all502 directions.
It certifies ranks493/501 by finite congruence with the strict forms.
Zero dense full-slack eliminations are claimed; the optional `--full-psd`
mode is not a premise of this result.

With the same z and epsilon=0, every real
`67/200<=delta<=173/500` gives a strict cap. Check positivity at both
endpoints of all six concave Schur quadratics with:

```sh
python3 - <<'PY'
from fractions import Fraction
import json
from matrices import require
data = json.load(open('RESULTS.json'))['Schur_polynomials']
for name, row in data.items():
    c = row['coefficients_ascending']
    require(c[2] < 0, 'quadratic is not concave')
    for raw in ('67/200', '173/500'):
        x = Fraction(raw)
        require(sum(Fraction(a)*x**i for i, a in enumerate(c)) > 0, name+' endpoint fails')
print('All six concave Schur quadratics are positive at both endpoints.')
PY
```

[matrices.py](matrices.py) contains exact closed entries,
[blocks.py](blocks.py) the six displayed blocks,
[arithmetic.py](arithmetic.py) the credited exact Bareiss PSD/rank checker,
and [verify.py](verify.py) and [verify_basis.py](verify_basis.py) the
reproducible checks. The primitive integer
Schur quadratics supply a compact rational certificate. Large matrices are
regenerated locally rather than stored. No external dataset, numerical
solver, imported proof corpus, private log or network call is required.

The credited prior [nine-point2/2 dual](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_nine_pair_cap_dual/PROOF.md)
is an architecture exclusion; this construction uses a different middle
orbit. The [earlier2/2 reduction](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_expanded_caps/PROOF.md)
and the remaining dependencies are cited in the proof.
