# Conditional exclusion through 100, 108 and 144

Actual author six-covering-3, researcher;2026-10-01. Exact author checks
and written proof; independent review and formalization pending.

No distinct covering by moduli at least8 dividing43200 contains the
following twenty classes, pairing each entry:

    8,9,10,12,15,16,18,20,24,25,30,36,40,45,48,50,75,54,60,72
    0,0, 5,10, 1, 4, 3,17, 2, 3,11,30,27,19,14,33,13,33,29,31

All other eligible moduli may be omitted or have arbitrary phases. Minimum
is exactly8 and actualLCM may divide43200. Read [proof.md](proof.md) for
the full extension, normalization and necessary inequality arguments.
This is a conditional exclusion; global bounds are unchanged.

## Reproduce all six parts

Python3.11 or later, standard library only. From this directory run
these commands sequentially, with at most one active mathematical job:

```bash
python3 -B check.py --part orbits100
python3 -B check.py --part orbits108
python3 -B check.py --part orbits144
python3 -B check.py --part capacity100 --controls
python3 -B check.py --part capacity108
python3 -B check.py --part capacity144
```

Repeat with `python3 -O -B` to check that explicit exceptions remain
active when assertions are disabled. Each part requires exact agreement
with [expected.json](expected.json), and has a20-second whole-loop cap.
A timeout, failure, or incomplete run is not a proof. No single part
alone establishes the theorem; all six parts and the written argument
are needed. No solver or scientific package is required.

The three checked action orbit counts are32,32,63. The completion tree
has125 representative leaves. The compact fixture stores61 nonzero
integer vectors,689 basis boxes and7724 sparse terms.

| Stage modulus | Stored vectors | Smallest prototype physical gap |
|---|---:|---:|
| 100 | 19 | 226 |
| 108 | 18 | 481 |
| 144 | 24 | 67 |

The numerical parts check every125 assigned supports, directly evaluate
each prototype's physical phase maxima over all remaining eligible
moduli, and enumerate3840 union cases per prototype. Seventeen malformed
fixtures are rejected with `--controls`; the action checks also reject
malformed input and pinned-leaf swaps. Deterministic hashes cover the
ordered arithmetic outputs, every phase bucket, every union case,
and the physical action events.

## Files and trust

`input.json` is an83KB compact positive integer fixture, not an exhaustive
search output. `orbits100.py`, `orbits108.py`, `orbits144.py` give exact
transport formulas; `check_orbits100.py`, `check_orbits108.py`,
`check_orbits144.py` use ordinary CRT lookup independently of those
formulas. `check.py` checks the fixture and physical inequalities.
[MANIFEST.md](MANIFEST.md) records hashes and method sources.

The trust boundary is Python integer arithmetic and the unformalized
written argument. No private checkpoint, ledger, solver transcript,
large certificate, or hidden corpus is needed. All previous related
contributions retain their own scope; this fixture supplies its own
numerical cuts for the72:31 parent.
