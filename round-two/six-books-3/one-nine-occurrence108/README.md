# One-nine roots at 108 edges

Actual author: six-books-3, researcher. See [PROOF.md](PROOF.md) for the
ordinary parity proof and the exact import boundary.

Every valid rootless graph of degree multiset `9^4,10^18` has at least two
one-nine roots. With independent degree-nine lows its type counts obey
`n3+3*n4>=2`. This removes the entire singleton-free independent-low
exception and also the exactly-one-singleton case. Combining published9102
rootlessness with the credited three-low count forces at least two
one-nine roots in every valid108-edge host. This is a structural reduction;
R(B4,B7) remains between22 and23 in the located primary literature.

Python3.12.14, standard library only. From this directory:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 check.py --expected expected.json
python3 -O check.py --expected expected.json
python3 independent.py --expected expected.json
python3 -O independent.py --expected expected.json
python3 check.py --self-test
python3 -O check.py --self-test
python3 independent.py --self-test
python3 -O independent.py --self-test
```

Run all commands serially with all native thread settings at one. The
programs enumerate all labeled simple graphs of orders1..6 for exact
endpoint identity controls, independently check every low-count profile,
and evaluate degree-correct but invalid22-point fixtures. These are checks
of the ordinary proof's identities, not a22-vertex host search. The theorem
requires the written parity/nonnegativity bridge and the stated imported
rootlessness result. Both programs were written by the same author.

The small primary21 fixture is the authors' known93-edge construction;
off-diagonal zeros are red. No network, external graph catalogue or solver
is needed for reproduction. `controls.json` uses red-neighborhood masks,
bits0..21, one mask per vertex, with low vertices0..3. It deliberately
contains no valid22-point witness. `expected.json` is frozen deterministic
evidence, `provenance.json` gives credits, and `manifest.json` gives file
sizes/hashes. No generated corpus or private operational data is published.
