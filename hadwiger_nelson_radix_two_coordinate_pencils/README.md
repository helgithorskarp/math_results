# The two-coordinate five-pencil subset is impossible

For the shared A5(z) architecture, none of the **6,912 curve quintets** in the
**54 realized two-coordinate affine pencils** has a common complex affine
parameter. The exclusion remains valid inside larger active sets. This is a
complete decision on the h4171 support profile `(1,1,2,2,2)`.

The 6,912 lifts normalize to 32 coefficient patterns. A compact certificate
checks 33 exact polynomial identities. Thirty-one patterns contradict their
unit-distance anchors; the last forces equal distinct radix powers of squared
modulus 1/4, which is impossible. [PROOF.md](PROOF.md) gives the argument,
including the exceptional free-vector solutions that must not be discarded.

The result moves **192 pair systems** out of the exact-five mode. They remain
in the six-or-more-active frontier. No global pair is deleted and no record
graph is established. The [HN3 handoff](HANDOFF.md) gives exact updated counts
and regenerable exclusion/mode interfaces.

From the repository root, with CPython 3.11.2 or later:

```sh
python3 -B hadwiger_nelson_radix_two_coordinate_pencils/verify.py --check-expected
python3 -O -B hadwiger_nelson_radix_two_coordinate_pencils/verify.py --check-expected
python3 -O -B hadwiger_nelson_radix_two_coordinate_pencils/controls.py
```

Verification requires only the standard library and committed predecessor
source. Expected output is in `EXPECTED.json`. The verifier reconstructs the
finite cover by masks on F4², independently of the producer's affine-span
construction, then checks every coefficient of every identity in Q(ω).

Optional fresh generation uses SymPy 1.14.0 (with python-flint 0.8.0 in the
tested environment):

```sh
python3 -B hadwiger_nelson_radix_two_coordinate_pencils/produce.py --out /tmp/hn-two-coordinate-certificate.json
cmp /tmp/hn-two-coordinate-certificate.json hadwiger_nelson_radix_two_coordinate_pencils/certificate.json
```

The output path must not exist. The 13,081-byte certificate has SHA-256
`2cee23437feab03d5cfbbeaa87b909fb1a4215194bf649daa523ab31bf84ed21`.
All normal forms and normalization transcripts agree entrywise between
producer and verifier; normal and optimized verification agree. These are
author-side implementation checks, pending independent reviewer-1 assessment.
