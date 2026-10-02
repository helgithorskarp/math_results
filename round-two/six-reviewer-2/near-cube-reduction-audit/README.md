# Independent near-cube all-order cone-reduction audit

Actual reviewer: **six-reviewer-2**, independent mathematical reviewer.
Target: LEMMA9639, `bafkreicsrk6m32djaect66rigwbz46nz3wcga6yxto4z3qowvgk56mip3a`.
The ordinary universal reduction is confirmed in the precise scope in
[REVIEW.md](REVIEW.md). [PROOF.md](PROOF.md) gives the complete original-space
argument and two proved conditional refinements: same-specified whole projected
gap tests, and rational joint greatest-rank feasibility for each fixed n,k.
No all-order positive witness or general singular-boundary rationality is asserted.

CPython **3.12.14**, standard library only. From this directory:

```sh
python3 -B verify.py --check EXPECTED.json
python3 -O -B verify.py --check EXPECTED.json
```

Both compare the **entire** deterministic three-phase record, not a selected
summary or digest. [EXPECTED.json](EXPECTED.json) includes all72 original
(n,k) domains n6..14, all1476 affine vectors, full field hashes, actual original
n6/n7 controls, and16 semantic damages/two positive controls. [basis.py](basis.py)
and [literal.py](literal.py) are separate complete coordinate/literal methods.
[core.py](core.py) solves the simultaneous star system and keeps every physical
sector. [linear.py](linear.py) is reused unchanged from the reviewer's own prior
exact Schur helper, credited in [PROVENANCE.json](PROVENANCE.json).
Checks use exceptions and remain active under -O. No floating point or solver.

The runner sets six numerical-thread variables to1 and starts one mathematical
child at a time. Each child has an unchanged45s internal/55s outer guard.
Dense original allocation is restricted to n6/n7, and computational order
checks to n6..32. Failure, timeout or incomplete work is not a mathematical
exclusion. The **all-order** argument is the unformalized ordinary proof,
not extrapolation from these finite domains.

After the primary proof/program/entire-oracle seal, [corroborate.py](corroborate.py)
obtains the exact11-file public target closure from the authorized Git repository
into a temporary directory, checks all input hashes, runs the original complete
checker normally and with -O, and compares every exported mathematical field
against the independent model. Run:

```sh
python3 -B corroborate.py --check COMPARISON.json
```

This optional later corroboration requires Git/network access to the exact
public repository. It is not an input to the independent runner or all-order
proof. [AUTHOR-INPUTS.json](AUTHOR-INPUTS.json) pins the input closure;
[COMPARISON.json](COMPARISON.json) records the complete scoped comparison.
[VALIDATION.json](VALIDATION.json) preserves methods, all whole records/timings,
exposure chronology, guards and operational mistakes. Target written proof and
prior unchanged model helpers were visible; no blind audit or independently
discovered construction is claimed. No credentials, ledgers, dense high-order
matrices or large proof corpus are published. [SHA256SUMS](SHA256SUMS) covers
all compact public source/evidence files except itself.
