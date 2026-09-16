# Four-contact mixed-depth Moser reflection stop

This package exactly decides one predeclared mixed-depth whole composition
from the independently accepted 115-point Moser-reflection stage. It does
**not** produce a five-chromatic graph and does not improve the published
509-point record.

## Frozen construction

Let `S1` be the accepted 115-point/447-edge support. For any exact finite
support `X`, reconstruct its complete unit graph and every reflected point

```text
z = p + q - r,
```

where `p != q` are unit neighbours of `r`. Define `F4(X)` to add exactly
those genuinely new collision-merged candidates having at least four
distinct unit neighbours in `X`, with the entire old neighbourhood measured
by exact distance tests rather than only by the generating route.

Before any point count or colouring computation, the sole construction was
frozen as

```text
A0 = S1,
A1 = F4(A0),
A2 = F4(A1).
```

The threshold is forcing-semantic: a new vertex with four old neighbours
blocks any old colouring which uses all four colours on those neighbours.
The second selective step couples the first-step blockers. No other
threshold, depth, subset, phase, or source was tested.

## Exact result

All coordinates lie in
`Q(sqrt(3),sqrt(11))^2` with coefficient denominator 12. Exact collision
merging and fresh all-pairs reconstruction give:

| support | points | complete unit edges | new points retained |
|---|---:|---:|---:|
| `A0` | 115 | 447 | -- |
| `A1` | 214 | 1,019 | 99 |
| `A2` | 382 | 2,026 | 168 |

This is not the accepted 398-point full stage in disguise. Exactly 342 of
the 382 points lie in that stage: `A2` omits 56 full-stage points and contains
40 depth-three points outside it. The final graph is connected and has no
articulation vertex or bridge.

The complete 382-point graph has the literal proper four-colouring in
`certificate.json`. Its first 115 symbols are a proper complete colouring of
`A0`, so this is an explicit surviving source input. Therefore the required
zero-extension property over the entire source-colouring set is false. This
existential witness decides the pass gate; enumerating every other source
colouring could not restore zero extensions and is not claimed.

The embedded seven-point Moser spindle has 11 edges and no proper
three-colouring, so the final graph has chromatic number exactly four. The
predeclared stop fires, and the Moser-reflection source is retired without a
second mixed-depth architecture.

## Reproduce

CPython 3.11+ and only the standard library are required. From this directory:

```sh
python3 -B verify.py --check-expected
python3 -B controls.py
python3 -O -B verify.py --check-expected
python3 -O -B controls.py
tmpfile=$(mktemp /tmp/hn-moser-f4.XXXXXX)
rm "$tmpfile"
python3 -B produce.py --out "$tmpfile"
python3 - "$tmpfile" <<'PY'
import json, pathlib, sys
assert json.loads(pathlib.Path(sys.argv[1]).read_text()) == json.loads(pathlib.Path("certificate.json").read_text())
print("CERTIFICATE_REGEN_OK")
PY
sha256sum -c SHA256SUMS
```

`verify.py` does not import the producer model. It uses a nested quadratic-pair
field representation, reconstructs all candidates, checks both defining
contacts of every reflection route, applies the four-contact predicate from
scratch, rebuilds every unit edge, and validates the literal colouring.

## Scope

This is exact author-side negative evidence for only the displayed `F4(F4(S1))`
support. It is not a theorem about arbitrary selective reflection closures,
other thresholds or depths, and it does not classify the full source-colouring
relation. The accepted 398-point full stage and 1,020-point next round remain
hard boundaries rather than prompts for partial-round searches.
