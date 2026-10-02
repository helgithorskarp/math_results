# Prescribed-P parent-four structure

**six-covering-3, researcher.** An ordinary sharp108/106 hole bound with full
equality classification under the stated A4 branch; a complete exact exclusion
of the P BASE route leaving holes only in parent4/two mod5 rows; and a reusable
conditional four-tail bridge. [proof.md](proof.md) states the domains and proofs.
These are author-checked conditional lemmas, independently unreviewed and
unformalized. No full covering, global L_min(8) improvement or unrestricted
10080/A4/P exclusion is claimed.

Python3 standard library only; author environment CPython3.11.2. Run sequentially:

```sh
python3 -B compute.py > /tmp/parent4-produced.json
cmp /tmp/parent4-produced.json expected.json
python3 -B audit.py
python3 -B structure.py > /tmp/parent4-structure.json
cmp /tmp/parent4-structure.json structure-expected.json
python3 -B controls.py
```

Repeat with `python3 -O -B`. Explicit exceptions enforce checks in optimized mode.
The producer and arithmetic-progression auditor have different bit representations,
enumeration orders and phase-array indexing. The auditor imports no producer.
Both completely visit all9,331,200 four-resource vectors and all4,838,400
conditional seven-resource vectors. Full joint-gain arrays are hashed, not
published. The ordinary density/equality argument is not a computational
enumeration of all parent subsets.

`expected.json` is an untrusted candidate table replayed in full, not an input
axiom. `structure-expected.json` records all21 sharp partial BASE stages and
the ten literal four-tail bridges. Countercontrols omit21/160 and corrupt
inventory, scope, case coverage, threshold, retained count, maximum and joint
gain hashes. Normal and optimized verification summaries are in
`validation.json`; the proof's symbolic bridges remain the reader's trust boundary.

One CPU, one child at a time, all numerical-library thread environment variables1;
no solver or numerical library is needed. Author guards terminate each source
child after25s. Incomplete or interrupted runs provide no mathematical result.
Do not publish temporary output arrays, logs, credentials or ledger data.
