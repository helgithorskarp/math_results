# Receiving interface

Use INPUTS.json to identify the exact F20 and F22 inputs; use TASKS.json for
all 260 physical children and their statuses. Reproduce before relying on
the patch. The three proof cores are independently checked against those
original files, so no historical partial trace needs to be shipped.

F20 gains clause [139,156], closing 63 children and retaining 67 UNKNOWN.
F22 gains [121,155] and [121,148], closing 36 children and retaining 94
UNKNOWN. In 29 residual F22 children with variable 121 false, variable 148
is forced true. Every retained task is emitted by interface.py from its
byte-pinned parent, preserving the entire full physical formula.

Do not infer a decision of either parent, any complete h3887 task, or a
Ramsey lower bound. Do not multiply this count by any older carrier count.
This gate recovers certificate evidence from existing runs; it does not
establish a solver speedup. The older raw proof streams and UNKNOWN logs
remain untouched. No solver was restarted. Physical completion of the
161 residual tasks remains with team-r55-1.

The original gate and both full trace scan summaries are preserved in
GATE.json and SCAN_SUMMARY.json. The unused wider candidates and the first
weaker F20 trial were not promoted to mathematical claims. Stop at this
physical interface; no width increase or adjacent trace source belongs to
this gate.
