# Independent audit of the Tammes G20 four-bridge obstruction

Actual author: **six-reviewer-2**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms LEMMA9878's exact induced-triangle-tree
scope. [PROOF.md](PROOF.md) reconstructs the reduction and proves a
wider closed cosine band **[7/13,3/5]**, plus a finite algebraic exceptional
set with at most **219** values on 0<c<1. The full twelve-label G20 contacts,
both cross contacts, actual faces and all induced adjacencies are required.
The fifteen-point nine-profile corollary retains every physical hypothesis
of LEMMA9813; no optimizer occurrence, profile realizability or global
Tammes15 bound is asserted.

From this directory, **Python 3.12** and the standard library only:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
python3 -B check.py
python3 -B verify.py
python3 -B controls.py
python3 -B -O check.py
python3 -B -O verify.py
python3 -B -O controls.py
```

Run sequentially. The primary checker reconstructs all 576 placements,
all 3024 raw long candidates and the entire retained 432-case set,
7344 point norms, 12960 contacts, 93744 Gram numerators and both 1152
cross-gap polynomials. It checks all 576 explicit Bézout identities,
38 distinct monic witnesses and strict full Bernstein signs on both
closed intervals. `verify.py` regenerates the whole expected record and
uses 514 exact nodes to prove the 76 full Bernstein polynomial identities.
Its nodal equalities do not substitute sampled signs for rigorous bounds.
The primary controls and separate nodal damage test check the stated
failure modes.

The whole primary expected output, including its terminal LF, is
**41480 bytes**, SHA256
`7f50bbc1d5625851b89e27bc761c627dbd391099492844eb72209906ad91d367`.
[EXPECTED.json](EXPECTED.json) is the complete compact record. Witnesses
are sorted by their full SHA256 keys; each `bindings` entry is
`[type, sorted_bridge_faces, index_in_sorted_witness_keys]`. All u,v,F,G
coefficients are regenerated and checked; their entire stream has a
separate hash. No large geometric stream is a runtime input or published
artifact.

[INDEPENDENCE.json](INDEPENDENCE.json) seals six finalized primary files
before first target-native access. Defining written formulas/counts and
dependency proofs were visible, **not blind**. The producer's code and
certificate establish no primary proof step. The point called 3 in this
checker is the single fresh outside label; a late bijection maps it to
the producer's 13, without a G22 or special thirteenth-point premise.
[DEPENDENCIES.json](DEPENDENCIES.json) and [NATIVE_INPUTS.json](NATIVE_INPUTS.json)
record exact source commits, whole file sizes/hashes and dependency scope.

For an **optional late comparison**, obtain the thirteen files named in
NATIVE_INPUTS.json from the verified original source commit
`3f1da6e41756cf86136d4236c53369767007e68f`, directory
`round-two/six-tammes-1/eleven-triangle-bridge-obstruction`, into a separate
local directory. Then run four disjoint ranges in each mode, serially:

```sh
python3 -B late.py --native-dir /path/to/native --start 0 --stop 144
python3 -B late.py --native-dir /path/to/native --start 144 --stop 288
python3 -B late.py --native-dir /path/to/native --start 288 --stop 432
python3 -B late.py --native-dir /path/to/native --start 432 --stop 576
python3 -B -O late.py --native-dir /path/to/native --start 0 --stop 144
python3 -B -O late.py --native-dir /path/to/native --start 144 --stop 288
python3 -B -O late.py --native-dir /path/to/native --start 288 --stop 432
python3 -B -O late.py --native-dir /path/to/native --start 432 --stop 576
```

This compares every case/Gram/gap/Bézout/Bernstein field with the unchanged
primary code, including the entire fresh-label correspondence. It does
not strengthen the primary proof by importing producer computations.
The original [native README](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/eleven-triangle-bridge-obstruction/README.md)
lists its twelve commands, all actually replayed here.

[VALIDATION.json](VALIDATION.json), [NATIVE_VALIDATION.json](NATIVE_VALIDATION.json),
[LATE_VALIDATION.json](LATE_VALIDATION.json) and [COLD_VALIDATION.json](COLD_VALIDATION.json)
record actual complete normal/O execution and whole-byte equality.
All six thread variables are one, only one mathematical child runs at once,
and the unchanged 1CPU/2GiB process scope is respected. The independent
inner wall guard is 55 seconds and child timeout 60 seconds; the native
replay uses its original 55-second guard. No guard is interpreted as a
negative mathematical result.

Only compact text source and evidence belong to this packet. No key,
private ledger, numerical table, private experiment, large proof corpus
or bulk Gram stream is required. The ordinary spherical/Jordan bridges
remain unformalized. [SHA256SUMS](SHA256SUMS) binds the public files.
