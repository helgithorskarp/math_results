# P17 interior lattice rigidity

**six-heesch-1, researcher.** A certified phase obstruction proves that two
contacting P17 copies which are both surrounded must have an integer relative
translation. Thus every prefix through `H-1` in a strict `H`-corona packing is
on the root's integer grid. Two coronas suffice for first-prefix integrality;
the earlier campaign proof required three. See [proof.md](proof.md).

For the relaxed final `Hh` convention, only the last layer needs fractional
translations, and a half-grid last layer suffices at every depth. This does
not establish a new exact Heesch number or a fourth/fifth-corona construction.

P17 is entry **43**, zero-based, in Kaplan's
[primary seventeen-cell file](https://cs.uwaterloo.ca/~csk/heesch/omino/17omino_2up.txt),
reported `Hc=Hh=3`. The previous “record seed” label was incorrect and is
corrected in the preceding finite-contact documentation. The prior all-motion
four-corona frontier remains `3<=Hc<=Hh<=4` until the last continuation is decided.

The complete phase census has 704 contacts, 352 floating contacts, and exactly
11 floating first supports. Reciprocal support leaves one self-reciprocal
pair. A three-pixel quarter-grid cover obstruction excludes that pair.
The support proof has 592 RUP additions; the pair proof has two. Positive
witnesses and every negative exclusion are checked without a SAT solver.

## Reproduce

From repository root, standard-library CPython 3.11:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 round-two/six-heesch-1/p17-interior-integrality/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O round-two/six-heesch-1/p17-interior-integrality/check.py
```

Both outputs equal [expected.json](expected.json). Five implementation files
from [finite-contact-types](../finite-contact-types/README.md) are byte-pinned
in [dependencies.json](dependencies.json). No external input is needed.
The new reader independently reconstructs both candidate pools by bounded
rectangle enumeration and checks all full-footprint conflicts and RUP steps.

Optional regeneration uses `python-sat==1.8.dev24` and single-threaded Glucose4:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 round-two/six-heesch-1/p17-interior-integrality/generate.py
```

It overwrites only compact local fixtures and traces, and rejects UNKNOWN,
conflict-budget exhaustion, candidate limits and proof-size guards. Deletion
records are omitted soundly before RUP checking; every retained addition is
verified. A first run stopped at the raw proof-size guard. Filtering deletion
records completed the certification without changing resource settings.

The written motion bridges and shared CNF/isometry primitives remain
unformalized trust boundaries. This is author validation, not an independent
peer-review verdict or a historical priority claim.
