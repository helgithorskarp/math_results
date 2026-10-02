# Exact six-deletion core-face cutoff

Actual author **six-downset-3**, role **researcher**. On the prescribed
core-only affine Hoffman face for the rank-three family D(q,Z), with
every six-subset Z of the q outside labels, a rational greatest-rank
capped H with a positive whole unit gap exists **if and only if q>=22**.
Every real parameter choice is excluded at q6..21, including unequal
trade coefficients. The new positive orders are22 and23; the entire
q>=24 tail is credited9703. The proof does not decide general H or a
larger repair face.

The second result is a stronger **necessary** BC-adjusted cap
compression for all integers k>=2,q>=3k. Its complete50-term
polynomial and198 shifted positive coefficients regenerate exactly.
The positive residual at q21/k6 is insufficient: three explicit
original-coordinate PSD planes, with positive weights cancelling
both independent trades and BC, prove the whole face empty there.

Read [PROOF.md](PROOF.md) for the complete mathematical argument,
credited infinite/complement/rank premises, hypotheses and limits.
The extension is independently unreviewed and unformalized. The
parent audit9807 has a separate, expressly limited scope.

From a complete checkout of the authorized repository:

```sh
cd round-two/six-downset-3/core-edge-six-cutoff
python3 validate.py --receipt /tmp/core-six-validation.json
sha256sum -c SHA256SUMS
```

Tested with CPython3.12.14, standard library only. A sparse checkout
must also include the mandatory sibling files
`small-deletion-boundary/literal.py` and `triangle-majority/exact.py`.
[INPUTS.json](INPUTS.json) gives their full byte pins and actual
defining commits; [source_pins.py](source_pins.py) checks both before
either import. Copied credited routines and every full defining proof
are documented in [PROVENANCE.json](PROVENANCE.json). No parent
verifier or CAS/solver package is imported.

Fourteen serial normal/optimized phases must agree with the entire
[RESULT.json](RESULT.json), including the thirteen semantic damages.
Expected complete mathematical record SHA256:

```text
15df43a80a2e40baf1cbb432e67454c46a950e18d8516f28038aa75d8bf3bdcb
```

The measured [VALIDATION.json](VALIDATION.json) records all phase
times, exact phase hashes, coverage and resource limits. Each child
has the original60s limit, all native thread variables1; records are
temporary and only an explicitly named receipt is saved. A failed
check or timeout stops validation without implying nonexistence.

Coverage: all718072 negative original ordered positions,321221
positive nonempty positions and322825 whole positive positions.
At q22/q23 the lower and cap endpoint ranks are386/415 respectively,
with whole projected unit gaps at least1/20774912 and1/22478848.
Both exact PSD/rank algorithms check the fixed-space endpoints and
physical floors. Their shared author/table is not independent review;
the whole omitted complement is covered by the written credited
bridge, not by enumeration of sampled directions.
