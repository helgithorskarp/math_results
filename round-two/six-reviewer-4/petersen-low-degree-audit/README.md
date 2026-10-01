# Independent Petersen-root low-degree Book108 audit

Actual reviewer **six-reviewer-4**, role **independent mathematical reviewer**.

Confirms the rooted finite lemma of 8941: a valid ordinary 22-point red-B4/blue-B7-free graph with 108 red edges, maximum degree ten and one full Petersen root has minimum degree at least eight. The unrooted application remains conditional on the separately credited 8828 root classification. No whole 108-edge exclusion or Ramsey endpoint is claimed.

[REVIEW.md](REVIEW.md) gives the complete ordinary reduction, finite coverage, verdict, credit and trust boundary. A new full-column hash join generates all 4,985 tagged incidences; adjacent-ground-transposition closure reconstructs all 51 orbits. Actual whole-vertex page counts and fresh synchronous elimination exclude them initially or within two rounds. This is a shallow certificate for the same rooted sector.

With CPython 3.11.2 and standard library only, run sequentially in this directory:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B check.py
python3 -B -O check.py
```

Both regenerate the complete independent record and print `PASS`. The record is in `expected.json`, including all 51 representatives, complete star-domain hashes and fresh round witnesses. `check.py --emit` prints the entire regenerated compact record. The independent proof needs no researcher executable, supplied orbit representatives, supplied deletion trace, solver or external package.

Optional original-certificate replay:

```sh
# From the publication repository root, extract the exact already published input:
git show aeddf654fc21becf85021682c5b211d0209d82d2:round-two/six-books-3/low-degree108/certificate.json > round-two/six-reviewer-4/petersen-low-degree-audit/input-certificate.json
cd round-two/six-reviewer-4/petersen-low-degree-audit
python3 -B compare.py input-certificate.json --controls
python3 -B -O compare.py input-certificate.json --controls
```

The original [public certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/low-degree108/certificate.json) is an untrusted input pinned by its raw SHA256. The replay rebuilds the independent census, orbit cover and every physical star domain, then verifies all 73 original steps/394 removals. Eight semantic damaged inputs reject, including a genuinely supported-star deletion. This is a separate check; `check.py` proves exclusion without that input.

All 1,024 six-point graphs with a fixed root split give 7,168 direct third-point comparisons plus 1,024 asymmetric-star controls. `primary21.json` is a normalized copy of the [known primary 21-point construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt), credited prior art. Its actual ten stars/completion pass and 196 asymmetric changes reject.

`PROVENANCE.json` records original source/input pins and exact scope; `VALIDATION.json` records complete runs. `SHA256SUMS` covers every other compact source file. Whole-incidence/star corpora, native logs, private ledgers and signing material are unnecessary and omitted. Ordinary reductions and enumeration/program correctness remain unformalized. Global bounds remain 22–23.
