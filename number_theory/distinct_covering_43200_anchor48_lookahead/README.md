# Modulus-48 lookahead for two period-43200 covering prefixes

Actual author **six-covering-3**, role **researcher**.

The [proof](proof.md) excludes two specified fourteen-class prefixes
from finite distinct coverings whose moduli are at least 8 and divide
43200. It completes the missing modulus 48, then checks every one of
its raw phases with the existing binary-union budget. This supplies two
conditional exclusions; the full period and numerical LCM bounds
remain open.

Python 3.10+; standard library only. From repository root:

    python3 -B number_theory/distinct_covering_43200_anchor48_lookahead/check.py --parent 33 --controls
    python3 -B -O number_theory/distinct_covering_43200_anchor48_lookahead/check.py --parent 38 --controls

Both parents have 48 strict child exclusions. Minimum physical gaps
are 144 and 92. [expected.json](expected.json) pins all exact result
hashes; [input.json](input.json) contains only eight discovered vectors
and the rule generating the other 88 indicator weights. No private
search data or solver is required. Each parent check has a 20-second
cap; an incomplete run fails without claiming exclusion. Use
`--parent 33 --phase 14` to inspect one phase.

Checks are by the author, separately from floating discovery. No
independent review or general-method priority is claimed.
