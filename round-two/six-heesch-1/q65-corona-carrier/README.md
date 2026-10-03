# A fresh Q65 polyomino carrier

six-heesch-1, researcher. Four complete disc coronas are checked for the
literal unmarked 65-cell shape, and a seven-copy conditional core blocks a
fifth from the displayed arrangement by arbitrary motions. Finiteness and
any exact Heesch value remain unproved; the finite-five target remains open.

The [proof](PROOF.md) states the two scopes. [four-coronas.json](four-coronas.json)
contains the construction, [obstruction.json](obstruction.json) the conditional
core. Run `python3 check.py` and then `python3 -O check.py` serially from this
directory. Standard library only, Python>=3.10. [expected.json](expected.json)
is the complete stable evidence; the reader imports only the local lower.py.

The source mask was discovered through a bounded family around Kaplan's known
17-omino index43. Positive geometry is checked directly; no heuristic absence
or period-search failure is used as a mathematical upper.

Next: construct a fourth that avoids the seven-host core, try a fifth, and
seek a separate shape-wide finite obstruction. No independent review or
formal proof is claimed. Published prior broad-polyform finite-five results
are acknowledged in the proof and remain distinct from this polyomino work.
