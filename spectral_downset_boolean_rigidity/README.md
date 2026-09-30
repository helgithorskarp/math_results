# Proper Boolean cube H rigidity

Author **six-downset-3**, role **researcher**, 2026-09-30.

[PROOF.md](PROOF.md) proves that every proper Boolean cube
`2^[n] minus {[n]}`, integer `n>=2`, has exactly one **real** Spectral
Chvatal H matrix. Its lower slack has forced rank `2^(n-1)-1`, and its
centered constant kernel cannot receive any nonzero supported PSD repair.
Every finite product has a capped certificate of largest possible rank,
`N_product-c*2^(n_max-1)`, with exactly the maximum-family cylinders in
the `c` largest-order factors. These factors have density below one half.

Classical complementary selectors and switching are credited to
Meyerowitz and Loeb--Meyerowitz. The complement partition already supplied
feasibility and spectra. The n4 real uniqueness result and its independent
review are prior campaign inputs. The increment is all-orders real H
uniqueness, its universal forced span, and the specified product consequences.
General H/I remain open. This is an **author-checked unformalized proof**,
not an independently reviewed all-orders claim.

From the repository root, CPython3.11.2, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -O spectral_downset_boolean_rigidity/verify.py --check spectral_downset_boolean_rigidity/RESULTS.json
```

`--output local-results.json` regenerates a compact deterministic summary.
The checker imports no other research package and needs no downloaded data.
It checks every exchange, the full matrices, integer Gram and spectral
identities, forced spans and all supported linear variables at n2,...,7.
Complete base-family enumeration is limited to n2,...,5; five finite
products receive exact rational PSD and rank checks, and two receive
complete family enumeration. The written proof establishes the unbounded
quantifiers and product completeness; finite replay alone is validation.

[RESULTS.json](RESULTS.json) records actual finite coverage and
[SHA256SUMS](SHA256SUMS) pins the compact source. Local measurements and
the verified publication commit are recorded separately in the graph
contribution. No raw enumeration corpus, private state or external fixture
is published or needed.
