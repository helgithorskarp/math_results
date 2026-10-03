# Thirteen-input LOW(3,4), two-binary exclusion

**six-sorting-2, researcher**, 2026-10-03. Complete conditional author proof;
independent-person review and formalization pending.

For the literal 28-comparator Q in [PROOF.md](PROOF.md), no completion
within 44 total gates can have its first strict ordinary two-LOW increase
a singleton, with no further preceding LOW binary and with its intervening
preparation having zero third-HIGH singletons and exactly two third-HIGH
binaries. Arbitrary repeated preparations and suffix depth are covered.
The proof also reduces the full stipulated LOW route to at most six
singleton separators, five binaries, and function blocks on at most five
physical inputs. The full route and unrestricted 44-versus-45 gap remain open.

Run with Python 3.11 (tested CPython 3.11.2), standard library only:

```
cd round-two/six-sorting-2/high3-low34-two-binary-exclusion
python3 run.py
```

`run.py` runs one child at a time, first in normal mode and then under
`-O`, with 45-second guards. It reconstructs the entire cover and checks
all 113 prefix functions, 1030 negative bindings, and 2034 head/tail
alternatives. The expected whole mathematical-record SHA256 is
`74e205f813a1ef8acfdcf4c2d494789f0e4b62f74fcafd17656c52d61cd9f22a`.
It compares the complete normal/optimized records. On the recorded host
the fresh source-only run took 121.22 seconds, with maximum child 10.53
seconds and peak scalar RSS 82136 KiB. A timeout means incomplete.

`cover.py` rebuilds original ground domains, the 150 two-binary words,
the seven early obstructions, the two-port function semigroup and the
113 actual-Q function classes. `verify.py` separately checks every actual
negative binding on the whole selected original cube, all heads and
whole tail functions, 98 intended damages per mode, and positive controls.
`numeric.py` credits verbatim generic primitives from an earlier public
result, but imports no earlier context or certificate. `fixture.json`
contains the literal Q, known 45-sorter and provenance. `certificate.json`
is the compact complete witness interface. Full generated rows, logs and
run records remain in ignored `generated/`; no private input is required.

See [PROOF.md](PROOF.md) for ordinary arbitrary-word coverage and the four
certificate implications, [checks.json](checks.json) for frozen validation,
and [SOURCE-CREDITS.md](SOURCE-CREDITS.md) for imported literature and code.
