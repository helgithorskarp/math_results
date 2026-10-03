# Degree-nine three-fifths audit

Actual **six-reviewer-1 / independent mathematical reviewer**.

[REVIEW.md](REVIEW.md) confirms the full original 10131/index1 theorem:
every degree-nine polynomial with all original zeros in the closed unit disk
has reciprocal critical-distance sum F>8 at every marked zero |a|<=3/5,
relative to the explicitly credited 10101 lower-region theorem.
[PROOF.md](PROOF.md) additionally proves **F>8+1/125000 on the closed annulus
11/20<=|a|<=3/5 only**. Multiplicities are counted and zero denominators mean
infinity. No optimality, unrestricted first-power result or entire-disk
quantitative margin is asserted.

The complete written proof/tree were exposed, NOT BLIND. Five primary files
were sealed before the new native target code/cover/expected/controls were
opened. Existing own exact-arithmetic and Gaussian engines and earlier q
fixtures are explicitly reused; no new native author module enters the primary
checker. Later native runs are corroboration.

Use CPython 3.12 with its standard library (tested 3.12.14):

```bash
python -B reproduce.py
```

This runs eight local/cold, normal/optimized positive children and fourteen
semantic rejection children, serially with six native thread variables set to
one and a fixed 45-second child guard. Full parsed records and full bytes agree
before any hashes are considered. The generated 4,071,621-byte primary record
and 40,562-byte Gaussian control record stay temporary; their fingerprints
and compact checked evidence are in [VALIDATION.json](VALIDATION.json).

To regenerate the complete primary record yourself, save it outside this
publication directory:

```bash
python -B check.py --output /tmp/three-fifths-primary.json
python -B literal.py > /tmp/three-fifths-literal.json
```

check.py verifies both fixed mass budgets m=1 and m=1000001/1000000, all 63
polar cells and all 272 origin leaves per budget, every complete coefficient
vector and rational integral in power/Bernstein bases, all seven centered
constants and all 271 closed split unions. PLAN.json is the full signed-body
partition, not an unchecked proof certificate. The ordinary continuous bridge
is PROOF.md. literal.py's nine controls check actual polynomial differentiation,
synthetic division, the communications and the complete centered expansion;
they are not claimed original-disk feasible witnesses.

For optional late native corroboration, point to the author's original source
directory in a checkout containing its pinned version:

```bash
python -B corroborate.py --native ../path/to/three-fifths-first-power
```

This checks all ten native source byte pins, full tree equality, two fresh
normal/optimized native records and 1,967 full vectors/19,149 coefficients
against a fresh independent reconstruction, followed by twenty native
semantic rejections. It establishes no perturbed-budget author claim. Source
pins, exposure chronology and credit are in [PROVENANCE.json](PROVENANCE.json)
and [PRIMARY_SEAL.json](PRIMARY_SEAL.json). The proof is ordinary and
unformalized; hashes detect changes and do not certify the analytic bridge.
