# Independent all-weight covering-budget audit

Actual author **six-reviewer-2**, role **independent mathematical reviewer**.
Target9031 is credited to six-covering-3. The review confirms its fixed-prefix
all-small-fractional-group obstruction and proves an extension to arbitrary
group sizes subject to a per-resource weighted average companion bound.
It supplies no covering existence/nonexistence or numerical LCM bound.

See [REVIEW.md](REVIEW.md) for definitions, proof, exact scope and the required
strengthening section. [CERTIFICATE.json](CERTIFICATE.json) is the credited
original probability witness, not reviewer-discovered marginals.

From this directory, Python3.11.2 standard library, run jobs serially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B audit.py > /tmp/fractional-budget-normal.json
python3 -B -O audit.py > /tmp/fractional-budget-optimized.json
cmp /tmp/fractional-budget-normal.json EXPECTED.json
cmp /tmp/fractional-budget-optimized.json EXPECTED.json
python3 -B controls.py > /tmp/fractional-controls-normal.json
python3 -B -O controls.py > /tmp/fractional-controls-optimized.json
cmp /tmp/fractional-controls-normal.json CONTROLS.json
cmp /tmp/fractional-controls-optimized.json CONTROLS.json
sha256sum -c SHA256SUMS
```

The independent audit constructs full physical CRT permutations from the
literal prescribed classes and frozen prime-digit paths. It checks every
congruence partition on every physical point for all72 divisors and55
generators, all primitive-block actions, complete phase-orbit probability
distributions, three actual common joint assignments, and all76 rational
ordinary/periodic coefficient records. The local mass is obtained from an
independent row/column-cover formula and compared with the six balanced
vertices. No original executable, discovery table, solver or numerical
library is imported.

The proof transports a legal common joint phase tuple uniformly through
the generated finite permutation group. Transitivity gives pointwise
orbit-averaged coefficients and thus all-weight domination. This is a
separate proof route from averaging the weight variables in the target.
The group need not be fully enumerated or shown to be the whole stabilizer.

Controls include all262144 local absorption identities,768 balanced-grid
symmetries,15625 size-six fractional-group probability cases,32 full53-resource
fractional-group cases, and six semantic corruptions. A fully legal probability
distribution fails the actual coefficient inequality. These controls support
the ordinary universal proofs; they are not their finite-domain substitutes.

The reviewer clears all1200 phase-orbit sizes with L=1152, using scale
(1152000000)^2. The target clears only its listed nonzero marginal sizes,
L=576, using twice the square of576000000. The reviewer's scale and cleared
margin are twice the original ones; every rational coefficient ratio agrees.
This representational difference is explicit, not a mathematical mismatch.

The largest reviewer job used134816KiB and29.171s, below its upfront90s guard.
All seven mathematical jobs were serial with native threads one. The original
checker was also replayed normally/optimized against its complete pre-existing
expected record, and its nine corruption controls passed. Own EXPECTED.json
was newly generated. [VALIDATION.json](VALIDATION.json) distinguishes these
checks; [PROVENANCE.json](PROVENANCE.json) records immutable input pins.

Written probability, finite-group averaging, additive-grid and conditional
restoration arguments remain unformalized. Shared signature identity is not
independent authorship. Original source:
https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/small-group-obstruction/proof.md
