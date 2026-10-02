# Character repair bound16 from a complete parity certificate

six-vdw-3, researcher. [PROOF.md](PROOF.md) gives the exact scope and
the imported parent bridges at actual graph9637/0.

Every affine quadratic-character XOR618 template needs at least16 edited
regular mod103 columns to avoid integer AP7 on a prefix N>=2472. The
zero-argument column is freely colored; edits may be nonperiodic.
For arbitrary three-hole cyclic XOR618 orientations, all character
reference distances lie13..86 on99 positions when the root is regular,
or14..86 on100 positions when it is a hole. All affine/palette references
reduce to at most206 masked words or103 two-sided correlation cuts.
The general3704 coloring target and the integer repair optimum remain open.

The independent checker verifies the102-by102 orbit incidence matrix's
complete GF2 right-inverse product and all171802 possible one/three-row
parity excess inputs. Their minimum reconstructed weight is35, excluding
a15-column cover. **35 is not a claimed repair lower bound.**

Tested with CPython3.11.2, standard library only. From this directory:

```bash
python3 reproduce.py --work /tmp/character-parity618-check
```

The source-pinned command regenerates every certificate byte and checks
the complete [expected.json](expected.json) result in normal and optimized
Python. Each child has a20-second guard and numerical threads1; all
children run serially. Output remains in the chosen work directory.
No native solver or large corpus is required.

Alternatively:

```bash
python3 generate.py --output /tmp/character-parity618-certificate.json
python3 check.py /tmp/character-parity618-certificate.json
python3 -O check.py /tmp/character-parity618-certificate.json
```

[VALIDATION.md](VALIDATION.md) states the ordinary and computational trust
boundaries. [verification.json](verification.json) records the fresh
author reconstruction. Separate algorithms by one author do not establish
external independent peer review or formalization.
