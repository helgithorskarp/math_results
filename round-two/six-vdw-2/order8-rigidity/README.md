# No order-eight multiplicative template on punctured F617

An **exact computer-assisted lemma** excludes every binary coloring
`c:F_617^* -> {0,1}` invariant under `H=<3^77>`, the subgroup of order
eight, that avoids monochromatic nonconstant seven-term arithmetic
progressions whose terms are all nonzero. All `2^77` labeled coset
patterns are covered. The proof uses seventeen small, independently
replayed refutations, after an elementary longest-run reduction.

Combined with the published
[order-at-least-11 classification](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_order11_rigidity),
this gives a useful stronger corollary: **every nonquadratic
progression-free punctured-field coloring has color-preserving
multiplicative stabilizer of order at most seven**. The remaining
possible stabilizer orders are `1,2,4,7`. The order-eight exclusion is
self-contained; the corollary imports that earlier classification.

Author: **six-vdw-2, researcher**, 2026-10-01. Shared signing identity
does not establish independent authorship. The present validation uses
separate same-author implementations; it is not independent peer review
or a proof-assistant formalization.

`W(2,7)` here means **two colors and seven terms**. This is an exclusion
of a specified finite-field construction family. It gives neither an
interval upper bound nor a new van der Waerden lower bound. The requested
AP-free coloring of `[1,3704]` remains open in this work.

## Proof and coverage

The field is prime of order 617; 3 is a primitive root and `616=8*77`.
An H-invariant coloring is a binary cyclic word `y_i=c(3^i)`, `i mod77`.
There are 23177 distinct punctured-field AP supports in these coordinates.
Each support contributes its positive and negative not-all-equal clause.

The actual progression `3,37,71,105,139,173,207` has coset coordinates
`1,8,1,2,0,18,8`. Its support `{0,1,2,8,18}`, and every cyclic shift of
that support, forbid a monochromatic cyclic run of length 19. An odd
binary cycle cannot alternate, so every putative AP-free word has a
longest run `L in {2,...,18}`. Rotate a longest run to position zero and
complement its color to zero. Then `y_0=...=y_(L-1)=0` and
`y_76=y_L=1`. Every cyclic window of length `L+1` must contain both colors.

These seventeen cases, each with only 77 variables, are all UNSAT by
exact positive-RUP replay. A longest-run partition is the coverage
argument; it is not an enumeration of a sample or a heuristic search.
The full argument and the proof-checker induction are in [PROOF.md](PROOF.md).

## Reproduce

Use Python 3.11 and GCC, with one thread and one CPU job at a time.
For example, from the repository root:

```sh
python3 -m venv scratch/order8-env
scratch/order8-env/bin/pip install -r round-two/six-vdw-2/order8-rigidity/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  scratch/order8-env/bin/python round-two/six-vdw-2/order8-rigidity/reproduce.py \
  --work scratch/order8-check
```

The script downloads a pinned official `drat-trim.c` source, checks its
SHA256, compiles the untrusted converter, generates all seventeen exact
CNFs, audits them from the definition, and proposes capped CaDiCaL195
proofs. It converts and independently checks every addition in both
normal and optimized Python. It also runs coverage, checker rejection,
and deliberately incomplete-solver controls. For offline converter
input add `--drat-source /path/to/drat-trim.c`; its hash must still match.

Every solver case has a 50000-conflict budget and external 30-second
timeout. Each conversion has a 25-second internal and 30-second external
timeout. An interrupted, UNKNOWN or timed-out case proves no exclusion.
The final success status is `EXACT_ORDER8_PUNCTURED_FIELD_EXCLUSION`.
Large generated CNFs and traces remain under the requested scratch path.

Resume complete proposal/conversion stages with the same command plus
`--resume`. Source and trace hashes must match; the mathematical audits
and exact proof replay always run again. An unmarked partial stage is
rejected. Different regenerated proof bytes are acceptable only if the
complete proof independently verifies; the expected reference hashes
are reproducibility diagnostics, not a premise of UNSAT.

Files: [encoder](encode.py), [independent definition-level audit](audit.py),
[strict proof checker](check_rup_lrat.py), [bounded solver proposal](solve.py),
[reproduction driver](reproduce.py), [controls](controls.py),
[expected exact case data](expected.json), and [validation record](VALIDATION.md).

## Dependencies and prior art

The new result closes the order-eight/index-77 frontier left open by
the earlier order-11 classification, graph lemma
`bafkreiebd2xk3lixbmcgk3ddfmgqwpgnmvhaa37vkweidlnweeyi7jggem`
at height 7226, source commit `3da9b6f6c56fa74c9cdc40153ff0ca68630ee68a`.
Its [independent review](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_affine_rigidity_review3),
graph `bafkreibziig3wb5bald3tkrlp3mdnnpylpjo2tbff3kku3z3smuqkh3sr4`
at height 7272, confirms the imported classification. That review's
affine-stabilizer extension is not needed for the present theorem.

The preceding [conditional logarithmic defect cut](../order8-log-defects/README.md)
excluded only words with at most eleven equal adjacent pairs; its graph
lemma `bafkreia5rsofa62ffsytamldfait2fswf5lphgzk5kue7nxhce52k5fnja`
at height 8532 and source commit `232121bc61f57d6a4271cdadaa5ea3cbbbcc8dc2`
are distinct from this complete exclusion. The present result does not
depend on that cut.

`check_rup_lrat.py` is reused byte-for-byte from the earlier
[period-618 certificate](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_618_three_ap_obstruction/check_rup_lrat.py),
graph `bafkreidlaq5uknmu22tpadoyvxe537hkgubmpyhynlekstrengbvtjlvti`
at height 7835. Its SHA256 is
`55543f905d42aaf0955906f97a8484ec8522a182512b1d2e8fe132bb45cb545c`.
The coset generator and solver interface adapt our preceding published
cut; the run-case encoder, independent run audit, and coverage proof are new.

Primary context was rechecked on 2026-10-01.
[Monroe, JCMCC 128, Tables 1 and 2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give `>3703` and modulus 617 for two colors/seven terms, using
`W(length,colors)`. Multiplicative prepartitioning is established in
[Heule, Section 4.3](https://www.cs.cmu.edu/~mheule/publications/JOC_08_03_A01.pdf).
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
give the 617 power-residue construction. The quantified order-eight
exclusion was not found in the inspected sources or committed graph;
this is bounded evidence, without a priority claim.
