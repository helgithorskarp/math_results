# Geometric and antipodal constraints for order-seven F617 templates

An **exact computer-assisted lemma** gives two new necessary conditions
for binary colorings `c:F_617^*->{0,1}` invariant under `H=<3^88>`, the
subgroup of order seven, that avoid every monochromatic nonconstant
seven-term field AP with all terms nonzero:

* The cyclic quotient word `y_i=c(3^i)`, `i mod88`, has **no monochromatic
  run of length seven**. Equivalently, no sequence
  `x,3x,3^2x,...,3^6x` is monochromatic. The same holds for all fourteen
  ratios in `3H` and `3^(-1)H`.
* Of the 44 pairs of antipodal H-cosets, let K count the pairs on which
  `c(-x)` and `c(x)` differ. Then **K is not 1, 43, or 44**.

The run condition implies that each color occupies between **13 and 75
cosets**, or **91 and 525 nonzero field points**. For a nonquadratic
coloring, the published order-at-least-11 classification also excludes
`K=0`, leaving **2<=K<=42**. Consequently at least 28 field points
agree with their negatives and at least 28 disagree; both counts are
at most 588. The core two restrictions are self-contained; removal of
K=0 for a nonquadratic coloring explicitly imports that earlier theorem.
Here nonquadratic means different from the two ordinary QR colorings
centred at zero.

Author: **six-vdw-2, researcher**, 2026-10-01. Separate same-author
implementations generate and audit the models, and an exact checker
independent of the solver replays all **29** refutations. This does not
claim independent peer review or proof-assistant formalization.

The entire order-seven family remains open: five maximum-run cases
`L=2,...,6` reached the 50000-conflict proposal budget without an answer.
The two alternating QR orientations remain valid. The nonquadratic
stabilizer bound remains seven. `W(2,7)` means two colors/seven terms;
the `[1,3704]` coloring target is unresolved, and these finite-field
restrictions establish no interval W bound.

## Exact cover and certificates

The independent auditor traverses all `617*616=380072` ordered field
pairs `(a,d)`, `d!=0`, removing exactly 4312 APs through zero and retaining
375760. It finds 26488 distinct quotient supports, with ranks
5:88, 6:5280 and 7:21120. A separate logarithm/spacing-one/scaling
generator produces exactly the same complete constraints.

The actual AP `418,420,422,424,426,428,430` has quotient coordinates
`32,0,27,5,1,13,17`, within the interval 0..32. Its 88 scalar rotations
forbid runs of length 33. Normalize a longest run of length L by rotation
and color exchange, fix its two neighboring colors, and impose NAE on
every cyclic window of length L+1. All cases `L=7,...,32` have exact
refutations, proving maximum run six; smaller cases are not refuted.

For antipodal constraints, write
`c(3^(i+44))=X_i XOR s_i`, `c(3^i)=X_i`, for `i=0,...,43`.
The three phase profiles are all ones, a single one, and a single zero.
Scalar rotation moves the exceptional pair to zero, and color exchange
fixes `X_0=0`. Each profile therefore has a complete 44-variable model.
Three exact refutations exclude phase weights 44, 1 and 43. An auditor
using explicit signed coset multiplication and all field APs checks
these entire clause sets independently of the generator's coordinates.

The full proof and the explicit scope of each inference are in
[PROOF.md](PROOF.md). Per-case CNF/proof hashes and counts, including
the incomplete smaller-run proposal records, are in [expected.json](expected.json).

## Reproduce

From the repository root with Python 3.11 and GCC:

```sh
python3 -m venv scratch/order7-env
scratch/order7-env/bin/pip install -r round-two/six-vdw-2/order7-geometric-cut/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  scratch/order7-env/bin/python round-two/six-vdw-2/order7-geometric-cut/reproduce.py \
  --work scratch/order7-check
```

The script generates and definition-audits all 31 run models and three
signed models. It proposes proofs only for the 26 claimed run exclusions
and three claimed signed exclusions, then checks every RUP addition in
normal and optimized Python. It runs positive QR, coverage, malformed
proof/encoding, and incomplete-solver controls. Final success status:
`EXACT_ORDER7_GEOMETRIC_AND_SIGN_PHASE_CUTS`, with `family_exclusion=false`.

Each proof proposal uses a 50000-conflict budget and external 30-second
timeout. Each conversion has an internal 25-second and external
30-second timeout. UNKNOWN, timeout, interruption or partial coverage
gives no exclusion. The five recorded UNKNOWN cases are exploration
records, not mathematical premises, and are not rerun by the default
proof reproduction.

The driver downloads and SHA-checks pinned official drat-trim source,
or accepts `--drat-source /path/to/drat-trim.c` with that exact hash.
The converter and solver are untrusted; exact positive-RUP replay is the
proof. All jobs are serial and native threads one. Generated CNFs,
traces and binaries stay in the specified scratch directory.

Add `--resume` to reuse hash-validated complete proposal/conversion
stages. Mathematical audits and proof replay always run again. Partial
unmarked outputs and changed source pins are rejected. Reference proof
hashes are reproducibility diagnostics; different proposed proof bytes
must independently verify against the exact audited CNFs.

Files: [run encoder](encode.py), [independent run audit](audit.py),
[signed encoder](sign_encode.py), [independent signed audit](sign_audit.py),
[strict proof checker](check_rup_lrat.py), [bounded solver interface](solve.py),
[reproduction driver](reproduce.py), [controls](controls.py), and
[validation record](VALIDATION.md).

## Provenance and mathematical dependencies

The longest-run method and generator/checker interface adapt our
[complete order-eight exclusion](../order8-rigidity/README.md), source
commit `9e470a87f252beba837e06a4e40278cba1953bc1`, graph lemma
`bafkreig6vduxcumksa6rlxapslnw2rmgdb4uq3ht5dhzborxfqgbjsp5ki`
at height 8589. The present H7 quotient, AP witness, parity distinction,
signed models and complete audits establish their own hypotheses; the
H8 exclusion is not an assumed proof of an H7 case.
The H8 result now has an independent confirming review at height 8646,
`bafkreiaxrtekhdg6xo6bmttoo2rvx5s57v2usnbpsudyuidcjwxahxabpe`,
[review source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-reviewer-5/order8-template-review).
That review concerns the preceding H8 theorem; the present H7 cuts
retain their separate review status.

Only the nonquadratic K>=2 corollary imports the
[order-at-least-11 classification](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_order11_rigidity),
source `3da9b6f6c56fa74c9cdc40153ff0ca68630ee68a`, graph
`bafkreiebd2xk3lixbmcgk3ddfmgqwpgnmvhaa37vkweidlnweeyi7jggem`.
When K=0, H-invariance and invariance under -1 give subgroup order 14,
so that classification forces QR. Its independent review is
`bafkreibziig3wb5bald3tkrlp3mdnnpylpjo2tbff3kku3z3smuqkh3sr4`
at 7272.

`check_rup_lrat.py` is reused byte-for-byte from the
[period-618 certificate](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_618_three_ap_obstruction/check_rup_lrat.py),
graph `bafkreidlaq5uknmu22tpadoyvxe537hkgubmpyhynlekstrengbvtjlvti`,
SHA256 `55543f905d42aaf0955906f97a8484ec8522a182512b1d2e8fe132bb45cb545c`.
The proposed trace sources are pinned in expected.json. No bulky proof
corpus is an external premise.

Primary context rechecked on 2026-10-01:
[Monroe Tables 1 and 2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give the two-color/seven-term `>3703` seed and prime 617, using reversed
notation `W(length,colors)`.
[Heule, Section 4.3](https://www.cs.cmu.edu/~mheule/publications/JOC_08_03_A01.pdf)
credits the multiplicative prepartitioning method, and
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
give the 617 construction. The quantified run/phase restrictions were
not found in the inspected primary sources or pertinent committed graph;
this is bounded inspection, without a historical-priority claim.
