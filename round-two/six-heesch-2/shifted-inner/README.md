# Shifted inner-network obstruction

Agent **six-heesch-2**, role **researcher**. A connected prototype containing
the origin, from an explicit 199-cell pool, cannot make two complete coronas
on the S17 network with doubled translations and independent zero-or-unit
translation shifts. The designated copy counts are 1,5,11; orientations
remain fixed. [proof.md](proof.md) states the exact scope and encoding.

The source is compact. Reproduction generates a bounded SAT proof, checks
every addition with a solver-independent native reader, and freshly replays
its dependency subset. The large traces are temporary rather than vendored.
The original [seed fixture](../seed.json), [geometry](../geometry.py) and
[definition checker](../check_geometry.py) are dependencies in the same
repository. The initial instance is also reconstructed through inverse poses.

Tested with CPython 3.11.2, python-sat 1.8.dev24 / Glucose4 and
GNU g++ 12.2.0, C++17. With the package installed in a local environment:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 round-two/six-heesch-2/shifted-inner/verify.py
```

The reader compiles its C++ checker and keeps temporary outputs in the ignored
local `scratch/` directory. `expected.json` pins the canonical input and the
positive seed control. The original full proof audit uses 30 MiB; the positive
control, input reconstruction, bounded solve and two release audits fit one
CPU and two GiB. An incomplete solve or audit aborts without an exclusion.

For sanitizer coverage of the native controls:

```sh
g++ -std=c++17 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer \
  round-two/six-heesch-2/shifted-inner/rup_audit.cpp -o /tmp/heesch-rup-check
/tmp/heesch-rup-check --self-test
```

Other placements and prototype cells outside the pool are outside this result.
No Heesch record or finite-five shape is claimed.
