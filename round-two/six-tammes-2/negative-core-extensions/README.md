# Arbitrary extensions of the negative-edge thirteen-point Tammes core

Actual author **six-tammes-2**, researcher. Computer-assisted author proof;
independent review pending. See [PROOF.md](PROOF.md) for the exact hypotheses.

A thirteen-point packing with the displayed23 contacts and `t<tau` in
`[14/25,593/1000]` admits at most one further unit point at threshold t.
The added points have no imposed contact pattern. The proof combines a
certified cut-polytope cover with the exact lower/critical boundary9003
and the unique quartic model8929. This conditional exclusion is useful
only when its core occurs; it establishes no unconditional Tammes-15 bound.

From the repository root, with Python3.11+:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 round-two/six-tammes-2/negative-core-extensions/check.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -O round-two/six-tammes-2/negative-core-extensions/check.py
python3 round-two/six-tammes-2/negative-core-extensions/controls.py
python3 -O round-two/six-tammes-2/negative-core-extensions/controls.py
```

The checker regenerates all34,580 witnesses on95 closed dyadic cells,
separately audits each, and compares the full exact output with
[EXPECTED.json](EXPECTED.json). Its SHA256 identifies canonical generated
witnesses, not a pre-supplied private corpus. The critical exception is
exactly labels1,4,7 and applies only to actual packings below tau.
The four damaged controls test coverage, that exception, strict norm and
the sign of a genuine homogeneous avoidance inequality. No assert
statements are used for the mathematical checks.

The source has an explicit160-second runtime guard per local run.
A guard exit, failed denominator or unresolved triple is incomplete
evidence. The successful author checks and memory measurements are in
[VALIDATION.json](VALIDATION.json). They use one native thread and one
mathematical job at a time. Bulk exploratory and witness output is omitted.

Optional local generation, writing bulk witnesses outside this directory:

```sh
python3 round-two/six-tammes-2/negative-core-extensions/generate.py --audit --trace /tmp/tammes-negative-extension-witnesses.json
```

[INPUTS.json](INPUTS.json) pins public source bytes for the two prerequisites.
The checker verifies those hashes before importing the80-bit interval
kernel. It does not automatically re-prove the prerequisites. Audit their
mathematics and follow the commands in
[negative-cross-reduction](../negative-cross-reduction/README.md) and
[negative-core-boundaries](../negative-core-boundaries/README.md).
The new computation itself uses only Python's standard library.

The separate witness audit shares the interval/model code and is by the
same author. The geometric, continuity and differentiation bridges are
unformalized. Review verdicts on neighboring positive-edge or incidence
results do not transfer to this claim. [SHA256SUMS](SHA256SUMS) identifies
the compact publication files; generated state is ignored.
