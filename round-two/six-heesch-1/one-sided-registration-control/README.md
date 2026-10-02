# One-sided registration control: a21-cell tile with Hc=Hh=1

Author **six-heesch-1**, role **researcher**. An exact certificate for one
selected two-cell edit: no floating contact can occur around a covered copy.
The prior half-grid theorem therefore registers every corona layer, including
the last one, to the root grid. A checked first disc has seven copies; a
complete necessary second-corona model has an uncovered cell at (0,11).
The resulting unrestricted Heesch values are exactly one, and plane tiling
is excluded. This is a calibration/reduction, not a record or priority claim.
Independent review is pending.

Read [proof.md](proof.md) for the written motion bridge and precise scope.
[input.json](input.json) contains the literal 21 cells, integer support
certificates, the necessary first prefix and the obstruction cell.
[floating-support.rup](floating-support.rup) is the 2,470-byte trace proving all
352 floating exclusions against an independently rebuilt half-grid formula.
The selected 1,200 mutation window itself is not published or classified here.

From the repository root, with CPython 3.11+ and the standard library:

```
python3 round-two/six-heesch-1/one-sided-registration-control/check.py
python3 -O round-two/six-heesch-1/one-sided-registration-control/check.py
```

Both runs must produce [expected.json](expected.json). The two byte-pinned
source dependencies are in [dependencies.json](dependencies.json). Guards
raise incomplete-check errors; a native solver status is never a proof.
The general one-sided implication is an elementary corollary of the credited
finite-contact and half-grid arguments; the new content is this literal
control certificate and its complete all-motion exclusion.
