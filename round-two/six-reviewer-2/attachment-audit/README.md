# Independent ordinary H attachment audit

Author **six-reviewer-2**, independent mathematical reviewer. Confirms
LEMMA9361 and proves its maximum-family classification under the weak
private-star bound. Read [REVIEW.md](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/attachment-audit/REVIEW.md)
and [PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/attachment-audit/PROOF.md).
Boundary greatest rank, general H/I and output caps are outside the claim.

Use CPython3.11+ standard library, POSIX signals. Verified3.12.14. All
mathematical checks use explicit exceptions and survive `-O`. No solver,
CAS, external certificate corpus or nonstandard package is required.

From this directory in a checkout of the authorized publication repository:

```sh
sha256sum -c SHA256SUMS
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B audit.py --expected EXPECTED.json
python3 -B -O audit.py --expected EXPECTED.json
python3 -B compare_original.py ../../six-downset-1/one-point-attachments/RESULTS.json --expected COMPARE-EXPECTED.json
python3 -B -O compare_original.py ../../six-downset-1/one-point-attachments/RESULTS.json --expected COMPARE-EXPECTED.json
```

Run serially, with unchanged60s internal guards and native1. `audit.py`
checks19 original-set fixtures, eight equality boundaries, nine complete
maximum-family censuses and15 damages; it enumerates the separate \(n=1\)
classification counterexample. `compare_original.py` is a **post-seal**
adapter that imports no author code and independently reconstructs all15
original matrices, their full encoded SHA256 inventories and all math
fields, plus9 censuses and256 coordinate-transport entries. Original
input source is pinned in AUTHOR-INPUTS.json at
`ca8d2e363536435ad034f08cf3845a6ffd276326`; its RESULTS file must match
that manifest. Full original matrix data are not an external input.

For separate later corroboration, from the target source directory run:

```sh
python3 -B verify.py --expected RESULTS.json
python3 -B -O verify.py --expected RESULTS.json
```

Both unchanged native records matched every stable field. Native execution
is not evidence of independent implementation. The independent core/proof
record was sealed before reading target programs/RESULTS, and remains
unchanged. See VALIDATION.json for versions, full hashes, timings and
provenance. `linear.py` is unchanged reviewer-owned code credited to prior
77e859b56ee1808932766c83bb6e428cb6ac0415/d55d74f60db6c1eb573f91e9e82c1f696ddab4af.

All infinite results rest on the ordinary proofs, not on fixture
extrapolation. The public packet is compact; transient raw execution
logs, fetched target copies and durable campaign state stay outside it.
