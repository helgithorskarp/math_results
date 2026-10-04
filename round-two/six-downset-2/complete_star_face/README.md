# Maximum-star incidence cone and complete saturated faces

six-downset-2, researcher. Complete ordinary author proof and exact
implementation controls, unformalized and independently unreviewed;
see [PROOF.md](PROOF.md).

For any finite nontrivial downset, eliminate only its maximum-star
singletons and retain the actual empty completion and every smaller-star
singleton. The entire ordinary H space is equivalent to T>=0 with fixed
diagonal/intersection entries; the extra cap is exactly T<=N G^-1 in the
original metric G=I+RR^T+bb^T. These are equivalences, not an existence proof
for general H. Positive whole-ground complementary saturation gives a
complete remaining-coordinate cone. A seed with exactly the forced lower
kernel and positive endpoint gaps gives the full relative-interior cube.

At n28, the explicit credited10208 seed gives the complete saturated
face affine hull of dimension3,629,809,216,575 and a closed parameter cube
of radius1/7270700478476198400000000. Its36 invariant directions are
included. Fixing one coordinate per invariant orbit to zero gives
3,629,809,216,539 directions with every nonzero perturbation noninvariant.
Original empty and unsaturated complement entries may change. The five
noncentral classes and ranks263644105/268435426 are preserved. Seed10208's
kernel and gaps are an explicit proof premise, not replayed or reviewed
by this packet. No huge n28 matrix or trillions of directions are enumerated.

## Reproduce

CPython3.12.14, standard library only. From this directory, use the same
single-thread settings in each serial run:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
python3 -B verify.py --check EXPECTED.json
python3 -B -O verify.py --check EXPECTED.json
```

The expected summary is compared only after every mathematical calculation.
Use `--record /tmp/maximum-star-record.json` to save the complete regenerated
record outside the contribution. Its358173B and SHA256
`ace42ea695bae05d07afd1fd7b8e3af227ffc56e4f35e63c11171a205c233a20`
agree across normal/optimized runs. Generated records are omitted from the
source packet; no private record, numerical proposal or solver output is
a runtime input. See [VALIDATION.json](VALIDATION.json) for operational data
and [CREDITS.md](CREDITS.md) for prior mechanisms and the seed boundary.

Exact finite controls cover nine original systems,72 affine matrices,
33457 original entries,6861 maximum-star actions and15 damaged inputs.
They include nonregular smaller-star coordinates and a zero upper cone.
They validate the implementation; the general real proof remains ordinary.
