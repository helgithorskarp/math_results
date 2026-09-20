# Independent review: four common neighbors in a torus thrackle

This package independently audits the claim and construction in
[`torus_thrackle_four_common_neighbors`](../torus_thrackle_four_common_neighbors/)
at source commit `c467f8943a53f8d7183ae9d91f11eda943a6063e` and Discovery Net CID
`bafkreidtu4t3kwr2kl7fgahu27fajkl5yxqojxwipcjcwh7wjnr77twq3y`.

**Verdict: accept with high confidence, with no historical-priority verdict.**
The theorem, the equality observation, and the explicit rotation construction
are correct under the stated convention that surfaces are closed and
orientable.  The full premise and completeness audit is in
[`REVIEW.md`](REVIEW.md).

The independent checker does not read the contributor's JSON certificate or
import their code.  It reconstructs the rotation system from the cyclic
formulas, computes faces as dart-permutation orbits, computes mod-two cellular
homology with integer bit sets, checks every original-edge pair, expands the
printed face-orbit table, and audits every nonempty induced `K_{2,n}`
subdrawing.  It also rejects or distinguishes five adversarial mutations.

Run with Python 3.11 or later, using only the standard library:

```sh
python3 independent_check.py | diff -u expected.json -
```

The command is silent on success.

The review establishes mathematical correctness of the precise theorem in the
target package.  It does not establish that the explicit `K_{2,4}` rotation
scheme is historically new, and it does not address nonorientable surfaces or
determine the general asymptotic thrackle genus of `K_{2,n}`.
