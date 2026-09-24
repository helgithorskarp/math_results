# Square-saturated hypercubes with asymptotic upper constant six

For every `n >= 14`, this construction proves

\[
\operatorname{sat}(Q_n,Q_2)<\left(6+\frac{49}{n+2}\right)2^n,
\qquad
\limsup_{n\to\infty}\operatorname{sat}(Q_n,Q_2)/2^n\le6.
\]

The new ingredient is a finite certificate that replicates to shortened
syndrome blocks. Blocks of lengths `3*2^t-1` and `10*2^t-1`, together with the
accepted Hamming blocks, fill the dimension gaps that previously gave the
uniform constant seven. This does not establish an exact saturation number,
convergence, or a matching lower bound. The previous `11/2` subsequence upper
bound remains unchanged.

- [Full proof, certificates, and six-interval parameter table](proof.md)
- [Three compact templates](templates.json)
- [Finite-condition checker](check_templates.py)
- [Full-quotient and rational-arithmetic audit](audit.py)
- [Deterministic cube constructor](construct.py)
- [Independent definition-level cube verifier](verify.py)

Run from this directory with CPython 3.11 or later; no third-party packages
are required:

```bash
python3 check_templates.py > /tmp/upper6-templates.json
cmp /tmp/upper6-templates.json EXPECTED_TEMPLATES.json
python3 audit.py > /tmp/upper6-audit.json
cmp /tmp/upper6-audit.json EXPECTED_AUDIT.json
python3 reproduce.py > /tmp/upper6-output.json
cmp /tmp/upper6-output.json EXPECTED_OUTPUT.json
sha256sum -c SHA256SUMS
```

The last script privately generates and independently verifies 12 saturated
cube witnesses through dimension 18, checking 1,242,793 selected edges and
1,656,375 missing edges. It removes the expanded witnesses when finished.
The measured CPython 3.11.2 run took 11.62 seconds and 259,132 KiB peak child
RSS on the research host. All three outputs matched byte-for-byte under
CPython 3.12.14. Hardware and runtime affect resource costs.

A single witness or exact bound can be reproduced separately:

```bash
python3 construct.py --blocks F 1 F 1 0 --output /tmp/upper6-witness.json
python3 verify.py /tmp/upper6-witness.json
python3 construct.py --dimension 1000000 --bound
```

Default dimension selection requires `n>=14`; explicit expanded blocks have
a deliberate cap of dimension 18. These finite edge counts validate the
construction and are not claimed to improve the best small-dimension bounds.

The optional [discovery script](discover.py) reproduces the F template with
OR-Tools 9.15.6755, CPython 3.12.14, one worker and seed 1:

```bash
python3 discover.py --seconds 30 --output /tmp/upper6-discovered.json
```

This returned the committed F certificate with 33 outside incidences. The
solver's optimality status is not part of the proof. Dependency versions,
output hashes and resource measurements are in [REPRODUCTION.json](REPRODUCTION.json).

The proof trusts exact finite certificate verification and the unformalized
universal arguments in `proof.md`. The independent graph verifier imports no
constructor or template code. Solvers were used only to discover templates;
solver soundness and optimality are not theorem assumptions. External review
of the new theorem is pending.

The [accepted upper-seven result](../hypercube_square_saturation_upper7/README.md)
and its [independent review](../hypercube_square_saturation_upper7_review1/REVIEW.md)
are the immediate durable dependencies. Primary literature and the limits of
the novelty search are recorded in the proof.
