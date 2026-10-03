# Independent joint-coercivity audit

Actual six-reviewer-5, independent mathematical reviewer, 2026-10-03.
[Verdict and scope](REVIEW.md), [ordinary proof and refinements](PROOF.md).
Confirms LEMMA9952 relative to its explicit stationary framework. The full
complex algebraic bound and specified-gap/specified-leading-mass original
corollary are retained. It does not settle the first-power endpoint.

Use CPython **3.12.14**, SymPy **1.14.0**, mpmath **1.3.0**. The primary
record includes these interpreter/library metadata; other interpreter versions
may produce different whole bytes even when the mathematical fields agree.
Install dependencies in an isolated environment or a directory in scratch.
Neither system package changes nor resource-limit changes are required.

From this directory, in an environment with the pinned packages:

```bash
python3 -I -B independent.py > /tmp/coercivity-independent.json
cmp /tmp/coercivity-independent.json EXPECTED.json
python3 -I -B -O independent.py > /tmp/coercivity-independent-O.json
cmp /tmp/coercivity-independent-O.json EXPECTED.json
python3 -I -B reproduce.py --work-dir /tmp/coercivity-cold --late-damages
```

The work directory must be new. `reproduce.py` runs one mathematical child
at a time, sets native thread variables to one, and enforces a fixed 55-second
child guard. A guard stop is operationally incomplete and proves no absence.
It downloads six whole pinned public files into that scratch directory,
checks their source hashes, regenerates the full native input chain, and runs
the late data-only comparison in normal/optimized modes. Native replay is
explicitly separate from independent mathematical verification.

For a directory containing the pinned packages, add
`--packages /absolute/path/to/packages` to `reproduce.py`. It inserts that
path into isolated children; this was the recorded local execution method.
To reproduce the six fresh primary corruptions in both modes, also add
`--primary-damages`. `--late-damages` checks three distinct corruptions of
the new unit, the credited parent witness, and the fifth primitive content.

The primary script reads **no producer source, fixture or generated table**.
It reconstructs the full defining ODE/kernel using SymPy's rational-function
coefficient field and dense univariate coefficient arrays, and obtains the
old univariate unit by fresh rational Euclid. The late adapter imports no
producer module; it reads regenerated output as data and checks entire maps,
pullbacks, matrix entries, minors and the credited 72-coefficient parent unit.

Whole primary output: **11464 bytes**, SHA256
`1572a135593fe5c1e6062e4c869a1a017a7cc32deb490ee998bb3ebdefe14fe3`.
The native canonical mathematical-record digest is
`9666b1b30eece3fef9a5de76044ff15771ce163f5bd9d76edd7d680e86259d64`;
its pretty-printed export has different whole bytes and is distinguished in
VALIDATION.json. No field normalization was used for normal/O comparisons.

Only compact source/evidence is published. Downloaded inputs, CAS packages,
raw execution streams, checkpoints and private research data remain in scratch.
The universal inequalities, complex segments, singular-value bridge,
real-root geometry and stationary interpretation are ordinary unformalized
proofs, not consequences of hashes or finitely sampled profiles.
