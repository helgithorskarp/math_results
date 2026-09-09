# Factor-clean bridge for the three-wheel residual frontier

This package closes the exact interface between h4091's real-root
classification and h4085's complete colour cover for

```text
S(u,v) = W + uW + vW,       |u|=|v|=1,
```

where `W` is the seven-point hexagonal wheel.  It performs no SAT calls and
searches for no new colour word.

The 15 injective algebraic components on which h4091's original thirteen
words all fail have 48 real embeddings.  For each component, the verifier
evaluates all 972 nonalignment event factors in its exact quotient
`Q[t]/(m)`.  In every case, the only factors that are not units are exactly
the component's two defining factors.  This is checked by 14,580 rational
polynomial gcds.

Consequently every real embedding in one component has the same labelled
343-vertex unit-edge graph.  The 48 embeddings therefore give exactly 15
distinct labelled edge sets (no assertion about abstract isomorphism between
different labelings is needed).  Their edge counts lie from 1,791 to 1,881.

On a factor-clean component, one of h4085's fixed words is proper exactly
when its bad-factor set avoids the defining pair.  Among the 62 h4085 words,
the minimum component-uniform cover size is four.  There are exactly three
minimum covers, with zero-based word indices

```text
18 24 34 40
24 31 34 40
24 31 40 47
```

The first is the canonical cover in `certificate.json`; it assigns all 15
components and all 48 embeddings using respectively `5,3,6,1` components and
`16,10,18,4` embeddings.  Exhaustive enumeration of every one-, two-, three-
and four-word subset proves both minimality and the complete list above.

This is a terminal reduction and cross-certificate for the shared three-wheel
architecture.  It independently checks h4085's fixed words on h4091's
survivor fields by a different exact representation, but it does not replace
h4085's proof for the other 1,007 real embeddings/alignment cases.  Together
with the now independently accepted h4085 theorem, the architecture has zero
unresolved candidates and yields no five-chromatic unit-distance graph.  The
[reviewer-1 package](../hadwiger_nelson_three_wheel_closure_review1) gives the
independent acceptance and exact-rational replay.

The comparison baseline was refreshed on 2026-09-09.  Haugland's August 2026
[primary paper](https://arxiv.org/abs/2608.04542) still identifies Parts's 509
vertices as the current record; Parts's original
[minimization paper](https://arxiv.org/abs/2010.12665) gives the 509-vertex,
2,442-edge construction.  This package does not improve it.

## Verification

From this directory, using CPython 3.11.2:

```bash
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py
```

The verifier uses only the Python standard library.  To replay h4091's full
800-system classification before checking this bridge:

```bash
python3 -B verify.py --full-dependency-replay --check-expected
```

The optional producer uses SymPy 1.14.0:

```bash
python3 -m pip install -r requirements.txt
python3 -B produce.py --output /tmp/three-wheel-factor-clean.json
cmp /tmp/three-wheel-factor-clean.json certificate.json
```

The published certificate is 6,963 bytes with SHA-256
`0897f1c7a0af1ef16c295e2816fbc4d06467e0881f09120d750478a259d51003`.
See [PROOF.md](PROOF.md) for the exact argument and [DEPENDENCIES.json](DEPENDENCIES.json)
for the pinned source boundary.
