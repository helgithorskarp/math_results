# Review of the Gaussian contact reduction

[REVIEW.md](REVIEW.md) accepts the stated first-contact equivalence in
researcher 1's [source](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md),
with no correction required. It checks critical levels, unbounded-input
posterior formulas, both volume boundaries, failure-preserving smoothing,
and transversality even when the minimizing volume is not unique.
The full conjecture and the required contact-flux sign remain open.

This is an analytic review by the functional/stability lane, which authored
one cited homothety precursor. It is separate from authorship of the contact
reduction, but is not independent of the whole dependency tree or external
human peer review. No Gaussian sign computation or formalization is claimed.
The sensitive steps have written derivations, including an elementary
one-dimensional critical-image argument valid for the Lipschitz envelope.
[REVIEW_SCOPE.json](REVIEW_SCOPE.json) records the exact verdict
and limitations; [INPUTS.json](INPUTS.json) pins all source versions and hashes.

The reviewed target is commit
`1d1f1c6e58ceb3010e05dcbe5fc477f4c7edde6f`, whose CONTACT_REDUCTION.md hash is
`949e497add957be5998b6653898308b4df888cf4403111a800392bd053de2c79`.
No reviewed proof file has been changed by this audit.

From this directory, verify the review packet with:

```sh
sha256sum -c SHA256SUMS
```

The following standard-library Python command checks each pinned input
against the corresponding committed blob, even if the current branch later
changes. It verifies provenance, not mathematical truth:

```sh
python3 - <<'PY'
from pathlib import Path
import hashlib, json, subprocess
repo = Path('../..').resolve()
for row in json.loads(Path('INPUTS.json').read_text()):
    blob = subprocess.check_output(
        ['git', 'show', row['source_commit'] + ':' + row['path']], cwd=repo)
    if hashlib.sha256(blob).hexdigest() != row['sha256']:
        raise RuntimeError('Pinned source mismatch: ' + row['path'])
print('CONTACT_REVIEW_PINNED_INPUTS_PASS')
PY
```

All evidence is compact written source. The prior author's finite audit is
not replayed or counted as an independent check of universal analysis.
Standard analytic inputs and the primary problem source are credited in
[SOURCES.md](SOURCES.md). The useful output is a reviewed reduction with
its remaining sign obligation isolated, not an additional sufficient class.
