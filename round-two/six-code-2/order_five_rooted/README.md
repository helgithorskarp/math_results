# C5 equality packings with a degree-twenty fixed point

This package constructs and classifies all **5,850 labelled** 68-word
packings invariant under the specified action of cycle type `5^3 1^3`
and having at least one fixed point of degree twenty. There are 32
completions of each saturated star and eight classes under the centralizer.
An explicit unused-point substitution rule produces every normalized code;
5,700 of the full labelled codes use all eighteen points.

See [PROOF.md](PROOF.md) for hypotheses, complete coverage, prior credit and
the trust boundary. Codes without a saturated fixed point, arbitrary point
isomorphism and the unrestricted `A(18,6,5)` endpoint remain outside the claim.
The order-five upper bound 68 and the classical fixture are earlier work.

CPython **3.11.2**, standard library only. Run these commands sequentially
from the repository root, choosing work directories which do not yet exist:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-code-2/order_five_rooted/reproduce.py --work scratch/c5-equality-normal
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -O round-two/six-code-2/order_five_rooted/reproduce.py --work scratch/c5-equality-optimized
```

The final `EXACT_RESULT.json` contains 100 rooted stars, 32 normalized
completions, 3,200 root-zero codes, 5,850 whole-carrier codes and eight
centralizer classes. Its SHA-256 is
`17c7bc785e77b32adbfc2e6a3e80e92ff2cec7039814a2a51a1c9eb2ddfe88f4`.
All literal generated evidence matches the frozen `EXPECTED.json` receipts.

- `generate.py`: full physical model and direct classical baseline check.
- `roots.py` / `root_audit.py`: separate recursive and physical pair-join
  enumerations of all saturated stars.
- `cover.py`: actual commuting point transports, checked independently by
  `physical.py` / `saturation_audit.py`.
- `equality.py` / `equality_audit.py`: counting-DAG producer and physical
  candidate, rule and complete positive-inventory checker.
- `construct.py`: eight fixed-point splits and 24 moving replacement rules.
- `saturation.py` / `saturation_audit.py`: generator-orbit producer versus
  full enumeration of every commuting permutation on every representative.
- `COUNT_CERTIFICATE.json`: compact untrusted 255-node counting certificate.
- `CLASSIFICATION.json`: eight literal representatives and class membership.
- `CONSTRUCTIONS.json`: complete positive normalized replacement rules.

The serial driver runs nine phases, each with an initial 60-second guard.
It retains local execution receipts and fails on incomplete phases. Full
inventories, model outputs and logs stay in the supplied scratch directory;
they are not publication files. Peak memory is comfortably below the
standing 2 GiB scope. No solver, external package, private catalogue,
large proof corpus or network access is needed for reproduction.

The exact evidence and ordinary bridges are author checked and unformalized;
independent review of this extension remains pending. Actual author:
**six-code-2, researcher**. Sharing a signing identity does not imply review.
