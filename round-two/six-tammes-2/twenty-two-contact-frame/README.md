# Tammes G22: one packing orientation

Author **six-tammes-2**, role **researcher**.

Deleting both `(6,8)` and `(9,13)` from the credited thirteen-point core
leaves a free circle parameter and four formal quadratic orientations.
On the full closed `[14/25,593/1000]`, this package proves that only
`(epsilon,eta)=(-1,+1)` packs and its two-contact Gram quantity is `>1/2`.
It reduces the motif to 39 affine-radical packing inequalities.
[PROOF.md](PROOF.md) includes complete chart, rank and tangent coverage.
This is an author proof with independent mathematical review pending;
the global Tammes-15 bounds are unchanged.

Use CPython 3.11 or later and SymPy 1.14.0:

```sh
python3 -m pip install -r requirements.txt
python3 check.py
python3 controls.py
```

The checker sets all native numerical threads to one and has a 160-second
guard. It regenerates the exact SymPy identities and signs, a separate
standard-library integer-polynomial coordinate audit, and every literal
interval witness. Its output must equal [EXPECTED.json](EXPECTED.json).
Normal and optimized Python are checked in [VALIDATION.json](VALIDATION.json).
A guard failure is incomplete verification.

For interval witnesses alone, without SymPy:

```sh
python3 replay.py bad g-half
python3 audit.py
```

The two compact [bad-branch](PLAN-bad.json) and
[Gram-bound](PLAN-g-half.json) partition trees cover the full fixed
rectangle, including all tangent loci. Prefix splits and literal leaf
instructions reconstruct every closed box. Generated adaptive traces,
heuristic grids, local environments and private campaign state are omitted.
The code imports no prior research source or coordinate dataset.

[INPUTS.json](INPUTS.json) records credited mathematical dependencies and
published source snapshots. [LITERATURE.md](LITERATURE.md) records the
primary-literature refresh. The fifteen-point strict-missing-edge
corollary uses prior claims 8835 and 9057; their proofs are separately
credited and are not rerun by this package. Written geometric bridges
and source-to-model interpretation remain unformalized.
