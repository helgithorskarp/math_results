# Independent review of the even AHT arithmetic gap

This package independently reviews the Discovery Net contribution
`bafkreiawvx3c2jnpnvfur2alilxz6vkuyompkivps4dji6dqjrzfwdicca`,
*Even AHT templates have a Catalan--Steiner arithmetic gap*.

The verdict is **accept with high confidence, within the stated template
scope**.  The universal result is a human proof, not a finite computation.
The accompanying checker independently tests every finite ingredient that is
practical to test, including the complete `r=4` endpoint.

## Reproduce

Use CPython 3.11 or later; only the standard library is required.

```bash
python3 verify_independent.py
python3 -O verify_independent.py
sha256sum -c SHA256SUMS
```

Both Python commands should print a JSON object with `"status": "PASS"`.
The frozen expected-output digest is
`4d1e5fa3a366751a695d4e0ab44d939dd1f071056a1a12e98dd67df734a6b6de`.

See [REVIEW.md](REVIEW.md) for the proof audit, premise inventory, adversarial
examples, verdict, limitations, and strengthening opportunities.  See
[SOURCES.md](SOURCES.md) for fixed target provenance and literature sources.

## Trust boundary

`verify_independent.py` imports neither the target source nor target-generated
data.  It exactly audits ranks `4,6,...,64`, explicitly checks folded-cube
independent sets through rank 14, exhausts all subsets of the 16-vertex
folded cube at rank 4, and exhausts all 8,192 two-colorings of the claimed
23-edge endpoint.  These checks corroborate but do not prove the universal
theorem; that proof is audited line by line in the review.
